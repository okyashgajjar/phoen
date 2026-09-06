"""
Customer Portal — the customer-facing negotiation view (spec B8).

The spec requires this to be "a real, separate, restricted view, not just
another internal screen with a different label". Three things enforce that:

  1. A portal account is scoped to exactly one `customer_id`, and every read is
     filtered by it. Previously the check compared the quotation's customer_id
     to the *user's own id*, which are different id spaces, so the scoping never
     worked as intended.

  2. A customer proposes, they do not decide. The old negotiate endpoint wrote
     the customer's requested discount straight onto the line, letting a
     customer set their own price and bypass discount governance entirely.
     Requests are now recorded in `negotiation_data` for a rep to accept.

  3. A confirmation is re-scored against the live ceilings. If the agreed terms
     breach them, the quote re-enters approval instead of closing.
"""

import copy
import io
from datetime import timezone, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from models.base import db
from models.sales import Quotation, QuotationStatus
from models.users import RoleEnum
from dependencies import get_current_user, get_portal_user, get_optional_user
from services.discount_engine import evaluate_quotation
from services.routing_engine import build_approval_chain, required_role, risk_band
from services.billing_engine import generate_invoices_and_schedules
from services.pdf_generator import generate_quotation_pdf

router = APIRouter()

# Statuses a customer is allowed to see at all.
#
# PENDING_APPROVAL is included on purpose: a customer's own counter-offer sends
# the quote back through approval, and the portal has to be able to say "your
# request is with our approvals team" -- the mockup's "Under Negotiation" state.
# DRAFT stays hidden because it was never sent, and REJECTED / EXPIRED stay
# hidden because the customer is told those outcomes by their rep, not by a
# status flip appearing in the portal.
CUSTOMER_VISIBLE = {
    QuotationStatus.READY.value,
    QuotationStatus.NEGOTIATION.value,
    QuotationStatus.PENDING_APPROVAL.value,
    QuotationStatus.APPROVED.value,
    QuotationStatus.CONFIRMED.value,
    QuotationStatus.WON.value,
    QuotationStatus.DISPATCHED.value,
    QuotationStatus.PAID.value,
}


class LineRequest(BaseModel):
    line_id: str
    requested_discount: float | None = Field(default=None, ge=0, le=100)
    comment: str | None = None


class NegotiationRequest(BaseModel):
    lines: list[LineRequest] = []
    counter_discount_percent: float | None = Field(default=None, ge=0, le=100)
    requested_delivery_date: str | None = None
    note: str | None = None


def _scope(current_user: dict | None) -> str | None:
    """The customer_id a request is confined to, or None for internal staff / guest view."""
    if not current_user:
        return None
    if current_user.get("role") == RoleEnum.customer.value:
        cid = current_user.get("customer_id")
        if not cid:
            raise HTTPException(status_code=403, detail="Portal account is not linked to a customer")
        return cid
    return None


def _load(quotation_id: str, current_user: dict | None = None) -> dict:
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    scope = _scope(current_user)
    if scope is not None:
        # 404 rather than 403: a customer should not be able to probe which
        # quotation ids exist for other companies.
        if quotation.get("customer_id") != scope:
            raise HTTPException(status_code=404, detail="Quotation not found")
        if quotation.get("status") not in CUSTOMER_VISIBLE:
            raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation


def _customer_view(quotation: dict) -> dict:
    """
    Strip internal commercial data before it leaves the building.

    Cost basis, margin, the blended risk score and the approval chain are all
    internal. A customer sees prices, discounts, status and their own requests.
    """
    from routers.quotations import _enrich_quotation

    # _enrich_quotation returns the same dict object it was given, so building
    # the customer view in place would rewrite the underlying record's lines
    # with the slimmed customer shape -- which then fails Quotation() validation
    # and loses negotiation data. Work on a copy.
    full = copy.deepcopy(_enrich_quotation(copy.deepcopy(quotation)))
    for internal in ("margin", "blended_risk_score", "flagReason", "flagged", "rep", "repAvatar"):
        full.pop(internal, None)

    # Read the lines from the raw record, not the enriched output: enrichment
    # runs them through the QuotationLine model, which has no negotiation_data
    # field and therefore drops every customer request.
    lines = []
    for line in quotation.get("lines", []) or []:
        negotiation = line.get("negotiation_data") or {}
        lines.append({
            "id": line.get("id"),
            "name": line.get("name") or line.get("description"),
            "quantity": line.get("qty") or line.get("quantity"),
            "unit_price": line.get("unit_price"),
            "discount_percent": line.get("discount_percent"),
            "line_total": line.get("line_total"),
            "is_recurring": line.get("is_recurring"),
            "requested_discount": negotiation.get("requested_discount"),
            "customer_comment": negotiation.get("customer_comment"),
            "request_status": negotiation.get("request_status"),
        })
    full["lines"] = lines
    return full


# ─────────────────────────────────────────────────────────────────────
# Read
# ─────────────────────────────────────────────────────────────────────
@router.get("/quotes")
def list_my_quotes(current_user: dict = Depends(get_portal_user)):
    """Every quotation belonging to this portal account's customer."""
    scope = _scope(current_user)
    mine = [
        q for q in db.list("quotations")
        if q.get("customer_id") == scope and q.get("status") in CUSTOMER_VISIBLE
    ]
    return [_customer_view(q) for q in mine]


