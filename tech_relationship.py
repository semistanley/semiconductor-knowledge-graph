from neo4j import GraphDatabase
from tech_Data import Date
import settings

settings.validate_neo4j_config()

config = Date()

URI = settings.NEO4J_URI
USER = settings.NEO4J_USER
PASSWORD = settings.NEO4J_PASSWORD

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def get_entity_label(entity_id):
    """根据 ID 前缀判断实体标签"""
    prefix_map = {
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
    for prefix, label in prefix_map.items():
        if entity_id.startswith(prefix):
            return label
    raise ValueError(f"未知实体 ID: {entity_id}")

def create_relationship(tx, rel):
    """创建关系（关联已存在的实体节点）"""
    start_label = get_entity_label(rel["start_id"])
    end_label = get_entity_label(rel["end_id"])

    query = f"""
    MATCH (start:{start_label} {{id: $start_id}})
    MATCH (end:{end_label} {{id: $end_id}})
    MERGE (start)-[r:{rel['relationship_type']} {{ 
        weight: $weight,
        description: $description 
    }}]->(end)
    """
    tx.run(
        query,
        start_id=rel["start_id"],
        end_id=rel["end_id"],
        weight=rel["weight"],
        description=rel["description"]
    )

try:
    with driver.session() as session:
        # 导入所有关系
        for i, rel in enumerate(config.relationships, 1):
            try:
                session.execute_write(create_relationship, rel)
                print(f"导入关系 {i}/{len(config.relationships)}: {rel['relationship_type']}")
            except Exception as e:
                print(f"关系 {i} 导入失败: {str(e)}")

    print("所有技术树关系导入完成！")
finally:
    driver.close()
