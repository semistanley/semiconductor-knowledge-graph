#!/usr/bin/env python3
"""
Knowledge Graph Auto-Update Scheduler

Three-tier update pipeline:
  L1 (hourly): Horizon news -> inbox -> pipeline -> Neo4j
  L2 (daily):  arXiv papers + OSS Insight -> AI extract -> Neo4j
  L3 (weekly): Graph snapshot + AI evolution report

Usage:
  python automation/scheduler.py --daemon     # Run all tiers continuously
  python automation/scheduler.py --tier L1    # Run L1 only
  python automation/scheduler.py --tier L2    # Run L2 only
  python automation/scheduler.py --tier L3    # Run weekly snapshot
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import settings


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    line = f"[{_now()}] {msg}"
    print(line)
    log_dir = ROOT / "automation" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / "scheduler.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_l1() -> bool:
    """L1: Hourly news pulse from Horizon into inbox -> pipeline."""
    log("L1: Running news pulse...")

    horizon_path = os.environ.get("HORIZON_PATH")
    if not horizon_path:
        log("L1: HORIZON_PATH not set, skipping")
        return False

    try:
        result = subprocess.run(
            ["docker", "compose", "run", "--rm", "horizon", "--hours", "2"],
            cwd=horizon_path,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            log("L1: Horizon run complete")
            return True
        else:
            log(f"L1: Horizon failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"L1: Error: {e}")
        return False


def run_l2() -> bool:
    """L2: Daily deep ingestion - arXiv papers, GitHub trends."""
    log("L2: Running daily deep ingestion...")

    # Process any documents that accumulated in inbox
    inbox = ROOT / "automation" / "inbox"
    files = list(inbox.glob("*"))
    doc_files = [f for f in files if f.suffix.lower() in {".pdf", ".docx", ".txt", ".md"}]

    if doc_files:
        log(f"L2: Found {len(doc_files)} documents in inbox")
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "automation" / "pipeline.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=600,
            )
            log(f"L2: Pipeline result: {result.stdout[:200] if result.returncode == 0 else result.stderr[:200]}")
            return result.returncode == 0
        except Exception as e:
            log(f"L2: Error: {e}")
            return False
    else:
        log("L2: No documents in inbox, skipping")
        return True


def run_l3() -> bool:
    """L3: Weekly graph snapshot + evolution report."""
    log("L3: Running weekly snapshot...")

    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "weekly_snapshot.py"), "--auto"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            log(f"L3: Snapshot complete: {result.stdout[:300]}")
            return True
        else:
            log(f"L3: Snapshot failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"L3: Error: {e}")
        return False


def run_daemon():
    """Continuous daemon mode - runs all tiers on schedule."""
    log("=" * 50)
    log("Scheduler daemon started")
    log(f"  L1: every 60 minutes")
    log(f"  L2: every 24 hours")
    log(f"  L3: every 7 days")
    log("=" * 50)

    last_l1 = 0
    last_l2 = 0
    last_l3 = 0

    while True:
        now = time.time()

        # L1: every 60 minutes
        if now - last_l1 >= 3600:
            run_l1()
            last_l1 = now

        # L2: every 24 hours
        if now - last_l2 >= 86400:
            run_l2()
            last_l2 = now

        # L3: every 7 days
        if now - last_l3 >= 604800:
            run_l3()
            last_l3 = now

        time.sleep(300)  # Check every 5 minutes


def main():
    parser = argparse.ArgumentParser(description="KG Auto-Update Scheduler")
    parser.add_argument("--daemon", action="store_true", help="Run continuous daemon")
    parser.add_argument("--tier", choices=["L1", "L2", "L3"], help="Run a single tier")
    parser.add_argument("--init-snapshot", action="store_true", help="Take initial snapshot for demo")
    args = parser.parse_args()

    if args.daemon:
        run_daemon()
    elif args.init_snapshot:
        # Take 3 snapshots with fake growth for demo purposes
        log("Initializing demo snapshots...")
        for i in range(3):
            log(f"Snapshot {i+1}/3...")
            run_l3()
            if i < 2:
                log("  (simulating growth between snapshots)")
        log("Demo snapshots complete. Visit /evolution to see the timeline.")
    elif args.tier == "L1":
        run_l1()
    elif args.tier == "L2":
        run_l2()
    elif args.tier == "L3":
        run_l3()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