@router.get("/quotes/{quotation_id}")
def get_customer_quote(quotation_id: str, current_user: dict | None = Depends(get_optional_user)):
    """
    One quotation, customer-safe. Internal staff, portal users, and shared guest views.
    """
    return _customer_view(_load(quotation_id, current_user))


@router.get("/quotes/{quotation_id}/pdf")
def download_portal_quote_pdf(quotation_id: str, current_user: dict | None = Depends(get_optional_user)):
    """Generate and stream executive commercial proposal PDF for portal and negotiation views."""
    quotation = _load(quotation_id, current_user)
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


# ─────────────────────────────────────────────────────────────────────
# Negotiate — a request, not a decision
# ─────────────────────────────────────────────────────────────────────
@router.post("/quotes/{quotation_id}/negotiate")
def negotiate_quote(
    quotation_id: str,
    body: NegotiationRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Record the customer's requested discounts and line comments.

    Nothing is applied to the order. The requested figure is stored alongside
    the line so a rep can accept or counter it, which keeps discount governance
    in force: a customer cannot set their own price.
    """
    quotation = _load(quotation_id, current_user)
    by_id = {l.get("id"): l for l in quotation.get("lines", []) or []}

    recorded = 0
    for req in body.lines:
        line = by_id.get(req.line_id)
        if line is None:
            raise HTTPException(status_code=404, detail=f"Line {req.line_id} not found on this quotation")
        negotiation = dict(line.get("negotiation_data") or {})
        if req.requested_discount is not None:
            negotiation["requested_discount"] = req.requested_discount
        if req.comment:
            negotiation["customer_comment"] = req.comment
        negotiation["request_status"] = "PENDING_REP_REVIEW"
        negotiation["requested_at"] = datetime.now(timezone.utc).isoformat()
        negotiation["requested_by"] = current_user.get("email")
        line["negotiation_data"] = negotiation
        recorded += 1

    metadata = dict(quotation.get("metadata") or {})
    if body.counter_discount_percent is not None:
        metadata["counter_discount_percent"] = body.counter_discount_percent
    if body.requested_delivery_date:
        metadata["requested_delivery_date"] = body.requested_delivery_date
    if body.note:
        metadata["customer_note"] = body.note
    quotation["metadata"] = metadata

    quotation["status"] = QuotationStatus.NEGOTIATION.value
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)

    db.insert("audit_logs", f"AUD-NEG-{quotation_id}-{int(datetime.now(timezone.utc).timestamp())}", {
        "entity_type": "QUOTATION",
        "entity_id": quotation_id,
        "action": "CUSTOMER_NEGOTIATION_REQUEST",
        "performed_by": current_user.get("email"),
        "reason": body.note or f"Customer requested changes on {recorded} line(s)",
        "new_value": {
            "lines_touched": recorded,
            "counter_discount_percent": body.counter_discount_percent,
        },
    })

    return {
        "message": f"Recorded {recorded} line request(s). Your sales contact will respond.",
        "quotation": _customer_view(quotation),
    }


# ─────────────────────────────────────────────────────────────────────
# Confirm — re-scored against live ceilings
# ─────────────────────────────────────────────────────────────────────
@router.post("/quotes/{quotation_id}/confirm")
def confirm_quote(quotation_id: str, current_user: dict = Depends(get_current_user)):
    """
    Customer accepts the terms as they stand.

    The quote is re-scored first. If the agreed terms breach the ceilings in
    force, it re-enters approval rather than closing, which is the spec's
    "if final terms exceed thresholds, the quotation automatically re-enters
    the approval flow".
    """
    quotation = _load(quotation_id, current_user)

    evaluation = evaluate_quotation(Quotation(**quotation))
    quotation["blended_risk_score"] = evaluation["score"]
    next_approver = required_role(evaluation)

    if next_approver is not None:
        quotation["status"] = QuotationStatus.PENDING_APPROVAL.value
        quotation["updated_at"] = datetime.now(timezone.utc)
        db.update("quotations", quotation_id, quotation)
        return {
            "message": (
                f"Terms exceed the approved discount ceiling by {evaluation['score']} points. "
                f"Sent to {next_approver} for approval."
            ),
            "requires_approval": True,
            "risk_band": risk_band(evaluation["score"]),
            "approval_chain": build_approval_chain(evaluation),
            "quotation": _customer_view(quotation),
        }

    quotation["status"] = QuotationStatus.CONFIRMED.value
    quotation["updated_at"] = datetime.now(timezone.utc)
    db.update("quotations", quotation_id, quotation)

    billing = generate_invoices_and_schedules(quotation_id)

    db.insert("audit_logs", f"AUD-CONF-{quotation_id}", {
        "entity_type": "QUOTATION",
        "entity_id": quotation_id,
        "action": "CUSTOMER_CONFIRMED",
        "performed_by": current_user.get("email"),
        "reason": "Customer confirmed quotation from the portal",
    })

    return {
        "message": "Quotation confirmed. Billing documents generated.",
        "requires_approval": False,
        "billing": billing,
        "quotation": _customer_view(quotation),
    }
