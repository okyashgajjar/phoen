from fastapi import APIRouter, Depends, HTTPException
from models.base import db
from models.sales import Quotation, QuotationStatus, QuotationLine, QuotationLineIn, STATUS_LABELS
from dependencies import get_current_user, RoleChecker
from models.users import RoleEnum
from services.discount_engine import calculate_blended_risk_score
from services.routing_engine import determine_approval_routing
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import uuid

router = APIRouter()

# ─── Avatar map (same as seed.py) ───
AVATARS = {
    "Marcus Vance": "https://lh3.googleusercontent.com/aida-public/AB6AXuAPPCmZWSHv5-hqsV8B7a1ZAECPiQItn-WV9xogMiJF9w-Wwv0lW7nz_la1neL_umllylkeWsgu_7FSD2pOWnm8q6XPvfiKqQhyu7j1xzouHlH_s2STTn1V9JHHdo0Eu0j3SAECmMOP6qrMR_PrChQgZgSVqVy4tyYNOMJUlvjFrvny8XcszlX1_cJIy-5LvL05M6wWURQqleEiw4-DcrpFqbL078c-3nWaf7c9-9c1r63DGe_rRAUQ",
    "Rachel Torres": "https://lh3.googleusercontent.com/aida-public/AB6AXuDDy3o_lnWgGPSUoB6P7Lp4hkbJFgtCgcakv09lYBTZEbeu45LrPMl-4j7D0fkePZHXv0SFP1ARMob5zvodbhlCTX9_i_ZNXVUl4gOB_g-RzHoTv_zqTypCWZyAlVCatqoMEUNzUaJds22kANc4-RQ4UwSK9Du9ZPIAiPkL-Q40vCvfw9YyzywdZ9NKDCgjYbrQatymSh81iyvilkTl4OuioHwk3E6wEqqj5gaJi_EYElr5UK2kTIkQ",
    "David Chen": "https://lh3.googleusercontent.com/aida-public/AB6AXuD6eGnNwcM2SWzLN7P5S_9fzAl71lAafDpxahswhQgzYLqqw_UYITDveOBT58W0KmwcQOrX4LYatjjzmk-y6DwcLx5R6RAk3k2dcTlzY52hxYLej98xxzfmBXfxl9rP__hIUR_nV7p524_UzAOEL4XkKSANGLIb6NcLx8gG654E6TSYV8JuaKRPE4Qdpu6MXyn18gJuHb1pLmcnJBQixHFZG3WZUz9Ina6EKZp_uqg8Z0hEccvcG-HL",
    "Sarah Jenkins": "https://lh3.googleusercontent.com/aida-public/AB6AXuD6eGnNwcM2SWzLN7P5S_9fzAl71lAafDpxahswhQgzYLqqw_UYITDveOBT58W0KmwcQOrX4LYatjjzmk-y6DwcLx5R6RAk3k2dcTlzY52hxYLej98xxzfmBXfxl9rP__hIUR_nV7p524_UzAOEL4XkKSANGLIb6NcLx8gG654E6TSYV8JuaKRPE4Qdpu6MXyn18gJuHb1pLmcnJBQixHFZG3WZUz9Ina6EKZp_uqg8Z0hEccvcG-HL",
}

