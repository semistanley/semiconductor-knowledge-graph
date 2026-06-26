# 半导体知识图谱平台 — Claude Code 自动化指令

你是本仓库的 KG 运维助手。目标：文档入库、三元组抽取、Neo4j 更新、Web 平台数据归档。

## 环境

- 配置：根目录 `.env`（API Key、Neo4j、MySQL 密码）
- Web：`python run_platform.py` 或 `docker compose up -d`
- 流水线：`python automation/pipeline.py`

## 标准流水线（Claude Code 执行）

1. 确认服务：`docker compose ps` 或检查 Neo4j/MySQL
2. 将 PDF/DOCX/TXT 放入 `automation/inbox/`
3. 运行：`python automation/pipeline.py`（或 `--auto-apply` 自动入库）
4. 输出在 `automation/outbox/*.json`，原文在 `automation/processed/`
5. 日志：`automation/logs/pipeline.log`

## 常用命令

```bash
# Docker 全栈
docker compose up -d --build

# 单次流水线
python automation/pipeline.py

# 监听 inbox（与 compose profile pipeline 相同）
python automation/pipeline.py --watch

# 确认入库已有 JSON
python automation/pipeline.py --apply automation/outbox/xxx.json

# 初始化 Neo4j 基础实体（首次部署）
python tech_entity.py && python tech_relationship.py
```

## 约束

- 不要修改 `.env` 中的密钥并提交到 Git
- 三元组入库前必须有 evidence；禁止编造实体
- 优先使用 `settings.py` 读取配置，勿在代码中硬编码密码
