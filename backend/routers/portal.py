from fastapi import APIRouter, Depends, HTTPException
from models.base import db
from models.sales import QuotationStatus, Quotation
from dependencies import RoleChecker, get_current_user
from models.users import RoleEnum
from services.discount_engine import calculate_blended_risk_score
from services.routing_engine import determine_approval_routing
from services.billing_engine import generate_invoices_and_schedules
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class NegotiationRequest(BaseModel):
    proposed_discounts: dict = {}  # line_id -> new_discount_percent

class CounterProposalRequest(BaseModel):
    note: str = ""

@router.get("/quotes/{quotation_id}")
def get_customer_quote(quotation_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.customer]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation or quotation["customer_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Quotation not found")
    from routers.quotations import _enrich_quotation
    return _enrich_quotation(quotation)

@router.post("/quotes/{quotation_id}/negotiate")
def negotiate_quote(quotation_id: str, body: NegotiationRequest, current_user: dict = Depends(RoleChecker([RoleEnum.customer]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation or quotation["customer_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Quotation not found")

    for line in quotation["lines"]:
        if line["id"] in body.proposed_discounts:
            new_disc = body.proposed_discounts[line["id"]]
            line["discount"] = new_disc
            line["discount_percent"] = new_disc
            # Re-flag
            cat = line.get("category", "")
            all_ceilings = db.list("category_discount_ceilings")
            for cc in all_ceilings:
                if cc.get("category") == cat:
                    if new_disc > cc.get("max_discount_percent", 100):
                        line["flagged"] = True
                        line["flagReason"] = f"Exceeds {cc['max_discount_percent']}% {cat.lower()} discount threshold"
                    else:
                        line["flagged"] = False
                        line["flagReason"] = None
                    break

    q_model = Quotation(**quotation)
    score = calculate_blended_risk_score(q_model)

    quotation["blended_risk_score"] = score
    quotation["status"] = QuotationStatus.NEGOTIATION.value
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)

    from routers.quotations import _enrich_quotation
    return _enrich_quotation(quotation)

@router.post("/quotes/{quotation_id}/counter")
def submit_counter_proposal(quotation_id: str, body: CounterProposalRequest, current_user: dict = Depends(RoleChecker([RoleEnum.customer]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation or quotation["customer_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Quotation not found")

    quotation["status"] = QuotationStatus.NEGOTIATION.value
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)

    from routers.quotations import _enrich_quotation
    return _enrich_quotation(quotation)

@router.post("/quotes/{quotation_id}/confirm")
def confirm_quote(quotation_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.customer]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation or quotation["customer_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Quotation not found")

    # Check thresholds
    q_model = Quotation(**quotation)
    required_status = determine_approval_routing(q_model.blended_risk_score)

    if required_status != QuotationStatus.READY:
        quotation["status"] = required_status.value
        db.update("quotations", quotation_id, quotation)
        from routers.quotations import _enrich_quotation
        return {"message": "Quotation re-entered approval flow due to thresholds", "quotation": _enrich_quotation(quotation)}

    quotation["status"] = QuotationStatus.WON.value
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)

    generate_invoices_and_schedules(quotation_id)

    from routers.quotations import _enrich_quotation
    return {"message": "Quotation confirmed", "quotation": _enrich_quotation(quotation)}
