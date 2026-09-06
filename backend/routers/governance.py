"""
Discount Governance — tier ceilings, category ceilings and approval chains.

Backs mockup Screen 18 ("Discount tiers and approval chains"). Everything the
approval flow depends on is edited here rather than in SQL:

  * per-tier discount ceilings
  * per-category ceilings, and the tier x category overrides that beat both
  * the approval bands that decide who signs off at what discount level

Every write goes through the audit ledger with user, timestamp and reason, which
is the spec's requirement that "all approvals, rejections, and edits must be
logged".
"""

import os
import sys
import uuid
from datetime import timezone, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import PricingRule, Category, Customer, ApprovalChainConfig, AuditLog
from dependencies import RoleChecker
from models.users import RoleEnum
from services.routing_engine import MANAGER_BAND

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────────────────────────────
class CeilingIn(BaseModel):
    tier: Optional[str] = None
    category_id: Optional[str] = None
    max_discount_percent: float = Field(ge=0, le=100)
    min_margin_percent: Optional[float] = Field(default=None, ge=0, le=100)
    approval_level: Optional[str] = None


class CeilingsUpdate(BaseModel):
    ceilings: list[CeilingIn]
    reason: Optional[str] = None


class ChainBandIn(BaseModel):
    id: Optional[str] = None
    approval_level: str
    role_name: str
    min_discount_percent: float = Field(ge=0, le=100)
    max_discount_percent: float = Field(ge=0, le=100)
    min_margin_percent: float = Field(default=0.0, ge=0, le=100)
    approver_role: Optional[str] = None
    description: Optional[str] = None
    active: bool = True


class ChainsUpdate(BaseModel):
    bands: list[ChainBandIn]
    reason: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────
def _f(v, default=0.0):
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _audit(session, entity_type, entity_id, action, old, new, user, reason):
    session.add(AuditLog(
        id=f"AUD-{uuid.uuid4().hex[:12].upper()}",
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        old_value=old,
        new_value=new,
        performed_by=(user.get("name") or user.get("email") or "system"),
        reason=reason,
        timestamp=datetime.now(timezone.utc),
    ))


def _rule_id(tier: Optional[str], category_id: Optional[str]) -> str:
    scope = f"{tier or 'ALL'}-{category_id or 'ALL'}".upper().replace(" ", "_")
    return f"DL-{scope}"


# ─────────────────────────────────────────────────────────────────────
# Read
# ─────────────────────────────────────────────────────────────────────
@router.get("/config")
def get_governance_config(
    current_user: dict = Depends(RoleChecker([RoleEnum.admin, RoleEnum.manager, RoleEnum.finance])),
):
    """
    The whole governance picture in one payload: the tiers and categories in
    use, every discount ceiling currently in force, and the approval bands.
    """
    session = SessionLocal()
    try:
        tiers = sorted({t[0] for t in session.query(Customer.tier).distinct() if t[0]})
        categories = [
            {"id": c.id, "name": c.name}
            for c in session.query(Category).order_by(Category.id).all()
        ]

        rules = (
            session.query(PricingRule)
            .filter(PricingRule.rule_type == "DISCOUNT_LIMIT")
            .filter(PricingRule.active.is_(True))
            .all()
        )

        tier_ceilings, category_ceilings, matrix, global_ceiling = {}, {}, {}, None
        for r in rules:
            tier = r.customer_tier or (r.scope_id if r.scope_type == "TIER" else None)
            cat = r.category_id
            entry = {
                "rule_id": r.id,
                "max_discount_percent": _f(r.max_discount_percent),
                "min_margin_percent": _f(r.min_margin_percent),
                "approval_level": r.approval_level,
            }
            if tier and cat:
                matrix[f"{tier}|{cat}"] = entry
            elif cat:
                category_ceilings[cat] = entry
            elif tier:
                tier_ceilings[tier] = entry
            else:
                global_ceiling = entry

        bands = [
            {
                "id": b.id,
                "approval_level": b.approval_level,
                "role_name": b.role_name,
                "min_discount_percent": _f(b.min_discount_percent),
                "max_discount_percent": _f(b.max_discount_percent),
                "min_margin_percent": _f(b.min_margin_percent),
                "approver_role": b.approver_role,
                "description": b.description,
                "active": bool(b.active),
            }
            for b in session.query(ApprovalChainConfig)
            .order_by(ApprovalChainConfig.min_discount_percent)
            .all()
        ]

        return {
            "tiers": tiers,
            "categories": categories,
            "tier_ceilings": tier_ceilings,
            "category_ceilings": category_ceilings,
            "tier_category_matrix": matrix,
            "global_ceiling": global_ceiling,
            "approval_bands": bands,
            "routing": {
                "manager_band_points": MANAGER_BAND,
                "explanation": (
                    "A quotation is scored in discount points over whichever ceiling "
                    "applies to each line. Zero means no approval is needed. Up to "
                    f"{MANAGER_BAND} points routes to the Sales Manager. Beyond that, "
                    "or on any breach of a rule marked for Finance, it routes to the "
                    "Sales Manager and then Finance."
                ),
            },
        }
    finally:
        session.close()


