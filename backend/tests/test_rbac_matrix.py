"""
Comprehensive RBAC Matrix Tests for DealFlow360.
Validates strict role boundary segregation across:
- sales_rep (Sales Person)
- manager (Sales Manager)
- finance (Finance Manager)
- admin (System Admin)
"""
from fastapi.testclient import TestClient
from main import app
from seed import seed_database

seed_database()
client = TestClient(app)

from tests.auth_helper import auth  # real login, signed JWT


# ─── 1. Sales Rep (Marcus) Restrictions & Access ───

def test_sales_rep_cannot_access_pending_approvals():
    res = client.get("/api/v1/approvals/pending", headers=auth("rep_marcus"))
    assert res.status_code == 403

def test_sales_rep_cannot_access_fulfillment_orders():
    res = client.get("/api/v1/fulfillment/orders", headers=auth("rep_marcus"))
    assert res.status_code == 403

def test_sales_rep_cannot_access_invoices():
    res = client.get("/api/v1/billing/invoices", headers=auth("rep_marcus"))
    assert res.status_code == 403

def test_sales_rep_cannot_access_subscriptions():
    res = client.get("/api/v1/billing/subscriptions", headers=auth("rep_marcus"))
    assert res.status_code == 403

def test_sales_rep_cannot_access_deal_health():
    res = client.get("/api/v1/reports/deal-health", headers=auth("rep_marcus"))
    assert res.status_code == 403

def test_sales_rep_cannot_access_catalog_rules():
    res = client.get("/api/v1/reports/catalog", headers=auth("rep_marcus"))
    assert res.status_code == 403

def test_sales_rep_cannot_create_users():
    res = client.post("/api/v1/auth/users", headers=auth("rep_marcus"), json={
        "email": "hacked@dealflow360.com", "password": "pass", "name": "Hacker", "role": "admin"
    })
    assert res.status_code == 403

def test_sales_rep_can_create_quotation():
    res = client.post("/api/v1/quotations/", headers=auth("rep_marcus"), json={
        "customer_id": "cust_acme", "title": "Marcus Proposal"
    })
    assert res.status_code == 200
    assert res.json()["rep"] == "Marcus Vance"


# ─── 2. Sales Manager (Sarah) Restrictions & Access ───

def test_manager_can_access_approvals_and_deal_health():
    res_app = client.get("/api/v1/approvals/pending", headers=auth("rep_sarah"))
    assert res_app.status_code == 200

    res_dh = client.get("/api/v1/reports/deal-health", headers=auth("rep_sarah"))
    assert res_dh.status_code == 200

def test_manager_cannot_access_invoices_or_subscriptions():
    res_inv = client.get("/api/v1/billing/invoices", headers=auth("rep_sarah"))
    assert res_inv.status_code == 403

    res_sub = client.get("/api/v1/billing/subscriptions", headers=auth("rep_sarah"))
    assert res_sub.status_code == 403

def test_manager_cannot_access_fulfillment():
    res = client.get("/api/v1/fulfillment/orders", headers=auth("rep_sarah"))
    assert res.status_code == 403

def test_manager_cannot_create_users():
    res = client.post("/api/v1/auth/users", headers=auth("rep_sarah"), json={
        "email": "mgr_user@dealflow360.com", "password": "pass", "name": "Mgr User", "role": "sales_rep"
    })
    assert res.status_code == 403


# ─── 3. Finance Manager (David) Restrictions & Access ───

def test_finance_can_access_invoices_subscriptions_and_fulfillment():
    res_inv = client.get("/api/v1/billing/invoices", headers=auth("fin_david"))
    assert res_inv.status_code == 200

    res_sub = client.get("/api/v1/billing/subscriptions", headers=auth("fin_david"))
    assert res_sub.status_code == 200

    res_ful = client.get("/api/v1/fulfillment/orders", headers=auth("fin_david"))
    assert res_ful.status_code == 200

    res_app = client.get("/api/v1/approvals/pending", headers=auth("fin_david"))
    assert res_app.status_code == 200

def test_finance_cannot_create_quotations():
    res = client.post("/api/v1/quotations/", headers=auth("fin_david"), json={
        "customer_id": "cust_acme", "title": "Finance Proposal"
    })
    assert res.status_code == 403

def test_finance_cannot_access_deal_health_or_catalog():
    res_dh = client.get("/api/v1/reports/deal-health", headers=auth("fin_david"))
    assert res_dh.status_code == 403

    res_cat = client.get("/api/v1/reports/catalog", headers=auth("fin_david"))
    assert res_cat.status_code == 403


# ─── 4. Admin Full Governance Access ───

def test_admin_has_full_governance_access():
    res_cat = client.get("/api/v1/reports/catalog", headers=auth("admin_1"))
    assert res_cat.status_code == 200

    res_inv = client.get("/api/v1/billing/invoices", headers=auth("admin_1"))
    assert res_inv.status_code == 200

    res_ful = client.get("/api/v1/fulfillment/orders", headers=auth("admin_1"))
    assert res_ful.status_code == 200

    res_dh = client.get("/api/v1/reports/deal-health", headers=auth("admin_1"))
    assert res_dh.status_code == 200

    res_users = client.get("/api/v1/auth/users/all", headers=auth("admin_1"))
    assert res_users.status_code == 200
