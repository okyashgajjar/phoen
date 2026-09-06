import os
import sys
import json
from datetime import timezone, datetime, date
from decimal import Decimal
from typing import Dict, Any, List, Optional

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import (
    Customer, SalesDocument, DocumentLine, CatalogItem, Variant,
    PricingRule, Warehouse, Inventory, Subscription, AuditLog, Category
)
from models.sales import normalize_status

# Standard internal users and personas
CORE_USERS = {
    "kavita_sharma": {
        "id": "kavita_sharma",
        "email": "kavita@dealflow360.com",
        "password": "password",
        "role": "sales_rep",
        "name": "Kavita Sharma",
        "tier": "Enterprise"
    },
    "rep_marcus": {
        "id": "rep_marcus",
        "email": "marcus@phoen.io",
        "password": "password",
        "role": "sales_rep",
        "name": "Kavita Sharma",
        "tier": "Enterprise"
    },
    "vikram_singhania": {
        "id": "vikram_singhania",
        "email": "vikram@dealflow360.com",
        "password": "password",
        "role": "manager",
        "name": "Vikramaditya Singhania",
        "tier": "Enterprise"
    },
    "rep_sarah": {
        "id": "rep_sarah",
        "email": "sarah@phoen.io",
        "password": "password",
        "role": "manager",
        "name": "Vikramaditya Singhania",
        "tier": "Enterprise"
    },
    "fin_david": {
        "id": "fin_david",
        "email": "david@phoen.io",
        "password": "password",
        "role": "finance",
        "name": "David Chen",
        "tier": "Enterprise"
    },
    "admin_1": {
        "id": "admin_1",
        "email": "admin@phoen.io",
        "password": "password",
        "role": "admin",
        "name": "Admin User",
        "tier": "Enterprise"
    },
    "alex_admin": {
        "id": "alex_admin",
        "email": "alex@dealflow360.com",
        "password": "password",
        "role": "admin",
        "name": "Alex Mercer",
        "tier": "Enterprise"
    },
    "rep_rachel": {
        "id": "rep_rachel",
        "email": "rachel@phoen.io",
        "password": "password",
        "role": "sales_rep",
        "name": "Meera Rao",
        "tier": "Enterprise"
    }
}

