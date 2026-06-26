# 半导体知识图谱平台

基于 **Neo4j 知识图谱 + DeepSeek AI** 的半导体工艺流程智能平台。

支持自然语言问答、文档三元组自动抽取、交互式知识图谱可视化与商业决策分析。

## 快速启动

```powershell
# Windows (PowerShell)
.\scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh
```

部署后访问 **http://localhost:5000**

## 功能

| 功能 | 说明 |
|------|------|
| **AI 智能问答** | 自然语言提问，自动转 Cypher 查询图谱，DeepSeek 生成专业回答 |
| **文档三元组抽取** | 上传 PDF/DOCX/TXT，AI 自动抽取实体/关系，确认后入库 |
| **知识图谱可视化** | ECharts 交互式图谱，点击展开邻居节点，查看节点详情 |
| **商业决策分析** | 每个节点附带 TRL 评估、商业价值评级、采购链/ROI/落地路径 |
| **自动化流水线** | inbox 文档自动触发 AI 抽取 → 入库 → 图谱更新 |
| **行业日报** | 集成 Horizon AI 新闻雷达，每天自动聚合全球半导体资讯 |
| **用户系统** | 注册/登录/会话管理，每个用户独立数据隔离 |
| **公开首页** | 无需登录即可预览平台功能和知识图谱统计数据 |

## 环境要求

