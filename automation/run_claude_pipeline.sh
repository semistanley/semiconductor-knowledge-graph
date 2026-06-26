#!/usr/bin/env bash
# Claude Code CLI 流水线入口
# 用法: ./automation/run_claude_pipeline.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== 1. Docker 服务检查 =="
if ! docker compose ps >/dev/null 2>&1; then
  echo "启动 Docker Compose..."
  docker compose up -d --build
fi

echo "== 2. Python 流水线 =="
python automation/pipeline.py "$@"

echo "== 3. Claude Code 汇总（可选）=="
if command -v claude >/dev/null 2>&1; then
  claude -p "$(cat automation/CLAUDE_PROMPT.md)"
else
  echo "未检测到 claude CLI，跳过。安装: https://docs.anthropic.com/en/docs/claude-code"
fi

echo "完成。outbox: automation/outbox | 日志: automation/logs/pipeline.log"
