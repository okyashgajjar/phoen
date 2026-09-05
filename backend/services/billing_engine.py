from models.base import db
import uuid
from datetime import date, timedelta

def generate_invoices_and_schedules(quotation_id: str):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        return None
        
    one_time_total = 0.0
    recurring_lines = []
    
    for line in quotation.get("lines", []):
        line_total = line.get("quantity") * line.get("unit_price") * (1 - line.get("discount_percent") / 100.0)
        
        if line.get("is_recurring"):
            recurring_lines.append(line)
        else:
            one_time_total += line_total
            
    # Generate one-time invoice
    if one_time_total > 0:
        invoice = {
            "id": str(uuid.uuid4()),
            "quotation_id": quotation_id,
            "amount": one_time_total,
            "is_recurring": False,
            "status": "unpaid",
            "due_date": date.today() + timedelta(days=30)
        }
        db.insert("invoices", invoice["id"], invoice)
        
    # Generate billing schedules for recurring
    for r_line in recurring_lines:
        # Find subscription plan for this product
        plans = db.list("subscription_plans")
        plan_id = None
        for p in plans:
            if p.get("product_id") == r_line.get("product_id"):
                plan_id = p.get("id")
                break
                
        schedule = {
            "id": str(uuid.uuid4()),
            "quotation_id": quotation_id,
            "subscription_plan_id": plan_id or "default_plan",
            "start_date": date.today(),
            "next_billing_date": date.today() + timedelta(days=30), # Assuming monthly
            "active": True
        }
        db.insert("billing_schedules", schedule["id"], schedule)
        
    return True

def calculate_proration(schedule_id: str, new_quantity: int):
    # Mock proration logic
    schedule = db.get("billing_schedules", schedule_id)
    if not schedule:
        return 0.0
        
    # In a real app, calculate days remaining in cycle, compute credit for unused old quantity,
    # and charge for new quantity for remaining days.
    # We will just return a mock credit/charge amount.
    return 15.50
