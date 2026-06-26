from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from database import db
from models import ArchiveEntry, ChatMessage, DocumentRecord, GraphUpdateLog

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_chat_message(
    user_id: int,
    role: str,
    content: str,
    metadata: dict | None = None,
    session_id: str | None = None,
) -> ChatMessage:
    msg = ChatMessage(
        user_id=user_id,
        role=role,
        content=content,
        metadata_json=json.dumps(metadata or {}, ensure_ascii=False),
        session_id=session_id or f"session_{user_id}",
    )
    db.session.add(msg)
    db.session.commit()
    return msg


def auto_archive(
    user_id: int,
    archive_type: str,
    title: str,
    content: dict[str, Any],
    source_id: int | None = None,
) -> ArchiveEntry:
    entry = ArchiveEntry(
        user_id=user_id,
        archive_type=archive_type,
        title=title,
        content_json=json.dumps(content, ensure_ascii=False),
        source_id=source_id,
    )
    db.session.add(entry)
    db.session.commit()
    return entry


def log_graph_update(
    user_id: int,
    update_type: str,
    entities_added: int,
    relations_added: int,
    payload: dict[str, Any],
    status: str = "success",
) -> GraphUpdateLog:
    log = GraphUpdateLog(
        user_id=user_id,
        update_type=update_type,
        entities_added=entities_added,
        relations_added=relations_added,
        payload_json=json.dumps(payload, ensure_ascii=False),
        status=status,
    )
    db.session.add(log)
    db.session.commit()
    return log


def save_document_record(
    user_id: int,
    filename: str,
    source_version: str,
    extraction_data: dict[str, Any],
) -> DocumentRecord:
    entities = extraction_data.get("entities") or []
    relations = extraction_data.get("relations") or []
    record = DocumentRecord(
        user_id=user_id,
        filename=filename,
        source_version=source_version,
        status="extracted",
        extraction_json=json.dumps(extraction_data, ensure_ascii=False),
        entities_count=len(entities),
        relations_count=len(relations),
    )
    db.session.add(record)
    db.session.commit()
    return record


def apply_knowledge_graph_update(
    user_id: int,
    payload: dict[str, Any],
    update_type: str,
    tech_data_path: str | None = None,
) -> dict[str, Any]:
    """确认三元组 -> Neo4j + tech_Data 同步 + 归档 + 日志"""
    from semiconductor_doc_ingest import (
        ExtractionPackage,
        Entity,
        Relation,
        apply_pending_to_neo4j,
        _sync_extraction_to_tech_data,
    )

    tech_data_path = tech_data_path or os.path.join(PROJECT_ROOT, "tech_Data.py")

    entities_confirmed = [e for e in payload.get("entities", []) if e.get("confirmed")]
    relations_confirmed = [r for r in payload.get("relations", []) if r.get("confirmed")]

    for e in entities_confirmed:
        e["confirmed"] = True
    for r in relations_confirmed:
        r["confirmed"] = True

    apply_payload = {
        "source_doc": payload.get("source_doc", "platform"),
        "source_version": payload.get("source_version", "v1"),
        "entities": entities_confirmed,
        "relations": relations_confirmed,
    }

    apply_pending_to_neo4j(apply_payload)

    pkg = ExtractionPackage(
        source_doc=apply_payload["source_doc"],
        source_version=apply_payload["source_version"],
        extracted_at=_now_iso(),
        entities=[
            Entity(
                label=e.get("label", ""),
                name=e.get("name", ""),
                description=e.get("description", ""),
                properties=e.get("properties"),
            )
            for e in entities_confirmed
        ],
        relations=[
            Relation(
                start_label=r.get("start_label", ""),
                start_name=r.get("start_name", ""),
                rel_type=r.get("rel_type", ""),
                end_label=r.get("end_label", ""),
                end_name=r.get("end_name", ""),
                description=r.get("description", ""),
                properties=r.get("properties"),
            )
            for r in relations_confirmed
        ],
        measurements=[],
        warnings=[],
    )

    sync_stat = {"added_entities": 0, "skipped_entities": 0, "added_relations": 0, "skipped_relations": 0}
    if pkg.entities or pkg.relations:
        sync_stat = _sync_extraction_to_tech_data(pkg, tech_data_path)

    archive = auto_archive(
        user_id=user_id,
        archive_type="kg_update",
        title=f"知识图谱更新 - {apply_payload['source_doc']}",
        content={
            "source_doc": apply_payload["source_doc"],
            "source_version": apply_payload["source_version"],
            "entities": entities_confirmed,
            "relations": relations_confirmed,
            "sync_stat": sync_stat,
            "applied_at": _now_iso(),
        },
    )

    log = log_graph_update(
        user_id=user_id,
        update_type=update_type,
        entities_added=sync_stat.get("added_entities", len(entities_confirmed)),
        relations_added=sync_stat.get("added_relations", len(relations_confirmed)),
        payload={
            "source_doc": apply_payload["source_doc"],
            "entities_count": len(entities_confirmed),
            "relations_count": len(relations_confirmed),
            "sync_stat": sync_stat,
        },
    )

    return {
        "ok": True,
        "added": {
            "entities": sync_stat.get("added_entities", len(entities_confirmed)),
            "relations": sync_stat.get("added_relations", len(relations_confirmed)),
        },
        "skipped": {
            "entities": sync_stat.get("skipped_entities", 0),
            "relations": sync_stat.get("skipped_relations", 0),
        },
        "archive_id": archive.id,
        "graph_update_id": log.id,
        "touched_nodes": list({e.get("name") for e in entities_confirmed if e.get("name")}),
    }
