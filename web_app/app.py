from __future__ import annotations

"""Flask Web App：半导体知识图谱平台（用户系统 + 持久化 + 自动归档 + KG 自动更新）"""

import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime
from typing import Any, Dict

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
WEB_APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if WEB_APP_ROOT not in sys.path:
    sys.path.insert(0, WEB_APP_ROOT)

from auth_utils import authenticate_user, get_current_user, login_required, register_user
from database import init_db
import settings
from models import ArchiveEntry, ChatMessage, DocumentRecord, GraphUpdateLog, UserCredit
from services import (
    apply_knowledge_graph_update,
    auto_archive,
    save_chat_message,
    save_document_record,
)
from semiconductor_doc_ingest import (
    extract_from_document,
    _sync_extraction_to_tech_data,
    _extract_json_block,
    _llm_fix_json,
    _llm_extract_triples,
    client as deepseek_client,
)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)
app.config["SECRET_KEY"] = settings.FLASK_SECRET_KEY
init_db(app)

_qa_system = None


def get_qa_system():
    global _qa_system
    if _qa_system is None:
        from semiconductor_kg_qa import 半导体知识图谱系统
        _qa_system = 半导体知识图谱系统()
    return _qa_system


@app.get("/login")
def login_page():
    if session.get("user_id"):
        return redirect(url_for("index"))
    return render_template("login.html")


@app.get("/register")
def register_page():
    if session.get("user_id"):
        return redirect(url_for("index"))
    return render_template("register.html")


@app.post("/api/auth/register")
def api_register():
    data = request.get_json(force=True) or {}
    user, err = register_user(
        data.get("username", ""),
        data.get("email", ""),
        data.get("password", ""),
    )
    if err:
        return jsonify({"error": err}), 400
    session["user_id"] = user.id
    session["username"] = user.username
    return jsonify({"ok": True, "user": user.to_dict()})


@app.post("/api/auth/login")
def api_login():
    data = request.get_json(force=True) or {}
    user, err = authenticate_user(
        data.get("username", ""),
        data.get("password", ""),
    )
    if err:
        return jsonify({"error": err}), 401
    session["user_id"] = user.id
    session["username"] = user.username
    return jsonify({"ok": True, "user": user.to_dict()})


@app.post("/api/auth/logout")
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/auth/me")
def api_me():
    user = get_current_user()
    if not user:
        return jsonify({"user": None}), 401
    return jsonify({"user": user.to_dict()})


@app.get("/")
def home():
    """公开首页（未登录可访问）；已登录则跳转应用主页"""
    if session.get("user_id"):
        return redirect(url_for("index"))
    return render_template("home.html")


@app.get("/app")
@login_required
def index():
    return render_template("index.html", user=get_current_user())


@app.get("/news")
def news_page():
    """行业日报页面（未登录可预览）"""
    user = get_current_user()
    return render_template("news.html", user=user)


@app.get("/api/public/stats")
def api_public_stats():
    """公开统计数据（无需登录）"""
    try:
        from models import User
        user_count = User.query.count()
    except Exception:
        user_count = 0

    node_count = "--"
    relation_count = "--"
    label_count = "--"
    try:
        with get_qa_system().driver.session() as s:
            r = s.run("MATCH (n) RETURN count(n) AS cnt")
            node_count = r.single()["cnt"]
            r = s.run("MATCH ()-[r]->() RETURN count(r) AS cnt")
            relation_count = r.single()["cnt"]
            r = s.run("MATCH (n) RETURN count(DISTINCT labels(n)[0]) AS cnt")
            label_count = r.single()["cnt"]
    except Exception:
        pass

    return jsonify({
        "node_count": node_count,
        "relation_count": relation_count,
        "label_count": label_count,
        "user_count": user_count,
    })




@app.get("/evolution")
def evolution_page():
    """KG evolution timeline (public)."""
    user = get_current_user()
    return render_template("evolution.html", user=user)