class DealFlowDatabase:
    """
    Direct SQLAlchemy adapter connecting to the real database schema
    (PostgreSQL / SQLite dealflow360.db) with transactional persistence.
    """
    def __init__(self):
        self._memory: Dict[str, Dict[str, Any]] = {
            "users": dict(CORE_USERS)
        }

    def _get_session(self):
        return SessionLocal()

    # ─── Mapping helpers ───
    def _map_line(self, line: DocumentLine) -> dict:
        qty = int(line.quantity or 1)
        unit_price = float(line.unit_price or 0.0)
        disc = float(line.discount_percent or 0.0)
        line_total = float(line.line_total or (qty * unit_price * (1 - disc / 100.0)))
        
        negotiation = {}
        if line.negotiation_data:
            if isinstance(line.negotiation_data, dict):
                negotiation = line.negotiation_data
            else:
                try:
                    negotiation = json.loads(line.negotiation_data)
                except Exception:
                    negotiation = {}

        sku_val = line.variant_id or line.catalog_item_id or line.id
        flagged = disc > 15.0 or bool(negotiation.get("requested_discount", 0) > 15.0)
        flag_reason = f"Exceeds 15% discount threshold ({disc}% applied)" if flagged else None

        return {
            "id": line.id,
            "document_id": line.document_id,
            "line_number": line.line_number,
            "sku": sku_val,
            "product_id": sku_val,
            "name": line.description,
            "description": line.description,
            "category": line.item_type or "Product",
            "qty": qty,
            "quantity": qty,
            "unit_price": unit_price,
            "unitPrice": unit_price,
            "discount": disc,
            "discount_percent": disc,
            "discount_amount": float(line.discount_amount or 0.0),
            "tax_rate": float(line.tax_rate or 18.0),
            "tax_amount": float(line.tax_amount or 0.0),
            "line_total": line_total,
            "warehouse_id": line.warehouse_id,
            "fulfillment_status": line.fulfillment_status or "PENDING",
            "allocated_quantity": int(line.allocated_quantity or 0),
            "negotiation_data": negotiation,
            "flagged": flagged,
            "flagReason": flag_reason,
            "is_recurring": (line.billing_type == "RECURRING")
        }

    def _map_sales_doc(self, doc: SalesDocument) -> dict:
        lines = [self._map_line(l) for l in (doc.lines or [])]
        cust = doc.customer
        if cust:
            cust_name = cust.company_name
            cust_tier = cust.tier or "Standard"
        else:
            u = self.get("users", doc.customer_id) or self.get("customers", doc.customer_id)
            cust_name = (u.get("name") or u.get("company_name")) if u else "Arvind Industrial Systems Pvt Ltd"
            cust_tier = (u.get("tier") or "Standard") if u else "Standard"

        # Single canonical normaliser (models.sales.normalize_status). The old
        # inline map missed ISSUED / AUTHORIZED / DISPATCHED / PAID and any
        # "Approved by <name>" spelling, which then failed enum validation
        # and 500'd the endpoint.
        raw_status = str(doc.status or "DRAFT").strip()
        normalized_status = normalize_status(raw_status)

        created_by = doc.created_by or (cust.account_manager if cust else None) or "Kavita Sharma"
        amount = float(doc.grand_total or 0.0)

        health_data = {}
        if doc.deal_health:
            if isinstance(doc.deal_health, dict):
                health_data = doc.deal_health
            else:
                try:
                    health_data = json.loads(doc.deal_health)
                except Exception:
                    health_data = {}

        return {
            "id": doc.id,
            "document_number": doc.document_number or doc.id,
            "document_type": doc.document_type,
            "customer_id": doc.customer_id,
            "customer_name": cust_name,
            "account": cust_name,
            "customer_tier": cust_tier,
            "sales_rep_id": created_by,
            "created_by": created_by,
            "rep": created_by,
            "status": normalized_status,
            "approval_status": doc.approval_status or ("Pending Review" if normalized_status == "PENDING_APPROVAL" else "Approved"),
            "title": doc.notes if doc.notes else f"Commercial Proposal {doc.id} - {cust_name}",
            "amount": amount,
            "grand_total": amount,
            "subtotal": float(doc.subtotal or 0.0),
            "discount_total": float(doc.discount_total or 0.0),
            "tax_total": float(doc.tax_total or 0.0),
            "currency": doc.currency or "INR",
            "deal_health": health_data,
            "notes": doc.notes or "",
            "quoteId": doc.document_number or f"QT-{doc.id.replace('INV-BILL-', '')}",
            "dueDate": (doc.document_date or datetime.now(timezone.utc)).strftime("%b %d, %Y"),
            "statusLabel": "Paid & Reconciled" if normalized_status == "PAID" else ("Payment Overdue" if normalized_status == "OVERDUE" else "Issued & Awaiting Payment"),
            "amount_formatted": f"₹{amount:,.2f}",
            "created_at": doc.created_at or datetime.now(timezone.utc),
            "updated_at": doc.updated_at or doc.created_at or datetime.now(timezone.utc),
            "lines": lines
        }

    def _map_customer(self, c: Customer) -> dict:
        return {
            "id": c.id,
            "customer_id": c.id,
            "code": c.code,
            "name": c.company_name,
            "company_name": c.company_name,
            "industry": c.industry,
            "tier": c.tier or "Standard",
            "customer_tier": c.tier or "Standard",
            "city": c.city,
            "state": c.state,
            "country": c.country or "India",
            "billing_address": c.billing_address,
            "shipping_address": c.shipping_address,
            "credit_limit": float(c.credit_limit or 0.0),
            "payment_terms_days": int(c.payment_terms_days or 30),
            "account_manager": c.account_manager or "Kavita Sharma",
            "status": c.status or "ACTIVE",
            "role": "customer",
            "email": f"{c.id.lower()}@customer.dealflow360.internal"
        }

    def _map_catalog_item(self, ci: CatalogItem) -> dict:
        return {
            "id": ci.id,
            "product_id": ci.id,
            "code": ci.code,
            "name": ci.name,
            "product_name": ci.name,
            "category": ci.item_type or "PRODUCT",
            "item_type": ci.item_type or "PRODUCT",
            "base_price": float(ci.base_price or 0.0),
            "unit": ci.unit or "unit",
            "tax_rate": float(ci.tax_rate or 18.0),
            "tax_percent": float(ci.tax_rate or 18.0),
            "description": ci.name,
            "is_recurring": bool(ci.is_recurring),
            "status": ci.status or "ACTIVE"
        }

    def _map_subscription(self, s: Subscription) -> dict:
        sub_id = s.id
        if sub_id and sub_id.startswith("SUBREC-"):
            sub_id = sub_id.replace("SUBREC-", "SUB-")
        cust = s.customer
        cust_name = cust.company_name if cust else "Arvind Industrial Systems Pvt Ltd"
        ann_rate = float(s.annual_rate or 0.0)
        mrr_rate = ann_rate / 12.0
        renewal_str = s.next_renewal_date.strftime("%b %d, %Y") if s.next_renewal_date else "Feb 28, 2027"
        status_raw = str(s.status or "ACTIVE").upper()
        status_lbl = "Active Contract" if status_raw == "ACTIVE" else ("Renewal Due" if status_raw == "PENDING_RENEWAL" else status_raw.replace("_", " "))

        return {
            "id": sub_id,
            "raw_id": s.id,
            "customer_id": s.customer_id,
            "account": cust_name,
            "customer_name": cust_name,
            "document_id": s.document_id,
            "plan_id": s.plan_id or s.plan_code or s.id,
            "plan": s.plan_name,
            "plan_name": s.plan_name,
            "annual_rate": ann_rate,
            "arr": f"₹{ann_rate:,.0f} / yr",
            "mrr": f"₹{mrr_rate:,.0f} / mo",
            "billing_cycle": s.billing_cycle or "ANNUAL",
            "start_date": s.start_date.isoformat() if s.start_date else None,
            "next_renewal_date": s.next_renewal_date.isoformat() if s.next_renewal_date else None,
            "renewal": renewal_str,
            "status": status_raw,
            "statusLabel": status_lbl,
            "active": (status_raw == "ACTIVE"),
            "plan_config": s.plan_config or {}
        }

    def _map_warehouse(self, w: Warehouse) -> dict:
        return {
            "id": w.id,
            "code": w.code,
            "name": w.name,
            "city": w.city,
            "state": w.state,
            "country": w.country or "India",
            "type": w.warehouse_type or "REGIONAL",
            "manager_name": w.manager_name or "Logistics Manager",
            "capacity_units": w.capacity_units or 10000,
            "status": w.status or "ACTIVE"
        }

    def _map_audit_log(self, a: AuditLog) -> dict:
        return {
            "id": a.id,
            "entity_type": a.entity_type,
            "entity_id": a.entity_id,
            "action": a.action,
            "old_value": a.old_value,
            "new_value": a.new_value,
            "performed_by": a.performed_by or "System",
            "reason": a.reason or "",
            "timestamp": a.timestamp or datetime.now(timezone.utc)
        }

    def _map_pricing_rule(self, pr: PricingRule) -> dict:
        rule_type = pr.rule_type or "PRICE_LIST"
        approval_lvl = pr.approval_level or "L0_AUTO"

        if rule_type == "MARGIN_FLOOR":
            cat_label = "Margin Floor Governance"
        elif rule_type == "DISCOUNT_LIMIT":
            cat_label = "Discount Cap"
        elif rule_type == "CUSTOMER_OVERRIDE":
            cat_label = "Customer Override"
        else:
            cat_label = "Price List"

        role_map = {
            "L0_AUTO": "Auto-Approval (L0)",
            "L1_SALES_MANAGER": "Sales Manager (L1)",
            "L2_FINANCE_DIRECTOR": "Commercial Finance (L2)",
            "L3_COMMERCIAL_VP": "Commercial VP (L3)",
            "L4_EXECUTIVE_BOARD": "Executive Board (L4)",
        }
        role_label = role_map.get(approval_lvl, approval_lvl)

        threshold_parts = []
        if pr.min_margin_percent is not None:
            threshold_parts.append(f"Min Margin: {float(pr.min_margin_percent):g}%")
        if pr.max_discount_percent is not None:
            threshold_parts.append(f"Max Disc: {float(pr.max_discount_percent):g}%")
        if pr.discount_percent is not None:
            threshold_parts.append(f"Disc: {float(pr.discount_percent):g}%")
        if pr.unit_price is not None:
            threshold_parts.append(f"Unit Price: ₹{float(pr.unit_price):,.2f}")
        if pr.customer_tier:
            threshold_parts.append(f"Tier: {pr.customer_tier}")
        if pr.minimum_quantity and pr.minimum_quantity > 1:
            threshold_parts.append(f"Min Qty: {pr.minimum_quantity}")

        threshold_str = " • ".join(threshold_parts) if threshold_parts else "Standard Policy"

        return {
            "id": pr.id,
            "name": pr.name or f"Rule {pr.id}",
            "rule_type": rule_type,
            "scope_type": pr.scope_type or "GLOBAL",
            "scope_id": pr.scope_id,
            "customer_id": pr.customer_id,
            "variant_id": pr.variant_id,
            "category_id": pr.category_id,
            "customer_tier": pr.customer_tier,
            "unit_price": float(pr.unit_price) if pr.unit_price is not None else None,
            "discount_percent": float(pr.discount_percent) if pr.discount_percent is not None else None,
            "max_discount_percent": float(pr.max_discount_percent) if pr.max_discount_percent is not None else None,
            "min_margin_percent": float(pr.min_margin_percent) if pr.min_margin_percent is not None else None,
            "minimum_quantity": pr.minimum_quantity or 1,
            "approval_level": approval_lvl,
            "currency": pr.currency or "INR",
            "active": bool(pr.active),
            "category": cat_label,
            "threshold": threshold_str,
            "role": role_label,
            "metadata": pr.metadata_json or {}
        }


    # ─── Public CRUD operations ───

    def get(self, collection: str, record_id: str):
        # 1. Check in-memory override first
        if collection in self._memory and record_id in self._memory[collection]:
            return self._memory[collection][record_id]

        session = self._get_session()
        try:
            if collection == "quotations":
                doc = session.query(SalesDocument).filter(
                    (SalesDocument.id == record_id) | (SalesDocument.document_number == record_id)
                ).first()
                if doc:
                    return self._map_sales_doc(doc)
                return None

            elif collection == "customers":
                c = session.query(Customer).filter(
                    (Customer.id == record_id) | (Customer.code == record_id)
                ).first()
                if c:
                    return self._map_customer(c)
                return None

            elif collection == "products":
                ci = session.query(CatalogItem).filter(
                    (CatalogItem.id == record_id) | (CatalogItem.code == record_id)
                ).first()
                if ci:
                    return self._map_catalog_item(ci)
                v = session.query(Variant).filter(
                    (Variant.id == record_id) | (Variant.sku == record_id)
                ).first()
                if v:
                    return {
                        "id": v.id,
                        "product_id": v.id,
                        "code": v.sku,
                        "name": v.name,
                        "category": "PRODUCT",
                        "base_price": float(v.selling_price or 0.0),
                        "unit": "unit",
                        "tax_percent": 18.0,
                        "description": v.name,
                        "is_recurring": False,
                        "status": v.status or "ACTIVE"
                    }
                return None

            elif collection == "users":
                # Check predefined personas
                if record_id in CORE_USERS:
                    return CORE_USERS[record_id]
                for u in CORE_USERS.values():
                    if u["email"] == record_id or u["name"] == record_id:
                        return u
                # Lookup real customer by ID
                c = session.query(Customer).filter(Customer.id == record_id).first()
                if c:
                    return self._map_customer(c)
                return None

            elif collection == "invoices":
                doc = session.query(SalesDocument).filter(
                    SalesDocument.id == record_id,
                    SalesDocument.document_type == "INVOICE"
                ).first()
                if doc:
                    return self._map_sales_doc(doc)
                return None

            elif collection == "subscriptions" or collection == "billing_schedules":
                alt_id = record_id.replace("SUB-", "SUBREC-") if record_id.startswith("SUB-") else record_id.replace("SUBREC-", "SUB-")
                sub = session.query(Subscription).filter((Subscription.id == record_id) | (Subscription.id == alt_id)).first()
                if sub:
                    return self._map_subscription(sub)
                return None

            elif collection == "warehouses":
                wh = session.query(Warehouse).filter(
                    (Warehouse.id == record_id) | (Warehouse.code == record_id)
                ).first()
                if wh:
                    return self._map_warehouse(wh)
                return None

            elif collection == "fulfillment_splits":
                if "fulfillment_splits" in self._memory and record_id in self._memory["fulfillment_splits"]:
                    return self._memory["fulfillment_splits"][record_id]
                all_splits = self.list("fulfillment_splits")
                for s in all_splits:
                    if s["id"] == record_id:
                        return s
                return None

            elif collection == "pricing_rules":
                pr = session.query(PricingRule).filter(PricingRule.id == record_id).first()
                if pr:
                    return self._map_pricing_rule(pr)
                return None

            return None
        finally:
            session.close()

    def list(self, collection: str) -> List[dict]:
        session = self._get_session()
        try:
            if collection == "quotations":
                docs = session.query(SalesDocument).filter(
                    SalesDocument.document_type == "QUOTATION"
                ).all()
                res = [self._map_sales_doc(d) for d in docs]
                # Overlay in-memory creations/modifications
                if "quotations" in self._memory:
                    mem_map = self._memory["quotations"]
                    res = [mem_map.get(q["id"], q) for q in res]
                    for k, v in mem_map.items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            elif collection == "customers":
                custs = session.query(Customer).all()
                res = [self._map_customer(c) for c in custs]
                if "customers" in self._memory:
                    for k, v in self._memory["customers"].items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            elif collection == "products":
                items = session.query(CatalogItem).all()
                res = [self._map_catalog_item(ci) for ci in items]
                if "products" in self._memory:
                    for k, v in self._memory["products"].items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            elif collection == "users":
                res = list(CORE_USERS.values())
                # Add memory users
                if "users" in self._memory:
                    for k, v in self._memory["users"].items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                # Add customers as users with role=customer
                custs = session.query(Customer).all()
                for c in custs:
                    mapped = self._map_customer(c)
                    if mapped["id"] not in [r["id"] for r in res]:
                        res.append(mapped)
                return res

            elif collection == "invoices":
                docs = session.query(SalesDocument).filter(
                    SalesDocument.document_type == "INVOICE"
                ).all()
                res = [self._map_sales_doc(d) for d in docs]
                if "invoices" in self._memory:
                    for k, v in self._memory["invoices"].items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            elif collection == "subscriptions" or collection == "billing_schedules":
                subs = session.query(Subscription).all()
                res = [self._map_subscription(s) for s in subs]
                if "subscriptions" in self._memory:
                    for k, v in self._memory["subscriptions"].items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            elif collection == "warehouses":
                whs = session.query(Warehouse).all()
                res = [self._map_warehouse(w) for w in whs]
                if "warehouses" in self._memory:
                    for k, v in self._memory["warehouses"].items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            elif collection in ["audit_logs", "approval_events"]:
                logs = session.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
                if collection == "audit_logs":
                    return [self._map_audit_log(a) for a in logs]
                # Map for approval_events
                mapped_events = []
                for a in logs:
                    if a.entity_type in ["quotation", "approval"] or str(a.action).lower() in ["approve", "reject"]:
                        mapped_events.append({
                            "id": a.id,
                            "quotation_id": a.entity_id,
                            "actor_id": a.performed_by,
                            "actor_role": "manager" if "vikram" in str(a.performed_by).lower() or "singhania" in str(a.performed_by).lower() else "finance",
                            "action": a.action,
                            "reason": a.reason or "",
                            "timestamp": a.timestamp,
                            "before_state": (a.old_value or {}).get("status") if isinstance(a.old_value, dict) else str(a.old_value or ""),
                            "after_state": (a.new_value or {}).get("status") if isinstance(a.new_value, dict) else str(a.new_value or ""),
                        })
                if "approval_events" in self._memory:
                    for k, v in self._memory["approval_events"].items():
                        if k not in [r["id"] for r in mapped_events]:
                            mapped_events.append(v)
                return mapped_events

            elif collection == "fulfillment_splits":
                orders = session.query(SalesDocument).filter(
                    SalesDocument.document_type.in_(["ORDER", "order"])
                ).all()
                warehouses = session.query(Warehouse).all()
                wh_names = [w.name for w in warehouses] or [
                    "Ahmedabad Enterprise Distribution Center",
                    "Mumbai Western Regional Logistics Hub",
                    "Bengaluru Tech Fulfillment Depot",
                    "Delhi NCR Enterprise Supply Hub",
                    "Hyderabad Cyber Logistics Center"
                ]

                res = []
                for idx, ord_doc in enumerate(orders):
                    cust = ord_doc.customer
                    cust_name = cust.company_name if cust else "Western Grid Technologies Pvt Ltd"
                    wh_assigned = wh_names[idx % len(wh_names)]

                    status_raw = str(ord_doc.status or "CONFIRMED").upper()
                    if status_raw == "CONFIRMED":
                        status_val = "STOCK_RESERVED"
                        status_lbl = "Stock Reserved & Allocated"
                    elif status_raw in ["DISPATCHED", "SHIPPED"]:
                        status_val = "DISPATCHED"
                        status_lbl = "Dispatched & Tracking Enabled"
                    elif status_raw in ["DELIVERED"]:
                        status_val = "DELIVERED"
                        status_lbl = "Delivered to Customer Site"
                    else:
                        status_val = status_raw
                        status_lbl = status_raw.replace("_", " ")

                    lines_count = len(ord_doc.lines or []) or 2
                    clean_id = ord_doc.id.replace("ORD-", "")
                    serials = [f"SN-HW-{clean_id}-{i+1:02d}" for i in range(min(3, max(1, lines_count)))]
                    date_str = ord_doc.document_date.strftime("%b %d, %Y") if ord_doc.document_date else "Feb 27, 2026"

                    res.append({
                        "id": ord_doc.id,
                        "order_id": ord_doc.id,
                        "account": cust_name,
                        "customer_name": cust_name,
                        "quoteId": ord_doc.document_number or f"PO-{ord_doc.id}",
                        "date": date_str,
                        "itemsCount": lines_count,
                        "warehouse": wh_assigned,
                        "amount": float(ord_doc.grand_total or 0.0),
                        "status": status_val,
                        "statusLabel": status_lbl,
                        "serials": serials,
                        "lines": [self._map_line(l) for l in (ord_doc.lines or [])]
                    })

                if "fulfillment_splits" in self._memory:
                    mem_map = self._memory["fulfillment_splits"]
                    res = [mem_map.get(o["id"], o) for o in res]
                    for k, v in mem_map.items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            elif collection == "category_discount_ceilings":
                # Standard ceilings
                return [
                    {"id": "CC-1", "category": "PRODUCT", "max_discount_percent": 25.0},
                    {"id": "CC-2", "category": "Hardware", "max_discount_percent": 15.0},
                    {"id": "CC-3", "category": "Software / SaaS", "max_discount_percent": 30.0},
                    {"id": "CC-4", "category": "Services", "max_discount_percent": 20.0},
                    {"id": "CC-5", "category": "SERVICE", "max_discount_percent": 20.0},
                    {"id": "CC-6", "category": "SUBSCRIPTION_PLAN", "max_discount_percent": 25.0},
                ]

            elif collection == "discount_tiers":
                return [
                    {"id": "DT-1", "customer_tier": "Enterprise", "max_discount_percent": 25.0},
                    {"id": "DT-2", "customer_tier": "Strategic", "max_discount_percent": 20.0},
                    {"id": "DT-3", "customer_tier": "Standard", "max_discount_percent": 15.0},
                    {"id": "DT-4", "customer_tier": "Gold", "max_discount_percent": 25.0},
                    {"id": "DT-5", "customer_tier": "Silver", "max_discount_percent": 18.0},
                    {"id": "DT-6", "customer_tier": "Bronze", "max_discount_percent": 12.0},
                ]

            elif collection == "approval_chain_rules":
                return [
                    {"id": "AR-1", "min_blended_score": 0.0, "max_blended_score": 4.99, "required_role": "sales_rep"},
                    {"id": "AR-2", "min_blended_score": 5.0, "max_blended_score": 14.99, "required_role": "manager"},
                    {"id": "AR-3", "min_blended_score": 15.0, "max_blended_score": 999.0, "required_role": "finance"},
                ]

            elif collection == "pricing_rules":
                rules = session.query(PricingRule).order_by(PricingRule.id.asc()).all()
                res = [self._map_pricing_rule(r) for r in rules]
                if "pricing_rules" in self._memory:
                    mem_map = self._memory["pricing_rules"]
                    res = [mem_map.get(r["id"], r) for r in res]
                    for k, v in mem_map.items():
                        if k not in [r["id"] for r in res]:
                            res.append(v)
                return res

            # In-memory collections fallback
            if collection in self._memory:
                return list(self._memory[collection].values())
            return []
        finally:
            session.close()

    def insert(self, collection: str, record_id: str, data: dict):
        if collection not in self._memory:
            self._memory[collection] = {}
        self._memory[collection][record_id] = data

        # Write through to database if applicable
        if collection in ["audit_logs", "approval_events"]:
            session = self._get_session()
            try:
                log_entry = AuditLog(
                    id=record_id,
                    entity_type=data.get("entity_type") or ("quotation" if data.get("quotation_id") else "system"),
                    entity_id=data.get("entity_id") or data.get("quotation_id") or record_id,
                    action=data.get("action") or "update",
                    old_value={"status": data.get("before_state")} if data.get("before_state") else data.get("old_value"),
                    new_value={"status": data.get("after_state")} if data.get("after_state") else data.get("new_value"),
                    performed_by=data.get("actor_id") or data.get("performed_by") or "Vikramaditya Singhania",
                    reason=data.get("reason") or "",
                    timestamp=data.get("timestamp") or datetime.now(timezone.utc)
                )
                session.add(log_entry)
                session.commit()
            except Exception as e:
                session.rollback()
            finally:
                session.close()

        elif collection == "quotations" or collection == "invoices":
            session = self._get_session()
            try:
                existing = session.query(SalesDocument).filter(SalesDocument.id == record_id).first()
                if not existing:
                    doc_type = "INVOICE" if collection == "invoices" else "QUOTATION"
                    doc_prefix = "INV" if collection == "invoices" else "QT"
                    doc = SalesDocument(
                        id=record_id,
                        document_number=data.get("document_number") or f"{doc_prefix}-{record_id}",
                        document_type=doc_type,
                        customer_id=data.get("customer_id") or "CUST-001",
                        document_date=datetime.now(timezone.utc),
                        currency=data.get("currency") or "INR",
                        subtotal=data.get("subtotal") or data.get("amount", 0.0),
                        discount_total=data.get("discount_total") or 0.0,
                        tax_total=data.get("tax_total") or 0.0,
                        grand_total=data.get("amount") or data.get("grand_total", 0.0),
                        status=data.get("status") or ("ISSUED" if doc_type == "INVOICE" else "DRAFT"),
                        approval_status=data.get("approval_status") or ("Authorized" if doc_type == "INVOICE" else "Pending Review"),
                        created_by=data.get("created_by") or data.get("sales_rep_id") or "David Chen",
                        notes=data.get("notes") or data.get("title") or "Commercial sales invoice"
                    )
                    session.add(doc)
                    session.flush()

                    if doc_type == "INVOICE":
                        amt = float(data.get("amount") or data.get("grand_total") or 0.0)
                        sub_amt = round(amt / 1.18, 2)
                        tax_amt = round(amt - sub_amt, 2)
                        doc_line = DocumentLine(
                            id=f"LINE-{record_id}-01",
                            document_id=record_id,
                            line_number=1,
                            item_type="SERVICE",
                            description=data.get("notes") or data.get("title") or "Enterprise Commercial Hardware & Cloud SaaS Billing",
                            quantity=1,
                            unit_price=amt,
                            discount_percent=0.0,
                            discount_amount=0.0,
                            tax_rate=18.0,
                            tax_amount=tax_amt,
                            line_total=amt,
                            billing_type="ONE_OFF",
                            fulfillment_status="FULFILLED"
                        )
                        session.add(doc_line)

                    session.commit()
            except Exception as e:
                session.rollback()
            finally:
                session.close()

        elif collection == "pricing_rules":
            session = self._get_session()
            try:
                pr = PricingRule(
                    id=record_id,
                    name=data.get("name") or f"Rule {record_id}",
                    rule_type=data.get("rule_type") or "MARGIN_FLOOR",
                    scope_type=data.get("scope_type") or "GLOBAL",
                    scope_id=data.get("scope_id"),
                    customer_id=data.get("customer_id"),
                    variant_id=data.get("variant_id"),
                    category_id=data.get("category_id"),
                    customer_tier=data.get("customer_tier"),
                    unit_price=Decimal(str(data["unit_price"])) if data.get("unit_price") is not None else None,
                    discount_percent=Decimal(str(data["discount_percent"])) if data.get("discount_percent") is not None else None,
                    max_discount_percent=Decimal(str(data["max_discount_percent"])) if data.get("max_discount_percent") is not None else None,
                    min_margin_percent=Decimal(str(data["min_margin_percent"])) if data.get("min_margin_percent") is not None else None,
                    minimum_quantity=int(data.get("minimum_quantity") or 1),
                    approval_level=data.get("approval_level") or "L0_AUTO",
                    currency=data.get("currency") or "INR",
                    active=bool(data.get("active", True)),
                    metadata_json=data.get("metadata", {})
                )
                session.add(pr)

                audit = AuditLog(
                    id=f"AUDIT-RULE-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:18]}",
                    entity_type="pricing_rule",
                    entity_id=record_id,
                    action="CREATE",
                    old_value=None,
                    new_value={"name": pr.name, "rule_type": pr.rule_type, "active": pr.active, "approval_level": pr.approval_level},
                    performed_by=data.get("performed_by") or "System Administrator",
                    reason=data.get("reason") or "Created pricing governance rule via Admin Console",
                    timestamp=datetime.now(timezone.utc)
                )
                session.add(audit)
                session.commit()
            except Exception as e:
                session.rollback()
            finally:
                session.close()

        return data

    def update(self, collection: str, record_id: str, data: dict):
        if collection not in self._memory:
            self._memory[collection] = {}
        if record_id in self._memory[collection]:
            self._memory[collection][record_id].update(data)
        else:
            self._memory[collection][record_id] = data

        # Write through to database for quotations, invoices, subscriptions, and fulfillment orders
        session = self._get_session()
        try:
            if collection in ["quotations", "invoices"]:
                doc = session.query(SalesDocument).filter(SalesDocument.id == record_id).first()
                if doc:
                    if "status" in data:
                        doc.status = data["status"]
                    if "approval_status" in data:
                        doc.approval_status = data["approval_status"]
                    if "amount" in data or "grand_total" in data:
                        doc.grand_total = data.get("amount") or data.get("grand_total")
                    if "notes" in data:
                        doc.notes = data["notes"]
                    
                    # Update or append line items if present
                    if "lines" in data and isinstance(data["lines"], list):
                        for line_data in data["lines"]:
                            lid = line_data.get("id")
                            if lid:
                                d_line = session.query(DocumentLine).filter(DocumentLine.id == lid).first()
                                if d_line:
                                    if "qty" in line_data or "quantity" in line_data:
                                        d_line.quantity = line_data.get("qty") or line_data.get("quantity")
                                    if "discount" in line_data or "discount_percent" in line_data:
                                        d_line.discount_percent = line_data.get("discount") or line_data.get("discount_percent")
                                    if "unit_price" in line_data or "unitPrice" in line_data:
                                        d_line.unit_price = line_data.get("unit_price") or line_data.get("unitPrice")
                                    # Customer negotiation requests and
                                    # fulfilment state were previously dropped
                                    # here, so a portal request was accepted by
                                    # the API and then silently lost.
                                    if "negotiation_data" in line_data:
                                        d_line.negotiation_data = line_data["negotiation_data"] or {}
                                    if "warehouse_id" in line_data:
                                        d_line.warehouse_id = line_data["warehouse_id"]
                                    if "fulfillment_status" in line_data:
                                        d_line.fulfillment_status = line_data["fulfillment_status"]
                                    if "allocated_quantity" in line_data:
                                        d_line.allocated_quantity = line_data["allocated_quantity"] or 0
                                    if "billing_type" in line_data:
                                        d_line.billing_type = line_data["billing_type"]
                                    q = d_line.quantity
                                    p = float(d_line.unit_price)
                                    d = float(d_line.discount_percent or 0.0)
                                    d_line.line_total = q * p * (1 - d / 100.0)

                    # Document-level metadata (counter-offer, requested delivery
                    # date, customer note) also needs to survive the write.
                    if "metadata" in data and isinstance(data["metadata"], dict):
                        merged = dict(doc.metadata_json or {})
                        merged.update(data["metadata"])
                        doc.metadata_json = merged
                    if "approval_status" in data:
                        doc.approval_status = data["approval_status"]
                    if "deal_health" in data and isinstance(data["deal_health"], dict):
                        doc.deal_health = data["deal_health"]
                    session.commit()

            elif collection in ["subscriptions", "billing_schedules"]:
                alt_id = record_id.replace("SUB-", "SUBREC-") if record_id.startswith("SUB-") else record_id.replace("SUBREC-", "SUB-")
                sub = session.query(Subscription).filter((Subscription.id == record_id) | (Subscription.id == alt_id)).first()
                if sub:
                    if "status" in data:
                        sub.status = data["status"]
                    if "annual_rate" in data:
                        sub.annual_rate = data["annual_rate"]
                    session.commit()

            elif collection == "fulfillment_splits":
                ord_doc = session.query(SalesDocument).filter(SalesDocument.id == record_id).first()
                if ord_doc:
                    if "status" in data:
                        ord_doc.status = data["status"]
                        for dl in ord_doc.lines:
                            dl.fulfillment_status = data["status"]
                    if "dispatch" in data:
                        meta = dict(ord_doc.metadata_json or {})
                        meta["dispatch"] = data["dispatch"]
                        ord_doc.metadata_json = meta
                    if "warehouse_id" in data:
                        ord_doc.primary_warehouse_id = data["warehouse_id"]
                    session.commit()

            elif collection == "pricing_rules":
                pr = session.query(PricingRule).filter(PricingRule.id == record_id).first()
                if pr:
                    old_state = {
                        "name": pr.name,
                        "active": pr.active,
                        "min_margin_percent": float(pr.min_margin_percent) if pr.min_margin_percent is not None else None,
                        "max_discount_percent": float(pr.max_discount_percent) if pr.max_discount_percent is not None else None,
                        "approval_level": pr.approval_level
                    }
                    if "active" in data:
                        pr.active = bool(data["active"])
                    if "name" in data:
                        pr.name = data["name"]
                    if "rule_type" in data:
                        pr.rule_type = data["rule_type"]
                    if "min_margin_percent" in data and data["min_margin_percent"] is not None:
                        pr.min_margin_percent = Decimal(str(data["min_margin_percent"]))
                    if "max_discount_percent" in data and data["max_discount_percent"] is not None:
                        pr.max_discount_percent = Decimal(str(data["max_discount_percent"]))
                    if "approval_level" in data and data["approval_level"]:
                        pr.approval_level = data["approval_level"]
                    if "customer_tier" in data:
                        pr.customer_tier = data["customer_tier"]

                    audit = AuditLog(
                        id=f"AUDIT-RULE-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:18]}",
                        entity_type="pricing_rule",
                        entity_id=record_id,
                        action="UPDATE",
                        old_value=old_state,
                        new_value={"name": pr.name, "active": pr.active, "approval_level": pr.approval_level},
                        performed_by=data.get("performed_by") or "System Administrator",
                        reason=data.get("reason") or "Modified pricing rule via Admin Console",
                        timestamp=datetime.now(timezone.utc)
                    )
                    session.add(audit)
                    session.commit()

            elif collection == "users":
                if record_id in CORE_USERS:
                    CORE_USERS[record_id].update(data)
                c = session.query(Customer).filter(Customer.id == record_id).first()
                if c:
                    if "name" in data or "company_name" in data:
                        c.company_name = data.get("name") or data.get("company_name")
                    if "tier" in data:
                        c.tier = data["tier"]
                    if "status" in data:
                        c.status = data["status"]

                audit = AuditLog(
                    id=f"AUDIT-USER-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:18]}",
                    entity_type="user",
                    entity_id=record_id,
                    action="UPDATE",
                    old_value={"id": record_id},
                    new_value={k: v for k, v in data.items() if k != "password"},
                    performed_by=data.get("performed_by") or "System Administrator",
                    reason=data.get("reason") or "Updated user profile via Admin Console",
                    timestamp=datetime.now(timezone.utc)
                )
                session.add(audit)
                session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()

        if collection in self._memory and record_id in self._memory[collection]:
            return self._memory[collection][record_id]
        return self.get(collection, record_id) or data

    def delete(self, collection: str, record_id: str):
        deleted = False
        if collection in self._memory and record_id in self._memory[collection]:
            del self._memory[collection][record_id]
            deleted = True

        session = self._get_session()
        try:
            if collection == "pricing_rules":
                pr = session.query(PricingRule).filter(PricingRule.id == record_id).first()
                if pr:
                    old_name = pr.name
                    session.delete(pr)
                    audit = AuditLog(
                        id=f"AUDIT-RULE-DEL-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:18]}",
                        entity_type="pricing_rule",
                        entity_id=record_id,
                        action="DELETE",
                        old_value={"name": old_name, "id": record_id},
                        new_value=None,
                        performed_by="System Administrator",
                        reason="Deleted pricing rule via Admin Console",
                        timestamp=datetime.now(timezone.utc)
                    )
                    session.add(audit)
                    session.commit()
                    deleted = True
            elif collection == "users":
                if record_id in CORE_USERS:
                    del CORE_USERS[record_id]
                    deleted = True
                audit = AuditLog(
                    id=f"AUDIT-USER-DEL-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:18]}",
                    entity_type="user",
                    entity_id=record_id,
                    action="DELETE",
                    old_value={"id": record_id},
                    new_value=None,
                    performed_by="System Administrator",
                    reason="User account removed or deactivated via Admin Console",
                    timestamp=datetime.now(timezone.utc)
                )
                session.add(audit)
                session.commit()
                deleted = True
        except Exception:
            session.rollback()
        finally:
            session.close()

        return deleted

# Global database instance
db = DealFlowDatabase()
