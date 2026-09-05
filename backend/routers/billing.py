from fastapi import APIRouter, Depends, HTTPException
from models.base import db
from dependencies import get_current_user, RoleChecker
from models.users import RoleEnum

router = APIRouter()

@router.get("/invoices")
def get_invoices(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin, RoleEnum.sales_rep, RoleEnum.manager]))):
    """Return invoices in frontend-compatible shape."""
    return db.list("invoices")

@router.get("/subscriptions")
def get_subscriptions(current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.admin, RoleEnum.manager]))):
    """Return subscription billing schedules in frontend-compatible shape."""
    return db.list("billing_schedules")

@router.post("/subscriptions/{schedule_id}/cancel")
def cancel_subscription(schedule_id: str, current_user: dict = Depends(RoleChecker([RoleEnum.finance, RoleEnum.manager]))):
    schedule = db.get("billing_schedules", schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Subscription not found")
    schedule["active"] = False
    schedule["status"] = "CANCELLED"
    db.update("billing_schedules", schedule_id, schedule)
    return schedule
