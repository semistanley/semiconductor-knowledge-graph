#!/usr/bin/env python3
"""
Weekly Knowledge Graph Snapshot

Takes a snapshot of current Neo4j graph state and saves to MySQL via SQLAlchemy.
Used to power the evolution timeline visualization.

Usage:
  python scripts/weekly_snapshot.py           # Manual snapshot
  python scripts/weekly_snapshot.py --auto     # Auto (from scheduler, uses Docker env)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "web_app"))

import settings
from neo4j import GraphDatabase


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_week_label() -> str:
    dt = datetime.now(timezone.utc)
    return f"{dt.year}-W{dt.isocalendar()[1]:02d}"


def take_snapshot(auto: bool = False) -> dict:
    settings.validate_neo4j_config()

    uri = settings.NEO4J_URI
    user = settings.NEO4J_USER
    password = settings.NEO4J_PASSWORD

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()

        with driver.session() as session:
            # Total counts
            r = session.run("MATCH (n) RETURN count(n) AS cnt")
            node_count = r.single()["cnt"]

            r = session.run("MATCH ()-[r]->() RETURN count(r) AS cnt")
            relation_count = r.single()["cnt"]

            # Label breakdown
            r = session.run(
                "MATCH (n) RETURN labels(n)[0] AS label, count(n) AS cnt ORDER BY cnt DESC"
            )
            label_breakdown = {rec["label"]: rec["cnt"] for rec in r}

            # Top growing nodes (nodes with most relationships)
            r = session.run(
                "MATCH (n)-[r]-() "
                "RETURN n.name AS name, labels(n)[0] AS label, count(r) AS degree "
                "ORDER BY degree DESC LIMIT 10"
            )
            top_nodes = [
                {"name": rec["name"], "label": rec["label"], "degree": rec["degree"]}
                for rec in r
            ]

        # Compare with previous snapshot
        new_relations = 0
        try:
            from database import db, init_db
            from models import GraphSnapshot
            from flask import Flask

            app = Flask(__name__)
            app.config["SECRET_KEY"] = "snapshot-temp"
            init_db(app)

            with app.app_context():
                prev = (
                    GraphSnapshot.query
                    .order_by(GraphSnapshot.created_at.desc())
                    .first()
                )
                if prev:
                    new_relations = max(0, relation_count - (prev.relation_count or 0))

                snap = GraphSnapshot(
                    week_label=get_week_label(),
                    node_count=node_count,
                    relation_count=relation_count,
                    label_breakdown=json.dumps(label_breakdown, ensure_ascii=False),
                    top_growing_nodes=json.dumps(top_nodes, ensure_ascii=False),
                    new_relations_count=new_relations,
                    ingested_docs_count=0,
                )
                db.session.add(snap)
                db.session.commit()
                snap_id = snap.id
        except Exception as e:
            print(f"Warning: Could not save to DB: {e}")
            snap_id = None

        result = {
            "week": get_week_label(),
            "node_count": node_count,
            "relation_count": relation_count,
            "label_breakdown": label_breakdown,
            "top_nodes": top_nodes,
            "new_relations": new_relations,
            "snap_id": snap_id,
            "timestamp": _now_iso(),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    finally:
        driver.close()


def main():
    parser = argparse.ArgumentParser(description="Weekly KG snapshot")
    parser.add_argument("--auto", action="store_true", help="Auto mode (from scheduler)")
    args = parser.parse_args()
    take_snapshot(auto=args.auto)


if __name__ == "__main__":
    main()
