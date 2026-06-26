"""统一配置：从 .env / 环境变量读取 API 与数据库密码"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env", override=False)


def env(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


def require_env(key: str) -> str:
    val = os.getenv(key, "").strip()
    if not val:
        raise RuntimeError(f"缺少环境变量 {key}，请复制 .env.example 为 .env 并填写")
    return val


# DeepSeek / OpenAI 兼容 API
DEEPSEEK_API_KEY: str = env("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE: str = env("DEEPSEEK_API_BASE", "https://api.deepseek.com")
DEEPSEEK_MODEL: str = env("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_SKIP_HEALTHCHECK: bool = env("DEEPSEEK_SKIP_HEALTHCHECK", "0") == "1"

# Neo4j 知识图谱
NEO4J_URI: str = env("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER: str = env("NEO4J_USER", "neo4j")
NEO4J_PASSWORD: str = env("NEO4J_PASSWORD")

# Flask
FLASK_SECRET_KEY: str = env("FLASK_SECRET_KEY", "change-me-in-production")
FLASK_DEBUG: bool = env("FLASK_DEBUG", "0") == "1"

# MySQL（Docker / 生产环境）
MYSQL_HOST: str = env("MYSQL_HOST", "")
MYSQL_PORT: str = env("MYSQL_PORT", "3306")
MYSQL_DATABASE: str = env("MYSQL_DATABASE", "semiconductor_kg")
MYSQL_USER: str = env("MYSQL_USER", "kg_user")
MYSQL_PASSWORD: str = env("MYSQL_PASSWORD", "")
MYSQL_ROOT_PASSWORD: str = env("MYSQL_ROOT_PASSWORD", "")


def get_sqlalchemy_uri() -> str:
    explicit = env("SQLALCHEMY_DATABASE_URI")
    if explicit:
        return explicit
    if MYSQL_HOST:
        from urllib.parse import quote_plus

        pwd = quote_plus(MYSQL_PASSWORD)
        return (
            f"mysql+pymysql://{MYSQL_USER}:{pwd}@{MYSQL_HOST}:{MYSQL_PORT}"
            f"/{MYSQL_DATABASE}?charset=utf8mb4"
        )
    db_path = ROOT_DIR / "web_app" / "data" / "platform.db"
    return f"sqlite:///{db_path.as_posix()}"


def validate_llm_config() -> None:
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("请设置 DEEPSEEK_API_KEY（见 .env.example）")


def validate_neo4j_config() -> None:
    if not NEO4J_PASSWORD:
        raise RuntimeError("请设置 NEO4J_PASSWORD（见 .env.example）")
