"""
DealFlow360 - Discount Governance Rule Resolver

Single source of truth for "what discount is this line actually allowed?".

Every ceiling is read from the pricing_rules table (rule_type = DISCOUNT_LIMIT).
Nothing here is hardcoded: if the admin edits a rule in the Discount Tier screen,
the next quotation recalculation picks it up immediately.

Resolution order for one line (most specific wins):
  1. TIER + CATEGORY rule   -> "Gold customers get 10% on Services"
  2. CATEGORY rule          -> "Services cap at 10% for everyone"
  3. TIER rule              -> "Gold customers get 15% overall"
  4. GLOBAL rule            -> company-wide backstop
"""

import os
import sys
from functools import lru_cache

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import PricingRule, CatalogItem, Variant, Customer

# Fallback used only when the pricing_rules table has no applicable row at all.
# This is a backstop against a mis-seeded database, not a business rule.
ABSOLUTE_BACKSTOP_CEILING = 15.0


def _f(value, default=0.0):
    """Numeric/Decimal columns come back as Decimal; normalise to float."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class RuleBook:
    """
    Loads every active DISCOUNT_LIMIT / MARGIN_FLOOR rule once, then answers
    per-line ceiling questions in memory. Built per scoring pass so a rule
    edit is visible on the very next recalculation.
    """

    def __init__(self, session=None):
        self._own_session = session is None
        self.session = session or SessionLocal()

        rules = (
            self.session.query(PricingRule)
            .filter(PricingRule.active.is_(True))
            .all()
        )

        self.tier_category = {}   # (tier, category_id) -> rule
        self.category_only = {}   # category_id         -> rule
        self.tier_only = {}       # tier                -> rule
        self.global_rules = []
        self.margin_floors = {}   # category_id         -> min margin %

        for r in rules:
            if r.rule_type == "MARGIN_FLOOR":
                key = r.category_id or "*"
                self.margin_floors[key] = _f(r.min_margin_percent)
                continue

            if r.rule_type != "DISCOUNT_LIMIT":
                continue

            tier = r.customer_tier or (r.scope_id if r.scope_type == "TIER" else None)
            cat = r.category_id

            if tier and cat:
                self.tier_category[(tier, cat)] = r
            elif cat:
                self.category_only[cat] = r
            elif tier:
                self.tier_only[tier] = r
            else:
                self.global_rules.append(r)

        # Item -> category lookup, resolved lazily and cached.
        self._item_category = {}
        self._variant_parent = {}

    # ─────────────────────────────────────────────────────────────
    # Category resolution
    # ─────────────────────────────────────────────────────────────
    def category_for(self, product_id: str) -> str | None:
        """
        A quotation line stores either a variant id or a catalog item id in
        product_id/sku. Resolve either one down to its real category id.
        """
        if not product_id:
            return None
        if product_id in self._item_category:
            return self._item_category[product_id]

        cat = None
        item = self.session.query(CatalogItem).filter(CatalogItem.id == product_id).first()
        if item is not None:
            cat = item.category_id
        else:
            variant = self.session.query(Variant).filter(Variant.id == product_id).first()
            if variant is not None:
                parent = (
                    self.session.query(CatalogItem)
                    .filter(CatalogItem.id == variant.catalog_item_id)
                    .first()
                )
                if parent is not None:
                    cat = parent.category_id

        self._item_category[product_id] = cat
        return cat

    def tier_for_customer(self, customer_id: str) -> str:
        if not customer_id:
            return "Standard"
        c = self.session.query(Customer).filter(Customer.id == customer_id).first()
        return (c.tier if c is not None and c.tier else "Standard")

    # ─────────────────────────────────────────────────────────────
    # Ceiling resolution
    # ─────────────────────────────────────────────────────────────
    def ceiling_for(self, tier: str, category_id: str | None) -> tuple[float, str, str]:
        """
        Return (max_discount_percent, approval_level, rule_source).
        rule_source names which rule won, so the Approval Detail screen can
        explain *why* a line was flagged instead of just asserting it.
        """
        if tier and category_id and (tier, category_id) in self.tier_category:
            r = self.tier_category[(tier, category_id)]
            return _f(r.max_discount_percent, ABSOLUTE_BACKSTOP_CEILING), (r.approval_level or ""), f"{tier}/{category_id}"

        if category_id and category_id in self.category_only:
            r = self.category_only[category_id]
            return _f(r.max_discount_percent, ABSOLUTE_BACKSTOP_CEILING), (r.approval_level or ""), f"category {category_id}"

        if tier and tier in self.tier_only:
            r = self.tier_only[tier]
            return _f(r.max_discount_percent, ABSOLUTE_BACKSTOP_CEILING), (r.approval_level or ""), f"tier {tier}"

        if self.global_rules:
            r = min(self.global_rules, key=lambda x: _f(x.max_discount_percent, 100.0))
            return _f(r.max_discount_percent, ABSOLUTE_BACKSTOP_CEILING), (r.approval_level or ""), "global policy"

        return ABSOLUTE_BACKSTOP_CEILING, "", "system backstop"

    def close(self):
        if self._own_session:
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
