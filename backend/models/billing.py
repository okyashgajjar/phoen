from pydantic import BaseModel
from typing import List
from enum import Enum
from datetime import date

class CadenceEnum(str, Enum):
    monthly = "monthly"
    quarterly = "quarterly"
    yearly = "yearly"

class SubscriptionPlan(BaseModel):
    id: str
    product_id: str
    cadence: CadenceEnum
    cancellation_rules: str
    proration_rules: str

class BillingSchedule(BaseModel):
    id: str
    quotation_id: str
    subscription_plan_id: str
    start_date: date
    next_billing_date: date
    active: bool = True

class InvoiceStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    void = "void"

class Invoice(BaseModel):
    id: str
    quotation_id: str
    amount: float
    is_recurring: bool
    status: InvoiceStatus
    due_date: date
