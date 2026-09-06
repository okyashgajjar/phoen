from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class QuotationStatus(str, Enum):
    """
    Canonical quotation lifecycle.

    Ordered the way a deal actually moves, so the pipeline board and the
    Deal Health "stalled" check can compare stages numerically.
    """
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    READY = "READY"
    NEGOTIATION = "NEGOTIATION"
    CONFIRMED = "CONFIRMED"
    DISPATCHED = "DISPATCHED"
    PAID = "PAID"
    WON = "WON"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

STATUS_LABELS = {
    "DRAFT": "Draft",
    "PENDING_APPROVAL": "Pending Approval",
    "APPROVED": "Approved",
    "READY": "Ready to Send",
    "NEGOTIATION": "In Negotiation",
    "CONFIRMED": "Confirmed",
    "DISPATCHED": "Dispatched",
    "PAID": "Paid",
    "WON": "Won / Signed",
    "REJECTED": "Rejected",
    "EXPIRED": "Expired",
}

class QuotationLineIn(BaseModel):
    product_id: str
    quantity: int = 1
    unit_price: float
    discount_percent: float = 0.0
    is_recurring: bool = False
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    variant_id: Optional[str] = None

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


# =====================================================================
# STATUS NORMALISATION
# =====================================================================
# The seeded dataset carries 18 distinct status spellings across three
# vocabularies ("Approved" / "CONFIRMED" / "Confirmed" / "Sent" / ...).
# Any of them reaching the Pydantic enum raises a validation error and the
# endpoint 500s, which is why approved quotations could not be opened.
#
# Every read normalises through this map, so the API speaks one vocabulary
# regardless of how the row was written.

_STATUS_ALIASES = {
    "DRAFT": QuotationStatus.DRAFT,
    "PENDING APPROVAL": QuotationStatus.PENDING_APPROVAL,
    "PENDING_APPROVAL": QuotationStatus.PENDING_APPROVAL,
    "PENDING REVIEW": QuotationStatus.PENDING_APPROVAL,
    "PENDING COMMERCIAL APPROVAL": QuotationStatus.PENDING_APPROVAL,
    "SENT": QuotationStatus.READY,
    "READY": QuotationStatus.READY,
    "ISSUED": QuotationStatus.READY,
    "APPROVED": QuotationStatus.APPROVED,
    "AUTHORIZED": QuotationStatus.APPROVED,
    "UNDER NEGOTIATION": QuotationStatus.NEGOTIATION,
    "NEGOTIATION": QuotationStatus.NEGOTIATION,
    "CONFIRMED": QuotationStatus.CONFIRMED,
    "DISPATCHED": QuotationStatus.DISPATCHED,
    "PAID": QuotationStatus.PAID,
    "WON": QuotationStatus.WON,
    "REJECTED": QuotationStatus.REJECTED,
    "EXPIRED": QuotationStatus.EXPIRED,
    "CANCELLED": QuotationStatus.REJECTED,
}


def normalize_status(raw) -> str:
    """Map any legacy status spelling onto the canonical enum value."""
    if raw is None:
        return QuotationStatus.DRAFT.value
    if isinstance(raw, QuotationStatus):
        return raw.value
    key = str(raw).strip().upper()
    if key in _STATUS_ALIASES:
        return _STATUS_ALIASES[key].value
    # "Approved by Sarah Jenkins", "Pending L2_SALES_DIRECTOR Approval", ...
    for alias, status in _STATUS_ALIASES.items():
        if key.startswith(alias + " ") or f" {alias}" in key:
            return status.value
    return QuotationStatus.DRAFT.value
