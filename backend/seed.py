"""
Seed data that matches the frontend's hardcoded demo data exactly.
This ensures the React UI renders real data from the API that looks
identical to what was previously hardcoded.
"""
from models.base import db
from datetime import datetime, date, timedelta

AVATARS = {
    "Marcus Vance": "https://lh3.googleusercontent.com/aida-public/AB6AXuAPPCmZWSHv5-hqsV8B7a1ZAECPiQItn-WV9xogMiJF9w-Wwv0lW7nz_la1neL_umllylkeWsgu_7FSD2pOWnm8q6XPvfiKqQhyu7j1xzouHlH_s2STTn1V9JHHdo0Eu0j3SAECmMOP6qrMR_PrChQgZgSVqVy4tyYNOMJUlvjFrvny8XcszlX1_cJIy-5LvL05M6wWURQqleEiw4-DcrpFqbL078c-3nWaf7c9-9c1r63DGe_rRAUQ",
    "Rachel Torres": "https://lh3.googleusercontent.com/aida-public/AB6AXuDDy3o_lnWgGPSUoB6P7Lp4hkbJFgtCgcakv09lYBTZEbeu45LrPMl-4j7D0fkePZHXv0SFP1ARMob5zvodbhlCTX9_i_ZNXVUl4gOB_g-RzHoTv_zqTypCWZyAlVCatqoMEUNzUaJds22kANc4-RQ4UwSK9Du9ZPIAiPkL-Q40vCvfw9YyzywdZ9NKDCgjYbrQatymSh81iyvilkTl4OuioHwk3E6wEqqj5gaJi_EYElr5UK2kTIkQ",
    "David Chen": "https://lh3.googleusercontent.com/aida-public/AB6AXuD6eGnNwcM2SWzLN7P5S_9fzAl71lAafDpxahswhQgzYLqqw_UYITDveOBT58W0KmwcQOrX4LYatjjzmk-y6DwcLx5R6RAk3k2dcTlzY52hxYLej98xxzfmBXfxl9rP__hIUR_nV7p524_UzAOEL4XkKSANGLIb6NcLx8gG654E6TSYV8JuaKRPE4Qdpu6MXyn18gJuHb1pLmcnJBQixHFZG3WZUz9Ina6EKZp_uqg8Z0hEccvcG-HL",
    "Sarah Jenkins": "https://lh3.googleusercontent.com/aida-public/AB6AXuD6eGnNwcM2SWzLN7P5S_9fzAl71lAafDpxahswhQgzYLqqw_UYITDveOBT58W0KmwcQOrX4LYatjjzmk-y6DwcLx5R6RAk3k2dcTlzY52hxYLej98xxzfmBXfxl9rP__hIUR_nV7p524_UzAOEL4XkKSANGLIb6NcLx8gG654E6TSYV8JuaKRPE4Qdpu6MXyn18gJuHb1pLmcnJBQixHFZG3WZUz9Ina6EKZp_uqg8Z0hEccvcG-HL",
}

