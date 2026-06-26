#!/usr/bin/env python3
"""
Technology Gap Radar

Identifies knowledge gaps and structural holes in the knowledge graph
that represent investment or research opportunities.

Strategy:
  1. Find high-degree nodes that are NOT connected to each other (missed synergy)
  2. Find nodes with single connections (underexplored areas)
  3. LLM analysis of top gaps → investment opportunity score

Usage:
  python scripts/gap_radar.py
  python scripts/gap_radar.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "web_app"))

import settings
from neo4j import GraphDatabase
from openai import OpenAI

client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=settings.DEEPSEEK_API_BASE)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_gaps() -> dict:
    settings.validate_neo4j_config()
    driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
    )

    gaps = []
    try:
        driver.verify_connectivity()
        with driver.session() as session:
            # Gap Type 1: High-degree nodes NOT connected to each other
            r = session.run("""
                MATCH (a:Technology) WHERE size([(a)-[]-()|1]) > 5
                MATCH (b:Technology) WHERE size([(b)-[]-()|1]) > 5 AND a.name < b.name
                WHERE NOT (a)-[*1..2]-(b)
                RETURN a.name AS tech_a, b.name AS tech_b,
                       size([(a)-[]-()|1]) AS deg_a,
                       size([(b)-[]-()|1]) AS deg_b
                LIMIT 15
            """)
            for rec in r:
                gaps.append({
                    "type": "missed_synergy",
                    "tech_a": rec["tech_a"],
                    "tech_b": rec["tech_b"],
                    "deg_a": rec["deg_a"],
                    "deg_b": rec["deg_b"],
                    "description": f"{rec['tech_a']} and {rec['tech_b']} are both well-connected ({rec['deg_a']}+{rec['deg_b']} links) but not connected — potential integration opportunity",
                })

            # Gap Type 2: Underexplored nodes (few connections, high potential)
            r = session.run("""
                MATCH (t:Technology)
                OPTIONAL MATCH (t)-[r]-(m)
                WITH t, count(r) AS degree
                WHERE degree <= 3 AND degree >= 1
                RETURN t.name AS tech, degree, t.description AS description
                ORDER BY degree ASC LIMIT 10
            """)
            for rec in r:
                gaps.append({
                    "type": "underexplored",
                    "tech": rec["tech"],
                    "degree": rec["degree"],
                    "description": rec["description"] or "",
                    "summary": f"{rec['tech']} has only {rec['degree']} connections — underexplored area with growth potential",
                })

            # Gap Type 3: Equipment without usage context
            r = session.run("""
                MATCH (e:Equipment)
                OPTIONAL MATCH (e)-[r]-(t:Technology)
                WITH e, count(r) AS tech_count
                WHERE tech_count <= 1
                RETURN e.name AS equipment, e.description AS description, tech_count
                LIMIT 10
            """)
            for rec in r:
                gaps.append({
                    "type": "unlinked_equipment",
                    "equipment": rec["equipment"],
                    "tech_count": rec["tech_count"],
                    "description": rec["description"] or "",
                    "summary": f"Equipment '{rec['equipment']}' has only {rec['tech_count']} technology links — needs process context",
                })

    finally:
        driver.close()

    # LLM analysis of top gaps
    top_gaps = gaps[:10]
    analysis = ""
    if top_gaps:
        gap_text = "\n".join(
            f"- {g.get('summary', g.get('description', ''))}" for g in top_gaps[:8]
        )
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": (
                    "You are a semiconductor investment analyst. Below is a list of knowledge gaps "
                    "discovered in a semiconductor technology knowledge graph. Each gap represents "
                    "a potential investment or research opportunity. Analyze the top gaps and provide:\n"
                    "1. The 3 most investable gaps (ranked by potential ROI)\n"
                    "2. For each: why it matters, estimated market size direction, and what needs to happen\n"
                    "3. One sentence summary for investors\n\n"
                    f"Gaps found:\n{gap_text}"
                )}],
                temperature=0.5,
                max_tokens=500,
            )
            analysis = (resp.choices[0].message.content or "").strip()
        except Exception as e:
            analysis = f"AI analysis unavailable: {e}"

    return {
        "generated_at": _now_iso(),
        "total_gaps": len(gaps),
        "missed_synergy_count": len([g for g in gaps if g["type"] == "missed_synergy"]),
        "underexplored_count": len([g for g in gaps if g["type"] == "underexplored"]),
        "unlinked_equipment_count": len([g for g in gaps if g["type"] == "unlinked_equipment"]),
        "gaps": gaps,
        "analysis": analysis,
    }


def main():
    parser = argparse.ArgumentParser(description="Technology Gap Radar")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = find_gaps()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("  TECHNOLOGY GAP RADAR")
        print("=" * 60)
        print(f"  Total gaps found: {result['total_gaps']}")
        print(f"  Missed synergies: {result['missed_synergy_count']}")
        print(f"  Underexplored:    {result['underexplored_count']}")
        print(f"  Unlinked equip:   {result['unlinked_equipment_count']}")
        print()
        for g in result["gaps"][:10]:
            tag = g["type"]
            print(f"  [{tag}] {g.get('summary', g.get('description', ''))[:100]}")
        print()
        if result["analysis"]:
            print("  AI Analysis:")
            print(result["analysis"])


if __name__ == "__main__":
    main()