def _relative_time(dt):
    """Convert datetime to relative time string like '2h ago'."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    delta = datetime.utcnow() - dt
    if delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    hours = delta.seconds // 3600
    if hours > 0:
        return f"{hours}h ago"
    minutes = delta.seconds // 60
    return f"{minutes}m ago"

def _enrich_quotation(q: dict) -> dict:
    """Enrich a raw quotation dict with frontend-expected fields."""
    # Customer name
    customer = db.get("users", q.get("customer_id", ""))
    q["account"] = customer.get("name", "Unknown") if customer else "Unknown"

    # Rep name and avatar
    rep = db.get("users", q.get("sales_rep_id", ""))
    rep_name = rep.get("name", "Unknown") if rep else "Unknown"
    q["rep"] = rep_name
    q["repAvatar"] = AVATARS.get(rep_name, "")

    # Status label
    q["statusLabel"] = STATUS_LABELS.get(q.get("status", ""), q.get("status", ""))

    # Items count
    q["items"] = q.get("items", len(q.get("lines", [])))

    # Amount — compute from lines if not already set
    if not q.get("amount"):
        total = 0.0
        for line in q.get("lines", []):
            qty = line.get("qty", line.get("quantity", 0))
            price = line.get("unit_price", line.get("unitPrice", 0))
            disc = line.get("discount", line.get("discount_percent", 0))
            total += qty * price * (1 - disc / 100.0)
        q["amount"] = round(total, 2)

    # Flagged status
    has_flag = any(line.get("flagged") for line in q.get("lines", []))
    if not q.get("flagged"):
        q["flagged"] = has_flag
    if has_flag and not q.get("flagReason"):
        for line in q.get("lines", []):
            if line.get("flagged"):
                q["flagReason"] = line.get("flagReason", "")
                break

    # Portal active
    q["portalActive"] = q.get("status") == "NEGOTIATION"

    # Time
    q["time"] = _relative_time(q.get("updated_at", datetime.utcnow()))

    return q


# ─── Quote ID counter ───
_quote_counter = 1050

class CreateQuotationRequest(BaseModel):
    customer_id: str
    title: str = "New Proposal"

@router.get("/")
def list_quotations(current_user: dict = Depends(get_current_user)):
    all_quotes = db.list("quotations")
    if current_user["role"] == RoleEnum.sales_rep.value:
        all_quotes = [q for q in all_quotes if q["sales_rep_id"] == current_user["id"]]
    elif current_user["role"] == RoleEnum.customer.value:
        all_quotes = [q for q in all_quotes if q["customer_id"] == current_user["id"]]
    return [_enrich_quotation(q) for q in all_quotes]

@router.get("/{quotation_id}")
def get_quotation(quotation_id: str, current_user: dict = Depends(get_current_user)):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return _enrich_quotation(quotation)

@router.post("/")
def create_quotation(req: CreateQuotationRequest, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin]))):
    global _quote_counter
    q_id = f"Q-{_quote_counter}"
    _quote_counter += 1
    quotation = {
        "id": q_id,
        "customer_id": req.customer_id,
        "sales_rep_id": current_user["id"],
        "status": QuotationStatus.DRAFT.value,
        "title": req.title,
        "lines": [],
        "blended_risk_score": 0.0,
        "amount": 0,
        "margin": "0.0%",
        "items": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db.insert("quotations", q_id, quotation)
    return _enrich_quotation(quotation)

@router.post("/{quotation_id}/lines")
def add_line(quotation_id: str, line: QuotationLineIn, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if quotation["status"] not in [QuotationStatus.DRAFT.value, QuotationStatus.NEGOTIATION.value]:
        raise HTTPException(status_code=400, detail="Cannot edit quotation in this status")

    # Lookup product details
    product = db.get("products", line.product_id)
    p_name = product.get("name", "") if product else ""
    p_category = product.get("category", "") if product else ""

    # Check if flagged
    flagged = False
    flag_reason = None
    # Category ceiling
    all_ceilings = db.list("category_discount_ceilings")
    for cc in all_ceilings:
        if cc.get("category") == p_category:
            if line.discount_percent > cc.get("max_discount_percent", 100):
                flagged = True
                flag_reason = f"Exceeds {cc['max_discount_percent']}% {p_category.lower()} discount threshold"
            break

    line_id = str(uuid.uuid4())[:8]
    line_dict = {
        "id": line_id,
        "sku": line.product_id,
        "name": p_name,
        "category": p_category,
        "product_id": line.product_id,
        "qty": line.quantity,
        "unit_price": line.unit_price,
        "unitPrice": line.unit_price,
        "discount": line.discount_percent,
        "discount_percent": line.discount_percent,
        "flagged": flagged,
        "flagReason": flag_reason,
        "is_recurring": line.is_recurring,
    }
    quotation["lines"].append(line_dict)

    # Recalculate blended risk score
    q_model = Quotation(**quotation)
    score = calculate_blended_risk_score(q_model)

    quotation["blended_risk_score"] = score
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)

    return _enrich_quotation(quotation)

class UpdateLineRequest(BaseModel):
    qty: Optional[int] = None
    discount: Optional[float] = None

@router.put("/{quotation_id}/lines/{line_id}")
def update_line(quotation_id: str, line_id: str, update: UpdateLineRequest, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    for line in quotation["lines"]:
        if line["id"] == line_id:
            if update.qty is not None:
                line["qty"] = max(1, update.qty)
            if update.discount is not None:
                disc = min(100, max(0, update.discount))
                line["discount"] = disc
                line["discount_percent"] = disc
                # Re-check flag
                cat = line.get("category", "")
                all_ceilings = db.list("category_discount_ceilings")
                for cc in all_ceilings:
                    if cc.get("category") == cat:
                        if disc > cc.get("max_discount_percent", 100):
                            line["flagged"] = True
                            line["flagReason"] = f"Exceeds {cc['max_discount_percent']}% {cat.lower()} discount threshold"
                        else:
                            line["flagged"] = False
                            line["flagReason"] = None
                        break
            break
    else:
        raise HTTPException(status_code=404, detail="Line not found")

    # Recalculate
    q_model = Quotation(**quotation)
    quotation["blended_risk_score"] = calculate_blended_risk_score(q_model)
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)
    return _enrich_quotation(quotation)

@router.post("/{quotation_id}/submit")
def submit_quotation(quotation_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    q_model = Quotation(**quotation)
    new_status = determine_approval_routing(q_model.blended_risk_score)

    quotation["status"] = new_status.value
    quotation["updated_at"] = datetime.utcnow()
    db.update("quotations", quotation_id, quotation)

    return _enrich_quotation(quotation)
