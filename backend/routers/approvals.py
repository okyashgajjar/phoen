from fastapi import APIRouter, Depends, HTTPException
from models.base import db
from models.sales import QuotationStatus, STATUS_LABELS, Quotation
from dependencies import RoleChecker, get_current_user
from models.users import RoleEnum
from services.routing_engine import determine_approval_routing
from services.split_engine import calculate_warehouse_split
from pydantic import BaseModel
from datetime import timezone, datetime
import uuid

router = APIRouter()

class ApprovalRequest(BaseModel):
    reason: str = ""

@router.get("/pending")
def get_pending_approvals(current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.finance, RoleEnum.admin]))):
    """Return quotations pending approval, filtered appropriately for the role."""
    all_quotes = db.list("quotations")
    pending = [q for q in all_quotes if q.get("status") == QuotationStatus.PENDING_APPROVAL.value]

    role = current_user.get("role")
    # Finance reviews Tier 2 / high-risk / low-margin quotations
    if role == RoleEnum.finance.value:
        pending = [
            q for q in pending 
            if q.get("blended_risk_score", 0) > 5.0 
            or (float(str(q.get("margin", "35%")).replace("%", "")) < 30.0 if "margin" in q else False)
            or any(line.get("flagged") for line in q.get("lines", []))
        ]

    # Enrich with customer and rep names
    from routers.quotations import _enrich_quotation
    return [_enrich_quotation(q) for q in pending]

@router.get("/{quotation_id}/chain")
def get_approval_chain(quotation_id: str, current_user: dict = Depends(get_current_user)):
    """Return the multi-tier approval chain for a quotation."""
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    # Build approval chain based on rules, scores, and status
    score = quotation.get("blended_risk_score", 0)
    status = quotation.get("status", "DRAFT")
    is_pending = (status == QuotationStatus.PENDING_APPROVAL.value)
    is_approved = (status in [QuotationStatus.READY.value, QuotationStatus.WON.value, "APPROVED"])
    is_rejected = (status == QuotationStatus.REJECTED.value)

    # Tier 1: Vikramaditya Singhania (Commercial Sales Director)
    tier1_status = "PENDING" if is_pending else ("APPROVED" if is_approved else ("REJECTED" if is_rejected else "PENDING"))
    tier1_label = "Action Required (Tier 1 Sign-Off)" if is_pending else ("Approved by Sales Director" if is_approved else ("Rejected" if is_rejected else "Action Pending"))

    # Tier 2: Pooja Iyer (Finance Administrator)
    tier2_status = "APPROVED" if is_approved else ("REJECTED" if is_rejected else ("PENDING" if (is_pending and current_user.get("role") == "finance") else "QUEUED"))
    tier2_label = "Approved (Fiscal Clearance)" if is_approved else ("Rejected" if is_rejected else ("Action Required (Fiscal Floor)" if tier2_status == "PENDING" else "Queued for Fiscal Clearance"))

    # Tier 3: Arjun Mehta (VP Commercial Operations)
    tier3_status = "APPROVED" if (is_approved and float(quotation.get("amount", 0)) > 5000000) else "QUEUED"
    tier3_label = "Approved (Executive Sign-Off)" if tier3_status == "APPROVED" else "Queued (Escalation Gate)"

    chain = [
        {
            "tier": 1,
            "name": "Vikramaditya Singhania",
            "role": "Commercial Sales Director (Tier 1)",
            "initials": "VS",
            "status": tier1_status,
            "statusLabel": tier1_label,
        },
        {
            "tier": 2,
            "name": "Pooja Iyer",
            "role": "Finance Administrator (Tier 2 - Fiscal Floor)",
            "initials": "PI",
            "status": tier2_status,
            "statusLabel": tier2_label,
        },
        {
            "tier": 3,
            "name": "Arjun Mehta",
            "role": "VP Commercial Operations (Tier 3 - Escalation)",
            "initials": "AM",
            "status": tier3_status,
            "statusLabel": tier3_label,
        },
    ]

    # Exceptions / guardrails
    exceptions = []
    for line in quotation.get("lines", []):
        disc = float(line.get("discount") or line.get("discount_percent") or 0.0)
        neg_data = line.get("negotiation_data") or {}
        req_disc = float(neg_data.get("requested_discount", 0.0)) if isinstance(neg_data, dict) else 0.0

        if disc > 15.0:
            exceptions.append({
                "rule": f"RULE-104: {line.get('category', 'Hardware')} Discount Ceiling",
                "description": f"Applied discount on {line.get('name') or line.get('sku')} is {disc:.1f}%. Standard regional sales cap is 15.0%.",
                "overage": f"+{disc - 15.0:.1f}% Exception",
            })
        elif req_disc > 15.0:
            exceptions.append({
                "rule": f"RULE-108: Client Counter-Discount Request",
                "description": f"Customer requested {req_disc:.1f}% discount on {line.get('name') or line.get('sku')}. Exceeds standard ceiling.",
                "overage": f"+{req_disc - 15.0:.1f}% Requested Gap",
            })
        elif line.get("flagged"):
            exceptions.append({
                "rule": f"RULE-104: {line.get('category', 'Category')} Policy Flag",
                "description": line.get("flagReason") or f"Item {line.get('sku', 'N/A')} requires supervisory clearance.",
                "overage": f"+{disc:.1f}% Flagged",
            })

    # Blended deal health check
    deal_health = quotation.get("deal_health") or {}
    dh_score = deal_health.get("overall_score")
    if dh_score is not None and float(dh_score) < 0.35:
        exceptions.append({
            "rule": "RULE-208: Blended Margin Floor & Deal Sentinel",
            "description": deal_health.get("recommended_action") or "Proposal overall health score is critical. Margin floor requires Director sign-off.",
            "overage": f"Health: {int(float(dh_score) * 100)}/100",
        })
    elif quotation.get("margin"):
        margin_val = float(str(quotation["margin"]).replace("%", "")) if isinstance(quotation.get("margin"), str) else 0
        if margin_val < 35.0:
            exceptions.append({
                "rule": "RULE-208: Blended Margin Floor",
                "description": f"Proposal blended margin is {quotation['margin']}. Standard enterprise target threshold is 35.0%.",
                "overage": f"-{35.0 - margin_val:.1f}% Below Floor",
            })

    return {
        "quotation_id": quotation_id,
        "blended_risk_score": score,
        "chain": chain,
        "exceptions": exceptions,
    }

