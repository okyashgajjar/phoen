"""
Product catalog — mockup Screens 16 and 17, spec A2.

Screen 16 is the catalog list; Screen 17 is one product with its three panels:
general info, variants, and the tier / currency price lists.

The existing /products router returns a flat pydantic Product with no variants,
no price rules and no stock, so there was nothing for a detail screen to render.
"""

import os
import sys
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import (
    CatalogItem, Variant, Category, PricingRule, Inventory, Warehouse, DocumentLine
)
from models.users import RoleEnum
from dependencies import RoleChecker, get_current_user

router = APIRouter()

INTERNAL_ROLES = [RoleEnum.admin, RoleEnum.manager, RoleEnum.finance, RoleEnum.sales_rep]


def _f(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def _margin(cost, price) -> float:
    price, cost = _f(price), _f(cost)
    return round((price - cost) / price * 100, 1) if price > 0 else 0.0


@router.get("/catalog")
def list_catalog(
    search: Optional[str] = None,
    category_id: Optional[str] = None,
    item_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    current_user: dict = Depends(RoleChecker(INTERNAL_ROLES)),
):
    """Screen 16 — the product catalog list, with the header counters."""
    session = SessionLocal()
    try:
        categories = {c.id: c.name for c in session.query(Category).all()}

        q = session.query(CatalogItem)
        if search:
            like = f"%{search.lower().strip()}%"
            # Match against name, code, brand, manufacturer part number, or matching variant names/skus
            matched_variant_item_ids = session.query(Variant.catalog_item_id).filter(
                func.lower(Variant.name).like(like) | func.lower(Variant.sku).like(like)
            ).distinct()
            q = q.filter(
                func.lower(CatalogItem.name).like(like)
                | func.lower(CatalogItem.code).like(like)
                | func.lower(CatalogItem.brand_name).like(like)
                | func.lower(CatalogItem.manufacturer_part_number).like(like)
                | CatalogItem.id.in_(matched_variant_item_ids)
            )
        if category_id:
            q = q.filter(CatalogItem.category_id == category_id)
        if item_type:
            q = q.filter(CatalogItem.item_type == item_type)
        if status:
            q = q.filter(CatalogItem.status == status)

        total = q.count()
        rows = q.order_by(CatalogItem.name).offset(offset).limit(limit).all()
        ids = [r.id for r in rows]

        variant_counts = dict(
            session.query(Variant.catalog_item_id, func.count(Variant.id))
            .filter(Variant.catalog_item_id.in_(ids))
            .group_by(Variant.catalog_item_id)
            .all()
        ) if ids else {}

        # Aggregate live warehouse stock across variants
        stock_by_item = {}
        if ids:
            var_rows = session.query(Variant.id, Variant.catalog_item_id).filter(Variant.catalog_item_id.in_(ids)).all()
            var_to_item = {v.id: v.catalog_item_id for v in var_rows}
            if var_to_item:
                inv_rows = (
                    session.query(
                        Inventory.variant_id,
                        func.sum(Inventory.available_quantity).label("avail"),
                        func.sum(Inventory.reserved_quantity).label("res"),
                    )
                    .filter(Inventory.variant_id.in_(list(var_to_item.keys())))
                    .group_by(Inventory.variant_id)
                    .all()
                )
                for inv in inv_rows:
                    cat_id = var_to_item.get(inv.variant_id)
                    free = max(0, int(inv.avail or 0) - int(inv.res or 0))
                    stock_by_item[cat_id] = stock_by_item.get(cat_id, 0) + free

        products = [{
            "id": r.id,
            "code": r.code,
            "name": r.name,
            "item_type": r.item_type,
            "category_id": r.category_id,
            "category": categories.get(r.category_id),
            "brand": r.brand_name,
            "unit": r.unit,
            "base_cost": _f(r.base_cost),
            "base_price": _f(r.base_price),
            "margin_percent": _margin(r.base_cost, r.base_price),
            "tax_rate": _f(r.tax_rate, 18.0),
            "is_recurring": bool(r.is_recurring),
            "billing_frequency": r.billing_frequency,
            "variant_count": variant_counts.get(r.id, 0),
            "stock_available": stock_by_item.get(r.id, 0),
            "status": r.status,
        } for r in rows]

        return {
            "products": products,
            "total": total,
            "offset": offset,
            "limit": limit,
            "summary": {
                "total_products": session.query(CatalogItem).count(),
                "active": session.query(CatalogItem).filter(CatalogItem.status == "ACTIVE").count(),
                "archived": session.query(CatalogItem).filter(CatalogItem.status != "ACTIVE").count(),
                "variants": session.query(Variant).count(),
                "pricing_rules": session.query(PricingRule).filter(PricingRule.active.is_(True)).count(),
                "categories": len(categories),
            },
            "categories": [{"id": k, "name": v} for k, v in sorted(categories.items())],
        }
    finally:
        session.close()


@router.get("/catalog/{product_id}")
def product_detail(
    product_id: str,
    current_user: dict = Depends(RoleChecker(INTERNAL_ROLES)),
):
    """
    Screen 17 — one product: general info, variants with their attributes and
    extra prices, the tier / currency price lists, and live stock per warehouse.
    """
    session = SessionLocal()
    try:
        item = session.query(CatalogItem).filter(CatalogItem.id == product_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Product not found")

        category = (
            session.query(Category).filter(Category.id == item.category_id).first()
            if item.category_id else None
        )

        variants = session.query(Variant).filter(Variant.catalog_item_id == item.id).all()
        variant_ids = [v.id for v in variants]

        stock_rows = []
        if variant_ids:
            stock_rows = (
                session.query(Inventory, Warehouse)
                .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
                .filter(Inventory.variant_id.in_(variant_ids))
                .all()
            )

        stock_by_variant = {}
        on_hand = 0
        for inv, wh in stock_rows:
            available = int(inv.available_quantity or 0)
            reserved = int(inv.reserved_quantity or 0)
            on_hand += available
            stock_by_variant.setdefault(inv.variant_id, []).append({
                "warehouse_id": wh.id,
                "warehouse": wh.name,
                "city": wh.city,
                "available": available,
                "reserved": reserved,
                "free": max(0, available - reserved),
                "reorder_level": int(inv.reorder_level or 0),
                "status": inv.status,
            })

        # Attributes are stored per variant as a JSON blob; roll them up into
        # the attribute/values/extra-price table the mockup shows.
        attribute_rollup = {}
        for v in variants:
            for key, value in (v.attributes or {}).items():
                if value in (None, "", "-"):
                    continue
                bucket = attribute_rollup.setdefault(key, {"values": [], "extra_prices": []})
                if value not in bucket["values"]:
                    bucket["values"].append(value)
                    bucket["extra_prices"].append(_f(v.extra_price))

        pricing = (
            session.query(PricingRule)
            .filter(PricingRule.active.is_(True))
            .filter(
                (PricingRule.category_id == item.category_id)
                | (PricingRule.variant_id.in_(variant_ids) if variant_ids else False)
            )
            .all()
        )

        price_lists = [{
            "rule_id": r.id,
            "name": r.name,
            "rule_type": r.rule_type,
            "scope": r.scope_type,
            "tier": r.customer_tier or r.scope_id,
            "currency": r.currency or "INR",
            "unit_price": _f(r.unit_price) if r.unit_price is not None else None,
            "discount_percent": _f(r.discount_percent) if r.discount_percent is not None else None,
            "max_discount_percent": _f(r.max_discount_percent) if r.max_discount_percent is not None else None,
            "min_margin_percent": _f(r.min_margin_percent) if r.min_margin_percent is not None else None,
            "approval_level": r.approval_level,
            "rule": (
                f"Capped at {_f(r.max_discount_percent)}% discount"
                if r.max_discount_percent is not None
                else f"Fixed price {_f(r.unit_price):,.2f}"
                if r.unit_price is not None
                else f"Minimum margin {_f(r.min_margin_percent)}%"
                if r.min_margin_percent is not None
                else "Base price, no adjustment"
            ),
        } for r in pricing]

        times_quoted = (
            session.query(func.count(DocumentLine.id))
            .filter(DocumentLine.catalog_item_id == item.id)
            .scalar()
        ) or 0

        return {
            "general": {
                "id": item.id,
                "code": item.code,
                "name": item.name,
                "description": item.metadata_json.get("description") if isinstance(item.metadata_json, dict) else None,
                "item_type": item.item_type,
                "category_id": item.category_id,
                "category": category.name if category is not None else None,
                "brand": item.brand_name,
                "manufacturer_part_number": item.manufacturer_part_number,
                "unit": item.unit,
                "base_cost": _f(item.base_cost),
                "base_price": _f(item.base_price),
                "margin_percent": _margin(item.base_cost, item.base_price),
                "tax_rate": _f(item.tax_rate, 18.0),
                "warranty_months": int(item.warranty_months or 0),
                # The mockup's "if subscription yes then recurring will be visible"
                "is_subscription": bool(item.is_recurring),
                "billing_frequency": item.billing_frequency,
                "quantity_on_hand": on_hand,
                "status": item.status,
                "times_quoted": times_quoted,
            },
            "variants": [{
                "id": v.id,
                "sku": v.sku,
                "name": v.name,
                "attributes": v.attributes or {},
                "extra_price": _f(v.extra_price),
                "cost_price": _f(v.cost_price),
                "selling_price": _f(v.selling_price),
                "margin_percent": _margin(v.cost_price, v.selling_price),
                "status": v.status,
                "stock": stock_by_variant.get(v.id, []),
                "total_free": sum(s["free"] for s in stock_by_variant.get(v.id, [])),
            } for v in variants],
            "attribute_summary": [{
                "attribute": k.replace("_", " ").title(),
                "values": v["values"],
                "extra_prices": v["extra_prices"],
            } for k, v in attribute_rollup.items()],
            "price_lists": price_lists,
            "stock_summary": {
                "total_on_hand": on_hand,
                "warehouses": len({s["warehouse_id"] for rows in stock_by_variant.values() for s in rows}),
            },
        }
    finally:
        session.close()
