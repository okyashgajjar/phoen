import requests
import json
import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import SalesDocument, DocumentLine, AuditLog

BASE_URL = "http://127.0.0.1:8000/api/v1"
HEADERS = {"Authorization": "Bearer fin_david"}

def run_tests():
    print("=== TESTING MANUAL INVOICE CREATION, PDF DOWNLOAD & DISPATCH WORKFLOW ===")

    # 1. Test Manual Invoice Creation with real customer
    payload = {
        "customer_id": "CUST-002",
        "title": "Industrial High-Performance Cloud Computing Cluster License",
        "amount": 425000.0,
        "due_date": "2026-04-15",
        "notes": "Custom high-density server nodes"
    }
    resp = requests.post(f"{BASE_URL}/billing/invoices", json=payload, headers=HEADERS)
    assert resp.status_code == 200, f"Failed create invoice: {resp.text}"
    inv_data = resp.json()
    inv_id = inv_data["id"]
    print(f"[OK] Created manual invoice: ID={inv_id}, Title='{inv_data.get('title')}', Amount=INR {inv_data.get('amount'):,.2f}")

    # 2. Test Download Invoice PDF
    pdf_resp = requests.get(f"{BASE_URL}/billing/invoices/{inv_id}/pdf", headers=HEADERS)
    assert pdf_resp.status_code == 200, f"Failed download invoice PDF: {pdf_resp.text}"
    assert "application/pdf" in pdf_resp.headers.get("Content-Type", "")
    assert pdf_resp.content.startswith(b"%PDF"), "Response is not a valid PDF file"
    assert len(pdf_resp.content) > 1000
    print(f"[OK] Downloaded Invoice PDF: Size={len(pdf_resp.content)} bytes, Header={pdf_resp.headers.get('Content-Disposition')}")

    # 3. Verify Database records in dealflow360.db
    session = SessionLocal()
    try:
        doc = session.query(SalesDocument).filter(SalesDocument.id == inv_id).first()
        assert doc is not None, "Invoice SalesDocument not found in database"
        assert doc.document_type == "INVOICE"
        assert float(doc.grand_total) == 425000.0
        print(f"[OK] Verified SalesDocument in database: DocNo={doc.document_number}, Customer={doc.customer_id}, Status={doc.status}")

        lines = session.query(DocumentLine).filter(DocumentLine.document_id == inv_id).all()
        assert len(lines) > 0, "No DocumentLine found for invoice"
        print(f"[OK] Verified {len(lines)} DocumentLine(s) in database: Desc='{lines[0].description}', Total=INR {float(lines[0].line_total):,.2f}")
    finally:
        session.close()

    # 4. Test Industry-Level Order Dispatch with Courier & AWB
    orders_resp = requests.get(f"{BASE_URL}/fulfillment/orders", headers=HEADERS)
    assert orders_resp.status_code == 200
    orders = orders_resp.json()
    target_order = None
    for o in orders:
        if o.get("status") in ["STOCK_RESERVED", "CONFIRMED"]:
            target_order = o
            break
    if not target_order:
        target_order = orders[0]

    order_id = target_order["id"]
    dispatch_payload = {
        "carrier": "Blue Dart Express",
        "tracking_number": f"BD-AIR-9928104",
        "warehouse_id": "WH-001",
        "warehouse_name": "Ahmedabad Enterprise Distribution Center",
        "shipping_mode": "Air Priority Express (Next-Day Air)",
        "box_count": 3,
        "gross_weight_kg": 21.6,
        "serials": ["SN-HW-0002-01", "SN-HW-0002-02", "SN-HW-0002-03"],
        "notes": "Fragile server racks securely palletized."
    }

    disp_resp = requests.post(f"{BASE_URL}/fulfillment/orders/{order_id}/dispatch", json=dispatch_payload, headers=HEADERS)
    assert disp_resp.status_code == 200, f"Failed dispatch order: {disp_resp.text}"
    disp_res = disp_resp.json()
    print(f"[OK] Dispatched Order {order_id}: Carrier={disp_res['dispatch']['carrier']}, AWB={disp_res['dispatch']['tracking_number']}")
    assert disp_res["order"]["status"] == "DISPATCHED"

    # 5. Test Download Delivery Challan PDF
    chal_resp = requests.get(f"{BASE_URL}/fulfillment/orders/{order_id}/challan", headers=HEADERS)
    assert chal_resp.status_code == 200, f"Failed download challan: {chal_resp.text}"
    assert "application/pdf" in chal_resp.headers.get("Content-Type", "")
    assert chal_resp.content.startswith(b"%PDF"), "Delivery Challan response is not a valid PDF file"
    assert len(chal_resp.content) > 1000
    print(f"[OK] Downloaded Delivery Challan PDF: Size={len(chal_resp.content)} bytes, Header={chal_resp.headers.get('Content-Disposition')}")

    # 6. Verify Dispatch Metadata & Audit Log in dealflow360.db
    session = SessionLocal()
    try:
        ord_doc = session.query(SalesDocument).filter(SalesDocument.id == order_id).first()
        assert ord_doc is not None
        assert ord_doc.status == "DISPATCHED"
        assert ord_doc.metadata_json.get("dispatch", {}).get("tracking_number") == "BD-AIR-9928104"
        print(f"[OK] Verified Order in database: Status={ord_doc.status}, Metadata AWB={ord_doc.metadata_json['dispatch']['tracking_number']}")

        audit = session.query(AuditLog).filter(AuditLog.entity_id == order_id).order_by(AuditLog.timestamp.desc()).first()
        assert audit is not None
        print(f"[OK] Verified AuditLog in database: Action={audit.action}, PerformedBy={audit.performed_by}")
    finally:
        session.close()

    print("\nALL INVOICE GENERATION, PDF ENGINE & DISPATCH WORKFLOW TESTS PASSED 100%!")

if __name__ == "__main__":
    run_tests()
