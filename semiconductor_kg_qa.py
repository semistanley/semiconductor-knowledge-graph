"""
半导体制造知识图谱问答系统
================================
该脚本提供了一个命令行界面，允许用户用中文自然语言提出问题，
系统会自动将问题转换成 Neo4j 的 Cypher 查询语句，执行查询，
并基于查询结果调用大语言模型（DeepSeek）生成最终的中文答案。

你会看到两种回答模式：
- graph_rag_directed_expanded：图谱查到证据，且做了“定向扩展子图”，适合回答为什么/怎么办/推荐
- llm_only_no_graph_result：图谱查不到证据，直接用大模型通用知识回答

环境依赖：
- neo4j>=5
- openai

使用方法：
1) 安装依赖：pip install neo4j openai
2) 打开 semiconductor_kg_qa.py，把文件顶部的 DEEPSEEK_API_KEY 替换成你的密钥
3) 运行：python semiconductor_kg_qa.py
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Dict, List

from openai import OpenAI
from neo4j import GraphDatabase, Driver

import settings

settings.validate_llm_config()
settings.validate_neo4j_config()

NEO4J_URI = settings.NEO4J_URI
NEO4J_USER = settings.NEO4J_USER
NEO4J_PASSWORD = settings.NEO4J_PASSWORD
DEEPSEEK_API_KEY = settings.DEEPSEEK_API_KEY
DEEPSEEK_API_BASE = settings.DEEPSEEK_API_BASE

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_BASE)

if not settings.DEEPSEEK_SKIP_HEALTHCHECK:
    try:
        _r = client.chat.completions.create(
            model=settings.DEEPSEEK_MODEL,
            messages=[{"role": "user", "content": "回复我一个：OK"}],
            temperature=0,
            max_tokens=10,
        )
        print("DeepSeek连通性测试：", (_r.choices[0].message.content or "").strip())
    except Exception as _e:
        print("DeepSeek连通性测试失败：", repr(_e))
        raise
else:
    print("DeepSeek连通性测试已跳过（DEEPSEEK_SKIP_HEALTHCHECK=1）")


# ---------------------------------------------------------------------------
# 同义词/别名映射（用于提升中文口语问题的命中率）
# ---------------------------------------------------------------------------
SYNONYM_MAP: dict[str, str] = {
    # 材料
    "氮化钛": "TiN",
    "钛氮化物": "TiN",
    "二氧化硅": "SiO2",
    "氧化硅": "SiO2",
    "氮化硅": "Si3N4",
    "碳化硅": "SiC",
    "氧化铪": "HfO2",
    "三氧化二铝": "Al2O3",
    "氧化铝": "Al2O3",
    "氧化锆": "ZrO2",
    "铝": "Al",
    "铜": "Cu",
    "钨": "W",

    # 常见工艺/技术缩写
    "物理气相沉积": "PVD",
    "化学气相沉积": "CVD",
    "原子层沉积": "ALD",

    # 方法
    "磁控溅射": "磁控溅射",
    "溅射": "溅射",
    "蒸镀": "蒸镀",
    "等离子体增强化学气相沉积": "PECVD",
    "低压化学气相沉积": "LPCVD",
    "常压化学气相沉积": "APCVD",
    "金属有机化学气相沉积": "MOCVD",
}


def normalize_query(text: str) -> str:
    """把用户问题做一轮同义词替换/归一化，提升图谱检索命中率。"""
    if not text:
        return text

    normalized = text
    for k, v in SYNONYM_MAP.items():
        if k in normalized:
            normalized = normalized.replace(k, v)
    return normalized



# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------
@dataclass
class QueryResult:
    cypher_query: str
    result: List[Dict]
    execution_time: float
    source: str = "knowledge_graph"


# ---------------------------------------------------------------------------
# 核心系统
# ---------------------------------------------------------------------------
class 半导体知识图谱系统:
    """将自然语言问题映射到知识图谱并生成答案（支持定向扩展，用于复杂推理/决策）"""

    def __init__(self) -> None:
        self.driver: Driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
        self.cache: dict[str, str] = {}

    def 自然语言转_cypher(self, 问题: str) -> str:
        """调用 LLM 将自然语言转换成 Cypher"""
        cache_key = f"nl2cypher:{问题}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        prompt = self._build_nl2cypher_prompt(问题)

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
        )
        cypher_query: str = (response.choices[0].message.content or "").strip()
        cypher_query = re.sub(r"^```[a-zA-Z]*|```$", "", cypher_query, flags=re.IGNORECASE).strip()
        self.cache[cache_key] = cypher_query
        return cypher_query

    def 执行_cypher查询(self, cypher_query: str, params: dict | None = None) -> QueryResult:
        开始 = time.time()
        with self.driver.session() as session:
            结果 = session.run(cypher_query, parameters=params or {})
            records = [dict(record) for record in 结果]
        return QueryResult(cypher_query=cypher_query, result=records, execution_time=time.time() - 开始)

    def 直接用大模型回答(self, 问题: str) -> str:
        """图谱无证据时的兜底回答：更像自然语言解释，不做大段列举。"""
        prompt = (
            "你是半导体制造领域的中文问答助手。\n"
            "请直接基于通用知识回答，不要在核心结论里出现“根据知识图谱”“证据”或“图谱未提供/图中没有”等措辞。\n\n"
            "要求：\n"
            "- 先用一段话给出最核心结论（不要罗列太多条目，且不要出现“知识图谱/证据/图中没有”等措辞）。\n"
            "- 再用一小段解释原因/原理（如需可在括号中简短标注依据）。\n"
            "- 最后给 3 条以内可执行建议（用短句）。\n"
            "\n"
            f"用户问题：{问题}\n"
        )

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        return (response.choices[0].message.content or "").strip()

    def _extract_keywords(self, 查询结果: QueryResult) -> List[str]:
        keywords: List[str] = []
        for row in 查询结果.result[:30]:
            if not isinstance(row, dict):
                continue
            for k in [
                "source_name",
                "technology_name",
                "material_name",
                "equipment_name",
                "method_name",
                "submethod_name",
                "name",
            ]:
                v = row.get(k)
                if isinstance(v, str) and v.strip():
                    keywords.append(v.strip())

        seen = set()
        keywords = [x for x in keywords if not (x in seen or seen.add(x))]
        return keywords[:5]

    def _expand_subgraph(self, 查询结果: QueryResult) -> QueryResult:
        kws = self._extract_keywords(查询结果)
        if not kws:
            return QueryResult(cypher_query="// no directed expansion", result=[], execution_time=0.0)

        cypher = """
        UNWIND $kws AS kw
        MATCH (n)
        WHERE toLower(n.name) CONTAINS toLower(kw) OR toLower(n.description) CONTAINS toLower(kw)

        OPTIONAL MATCH (n)-[r1:NEED_EQUIPMENT|HAS_PARAMETER|HAS_ABILITY|USED_FOR|USED_IN|HAS_ACTION]->(m1)
        WHERE (n:Technology OR n:Method OR n:SubMethod)

        OPTIONAL MATCH (n)-[r2:HAS_PARAMETER|USED_IN]->(m2)
        WHERE (n:Material)
        OPTIONAL MATCH (t2:Technology)-[r2b:EFFICIENT_PRECIPITATION]->(n)
        WHERE (n:Material)

        OPTIONAL MATCH (n)-[r3:MEASURES|ENABLES|USED_FOR|USED_FOR_ANALYSIS]->(m3)
        WHERE (n:Equipment)

        OPTIONAL MATCH (n)-[r4:MANUFACTURED_IN|USED_IN|MADE_FROM]->(m4)
        WHERE (n:ChipStructure OR n:ManufacturingStage)

        RETURN
          labels(n) AS n_labels, n.name AS n_name,
          collect(DISTINCT {rel:type(r1), desc:r1.description, m_labels:labels(m1), m_name:m1.name, m_desc:m1.description}) AS tech_method_edges,
          collect(DISTINCT {rel:type(r2), desc:r2.description, m_labels:labels(m2), m_name:m2.name, m_desc:m2.description}) AS material_edges,
          collect(DISTINCT {rel:type(r2b), desc:r2b.description, t_name:t2.name}) AS material_supported_by,
          collect(DISTINCT {rel:type(r3), desc:r3.description, m_labels:labels(m3), m_name:m3.name, m_desc:m3.description}) AS equipment_edges,
          collect(DISTINCT {rel:type(r4), desc:r4.description, m_labels:labels(m4), m_name:m4.name, m_desc:m4.description}) AS structure_stage_edges
        LIMIT 20
        """.strip()

        开始 = time.time()
        with self.driver.session() as session:
            res = session.run(cypher, kws=kws)
            records = [dict(rec) for rec in res]

        return QueryResult(cypher_query=cypher, result=records, execution_time=time.time() - 开始)

    def 生成_回复(self, 问题: str, 查询结果: QueryResult) -> str:
        if not 查询结果.result:
            return "【图谱未检索到证据】"

        结果文本 = "\n".join([str(r) for r in 查询结果.result[:10]])

        # 关键：要求“自然语言整合”，避免大段条目堆砌
        prompt = (
            "你是‘半导体制造知识图谱智能问答助手’。请严格基于【知识图谱查询结果】回答。\n\n"
            "输出要求（非常重要）：\n"
            "- 不要大段罗列。请先用1段自然语言把核心结论说清楚（像工程师给老板汇报那样），且不要出现“根据知识图谱”“证据”“图谱未提供/图中没有”等措辞。\n"
            "- 再用1段说明‘为什么’（把关键关系串起来讲清楚）。如需引用证据，仅在解释部分用括号简短标注（例如：ALD->NEED_EQUIPMENT->低温沉积系统）。\n"
            "- 最后给不超过3条‘怎么办/下一步’建议（每条一句话）。\n"
            "- 不要编造具体数值/型号；若某些细节图谱未覆盖，可直接基于通用知识补充回答，但避免给出未经验证的精确数值/型号；回答中不要出现“图谱未提供/图中没有”等表述。\n\n"
            f"用户问题：{问题}\n\n"
            "【知识图谱查询结果（确凿证据）】\n"
            f"{结果文本}\n"
        )

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=550,
        )
        return (response.choices[0].message.content or "").strip()

    def 处理问题(self, 问题: str) -> Dict:
        normalized_question = normalize_query(问题)
        query_params = {}

        try:
            cypher_query = self.自然语言转_cypher(normalized_question)
        except Exception:
            kw = normalized_question.strip()[:80]
            query_params = {"kw": kw}
            cypher_query = (
                "MATCH (n) "
                "WHERE toLower(n.name) CONTAINS toLower($kw) "
                "OR toLower(n.description) CONTAINS toLower($kw) "
                "RETURN n.id AS id, n.name AS name, labels(n) AS type, n.description AS description LIMIT 20"
            )

        try:
            main_res = self.执行_cypher查询(cypher_query, query_params)
        except Exception as exc:
            ans = self.直接用大模型回答(normalized_question)
            return {
                "error": str(exc),
                "cypher": {"main": cypher_query, "expansion": None},
                "results": {"main": [], "expansion": []},
                "response": ans,
                "execution_time": 0.0,
                "mode": "llm_only_due_to_query_error",
            }

        if main_res.result:
            try:
                exp_res = self._expand_subgraph(main_res)
                llm_query = QueryResult(
                    cypher_query=f"{main_res.cypher_query}\n\n// DIRECTED EXPANSION QUERY:\n{exp_res.cypher_query}",
                    result=main_res.result + exp_res.result,
                    execution_time=main_res.execution_time + exp_res.execution_time,
                )
                ans = self.生成_回复(问题, llm_query)
                return {
                    "cypher": {"main": main_res.cypher_query, "expansion": exp_res.cypher_query},
                    "results": {"main": main_res.result, "expansion": exp_res.result},
                    "response": ans,
                    "execution_time": llm_query.execution_time,
                    "mode": "graph_rag_directed_expanded",
                }
            except Exception:
                ans = self.生成_回复(问题, main_res)
                return {
                    "cypher": {"main": main_res.cypher_query, "expansion": None},
                    "results": {"main": main_res.result, "expansion": []},
                    "response": ans,
                    "execution_time": main_res.execution_time,
                    "mode": "graph_rag_base_only",
                }

        ans = self.直接用大模型回答(normalized_question)
        return {
            "cypher": {"main": cypher_query, "expansion": None},
            "results": {"main": [], "expansion": []},
            "response": ans,
            "execution_time": main_res.execution_time,
            "mode": "llm_only_no_graph_result",
        }

    @staticmethod
    def _build_nl2cypher_prompt(问题: str) -> str:
        模式信息 = (
            "节点标签：Action/Technology/Method/SubMethod/Material/Capability/Equipment/ChipStructure/ManufacturingStage/Parameter\n"
            "节点属性：id/name/description\n"
            "常用关系：EFFICIENT_PRECIPITATION、NEED_EQUIPMENT、HAS_PARAMETER、HAS_ABILITY、USED_FOR、USED_IN、HAS_ACTION 等\n"
        )

        return (
            "你是‘半导体制造知识图谱Cypher生成器’，把中文问题转换为可执行的 Cypher。\n"
            "要求：\n"
            "- 只输出 Cypher，不要解释。\n"
            "- 尽量用 toLower + CONTAINS 对 name/description 做模糊匹配。\n"
            "- 优先返回结构化字段并起别名（AS）。\n\n"
            f"{模式信息}\n"
            f"用户问题：{问题}\n"
        )


    def simulate_impact(self, scenario: str) -> dict:
        """Supply chain shock: trace affected nodes and generate impact analysis."""
        try:
            cypher_query = self.自然语言转_cypher(scenario)
            main_res = self.执行_cypher查询(cypher_query)
        except Exception:
            main_res = QueryResult(cypher_query="", result=[], execution_time=0.0)

        keywords = self._extract_keywords(main_res) if main_res.result else []

        # BFS traversal: find all nodes 1-2 hops from affected nodes
        affected_nodes = []
        affected_edges = []
        if keywords:
            bfs_query = """
            UNWIND $kws AS kw
            MATCH (n)
            WHERE toLower(n.name) CONTAINS toLower(kw)
            WITH n LIMIT 3

            OPTIONAL MATCH (n)-[r1]-(m1)
            WHERE type(r1) IN [
              'NEED_EQUIPMENT','HAS_PARAMETER','USED_FOR','USED_IN',
              'EFFICIENT_PRECIPITATION','HAS_ABILITY','ENABLES','MADE_FROM'
            ]
            RETURN
              n.name AS source, labels(n)[0] AS source_label,
              type(r1) AS rel, m1.name AS target, labels(m1)[0] AS target_label
            LIMIT 50
            """
            try:
                with self.driver.session() as session:
                    res = session.run(bfs_query, kws=keywords[:5])
                    for rec in res:
                        affected_nodes.append({
                            "source": rec["source"],
                            "source_label": rec["source_label"],
                            "rel": rec["rel"],
                            "target": rec["target"],
                            "target_label": rec["target_label"],
                        })
            except Exception:
                pass

        # Classify impacts
        equipment_impact = [n for n in affected_nodes if n["rel"] == "NEED_EQUIPMENT"]
        material_impact = [n for n in affected_nodes if n["rel"] == "EFFICIENT_PRECIPITATION"]
        process_impact = [n for n in affected_nodes if n["rel"] in ("USED_FOR", "USED_IN")]
        all_affected = list(set(
            [n["source"] for n in affected_nodes] +
            [n["target"] for n in affected_nodes]
        ))

        # LLM analysis
        impact_text = ""
        if affected_nodes:
            summary = f"Total {len(affected_nodes)} impact paths, {len(all_affected)} nodes affected."
            eq_list = ", ".join(set(n["target"] for n in equipment_impact[:5]))
            mat_list = ", ".join(set(n["target"] for n in material_impact[:5]))
            proc_list = ", ".join(set(n["target"] for n in process_impact[:5]))

            prompt = (
                "You are a semiconductor supply chain analyst. Analyze this shock scenario:\n"
                f"Scenario: {scenario}\n"
                f"Graph found {summary}\n"
                f"Affected equipment: {eq_list}\n"
                f"Affected materials/tech: {mat_list}\n"
                f"Affected processes: {proc_list}\n\n"
                "Provide a structured analysis with exactly 3 sections:\n"
                "1. DIRECT IMPACT: which technologies/equipment/materials are directly affected\n"
                "2. CASCADE EFFECT: how the impact propagates downstream (2 sentences max)\n"
                "3. ALTERNATIVES: what substitute technologies or equipment exist\n"
                "Keep each section to 2-3 sentences. Be specific but concise."
            )
            try:
                resp = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                    max_tokens=400,
                )
                impact_text = (resp.choices[0].message.content or "").strip()
            except Exception:
                impact_text = summary

        return {
            "scenario": scenario,
            "affected_nodes": all_affected[:30],
            "affected_count": len(all_affected),
            "impact_paths": affected_nodes[:50],
            "equipment_impact": [{"equipment": n["target"], "affected_tech": n["source"]} for n in equipment_impact[:8]],
            "material_impact": [{"technology": n["source"], "material": n["target"]} for n in material_impact[:8]],
            "process_impact": [{"technology": n["source"], "process": n["target"]} for n in process_impact[:8]],
            "analysis": impact_text,
        }


def main() -> None:
    print("=== 半导体制造知识图谱问答系统 ===")
    print("输入 '退出' 结束\n")

    qa_system = 半导体知识图谱系统()

    while True:
        try:
            用户输入 = input("\n请输入您的问题: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if 用户输入.lower() in {"退出", "quit", "exit"}:
            print("感谢使用，再见！")
            break

        if not 用户输入:
            print("请勿输入空问题！")
            continue

        print("\n处理中，请稍候...\n")
        开始 = time.time()
        结果 = qa_system.处理问题(用户输入)
        用时 = time.time() - 开始

        print("=" * 60)
        if "error" in 结果:
            print(f"出错: {结果['error']}")
            print("=" * 60)
            continue

        print(f"问题: {用户输入}")
        print("-" * 60)
        print(f"回复: {结果['response']}")
        print("-" * 60)
        print(f"Cypher(main): {结果.get('cypher', {}).get('main')}")
        print(f"Cypher(expansion): {结果.get('cypher', {}).get('expansion')}")
        print(f"查询耗时: {结果['execution_time']:.2f}s  总耗时: {用时:.2f}s")
        print("=" * 60)


if __name__ == "__main__":
    main()
