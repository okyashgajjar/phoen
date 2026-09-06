"""
Create customer records for ids that sales documents reference but that never
existed in the `customers` table.

Nine ids (cust_acme, cust_nova, cust_zenith, ...) carried 40+ documents between
them with no matching customer row. Consequences:

  * the tier lookup found nothing and silently fell back to "Standard", so the
    discount engine scored those deals against the wrong ceilings
  * the account name came from a hardcoded fallback string in base.py
  * a portal login could not be scoped to them at all

Tier is inferred from what the account actually buys: total document value puts
it in the same bands the seeded customers use.

    python scripts/repair_orphan_customers.py
"""

import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from database.config import SessionLocal, engine, DATABASE_URL
from database.models import Base, Customer, SalesDocument
from sqlalchemy import func

# Value thresholds (INR) matching the spread of the seeded customer base.
TIER_BANDS = [
    (50_000_000, "Strategic"),
    (10_000_000, "Enterprise"),
    (2_000_000, "Standard"),
    (0, "SMB"),
]

NAME_OVERRIDES = {
    "cust_acme": "Acme Corp",
    "cust_apex": "Apex Manufacturing",
    "cust_cyberdyne": "Cyberdyne Systems",
    "cust_enterprise": "Enterprise Holdings",
    "cust_global": "Global Logistics",
    "cust_nova": "Nova Retail",
    "cust_starlight": "Starlight Media",
    "cust_techcorp": "TechCorp Industries",
    "cust_zenith": "Zenith Co",
}


def tier_for(total: float) -> str:
    for threshold, tier in TIER_BANDS:
        if total >= threshold:
            return tier
    return "SMB"


def main():
    print(f"database: {DATABASE_URL}")
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        known = {c.id for c in session.query(Customer.id).all()}
        orphans = (
            session.query(
                SalesDocument.customer_id,
                func.count(SalesDocument.id),
                func.coalesce(func.sum(SalesDocument.grand_total), 0),
            )
            .group_by(SalesDocument.customer_id)
            .all()
        )

        created = 0
        for cid, doc_count, total in orphans:
            if not cid or cid in known:
                continue

            total = float(total or 0)
            tier = tier_for(total)
            name = NAME_OVERRIDES.get(
                cid, cid.replace("cust_", "").replace("_", " ").title()
            )

            session.add(Customer(
                id=cid,
                code=cid.upper().replace("CUST_", "CUST-"),
                company_name=name,
                industry="Technology",
                tier=tier,
                city="Mumbai",
                state="Maharashtra",
                country="India",
                credit_limit=max(total, 1_000_000),
                payment_terms_days=30,
                account_manager="Kavita Sharma",
                status="ACTIVE",
                created_at=datetime.utcnow(),
            ))
            created += 1
            print(f"  {cid:20} {name:26} {doc_count:>3} docs  INR {total:>15,.0f}  -> {tier}")

        session.commit()

        remaining = session.execute(
            SalesDocument.__table__.select().where(
                ~SalesDocument.customer_id.in_(
                    session.query(Customer.id).scalar_subquery()
                )
            )
        ).fetchall()
        print()
        print(f"  customers created        : {created}")
        print(f"  documents still orphaned : {len(remaining)}")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