# ─────────────────────────────────────────────────────────────────────
# Write — ceilings
# ─────────────────────────────────────────────────────────────────────
@router.put("/ceilings")
def update_ceilings(
    payload: CeilingsUpdate,
    current_user: dict = Depends(RoleChecker([RoleEnum.admin, RoleEnum.finance])),
):
    """
    Upsert discount ceilings. Each entry is scoped by tier, category, both
    (a tier x category override) or neither (the global backstop).

    The next quotation recalculation picks these up immediately — the rule book
    is rebuilt per scoring pass, so there is nothing to restart.
    """
    if not payload.ceilings:
        raise HTTPException(status_code=400, detail="No ceilings supplied")

    session = SessionLocal()
    written = []
    try:
        for c in payload.ceilings:
            scope_type = (
                "TIER" if c.tier and not c.category_id else
                "CATEGORY" if c.category_id and not c.tier else
                "TIER" if c.tier and c.category_id else
                "GLOBAL"
            )
            rid = _rule_id(c.tier, c.category_id)
            existing = session.query(PricingRule).filter(PricingRule.id == rid).first()

            old = None
            if existing is not None:
                old = {
                    "max_discount_percent": _f(existing.max_discount_percent),
                    "min_margin_percent": _f(existing.min_margin_percent),
                    "approval_level": existing.approval_level,
                }
                existing.max_discount_percent = c.max_discount_percent
                if c.min_margin_percent is not None:
                    existing.min_margin_percent = c.min_margin_percent
                if c.approval_level is not None:
                    existing.approval_level = c.approval_level
                existing.active = True
                action = "UPDATE"
            else:
                session.add(PricingRule(
                    id=rid,
                    name=f"Discount ceiling {c.tier or 'all tiers'} / {c.category_id or 'all categories'}",
                    rule_type="DISCOUNT_LIMIT",
                    scope_type=scope_type,
                    scope_id=c.tier or c.category_id,
                    customer_tier=c.tier,
                    category_id=c.category_id,
                    max_discount_percent=c.max_discount_percent,
                    min_margin_percent=c.min_margin_percent or 0.0,
                    approval_level=c.approval_level,
                    currency="INR",
                    active=True,
                ))
                action = "CREATE"

            _audit(
                session, "PRICING_RULE", rid, action, old,
                {
                    "max_discount_percent": c.max_discount_percent,
                    "min_margin_percent": c.min_margin_percent,
                    "approval_level": c.approval_level,
                    "tier": c.tier,
                    "category_id": c.category_id,
                },
                current_user,
                payload.reason or "Discount ceiling updated from governance screen",
            )
            written.append(rid)

        session.commit()
        return {"updated": written, "count": len(written)}
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Could not save ceilings: {exc}")
    finally:
        session.close()


@router.delete("/ceilings/{rule_id}")
def delete_ceiling(
    rule_id: str,
    current_user: dict = Depends(RoleChecker([RoleEnum.admin])),
):
    """Retire a ceiling. Deactivated rather than deleted, so the audit trail keeps its referent."""
    session = SessionLocal()
    try:
        rule = session.query(PricingRule).filter(PricingRule.id == rule_id).first()
        if rule is None:
            raise HTTPException(status_code=404, detail="Ceiling not found")
        rule.active = False
        _audit(session, "PRICING_RULE", rule_id, "DEACTIVATE",
               {"active": True}, {"active": False}, current_user,
               "Ceiling retired from governance screen")
        session.commit()
        return {"deactivated": rule_id}
    finally:
        session.close()


