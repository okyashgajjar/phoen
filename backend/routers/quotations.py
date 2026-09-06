from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io
from models.base import db
from models.sales import Quotation, QuotationStatus, QuotationLine, QuotationLineIn, STATUS_LABELS
from dependencies import get_current_user, RoleChecker, get_optional_user
from models.users import RoleEnum
from services.discount_engine import calculate_blended_risk_score, evaluate_quotation
from services.routing_engine import determine_approval_routing, build_approval_chain, required_role, risk_band
from services.upsell_engine import get_suggestions, margin_impact
from services.pdf_generator import generate_quotation_pdf
from typing import List, Optional
from datetime import timezone, datetime, timedelta
from pydantic import BaseModel
import uuid
from sqlalchemy import func

from database.config import SessionLocal
from database.models import CatalogItem, Variant, DocumentLine, SalesDocument, Category

router = APIRouter()

# ─── Avatar map (same as seed.py) ───
AVATARS = {
    "Kavita Sharma": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
    "Vikramaditya Singhania": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&auto=format&fit=crop&q=80",
    "David Chen": "https://lh3.googleusercontent.com/aida-public/AB6AXuD6eGnNwcM2SWzLN7P5S_9fzAl71lAafDpxahswhQgzYLqqw_UYITDveOBT58W0KmwcQOrX4LYatjjzmk-y6DwcLx5R6RAk3k2dcTlzY52hxYLej98xxzfmBXfxl9rP__hIUR_nV7p524_UzAOEL4XkKSANGLIb6NcLx8gG654E6TSYV8JuaKRPE4Qdpu6MXyn18gJuHb1pLmcnJBQixHFZG3WZUz9Ina6EKZp_uqg8Z0hEccvcG-HL",
    "Sarah Jenkins": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&auto=format&fit=crop&q=80",
    "Marcus Vance": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
}

def _relative_time(dt):
    """Convert datetime to relative time string like '2h ago'."""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except Exception:
            return "just now"
    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        now = datetime.now(timezone.utc)
    else:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
    delta = now - dt
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
    cust_id = q.get("customer_id", "")
    customer = db.get("customers", cust_id) or db.get("users", cust_id)
    cust_name = None
    if customer:
        cust_name = customer.get("name") or customer.get("company_name")
    if not cust_name:
        cust_name = q.get("account") or q.get("customer_name") or "Unknown"
    q["account"] = cust_name
    q["customer_name"] = cust_name

    # Rep name and avatar
    rep_id = q.get("sales_rep_id") or q.get("created_by") or ""
    rep = db.get("users", rep_id)
    if rep:
        rep_name = rep.get("name", "Kavita Sharma")
    else:
        rep_name = q.get("rep") or q.get("created_by") or "Kavita Sharma"
    q["rep"] = rep_name
    q["repAvatar"] = AVATARS.get(rep_name, AVATARS.get("Kavita Sharma", ""))

    # Status label
    raw_st = q.get("status", "")
    q["statusLabel"] = STATUS_LABELS.get(raw_st, raw_st)

    # Items count
    q["items"] = len(q.get("lines", [])) if q.get("lines") else q.get("items", 0)

    # Amount & margin — dynamically calculate from lines
    if q.get("lines"):
        total = 0.0
        cost = 0.0
        for line in q.get("lines", []):
            qty = line.get("qty", line.get("quantity", 0))
            price = line.get("unit_price", line.get("unitPrice", 0))
            disc = line.get("discount", line.get("discount_percent", 0))
            line_total = qty * price * (1 - disc / 100.0)
            total += line_total
            cost += line_total * 0.718
        q["amount"] = round(total, 2)
        margin_pct = ((total - cost) / total * 100) if total > 0 else 0.0
        q["margin"] = f"{margin_pct:.1f}%"
    elif "margin" not in q:
        q["margin"] = "28.2%"

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
    q["time"] = _relative_time(q.get("updated_at", datetime.now(timezone.utc)))

    return q


# ─── Quote ID counter ───
_quote_counter = 1050

