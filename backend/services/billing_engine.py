"""
DealFlow360 - Hybrid Billing Engine

One order can carry one-time hardware/services and recurring subscription lines
at the same time. They must be billed separately and stay reconciled against the
same order, which is what the spec's step 6 checks.

  one-time lines  -> a single invoice, due on the customer's payment terms
  recurring lines -> a subscription with its own billing schedule

Proration is computed from the actual days remaining in the current cycle, not
a placeholder. The previous version returned a constant 15.50 for every change
and fell back to a hardcoded 28,600 order total when it could not read the lines.
"""

import os
import sys
import uuid
from datetime import date, datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import Customer, CatalogItem
from models.base import db

CYCLE_DAYS = {
    "WEEKLY": 7,
    "MONTHLY": 30,
    "QUARTERLY": 91,
    "HALF_YEARLY": 182,
    "YEARLY": 365,
    "ANNUAL": 365,
}

DEFAULT_PAYMENT_TERMS_DAYS = 30


def _cycle_days(cycle: str) -> int:
    return CYCLE_DAYS.get((cycle or "MONTHLY").upper(), 30)


def _line_net(line) -> float:
    """Net of discount, before tax."""
    qty = float(line.get("qty") or line.get("quantity") or 1)
    price = float(line.get("unit_price") or line.get("unitPrice") or 0.0)
    disc = float(line.get("discount_percent") or line.get("discount") or 0.0)
    return qty * price * (1.0 - disc / 100.0)


def _line_tax(line, net: float) -> float:
    rate = float(line.get("tax_rate") or 0.0)
    return net * rate / 100.0


def split_billing_lines(quotation: dict) -> dict:
    """Separate the order into its one-time and recurring halves."""
    one_time, recurring = [], []
    for line in quotation.get("lines", []) or []:
        net = _line_net(line)
        entry = {
            "line_id": line.get("id"),
            "description": line.get("name") or line.get("description"),
            "quantity": int(line.get("qty") or line.get("quantity") or 1),
            "unit_price": float(line.get("unit_price") or line.get("unitPrice") or 0.0),
            "discount_percent": float(line.get("discount_percent") or line.get("discount") or 0.0),
            "net": round(net, 2),
            "tax": round(_line_tax(line, net), 2),
            "product_id": line.get("product_id") or line.get("sku"),
        }
        (recurring if line.get("is_recurring") else one_time).append(entry)
    return {"one_time": one_time, "recurring": recurring}


def generate_invoices_and_schedules(quotation_id: str):
    """
    Turn a confirmed quotation into an invoice for its one-time lines and a
    subscription schedule for each recurring line.
    """
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        return None

    parts = split_billing_lines(quotation)
    session = SessionLocal()
    try:
        customer = (
            session.query(Customer)
            .filter(Customer.id == quotation.get("customer_id"))
            .first()
        )
        account_name = customer.company_name if customer is not None else (
            quotation.get("account") or "Customer"
        )
        terms = int(customer.payment_terms_days) if customer is not None and customer.payment_terms_days else DEFAULT_PAYMENT_TERMS_DAYS

        q_num = quotation_id.replace("Q-", "").replace("QUO-", "")
        created = []

        # ── One-time invoice ──────────────────────────────────────────
        if parts["one_time"]:
            net = sum(l["net"] for l in parts["one_time"])
            tax = sum(l["tax"] for l in parts["one_time"])
            total = net + tax
            due = date.today() + timedelta(days=terms)

            invoice = {
                "id": f"INV-{q_num}",
                "quotation_id": quotation_id,
                "quoteId": quotation_id,
                "account": account_name,
                "customer_id": quotation.get("customer_id"),
                "subtotal": round(net, 2),
                "tax_total": round(tax, 2),
                "amount_value": round(total, 2),
                "amount": f"INR {total:,.2f}",
                "dueDate": due.strftime("%b %d, %Y"),
                "due_date": due.isoformat(),
                "status": "UNPAID",
                "statusLabel": f"Unpaid (Net {terms})",
                "paymentMethod": "NEFT / RTGS",
                "is_recurring": False,
                "lines": parts["one_time"],
            }
            db.insert("invoices", invoice["id"], invoice)
            created.append(invoice["id"])

        # ── Recurring subscriptions ───────────────────────────────────
        for idx, line in enumerate(parts["recurring"]):
            plan_name = line["description"] or "Recurring Plan"
            cycle = "MONTHLY"
            plan_id = None

            item = (
                session.query(CatalogItem)
                .filter(CatalogItem.id == line["product_id"])
                .first()
            )
            if item is not None:
                plan_id = item.id
                plan_name = item.name
                if item.billing_frequency:
                    cycle = item.billing_frequency.upper()

            days = _cycle_days(cycle)
            per_cycle = line["net"]
            annual = per_cycle * (365.0 / days)
            next_bill = date.today() + timedelta(days=days)

            sub_id = f"SUB-{q_num}-{idx + 1}"
            schedule = {
                "id": sub_id,
                "quotation_id": quotation_id,
                "customer_id": quotation.get("customer_id"),
                "account": account_name,
                "plan": plan_name,
                "plan_id": plan_id,
                "billing_cycle": cycle,
                "cycle_days": days,
                "amount_per_cycle": round(per_cycle, 2),
                "mrr": round(annual / 12.0, 2),
                "arr": round(annual, 2),
                "start_date": date.today().isoformat(),
                "next_billing_date": next_bill.isoformat(),
                "renewal": next_bill.strftime("%b %d, %Y"),
                "status": "ACTIVE",
                "active": True,
                "proration_history": [],
            }
            db.insert("billing_schedules", schedule["id"], schedule)
            created.append(sub_id)

        return {"created": created, "one_time": parts["one_time"], "recurring": parts["recurring"]}
    finally:
        session.close()