# ─────────────────────────────────────────────────────────────────────
# Write — approval chain
# ─────────────────────────────────────────────────────────────────────
@router.put("/approval-chain")
def update_approval_chain(
    payload: ChainsUpdate,
    current_user: dict = Depends(RoleChecker([RoleEnum.admin, RoleEnum.finance])),
):
    """Replace the approval bands. Overlapping or inverted bands are rejected."""
    bands = sorted(payload.bands, key=lambda b: b.min_discount_percent)

    for b in bands:
        if b.max_discount_percent < b.min_discount_percent:
            raise HTTPException(
                status_code=400,
                detail=f"Band {b.approval_level}: max ({b.max_discount_percent}) is below min ({b.min_discount_percent})",
            )
    for a, b in zip(bands, bands[1:]):
        if b.min_discount_percent <= a.max_discount_percent:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Bands overlap: {a.approval_level} ends at {a.max_discount_percent}% "
                    f"but {b.approval_level} starts at {b.min_discount_percent}%"
                ),
            )

    session = SessionLocal()
    try:
        existing = {b.id: b for b in session.query(ApprovalChainConfig).all()}
        kept = set()

        for idx, b in enumerate(bands, start=1):
            bid = b.id or f"AC-{idx:03d}"
            kept.add(bid)
            row = existing.get(bid)
            old = None
            if row is not None:
                old = {
                    "min": _f(row.min_discount_percent),
                    "max": _f(row.max_discount_percent),
                    "approver_role": row.approver_role,
                }
                row.approval_level = b.approval_level
                row.role_name = b.role_name
                row.min_discount_percent = b.min_discount_percent
                row.max_discount_percent = b.max_discount_percent
                row.min_margin_percent = b.min_margin_percent
                row.approver_role = b.approver_role
                row.description = b.description
                row.active = b.active
                action = "UPDATE"
            else:
                session.add(ApprovalChainConfig(
                    id=bid,
                    approval_level=b.approval_level,
                    role_name=b.role_name,
                    min_discount_percent=b.min_discount_percent,
                    max_discount_percent=b.max_discount_percent,
                    min_margin_percent=b.min_margin_percent,
                    approver_role=b.approver_role,
                    description=b.description,
                    active=b.active,
                ))
                action = "CREATE"

            _audit(session, "APPROVAL_CHAIN", bid, action, old,
                   {
                       "min": b.min_discount_percent,
                       "max": b.max_discount_percent,
                       "approver_role": b.approver_role,
                   },
                   current_user,
                   payload.reason or "Approval chain updated from governance screen")

        for bid, row in existing.items():
            if bid not in kept:
                row.active = False
                _audit(session, "APPROVAL_CHAIN", bid, "DEACTIVATE",
                       {"active": True}, {"active": False}, current_user,
                       "Band removed from governance screen")

        session.commit()
        return {"bands": len(bands)}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Could not save approval chain: {exc}")
    finally:
        session.close()


# ─────────────────────────────────────────────────────────────────────
# Impact preview
# ─────────────────────────────────────────────────────────────────────
@router.get("/impact")
def governance_impact(
    current_user: dict = Depends(RoleChecker([RoleEnum.admin, RoleEnum.manager, RoleEnum.finance])),
):
    """
    How the ceilings currently in force score the live pipeline: how many open
    quotations would need no approval, a manager, or manager plus finance.

    Lets an admin see what a ceiling change actually does before standing behind
    it, rather than discovering it one deal at a time.
    """
    from models.base import db
    from models.sales import Quotation
    from services.discount_engine import evaluate_quotation
    from services.routing_engine import required_role, risk_band

    buckets = {"none": 0, "manager": 0, "finance": 0}
    worst = []

    for q in db.list("quotations"):
        if not q.get("lines"):
            continue
        try:
            ev = evaluate_quotation(Quotation(**q))
        except Exception:
            continue
        role = required_role(ev)
        buckets["none" if role is None else role] += 1
        if ev["score"] > 0:
            worst.append({
                "quotation_id": q.get("id"),
                "account": q.get("account"),
                "score": ev["score"],
                "band": risk_band(ev["score"]),
                "breached_lines": ev["breached_lines"],
                "tier": ev["tier"],
            })

    worst.sort(key=lambda x: x["score"], reverse=True)
    total = sum(buckets.values())
    return {
        "evaluated": total,
        "auto_approved": buckets["none"],
        "needs_manager": buckets["manager"],
        "needs_finance": buckets["finance"],
        "auto_approved_pct": round(buckets["none"] / total * 100, 1) if total else 0.0,
        "top_breaches": worst[:10],
    }