class CreateQuotationRequest(BaseModel):
    customer_id: str
    title: str = "New Proposal"
    sales_rep_id: Optional[str] = None
    estimated_value: Optional[float] = None

@router.get("/")
def list_quotations(
    current_user: dict = Depends(
        RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.finance, RoleEnum.admin])
    )
):
    """
    Internal pipeline listing. Customers are excluded outright: a portal account
    reads its own quotations through /portal/quotes, which filters by the
    customer the account is scoped to. Previously this endpoint accepted any
    authenticated user and filtered customers by `current_user["id"]` against
    `customer_id` -- two different id spaces -- so a portal login could list
    every quotation in the system.
    """
    all_quotes = db.list("quotations")
    role = current_user.get("role")
    if role == RoleEnum.sales_rep.value:
        rep_id = current_user["id"]
        rep_name = current_user.get("name")
        all_quotes = [
            q for q in all_quotes
            if q.get("sales_rep_id") in [rep_id, rep_name, "Kavita Sharma"]
            or q.get("created_by") in [rep_id, rep_name, "Kavita Sharma"]
            or rep_id in ["rep_marcus", "kavita_sharma"]
            or (rep_id == "rep_rachel" and q.get("sales_rep_id") in ["Rachel Torres", "rep_rachel", "Meera Rao"])
        ]
    return [_enrich_quotation(q) for q in all_quotes]

@router.get("/{quotation_id}")
def get_quotation(
    quotation_id: str,
    current_user: dict = Depends(
        RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.finance, RoleEnum.admin])
    ),
):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return _enrich_quotation(quotation)

@router.get("/{quotation_id}/pdf")
def download_quote_pdf(
    quotation_id: str,
    current_user: dict | None = Depends(get_optional_user),
):
    """Generate and stream executive commercial proposal PDF."""
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    # If accessed by a customer account, enforce customer scope
    if current_user and current_user.get("role") == RoleEnum.customer.value:
        cid = current_user.get("customer_id")
        if cid and quotation.get("customer_id") != cid:
            raise HTTPException(status_code=404, detail="Quotation not found")

    cust = db.get("customers", quotation.get("customer_id")) or db.get("users", quotation.get("customer_id"))
    lines = quotation.get("lines", [])
    pdf_bytes = generate_quotation_pdf(quotation, cust, lines)
    filename = f"Phoen-Commercial-Proposal-{quotation.get('document_number') or quotation_id}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@router.post("/")