@router.post("/{quotation_id}/approve")
def approve_quotation(quotation_id: str, body: ApprovalRequest = ApprovalRequest(), current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.finance, RoleEnum.admin]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    old_status = quotation["status"]

    if old_status != QuotationStatus.PENDING_APPROVAL.value:
        raise HTTPException(status_code=400, detail="Quotation is not pending approval")

    new_status = QuotationStatus.READY.value
    quotation["status"] = new_status
    actor_name = current_user.get("name") or "Vikramaditya Singhania"
    quotation["approval_status"] = f"Approved by {actor_name}"
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)

    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "quotation_id": quotation_id,
        "entity_type": "quotation",
        "entity_id": quotation_id,
        "actor_id": actor_name,
        "actor_role": current_user.get("role", "manager"),
        "action": "approve",
        "reason": body.reason or "Authorized under regional sales quota allowances",
        "timestamp": datetime.now(timezone.utc),
        "before_state": old_status,
        "after_state": new_status,
    }
    db.insert("approval_events", audit["id"], audit)

    # Trigger fulfillment split on approval
    calculate_warehouse_split(quotation_id)

    from routers.quotations import _enrich_quotation
    return _enrich_quotation(quotation)

@router.post("/{quotation_id}/reject")
def reject_quotation(quotation_id: str, body: ApprovalRequest = ApprovalRequest(), current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.finance, RoleEnum.admin]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    old_status = quotation["status"]

    if old_status != QuotationStatus.PENDING_APPROVAL.value:
        raise HTTPException(status_code=400, detail="Quotation is not pending approval")

    new_status = QuotationStatus.REJECTED.value
    quotation["status"] = new_status
    actor_name = current_user.get("name") or "Vikramaditya Singhania"
    quotation["approval_status"] = f"Rejected by {actor_name}"
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)

    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "quotation_id": quotation_id,
        "entity_type": "quotation",
        "entity_id": quotation_id,
        "actor_id": actor_name,
        "actor_role": current_user.get("role", "manager"),
        "action": "reject",
        "reason": body.reason or "Discount exception rejected; quote restructured",
        "timestamp": datetime.now(timezone.utc),
        "before_state": old_status,
        "after_state": new_status,
    }
    db.insert("approval_events", audit["id"], audit)

    from routers.quotations import _enrich_quotation
    return _enrich_quotation(quotation)

@router.get("/events")
def get_all_approval_events(current_user: dict = Depends(get_current_user)):
    events = db.list("approval_events")
    return events[:50]

@router.get("/events/{quotation_id}")
def get_approval_events(quotation_id: str, current_user: dict = Depends(get_current_user)):
    events = [e for e in db.list("approval_events") if e.get("quotation_id") == quotation_id]
    return events
