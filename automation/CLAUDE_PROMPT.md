# Claude Code：运行半导体 KG 自动化流水线

请按 AGENTS.md 执行：

1. 检查 `docker compose ps`；若 web/mysql/neo4j 未运行则 `docker compose up -d`
2. 扫描 `automation/inbox/` 是否有待处理文档
3. 若有文档：运行 `python automation/pipeline.py`
4. 汇总 outbox 新增 JSON 数量、实体/关系条数，并提示是否执行 `--auto-apply`
5. 将执行摘要写入 `automation/logs/claude_run_$(date +%Y%m%d_%H%M%S).md`

若 inbox 为空，仅报告平台健康状态与最近 5 条 pipeline.log。
