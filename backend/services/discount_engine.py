"""
DealFlow360 - Blended Discount Risk Engine

Implements the blended risk score described in the spec:

  "different products are allowed different discount limits, and the system
   checks every line against its own limit, not just one overall limit"

Two things drive the score:

  1. WORST LINE  - the single largest breach on any one line. One line 8 points
     over its own ceiling is enough to require approval, even when the customer
     tier would have allowed that headline number.

  2. BLENDED SPREAD - the value-weighted average breach across the whole order.
     Catches the rep who keeps every line technically within limits but still
     gives away more margin than the company intends overall.

The final score is the higher of the two signals, so neither a single bad line
nor a wide spread of small breaches can slip through.
"""

from services.pricing_rules import RuleBook


def _line_value(line) -> float:
    qty = getattr(line, "qty", None) or getattr(line, "quantity", 1) or 1
    price = getattr(line, "unit_price", None) or getattr(line, "unitPrice", 0.0) or 0.0
    return float(qty) * float(price)


def _line_discount(line) -> float:
    disc = getattr(line, "discount_percent", None)
    if disc is None:
        disc = getattr(line, "discount", 0.0)
    return float(disc or 0.0)


def evaluate_quotation(quotation) -> dict:
    """
    Score a quotation and return the full breakdown.

    Returns:
      {
        "score":        float,   # blended risk score, in discount points
        "worst_line":   float,   # largest single-line breach
        "weighted":     float,   # value-weighted average breach
        "tier":         str,
        "lines":        [ {line_id, name, category, given, allowed, over_by,
                           value, source, breached} ],
        "breached_lines": int,
      }
    """
    customer_id = getattr(quotation, "customer_id", "") or ""
    lines = list(getattr(quotation, "lines", []) or [])

    with RuleBook() as book:
        tier = book.tier_for_customer(customer_id)

        breakdown = []
        total_value = 0.0
        weighted_overage = 0.0
        worst = 0.0

        for line in lines:
            # Recurring subscription lines are governed by plan terms, not by
            # the one-time product discount ceilings.
            if getattr(line, "is_recurring", False):
                continue

            product_id = getattr(line, "product_id", "") or getattr(line, "sku", "")
            category_id = book.category_for(product_id)
            allowed, approval_level, source = book.ceiling_for(tier, category_id)

            given = _line_discount(line)
            value = _line_value(line)
            over_by = max(0.0, given - allowed)

            total_value += value
            weighted_overage += over_by * value
            worst = max(worst, over_by)

            breakdown.append({
                "line_id": getattr(line, "id", ""),
                "name": getattr(line, "name", "") or getattr(line, "description", ""),
                "category": category_id or "UNCATEGORISED",
                "given": round(given, 2),
                "allowed": round(allowed, 2),
                "over_by": round(over_by, 2),
                "value": round(value, 2),
                "approval_level": approval_level,
                "source": source,
                "breached": over_by > 0,
            })

    weighted = (weighted_overage / total_value) if total_value > 0 else 0.0
    score = max(worst, weighted)

    return {
        "score": round(score, 2),
        "worst_line": round(worst, 2),
        "weighted": round(weighted, 2),
        "tier": tier,
        "lines": breakdown,
        "breached_lines": sum(1 for b in breakdown if b["breached"]),
    }


def calculate_blended_risk_score(quotation) -> float:
    """Backwards-compatible entry point used by the routers."""
    return evaluate_quotation(quotation)["score"]
