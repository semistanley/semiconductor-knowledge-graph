"""启动半导体知识图谱 Web 平台"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "web_app"))

import settings  # noqa: F401 — 加载 .env

from app import app

if __name__ == "__main__":
    port = int(settings.env("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=settings.FLASK_DEBUG)
