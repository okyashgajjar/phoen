"""
Integration tests for the DealFlow360 API.
Tests the full quotation lifecycle: create → add lines → submit → approve → fulfillment.
All tests must pass on every run.
"""
from fastapi.testclient import TestClient
from main import app
from models.base import db
from seed import seed_database

# Initialize the mock memory DB for tests
seed_database()

client = TestClient(app)

# ─── Helper: get auth header for a user ───
from tests.auth_helper import auth  # real login, signed JWT


# ─── Basic ───

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "DealFlow360" in response.json()["message"]


def test_login_success():
    response = client.post("/api/v1/auth/login", json={"email": "marcus@dealflow360.com", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    # A signed JWT, not the user id. The old assertion (access_token ==
    # "rep_marcus") encoded the vulnerability it was meant to test.
    assert data["access_token"].count(".") == 2


def test_token_is_not_the_user_id():
    """The previous scheme accepted a bare user id or email as the token."""
    for forged in ("rep_marcus", "marcus@dealflow360.com"):
        res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {forged}"})
        assert res.status_code == 401


def test_tampered_token_rejected():
    token = client.post(
        "/api/v1/auth/login",
        json={"email": "marcus@dealflow360.com", "password": "password"},
    ).json()["access_token"]
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token[:-4]}AAAA"})
    assert res.status_code == 401


def test_login_failure():
    response = client.post("/api/v1/auth/login", json={"email": "bad@dealflow360.com", "password": "wrong"})
    assert response.status_code == 401


# ─── Quotations ───

def test_list_quotations():
    response = client.get("/api/v1/quotations/", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check enriched fields are present
    q = data[0]
    assert "account" in q
    assert "rep" in q
    assert "statusLabel" in q


def test_list_quotations_all_as_admin():
    response = client.get("/api/v1/quotations/", headers=auth("admin_1"))
    assert response.status_code == 200
    data = response.json()
    # Admin sees all seeded quotations (mock + sqlite)
    assert len(data) >= 10


def test_get_single_quotation():
    response = client.get("/api/v1/quotations/Q-1042", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "Q-1042"
    assert data["account"] == "Acme Corp"
    assert len(data["lines"]) == 3


def test_create_quotation():
    response = client.post(
        "/api/v1/quotations/",
        headers=auth("rep_marcus"),
        json={"customer_id": "cust_acme", "title": "Test Proposal"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("Q-")
    assert data["status"] == "DRAFT"
    assert data["account"] == "Acme Corp"


def test_add_line_and_risk_score():
    # Create a fresh quotation
    create_res = client.post(
        "/api/v1/quotations/",
        headers=auth("rep_marcus"),
        json={"customer_id": "cust_acme", "title": "Risk Test"}
    )
    q_id = create_res.json()["id"]

    # Add a line with discount above ceiling (Gold tier = 15%, Hardware ceiling = 15%)
    line_res = client.post(
        f"/api/v1/quotations/{q_id}/lines",
        headers=auth("rep_marcus"),
        json={
            "product_id": "SKU-HW-709",
            "quantity": 2,
            "unit_price": 4500.0,
            "discount_percent": 20.0,
        }
    )
    assert line_res.status_code == 200
    data = line_res.json()
    # 20% - 15% = 5.0 overage
    assert data["blended_risk_score"] == 5.0
    # Line should be flagged
    assert data["lines"][0]["flagged"] is True


def test_submit_quotation_triggers_approval():
    create_res = client.post(
        "/api/v1/quotations/",
        headers=auth("rep_marcus"),
        json={"customer_id": "cust_acme", "title": "Submit Test"}
    )
    q_id = create_res.json()["id"]

    # Add an over-ceiling line
    client.post(
        f"/api/v1/quotations/{q_id}/lines",
        headers=auth("rep_marcus"),
        json={"product_id": "SKU-HW-709", "quantity": 1, "unit_price": 4500, "discount_percent": 16.0}
    )

    # Submit
    submit_res = client.post(f"/api/v1/quotations/{q_id}/submit", headers=auth("rep_marcus"))
    assert submit_res.status_code == 200
    assert submit_res.json()["status"] == "PENDING_APPROVAL"


def test_submit_no_risk_goes_to_ready():
    create_res = client.post(
        "/api/v1/quotations/",
        headers=auth("rep_marcus"),
        json={"customer_id": "cust_acme", "title": "No Risk Test"}
    )
    q_id = create_res.json()["id"]

    # Add a line within ceiling
    client.post(
        f"/api/v1/quotations/{q_id}/lines",
        headers=auth("rep_marcus"),
        json={"product_id": "SKU-HW-709", "quantity": 1, "unit_price": 4500, "discount_percent": 10.0}
    )

    submit_res = client.post(f"/api/v1/quotations/{q_id}/submit", headers=auth("rep_marcus"))
    assert submit_res.status_code == 200
    assert submit_res.json()["status"] == "READY"


# ─── Approvals ───

def test_approval_flow():
    # Q-1042 is seeded as PENDING_APPROVAL
    # Approve as manager
    approve_res = client.post(
        "/api/v1/approvals/Q-1042/approve",
        headers=auth("rep_sarah"),
        json={"reason": "Approved via test"}
    )
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "READY"


def test_get_pending_approvals():
    response = client.get("/api/v1/approvals/pending", headers=auth("rep_sarah"))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should have pending quotes from seed
    pending_ids = [q["id"] for q in data]
    assert "Q-1042" in pending_ids


def test_get_approval_chain():
    response = client.get("/api/v1/approvals/Q-1042/chain", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert "chain" in data
    assert len(data["chain"]) == 3
    assert data["chain"][0]["tier"] == 1


def test_reject_quotation():
    # First we need a pending quotation - use Q-1049
    reject_res = client.post(
        "/api/v1/approvals/Q-1049/reject",
        headers=auth("rep_sarah"),
        json={"reason": "Too risky"}
    )
    assert reject_res.status_code == 200
    assert reject_res.json()["status"] == "REJECTED"


# ─── Fulfillment ───

def test_get_fulfillment_orders():
    response = client.get("/api/v1/fulfillment/orders", headers=auth("fin_david"))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # 3 seeded orders


# ─── Billing ───

def test_get_invoices():
    response = client.get("/api/v1/billing/invoices", headers=auth("fin_david"))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4  # 4 seeded invoices
    assert data[0]["id"].startswith("INV-")


def test_get_subscriptions():
    response = client.get("/api/v1/billing/subscriptions", headers=auth("fin_david"))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4  # 4 seeded subs
    assert data[0]["id"].startswith("SUB-")


# ─── Reports ───

def test_dashboard_kpis():
    response = client.get("/api/v1/reports/dashboard", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert "total_pipeline" in data
    assert "pending_review_count" in data
    assert data["total_pipeline"] > 0


def test_deal_health():
    response = client.get("/api/v1/reports/deal-health", headers=auth("rep_sarah"))
    assert response.status_code == 200
    data = response.json()
    assert "anomalies" in data
    assert "health_score" in data


def test_catalog_rules():
    response = client.get("/api/v1/reports/catalog", headers=auth("admin_1"))
    assert response.status_code == 200
    data = response.json()
    assert "rules" in data
    assert "products" in data
    assert len(data["rules"]) >= 5
    assert len(data["products"]) >= 5


# ─── Products ───

def test_list_products():
    response = client.get("/api/v1/products/", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5


# ─── RBAC ───

def test_customer_cannot_access_internal_routes():
    """
    A portal account has no business on the internal pipeline endpoint at all.

    This test previously asserted 200 and then checked the response was filtered
    -- but the filter compared the quotation's customer_id to the *user's own
    id*, two different id spaces, so it never actually matched and a portal
    login could list every quotation in the system. The endpoint now refuses the
    customer role outright, which is what the test name always claimed.
    """
    response = client.get("/api/v1/quotations/", headers=auth("cust_acme"))
    assert response.status_code == 403

    # The customer reads their own quotations through the portal instead.
    own = client.get("/api/v1/portal/quotes", headers=auth("cust_acme"))
    assert own.status_code == 200
    for q in own.json():
        assert q["customer_id"] == "cust_acme"


def test_unauthenticated_rejected():
    response = client.get("/api/v1/quotations/")
    assert response.status_code in [401, 403]


# ─── End-to-end Flow ───

def test_full_quotation_lifecycle():
    """End-to-end: create → add lines → submit → approve → check fulfillment."""
    # 1. Create
    create_res = client.post(
        "/api/v1/quotations/",
        headers=auth("rep_marcus"),
        json={"customer_id": "cust_acme", "title": "E2E Test"}
    )
    assert create_res.status_code == 200
    q_id = create_res.json()["id"]

    # 2. Add line with overage
    client.post(
        f"/api/v1/quotations/{q_id}/lines",
        headers=auth("rep_marcus"),
        json={"product_id": "SKU-HW-709", "quantity": 2, "unit_price": 4500, "discount_percent": 18.0}
    )

    # 3. Submit → should go to PENDING_APPROVAL
    submit_res = client.post(f"/api/v1/quotations/{q_id}/submit", headers=auth("rep_marcus"))
    assert submit_res.json()["status"] == "PENDING_APPROVAL"

    # 4. Approve as manager
    approve_res = client.post(
        f"/api/v1/approvals/{q_id}/approve",
        headers=auth("rep_sarah"),
        json={"reason": "E2E approved"}
    )
    assert approve_res.json()["status"] == "READY"

    # 5. Check fulfillment split was generated (accessible by finance and admin)
    splits = client.get("/api/v1/fulfillment/orders", headers=auth("fin_david")).json()
    e2e_splits = [s for s in splits if s.get("quotation_id") == q_id]
    assert len(e2e_splits) >= 1


# ─── Integration & RBAC Fix Tests ───

def test_admin_can_manage_full_cpq_lifecycle():
    # Admin creates quotation
    create_res = client.post(
        "/api/v1/quotations/",
        headers=auth("admin_1"),
        json={"customer_id": "cust_acme", "title": "Admin CPQ Test"}
    )
    assert create_res.status_code == 200
    q_id = create_res.json()["id"]

    # Admin adds line item
    add_res = client.post(
        f"/api/v1/quotations/{q_id}/lines",
        headers=auth("admin_1"),
        json={"product_id": "SKU-HW-709", "quantity": 3, "unit_price": 4500, "discount_percent": 18.0}
    )
    assert add_res.status_code == 200
    line_id = add_res.json()["lines"][0]["id"]

    # Admin updates line item
    update_res = client.put(
        f"/api/v1/quotations/{q_id}/lines/{line_id}",
        headers=auth("admin_1"),
        json={"qty": 4, "discount": 20.0}
    )
    assert update_res.status_code == 200
    assert update_res.json()["lines"][0]["qty"] == 4
    assert update_res.json()["amount"] > 0

    # Admin submits quotation
    sub_res = client.post(f"/api/v1/quotations/{q_id}/submit", headers=auth("admin_1"))
    assert sub_res.status_code == 200
    assert sub_res.json()["status"] == "PENDING_APPROVAL"

    # Admin approves quotation directly
    app_res = client.post(
        f"/api/v1/approvals/{q_id}/approve",
        headers=auth("admin_1"),
        json={"reason": "Admin superuser approval"}
    )
    assert app_res.status_code == 200
    assert app_res.json()["status"] == "READY"


def test_portal_staff_preview_and_customer_flow():
    # Admin or sales rep can view portal quote preview
    res_admin = client.get("/api/v1/portal/quotes/Q-1042", headers=auth("admin_1"))
    assert res_admin.status_code == 200

    res_rep = client.get("/api/v1/portal/quotes/Q-1042", headers=auth("rep_marcus"))
    assert res_rep.status_code == 200

    # Real customer can view
    res_cust = client.get("/api/v1/portal/quotes/Q-1042", headers=auth("cust_acme"))
    assert res_cust.status_code == 200

    # A different customer is blocked. 404 rather than 403 on purpose: a 403
    # would confirm the quotation exists, letting one customer enumerate
    # another's document ids.
    res_other = client.get("/api/v1/portal/quotes/Q-1042", headers=auth("cust_zenith"))
    assert res_other.status_code == 404


def test_quote_confirmation_generates_invoice_and_fulfillment():
    # 1. Create and approve quote
    q_res = client.post(
        "/api/v1/quotations/",
        headers=auth("admin_1"),
        json={"customer_id": "cust_acme", "title": "Portal Execution Contract"}
    )
    q_id = q_res.json()["id"]

    client.post(
        f"/api/v1/quotations/{q_id}/lines",
        headers=auth("admin_1"),
        json={"product_id": "SKU-HW-709", "quantity": 1, "unit_price": 5000, "discount_percent": 0.0}
    )
    # Direct submit and approve
    client.post(f"/api/v1/quotations/{q_id}/submit", headers=auth("admin_1"))
    # In case it's READY directly (0% discount) or PENDING_APPROVAL
    quote_data = client.get(f"/api/v1/quotations/{q_id}", headers=auth("admin_1")).json()
    if quote_data["status"] == "PENDING_APPROVAL":
        client.post(f"/api/v1/approvals/{q_id}/approve", headers=auth("admin_1"))

    # 2. Confirm in customer portal
    conf_res = client.post(f"/api/v1/portal/quotes/{q_id}/confirm", headers=auth("cust_acme"))
    assert conf_res.status_code == 200
    # CONFIRMED, not WON: the lifecycle now distinguishes a confirmed order
    # (goes to fulfilment and billing) from a closed-won deal.
    assert conf_res.json()["quotation"]["status"] == "CONFIRMED"
    assert conf_res.json()["requires_approval"] is False

    # 3. Check invoice created with UI attributes
    invoices = client.get("/api/v1/billing/invoices", headers=auth("admin_1")).json()
    quote_invoices = [i for i in invoices if i.get("quoteId") == q_id or i.get("quotation_id") == q_id]
    assert len(quote_invoices) >= 1
    assert quote_invoices[0]["account"] == "Acme Corp"
    assert "status" in quote_invoices[0]

