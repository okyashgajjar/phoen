import pytest
from fastapi.testclient import TestClient
from main import app
from models.base import db
from database.config import SessionLocal
from database.models import PricingRule, AuditLog

client = TestClient(app)

def get_token(role="admin"):
    login_payloads = {
        "admin": {"email": "alex@dealflow360.com", "password": "password"},
        "sales_rep": {"email": "kavita@dealflow360.com", "password": "password"},
        "manager": {"email": "vikram@dealflow360.com", "password": "password"},
    }
    resp = client.post("/api/v1/auth/login", json=login_payloads[role])
    assert resp.status_code == 200
    return resp.json()["access_token"]

def test_admin_get_catalog_rules():
    token = get_token("admin")
    resp = client.get("/api/v1/reports/catalog", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "rules" in data
    assert "products" in data
    assert len(data["rules"]) > 100 # Verify 137+ real rules from DB
    assert len(data["products"]) > 0

    # Verify rule structure
    rule = data["rules"][0]
    assert "id" in rule
    assert "rule_type" in rule
    assert "threshold" in rule
    assert "role" in rule
    assert "active" in rule

def test_admin_pricing_rule_crud_and_audit_log():
    token = get_token("admin")
    rule_id = "TEST-RULE-001"

    # 1. Create rule
    create_payload = {
        "id": rule_id,
        "name": "Test High-Tier Margin Floor",
        "rule_type": "MARGIN_FLOOR",
        "scope_type": "TIER",
        "customer_tier": "Enterprise",
        "min_margin_percent": 18.5,
        "max_discount_percent": 10.0,
        "approval_level": "L2_FINANCE_DIRECTOR",
        "active": True
    }
    create_resp = client.post(
        "/api/v1/reports/catalog/rules",
        json=create_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["id"] == rule_id
    assert created["name"] == "Test High-Tier Margin Floor"
    assert created["min_margin_percent"] == 18.5
    assert created["active"] is True

    # Check persistence in DB
    session = SessionLocal()
    db_rule = session.query(PricingRule).filter(PricingRule.id == rule_id).first()
    assert db_rule is not None
    assert float(db_rule.min_margin_percent) == 18.5
    session.close()

    # 2. Update rule (Toggle active to False and modify discount limit)
    update_payload = {
        "active": False,
        "max_discount_percent": 12.0
    }
    update_resp = client.put(
        f"/api/v1/reports/catalog/rules/{rule_id}",
        json=update_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["active"] is False

    # Check updated in DB
    session = SessionLocal()
    db_rule = session.query(PricingRule).filter(PricingRule.id == rule_id).first()
    assert db_rule.active is False
    assert float(db_rule.max_discount_percent) == 12.0
    session.close()

    # 3. Delete rule
    del_resp = client.delete(
        f"/api/v1/reports/catalog/rules/{rule_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert del_resp.status_code == 200

    session = SessionLocal()
    db_rule = session.query(PricingRule).filter(PricingRule.id == rule_id).first()
    assert db_rule is None
    session.close()

    # 4. Check audit logs
    audit_resp = client.get("/api/v1/reports/audit-logs", headers={"Authorization": f"Bearer {token}"})
    assert audit_resp.status_code == 200
    logs = audit_resp.json()
    assert len(logs) > 0
    rule_actions = [log for log in logs if log.get("entity_id") == rule_id]
    assert len(rule_actions) >= 2 # CREATE, UPDATE, DELETE

def test_admin_user_management_crud():
    token = get_token("admin")

    # 1. Create user
    user_payload = {
        "name": "Integration Test Sales Rep",
        "email": "test_rep_crud@phoen.io",
        "password": "testpassword123",
        "role": "sales_rep",
        "tier": "Strategic"
    }
    create_resp = client.post(
        "/api/v1/auth/users",
        json=user_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_resp.status_code == 200
    created_user = create_resp.json()
    user_id = created_user["id"]
    assert created_user["name"] == "Integration Test Sales Rep"
    assert created_user["tier"] == "Strategic"

    # 2. Update user
    update_payload = {
        "name": "Integration Test Senior Rep",
        "tier": "Enterprise"
    }
    update_resp = client.put(
        f"/api/v1/auth/users/{user_id}",
        json=update_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_resp.status_code == 200
    updated_user = update_resp.json()
    assert updated_user["name"] == "Integration Test Senior Rep"
    assert updated_user["tier"] == "Enterprise"

    # 3. Delete user
    del_resp = client.delete(
        f"/api/v1/auth/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert del_resp.status_code == 200

    # Verify cannot delete self
    self_del_resp = client.delete(
        "/api/v1/auth/users/alex_admin",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert self_del_resp.status_code == 400

def test_rbac_sales_rep_cannot_mutate_rules_or_users():
    rep_token = get_token("sales_rep")

    # Rep cannot create rules
    r1 = client.post(
        "/api/v1/reports/catalog/rules",
        json={"name": "Hacked Rule"},
        headers={"Authorization": f"Bearer {rep_token}"}
    )
    assert r1.status_code == 403

    # Rep cannot update users
    r2 = client.put(
        "/api/v1/auth/users/kavita_sharma",
        json={"name": "Hacked Name"},
        headers={"Authorization": f"Bearer {rep_token}"}
    )
    assert r2.status_code == 403

    # Rep cannot view audit logs
    r3 = client.get(
        "/api/v1/reports/audit-logs",
        headers={"Authorization": f"Bearer {rep_token}"}
    )
    assert r3.status_code == 403