- **Docker Desktop** (推荐)
- 或 Python 3.11+ + MySQL + Neo4j (手动安装)
- DeepSeek API Key ([获取地址](https://platform.deepseek.com/))

## 技术栈

| 层次 | 技术 |
|------|------|
| **后端框架** | Python Flask + SQLAlchemy |
| **数据库** | MySQL 8.4 (生产) / SQLite (本地开发) |
| **知识图谱** | Neo4j 5.26 Community |
| **AI 引擎** | DeepSeek (OpenAI 兼容 API) |
| **前端可视化** | ECharts + 原生 JavaScript |
| **部署** | Docker Compose (4 服务) |
| **自动化** | Python pipeline + Claude Code 集成 |

## 配置

首次运行 `.\scripts\deploy.ps1` 会自动从 `.env.example` 生成 `.env`。
编辑 `.env` 填入：

| 配置项 | 说明 |
|--------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `NEO4J_PASSWORD` | Neo4j 数据库密码 |
| `FLASK_SECRET_KEY` | Flask 会话密钥 |
| `MYSQL_PASSWORD` | MySQL 用户密码 |
| `MYSQL_ROOT_PASSWORD` | MySQL root 密码 |

## 项目结构

```
.
├── web_app/                  # Flask Web 应用
│   ├── app.py                # 路由 & API (含公开首页/统计 API)
│   ├── models.py             # 数据模型 (User/ChatMessage/Document/...)
│   ├── database.py           # SQLAlchemy 初始化 (MySQL/SQLite 双模式)
│   ├── auth_utils.py         # 用户认证 (注册/登录/会话)
│   ├── services.py           # 业务服务 (入库/归档/日志)
│   ├── templates/
│   │   ├── home.html         # 公开首页 (无需登录)
│   │   ├── index.html        # 问答页面 (左聊天/右图谱)
│   │   ├── ingest.html       # 文档三元组抽取
│   │   ├── archives.html     # 历史归档
│   │   ├── news.html         # 行业日报 (Horizon 聚合)
│   │   ├── login.html        # 登录页
│   │   └── register.html     # 注册页
│   └── static/
│       ├── css/style.css     # 全局样式
│       ├── css/home.css      # 首页专用样式
│       └── js/
│           ├── app.js        # 问答/图谱/三元组交互
│           ├── auth.js       # 认证逻辑
│           ├── home.js       # 首页背景知识图谱
│           ├── ingest.js     # 文档上传交互
│           └── echarts.min.js
├── semiconductor_kg_qa.py    # 知识图谱问答引擎 (NL→Cypher→LLM)
├── semiconductor_doc_ingest.py # 文档抽取管道 (PDF/DOCX→三元组→Neo4j)
├── tech_Data.py              # 初始知识图谱数据 (10大类/200+节点/100+关系)
├── settings.py               # 统一配置管理 (.env → 全局变量)
├── automation/
│   ├── pipeline.py           # 自动化流水线 (inbox 监听 → 抽取 → 入库)
│   └── inbox/                # 文档投放目录
├── scripts/
│   ├── deploy.ps1            # Windows 一键部署
│   ├── deploy.sh             # Linux/Mac 一键部署
│   ├── docker-entrypoint.sh  # Docker 启动 (等待 MySQL/Neo4j → 播种 → 启动)
│   ├── seed_neo4j.py         # Neo4j 知识图谱幂等播种
│   └── mysql-init.sql        # MySQL 初始化 (字符集/权限)
├── docker-compose.yml        # MySQL + Neo4j + Web + Pipeline 四服务
├── Dockerfile                # Python 3.12 + Gunicorn
└── .env.example              # 环境变量模板
```

## 页面路由

| 路径 | 认证 | 说明 |
|------|------|------|
| `/` | 公开 | 平台首页（知识图谱概览 + 功能展示） |
| `/app` | 登录 | AI 智能问答 + 图谱可视化 |
| `/ingest` | 登录 | 文档上传 + 三元组抽取 |
| `/archives` | 登录 | 历史归档 + 图谱更新日志 |
| `/news` | 公开 | 半导体行业日报 |
| `/login` | 公开 | 登录 |
| `/register` | 公开 | 注册 |

## API 接口

### 认证
| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/auth/register` | 公开 | 注册 |
| POST | `/api/auth/login` | 公开 | 登录 |
| POST | `/api/auth/logout` | 登录 | 登出 |
| GET | `/api/auth/me` | 登录 | 当前用户 |

### 公开
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/public/stats` | 知识图谱统计 (节点数/关系数/类别数/用户数) |

### 核心功能 (需登录)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat` | AI 问答 + 图谱检索 + 三元组抽取 |
| GET | `/api/chat/history` | 对话历史 |
| POST | `/api/chat/confirm_triples` | 确认三元组入库 |
| POST | `/api/ingest/extract` | 文档上传抽取三元组 |
| POST | `/api/ingest/apply` | 确认入库 |
| GET | `/api/graph/overview` | 图谱概览骨架 |
| POST | `/api/graph/expand` | 点击节点展开邻居子图 |
| GET | `/api/graph/updates` | 图谱更新日志 |
| GET | `/api/archives` | 归档列表 |

## 自动化流水线

```powershell
# 方式 1: Docker pipeline 服务 (持续监听)
docker compose --profile pipeline up -d pipeline

# 方式 2: 手动处理一次
docker compose run --rm web python automation/pipeline.py

# 方式 3: 本地运行
# 将文档放入 automation/inbox/ 后运行
python automation/pipeline.py
```

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 复制配置
copy .env.example .env   # 编辑填入密钥

# 本地启动 (使用 SQLite，无需 MySQL/Neo4j Docker)
python web_app/app.py
```

`settings.py` 会自动检测：`MYSQL_HOST` 为空时使用 SQLite，Docker 环境自动使用 MySQL。

## 常见问题

**Q: 打开首页报 TemplateNotFound**
A: 请确保从 `web_app/` 目录启动：`python web_app/app.py`

**Q: Docker 启动后 Web 容器反复重启**
A: 首次启动 MySQL/Neo4j 需要 1-2 分钟初始化，Web 容器会自动等待 (最多 60 次重试)。查看日志：`docker compose logs web`

**Q: Neo4j 图谱为空**
A: Docker 首次启动会自动运行 `seed_neo4j.py`。也可以手动运行：`docker compose exec web python scripts/seed_neo4j.py`

**Q: 页面改了没变化**
A: `Ctrl + F5` 强制刷新浏览器缓存

## License

MIT
