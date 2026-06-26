#!/usr/bin/env python3
"""
Technology Investment Signal Engine

Analyzes knowledge graph dynamics to generate investment signals.
Computes: heat score, maturity score, commercialization score → red/yellow/green signal.

Usage:
  python scripts/signal_engine.py              # Generate signals
  python scripts/signal_engine.py --json        # JSON output
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "web_app"))

import settings
from neo4j import GraphDatabase

# Industry mapping: technology node -> related public companies
TECH_COMPANY_MAP = {
    "EUV光刻": ["ASML", "Zeiss", "Trumpf"],
    "DUV光刻": ["ASML", "Nikon", "Canon"],
    "ALD": ["ASM International", "Lam Research", "Tokyo Electron"],
    "PVD": ["Applied Materials", "Evatec", "ULVAC"],
    "CVD": ["Applied Materials", "Lam Research", "Tokyo Electron"],
    "PECVD": ["Applied Materials", "Lam Research"],
    "MOCVD": ["Aixtron", "Veeco"],
    "溅射": ["Applied Materials", "Evatec", "ULVAC"],
    "刻蚀": ["Lam Research", "Tokyo Electron", "Applied Materials"],
    "CMP": ["Applied Materials", "Ebara"],
    "3D集成": ["TSMC", "Samsung", "Intel"],
    "SiC": ["Wolfspeed", "STMicro", "ON Semi", "ROHM"],
    "GaN": ["Navitas", "EPC", "Infineon"],
    "TiN": ["Applied Materials", "Lam Research"],
    "光刻胶": ["JSR", "TOK", "ShinEtsu", "DuPont"],
}

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_signals() -> list[dict]:
    settings.validate_neo4j_config()
    driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
    )

    signals = []
    try:
        driver.verify_connectivity()

        with driver.session() as session:
            # Get all technology nodes with their degree and neighbor diversity
            result = session.run("""
                MATCH (t:Technology)
                OPTIONAL MATCH (t)-[r]-(m)
                WITH t, count(DISTINCT r) AS degree, count(DISTINCT labels(m)[0]) AS neighbor_diversity
                RETURN t.name AS tech, degree, neighbor_diversity,
                       t.description AS description
                ORDER BY degree DESC
                LIMIT 30
            """)

            for rec in result:
                tech = rec["tech"]
                degree = rec["degree"]
                diversity = rec["neighbor_diversity"]

                # ---- Scoring Model ----
                # Heat: how many connections (0-10)
                heat = min(10, degree / 6)
                # Maturity: neighbor diversity (0-10)
                maturity = min(10, diversity * 2)
                # Commercialization: equipment + material connections
                commercialization = min(10, (degree - diversity) / 3) if degree > diversity else 5

                # Composite score
                composite = heat * 0.4 + maturity * 0.3 + commercialization * 0.3

                # Signal level
                if composite >= 7.0:
                    signal = "RED"      # High priority - invest now
                elif composite >= 4.5:
                    signal = "YELLOW"   # Watch closely
                else:
                    signal = "GREEN"    # Monitor

                companies = TECH_COMPANY_MAP.get(tech, [])
                # Also search for equipment/material nodes connected to this tech
                equip_result = session.run("""
                    MATCH (t:Technology {name: $tech})-[r:NEED_EQUIPMENT|EFFICIENT_PRECIPITATION]-(m)
                    RETURN m.name AS name, labels(m)[0] AS label LIMIT 5
                """, tech=tech)
                linked_entities = [{"name": r["name"], "label": r["label"]} for r in equip_result]

                signals.append({
                    "technology": tech,
                    "description": rec["description"] or "",
                    "degree": degree,
                    "neighbor_diversity": diversity,
                    "heat_score": round(heat, 1),
                    "maturity_score": round(maturity, 1),
                    "commercialization_score": round(commercialization, 1),
                    "composite_score": round(composite, 1),
                    "signal": signal,
                    "related_companies": companies[:5],
                    "linked_entities": linked_entities,
                })

        # Sort by composite score descending
        signals.sort(key=lambda s: s["composite_score"], reverse=True)

    finally:
        driver.close()

    return signals


def main():
    parser = argparse.ArgumentParser(description="Investment Signal Engine")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    signals = generate_signals()

    if args.json:
        print(json.dumps({
            "generated_at": _now_iso(),
            "total_signals": len(signals),
            "red": len([s for s in signals if s["signal"] == "RED"]),
            "yellow": len([s for s in signals if s["signal"] == "YELLOW"]),
            "green": len([s for s in signals if s["signal"] == "GREEN"]),
            "signals": signals,
        }, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("  TECHNOLOGY INVESTMENT SIGNALS")
        print("=" * 70)
        for s in signals[:15]:
            icon = {"RED": "red", "YELLOW": "yellow", "GREEN": "green"}[s["signal"]]
            print(f"\n  {s['signal']:8s} | {s['technology']:12s} | Score: {s['composite_score']:.1f}")
            print(f"           Heat: {s['heat_score']:.1f}  Maturity: {s['maturity_score']:.1f}  Commercialization: {s['commercialization_score']:.1f}")
            if s["related_companies"]:
                print(f"           Companies: {', '.join(s['related_companies'][:3])}")
        print(f"\n  Total: {len(signals)} signals")
        print(f"  RED: {len([s for s in signals if s['signal']=='RED'])} | YELLOW: {len([s for s in signals if s['signal']=='YELLOW'])} | GREEN: {len([s for s in signals if s['signal']=='GREEN'])}")


if __name__ == "__main__":
    main()
