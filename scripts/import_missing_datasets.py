"""
Import the seed datasets that the original importer never loaded.

Four CSVs in seed-data-mumbai/ had no table to land in, which is why whole
features had nothing real to run on:

    product_recommendations.csv (744)  -> the upsell / cross-sell panel
    deal_health.csv             (100)  -> the Deal Health & Anomaly dashboard
    approval_chains.csv         (5)    -> the configurable approval bands
    warehouse_allocations.csv   (392)  -> the persisted fulfilment split

Run after scripts/backfill_line_links.py. Idempotent - existing rows are
replaced, so re-running is safe.

    python scripts/import_missing_datasets.py

If the database sits on a mounted or synced folder and SQLite raises
"disk I/O error", copy it to a local disk, run this, and copy it back.
"""

import csv
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

CSV_DIR = os.path.join(ROOT, "seed-data-mumbai")

from database.config import SessionLocal, engine, DATABASE_URL
from database.models import (
    Base, ProductRecommendation, DealHealth, ApprovalChainConfig,
    WarehouseAllocation, CatalogItem, SalesDocument, DocumentLine,
    Variant, Warehouse,
)


def _bool(v):
    return str(v).strip().lower() in ("true", "1", "yes", "y")


def _f(v, default=0.0):
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return default


def _i(v, default=0):
    try:
        return int(float(str(v).strip()))
    except (TypeError, ValueError):
        return default


def _dt(v):
    if not v:
        return None
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _rows(name):
    path = os.path.join(CSV_DIR, name)
    if not os.path.exists(path):
        print(f"  ! missing {name}, skipped")
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    print(f"database: {DATABASE_URL}")
    Base.metadata.create_all(engine)

    session = SessionLocal()
    try:
        items = {r[0] for r in session.query(CatalogItem.id)}
        docs = {r[0] for r in session.query(SalesDocument.id)}
        lines = {r[0] for r in session.query(DocumentLine.id)}
        variants = {r[0] for r in session.query(Variant.id)}
        warehouses = {r[0] for r in session.query(Warehouse.id)}

        # The seed CSVs use the regional id space (QT-MUM-0001); the database
        # was loaded with the prefix stripped (QT-0001). Map between them.
        def doc_id(raw):
            raw = (raw or "").strip()
            if raw in docs:
                return raw
            candidate = raw.replace("QT-MUM-", "QT-")
            return candidate if candidate in docs else None

        # ── product_recommendations ─────────────────────────────────
        session.query(ProductRecommendation).delete()
        kept = skipped = 0
        for r in _rows("product_recommendations.csv"):
            src, tgt = r["source_product_id"].strip(), r["recommended_product_id"].strip()
            if src not in items or tgt not in items:
                skipped += 1
                continue
            session.add(ProductRecommendation(
                id=r["recommendation_id"].strip(),
                source_product_id=src,
                recommended_product_id=tgt,
                recommendation_type=r["recommendation_type"].strip(),
                confidence_score=_f(r["confidence_score"]),
                co_purchase_rate=_f(r["co_purchase_rate"]),
                margin_delta=_f(r["margin_delta"]),
                priority=_i(r["priority"], 99),
                promotion_active=_bool(r["promotion_active"]),
                minimum_margin_percent=_f(r["minimum_margin_percent"]),
                reason=r.get("reason"),
                status=r.get("status", "ACTIVE").strip(),
            ))
            kept += 1
        print(f"  product_recommendations : {kept} imported, {skipped} skipped")

        # ── deal_health ─────────────────────────────────────────────
        session.query(DealHealth).delete()
        kept = skipped = 0
        for r in _rows("deal_health.csv"):
            did = doc_id(r["quotation_id"])
            if not did:
                skipped += 1
                continue
            session.add(DealHealth(
                id=r["deal_health_id"].strip(),
                quotation_id=did,
                days_inactive=_i(r["days_inactive"]),
                discount_anomaly_score=_f(r["discount_anomaly_score"]),
                delivery_risk_score=_f(r["delivery_risk_score"]),
                approval_delay_score=_f(r["approval_delay_score"]),
                inventory_risk_score=_f(r["inventory_risk_score"]),
                overall_health_score=_f(r["overall_health_score"]),
                health_status=r["health_status"].strip(),
                recommended_action=r.get("recommended_action"),
                last_evaluated_at=_dt(r.get("last_evaluated_at")),
            ))
            kept += 1
        print(f"  deal_health             : {kept} imported, {skipped} skipped")

        # ── approval_chains ─────────────────────────────────────────
        session.query(ApprovalChainConfig).delete()
        kept = 0
        for r in _rows("approval_chains.csv"):
            approver = (r.get("approver_role") or "").strip()
            session.add(ApprovalChainConfig(
                id=r["chain_id"].strip(),
                approval_level=r["approval_level"].strip(),
                role_name=r["role_name"].strip(),
                min_discount_percent=_f(r["min_discount_percent"]),
                max_discount_percent=_f(r["max_discount_percent"], 100.0),
                min_margin_percent=_f(r["min_margin_percent"]),
                approver_role=None if approver.lower() in ("", "none") else approver,
                description=r.get("description"),
                active=True,
            ))
            kept += 1
        print(f"  approval_chains         : {kept} imported")

        # ── warehouse_allocations ───────────────────────────────────
        session.query(WarehouseAllocation).delete()
        kept = skipped = 0
        for r in _rows("warehouse_allocations.csv"):
            did = doc_id(r["quotation_id"])
            lid = r["quotation_line_id"].strip()
            if not did or lid not in lines:
                skipped += 1
                continue
            vid = r["variant_id"].strip()
            wid = r["warehouse_id"].strip()
            session.add(WarehouseAllocation(
                id=r["allocation_id"].strip(),
                quotation_id=did,
                quotation_line_id=lid,
                variant_id=vid if vid in variants else None,
                warehouse_id=wid if wid in warehouses else None,
                allocated_quantity=_i(r["allocated_quantity"]),
                fulfillment_status=r.get("fulfillment_status", "ALLOCATED").strip(),
                allocated_at=_dt(r.get("allocated_at")),
            ))
            kept += 1
        print(f"  warehouse_allocations   : {kept} imported, {skipped} skipped")

        session.commit()
        print("committed.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
