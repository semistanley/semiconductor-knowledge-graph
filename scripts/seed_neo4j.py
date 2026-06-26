#!/usr/bin/env python3
"""
Neo4j 知识图谱初始化播种脚本

幂等导入（使用 MERGE，重复运行不会重复插入相同数据）。
从 tech_Data.py 读取所有实体和关系，导入到 Neo4j 图数据库。

用法：
  python scripts/seed_neo4j.py          # 导入全部数据
  python scripts/seed_neo4j.py --reset  # 清空后重新导入（危险！）
"""

from __future__ import annotations

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from neo4j import GraphDatabase
import settings

settings.validate_neo4j_config()

URI = settings.NEO4J_URI
USER = settings.NEO4J_USER
PASSWORD = settings.NEO4J_PASSWORD

LABEL_MAP = {
    "Action": "Action",
    "Technology": "Technology",
    "Method": "Method",
    "SubMethod": "SubMethod",
    "Material": "Material",
    "Capability": "Capability",
    "Equipment": "Equipment",
    "ChipStructure": "ChipStructure",
    "ManufacturingStage": "ManufacturingStage",
    "Parameter": "Parameter",
}

# Entity ID prefix -> Label mapping
ID_PREFIX_MAP = {
    "action_": "Action",
    "tech_": "Technology",
    "method_": "Method",
    "submethod_": "SubMethod",
    "material_": "Material",
    "capability_": "Capability",
    "equipment_": "Equipment",
    "structure_": "ChipStructure",
    "stage_": "ManufacturingStage",
    "parameter_": "Parameter",
}


def get_label_by_id(entity_id: str) -> str:
    for prefix, label in ID_PREFIX_MAP.items():
        if entity_id.startswith(prefix):
            return label
    raise ValueError(f"Unknown entity ID prefix: {entity_id}")


def seed_entities(driver):
    """从 tech_Data.py 导入所有实体节点（幂等）"""
    from tech_Data import Date

    config = Date()

    entity_groups = [
        ("Action", config.Action),
        ("Technology", config.Technology),
        ("Method", config.Method),
        ("SubMethod", config.SubMethod),
        ("Material", config.Material),
        ("Capability", config.Capability),
        ("Equipment", config.Equipment),
        ("ChipStructure", config.ChipStructure),
        ("ManufacturingStage", config.ManufacturingStage),
        ("Parameter", config.Parameter),
    ]

    total = 0
    with driver.session() as session:
        for label, entities in entity_groups:
            count = len(entities) if entities else 0
            if count == 0:
                continue

            session.execute_write(
                _import_entities, entities, label
            )
            print(f"  [{label}] 导入 {count} 个节点")
            total += count

    print(f"实体导入完成，共 {total} 个节点")
    return total


def _import_entities(tx, entities, label):
    query = f"""
    UNWIND $entities AS entity
    MERGE (n:{label} {{id: entity.id}})
    ON CREATE SET
        n.name = entity.name,
        n.description = entity.description
    ON MATCH SET
        n.name = entity.name,
        n.description = COALESCE(entity.description, n.description)
    """
    tx.run(query, entities=entities)


def seed_relations(driver):
    """从 tech_Data.py 导入所有关系（幂等）"""
    from tech_Data import Date

    config = Date()

    if not config.relationships:
        print("  没有找到关系数据")
        return 0

    total = len(config.relationships)
    with driver.session() as session:
        for i, rel in enumerate(config.relationships):
            try:
                session.execute_write(_create_relation, rel)
                if (i + 1) % 50 == 0:
                    print(f"  关系进度: {i+1}/{total}")
            except Exception as e:
                print(f"  关系 {i+1} 导入失败: {e}")

    print(f"关系导入完成，共 {total} 条")
    return total


def _create_relation(tx, rel):
    start_label = get_label_by_id(rel["start_id"])
    end_label = get_label_by_id(rel["end_id"])

    query = f"""
    MATCH (start:{start_label} {{id: $start_id}})
    MATCH (end:{end_label} {{id: $end_id}})
    MERGE (start)-[r:{rel['relationship_type']}]->(end)
    ON CREATE SET
        r.weight = $weight,
        r.description = $description
    ON MATCH SET
        r.weight = $weight,
        r.description = COALESCE($description, r.description)
    """
    tx.run(
        query,
        start_id=rel["start_id"],
        end_id=rel["end_id"],
        weight=rel.get("weight", 1.0),
        description=rel.get("description", ""),
    )


def reset_graph(driver):
    """清空整个图数据库（危险操作）"""
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("图数据库已清空")


def verify(driver):
    """验证播种结果"""
    with driver.session() as session:
        r = session.run("MATCH (n) RETURN count(n) AS cnt")
        node_count = r.single()["cnt"]
        r = session.run("MATCH ()-[r]->() RETURN count(r) AS cnt")
        rel_count = r.single()["cnt"]
        r = session.run(
            "MATCH (n) RETURN labels(n)[0] AS label, count(n) AS cnt ORDER BY cnt DESC"
        )
        labels_info = [(rec["label"], rec["cnt"]) for rec in r]

    print(f"\n图数据库统计:")
    print(f"  节点总数: {node_count}")
    print(f"  关系总数: {rel_count}")
    print(f"  节点分布:")
    for label, cnt in labels_info:
        print(f"    {label}: {cnt}")


def main():
    parser = argparse.ArgumentParser(description="播种 Neo4j 知识图谱")
    parser.add_argument("--reset", action="store_true", help="清空后重新导入")
    parser.add_argument("--verify-only", action="store_true", help="仅验证，不导入")
    args = parser.parse_args()

    print(f"连接 Neo4j: {URI}")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    try:
        driver.verify_connectivity()
        print("连接成功")

        if args.verify_only:
            verify(driver)
            return

        if args.reset:
            print("重置图数据库...")
            reset_graph(driver)

        start = time.time()

        print("\n导入实体节点...")
        node_count = seed_entities(driver)

        print("\n导入关系...")
        rel_count = seed_relations(driver)

        elapsed = time.time() - start
        print(f"\n播种完成！耗时: {elapsed:.1f}s 节点: {node_count} 关系: {rel_count}")

        verify(driver)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
