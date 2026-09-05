from models.base import db
from models.sales import QuotationStatus

def determine_approval_routing(blended_risk_score: float) -> QuotationStatus:
    """Determine which approval status a quotation should be routed to,
    based on the blended risk score and configured approval chain rules."""
    # If no risk, it can go straight to READY (approved)
    if blended_risk_score <= 0.0:
        return QuotationStatus.READY

    all_rules = db.list("approval_chain_rules")

    required_role = None
    for rule in all_rules:
        if rule.get("min_blended_score") <= blended_risk_score < rule.get("max_blended_score", float('inf')):
            required_role = rule.get("required_role")

    if required_role == "finance":
        return QuotationStatus.PENDING_APPROVAL
    elif required_role == "manager":
        return QuotationStatus.PENDING_APPROVAL

    # Default fallback
    return QuotationStatus.PENDING_APPROVAL
