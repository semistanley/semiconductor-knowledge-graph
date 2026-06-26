from neo4j import GraphDatabase
from tech_Data import Date
import settings

settings.validate_neo4j_config()

config = Date()

URI = settings.NEO4J_URI
USER = settings.NEO4J_USER
PASSWORD = settings.NEO4J_PASSWORD

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def import_entities(tx, entities, label):
    """批量导入实体节点"""
    query = f"""
    UNWIND $entities AS entity
    MERGE (n:{label} {{id: entity.id}})
    ON CREATE SET 
        n.name = entity.name,
        n.description = entity.description
    """
    tx.run(query, entities=entities)

try:
    with driver.session() as session:
        # 实体类型配置：(数据列表, 节点标签)
        entity_configs = [
            (config.Action, "Action"),
            (config.Technology, "Technology"),
            (config.Method, "Method"),
            (config.SubMethod, "SubMethod"),
            (config.Material, "Material"),
            (config.Capability, "Capability"),
            (config.Equipment, "Equipment"),
            (config.ChipStructure, "ChipStructure"),
            (config.ManufacturingStage, "ManufacturingStage"),
            (config.Parameter, "Parameter"),
        ]

        # 导入所有实体
        for entities, label in entity_configs:
            session.execute_write(import_entities, entities, label)
            print(f"导入 {label} 实体 {len(entities)} 条")

    print("所有实体导入完成！")
finally:
    driver.close()
