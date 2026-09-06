from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean, Text, Numeric, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(String(50), primary_key=True, index=True) # e.g. BRD-001
    name = Column(String(100), nullable=False)
    code = Column(String(50))
    country = Column(String(100))
    support_level = Column(String(50))
    status = Column(String(50))

class Category(Base):
    __tablename__ = 'categories'
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(String(50), ForeignKey('categories.id'), nullable=True)
    description = Column(Text)
    status = Column(String(50))
    
    subcategories = relationship("Category")

class Product(Base):
    __tablename__ = 'products'
    id = Column(String(50), primary_key=True, index=True)
    code = Column(String(100))
    name = Column(String(255), nullable=False)
    brand_id = Column(String(50), ForeignKey('brands.id'))
    category_id = Column(String(50), ForeignKey('categories.id'))
    subcategory_id = Column(String(50), ForeignKey('categories.id'), nullable=True)
    product_type = Column(String(50))
    description = Column(Text)
    manufacturer_part_number = Column(String(100))
    unit = Column(String(20))
    base_cost = Column(Numeric(18, 2))
    base_price = Column(Numeric(18, 2))
    tax_rate = Column(Numeric(5, 2))
    warranty_months = Column(Integer)
    status = Column(String(50))
    is_serialized = Column(Boolean)
    is_recurring = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    brand = relationship("Brand")
    category = relationship("Category", foreign_keys=[category_id])
    subcategory = relationship("Category", foreign_keys=[subcategory_id])
    variants = relationship("ProductVariant", back_populates="product")

class ProductVariant(Base):
    __tablename__ = 'product_variants'
    id = Column(String(50), primary_key=True, index=True)
    product_id = Column(String(50), ForeignKey('products.id'))
    sku = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    cpu = Column(String(100))
    ram = Column(String(100))
    storage = Column(String(100))
    storage_type = Column(String(50))
    gpu = Column(String(100))
    screen_size = Column(String(50))
    resolution = Column(String(50))
    color = Column(String(50))
    connectivity = Column(String(100))
    operating_system = Column(String(100))
    form_factor = Column(String(50))
    warranty_months = Column(Integer)
    extra_price = Column(Numeric(18, 2))
    cost_price = Column(Numeric(18, 2))
    selling_price = Column(Numeric(18, 2))
    barcode = Column(String(100))
    status = Column(String(50))

    product = relationship("Product", back_populates="variants")

class Warehouse(Base):
    __tablename__ = 'warehouses'
    id = Column(String(50), primary_key=True, index=True)
    code = Column(String(50), unique=True)
    name = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    warehouse_type = Column(String(50))
    manager_name = Column(String(100))
    capacity_units = Column(Integer)
    status = Column(String(50))

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(String(50), primary_key=True, index=True)
    warehouse_id = Column(String(50), ForeignKey('warehouses.id'))
    variant_id = Column(String(50), ForeignKey('product_variants.id'))
    available_quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    allocated_quantity = Column(Integer, default=0)
    backorder_quantity = Column(Integer, default=0)
    reorder_level = Column(Integer)
    reorder_quantity = Column(Integer)
    safety_stock = Column(Integer)
    incoming_quantity = Column(Integer, default=0)
    average_daily_demand = Column(Float)
    status = Column(String(50))
    last_restocked_at = Column(DateTime)
    next_expected_restock = Column(DateTime)

    __table_args__ = (
        UniqueConstraint('warehouse_id', 'variant_id', name='uix_warehouse_variant'),
    )

    warehouse = relationship("Warehouse")
    variant = relationship("ProductVariant")

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(String(50), primary_key=True, index=True)
    code = Column(String(50), unique=True)
    company_name = Column(String(255))
    industry = Column(String(100))
    tier = Column(String(50))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    billing_address = Column(Text)
    shipping_address = Column(Text)
    credit_limit = Column(Numeric(18, 2))
    payment_terms_days = Column(Integer)
    account_manager = Column(String(100))
    status = Column(String(50))

class PriceList(Base):
    __tablename__ = 'price_lists'
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100))
    customer_tier = Column(String(50))
    currency = Column(String(10))
    variant_id = Column(String(50), ForeignKey('product_variants.id'))
    unit_price = Column(Numeric(18, 2))
    minimum_quantity = Column(Integer, default=1)
    effective_from = Column(DateTime)
    effective_to = Column(DateTime)
    status = Column(String(50))

    variant = relationship("ProductVariant")

class CustomerPriceList(Base):
    __tablename__ = 'customer_price_lists'
    id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey('customers.id'))
    price_list_id = Column(String(50), ForeignKey('price_lists.id'))
    effective_from = Column(DateTime)
    effective_to = Column(DateTime)
    status = Column(String(50))

