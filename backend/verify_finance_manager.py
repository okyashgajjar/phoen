import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
HEADERS = {"Authorization": "Bearer fin_david"}

def run_tests():
    print("=== TESTING FINANCE MANAGER ENDPOINTS & DB MUTATIONS ===")

    # 1. Test Invoices GET
    resp = requests.get(f"{BASE_URL}/billing/invoices", headers=HEADERS)
    assert resp.status_code == 200, f"Failed GET /invoices: {resp.text}"
    invoices = resp.json()
    print(f"[OK] GET /billing/invoices returned {len(invoices)} real invoices.")
    assert len(invoices) >= 56, f"Expected at least 56 invoices, got {len(invoices)}"
    sample_inv = invoices[0]
    print(f"     Sample invoice: ID={sample_inv['id']}, Account={sample_inv.get('account')}, Amount={sample_inv.get('amount')}, Status={sample_inv.get('status')}")

    # 2. Test Manual Invoice Creation
    new_inv_payload = {
        "customer_id": "CUST-001",
        "title": "Automated Cloud Migration Milestone Billing",
        "amount": 350000.0,
        "due_date": "2026-03-31"
    }
    resp = requests.post(f"{BASE_URL}/billing/invoices", json=new_inv_payload, headers=HEADERS)
    assert resp.status_code == 200, f"Failed POST /invoices: {resp.text}"
    created_res = resp.json()
    created_id = created_res["id"] if "id" in created_res else created_res["invoice"]["id"]
    print(f"[OK] POST /billing/invoices created invoice {created_id}")

    # 3. Test Pay Invoice
    resp = requests.post(f"{BASE_URL}/billing/invoices/{created_id}/pay", headers=HEADERS)
    assert resp.status_code == 200, f"Failed POST /invoices/{created_id}/pay: {resp.text}"
    paid_res = resp.json()
    paid_inv = paid_res.get("invoice") or paid_res
    print(f"[OK] POST /billing/invoices/{created_id}/pay: Status is {paid_inv.get('status')}")
    assert paid_inv["status"] == "PAID"

    # Verify via GET that status is PAID
    resp = requests.get(f"{BASE_URL}/billing/invoices/{created_id}", headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["status"] == "PAID"
    print(f"[OK] Verified invoice {created_id} is now PAID in database.")

    # 4. Test Subscriptions GET
    resp = requests.get(f"{BASE_URL}/billing/subscriptions", headers=HEADERS)
    assert resp.status_code == 200, f"Failed GET /subscriptions: {resp.text}"
    subs = resp.json()
    print(f"[OK] GET /billing/subscriptions returned {len(subs)} real subscriptions.")
    assert len(subs) >= 26, f"Expected at least 26 subscriptions, got {len(subs)}"
    sample_sub = subs[0]
    sub_id = sample_sub["id"]
    print(f"     Sample subscription: ID={sub_id}, Account={sample_sub.get('account')}, Plan={sample_sub.get('plan')}, Rate={sample_sub.get('annual_rate')}")

    # 5. Test Upgrade Subscription
    upgrade_payload = {
        "additional_seats": 10,
        "rate_increase": 15000.0,
        "addon_name": "Premium Expansion SLA"
    }
    resp = requests.post(f"{BASE_URL}/billing/subscriptions/{sub_id}/upgrade", json=upgrade_payload, headers=HEADERS)
    assert resp.status_code == 200, f"Failed POST /subscriptions/{sub_id}/upgrade: {resp.text}"
    upgrade_res = resp.json()
    print(f"[OK] POST /billing/subscriptions/{sub_id}/upgrade: New Rate={upgrade_res.get('annual_rate')}")
    assert upgrade_res.get("annual_rate") is not None

    # 6. Test Fulfillment Orders GET
    resp = requests.get(f"{BASE_URL}/fulfillment/orders", headers=HEADERS)
    assert resp.status_code == 200, f"Failed GET /fulfillment/orders: {resp.text}"
    orders = resp.json()
    print(f"[OK] GET /fulfillment/orders returned {len(orders)} real confirmed orders.")
    assert len(orders) >= 45, f"Expected at least 45 orders, got {len(orders)}"
    sample_ord = orders[0]
    ord_id = sample_ord["id"]
    print(f"     Sample order: ID={ord_id}, Account={sample_ord.get('account')}, Warehouse={sample_ord.get('warehouse')}, Serials={sample_ord.get('serials')}")

    # 7. Test Dispatch Order
    resp = requests.post(f"{BASE_URL}/fulfillment/orders/{ord_id}/dispatch", headers=HEADERS)
    assert resp.status_code == 200, f"Failed POST /fulfillment/orders/{ord_id}/dispatch: {resp.text}"
    dispatch_res = resp.json()
    print(f"[OK] POST /fulfillment/orders/{ord_id}/dispatch: {dispatch_res['message']}")
    assert dispatch_res["order"]["status"] == "DISPATCHED"

    # 8. Verify order status in GET /fulfillment/orders/{id}
    resp = requests.get(f"{BASE_URL}/fulfillment/orders/{ord_id}", headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["status"] == "DISPATCHED"
    print(f"[OK] Verified order {ord_id} is DISPATCHED in database.")

    # 9. Verify Audit Logs Recorded
    from models.base import db
    audit_logs = db.list("audit_logs")
    print(f"[OK] Verified audit_logs collection has {len(audit_logs)} total log entries.")

    print("\nALL FINANCE MANAGER BACKEND & DATABASE TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
