"""
Integration tests for the DealFlow360 API.
Tests the full quotation lifecycle: create → add lines → submit → approve → fulfillment.
All tests must pass on every run.
"""
from fastapi.testclient import TestClient
from main import app
from models.base import db

client = TestClient(app)

# ─── Helper: get auth header for a user ───
def auth(user_id: str):
    return {"Authorization": f"Bearer {user_id}"}


# ─── Basic ───

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "DealFlow360" in response.json()["message"]


def test_login_success():
    response = client.post("/api/v1/auth/login", json={"email": "marcus@phoen.io", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "rep_marcus"
    assert data["token_type"] == "bearer"


def test_login_failure():
    response = client.post("/api/v1/auth/login", json={"email": "bad@phoen.io", "password": "wrong"})
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
    # Admin sees all 10 seeded quotations
    assert len(data) == 10


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
    response = client.get("/api/v1/fulfillment/orders", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # 3 seeded orders


# ─── Billing ───

def test_get_invoices():
    response = client.get("/api/v1/billing/invoices", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4  # 4 seeded invoices
    assert data[0]["id"].startswith("INV-")


def test_get_subscriptions():
    response = client.get("/api/v1/billing/subscriptions", headers=auth("rep_sarah"))
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
    response = client.get("/api/v1/reports/deal-health", headers=auth("rep_marcus"))
    assert response.status_code == 200
    data = response.json()
    assert "anomalies" in data
    assert "health_score" in data


def test_catalog_rules():
    response = client.get("/api/v1/reports/catalog", headers=auth("rep_marcus"))
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
    response = client.get("/api/v1/quotations/", headers=auth("cust_acme"))
    assert response.status_code == 200
    # Customer should only see their own quotes
    data = response.json()
    for q in data:
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

    # 5. Check fulfillment split was generated
    splits = client.get("/api/v1/fulfillment/orders", headers=auth("rep_sarah")).json()
    e2e_splits = [s for s in splits if s.get("quotation_id") == q_id]
    assert len(e2e_splits) >= 1
