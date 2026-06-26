#!/usr/bin/env bash
# 半导体知识图谱平台 - 一键部署 (Linux / macOS)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT"

BUILD=false
PIPELINE=false
NO_SEED=false
LOGS=false

usage() {
  cat <<EOF
用法: $0 [选项]

选项:
  --build       重新构建 Docker 镜像
  --pipeline    同时启动自动化流水线服务
  --no-seed     跳过 Neo4j 播种
  --logs        启动后跟踪日志
  -h, --help    显示帮助
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build)    BUILD=true; shift ;;
    --pipeline) PIPELINE=true; shift ;;
    --no-seed)  NO_SEED=true; shift ;;
    --logs)     LOGS=true; shift ;;
    -h|--help)  usage ;;
    *) echo "未知参数: $1"; usage ;;
  esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m'

echo ""
echo -e "${CYAN}========================================"
echo -e "  半导体知识图谱平台 - 一键部署"
echo -e "========================================${NC}"
echo ""

# 1. Check Docker
echo -e "${YELLOW}[1/5] 检查 Docker...${NC}"
if ! docker info &>/dev/null; then
    echo -e "${RED}  [错误] Docker 未运行，请先启动 Docker${NC}"
    exit 1
fi
echo -e "${GREEN}  Docker 已就绪${NC}"

# 2. Check .env
echo -e "${YELLOW}[2/5] 检查配置文件...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}  .env 已从 .env.example 生成，请编辑后重新运行${NC}"
    echo -e "${YELLOW}    - DEEPSEEK_API_KEY: DeepSeek API 密钥${NC}"
    echo -e "${YELLOW}    - NEO4J_PASSWORD: Neo4j 数据库密码${NC}"
    echo -e "${YELLOW}    - FLASK_SECRET_KEY: Flask 会话密钥${NC}"
    exit 1
fi

if grep -qE "your_deepseek_api_key_here|change_me" .env; then
    echo -e "${RED}  [警告] .env 中仍有占位符未替换${NC}"
    read -rp "  按 Enter 继续或 Ctrl+C 退出... "
fi
echo -e "${GREEN}  .env 配置完成${NC}"

# 3. Pull / Build
echo -e "${YELLOW}[3/5] 准备镜像...${NC}"
if $BUILD; then
    echo -e "${YELLOW}  重新构建 Docker 镜像...${NC}"
    docker compose build
else
    echo -e "${YELLOW}  拉取基础镜像...${NC}"
    docker compose pull mysql neo4j 2>/dev/null || true
fi

# 4. Start
echo -e "${YELLOW}[4/5] 启动服务...${NC}"
CMD=(docker compose up -d)
$BUILD && CMD+=(--build)

if $PIPELINE; then
    echo -e "${YELLOW}  启动 Web + MySQL + Neo4j + 流水线...${NC}"
    docker compose --profile pipeline "${CMD[@]}"
else
    echo -e "${YELLOW}  启动 Web + MySQL + Neo4j...${NC}"
    "${CMD[@]}"
fi

# 5. Wait
echo -e "${YELLOW}[5/5] 等待服务就绪...${NC}"
echo -e "${YELLOW}  首次启动需 2-5 分钟（下载镜像 + 初始化数据库 + Neo4j 播种）${NC}"
echo ""

if $LOGS; then
    echo -e "${CYAN}  跟踪 Web 服务日志...${NC}"
    docker compose logs -f web
fi

# Done
echo -e "${GREEN}========================================"
echo -e "  部署完成！访问地址:"
echo -e "========================================${NC}"
echo ""
echo -e "${WHITE}  平台首页:   http://localhost:5000${NC}"
echo -e "${WHITE}  AI 问答:    http://localhost:5000/app${NC}"
echo -e "${WHITE}  文档抽取:   http://localhost:5000/ingest${NC}"
echo -e "${WHITE}  行业日报:   http://localhost:5000/news${NC}"
echo ""
echo -e "${GRAY}  Neo4j 浏览器: http://localhost:7474${NC}"
echo -e "${GRAY}  MySQL:         localhost:3307${NC}"
echo ""
echo -e "${YELLOW}自动化流水线:${NC}"
echo -e "${GRAY}  docker compose --profile pipeline up -d pipeline${NC}"
echo ""
