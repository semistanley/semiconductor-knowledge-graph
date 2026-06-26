from __future__ import annotations

from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from database import db


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow)

    chat_messages = db.relationship("ChatMessage", backref="user", lazy="dynamic")
    documents = db.relationship("DocumentRecord", backref="user", lazy="dynamic")
    archives = db.relationship("ArchiveEntry", backref="user", lazy="dynamic")
    graph_updates = db.relationship("GraphUpdateLog", backref="user", lazy="dynamic")
    credits = db.relationship("UserCredit", backref="user", uselist=False, lazy="joined")
    contributions = db.relationship("Contribution", backref="user", lazy="dynamic")
    verifications = db.relationship("Verification", backref="user", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    metadata_json = db.Column(db.Text, default="{}")
    session_id = db.Column(db.String(64), index=True)
    created_at = db.Column(db.DateTime, default=_utcnow, index=True)


class DocumentRecord(db.Model):
    __tablename__ = "document_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    source_version = db.Column(db.String(64), default="v1")
    status = db.Column(db.String(32), default="uploaded")
    extraction_json = db.Column(db.Text, default="{}")
    entities_count = db.Column(db.Integer, default=0)
    relations_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=_utcnow, index=True)
    applied_at = db.Column(db.DateTime, nullable=True)


class ArchiveEntry(db.Model):
    __tablename__ = "archive_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    archive_type = db.Column(db.String(32), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content_json = db.Column(db.Text, nullable=False)
    source_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=_utcnow, index=True)


class GraphUpdateLog(db.Model):
    __tablename__ = "graph_update_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    update_type = db.Column(db.String(32), nullable=False)
    entities_added = db.Column(db.Integer, default=0)
    relations_added = db.Column(db.Integer, default=0)
    payload_json = db.Column(db.Text, default="{}")
    status = db.Column(db.String(32), default="success")
    created_at = db.Column(db.DateTime, default=_utcnow, index=True)


class GraphSnapshot(db.Model):
    """Weekly knowledge graph snapshot for evolution tracking."""
    __tablename__ = "graph_snapshots"

    id = db.Column(db.Integer, primary_key=True)
    week_label = db.Column(db.String(32), nullable=False, index=True)
    node_count = db.Column(db.Integer, default=0)
    relation_count = db.Column(db.Integer, default=0)
    label_breakdown = db.Column(db.Text, default="{}")
    top_growing_nodes = db.Column(db.Text, default="[]")
    new_relations_count = db.Column(db.Integer, default=0)
    ingested_docs_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=_utcnow, index=True)


class UserCredit(db.Model):
    """Reputation and credit score per user."""
    __tablename__ = "user_credits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False, index=True)
    total_credits = db.Column(db.Integer, default=0)
    reputation_score = db.Column(db.Float, default=50.0)
    contributions_count = db.Column(db.Integer, default=0)
    verifications_given = db.Column(db.Integer, default=0)
    verifications_received = db.Column(db.Integer, default=0)
    domain_badges = db.Column(db.Text, default="[]")
    company = db.Column(db.String(120), default="")
    role = db.Column(db.String(120), default="")
    is_verified_pro = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_credits": self.total_credits,
            "reputation_score": round(self.reputation_score, 1),
            "contributions_count": self.contributions_count,
            "verifications_given": self.verifications_given,
            "verifications_received": self.verifications_received,
            "domain_badges": self.domain_badges,
            "company": self.company,
            "role": self.role,
            "is_verified_pro": self.is_verified_pro,
        }


class Contribution(db.Model):
    """Track each knowledge contribution by a user."""
    __tablename__ = "contributions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    contrib_type = db.Column(db.String(32), nullable=False)
    entity_name = db.Column(db.String(255), default="")
    entity_label = db.Column(db.String(64), default="")
    credits_earned = db.Column(db.Integer, default=0)
    verified_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=_utcnow, index=True)


class Verification(db.Model):
    """Track peer verification of contributions."""
    __tablename__ = "verifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    contribution_id = db.Column(db.Integer, db.ForeignKey("contributions.id"), nullable=True)
    entity_name = db.Column(db.String(255), default="")
    comment = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=_utcnow)
