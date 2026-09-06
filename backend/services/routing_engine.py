"""
DealFlow360 - Approval Routing Engine

Decides who has to sign off on a quotation, from the blended risk score and
the approval_level recorded on whichever pricing rule was breached.

The spec's requirement is that routing happens automatically: the rep never
presses "request approval". submit_quotation() calls this, and the quote lands
in the right queue by itself.

Bands (in discount points over the applicable ceiling):
    0            -> no approval, straight to READY
    0 < s <= 5   -> Sales Manager
    s > 5        -> Sales Manager, then Finance

A rule carrying an explicit approval_level of L3/VP/FINANCE escalates to the
finance chain regardless of band, because that ceiling was authored as
high-sensitivity by the admin.
"""

from models.sales import QuotationStatus

MANAGER_BAND = 5.0

FINANCE_LEVELS = {"L3_VP_COMMERCIAL", "L4_CFO", "FINANCE", "L3_FINANCE"}


def build_approval_chain(evaluation: dict) -> list[dict]:
    """
    Turn a discount_engine evaluation into the ordered chain of approval steps
    the Approval Detail screen renders. Steps that are not required are simply
    absent, which is what the mockup asks for ("Finance only shown when
    required").
    """
    score = evaluation.get("score", 0.0)
    breached = [l for l in evaluation.get("lines", []) if l.get("breached")]
    escalated = any(l.get("approval_level") in FINANCE_LEVELS for l in breached)

    chain = [{"step": "Submitted", "role": "sales_rep", "required": True}]

    if score <= 0 and not escalated:
        chain.append({"step": "Auto-Approved", "role": "system", "required": True})
        return chain

    chain.append({
        "step": "Sales Manager",
        "role": "manager",
        "required": True,
        "reason": f"Blended risk {score} pt over ceiling",
    })

    if score > MANAGER_BAND or escalated:
        why = (
            f"Breach on a rule marked {', '.join(sorted({l['approval_level'] for l in breached if l.get('approval_level') in FINANCE_LEVELS}))}"
            if escalated
            else f"Blended risk {score} pt exceeds the {MANAGER_BAND} pt manager band"
        )
        chain.append({
            "step": "Finance",
            "role": "finance",
            "required": True,
            "reason": why,
        })

    chain.append({"step": "Confirmed", "role": "system", "required": True})
    return chain


def required_role(evaluation: dict) -> str | None:
    """Return the role that must act next, or None when no approval is needed."""
    score = evaluation.get("score", 0.0)
    breached = [l for l in evaluation.get("lines", []) if l.get("breached")]
    escalated = any(l.get("approval_level") in FINANCE_LEVELS for l in breached)

    if score <= 0 and not escalated:
        return None
    if score > MANAGER_BAND or escalated:
        return "finance"
    return "manager"


def risk_band(score: float) -> str:
    """LOW / MEDIUM / HIGH label used by the Approvals list screen."""
    if score <= 0:
        return "LOW"
    if score <= MANAGER_BAND:
        return "MEDIUM"
    return "HIGH"


def determine_approval_routing(blended_risk_score: float) -> QuotationStatus:
    """
    Backwards-compatible entry point used by the routers.

    A clean quotation goes straight to READY. Anything over its ceiling goes to
    PENDING_APPROVAL. The previous version returned PENDING_APPROVAL for every
    quotation including clean ones, which meant nothing could ever skip approval.
    """
    if blended_risk_score is None or blended_risk_score <= 0.0:
        return QuotationStatus.READY
    return QuotationStatus.PENDING_APPROVAL