@app.get("/api/evolution/data")
def api_evolution_data():
    """Return all snapshots for evolution timeline."""
    try:
        from models import GraphSnapshot
        snaps = (
            GraphSnapshot.query
            .order_by(GraphSnapshot.created_at.asc())
            .all()
        )
        return jsonify({
            "snapshots": [
                {
                    "id": s.id,
                    "week_label": s.week_label,
                    "node_count": s.node_count,
                    "relation_count": s.relation_count,
                    "label_breakdown": json.loads(s.label_breakdown or "{}"),
                    "top_growing_nodes": json.loads(s.top_growing_nodes or "[]"),
                    "new_relations_count": s.new_relations_count,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                }
                for s in snaps
            ]
        })
    except Exception as e:
        return jsonify({"snapshots": [], "error": str(e)})



@app.get("/dashboard")
@login_required
def dashboard_page():
    """ROI dashboard for investors and admins."""
    return render_template("dashboard.html", user=get_current_user())


@app.get("/api/dashboard")
@login_required
def api_dashboard():
    """Aggregate platform metrics for ROI dashboard."""
    try:
        from models import User, ChatMessage, GraphSnapshot
        from database import db
        from datetime import datetime, timezone, timedelta

        user_count = User.query.count()
        queries_total = ChatMessage.query.filter_by(role="user").count()

        # Recent weekly activity
        now = datetime.now(timezone.utc)
        weekly = []
        for i in range(6, -1, -1):
            week_start = now - timedelta(days=i * 7 + now.weekday())
            week_label = week_start.strftime("%m/%d")
            week_users = User.query.filter(User.created_at >= week_start).count()
            week_queries = ChatMessage.query.filter(
                ChatMessage.role == "user",
                ChatMessage.created_at >= week_start
            ).count()
            weekly.append({"week": week_label, "users": week_users, "queries": week_queries})

        # Latest graph stats
        node_count = "--"
        relation_count = "--"
        try:
            snap = GraphSnapshot.query.order_by(GraphSnapshot.created_at.desc()).first()
            if snap:
                node_count = snap.node_count
                relation_count = snap.relation_count
        except Exception:
            pass

        return jsonify({
            "user_count": user_count,
            "queries_total": queries_total,
            "node_count": node_count,
            "relation_count": relation_count,
            "weekly_activity": weekly,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/signals")
@login_required
def signals_page():
    """Investment signals and gap radar dashboard."""
    return render_template("signals.html", user=get_current_user())


@app.get("/api/signals")
@login_required
def api_signals():
    """Generate technology investment signals."""
    try:
        import sys, os
        ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if ROOT not in sys.path:
            sys.path.insert(0, ROOT)
        from signal_engine import generate_signals
        signals = generate_signals()
        return jsonify({
            "signals": signals,
            "total": len(signals),
            "red": len([s for s in signals if s["signal"] == "RED"]),
            "yellow": len([s for s in signals if s["signal"] == "YELLOW"]),
            "green": len([s for s in signals if s["signal"] == "GREEN"]),
        })
    except Exception as e:
        return jsonify({"signals": [], "error": str(e)})


@app.get("/api/gaps")
@login_required
def api_gaps():
    """Technology gap radar analysis."""
    try:
        import sys, os
        ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if ROOT not in sys.path:
            sys.path.insert(0, ROOT)
        from gap_radar import find_gaps
        result = find_gaps()
        return jsonify(result)
    except Exception as e:
        return jsonify({"gaps": [], "error": str(e)})
@app.get("/simulate")
@login_required
def simulate_page():
    """Supply chain shock simulator."""
    return render_template("simulate.html", user=get_current_user())


@app.post("/api/simulate")
@login_required
def api_simulate():
    """Run supply chain shock simulation."""
    payload = request.get_json(force=True) or {}
    scenario = (payload.get("scenario") or "").strip()
    if not scenario:
        return jsonify({"error": "scenario is required"}), 400
    try:
        result = get_qa_system().simulate_impact(scenario)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.get("/leaderboard")
def leaderboard_page():
    """Expert leaderboard (public view)."""
    user = get_current_user()
    return render_template("leaderboard.html", user=user)


@app.get("/profile")
@login_required
def profile_page():
    """User profile page."""
    return render_template("profile.html", user=get_current_user())


@app.get("/api/leaderboard")
def api_leaderboard():
    """Return expert leaderboard with current user's rank."""
    from credit_service import get_leaderboard, get_or_create_credit
    lb = get_leaderboard(20)
    my_rank = None
    my_score = None
    my_credits = None
    uid = session.get("user_id")
    if uid:
        uc = UserCredit.query.filter_by(user_id=uid).first()
        if uc:
            my_rank = UserCredit.query.filter(
                UserCredit.reputation_score > uc.reputation_score
            ).count() + 1
            my_score = round(uc.reputation_score, 1)
            my_credits = uc.total_credits
    return jsonify({
        "leaderboard": lb,
        "my_rank": my_rank,
        "my_score": my_score,
        "my_credits": my_credits,
    })


@app.get("/api/profile")
@login_required
def api_profile():
    """Get current user's full profile with credits."""
    from credit_service import get_user_credit
    result = get_user_credit(session["user_id"])
    if not result:
        from credit_service import get_or_create_credit
        get_or_create_credit(session["user_id"])
        result = get_user_credit(session["user_id"])
    return jsonify(result or {})


@app.post("/api/profile/update")
@login_required
def api_profile_update():
    """Update user's company and role."""
    from credit_service import get_or_create_credit
    data = request.get_json(force=True) or {}
    uc = get_or_create_credit(session["user_id"])
    uc.company = (data.get("company") or "").strip()
    uc.role = (data.get("role") or "").strip()
    db.session.commit()
    return jsonify({"ok": True, "company": uc.company, "role": uc.role})


@app.post("/api/credits/award")
@login_required
def api_award_credits():
    """Award credits for a contribution action."""
    from credit_service import award_credits
    data = request.get_json(force=True) or {}
    action = data.get("action", "entity_added")
    entity = data.get("entity_name", "")
    label = data.get("entity_label", "")
    earned = award_credits(session["user_id"], action, entity, label)
    return jsonify({"ok": True, "credits_earned": earned})


@app.post("/api/credits/verify")
@login_required
def api_verify_contribution():
    """Verify another user's contribution."""
    from credit_service import verify_contribution
    data = request.get_json(force=True) or {}
    contrib_id = data.get("contribution_id", 0)
    entity = data.get("entity_name", "")
    comment = data.get("comment", "")
    earned = verify_contribution(session["user_id"], contrib_id, entity, comment)
    return jsonify({"ok": True, "credits_earned": earned})
@app.get("/ingest")
@login_required
def ingest_page():
    return render_template("ingest.html", user=get_current_user())


@app.get("/archives")
@login_required
def archives_page():
    return render_template("archives.html", user=get_current_user())


@app.get("/api/archives")
@login_required
def api_archives():
    user = get_current_user()
    entries = (
        ArchiveEntry.query.filter_by(user_id=user.id)
        .order_by(ArchiveEntry.created_at.desc())
        .limit(200)
        .all()
    )
    return jsonify({
        "archives": [
            {
                "id": e.id,
                "type": e.archive_type,
                "title": e.title,
                "content": json.loads(e.content_json or "{}"),
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in entries
        ]
    })


@app.get("/api/chat/history")
@login_required
def api_chat_history():
    user = get_current_user()
    messages = (
        ChatMessage.query.filter_by(user_id=user.id)
        .order_by(ChatMessage.created_at.asc())
        .limit(500)
        .all()
    )
    return jsonify({
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "metadata": json.loads(m.metadata_json or "{}"),
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ]
    })


@app.get("/api/graph/updates")
@login_required
def api_graph_updates():
    user = get_current_user()
    logs = (
        GraphUpdateLog.query.filter_by(user_id=user.id)
        .order_by(GraphUpdateLog.created_at.desc())
        .limit(100)
        .all()
    )
    return jsonify({
        "updates": [
            {
                "id": l.id,
                "type": l.update_type,
                "entities_added": l.entities_added,
                "relations_added": l.relations_added,
                "status": l.status,
                "created_at": l.created_at.isoformat() if l.created_at else None,
            }
            for l in logs
        ]
    })


@app.get("/api/graph/overview")
@login_required
def api_graph_overview():
    """返回图谱“骨架”，用于首页背景可视化。"""
    query = "MATCH (n)-[r]-(m) WHERE type(r) IN ['EFFICIENT_PRECIPITATION','NEED_EQUIPMENT','HAS_PARAMETER','HAS_ABILITY','USED_FOR','USED_IN','HAS_ACTION','MEASURES','ENABLES','USED_FOR_ANALYSIS','MANUFACTURED_IN','MADE_FROM','RELATED'] RETURN n, r, m LIMIT 200"
    try:
        with get_qa_system().driver.session() as session:
            result = session.run(query)
            rows = [{"n": rec["n"], "r": rec["r"], "m": rec["m"]} for rec in result]
        graph_payload = _to_graph_payload(rows, "overview")
        return jsonify(graph_payload)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/graph/expand")
@login_required
def api_graph_expand():
    """点击节点展开一跳邻居。"""
    payload = request.get_json(force=True)
    node_id = payload.get("id") or payload.get("node_name") or payload.get("node_name")
    if not node_id:
        return jsonify({"nodes": [], "links": []})

    # 查询该节点的邻居
    query = """
    MATCH (n)-[r]-(m)
    WHERE n.name = $name OR elementId(n) = $name
    RETURN n, r, m LIMIT 50
    """
    try:
        with get_qa_system().driver.session() as session:
            result = session.run(query, name=node_id)
            rows = [{"n": rec["n"], "r": rec["r"], "m": rec["m"]} for rec in result]
        graph_payload = _to_graph_payload(rows, "expand")
        return jsonify(graph_payload)
    except Exception as e:
        print(f"Expand error: {e}")
        return jsonify({"nodes": [], "links": []})


@app.post("/api/ingest/extract")
@login_required
def api_ingest_extract():
    """上传文档 -> 抽取三元组 (不入库)"""
    user = get_current_user()
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    source_version = request.form.get("source_version", "v1")

    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        pkg = extract_from_document(tmp_path, source_version)
        _sync_extraction_to_tech_data(pkg, os.path.join(PROJECT_ROOT, "tech_Data.py"))
        
        try:
            os.remove(tmp_path)
        except Exception:
            pass

        response_data = {
            "source_doc": pkg.source_doc,
            "source_version": pkg.source_version,
            "extracted_at": pkg.extracted_at,
            "entities": [
                {
                    "label": e.label,
                    "name": e.name,
                    "description": e.description,
                    "properties": e.properties or {},
                    "confirmed": True
                }
                for e in pkg.entities
            ],
            "relations": [
                {
                    "start_label": r.start_label,
                    "start_name": r.start_name,
                    "rel_type": r.rel_type,
                    "end_label": r.end_label,
                    "end_name": r.end_name,
                    "description": r.description,
                    "properties": r.properties or {},
                    "confirmed": True
                }
                for r in pkg.relations
            ],
            "measurements": [],
            "warnings": pkg.warnings,
        }

        doc_record = save_document_record(user.id, file.filename, source_version, response_data)
        auto_archive(
            user_id=user.id,
            archive_type="document_extract",
            title=f"文档抽取 - {file.filename}",
            content=response_data,
            source_id=doc_record.id,
        )

        response_data["document_id"] = doc_record.id
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/ingest/apply")
@login_required
def api_ingest_apply():
    """将前端确认后的 JSON 入库并自动更新知识图谱"""
    user = get_current_user()
    payload = request.get_json(force=True)
    if not payload:
        return jsonify({"error": "Empty payload"}), 400

    try:
        result = apply_knowledge_graph_update(user.id, payload, "document_ingest")
        return jsonify({"status": "success", "message": "已成功入库并更新知识图谱", **result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/chat/confirm_triples")
@login_required
def api_chat_confirm_triples():
    """将聊天界面勾选的三元组入库并自动更新知识图谱"""
    user = get_current_user()
    payload = request.get_json(force=True)
    triples = payload.get("triples", {})
    
    ingest_payload = {
        "source_doc": "chat_interaction",
        "source_version": "v1",
        "entities": [],
        "relations": []
    }

    for e in triples.get("entities", []):
        e["confirmed"] = True
        ingest_payload["entities"].append(e)

    for r in triples.get("relations", []):
        r["confirmed"] = True
        ingest_payload["relations"].append(r)

    try:
        result = apply_knowledge_graph_update(user.id, ingest_payload, "chat_confirm")
        return jsonify(result)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


def _parse_reasoning_path(answer: str) -> list[str]:
    """从LLM输出中解析‘推理链路’里的节点序列。"""
    if not answer:
        return []

    nodes: list[str] = []
    nodes.extend(re.findall(r"`([^`]{1,50})`", answer))

    if len(nodes) < 2 and "->" in answer:
        parts = re.split(r"->", answer)
        for p in parts:
            t = re.sub(r"[*_#\[\]()\\]", "", p).strip()
            if 1 <= len(t) <= 30 and any(ch.isalnum() for ch in t):
                nodes.append(t)

    seen = set()
    out = []
    for n in nodes:
        n = n.strip()
        if not n or n in seen:
            continue
        seen.add(n)
        out.append(n)
    return out[:20]


# 关系英文 -> 中文（用于展示）
REL_TYPE_ZH = {
    "EFFICIENT_PRECIPITATION": "高效沉积",
    "NEED_EQUIPMENT": "需要设备",
    "HAS_PARAMETER": "包含参数",
    "HAS_ABILITY": "具备能力",
    "USED_FOR": "用于",
    "USED_IN": "应用于",
    "HAS_ACTION": "包含动作",
    "MEASURES": "测量",
    "ENABLES": "使能",
    "USED_FOR_ANALYSIS": "用于分析",
    "MANUFACTURED_IN": "制造于",
    "MADE_FROM": "由…制成",
    "RELATED": "相关",
}


def _llm_make_demo_subgraph(question: str, answer: str) -> dict:
    """当图数据库查不到任何连线时，用LLM生成“展示用子图”（不入库）。"""

    q = (question or "").strip()
    a = (answer or "").strip()
    if not a:
        return {"nodes": [], "links": []}

    prompt = f"""你是“半导体知识图谱可视化子图生成器”。

用户问：{q}
系统答：{a}

现在图数据库没有可用连线。为了让前端图谱更直观，请你只生成【展示用】的一个小子图：

硬性要求：
- 只能输出 JSON（不要解释，不要Markdown）。
- nodes 数量 6~12 个；links 数量 8~16 条。
- links 必须让 nodes 尽量连通（避免孤立点）。
- rel_type 只能从：USED_FOR, NEED_EQUIPMENT, HAS_PARAMETER, USED_IN, HAS_ABILITY, RELATED 中选择。
- 每个 node 必须有 name；label 从：Technology, Material, Equipment, Method, Parameter, Capability, Entity 里选；description 用一句中文短描述。
- 每个 link 必须有 source/target/rel_type；description 用一句中文短描述。

输出 JSON 结构示例：
{{
  "nodes": [{{"name":"ALD","label":"Technology","description":"原子层沉积技术"}}],
  "links": [{{"source":"ALD","rel_type":"NEED_EQUIPMENT","target":"ALD反应腔","description":"ALD 需要反应腔来实现前驱体脉冲"}}]
}}
"""

    try:
        resp = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1800,
        )
        content = (resp.choices[0].message.content or "").strip()
        try:
            json_str = _extract_json_block(content)
            demo = json.loads(json_str)
        except Exception:
            demo = _llm_fix_json(content, 1)

        nodes = demo.get("nodes") or []
        links = demo.get("links") or []

        clean_nodes = []
        seen = set()
        for n in nodes:
            name = (n.get("name") or "").strip()
            if not name or name in seen:
                continue
            seen.add(name)
            clean_nodes.append({
                "id": name,
                "name": name,
                "category": (n.get("label") or "Entity").strip() or "Entity",
                "description": (n.get("description") or "").strip(),
                "source": "ai_demo",
            })

        node_set = set([n["name"] for n in clean_nodes])
        clean_links = []
        for l in links:
            s = (l.get("source") or "").strip()
            t = (l.get("target") or "").strip()
            rt = (l.get("rel_type") or "").strip() or "RELATED"
            if not s or not t:
                continue
            if s not in node_set:
                node_set.add(s)
                clean_nodes.append({"id": s, "name": s, "category": "Entity", "description": "", "source": "ai_demo"})
            if t not in node_set:
                node_set.add(t)
                clean_nodes.append({"id": t, "name": t, "category": "Entity", "description": "", "source": "ai_demo"})

            clean_links.append({
                "key": f"{s}->{rt}->{t}",
                "source": s,
                "target": t,
                "label": REL_TYPE_ZH.get(rt, rt),
                "rel_type": rt,
                "description": (l.get("description") or "").strip(),
                "sourceStage": "ai_demo",
            })

        return {"nodes": clean_nodes[:25], "links": clean_links[:40]}
    except Exception:
        return {"nodes": [], "links": []}


def _get_fallback_graph(question: str = "", answer: str = "") -> dict:
    """半固定半动态兜底子图（保证有连线、且尽量和问题相关，仍然不入库）。"""

    text = f"{question} {answer}".strip()
    candidates: list[str] = []
    candidates += re.findall(r"\b[A-Za-z][A-Za-z0-9\-]{1,10}\b", text)
    candidates += re.findall(r"[\u4e00-\u9fa5]{2,8}", text)

    stop = {"问题", "系统", "回答", "图谱", "知识", "设备", "材料", "工艺", "方法", "推荐", "如何", "什么"}
    seen = set()
    cleaned: list[str] = []
    for c in candidates:
        c = c.strip()
        if not c or c in stop or c in seen:
            continue
        seen.add(c)
        cleaned.append(c)

    obj = cleaned[0] if len(cleaned) >= 1 else "TiN"
    tech = cleaned[1] if len(cleaned) >= 2 else "PVD"
    if obj == tech:
        tech = "PVD" if obj != "PVD" else "ALD"

    source_tag = "ai_demo_dynamic"

    nodes = [
        {"id": "半导体技术", "name": "半导体技术", "category": "Technology", "source": source_tag},
        {"id": "沉积", "name": "沉积", "category": "Method", "source": source_tag},
        {"id": tech, "name": tech, "category": "Technology", "source": source_tag},
        {"id": "CVD", "name": "CVD", "category": "Technology", "source": source_tag},
        {"id": "工艺设备", "name": "工艺设备", "category": "Equipment", "source": source_tag},
        {"id": obj, "name": obj, "category": "Material", "source": source_tag},
    ]

    links = [
        {"source": "半导体技术", "target": "沉积", "rel_type": "RELATED", "label": REL_TYPE_ZH.get("RELATED", "相关")},
        {"source": "沉积", "target": tech, "rel_type": "RELATED", "label": REL_TYPE_ZH.get("RELATED", "相关")},
        {"source": "沉积", "target": "CVD", "rel_type": "RELATED", "label": REL_TYPE_ZH.get("RELATED", "相关")},
        {"source": tech, "target": "工艺设备", "rel_type": "NEED_EQUIPMENT", "label": REL_TYPE_ZH.get("NEED_EQUIPMENT", "需要设备")},
        {"source": tech, "target": obj, "rel_type": "USED_FOR", "label": REL_TYPE_ZH.get("USED_FOR", "用于")},
    ]

    for link in links:
        link["key"] = f"{link['source']}->{link['rel_type']}->{link['target']}"

    return {"nodes": nodes, "links": links}


def _to_graph_payload(result_rows: list[dict], source_tag: str) -> dict:
    nodes: dict[str, dict] = {}
    links: list[dict] = []

    def add_node(name: str, label: str | None = None, props: dict | None = None):
        if not name:
            return
        if name not in nodes:
            node_data = {"id": name, "name": name, "category": label or "Entity", "source": source_tag}
            if props:
                for k, v in props.items():
                    if k not in ("id", "name") and v:
                        node_data[k] = v
            nodes[name] = node_data
        else:
            if props:
                for k, v in props.items():
                    if v and not nodes[name].get(k):
                        nodes[name][k] = v
            if label and nodes[name].get('category') == 'Entity':
                nodes[name]['category'] = label

    def add_link(src: str, dst: str, rel: str, props: dict | None = None):
        if not src or not dst or not rel:
            return
        link_key = f"{src}->{rel}->{dst}"
        if any(l.get('key') == link_key for l in links):
            return
        links.append({"key": link_key, "source": src, "target": dst, "label": REL_TYPE_ZH.get(rel, rel), "rel_type": rel, **(props or {})})

    for row in result_rows[:200]:
        if not isinstance(row, dict):
            continue

        n, r, m = row.get("n"), row.get("r"), row.get("m")
        if n is not None and r is not None and m is not None:
            n_name = n.get("name", str(getattr(n, 'element_id', getattr(n, 'id', ''))))
            m_name = m.get("name", str(getattr(m, 'element_id', getattr(m, 'id', ''))))
            add_node(n_name, list(n.labels)[0] if n.labels else "Node", dict(n))
            add_node(m_name, list(m.labels)[0] if m.labels else "Node", dict(m))
            add_link(n_name, m_name, r.type, {"description": r.get("description")})
            continue

        root = row.get("n_name")
        if isinstance(root, str) and any(key.endswith('_edges') or key.endswith('_by') for key in row):
            root_labels = row.get("n_labels")
            add_node(root, ",".join(root_labels) if isinstance(root_labels, list) else "Entity")
            for key in ["tech_method_edges", "material_edges", "equipment_edges", "structure_stage_edges"]:
                for e in row.get(key) or []:
                    if not isinstance(e, dict):
                        continue
                    m_name = e.get("m_name")
                    if not m_name:
                        continue
                    add_node(m_name, ",".join(e.get("m_labels") or []) or "Entity", {"description": e.get("m_desc")})
                    add_link(root, m_name, e.get("rel") or "RELATED", {"description": e.get("desc")})
            for e in row.get("material_supported_by") or []:
                if not isinstance(e, dict):
                    continue
                t_name = e.get("t_name")
                if not t_name:
                    continue
                add_node(t_name, "Technology")
                add_link(t_name, root, e.get("rel") or "EFFICIENT_PRECIPITATION", {"description": e.get("desc")})
            return {"nodes": list(nodes.values()), "links": links}

        node_map = {
            "technology_name": "Technology",
            "material_name": "Material",
            "equipment_name": "Equipment",
            "method_name": "Method",
            "parameter_name": "Parameter",
            "capability_name": "Capability",
            "source_name": "Entity",
            "name": "Entity",
        }
        found_nodes = {key: row[key] for key in node_map if row.get(key) and isinstance(row[key], str)}
        for key, name in found_nodes.items():
            add_node(name, node_map[key], {"description": row.get(f"{key.replace('_name', '_desc')}") or row.get("evidence")})

        if "technology_name" in found_nodes and "material_name" in found_nodes:
            add_link(found_nodes["technology_name"], found_nodes["material_name"], "EFFICIENT_PRECIPITATION", {"description": row.get("evidence")})
        if "technology_name" in found_nodes and "equipment_name" in found_nodes:
            add_link(found_nodes["technology_name"], found_nodes["equipment_name"], "NEED_EQUIPMENT", {"description": row.get("equipment_desc")})
        if "method_name" in found_nodes and "equipment_name" in found_nodes:
            add_link(found_nodes["method_name"], found_nodes["equipment_name"], "NEED_EQUIPMENT")

    # 孤立节点补边/移除逻辑（略，保持原逻辑即可）
    return {"nodes": list(nodes.values()), "links": links}


def _deduplicate_llm_extraction(extracted: dict, graph_payload: dict) -> dict:
    existing_entities = set()
    existing_relations = set()

    for n in (graph_payload.get("nodes") or []):
        existing_entities.add(((n.get("category") or "").strip(), (n.get("name") or "").strip()))

    for l in (graph_payload.get("links") or []):
        existing_relations.add(((l.get("source") or "").strip(), (l.get("label") or "").strip(), (l.get("target") or "").strip()))

    out_entities = []
    for e in (extracted.get("entities") or []):
        label = (e.get("label") or "").strip()
        name = (e.get("name") or "").strip()
        if not label or not name:
            continue
        key = (label, name)
        if key in existing_entities:
            continue
        existing_entities.add(key)
        out_entities.append(e)

    out_relations = []
    for r in (extracted.get("relations") or []):
        s = (r.get("start_name") or "").strip()
        t = (r.get("rel_type") or "").strip()
        o = (r.get("end_name") or "").strip()
        if not s or not t or not o:
            continue
        key = (s, t, o)
        if key in existing_relations:
            continue
        existing_relations.add(key)
        out_relations.append(r)

    return {
        "entities": out_entities,
        "relations": out_relations,
        "measurements": extracted.get("measurements") or [],
        "warnings": extracted.get("warnings") or [],
    }


@app.post("/api/chat")
@login_required
def api_chat():
    user = get_current_user()
    payload: Dict[str, Any] = request.get_json(force=True)
    question = (payload.get("question") or "").strip()
    if not question:
        return jsonify({"error": "question 不能为空"}), 400

    chat_session = payload.get("session_id") or f"session_{user.id}_{uuid.uuid4().hex[:8]}"
    save_chat_message(user.id, "user", question, {"session_id": chat_session}, chat_session)

    trace = [{"step": "input", "message": question}]
    result = get_qa_system().处理问题(question)

    results_block = result.get("results") or {}
    main_rows = results_block.get("main") or []
    exp_rows = results_block.get("expansion") or []

    graph_main = _to_graph_payload(main_rows, "main")
    graph_expansion = _to_graph_payload(exp_rows, "expansion")

    # 1) 让左侧“候选三元组”恢复：从回答里抽取候选三元组，写入 trace
    try:
        extracted = _llm_extract_triples(result.get("response") or "")
    except Exception:
        extracted = {"entities": [], "relations": [], "measurements": [], "warnings": []}

    # 去重：避免与图谱已展示的节点/关系重复
    merged_for_dedupe = {
        "nodes": (graph_main.get("nodes") or []) + (graph_expansion.get("nodes") or []),
        "links": (graph_main.get("links") or []) + (graph_expansion.get("links") or []),
    }
    extracted = _deduplicate_llm_extraction(extracted, merged_for_dedupe)

    if (extracted.get("entities") or []) or (extracted.get("relations") or []):
        trace.append({
            "step": "extracted_triples",
            "message": "已从回答中抽取候选三元组（勾选后可入库）",
            "triples": {
                "entities": extracted.get("entities") or [],
                "relations": extracted.get("relations") or [],
            },
        })
    else:
        trace.append({
            "step": "extracted_triples",
            "message": "未抽取到可入库的候选三元组（你可以换个问法或补充更多上下文）",
            "triples": {"entities": [], "relations": []},
        })

    # 2) 让右侧图谱“自动生成”恢复：如果主图没数据，用 LLM 生成展示用子图
    if not graph_main.get("nodes") and not graph_expansion.get("nodes"):
        demo_graph = _llm_make_demo_subgraph(question, result.get("response", ""))
        if demo_graph.get("nodes"):
            graph_main = demo_graph
            trace.append({"step": "graph_fallback", "message": "图谱无数据，已生成演示用子图（不入库）"})
        else:
            graph_main = _get_fallback_graph(question, result.get("response", ""))
            trace.append({"step": "graph_fallback", "message": "图谱无数据，已加载默认子图（不入库）"})

    response_text = result.get("response")
    save_chat_message(
        user.id,
        "ai",
        response_text or "",
        {
            "mode": result.get("mode"),
            "cypher": result.get("cypher"),
            "session_id": chat_session,
        },
        chat_session,
    )
    auto_archive(
        user_id=user.id,
        archive_type="chat",
        title=f"问答 - {question[:40]}",
        content={
            "question": question,
            "answer": response_text,
            "mode": result.get("mode"),
            "session_id": chat_session,
        },
    )

    return jsonify({
        "response": response_text,
        "mode": result.get("mode"),
        "cypher": result.get("cypher"),
        "graph": {"main": graph_main, "expansion": graph_expansion},
        "reasoning_path": _parse_reasoning_path(result.get("response") or ""),
        "trace": trace,
        "session_id": chat_session,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
