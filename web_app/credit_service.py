"""Reputation and credit management service."""

from __future__ import annotations

import json
from database import db
from models import User, UserCredit, Contribution, Verification


CREDIT_RULES = {
    "entity_added": 10,
    "relation_added": 10,
    "verified_by_peer": 15,
    "verify_others": 5,
    "referral": 50,
    "daily_login": 1,
}


def get_or_create_credit(user_id: int) -> UserCredit:
    uc = UserCredit.query.filter_by(user_id=user_id).first()
    if not uc:
        uc = UserCredit(user_id=user_id)
        db.session.add(uc)
        db.session.commit()
    return uc


def award_credits(user_id: int, action: str, entity_name: str = "", entity_label: str = "") -> int:
    earned = CREDIT_RULES.get(action, 5)
    uc = get_or_create_credit(user_id)
    uc.total_credits += earned
    uc.contributions_count += 1

    # Update reputation: 50 base + credits/10 + verifications*2
    uc.reputation_score = min(100, 50 + uc.total_credits / 10 + uc.verifications_received * 2)

    # Track contribution
    contrib = Contribution(
        user_id=user_id,
        contrib_type=action,
        entity_name=entity_name,
        entity_label=entity_label,
        credits_earned=earned,
    )
    db.session.add(contrib)
    db.session.commit()
    return earned


def verify_contribution(verifier_id: int, contrib_id: int, entity_name: str = "", comment: str = "") -> int:
    # Award to verifier
    verifier_uc = get_or_create_credit(verifier_id)
    verifier_uc.total_credits += CREDIT_RULES["verify_others"]
    verifier_uc.verifications_given += 1

    # Award to original contributor
    contrib = Contribution.query.get(contrib_id)
    if contrib:
        contrib.verified_count += 1
        contrib_uc = get_or_create_credit(contrib.user_id)
        contrib_uc.total_credits += CREDIT_RULES["verified_by_peer"]
        contrib_uc.verifications_received += 1

    # Record verification
    v = Verification(
        user_id=verifier_id,
        contribution_id=contrib_id,
        entity_name=entity_name,
        comment=comment,
    )
    db.session.add(v)
    db.session.commit()
    return CREDIT_RULES["verify_others"]


def award_referral(referrer_id: int, new_user_id: int) -> tuple[int, int]:
    ref_earned = CREDIT_RULES["referral"]
    new_earned = CREDIT_RULES["referral"]
    award_credits(referrer_id, "referral", f"referred_user_{new_user_id}")
    award_credits(new_user_id, "referral", f"referred_by_{referrer_id}")
    return ref_earned, new_earned


def get_leaderboard(limit: int = 20) -> list[dict]:
    credits = (
        UserCredit.query
        .order_by(UserCredit.reputation_score.desc())
        .limit(limit)
        .all()
    )
    result = []
    for rank, uc in enumerate(credits, 1):
        user = User.query.get(uc.user_id)
        result.append({
            "rank": rank,
            "username": user.username if user else "unknown",
            "reputation_score": round(uc.reputation_score, 1),
            "total_credits": uc.total_credits,
            "contributions_count": uc.contributions_count,
            "verifications_received": uc.verifications_received,
            "company": uc.company or "",
            "role": uc.role or "",
            "is_verified_pro": uc.is_verified_pro,
            "badges": json.loads(uc.domain_badges or "[]"),
        })
    return result


def get_user_credit(user_id: int) -> dict | None:
    uc = UserCredit.query.filter_by(user_id=user_id).first()
    if not uc:
        return None

    user = User.query.get(user_id)
    recent = (
        Contribution.query
        .filter_by(user_id=user_id)
        .order_by(Contribution.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "user": user.to_dict() if user else {},
        "credits": uc.to_dict(),
        "rank": UserCredit.query.filter(
            UserCredit.reputation_score > uc.reputation_score
        ).count() + 1,
        "recent_contributions": [
            {
                "id": c.id,
                "type": c.contrib_type,
                "entity_name": c.entity_name,
                "entity_label": c.entity_label,
                "credits_earned": c.credits_earned,
                "verified_count": c.verified_count,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in recent
        ],
    }
