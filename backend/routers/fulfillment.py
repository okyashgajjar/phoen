from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io
from models.base import db
from dependencies import RoleChecker, get_current_user
from models.users import RoleEnum
from pydantic import BaseModel
from typing import Optional, List
from datetime import timezone, datetime
from services.pdf_generator import generate_delivery_challan_pdf

router = APIRouter()

class DispatchPayload(BaseModel):
    carrier: Optional[str] = "Blue Dart Express"
    tracking_number: Optional[str] = None
    warehouse_id: Optional[str] = "WH-001"
    warehouse_name: Optional[str] = "Ahmedabad Enterprise Distribution Center"
    shipping_mode: Optional[str] = "Air Priority Express"
    box_count: Optional[int] = 2
    gross_weight_kg: Optional[float] = 14.5
    serials: Optional[List[str]] = None
    notes: Optional[str] = "Standard freight shipment"

@router.get("/orders")
def get_fulfillment_orders(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    """Return fulfillment orders in frontend-compatible shape."""
    return db.list("fulfillment_splits")

@router.get("/orders/{order_id}")
def get_fulfillment_order(order_id: str, current_user: dict = Depends(get_current_user)):
    order = db.get("fulfillment_splits", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/{order_id}/challan")
def download_delivery_challan(order_id: str, current_user: dict = Depends(get_current_user)):
    """Generate and stream official Delivery Challan & Packing Slip PDF."""
    order = db.get("fulfillment_splits", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    customer = None
    cust_id = order.get("customer_id")
    if cust_id:
        customer = db.get("customers", cust_id) or db.get("users", cust_id)

    dispatch_data = order.get("dispatch") or {}
    lines = order.get("lines") or []
    pdf_bytes = generate_delivery_challan_pdf(order, customer, dispatch_data, lines)

    filename = f"CHALLAN-{order_id}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@router.post("/orders/{order_id}/override")
def override_split(order_id: str, new_splits: list, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    order = db.get("fulfillment_splits", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order["splits"] = new_splits
    order["is_manual_override"] = True
    db.update("fulfillment_splits", order_id, order)
    return order

@router.post("/orders/{order_id}/dispatch")
def dispatch_order(order_id: str, payload: Optional[DispatchPayload] = None, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    order = db.get("fulfillment_splits", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    p = payload or DispatchPayload()
    carrier_name = p.carrier or "Blue Dart Express"
    clean_id = order_id.replace("ORD-", "")
    tracking_no = p.tracking_number or f"BD-EXP-{clean_id}-99"
    wh_name = p.warehouse_name or order.get("warehouse") or "Ahmedabad Enterprise Distribution Center"
    serials = p.serials or order.get("serials") or [f"SN-HW-{clean_id}-01", f"SN-HW-{clean_id}-02"]

    dispatch_info = {
        "carrier": carrier_name,
        "tracking_number": tracking_no,
        "warehouse_id": p.warehouse_id or "WH-001",
        "warehouse_name": wh_name,
        "shipping_mode": p.shipping_mode or "Air Priority Express",
        "box_count": p.box_count or 2,
        "gross_weight_kg": p.gross_weight_kg or 14.5,
        "dispatched_at": datetime.now(timezone.utc).strftime("%d-%b-%Y %H:%M"),
        "dispatched_by": current_user.get("name") or "David Chen",
        "serials": serials,
        "notes": p.notes or "Standard dispatch"
    }

    order["status"] = "DISPATCHED"
    order["statusLabel"] = "Dispatched & In-Transit"
    order["warehouse"] = wh_name
    order["serials"] = serials
    order["dispatch"] = dispatch_info
    
    db.update("fulfillment_splits", order_id, {
        "status": "DISPATCHED",
        "warehouse_id": p.warehouse_id or "WH-001",
        "dispatch": dispatch_info
    })

    try:
        user_id = current_user.get("id", "david-chen") if isinstance(current_user, dict) else getattr(current_user, "id", "david-chen")
        user_name = current_user.get("name", "David Chen") if isinstance(current_user, dict) else getattr(current_user, "name", "David Chen")
        db.insert("audit_logs", f"AUD-DISP-{order_id}", {
            "entity_type": "sales_documents",
            "entity_id": order_id,
            "action": "DISPATCH_SHIPPED",
            "user_id": user_id,
            "notes": f"Order {order_id} dispatched via {carrier_name} (AWB: {tracking_no}) from {wh_name} by {user_name}"
        })
    except Exception:
        pass

    return {
        "status": "success",
        "message": f"Order {order_id} successfully dispatched via {carrier_name} ({tracking_no})",
        "order": order,
        "dispatch": dispatch_info
    }

@router.get("/backorders")
def get_backorders(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    return db.list("backorder_records")

@router.post("/backorders/{backorder_id}/consolidate")
def consolidate_backorder(backorder_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin]))):
    bo = db.get("backorder_records", backorder_id)
    if bo:
        bo["resolved"] = True
        db.update("backorder_records", backorder_id, bo)
    return bo
