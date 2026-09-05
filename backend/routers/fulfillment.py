from fastapi import APIRouter, Depends, HTTPException
from models.base import db
from dependencies import RoleChecker, get_current_user
from models.users import RoleEnum

router = APIRouter()

@router.get("/orders")
def get_fulfillment_orders(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.manager, RoleEnum.sales_rep, RoleEnum.admin]))):
    """Return fulfillment orders in frontend-compatible shape."""
    return db.list("fulfillment_splits")

@router.get("/orders/{order_id}")
def get_fulfillment_order(order_id: str, current_user: dict = Depends(get_current_user)):
    order = db.get("fulfillment_splits", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders/{order_id}/override")
def override_split(order_id: str, new_splits: list, current_user: dict = Depends(RoleChecker([RoleEnum.finance]))):
    order = db.get("fulfillment_splits", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order["splits"] = new_splits
    order["is_manual_override"] = True
    db.update("fulfillment_splits", order_id, order)
    return order

@router.get("/backorders")
def get_backorders(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.manager]))):
    return db.list("backorder_records")

@router.post("/backorders/{backorder_id}/consolidate")
def consolidate_backorder(backorder_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.finance]))):
    bo = db.get("backorder_records", backorder_id)
    if bo:
        bo["resolved"] = True
        db.update("backorder_records", backorder_id, bo)
    return bo
