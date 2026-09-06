"""
Phoen Autonomous Business Engines & Services.

Houses the algorithmic core of Phoen:
1. discount_engine: Dual-ceiling blended risk scoring
2. split_engine: Multi-warehouse auto-split logistics
3. billing_engine: Milestone & recurring subscription generation
4. upsell_engine: 4-layer AI co-purchase graph recommendation
5. pdf_generator: ReportLab 2.0 flowable executive PDF generation
6. routing_engine: Multi-tier approval routing (L0 - L4)
"""

from .discount_engine import evaluate_quotation as evaluate_discount_risk
from .split_engine import plan_split, DEFAULT_SHIPMENT_COST
from .billing_engine import (
    split_billing_lines,
    generate_invoices_and_schedules,
    calculate_proration,
)
from .pdf_generator import generate_quotation_pdf
from .upsell_engine import get_suggestions as get_upsell_suggestions
from .routing_engine import build_approval_chain
from .pricing_rules import RuleBook

__all__ = [
    "evaluate_discount_risk",
    "plan_split",
    "DEFAULT_SHIPMENT_COST",
    "split_billing_lines",
    "generate_invoices_and_schedules",
    "calculate_proration",
    "generate_quotation_pdf",
    "get_upsell_suggestions",
    "build_approval_chain",
    "RuleBook",
]
