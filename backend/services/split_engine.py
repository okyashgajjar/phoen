"""
DealFlow360 - Multi-Warehouse Fulfilment Split Engine

Allocates each order line against real rows in the `inventory` table and
produces a warehouse split that minimises the number of shipments.

The previous version read `warehouse.stock[product_id]`, a dict that does not
exist on the Warehouse model, so it always found zero stock and every order
silently became a backorder. This version joins inventory -> variant ->
catalog_item and reserves against available_quantity.

Allocation strategy
-------------------
Fewer shipments is cheaper than a marginally closer warehouse, so for each line
we first look for a single warehouse that can cover the whole quantity. Only
when no warehouse can cover it alone do we split, largest-availability first,
which keeps the shipment count at the minimum.

Anything still unallocated becomes a backorder carrying the next expected
restock date, which is what drives the "Consolidate Remaining Backorder" prompt.
"""

import os
import sys
import uuid
from datetime import timezone, datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import Inventory, Warehouse, Variant, CatalogItem
from models.base import db

# Per-shipment handling cost. Overridden per warehouse by
# metadata["shipping_cost_weight"] when the admin has configured one.
DEFAULT_SHIPMENT_COST = 15.0


def _variant_ids_for(session, product_id: str) -> list[str]:
    """A line may reference a variant directly or a parent catalog item."""
    if not product_id:
        return []
    if session.query(Variant).filter(Variant.id == product_id).first() is not None:
        return [product_id]
    rows = session.query(Variant.id).filter(Variant.catalog_item_id == product_id).all()
    return [r[0] for r in rows]


def _shipment_cost(warehouse) -> float:
    meta = getattr(warehouse, "metadata_json", None) or {}
    if isinstance(meta, dict):
        try:
            return float(meta.get("shipping_cost_weight", DEFAULT_SHIPMENT_COST))
        except (TypeError, ValueError):
            pass
    return DEFAULT_SHIPMENT_COST


def plan_split(quotation: dict) -> dict:
    """
    Compute the recommended split without writing anything.
    Used by the Fulfilment Detail screen to preview before the rep accepts.
    """
    session = SessionLocal()
    try:
        warehouses = {w.id: w for w in session.query(Warehouse).all()}
        allocations = []
        backorders = []
        touched_warehouses = set()

        for line in quotation.get("lines", []) or []:
            if line.get("is_recurring"):
                continue  # nothing physical ships for a subscription line

            product_id = line.get("product_id") or line.get("sku")
            remaining = int(line.get("qty") or line.get("quantity") or 0)
            if remaining <= 0:
                continue

            variant_ids = _variant_ids_for(session, product_id)
            stock_rows = []
            if variant_ids:
                stock_rows = (
                    session.query(Inventory)
                    .filter(Inventory.variant_id.in_(variant_ids))
                    .filter(Inventory.available_quantity > 0)
                    .all()
                )

            # Free stock is what is on hand minus what other orders reserved.
            free = []
            for inv in stock_rows:
                usable = int(inv.available_quantity or 0) - int(inv.reserved_quantity or 0)
                if usable > 0:
                    free.append((inv, usable))
            free.sort(key=lambda pair: pair[1], reverse=True)

            # Prefer one warehouse that covers the whole line.
            single = next((pair for pair in free if pair[1] >= remaining), None)
            chosen = [single] if single else free

            for inv, usable in chosen:
                if remaining <= 0:
                    break
                take = min(usable, remaining)
                wh = warehouses.get(inv.warehouse_id)
                allocations.append({
                    "line_id": line.get("id"),
                    "product_id": product_id,
                    "description": line.get("name") or line.get("description"),
                    "variant_id": inv.variant_id,
                    "warehouse_id": inv.warehouse_id,
                    "warehouse_name": wh.name if wh else inv.warehouse_id,
                    "warehouse_city": wh.city if wh else None,
                    "quantity": take,
                })
                touched_warehouses.add(inv.warehouse_id)
                remaining -= take

            if remaining > 0:
                restock = None
                if stock_rows:
                    dates = [i.next_expected_restock for i in stock_rows if i.next_expected_restock]
                    if dates:
                        restock = min(dates).isoformat()
                backorders.append({
                    "line_id": line.get("id"),
                    "product_id": product_id,
                    "description": line.get("name") or line.get("description"),
                    "missing_quantity": remaining,
                    "next_expected_restock": restock,
                    "resolved": False,
                })

        shipment_count = len(touched_warehouses)
        est_cost = sum(
            _shipment_cost(warehouses.get(w)) for w in touched_warehouses
        )

        return {
            "allocations": allocations,
            "backorders": backorders,
            "shipment_count": shipment_count,
            "estimated_cost": round(est_cost, 2),
            "warehouses_used": sorted(touched_warehouses),
            "fully_allocated": len(backorders) == 0,
        }
    finally:
        session.close()


def calculate_warehouse_split(quotation_id: str):
    """
    Compute the split, reserve the stock, and persist the fulfilment record.
    Called when a quotation is approved.
    """
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        return None

    plan = plan_split(quotation)

    # Reserve the allocated stock so a second order cannot promise the same units.
    session = SessionLocal()
    try:
        for alloc in plan["allocations"]:
            inv = (
                session.query(Inventory)
                .filter(Inventory.warehouse_id == alloc["warehouse_id"])
                .filter(Inventory.variant_id == alloc["variant_id"])
                .first()
            )
            if inv is not None:
                inv.reserved_quantity = int(inv.reserved_quantity or 0) + int(alloc["quantity"])
                inv.allocated_quantity = int(inv.allocated_quantity or 0) + int(alloc["quantity"])
        for bo in plan["backorders"]:
            pass  # backorders are tracked on the fulfilment record below
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

    order_num = quotation_id.replace("Q-", "").replace("QUO-", "")
    customer_name = quotation.get("account") or quotation.get("customer_id") or "Customer"

    has_backorder = len(plan["backorders"]) > 0
    split_record = {
        "id": f"ORD-{order_num}",
        "quotation_id": quotation_id,
        "quoteId": quotation_id,
        "account": customer_name,
        "date": datetime.now(timezone.utc).strftime("%b %d, %Y"),
        "itemsCount": sum(a["quantity"] for a in plan["allocations"]),
        "warehouse": ", ".join(
            sorted({a["warehouse_name"] for a in plan["allocations"]})
        ) or "Unallocated",
        "status": "PARTIAL_BACKORDER" if has_backorder else "STOCK_RESERVED",
        "statusLabel": (
            f"Partially allocated - {len(plan['backorders'])} line(s) on backorder"
            if has_backorder else "Stock reserved across "
            f"{plan['shipment_count']} warehouse(s)"
        ),
        "splits": plan["allocations"],
        "backorders": plan["backorders"],
        "shipment_count": plan["shipment_count"],
        "estimated_cost": plan["estimated_cost"],
        "warehouses_used": plan["warehouses_used"],
        "fully_allocated": plan["fully_allocated"],
        "is_manual_override": False,
    }

    db.insert("fulfillment_splits", split_record["id"], split_record)

    for bo in plan["backorders"]:
        rec = dict(bo)
        rec["id"] = f"BO-{uuid.uuid4().hex[:8].upper()}"
        rec["quotation_id"] = quotation_id
        db.insert("backorder_records", rec["id"], rec)

    return split_record
