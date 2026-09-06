"""
Move users out of the hardcoded CORE_USERS dict and into the database, with
PBKDF2 password hashes.

Before this, `backend/models/base.py` held eight personas in a Python dict with
plaintext passwords, so signup never persisted, an account could not be
disabled, and the bearer token was the user's own id.

Also provisions a portal login for a handful of real customers, which is what
makes the customer portal a genuinely separate, restricted view rather than an
internal screen with a different label.

    python scripts/seed_users.py
    python scripts/seed_users.py --portal-logins 25

Idempotent: an existing account is updated in place, and its password is only
rehashed when it is still plaintext or below the current work factor.
"""

import argparse
import os
import sys
import unicodedata
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env"))

from database.config import SessionLocal, engine, DATABASE_URL
from database.models import Base, AppUser, Customer
from services.security import hash_password, needs_rehash

DEFAULT_PASSWORD = "password"

# The internal personas the demo logs in as.
STAFF = [
    ("kavita_sharma",     "kavita@dealflow360.com",  "Kavita Sharma",          "sales_rep", "Enterprise"),
    ("rep_marcus",        "marcus@dealflow360.com",  "Marcus Rodrigues",       "sales_rep", "Enterprise"),
    ("rep_rachel",        "rachel@dealflow360.com",  "Meera Rao",              "sales_rep", "Enterprise"),
    ("vikram_singhania",  "vikram@dealflow360.com",  "Vikramaditya Singhania", "manager",   "Enterprise"),
    ("mgr_sarah",         "sarah@dealflow360.com",   "Sarah Jenkins",          "manager",   "Enterprise"),
    ("fin_david",         "david@dealflow360.com",   "David Chen",             "finance",   "Enterprise"),
    ("alex_admin",        "alex@dealflow360.com",    "Alex Mercer",            "admin",     "Enterprise"),
    ("admin_1",           "admin@dealflow360.com",   "Admin User",             "admin",     "Enterprise"),
]


# Portal accounts the demo and tests rely on, with fixed addresses.
PINNED_PORTAL_EMAILS = {
    "cust_acme": "acme@portal.dealflow360.com",
    "cust_zenith": "zenith@portal.dealflow360.com",
}


def portal_email(customer) -> str:
    """A stable, readable portal login derived from the company name."""
    if customer.id in PINNED_PORTAL_EMAILS:
        return PINNED_PORTAL_EMAILS[customer.id]
    raw = unicodedata.normalize("NFKD", customer.company_name or customer.id)
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in raw)
    slug = "-".join(part for part in slug.split("-") if part)[:40].strip("-")
    return f"{slug}@portal.dealflow360.com"


def upsert(session, user_id, email, name, role, tier, customer_id=None):
    existing = (
        session.query(AppUser)
        .filter((AppUser.id == user_id) | (AppUser.email == email))
        .first()
    )
    if existing is not None:
        existing.email = email
        existing.name = name
        existing.role = role
        existing.tier = tier
        existing.customer_id = customer_id
        if existing.status is None:
            existing.status = "ACTIVE"
        if needs_rehash(existing.password_hash or ""):
            existing.password_hash = hash_password(DEFAULT_PASSWORD)
            return "rehashed"
        return "kept"

    session.add(AppUser(
        id=user_id,
        email=email,
        password_hash=hash_password(DEFAULT_PASSWORD),
        name=name,
        role=role,
        tier=tier,
        status="ACTIVE",
        customer_id=customer_id,
        created_at=datetime.utcnow(),
    ))
    return "created"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portal-logins", type=int, default=15,
                    help="how many customers get a portal login (default 15)")
    args = ap.parse_args()

    print(f"database: {DATABASE_URL}")
    Base.metadata.create_all(engine)

    session = SessionLocal()
    try:
        counts = {"created": 0, "rehashed": 0, "kept": 0}

        for user_id, email, name, role, tier in STAFF:
            counts[upsert(session, user_id, email, name, role, tier)] += 1
        print(f"  staff accounts   : {counts}")

        counts = {"created": 0, "rehashed": 0, "kept": 0}

        # Prefer customers that actually have a quotation the portal can show.
        # Seeding the first N customers by id gave accounts whose quotes were
        # all drafts or rejects, so the portal opened empty in a demo.
        from database.models import SalesDocument
        from models.sales import normalize_status
        VISIBLE = {"READY", "NEGOTIATION", "APPROVED", "CONFIRMED", "WON", "DISPATCHED", "PAID"}

        ranked = {}
        for doc in session.query(SalesDocument).filter(SalesDocument.document_type == "QUOTATION"):
            if normalize_status(doc.status) in VISIBLE and doc.customer_id:
                ranked[doc.customer_id] = ranked.get(doc.customer_id, 0) + 1

        preferred = [cid for cid, _ in sorted(ranked.items(), key=lambda kv: kv[1], reverse=True)]

        # Always provision these, whatever the ranking: the seeded demo data and
        # the test suite both log in as them.
        for pinned in ("cust_acme", "cust_zenith"):
            if pinned in preferred:
                preferred.remove(pinned)
            preferred.insert(0, pinned)
        customers = []
        seen = set()
        for cid in preferred:
            c = session.query(Customer).filter(Customer.id == cid).first()
            if c is not None and c.id not in seen:
                customers.append(c)
                seen.add(c.id)
            if len(customers) >= args.portal_logins:
                break
        if len(customers) < args.portal_logins:
            for c in (session.query(Customer)
                      .filter(Customer.status == "ACTIVE")
                      .order_by(Customer.id).all()):
                if c.id not in seen:
                    customers.append(c)
                    seen.add(c.id)
                if len(customers) >= args.portal_logins:
                    break
        for c in customers:
            counts[upsert(
                session,
                user_id=f"portal_{c.id}",
                email=portal_email(c),
                name=f"{c.company_name} (Portal)",
                role="customer",
                tier=c.tier or "Standard",
                customer_id=c.id,
            )] += 1
        print(f"  portal logins    : {counts}")

        session.commit()

        total = session.query(AppUser).count()
        hashed = sum(
            1 for u in session.query(AppUser).all()
            if (u.password_hash or "").startswith("pbkdf2_sha256$")
        )
        print(f"  users in database: {total} ({hashed} with hashed passwords)")
        print()
        print("  Sample logins (password: 'password')")
        for u in session.query(AppUser).order_by(AppUser.role).limit(4):
            print(f"    {u.role:10} {u.email}")
        for u in session.query(AppUser).filter(AppUser.role == "customer").limit(2):
            n = ranked.get(u.customer_id, 0)
            print(f"    {'customer':10} {u.email}")
            print(f"    {'':10}   scoped to {u.customer_id}, {n} visible quotation(s)")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
