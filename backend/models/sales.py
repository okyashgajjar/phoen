from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class QuotationStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    READY = "READY"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    REJECTED = "REJECTED"

STATUS_LABELS = {
    "DRAFT": "Draft",
    "PENDING_APPROVAL": "Pending Approval",
    "READY": "Ready to Send",
    "NEGOTIATION": "In Negotiation",
    "WON": "Won / Signed",
    "REJECTED": "Rejected",
}

class QuotationLineIn(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    discount_percent: float
    is_recurring: bool = False

class QuotationLine(BaseModel):
    id: str
    sku: str = ""
    name: str = ""
    category: str = ""
    product_id: str
    qty: int = 1
    unit_price: float = 0.0
    unitPrice: float = 0.0
    discount: float = 0.0
    discount_percent: float = 0.0
    flagged: bool = False
    flagReason: Optional[str] = None
    is_recurring: bool = False

class Quotation(BaseModel):
    id: str
    customer_id: str
    sales_rep_id: str
    status: QuotationStatus
    lines: List[QuotationLine] = []
    blended_risk_score: float = 0.0
    created_at: datetime
    updated_at: datetime
    # Enriched fields for frontend
    account: str = ""
    title: str = ""
    amount: float = 0.0
    rep: str = ""
    repAvatar: str = ""
    statusLabel: str = ""
    items: int = 0
    margin: str = "0.0%"
    flagged: bool = False
    flagReason: Optional[str] = None
    portalActive: bool = False
    time: str = ""

class ApprovalEvent(BaseModel):
    id: str
    quotation_id: str
    actor_id: str
    action: str # approve, reject, revise
    reason: str
    timestamp: datetime
    before_state: str
    after_state: str

class ApprovalChainRule(BaseModel):
    id: str
    min_blended_score: float
    max_blended_score: float
    required_role: str # manager, finance
