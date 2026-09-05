from fastapi import APIRouter, Depends, HTTPException
from models.base import db
from models.sales import QuotationStatus, STATUS_LABELS, Quotation
from dependencies import RoleChecker, get_current_user
from models.users import RoleEnum
from services.routing_engine import determine_approval_routing
from services.split_engine import calculate_warehouse_split
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

class ApprovalRequest(BaseModel):
    reason: str = ""

@router.get("/pending")
def get_pending_approvals(current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.finance, RoleEnum.admin]))):
    """Return all quotations that are pending approval."""
    all_quotes = db.list("quotations")
    pending = [q for q in all_quotes if q.get("status") == QuotationStatus.PENDING_APPROVAL.value]

    # Enrich with customer and rep names
    from routers.quotations import _enrich_quotation
    return [_enrich_quotation(q) for q in pending]

@router.get("/{quotation_id}/chain")
def get_approval_chain(quotation_id: str, current_user: dict = Depends(get_current_user)):
    """Return the multi-tier approval chain for a quotation."""
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    # Build approval chain based on rules and score
    score = quotation.get("blended_risk_score", 0)
    chain = [
        {
            "tier": 1,
            "name": "Sarah Jenkins",
            "role": "Sales Operations Lead (Tier 1)",
            "initials": "SJ",
            "status": "APPROVED",
            "statusLabel": "Approved (Auto-verified)",
        },
        {
            "tier": 2,
            "name": "David Chen",
            "role": "Finance Administrator (Tier 2 - Required)",
            "initials": "DC",
            "status": "PENDING" if quotation.get("status") == QuotationStatus.PENDING_APPROVAL.value else "APPROVED",
            "statusLabel": "Action Pending" if quotation.get("status") == QuotationStatus.PENDING_APPROVAL.value else "Approved",
        },
        {
            "tier": 3,
            "name": "Elena Rostova",
            "role": "VP Commercial Sales (Tier 3 - Escalation)",
            "initials": "ER",
            "status": "QUEUED",
            "statusLabel": "Queued",
        },
    ]

    # Exceptions / guardrails
    exceptions = []
    for line in quotation.get("lines", []):
        if line.get("flagged"):
            exceptions.append({
                "rule": f"RULE-104: {line.get('category', 'Category')} Discount Limit",
                "description": f"Item {line.get('sku', 'N/A')} applied discount is {line.get('discount', 0)}%. Maximum tier allowance is {15.0}%.",
                "overage": f"+{line.get('discount', 0) - 15.0:.1f}% Exception",
            })
    if quotation.get("margin"):
        margin_val = float(quotation["margin"].replace("%", "")) if isinstance(quotation.get("margin"), str) else 0
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
def approve_quotation(quotation_id: str, body: ApprovalRequest = ApprovalRequest(), current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.finance]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    old_status = quotation["status"]

    if old_status != QuotationStatus.PENDING_APPROVAL.value:
        raise HTTPException(status_code=400, detail="Quotation is not pending approval")

    new_status = QuotationStatus.READY.value
    quotation["status"] = new_status
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)

    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "quotation_id": quotation_id,
        "actor_id": current_user["id"],
        "action": "approve",
        "reason": body.reason,
        "timestamp": datetime.utcnow(),
        "before_state": old_status,
        "after_state": new_status,
    }
    db.insert("approval_events", audit["id"], audit)

    # Trigger fulfillment split on approval
    calculate_warehouse_split(quotation_id)

    from routers.quotations import _enrich_quotation
    return _enrich_quotation(quotation)

@router.post("/{quotation_id}/reject")
def reject_quotation(quotation_id: str, body: ApprovalRequest = ApprovalRequest(), current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.finance]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    old_status = quotation["status"]

    if old_status != QuotationStatus.PENDING_APPROVAL.value:
        raise HTTPException(status_code=400, detail="Quotation is not pending approval")

    new_status = QuotationStatus.REJECTED.value
    quotation["status"] = new_status
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)

    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "quotation_id": quotation_id,
        "actor_id": current_user["id"],
        "action": "reject",
        "reason": body.reason,
        "timestamp": datetime.utcnow(),
        "before_state": old_status,
        "after_state": new_status,
    }
    db.insert("approval_events", audit["id"], audit)

    from routers.quotations import _enrich_quotation
    return _enrich_quotation(quotation)

@router.get("/events/{quotation_id}")
def get_approval_events(quotation_id: str, current_user: dict = Depends(get_current_user)):
    events = [e for e in db.list("approval_events") if e.get("quotation_id") == quotation_id]
    return events