class DiscountRule(Base):
    __tablename__ = 'discount_rules'
    id = Column(String(50), primary_key=True, index=True)
    customer_tier = Column(String(50))
    category_id = Column(String(50), ForeignKey('categories.id'))
    max_discount_percent = Column(Numeric(5, 2))
    min_margin_percent = Column(Numeric(5, 2))
    approval_level = Column(String(50))
    risk_level = Column(String(50))
    active = Column(Boolean)

class Quotation(Base):
    __tablename__ = 'quotations'
    id = Column(String(50), primary_key=True, index=True)
    quotation_number = Column(String(100), unique=True)
    customer_id = Column(String(50), ForeignKey('customers.id'))
    quotation_date = Column(DateTime)
    valid_until = Column(DateTime)
    currency = Column(String(10))
    subtotal = Column(Numeric(18, 2))
    discount_total = Column(Numeric(18, 2))
    tax_total = Column(Numeric(18, 2))
    grand_total = Column(Numeric(18, 2))
    status = Column(String(50))
    approval_status = Column(String(50))
    deal_health = Column(String(50))
    created_by = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer")

class QuotationLine(Base):
    __tablename__ = 'quotation_lines'
    id = Column(String(50), primary_key=True, index=True)
    quotation_id = Column(String(50), ForeignKey('quotations.id'))
    line_number = Column(Integer)
    item_type = Column(String(50))
    variant_id = Column(String(50), ForeignKey('product_variants.id'), nullable=True)
    service_id = Column(String(50), nullable=True)
    subscription_plan_id = Column(String(50), nullable=True)
    description = Column(Text)
    quantity = Column(Integer)
    unit_price = Column(Numeric(18, 2))
    discount_percent = Column(Numeric(5, 2))
    discount_amount = Column(Numeric(18, 2))
    tax_rate = Column(Numeric(5, 2))
    tax_amount = Column(Numeric(18, 2))
    line_total = Column(Numeric(18, 2))
    billing_type = Column(String(50))
    fulfillment_warehouse_id = Column(String(50), ForeignKey('warehouses.id'), nullable=True)
    fulfillment_status = Column(String(50))

    quotation = relationship("Quotation")
    variant = relationship("ProductVariant")

class Service(Base):
    __tablename__ = 'services'
    id = Column(String(50), primary_key=True, index=True)
    code = Column(String(50), unique=True)
    name = Column(String(255))
    category = Column(String(100))
    description = Column(Text)
    cost = Column(Numeric(18, 2))
    selling_price = Column(Numeric(18, 2))
    tax_rate = Column(Numeric(5, 2))
    min_margin_percent = Column(Numeric(5, 2))
    recurring = Column(Boolean)
    billing_frequency = Column(String(50))
    status = Column(String(50))

class ProductServiceRule(Base):
    __tablename__ = 'product_service_rules'
    id = Column(String(50), primary_key=True, index=True)
    product_id = Column(String(50), ForeignKey('products.id'))
    service_id = Column(String(50), ForeignKey('services.id'))
    recommended = Column(Boolean)
    required = Column(Boolean)
    priority = Column(Integer)

class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'
    id = Column(String(50), primary_key=True, index=True)
    code = Column(String(50), unique=True)
    name = Column(String(255))
    billing_frequency = Column(String(50))
    billing_interval = Column(Integer)
    price = Column(Numeric(18, 2))
    setup_fee = Column(Numeric(18, 2))
    proration_enabled = Column(Boolean)
    cancellation_policy = Column(Text)
    refund_policy = Column(Text)
    status = Column(String(50))

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey('customers.id'))
    quotation_id = Column(String(50), ForeignKey('quotations.id'))
    plan_id = Column(String(50), ForeignKey('subscription_plans.id'))
    plan_name = Column(String(255))
    annual_rate = Column(Numeric(18, 2))
    billing_cycle = Column(String(50))
    start_date = Column(DateTime)
    next_renewal_date = Column(DateTime)
    status = Column(String(50))

class ProductRecommendation(Base):
    __tablename__ = 'product_recommendations'
    id = Column(String(50), primary_key=True, index=True)
    source_product_id = Column(String(50), ForeignKey('products.id'))
    recommended_product_id = Column(String(50), ForeignKey('products.id'))
    recommendation_type = Column(String(50))
    confidence_score = Column(Float)
    co_purchase_rate = Column(Float)
    margin_delta = Column(Float)
    priority = Column(Integer)
    promotion_active = Column(Boolean)
    min_margin_percent = Column(Numeric(5, 2))
    reason = Column(Text)
    status = Column(String(50))