def seed_database():
    """Populate the mock DB with demo data matching the frontend."""

    # ─── Users ───
    db.insert("users", "rep_marcus", {
        "id": "rep_marcus", "email": "marcus@phoen.io", "password": "password",
        "role": "sales_rep", "name": "Marcus Vance", "tier": "Gold"
    })
    db.insert("users", "rep_rachel", {
        "id": "rep_rachel", "email": "rachel@phoen.io", "password": "password",
        "role": "sales_rep", "name": "Rachel Torres", "tier": "Gold"
    })
    db.insert("users", "rep_sarah", {
        "id": "rep_sarah", "email": "sarah@phoen.io", "password": "password",
        "role": "manager", "name": "Sarah Jenkins", "tier": "Gold"
    })
    db.insert("users", "fin_david", {
        "id": "fin_david", "email": "david@phoen.io", "password": "password",
        "role": "finance", "name": "David Chen", "tier": "Gold"
    })
    db.insert("users", "admin_1", {
        "id": "admin_1", "email": "admin@phoen.io", "password": "password",
        "role": "admin", "name": "Admin User", "tier": "Gold"
    })

    # ─── Customers ───
    db.insert("users", "cust_acme", {
        "id": "cust_acme", "email": "john@acmecorp.com", "password": "password",
        "role": "customer", "name": "Acme Corp", "tier": "Gold"
    })
    db.insert("users", "cust_zenith", {
        "id": "cust_zenith", "email": "info@zenith.co", "password": "password",
        "role": "customer", "name": "Zenith Co", "tier": "Silver"
    })
    db.insert("users", "cust_global", {
        "id": "cust_global", "email": "ops@globallogistics.com", "password": "password",
        "role": "customer", "name": "Global Logistics", "tier": "Bronze"
    })
    db.insert("users", "cust_apex", {
        "id": "cust_apex", "email": "info@apexdynamics.io", "password": "password",
        "role": "customer", "name": "Apex Dynamics", "tier": "Gold"
    })
    db.insert("users", "cust_cyberdyne", {
        "id": "cust_cyberdyne", "email": "sales@cyberdyne.com", "password": "password",
        "role": "customer", "name": "Cyberdyne Inc", "tier": "Gold"
    })
    db.insert("users", "cust_techcorp", {
        "id": "cust_techcorp", "email": "procurement@techcorp.com", "password": "password",
        "role": "customer", "name": "TechCorp Industries", "tier": "Gold"
    })
    db.insert("users", "cust_enterprise", {
        "id": "cust_enterprise", "email": "info@enterprise.com", "password": "password",
        "role": "customer", "name": "Enterprise Solutions", "tier": "Gold"
    })
    db.insert("users", "cust_starlight", {
        "id": "cust_starlight", "email": "info@starlightltd.com", "password": "password",
        "role": "customer", "name": "Starlight Ltd", "tier": "Silver"
    })
    db.insert("users", "cust_nova", {
        "id": "cust_nova", "email": "info@novasystems.io", "password": "password",
        "role": "customer", "name": "Nova Systems", "tier": "Silver"
    })

    # ─── Products ───
    db.insert("products", "SKU-HW-709", {
        "id": "SKU-HW-709", "name": "Server Rack Ultra 2U Enterprise Edition",
        "category": "Hardware", "base_price": 4500.0, "unit": "pc",
        "tax_percent": 0.0, "is_recurring": False
    })
    db.insert("products", "SKU-SW-ENT", {
        "id": "SKU-SW-ENT", "name": "Cloud Ops Platform Annual Seat License",
        "category": "Software / SaaS", "base_price": 120.0, "unit": "seat/yr",
        "tax_percent": 0.0, "is_recurring": True
    })
    db.insert("products", "SKU-SLA-PREM", {
        "id": "SKU-SLA-PREM", "name": "24/7 Dedicated Support SLA & Technical Account Manager",
        "category": "Services", "base_price": 3040.0, "unit": "contract",
        "tax_percent": 0.0, "is_recurring": False
    })
    db.insert("products", "SKU-SEC-AUD", {
        "id": "SKU-SEC-AUD", "name": "Cybersecurity Compliance Audit",
        "category": "Services", "base_price": 15000.0, "unit": "project",
        "tax_percent": 0.0, "is_recurring": False
    })
    db.insert("products", "SKU-NET-EDGE", {
        "id": "SKU-NET-EDGE", "name": "Fiber Optical Router Edge 10G",
        "category": "Hardware", "base_price": 8200.0, "unit": "pc",
        "tax_percent": 0.0, "is_recurring": False
    })

    # ─── Discount Tiers ───
    db.insert("discount_tiers", "tier_gold", {"id": "tier_gold", "customer_tier": "Gold", "max_discount_percent": 15.0})
    db.insert("discount_tiers", "tier_silver", {"id": "tier_silver", "customer_tier": "Silver", "max_discount_percent": 10.0})
    db.insert("discount_tiers", "tier_bronze", {"id": "tier_bronze", "customer_tier": "Bronze", "max_discount_percent": 5.0})

    # ─── Category Discount Ceilings ───
    db.insert("category_discount_ceilings", "cat_hw", {"id": "cat_hw", "category": "Hardware", "max_discount_percent": 15.0})
    db.insert("category_discount_ceilings", "cat_sw", {"id": "cat_sw", "category": "Software / SaaS", "max_discount_percent": 25.0})
    db.insert("category_discount_ceilings", "cat_svc", {"id": "cat_svc", "category": "Services", "max_discount_percent": 10.0})

    # ─── Approval Chain Rules ───
    db.insert("approval_chain_rules", "rule_mgr", {"id": "rule_mgr", "min_blended_score": 0.1, "max_blended_score": 20.0, "required_role": "manager"})
    db.insert("approval_chain_rules", "rule_fin", {"id": "rule_fin", "min_blended_score": 20.0, "max_blended_score": 999.0, "required_role": "finance"})

    # ─── Warehouses ───
    db.insert("warehouses", "wh_east", {
        "id": "wh_east", "name": "US-East Central Hub (Virginia)",
        "location": "Virginia, US", "shipping_cost_weighting": 1.0,
        "stock": {"SKU-HW-709": 50, "SKU-NET-EDGE": 20, "SKU-SW-ENT": 9999}
    })
    db.insert("warehouses", "wh_eu", {
        "id": "wh_eu", "name": "EU-West Hub (Frankfurt)",
        "location": "Frankfurt, DE", "shipping_cost_weighting": 1.5,
        "stock": {"SKU-HW-709": 30, "SKU-NET-EDGE": 10}
    })

    # ─── Quotations (matching frontend's quotesData) ───
    now = datetime.utcnow()

    quotes = [
        {
            "id": "Q-1045", "customer_id": "cust_acme", "sales_rep_id": "rep_marcus",
            "status": "DRAFT", "title": "Enterprise Cloud Migration Bundle",
            "lines": [], "blended_risk_score": 0.0,
            "created_at": now - timedelta(hours=2), "updated_at": now - timedelta(hours=2),
        },
        {
            "id": "Q-1048", "customer_id": "cust_zenith", "sales_rep_id": "rep_rachel",
            "status": "DRAFT", "title": "Hardware Bundle & Rack Systems",
            "lines": [], "blended_risk_score": 0.0,
            "created_at": now - timedelta(hours=5), "updated_at": now - timedelta(hours=5),
        },
        {
            "id": "Q-1042", "customer_id": "cust_acme", "sales_rep_id": "rep_marcus",
            "status": "PENDING_APPROVAL", "title": "Hardware & SLA Tier Expansion",
            "lines": [
                {"id": "line_1", "sku": "SKU-HW-709", "name": "Server Rack Ultra 2U Enterprise Edition",
                 "category": "Hardware", "product_id": "SKU-HW-709",
                 "qty": 4, "unit_price": 4500.0, "unitPrice": 4500.0,
                 "discount": 18.0, "discount_percent": 18.0,
                 "flagged": True, "flagReason": "Exceeds 15% hardware discount threshold",
                 "is_recurring": False},
                {"id": "line_2", "sku": "SKU-SW-ENT", "name": "Cloud Ops Platform Annual Seat License",
                 "category": "Software / SaaS", "product_id": "SKU-SW-ENT",
                 "qty": 100, "unit_price": 120.0, "unitPrice": 120.0,
                 "discount": 10.0, "discount_percent": 10.0,
                 "flagged": False, "flagReason": None, "is_recurring": True},
                {"id": "line_3", "sku": "SKU-SLA-PREM", "name": "24/7 Dedicated Support SLA & Technical Account Manager",
                 "category": "Services", "product_id": "SKU-SLA-PREM",
                 "qty": 1, "unit_price": 3040.0, "unitPrice": 3040.0,
                 "discount": 0.0, "discount_percent": 0.0,
                 "flagged": False, "flagReason": None, "is_recurring": False},
            ],
            "blended_risk_score": 3.0,
            "created_at": now - timedelta(minutes=12), "updated_at": now - timedelta(minutes=12),
        },
        {
            "id": "Q-1046", "customer_id": "cust_global", "sales_rep_id": "fin_david",
            "status": "PENDING_APPROVAL", "title": "Fleet Tracking API Platform",
            "lines": [], "blended_risk_score": 0.5,
            "created_at": now - timedelta(hours=1), "updated_at": now - timedelta(hours=1),
        },
        {
            "id": "Q-1049", "customer_id": "cust_starlight", "sales_rep_id": "rep_sarah",
            "status": "PENDING_APPROVAL", "title": "Cybersecurity Compliance Audit",
            "lines": [], "blended_risk_score": 0.5,
            "created_at": now - timedelta(hours=3), "updated_at": now - timedelta(hours=3),
        },
        {
            "id": "Q-1041", "customer_id": "cust_apex", "sales_rep_id": "rep_rachel",
            "status": "READY", "title": "Automation & ERP Integration",
            "lines": [], "blended_risk_score": 0.0,
            "created_at": now - timedelta(days=1), "updated_at": now - timedelta(days=1),
        },
        {
            "id": "Q-1044", "customer_id": "cust_nova", "sales_rep_id": "rep_marcus",
            "status": "READY", "title": "Cloud Infrastructure Upgrade",
            "lines": [], "blended_risk_score": 0.0,
            "created_at": now - timedelta(days=2), "updated_at": now - timedelta(days=2),
        },
        {
            "id": "Q-1040", "customer_id": "cust_cyberdyne", "sales_rep_id": "fin_david",
            "status": "NEGOTIATION", "title": "AI Analytics & Data Warehouse",
            "lines": [], "blended_risk_score": 0.0,
            "created_at": now - timedelta(minutes=18), "updated_at": now - timedelta(minutes=18),
        },
        {
            "id": "Q-1039", "customer_id": "cust_techcorp", "sales_rep_id": "rep_rachel",
            "status": "WON", "title": "Global SaaS Enterprise License",
            "lines": [], "blended_risk_score": 0.0,
            "created_at": now - timedelta(hours=1), "updated_at": now - timedelta(hours=1),
        },
        {
            "id": "Q-1038", "customer_id": "cust_enterprise", "sales_rep_id": "rep_marcus",
            "status": "WON", "title": "Annual Security Suite Renewal",
            "lines": [], "blended_risk_score": 0.0,
            "created_at": now - timedelta(days=3), "updated_at": now - timedelta(days=3),
        },
    ]

    # Amounts and margins matching frontend
    amounts = {
        "Q-1045": 12400, "Q-1048": 30800, "Q-1042": 28600, "Q-1046": 54000,
        "Q-1049": 46000, "Q-1041": 62750, "Q-1044": 32000, "Q-1040": 62000,
        "Q-1039": 142000, "Q-1038": 85000,
    }
    margins = {
        "Q-1045": "42.5%", "Q-1048": "38.0%", "Q-1042": "28.2%", "Q-1046": "35.4%",
        "Q-1049": "40.1%", "Q-1041": "44.8%", "Q-1044": "41.2%", "Q-1040": "36.8%",
        "Q-1039": "46.5%", "Q-1038": "48.1%",
    }
    items_count = {
        "Q-1045": 2, "Q-1048": 4, "Q-1042": 3, "Q-1046": 5,
        "Q-1049": 2, "Q-1041": 6, "Q-1044": 3, "Q-1040": 4,
        "Q-1039": 8, "Q-1038": 4,
    }

    for q in quotes:
        q_id = q["id"]
        q["amount"] = amounts.get(q_id, 0)
        q["margin"] = margins.get(q_id, "0.0%")
        q["items"] = items_count.get(q_id, len(q.get("lines", [])))
        db.insert("quotations", q_id, q)

    # ─── Fulfillment Orders ───
    db.insert("fulfillment_splits", "ORD-8821", {
        "id": "ORD-8821", "quotation_id": "Q-1042",
        "account": "Acme Corp", "quoteId": "Q-1042",
        "date": "Sept 05, 2026", "itemsCount": 3,
        "warehouse": "US-East Central Hub (Virginia)",
        "status": "STOCK_RESERVED", "statusLabel": "Stock Reserved",
        "serials": ["SN-HW-99401", "SN-HW-99402", "SN-HW-99403", "SN-HW-99404"],
        "splits": [], "estimated_cost": 45.0, "is_manual_override": False,
    })
    db.insert("fulfillment_splits", "ORD-8819", {
        "id": "ORD-8819", "quotation_id": "Q-1039",
        "account": "TechCorp Industries", "quoteId": "Q-1039",
        "date": "Sept 04, 2026", "itemsCount": 8,
        "warehouse": "EU-West Hub (Frankfurt)",
        "status": "DISPATCHED", "statusLabel": "Dispatched & Tracking Enabled",
        "serials": ["SN-HW-88102", "SN-HW-88103"],
        "splits": [], "estimated_cost": 120.0, "is_manual_override": False,
    })
    db.insert("fulfillment_splits", "ORD-8818", {
        "id": "ORD-8818", "quotation_id": "Q-1041",
        "account": "Apex Dynamics", "quoteId": "Q-1041",
        "date": "Sept 03, 2026", "itemsCount": 6,
        "warehouse": "US-East Central Hub (Virginia)",
        "status": "PENDING_ALLOCATION", "statusLabel": "Pending Serial Allocation",
        "serials": [],
        "splits": [], "estimated_cost": 90.0, "is_manual_override": False,
    })

    # ─── Invoices ───
    db.insert("invoices", "INV-2042", {
        "id": "INV-2042", "quotation_id": "Q-1042",
        "account": "Acme Corp", "quoteId": "Q-1042",
        "amount": "$28,600.00", "dueDate": "Oct 05, 2026",
        "status": "UNPAID", "statusLabel": "Unpaid (Net 30)",
        "paymentMethod": "ACH / Wire Transfer",
        "is_recurring": False,
    })
    db.insert("invoices", "INV-2039", {
        "id": "INV-2039", "quotation_id": "Q-1039",
        "account": "TechCorp Industries", "quoteId": "Q-1039",
        "amount": "$142,000.00", "dueDate": "Sept 15, 2026",
        "status": "PAID", "statusLabel": "Paid & Cleared",
        "paymentMethod": "Wire Direct (#TX-99402)",
        "is_recurring": False,
    })
    db.insert("invoices", "INV-2038", {
        "id": "INV-2038", "quotation_id": "Q-1038",
        "account": "Enterprise Solutions", "quoteId": "Q-1038",
        "amount": "$85,000.00", "dueDate": "Sept 01, 2026",
        "status": "PAID", "statusLabel": "Paid & Cleared",
        "paymentMethod": "Corporate Credit Card",
        "is_recurring": False,
    })
    db.insert("invoices", "INV-2035", {
        "id": "INV-2035", "quotation_id": "Q-1035",
        "account": "Starlight Ltd", "quoteId": "Q-1035",
        "amount": "$46,000.00", "dueDate": "Aug 20, 2026",
        "status": "OVERDUE", "statusLabel": "Overdue (5 Days)",
        "paymentMethod": "ACH Wire",
        "is_recurring": False,
    })

    # ─── Subscriptions ───
    db.insert("billing_schedules", "SUB-9021", {
        "id": "SUB-9021", "quotation_id": "Q-1039",
        "account": "TechCorp Industries",
        "plan": "Enterprise Cloud Platform (1,000 Seats)",
        "mrr": "$11,833/mo", "arr": "$142,000/yr",
        "renewal": "Sept 04, 2027", "status": "ACTIVE",
        "subscription_plan_id": "plan_enterprise",
        "start_date": "2026-09-04", "next_billing_date": "2026-10-04",
        "active": True,
    })
    db.insert("billing_schedules", "SUB-9018", {
        "id": "SUB-9018", "quotation_id": "Q-1042",
        "account": "Acme Corp",
        "plan": "Cloud Ops Annual License (100 Seats)",
        "mrr": "$900/mo", "arr": "$10,800/yr",
        "renewal": "Oct 05, 2027", "status": "PENDING_ONBOARDING",
        "subscription_plan_id": "plan_cloudops",
        "start_date": "2026-10-05", "next_billing_date": "2026-11-05",
        "active": True,
    })
    db.insert("billing_schedules", "SUB-8994", {
        "id": "SUB-8994", "quotation_id": "Q-1041",
        "account": "Apex Dynamics",
        "plan": "Automation ERP Suite & API Nodes",
        "mrr": "$5,229/mo", "arr": "$62,750/yr",
        "renewal": "Nov 12, 2026", "status": "ACTIVE",
        "subscription_plan_id": "plan_erp",
        "start_date": "2025-11-12", "next_billing_date": "2026-10-12",
        "active": True,
    })
    db.insert("billing_schedules", "SUB-8950", {
        "id": "SUB-8950", "quotation_id": "Q-1040",
        "account": "Cyberdyne Inc",
        "plan": "AI Analytics Data Warehouse",
        "mrr": "$4,166/mo", "arr": "$50,000/yr",
        "renewal": "Dec 01, 2026", "status": "UPCOMING_RENEWAL",
        "subscription_plan_id": "plan_ai",
        "start_date": "2025-12-01", "next_billing_date": "2026-12-01",
        "active": True,
    })

    # ─── Catalog Rules ───
    db.insert("upsell_rules", "RULE-104", {"id": "RULE-104", "name": "Hardware Maximum Discount Cap", "category": "Hardware", "threshold": "15.0%", "role": "Sales Manager", "active": True})
    db.insert("upsell_rules", "RULE-105", {"id": "RULE-105", "name": "Software Tier 2 Volume Discount", "category": "Software", "threshold": "25.0%", "role": "Auto-Approved", "active": True})
    db.insert("upsell_rules", "RULE-208", {"id": "RULE-208", "name": "Blended Contract Margin Floor", "category": "Global CPQ", "threshold": "35.0%", "role": "Finance VP", "active": True})
    db.insert("upsell_rules", "RULE-302", {"id": "RULE-302", "name": "Multi-Year SLA Price Lock Guarantee", "category": "Services", "threshold": "10.0%", "role": "Sales Ops Lead", "active": True})
    db.insert("upsell_rules", "RULE-401", {"id": "RULE-401", "name": "Non-Standard SLA Payment Terms (> 60 Days)", "category": "Billing", "threshold": "60 Days", "role": "Treasury Admin", "active": False})
