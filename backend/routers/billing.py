from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io
from models.base import db
from dependencies import get_current_user, RoleChecker
from models.users import RoleEnum
from pydantic import BaseModel
from typing import Optional, List
from datetime import timezone, datetime
import uuid
from services.pdf_generator import generate_invoice_pdf

router = APIRouter()

class InvoiceCreate(BaseModel):
    customer_id: str
    amount: float
    title: Optional[str] = "Commercial Sales & Cloud SaaS Billing"
    notes: Optional[str] = None
    due_date: Optional[str] = None
    payment_terms_days: Optional[int] = 30
    quote_id: Optional[str] = None

class SubscriptionUpgrade(BaseModel):
    additional_seats: Optional[int] = 5
    addon_name: Optional[str] = "24/7 Premium Enterprise SLA"
    rate_increase: Optional[float] = 12000.0

@router.get("/invoices")
def get_invoices(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    """Return invoices in frontend-compatible shape."""
    return db.list("invoices")

@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    inv = db.get("invoices", invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv

@router.get("/invoices/{invoice_id}/pdf")
def download_invoice_pdf(invoice_id: str, current_user: dict = Depends(get_current_user)):
    """Generate and stream official Tax Invoice PDF."""
    inv = db.get("invoices", invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    customer = None
    cust_id = inv.get("customer_id")
    if cust_id:
        customer = db.get("customers", cust_id) or db.get("users", cust_id)
    
    lines = inv.get("lines") or []
    pdf_bytes = generate_invoice_pdf(inv, customer, lines)
    
    filename = f"INVOICE-{inv.get('document_number') or invoice_id}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@router.post("/invoices")
def create_invoice(payload: InvoiceCreate, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    """Generate a real commercial billing invoice and record audit event."""
    inv_id = f"INV-BILL-{uuid.uuid4().hex[:6].upper()}"
    inv_number = f"INV-2026-{uuid.uuid4().hex[:4].upper()}"
    
    customer = db.get("customers", payload.customer_id) or db.get("users", payload.customer_id)
    cust_name = customer.get("name") or customer.get("company_name") if customer else "Enterprise Client"
    
    desc_notes = payload.notes or payload.title or "Commercial Sales & Cloud SaaS Billing"
    
    due_str = (datetime.now(timezone.utc)).strftime("%b %d, %Y")
    if payload.due_date:
        try:
            dt = datetime.strptime(payload.due_date, "%Y-%m-%d")
            due_str = dt.strftime("%b %d, %Y")
        except Exception:
            due_str = payload.due_date

    invoice_data = {
        "id": inv_id,
        "document_number": inv_number,
        "document_type": "INVOICE",
        "customer_id": payload.customer_id,
        "customer_name": cust_name,
        "account": cust_name,
        "amount": payload.amount,
        "grand_total": payload.amount,
        "subtotal": round(payload.amount / 1.18, 2),
        "tax_total": round(payload.amount - (payload.amount / 1.18), 2),
        "discount_total": 0.0,
        "currency": "INR",
        "status": "ISSUED",
        "approval_status": "Authorized",
        "created_by": current_user.get("name") or "David Chen",
        "title": payload.title or desc_notes,
        "notes": desc_notes,
        "quoteId": payload.quote_id or f"QT-MANUAL-{inv_id.replace('INV-BILL-', '')}",
        "dueDate": due_str,
        "statusLabel": "Issued & Awaiting Payment",
        "created_at": datetime.now(timezone.utc),
        "lines": [{
            "description": desc_notes,
            "quantity": 1,
            "unit_price": payload.amount,
            "tax_rate": 18.0,
            "line_total": payload.amount
        }]
    }
    
    db.insert("invoices", inv_id, invoice_data)
    
    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "entity_type": "invoice",
        "entity_id": inv_id,
        "actor_id": current_user.get("name") or "David Chen",
        "actor_role": current_user.get("role", "finance"),
        "action": "create_invoice",
        "reason": f"Generated manual invoice for {cust_name} (₹{payload.amount:,.2f})",
        "timestamp": datetime.now(timezone.utc),
    }
    db.insert("audit_logs", audit["id"], audit)
    
    return invoice_data

@router.post("/invoices/{invoice_id}/pay")
def pay_invoice(invoice_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    """Mark invoice as paid and reconciled."""
    inv = db.get("invoices", invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    old_status = inv.get("status")
    inv["status"] = "PAID"
    inv["statusLabel"] = "Paid & Reconciled"
    inv["approval_status"] = "Payment Reconciled"
    inv["updated_at"] = datetime.now(timezone.utc)
    
    db.update("invoices", invoice_id, inv)
    
    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "entity_type": "invoice",
        "entity_id": invoice_id,
        "actor_id": current_user.get("name") or "David Chen",
        "actor_role": current_user.get("role", "finance"),
        "action": "reconcile_payment",
        "reason": f"Recorded full payment reconciliation for {invoice_id} via NEFT/RTGS wire",
        "timestamp": datetime.now(timezone.utc),
        "before_state": old_status,
        "after_state": "PAID"
    }
    db.insert("audit_logs", audit["id"], audit)
    
    return inv

@router.get("/subscriptions")
def get_subscriptions(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    """Return subscription billing schedules in frontend-compatible shape."""
    return db.list("subscriptions")

@router.post("/subscriptions/{schedule_id}/upgrade")
def upgrade_subscription(schedule_id: str, payload: SubscriptionUpgrade = SubscriptionUpgrade(), current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    """Add expansion seats / SLA add-ons to an active subscription."""
    sub = db.get("subscriptions", schedule_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    old_rate = float(sub.get("annual_rate") or 0.0)
    new_rate = old_rate + payload.rate_increase
    sub["annual_rate"] = new_rate
    sub["arr"] = f"₹{new_rate:,.0f} / yr"
    sub["mrr"] = f"₹{new_rate / 12:,.0f} / mo"
    sub["plan_name"] = f"{sub.get('plan_name', 'Plan')} + {payload.additional_seats}x Seats ({payload.addon_name})"
    sub["plan"] = sub["plan_name"]
    
    db.update("subscriptions", schedule_id, sub)
    
    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "entity_type": "subscription",
        "entity_id": schedule_id,
        "actor_id": current_user.get("name") or "David Chen",
        "actor_role": current_user.get("role", "finance"),
        "action": "upgrade_subscription",
        "reason": f"Contract expansion: Added {payload.additional_seats} seats (+₹{payload.rate_increase:,.0f}/yr ARR)",
        "timestamp": datetime.now(timezone.utc),
    }
    db.insert("audit_logs", audit["id"], audit)
    
    return sub

@router.post("/subscriptions/{schedule_id}/cancel")
def cancel_subscription(schedule_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    sub = db.get("subscriptions", schedule_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    old_status = sub.get("status")
    sub["active"] = False
    sub["status"] = "CANCELLED"
    sub["statusLabel"] = "Contract Cancelled"
    
    db.update("subscriptions", schedule_id, sub)
    
    # Audit log
    audit = {
        "id": str(uuid.uuid4()),
        "entity_type": "subscription",
        "entity_id": schedule_id,
        "actor_id": current_user.get("name") or "David Chen",
        "actor_role": current_user.get("role", "finance"),
        "action": "cancel_subscription",
        "reason": "Contract terminated or paused per customer notice",
        "timestamp": datetime.now(timezone.utc),
        "before_state": old_status,
        "after_state": "CANCELLED"
    }
    db.insert("audit_logs", audit["id"], audit)
    
    return sub
