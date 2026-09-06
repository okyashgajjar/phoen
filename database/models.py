"""
DealFlow360 Compressed Database Schema (11 Physical Core Tables)
Consolidates 25 original tables into 11 high-performance relational tables.
Includes PostgreSQL JSONB support with SQLite JSON fallback and compatibility aliases.
"""

from sqlalchemy import (
    Column, String, Integer, Float, ForeignKey, DateTime, Boolean, 
    Text, Numeric, UniqueConstraint, CheckConstraint, Index
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TypeDecorator
import json

Base = declarative_base()

# JSON Type compatible with both PostgreSQL and SQLite
class JSONType(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, (dict, list)):
                return json.dumps(value)
            return value
        return '{}'

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                return json.loads(value)
            except Exception:
                return {}
        return {}

# =====================================================================
# TABLE 1: CUSTOMERS (Master Client Entity)
# =====================================================================
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String(50), primary_key=True, index=True) # e.g. CUST-001
    code = Column(String(50), unique=True, nullable=False, index=True)
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    tier = Column(String(50), nullable=False, default='Standard', index=True)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default='India')
    billing_address = Column(Text)
    shipping_address = Column(Text)
    credit_limit = Column(Numeric(18, 2), default=0.0, nullable=False)
    payment_terms_days = Column(Integer, default=30, nullable=False)
    account_manager = Column(String(100))
    status = Column(String(50), default='ACTIVE', nullable=False, index=True)
    metadata_json = Column('metadata', JSONType, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sales_documents = relationship("SalesDocument", back_populates="customer")
    subscriptions = relationship("Subscription", back_populates="customer")


# =====================================================================
# TABLE 2: CATEGORIES (Hierarchical Taxonomy Core)
# =====================================================================
class Category(Base):
    __tablename__ = 'categories'

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(String(50), ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)
    description = Column(Text)
    status = Column(String(50), default='ACTIVE', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    catalog_items = relationship("CatalogItem", foreign_keys="[CatalogItem.category_id]", back_populates="category")


# =====================================================================
# TABLE 3: CATALOG_ITEMS (Products + Services + Plans + Brands)
# =====================================================================
class CatalogItem(Base):
    __tablename__ = 'catalog_items'

    id = Column(String(50), primary_key=True, index=True)
    code = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    item_type = Column(String(50), nullable=False, index=True) # PRODUCT, SERVICE, SUBSCRIPTION_PLAN, BRAND
    category_id = Column(String(50), ForeignKey('categories.id', ondelete='RESTRICT'), nullable=True, index=True)
    subcategory_id = Column(String(50), ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    brand_name = Column(String(100), index=True)
    brand_code = Column(String(50))
    manufacturer_part_number = Column(String(100))
    unit = Column(String(20), default='unit', nullable=False)
    base_cost = Column(Numeric(18, 2), default=0.0, nullable=False)
    base_price = Column(Numeric(18, 2), default=0.0, nullable=False)
    tax_rate = Column(Numeric(5, 2), default=18.00, nullable=False)
    warranty_months = Column(Integer, default=0, nullable=False)
    is_recurring = Column(Boolean, default=False, nullable=False)
    billing_frequency = Column(String(50))
    status = Column(String(50), default='ACTIVE', nullable=False)
    metadata_json = Column('metadata', JSONType, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("item_type IN ('PRODUCT', 'SERVICE', 'SUBSCRIPTION_PLAN', 'BRAND')", name='chk_catalog_item_type'),
    )

    # Relationships
    category = relationship("Category", foreign_keys=[category_id], back_populates="catalog_items")
    subcategory = relationship("Category", foreign_keys=[subcategory_id])
    variants = relationship("Variant", back_populates="catalog_item", cascade="all, delete-orphan")


# =====================================================================
# TABLE 4: VARIANTS (Sellable SKUs + JSONB Hardware Specs)
# =====================================================================
class Variant(Base):
    __tablename__ = 'variants'

    id = Column(String(50), primary_key=True, index=True)
    catalog_item_id = Column(String(50), ForeignKey('catalog_items.id', ondelete='CASCADE'), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    extra_price = Column(Numeric(18, 2), default=0.0, nullable=False)
    cost_price = Column(Numeric(18, 2), nullable=False)
    selling_price = Column(Numeric(18, 2), nullable=False)
    barcode = Column(String(100))
    status = Column(String(50), default='ACTIVE', nullable=False)
    attributes = Column(JSONType, default=dict, nullable=False) # cpu, ram, storage, gpu, screen_size...
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    catalog_item = relationship("CatalogItem", back_populates="variants")
    inventory_items = relationship("Inventory", back_populates="variant")

    # Helper accessors for common attributes
    @property
    def cpu(self):
        return (self.attributes or {}).get('cpu')

    @property
    def ram(self):
        return (self.attributes or {}).get('ram')

    @property
    def storage(self):
        return (self.attributes or {}).get('storage')

    @property
    def gpu(self):
        return (self.attributes or {}).get('gpu')


# =====================================================================
# TABLE 5: WAREHOUSES (Physical Logistics Centers)
# =====================================================================
class Warehouse(Base):
    __tablename__ = 'warehouses'

    id = Column(String(50), primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100))
    country = Column(String(100), default='India')
    warehouse_type = Column(String(50), default='REGIONAL')
    manager_name = Column(String(100))
    capacity_units = Column(Integer, default=10000)
    status = Column(String(50), default='ACTIVE', nullable=False)

    # Relationships
    inventory_records = relationship("Inventory", back_populates="warehouse")


# =====================================================================
# TABLE 6: INVENTORY (Warehouse Balances & Replenishment)
# =====================================================================
class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(String(50), primary_key=True, index=True)
    warehouse_id = Column(String(50), ForeignKey('warehouses.id', ondelete='CASCADE'), nullable=False)
    variant_id = Column(String(50), ForeignKey('variants.id', ondelete='CASCADE'), nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0, nullable=False)
    allocated_quantity = Column(Integer, default=0, nullable=False)
    backorder_quantity = Column(Integer, default=0, nullable=False)
    reorder_level = Column(Integer, default=10, nullable=False)
    reorder_quantity = Column(Integer, default=50, nullable=False)
    safety_stock = Column(Integer, default=5, nullable=False)
    incoming_quantity = Column(Integer, default=0, nullable=False)
    average_daily_demand = Column(Float, default=0.0, nullable=False)
    status = Column(String(50), default='IN_STOCK', nullable=False, index=True)
    last_restocked_at = Column(DateTime)
    next_expected_restock = Column(DateTime)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('warehouse_id', 'variant_id', name='uix_warehouse_variant'),
        Index('ix_inventory_lookup', 'warehouse_id', 'variant_id'),
    )

    # Relationships
    warehouse = relationship("Warehouse", back_populates="inventory_records")
    variant = relationship("Variant", back_populates="inventory_items")


# =====================================================================
# TABLE 7: PRICING_RULES (Unified Pricing & Discount Engine)
# =====================================================================
class PricingRule(Base):
    __tablename__ = 'pricing_rules'

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    rule_type = Column(String(50), nullable=False) # PRICE_LIST, CUSTOMER_OVERRIDE, DISCOUNT_LIMIT, MARGIN_FLOOR
    scope_type = Column(String(50), nullable=False) # GLOBAL, TIER, CUSTOMER, CATEGORY, ITEM, VARIANT
    scope_id = Column(String(50))
    customer_id = Column(String(50), ForeignKey('customers.id', ondelete='CASCADE'), nullable=True)
    variant_id = Column(String(50), ForeignKey('variants.id', ondelete='CASCADE'), nullable=True)
    category_id = Column(String(50), ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    customer_tier = Column(String(50), index=True)
    unit_price = Column(Numeric(18, 2), nullable=True)
    discount_percent = Column(Numeric(5, 2), nullable=True)
    max_discount_percent = Column(Numeric(5, 2), nullable=True)
    min_margin_percent = Column(Numeric(5, 2), nullable=True)
    minimum_quantity = Column(Integer, default=1, nullable=False)
    approval_level = Column(String(50), nullable=True)
    currency = Column(String(10), default='INR', nullable=False)
    effective_from = Column(DateTime)
    effective_to = Column(DateTime)
    active = Column(Boolean, default=True, nullable=False)
    metadata_json = Column('metadata', JSONType, default=dict)

    __table_args__ = (
        Index('ix_pricing_scope', 'scope_type', 'scope_id', 'active'),
        Index('ix_pricing_variant_tier', 'variant_id', 'customer_tier'),
    )


# =====================================================================
# TABLE 8: SALES_DOCUMENTS (Quotations + Orders + Invoices)
# =====================================================================
class SalesDocument(Base):
    __tablename__ = 'sales_documents'

    id = Column(String(50), primary_key=True, index=True)
    document_number = Column(String(100), unique=True, nullable=False, index=True)
    document_type = Column(String(50), nullable=False, index=True) # QUOTATION, ORDER, INVOICE
    customer_id = Column(String(50), ForeignKey('customers.id', ondelete='RESTRICT'), nullable=False, index=True)
    parent_document_id = Column(String(50), ForeignKey('sales_documents.id', ondelete='SET NULL'), nullable=True, index=True)
    document_date = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    currency = Column(String(10), default='INR', nullable=False)
    subtotal = Column(Numeric(18, 2), default=0.0, nullable=False)
    discount_total = Column(Numeric(18, 2), default=0.0, nullable=False)
    tax_total = Column(Numeric(18, 2), default=0.0, nullable=False)
    grand_total = Column(Numeric(18, 2), default=0.0, nullable=False)
    status = Column(String(50), nullable=False, index=True)
    approval_status = Column(String(50), nullable=True)
    deal_health = Column(JSONType, default=dict, nullable=False) # JSON snapshot
    primary_warehouse_id = Column(String(50), ForeignKey('warehouses.id', ondelete='SET NULL'), nullable=True)
    created_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    metadata_json = Column('metadata', JSONType, default=dict, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("document_type IN ('QUOTATION', 'ORDER', 'INVOICE')", name='chk_sales_doc_type'),
        Index('ix_sales_documents_type_status', 'document_type', 'status'),
        Index('ix_sales_documents_customer', 'customer_id', 'document_type'),
    )

    # Relationships
    customer = relationship("Customer", back_populates="sales_documents")
    lines = relationship("DocumentLine", back_populates="document", cascade="all, delete-orphan")
    parent_document = relationship("SalesDocument", remote_side=[id], backref="child_documents")


# =====================================================================
# TABLE 9: DOCUMENT_LINES (Quote Lines + Invoice Lines + Allocations)
# =====================================================================
class DocumentLine(Base):
    __tablename__ = 'document_lines'

    id = Column(String(50), primary_key=True, index=True)
    document_id = Column(String(50), ForeignKey('sales_documents.id', ondelete='CASCADE'), nullable=False, index=True)
    line_number = Column(Integer, nullable=False)
    item_type = Column(String(50), nullable=False) # PRODUCT, SERVICE, SUBSCRIPTION, VARIANT, SUBSCRIPTION_PLAN
    variant_id = Column(String(50), ForeignKey('variants.id', ondelete='SET NULL'), nullable=True, index=True)
    catalog_item_id = Column(String(50), ForeignKey('catalog_items.id', ondelete='SET NULL'), nullable=True)
    description = Column(Text)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(18, 2), nullable=False)
    discount_percent = Column(Numeric(5, 2), default=0.0, nullable=False)
    discount_amount = Column(Numeric(18, 2), default=0.0, nullable=False)
    tax_rate = Column(Numeric(5, 2), default=18.00, nullable=False)
    tax_amount = Column(Numeric(18, 2), default=0.0, nullable=False)
    line_total = Column(Numeric(18, 2), nullable=False)
    billing_type = Column(String(50), nullable=True)
    warehouse_id = Column(String(50), ForeignKey('warehouses.id', ondelete='SET NULL'), nullable=True, index=True)
    fulfillment_status = Column(String(50), default='PENDING', nullable=False)
    allocated_quantity = Column(Integer, default=0, nullable=False)
    negotiation_data = Column(JSONType, default=dict, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("item_type IN ('PRODUCT', 'SERVICE', 'SUBSCRIPTION', 'VARIANT', 'SUBSCRIPTION_PLAN')", name='chk_doc_line_item_type'),
        Index('ix_document_lines_doc_num', 'document_id', 'line_number'),
    )

    # Relationships
    document = relationship("SalesDocument", back_populates="lines")
    variant = relationship("Variant")


# =====================================================================
# TABLE 10: SUBSCRIPTIONS (Customer Recurring Contracts + Plan Terms)
# =====================================================================
class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey('customers.id', ondelete='RESTRICT'), nullable=False, index=True)
    document_id = Column(String(50), ForeignKey('sales_documents.id', ondelete='SET NULL'), nullable=True)
    plan_id = Column(String(50), ForeignKey('catalog_items.id', ondelete='SET NULL'), nullable=True)
    plan_code = Column(String(50), nullable=True)
    plan_name = Column(String(255), nullable=False)
    annual_rate = Column(Numeric(18, 2), nullable=False)
    billing_cycle = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    next_renewal_date = Column(DateTime, nullable=False, index=True)
    status = Column(String(50), default='ACTIVE', nullable=False)
    plan_config = Column(JSONType, default=dict, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="subscriptions")


# =====================================================================
# TABLE 11: AUDIT_LOGS (Unified System Event Ledger)
# =====================================================================
class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(String(50), primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    old_value = Column(JSONType, nullable=True)
    new_value = Column(JSONType, nullable=True)
    performed_by = Column(String(100), nullable=True)
    reason = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index('ix_audit_logs_lookup', 'entity_type', 'entity_id', 'timestamp'),
    )


# =====================================================================
# TABLE 12: PRODUCT_RECOMMENDATIONS (Upsell / Cross-Sell Co-Purchase Graph)
# =====================================================================
# Drives the live suggestion panel beside the quotation cart. Rows are the
# historical co-purchase pairs from the seed dataset: which product tends to
# be bought alongside which, how strong that signal is, and what it does to
# margin. `minimum_margin_percent` is the floor the spec asks for, so only
# healthy-margin suggestions ever surface.
class ProductRecommendation(Base):
    __tablename__ = 'product_recommendations'

    id = Column(String(50), primary_key=True, index=True)
    source_product_id = Column(String(50), ForeignKey('catalog_items.id', ondelete='CASCADE'), nullable=False, index=True)
    recommended_product_id = Column(String(50), ForeignKey('catalog_items.id', ondelete='CASCADE'), nullable=False, index=True)
    recommendation_type = Column(String(50), nullable=False)  # UPSELL, CROSS_SELL, ATTACHMENT
    confidence_score = Column(Float, default=0.0, nullable=False)
    co_purchase_rate = Column(Float, default=0.0, nullable=False)
    margin_delta = Column(Numeric(18, 2), default=0.0, nullable=False)
    priority = Column(Integer, default=99, nullable=False)
    promotion_active = Column(Boolean, default=False, nullable=False)
    minimum_margin_percent = Column(Numeric(5, 2), default=0.0, nullable=False)
    reason = Column(Text)
    status = Column(String(50), default='ACTIVE', nullable=False, index=True)

    __table_args__ = (
        Index('ix_prod_rec_lookup', 'source_product_id', 'status', 'priority'),
    )

    source_product = relationship("CatalogItem", foreign_keys=[source_product_id])
    recommended_product = relationship("CatalogItem", foreign_keys=[recommended_product_id])


# =====================================================================
# TABLE 13: DEAL_HEALTH (Stall / Anomaly / Slippage Scoring per Quotation)
# =====================================================================
class DealHealth(Base):
    __tablename__ = 'deal_health'

    id = Column(String(50), primary_key=True, index=True)
    quotation_id = Column(String(50), ForeignKey('sales_documents.id', ondelete='CASCADE'), nullable=False, index=True)
    days_inactive = Column(Integer, default=0, nullable=False)
    discount_anomaly_score = Column(Float, default=0.0, nullable=False)
    delivery_risk_score = Column(Float, default=0.0, nullable=False)
    approval_delay_score = Column(Float, default=0.0, nullable=False)
    inventory_risk_score = Column(Float, default=0.0, nullable=False)
    overall_health_score = Column(Float, default=0.0, nullable=False)
    health_status = Column(String(50), default='Healthy', nullable=False, index=True)
    recommended_action = Column(Text)
    last_evaluated_at = Column(DateTime)

    quotation = relationship("SalesDocument")


# =====================================================================
# TABLE 14: APPROVAL_CHAINS (Discount Band -> Required Approver)
# =====================================================================
# The configurable side of approval routing, edited from the Discount Tier &
# Approval Chain Setup screen. Bands are expressed in discount percent so an
# admin can retune who signs off without touching code.
class ApprovalChainConfig(Base):
    __tablename__ = 'approval_chains'

    id = Column(String(50), primary_key=True, index=True)
    approval_level = Column(String(50), nullable=False, index=True)
    role_name = Column(String(150), nullable=False)
    min_discount_percent = Column(Numeric(5, 2), default=0.0, nullable=False)
    max_discount_percent = Column(Numeric(5, 2), default=100.0, nullable=False)
    min_margin_percent = Column(Numeric(5, 2), default=0.0, nullable=False)
    approver_role = Column(String(100), nullable=True)
    description = Column(Text)
    active = Column(Boolean, default=True, nullable=False)


# =====================================================================
# TABLE 15: WAREHOUSE_ALLOCATIONS (Persisted Fulfilment Split per Line)
# =====================================================================
class WarehouseAllocation(Base):
    __tablename__ = 'warehouse_allocations'

    id = Column(String(50), primary_key=True, index=True)
    quotation_id = Column(String(50), ForeignKey('sales_documents.id', ondelete='CASCADE'), nullable=False, index=True)
    quotation_line_id = Column(String(50), ForeignKey('document_lines.id', ondelete='CASCADE'), nullable=False, index=True)
    variant_id = Column(String(50), ForeignKey('variants.id', ondelete='SET NULL'), nullable=True)
    warehouse_id = Column(String(50), ForeignKey('warehouses.id', ondelete='SET NULL'), nullable=True, index=True)
    allocated_quantity = Column(Integer, default=0, nullable=False)
    fulfillment_status = Column(String(50), default='ALLOCATED', nullable=False, index=True)
    allocated_at = Column(DateTime)


# =====================================================================
# TABLE 16: APP_USERS (Internal Staff + Customer Portal Logins)
# =====================================================================
# Users previously lived in a hardcoded CORE_USERS dict in
# backend/models/base.py, so signup never persisted and there was no way to
# revoke an account. `password_hash` holds a PBKDF2-SHA256 digest -- never a
# plaintext password.
#
# `customer_id` is what makes the portal a genuinely restricted view: a portal
# login is scoped to exactly one customer, and the portal endpoints refuse any
# document that does not belong to it.
class AppUser(Base):
    __tablename__ = 'app_users'

    id = Column(String(50), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, index=True)  # sales_rep, manager, finance, admin, customer
    tier = Column(String(50), default='Standard')
    status = Column(String(50), default='ACTIVE', nullable=False, index=True)
    customer_id = Column(String(50), ForeignKey('customers.id', ondelete='CASCADE'), nullable=True, index=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "role IN ('sales_rep', 'manager', 'finance', 'admin', 'customer')",
            name='chk_app_user_role',
        ),
    )

    customer = relationship("Customer")


# =====================================================================
# BACKWARD COMPATIBILITY ALIASES FOR LEGACY CODE
# =====================================================================
Product = CatalogItem
Service = CatalogItem
SubscriptionPlan = CatalogItem
ProductVariant = Variant
Quotation = SalesDocument
Order = SalesDocument
Invoice = SalesDocument
QuotationLine = DocumentLine
InvoiceLine = DocumentLine
PriceList = PricingRule
CustomerPriceList = PricingRule
DiscountRule = PricingRule
ApprovalChain = PricingRule
