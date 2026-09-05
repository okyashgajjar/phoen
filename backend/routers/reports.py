from fastapi import APIRouter, Depends
from models.base import db
from dependencies import RoleChecker
from models.users import RoleEnum
from datetime import datetime

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_kpis(current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.admin, RoleEnum.sales_rep]))):
    quotations = db.list("quotations")

    total_pipeline = sum(q.get("amount", 0) for q in quotations if q.get("status") not in ["WON", "REJECTED"])
    pending_review = [q for q in quotations if q.get("status") == "PENDING_APPROVAL"]
    pending_value = sum(q.get("amount", 0) for q in pending_review)
    ready = [q for q in quotations if q.get("status") == "READY"]
    ready_value = sum(q.get("amount", 0) for q in ready)
    negotiation = [q for q in quotations if q.get("status") == "NEGOTIATION"]
    negotiation_value = sum(q.get("amount", 0) for q in negotiation)
    won = [q for q in quotations if q.get("status") == "WON"]
    won_value = sum(q.get("amount", 0) for q in won)

    return {
        "total_pipeline": total_pipeline,
        "total_active_deals": len([q for q in quotations if q.get("status") not in ["WON", "REJECTED"]]),
        "pending_review_value": pending_value,
        "pending_review_count": len(pending_review),
        "ready_value": ready_value,
        "ready_count": len(ready),
        "negotiation_value": negotiation_value,
        "negotiation_count": len(negotiation),
        "won_value": won_value,
        "won_count": len(won),
        "win_velocity_days": 11.4,
    }

@router.get("/deal-health")
def get_deal_health(current_user: dict = Depends(RoleChecker([RoleEnum.manager, RoleEnum.admin, RoleEnum.sales_rep]))):
    quotations = db.list("quotations")

    stalled_deals = []
    discount_anomalies = []

    now = datetime.utcnow()

    for q in quotations:
        updated_at = q.get("updated_at")
        if updated_at:
            if isinstance(updated_at, str):
                updated_at = datetime.fromisoformat(updated_at)
            if (now - updated_at).days > 7 and q.get("status") not in ["WON", "REJECTED"]:
                stalled_deals.append(q)

        if q.get("blended_risk_score", 0) > 10.0:
            discount_anomalies.append(q)

    # Build anomalies list matching frontend shape
    anomalies = []
    for q in quotations:
        for line in q.get("lines", []):
            if line.get("flagged"):
                anomalies.append({
                    "id": f"ANOM-{abs(hash(q['id'] + line.get('id', ''))) % 1000:03d}",
                    "deal": f"{q['id']} ({db.get('users', q.get('customer_id', '')).get('name', 'Unknown') if db.get('users', q.get('customer_id', '')) else 'Unknown'})",
                    "issue": f"{line.get('category', 'Item')} discount {line.get('discount', 0)}% exceeds {15.0}% rep cap",
                    "severity": "HIGH",
                    "impact": f"-{line.get('discount', 0) - 15.0:.1f}% Margin",
                    "time": "12m ago",
                })

    # Check for stalled negotiation deals
    for q in stalled_deals:
        customer = db.get("users", q.get("customer_id", ""))
        c_name = customer.get("name", "Unknown") if customer else "Unknown"
        anomalies.append({
            "id": f"ANOM-{abs(hash(q['id'])) % 1000:03d}",
            "deal": f"{q['id']} ({c_name})",
            "issue": f"Stagnant in {q.get('status', 'Unknown')} state > 7 days without activity",
            "severity": "MEDIUM",
            "impact": "Churn Risk",
            "time": "1 day ago",
        })

    # Check overdue invoices
    for inv in db.list("invoices"):
        if inv.get("status") == "OVERDUE":
            anomalies.append({
                "id": f"ANOM-{abs(hash(inv['id'])) % 1000:03d}",
                "deal": f"{inv.get('quoteId', 'N/A')} ({inv.get('account', 'Unknown')})",
                "issue": f"Invoice {inv['id']} overdue",
                "severity": "MEDIUM",
                "impact": "Delayed Receivables",
                "time": "2 days ago",
            })

    return {
        "anomalies": anomalies,
        "stalled_deals_count": len(stalled_deals),
        "discount_anomalies_count": len(discount_anomalies),
        "total_active_deals": len([q for q in quotations if q.get("status") not in ["WON", "REJECTED"]]),
        "health_score": 88.4,
    }

@router.get("/catalog")
def get_catalog_rules(current_user: dict = Depends(RoleChecker([RoleEnum.admin, RoleEnum.manager, RoleEnum.sales_rep]))):
    """Return catalog rules and products for the Catalog & Rules view."""
    rules = db.list("upsell_rules")
    products = db.list("products")

    catalog_products = []
    for p in products:
        catalog_products.append({
            "sku": p["id"],
            "name": p["name"],
            "category": p["category"],
            "listPrice": f"${p['base_price']:,.0f}",
            "costBasis": f"${p['base_price'] * 0.7:,.0f}",
            "tierDiscount": f"Up to 15%",
        })

    return {
        "rules": rules,
        "products": catalog_products,
    }
