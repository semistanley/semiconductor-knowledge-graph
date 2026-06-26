#!/usr/bin/env python3
"""
半导体知识图谱自动化流水线

流程：inbox 文档 -> LLM 抽取三元组 -> outbox JSON -> （可选）自动确认入库 Neo4j + tech_Data

用法：
  python automation/pipeline.py                  # 处理 inbox 一次
  python automation/pipeline.py --watch          # 监听 inbox（Docker pipeline 服务）
  python automation/pipeline.py --apply out.json # 确认并入库指定 pending 文件
  python automation/pipeline.py --auto-apply     # 抽取后自动全部 confirmed 入库
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import settings
from semiconductor_doc_ingest import (
    apply_pending_to_neo4j,
    extract_from_document,
    save_pending,
    _sync_extraction_to_tech_data,
)

SUPPORTED = {".pdf", ".docx", ".doc", ".txt", ".md"}


def _log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line)
    log_dir = ROOT / settings.env("PIPELINE_LOG_DIR", "automation/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / "pipeline.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _paths() -> tuple[Path, Path, Path]:
    inbox = ROOT / settings.env("PIPELINE_INBOX", "automation/inbox")
    outbox = ROOT / settings.env("PIPELINE_OUTBOX", "automation/outbox")
    processed = ROOT / "automation/processed"
    for p in (inbox, outbox, processed):
        p.mkdir(parents=True, exist_ok=True)
    return inbox, outbox, processed


def _package_to_pending(pkg, auto_confirm: bool) -> dict:
    return {
        "source_doc": pkg.source_doc,
        "source_version": pkg.source_version,
        "extracted_at": pkg.extracted_at,
        "entities": [
            {
                "label": e.label,
                "name": e.name,
                "description": e.description,
                "properties": e.properties or {},
                "confirmed": auto_confirm,
            }
            for e in pkg.entities
        ],
        "relations": [
            {
                "start_label": r.start_label,
                "start_name": r.start_name,
                "rel_type": r.rel_type,
                "end_label": r.end_label,
                "end_name": r.end_name,
                "description": r.description,
                "properties": r.properties or {},
                "confirmed": auto_confirm,
            }
            for r in pkg.relations
        ],
        "measurements": [{**m, "confirmed": auto_confirm} for m in (pkg.measurements or [])],
        "warnings": pkg.warnings,
    }


def process_file(file_path: Path, outbox: Path, processed: Path, auto_apply: bool) -> Path | None:
    _log(f"开始处理: {file_path.name}")
    version = f"pipe_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    pkg = extract_from_document(str(file_path), version)
    _sync_extraction_to_tech_data(pkg, str(ROOT / "tech_Data.py"))

    pending = _package_to_pending(pkg, auto_confirm=auto_apply)
    out_name = f"{file_path.stem}_{version}.json"
    out_path = outbox / out_name
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)

    _log(
        f"抽取完成: 实体 {len(pkg.entities)} 关系 {len(pkg.relations)} -> {out_path.name}"
    )

    if auto_apply and (pending["entities"] or pending["relations"]):
        apply_pending_to_neo4j(pending)
        _log(f"已自动入库 Neo4j: {out_path.name}")

    dest = processed / file_path.name
    if dest.exists():
        dest = processed / f"{file_path.stem}_{int(time.time())}{file_path.suffix}"
    shutil.move(str(file_path), str(dest))
    _log(f"原文档已归档至 processed/: {dest.name}")
    return out_path


def run_once(auto_apply: bool | None = None) -> int:
    if auto_apply is None:
        auto_apply = settings.env("PIPELINE_AUTO_APPLY", "0") == "1"

    inbox, outbox, processed = _paths()
    files = sorted(
        p for p in inbox.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )
    if not files:
        _log("inbox 为空，无待处理文档")
        return 0

    count = 0
    for fp in files:
        try:
            process_file(fp, outbox, processed, auto_apply)
            count += 1
        except Exception as e:
            _log(f"处理失败 {fp.name}: {e}")
    _log(f"本轮完成，共处理 {count} 个文件")
    return count


def apply_pending_file(pending_path: Path) -> None:
    with open(pending_path, "r", encoding="utf-8") as f:
        pending = json.load(f)
    for e in pending.get("entities", []):
        e["confirmed"] = True
    for r in pending.get("relations", []):
        r["confirmed"] = True
    apply_pending_to_neo4j(pending)
    _log(f"已入库: {pending_path.name}")


def watch_loop(auto_apply: bool, interval: int = 30) -> None:
    _log(f"监听模式启动，间隔 {interval}s，auto_apply={auto_apply}")
    while True:
        run_once(auto_apply)
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="半导体 KG 自动化流水线")
    parser.add_argument("--watch", action="store_true", help="持续监听 inbox")
    parser.add_argument("--interval", type=int, default=30, help="监听间隔秒")
    parser.add_argument("--auto-apply", action="store_true", help="抽取后自动全部入库")
    parser.add_argument("--apply", type=str, help="将指定 pending JSON 入库")
    args = parser.parse_args()

    settings.validate_llm_config()
    settings.validate_neo4j_config()

    if args.apply:
        apply_pending_file(Path(args.apply))
        return

    auto = args.auto_apply or settings.env("PIPELINE_AUTO_APPLY", "0") == "1"
    if args.watch:
        watch_loop(auto, args.interval)
    else:
        run_once(auto)


if __name__ == "__main__":
    main()