class DealHealth(Base):
    __tablename__ = 'deal_health'
    id = Column(String(50), primary_key=True, index=True)
    quotation_id = Column(String(50), ForeignKey('quotations.id'))
    days_inactive = Column(Integer)
    discount_anomaly_score = Column(Float)
    delivery_risk_score = Column(Float)
    approval_delay_score = Column(Float)
    inventory_risk_score = Column(Float)
    overall_health_score = Column(Float)
    health_status = Column(String(50))
    recommended_action = Column(Text)
    last_evaluated_at = Column(DateTime)

class Negotiation(Base):
    __tablename__ = 'negotiations'
    id = Column(String(50), primary_key=True, index=True)
    quotation_id = Column(String(50), ForeignKey('quotations.id'))
    customer_id = Column(String(50), ForeignKey('customers.id'))
    quotation_line_id = Column(String(50), ForeignKey('quotation_lines.id'))
    original_discount_percent = Column(Numeric(5, 2))
    requested_discount_percent = Column(Numeric(5, 2))
    customer_message = Column(Text)
    status = Column(String(50))
    submitted_at = Column(DateTime)
    resolved_at = Column(DateTime, nullable=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(String(50), primary_key=True, index=True)
    customer_po_number = Column(String(100))
    quotation_id = Column(String(50), ForeignKey('quotations.id'))
    customer_id = Column(String(50), ForeignKey('customers.id'))
    order_date = Column(DateTime)
    grand_total = Column(Numeric(18, 2))
    currency = Column(String(10))
    status = Column(String(50))
    primary_warehouse_id = Column(String(50), ForeignKey('warehouses.id'))
    promised_delivery_date = Column(DateTime)
    logistics_partner = Column(String(100))

class WarehouseAllocation(Base):
    __tablename__ = 'warehouse_allocations'
    id = Column(String(50), primary_key=True, index=True)
    quotation_id = Column(String(50), ForeignKey('quotations.id'))
    quotation_line_id = Column(String(50), ForeignKey('quotation_lines.id'))
    variant_id = Column(String(50), ForeignKey('product_variants.id'))
    warehouse_id = Column(String(50), ForeignKey('warehouses.id'))
    allocated_quantity = Column(Integer)
    status = Column(String(50))
    allocated_at = Column(DateTime)

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(String(50), primary_key=True, index=True)
    invoice_number = Column(String(100), unique=True)
    quotation_id = Column(String(50), ForeignKey('quotations.id'))
    customer_id = Column(String(50), ForeignKey('customers.id'))
    invoice_date = Column(DateTime)
    due_date = Column(DateTime)
    currency = Column(String(10))
    subtotal = Column(Numeric(18, 2))
    discount_total = Column(Numeric(18, 2))
    tax_total = Column(Numeric(18, 2))
    grand_total = Column(Numeric(18, 2))
    billing_type = Column(String(50))
    status = Column(String(50))

class InvoiceLine(Base):
    __tablename__ = 'invoice_lines'
    id = Column(String(50), primary_key=True, index=True)
    invoice_id = Column(String(50), ForeignKey('invoices.id'))
    item_type = Column(String(50))
    variant_id = Column(String(50), ForeignKey('product_variants.id'), nullable=True)
    service_id = Column(String(50), nullable=True)
    subscription_plan_id = Column(String(50), nullable=True)
    description = Column(Text)
    quantity = Column(Integer)
    unit_price = Column(Numeric(18, 2))
    discount_percent = Column(Numeric(5, 2))
    discount_amount = Column(Numeric(18, 2))
    tax_rate = Column(Numeric(5, 2))
    tax_amount = Column(Numeric(18, 2))
    line_total = Column(Numeric(18, 2))
    billing_type = Column(String(50))

class ApprovalChain(Base):
    __tablename__ = 'approval_chains'
    id = Column(String(50), primary_key=True, index=True)
    approval_level = Column(Integer)
    role_name = Column(String(100))
    min_discount_percent = Column(Numeric(5, 2))
    max_discount_percent = Column(Numeric(5, 2))
    min_margin_percent = Column(Numeric(5, 2))
    approver_role = Column(String(100))
    description = Column(Text)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(String(50), primary_key=True, index=True)
    entity_type = Column(String(50), index=True)
    entity_id = Column(String(50), index=True)
    action = Column(String(50))
    old_value = Column(Text)
    new_value = Column(Text)
    performed_by = Column(String(100))
    reason = Column(Text)
    timestamp = Column(DateTime)