def calculate_proration(schedule_id: str, new_quantity: int) -> dict:
    """
    Mid-cycle quantity change.

    Credit the unused portion of what the customer already paid for the days
    remaining, then charge the new rate for those same days. The difference is
    what lands on the next invoice - negative means a credit note is due.
    """
    schedule = db.get("billing_schedules", schedule_id)
    if not schedule:
        return {"error": "schedule not found"}

    days = int(schedule.get("cycle_days") or _cycle_days(schedule.get("billing_cycle")))
    per_cycle = float(schedule.get("amount_per_cycle") or 0.0)
    old_qty = int(schedule.get("quantity") or 1) or 1

    next_bill_raw = schedule.get("next_billing_date")
    try:
        next_bill = datetime.fromisoformat(str(next_bill_raw)).date()
    except (TypeError, ValueError):
        next_bill = date.today() + timedelta(days=days)

    days_remaining = max(0, (next_bill - date.today()).days)
    unused_fraction = days_remaining / days if days else 0.0

    unit_rate = per_cycle / old_qty if old_qty else per_cycle
    credit = unit_rate * old_qty * unused_fraction
    charge = unit_rate * int(new_quantity) * unused_fraction
    delta = charge - credit

    result = {
        "schedule_id": schedule_id,
        "days_remaining": days_remaining,
        "cycle_days": days,
        "old_quantity": old_qty,
        "new_quantity": int(new_quantity),
        "credit_for_unused": round(credit, 2),
        "charge_for_remainder": round(charge, 2),
        "net_adjustment": round(delta, 2),
        "credit_note_required": delta < 0,
        "effective_from": date.today().isoformat(),
    }

    history = list(schedule.get("proration_history") or [])
    history.append(result)
    schedule["proration_history"] = history
    schedule["quantity"] = int(new_quantity)
    schedule["amount_per_cycle"] = round(unit_rate * int(new_quantity), 2)
    db.update("billing_schedules", schedule_id, schedule)

    return result


def calculate_cancellation_refund(schedule_id: str) -> dict:
    """Partial refund for the unused remainder of a cancelled cycle."""
    schedule = db.get("billing_schedules", schedule_id)
    if not schedule:
        return {"error": "schedule not found"}

    days = int(schedule.get("cycle_days") or _cycle_days(schedule.get("billing_cycle")))
    per_cycle = float(schedule.get("amount_per_cycle") or 0.0)

    try:
        next_bill = datetime.fromisoformat(str(schedule.get("next_billing_date"))).date()
    except (TypeError, ValueError):
        next_bill = date.today() + timedelta(days=days)

    days_remaining = max(0, (next_bill - date.today()).days)
    refund = per_cycle * (days_remaining / days) if days else 0.0

    return {
        "schedule_id": schedule_id,
        "days_remaining": days_remaining,
        "refund_amount": round(refund, 2),
        "credit_note_required": refund > 0,
        "cancelled_on": date.today().isoformat(),
    }