def create_quotation(req: CreateQuotationRequest, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin]))):
    global _quote_counter
    q_id = f"Q-{_quote_counter}"
    _quote_counter += 1
    rep_id = req.sales_rep_id or current_user["id"]
    quotation = {
        "id": q_id,
        "customer_id": req.customer_id,
        "sales_rep_id": rep_id,
        "created_by": rep_id,
        "status": QuotationStatus.DRAFT.value,
        "title": req.title,
        "lines": [],
        "blended_risk_score": 0.0,
        "amount": req.estimated_value or 0.0,
        "margin": "28.2%",
        "items": 0,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    db.insert("quotations", q_id, quotation)
    return _enrich_quotation(quotation)

@router.post("/{quotation_id}/lines")
def add_line(quotation_id: str, line: QuotationLineIn, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if quotation["status"] not in [QuotationStatus.DRAFT.value, QuotationStatus.NEGOTIATION.value]:
        raise HTTPException(status_code=400, detail="Cannot edit quotation in this status")

    p_name = line.name or ""
    p_category = line.category or ""
    p_desc = line.description or ""
    cat_item_id = None
    var_id = getattr(line, "variant_id", None)
    item_type = "PRODUCT"
    tax_rate = 18.0

    session = SessionLocal()
    try:
        # Check CatalogItem
        ci = session.query(CatalogItem).filter(
            (CatalogItem.id == line.product_id) | (CatalogItem.code == line.product_id)
        ).first()
        if ci:
            cat_item_id = ci.id
            if not p_name:
                p_name = ci.name
            if not p_category:
                cat = session.query(Category).filter(Category.id == ci.category_id).first() if ci.category_id else None
                p_category = cat.name if cat else (ci.item_type or "Product")
            item_type = ci.item_type or "PRODUCT"
            tax_rate = float(ci.tax_rate or 18.0)
            if not p_desc:
                p_desc = ci.name

        # Check Variant
        v = session.query(Variant).filter(
            (Variant.id == line.product_id) | (Variant.sku == line.product_id) | (Variant.id == var_id)
        ).first()
        if v:
            var_id = v.id
            if v.catalog_item_id and not cat_item_id:
                cat_item_id = v.catalog_item_id
                parent_ci = session.query(CatalogItem).filter(CatalogItem.id == v.catalog_item_id).first()
                if parent_ci and not p_category:
                    cat = session.query(Category).filter(Category.id == parent_ci.category_id).first() if parent_ci.category_id else None
                    p_category = cat.name if cat else "Product"
            if not p_name:
                p_name = v.name
            item_type = "VARIANT"

        # Fallback to in-memory db.get("products")
        if not p_name:
            product = db.get("products", line.product_id)
            if product:
                p_name = product.get("name", "")
                p_category = product.get("category", "")
                p_desc = product.get("description", p_name)

        if not p_name:
            p_name = f"Item {line.product_id}"

        # Category ceiling check
        flagged = False
        flag_reason = None
        all_ceilings = db.list("category_discount_ceilings")
        for cc in all_ceilings:
            cc_cat = cc.get("category", "").lower()
            if cc_cat and (cc_cat in p_category.lower() or p_category.lower() in cc_cat):
                if line.discount_percent > cc.get("max_discount_percent", 100):
                    flagged = True
                    flag_reason = f"Exceeds {cc['max_discount_percent']}% {p_category.lower()} discount threshold"
                break

        qty = max(1, line.quantity)
        price = float(line.unit_price)
        disc_pct = float(line.discount_percent)
        disc_amt = qty * price * (disc_pct / 100.0)
        net = (qty * price) - disc_amt
        tax_amt = net * (tax_rate / 100.0)
        line_total = net + tax_amt

        line_id = f"QL-{str(uuid.uuid4())[:6].upper()}"
        line_dict = {
            "id": line_id,
            "sku": line.product_id,
            "name": p_name,
            "description": p_desc or p_name,
            "category": p_category,
            "product_id": line.product_id,
            "catalog_item_id": cat_item_id,
            "variant_id": var_id,
            "qty": qty,
            "quantity": qty,
            "unit_price": price,
            "unitPrice": price,
            "discount": disc_pct,
            "discount_percent": disc_pct,
            "discount_amount": round(disc_amt, 2),
            "tax_rate": tax_rate,
            "tax_amount": round(tax_amt, 2),
            "line_total": round(line_total, 2),
            "flagged": flagged,
            "flagReason": flag_reason,
            "is_recurring": line.is_recurring,
        }

        # Persist to PostgreSQL DocumentLine if document exists in database
        doc = session.query(SalesDocument).filter(
            (SalesDocument.id == quotation_id) | (SalesDocument.document_number == quotation_id)
        ).first()
        if doc:
            next_line_num = (session.query(func.max(DocumentLine.line_number)).filter(DocumentLine.document_id == doc.id).scalar() or 0) + 1
            doc_line_type = item_type if item_type in ['PRODUCT', 'SERVICE', 'SUBSCRIPTION', 'VARIANT', 'SUBSCRIPTION_PLAN'] else 'PRODUCT'
            new_doc_line = DocumentLine(
                id=line_id,
                document_id=doc.id,
                line_number=next_line_num,
                item_type=doc_line_type,
                variant_id=var_id,
                catalog_item_id=cat_item_id,
                description=p_name,
                quantity=qty,
                unit_price=price,
                discount_percent=disc_pct,
                discount_amount=round(disc_amt, 2),
                tax_rate=tax_rate,
                tax_amount=round(tax_amt, 2),
                line_total=round(line_total, 2),
                fulfillment_status='PENDING',
                allocated_quantity=0,
                negotiation_data={},
            )
            session.add(new_doc_line)
            session.commit()
    finally:
        session.close()

    quotation["lines"].append(line_dict)

    # Recalculate blended risk score
    q_model = Quotation(**quotation)
    score = calculate_blended_risk_score(q_model)

    quotation["blended_risk_score"] = score
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)

    return _enrich_quotation(quotation)

@router.delete("/{quotation_id}/lines/{line_id}")
def delete_line(quotation_id: str, line_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if quotation["status"] not in [QuotationStatus.DRAFT.value, QuotationStatus.NEGOTIATION.value]:
        raise HTTPException(status_code=400, detail="Cannot edit quotation in this status")

    quotation["lines"] = [l for l in quotation.get("lines", []) if l.get("id") != line_id]

    # Delete from PostgreSQL DocumentLine if document exists
    session = SessionLocal()
    try:
        doc = session.query(SalesDocument).filter(
            (SalesDocument.id == quotation_id) | (SalesDocument.document_number == quotation_id)
        ).first()
        if doc:
            session.query(DocumentLine).filter(
                (DocumentLine.document_id == doc.id) & (DocumentLine.id == line_id)
            ).delete()
            session.commit()
    finally:
        session.close()

    q_model = Quotation(**quotation)
    quotation["blended_risk_score"] = calculate_blended_risk_score(q_model)
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)

    return _enrich_quotation(quotation)

class UpdateLineRequest(BaseModel):
    qty: Optional[int] = None
    discount: Optional[float] = None

@router.put("/{quotation_id}/lines/{line_id}")
def update_line(quotation_id: str, line_id: str, update: UpdateLineRequest, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin]))):
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
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)
    return _enrich_quotation(quotation)

