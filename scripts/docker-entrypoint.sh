#!/bin/bash
set -euo pipefail

echo "[entrypoint] waiting for MySQL at ${MYSQL_HOST:-mysql}:${MYSQL_PORT:-3306}..."
for i in $(seq 1 60); do
  if python - <<'PY'
import os, sys
import pymysql
host = os.getenv("MYSQL_HOST", "mysql")
port = int(os.getenv("MYSQL_PORT", "3306"))
user = os.getenv("MYSQL_USER", "kg_user")
pwd = os.getenv("MYSQL_PASSWORD", "")
db = os.getenv("MYSQL_DATABASE", "semiconductor_kg")
try:
    conn = pymysql.connect(host=host, port=port, user=user, password=pwd, database=db, connect_timeout=3)
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
  then
    echo "[entrypoint] MySQL is ready"
    break
  fi
  sleep 2
done

echo "[entrypoint] waiting for Neo4j at ${NEO4J_URI:-bolt://neo4j:7687}..."
for i in $(seq 1 60); do
  if python - <<'PY'
import os, sys
from neo4j import GraphDatabase
uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
user = os.getenv("NEO4J_USER", "neo4j")
pwd = os.getenv("NEO4J_PASSWORD", "")
try:
    d = GraphDatabase.driver(uri, auth=(user, pwd))
    d.verify_connectivity()
    d.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
  then
    echo "[entrypoint] Neo4j is ready"
    break
  fi
  sleep 3
done

echo "[entrypoint] seeding Neo4j knowledge graph (idempotent)..."
python /app/scripts/seed_neo4j.py || echo "[entrypoint] WARNING: Neo4j seed failed (graph may be empty)"

echo "[entrypoint] initializing SQLAlchemy tables..."
python - <<'PY'
import os, sys
ROOT = "/app"
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "web_app"))
os.chdir(os.path.join(ROOT, "web_app"))
from app import app
from database import init_db
init_db(app)
print("[entrypoint] database tables ready")
PY

exec "$@"
