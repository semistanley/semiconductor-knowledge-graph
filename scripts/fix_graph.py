#!/usr/bin/env python3
"""Apply critical fixes to app.py for graph rendering"""
import sys

path = '/app/web_app/app.py' if len(sys.argv) < 2 else sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

count = 0

# Fix 1: Graph overview - query ALL relationship types, use Cypher single-quotes
old1 = 'MATCH (t:Technology)-[r]-(m) RETURN t as n, r, m LIMIT 100'
new1 = (
    "MATCH (n)-[r]-(m) "
    "WHERE type(r) IN ["
    "'EFFICIENT_PRECIPITATION','NEED_EQUIPMENT','HAS_PARAMETER',"
    "'HAS_ABILITY','USED_FOR','USED_IN','HAS_ACTION','MEASURES',"
    "'ENABLES','USED_FOR_ANALYSIS','MANUFACTURED_IN','MADE_FROM','RELATED'"
    "] "
    "RETURN n, r, m LIMIT 200"
)
if old1 in content:
    content = content.replace(old1, new1)
    count += 1
    print("Fix 1 applied: graph overview query")
else:
    print("Fix 1 SKIPPED: pattern not found")

# Fix 2: graph/expand accept node_name from frontend
old2 = 'node_id = payload.get("id")'
new2 = 'node_id = payload.get("id") or payload.get("node_name")'
if old2 in content:
    content = content.replace(old2, new2)
    count += 1
    print("Fix 2 applied: node_name fallback")
else:
    print("Fix 2 SKIPPED: pattern not found")

# Fix 3: Prevent Neo4j props from overwriting graph node id/name
old3 = 'nodes[name] = {"id": name, "name": name, "category": label or "Entity", "source": source_tag, **(props or {})}'
new3 = (
    'node_data = {"id": name, "name": name, "category": label or "Entity", "source": source_tag}\n'
    '            if props:\n'
    '                for k, v in props.items():\n'
    '                    if k not in ("id", "name") and v:\n'
    '                        node_data[k] = v\n'
    '            nodes[name] = node_data'
)
if old3 in content:
    content = content.replace(old3, new3)
    count += 1
    print("Fix 3 applied: id/name protection")
else:
    print("Fix 3 SKIPPED: pattern not found")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
compile(content, path, 'exec')
print(f"\nAll {count} fixes applied. Syntax valid.")