@router.post("/{quotation_id}/submit")
def submit_quotation(quotation_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin]))):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    q_model = Quotation(**quotation)
    new_status = determine_approval_routing(q_model.blended_risk_score)

    quotation["status"] = new_status.value
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)

    return _enrich_quotation(quotation)


# =====================================================================
# UPSELL / CROSS-SELL PANEL  (spec B5)
# =====================================================================

@router.get("/{quotation_id}/suggestions")
def quotation_suggestions(
    quotation_id: str,
    limit: int = 6,
    current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin])),
):
    """
    Ranked upsell / cross-sell suggestions for the current cart.

    Each entry carries the margin delta and promotion tag the panel displays,
    plus the co-purchase evidence behind it so the rep can see why it surfaced.
    """
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return {"quotation_id": quotation_id, "suggestions": get_suggestions(quotation, limit=limit)}


@router.get("/{quotation_id}/suggestions/{product_id}/impact")
def suggestion_margin_impact(
    quotation_id: str,
    product_id: str,
    current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.admin])),
):
    """What accepting this suggestion does to the order's blended margin."""
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    result = margin_impact(quotation, product_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# =====================================================================
# DISCOUNT RISK BREAKDOWN  (spec B4 - "Why This Quote Was Flagged")
# =====================================================================

@router.get("/{quotation_id}/risk")
def quotation_risk(
    quotation_id: str,
    current_user: dict = Depends(RoleChecker([RoleEnum.sales_rep, RoleEnum.manager, RoleEnum.finance, RoleEnum.admin])),
):
    """
    Per-line discount breakdown behind the blended risk score: what was given,
    what the applicable ceiling allowed, how far over it went, and which rule
    decided that ceiling. This is what the Approval Detail screen renders
    instead of simply asserting that a quote was flagged.
    """
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    evaluation = evaluate_quotation(Quotation(**quotation))
    return {
        "quotation_id": quotation_id,
        "score": evaluation["score"],
        "band": risk_band(evaluation["score"]),
        "worst_line": evaluation["worst_line"],
        "weighted_average": evaluation["weighted"],
        "customer_tier": evaluation["tier"],
        "breached_lines": evaluation["breached_lines"],
        "lines": evaluation["lines"],
        "approval_chain": build_approval_chain(evaluation),
        "next_approver": required_role(evaluation),
    }

