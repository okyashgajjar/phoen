# Target Compressed Architecture: 11 Core Physical Tables

## 1. Architectural Philosophy
The compressed data model strikes a balance between **relational rigor** (strict foreign keys, composite unique constraints, explicit financial precision) and **PostgreSQL JSONB capability** (for extensible specifications, audit snapshots, and dynamic rules).

---

## 2. Complete Physical DDL Definitions

### Table 1: `customers`
```sql
CREATE TABLE customers (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    tier VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    billing_address TEXT,
    shipping_address TEXT,
    credit_limit NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    payment_terms_days INTEGER DEFAULT 30 NOT NULL,
    account_manager VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ
);
CREATE INDEX ix_customers_tier ON customers(tier);
CREATE INDEX ix_customers_status ON customers(status);
```

### Table 2: `categories`
```sql
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50) REFERENCES categories(id) ON DELETE SET NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX ix_categories_parent_id ON categories(parent_id);
```

### Table 3: `catalog_items`
```sql
CREATE TABLE catalog_items (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    item_type VARCHAR(50) NOT NULL CHECK (item_type IN ('PRODUCT', 'SERVICE', 'SUBSCRIPTION_PLAN')),
    category_id VARCHAR(50) REFERENCES categories(id) ON DELETE RESTRICT,
    subcategory_id VARCHAR(50) REFERENCES categories(id) ON DELETE SET NULL,
    brand_name VARCHAR(100),
    brand_code VARCHAR(50),
    manufacturer_part_number VARCHAR(100),
    unit VARCHAR(20) DEFAULT 'unit' NOT NULL,
    base_cost NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    base_price NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    tax_rate NUMERIC(5, 2) DEFAULT 18.00 NOT NULL,
    warranty_months INTEGER DEFAULT 0 NOT NULL,
    is_recurring BOOLEAN DEFAULT FALSE NOT NULL,
    billing_frequency VARCHAR(50),
    status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ
);
CREATE INDEX ix_catalog_items_type ON catalog_items(item_type);
CREATE INDEX ix_catalog_items_category ON catalog_items(category_id);
CREATE INDEX ix_catalog_items_brand ON catalog_items(brand_name);
CREATE INDEX ix_catalog_items_meta_gin ON catalog_items USING GIN(metadata);
```

### Table 4: `variants`
```sql
CREATE TABLE variants (
    id VARCHAR(50) PRIMARY KEY,
    catalog_item_id VARCHAR(50) NOT NULL REFERENCES catalog_items(id) ON DELETE CASCADE,
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    extra_price NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    cost_price NUMERIC(18, 2) NOT NULL,
    selling_price NUMERIC(18, 2) NOT NULL,
    barcode VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL,
    attributes JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ
);
CREATE INDEX ix_variants_catalog_item ON variants(catalog_item_id);
CREATE INDEX ix_variants_sku ON variants(sku);
CREATE INDEX ix_variants_attr_gin ON variants USING GIN(attributes);
```

### Table 5: `warehouses`
```sql
CREATE TABLE warehouses (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    warehouse_type VARCHAR(50) DEFAULT 'REGIONAL',
    manager_name VARCHAR(100),
    capacity_units INTEGER DEFAULT 10000,
    status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL
);
CREATE INDEX ix_warehouses_city ON warehouses(city);
```

### Table 6: `inventory`
```sql
CREATE TABLE inventory (
    id VARCHAR(50) PRIMARY KEY,
    warehouse_id VARCHAR(50) NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
    variant_id VARCHAR(50) NOT NULL REFERENCES variants(id) ON DELETE CASCADE,
    available_quantity INTEGER DEFAULT 0 NOT NULL,
    reserved_quantity INTEGER DEFAULT 0 NOT NULL,
    allocated_quantity INTEGER DEFAULT 0 NOT NULL,
    backorder_quantity INTEGER DEFAULT 0 NOT NULL,
    reorder_level INTEGER DEFAULT 10 NOT NULL,
    reorder_quantity INTEGER DEFAULT 50 NOT NULL,
    safety_stock INTEGER DEFAULT 5 NOT NULL,
    incoming_quantity INTEGER DEFAULT 0 NOT NULL,
    average_daily_demand FLOAT DEFAULT 0.0 NOT NULL,
    status VARCHAR(50) DEFAULT 'IN_STOCK' NOT NULL,
    last_restocked_at TIMESTAMPTZ,
    next_expected_restock TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    CONSTRAINT uix_warehouse_variant UNIQUE (warehouse_id, variant_id)
);
CREATE INDEX ix_inventory_lookup ON inventory(warehouse_id, variant_id);
CREATE INDEX ix_inventory_status ON inventory(status);
```

### Table 7: `pricing_rules`
```sql
CREATE TABLE pricing_rules (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rule_type VARCHAR(50) NOT NULL CHECK (rule_type IN ('PRICE_LIST', 'CUSTOMER_OVERRIDE', 'DISCOUNT_LIMIT', 'MARGIN_FLOOR')),
    scope_type VARCHAR(50) NOT NULL CHECK (scope_type IN ('GLOBAL', 'TIER', 'CUSTOMER', 'CATEGORY', 'ITEM', 'VARIANT')),
    scope_id VARCHAR(50),
    customer_id VARCHAR(50) REFERENCES customers(id) ON DELETE CASCADE,
    variant_id VARCHAR(50) REFERENCES variants(id) ON DELETE CASCADE,
    category_id VARCHAR(50) REFERENCES categories(id) ON DELETE CASCADE,
    customer_tier VARCHAR(50),
    unit_price NUMERIC(18, 2),
    discount_percent NUMERIC(5, 2),
    max_discount_percent NUMERIC(5, 2),
    min_margin_percent NUMERIC(5, 2),
    minimum_quantity INTEGER DEFAULT 1 NOT NULL,
    approval_level VARCHAR(50),
    currency VARCHAR(10) DEFAULT 'INR' NOT NULL,
    effective_from TIMESTAMPTZ,
    effective_to TIMESTAMPTZ,
    active BOOLEAN DEFAULT TRUE NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL
);
CREATE INDEX ix_pricing_scope ON pricing_rules(scope_type, scope_id, active);
CREATE INDEX ix_pricing_variant_tier ON pricing_rules(variant_id, customer_tier);
```

### Table 8: `sales_documents`
```sql
CREATE TABLE sales_documents (
    id VARCHAR(50) PRIMARY KEY,
    document_number VARCHAR(100) UNIQUE NOT NULL,
    document_type VARCHAR(50) NOT NULL CHECK (document_type IN ('QUOTATION', 'ORDER', 'INVOICE')),
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    parent_document_id VARCHAR(50) REFERENCES sales_documents(id) ON DELETE SET NULL,
    document_date TIMESTAMPTZ NOT NULL,
    valid_until TIMESTAMPTZ,
    due_date TIMESTAMPTZ,
    currency VARCHAR(10) DEFAULT 'INR' NOT NULL,
    subtotal NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    discount_total NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    tax_total NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    grand_total NUMERIC(18, 2) DEFAULT 0 NOT NULL,
    status VARCHAR(50) NOT NULL,
    approval_status VARCHAR(50),
    deal_health JSONB DEFAULT '{}'::jsonb NOT NULL,
    primary_warehouse_id VARCHAR(50) REFERENCES warehouses(id) ON DELETE SET NULL,
    created_by VARCHAR(100),
    notes TEXT,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ
);
CREATE INDEX ix_sales_documents_type_status ON sales_documents(document_type, status);
CREATE INDEX ix_sales_documents_customer ON sales_documents(customer_id, document_type);
CREATE INDEX ix_sales_documents_parent ON sales_documents(parent_document_id);
```

### Table 9: `document_lines`
```sql
CREATE TABLE document_lines (
    id VARCHAR(50) PRIMARY KEY,
    document_id VARCHAR(50) NOT NULL REFERENCES sales_documents(id) ON DELETE CASCADE,
    line_number INTEGER NOT NULL,
    item_type VARCHAR(50) NOT NULL CHECK (item_type IN ('VARIANT', 'SERVICE', 'SUBSCRIPTION_PLAN')),
    variant_id VARCHAR(50) REFERENCES variants(id) ON DELETE SET NULL,
    catalog_item_id VARCHAR(50) REFERENCES catalog_items(id) ON DELETE SET NULL,
    description TEXT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(18, 2) NOT NULL,
    discount_percent NUMERIC(5, 2) DEFAULT 0.00 NOT NULL,
    discount_amount NUMERIC(18, 2) DEFAULT 0.00 NOT NULL,
    tax_rate NUMERIC(5, 2) DEFAULT 18.00 NOT NULL,
    tax_amount NUMERIC(18, 2) DEFAULT 0.00 NOT NULL,
    line_total NUMERIC(18, 2) NOT NULL,
    billing_type VARCHAR(50),
    warehouse_id VARCHAR(50) REFERENCES warehouses(id) ON DELETE SET NULL,
    fulfillment_status VARCHAR(50) DEFAULT 'PENDING' NOT NULL,
    allocated_quantity INTEGER DEFAULT 0 NOT NULL,
    negotiation_data JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX ix_document_lines_doc ON document_lines(document_id, line_number);
CREATE INDEX ix_document_lines_variant ON document_lines(variant_id);
CREATE INDEX ix_document_lines_warehouse ON document_lines(warehouse_id);
```

### Table 10: `subscriptions`
```sql
CREATE TABLE subscriptions (
    id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    document_id VARCHAR(50) REFERENCES sales_documents(id) ON DELETE SET NULL,
    plan_id VARCHAR(50) REFERENCES catalog_items(id) ON DELETE SET NULL,
    plan_code VARCHAR(50),
    plan_name VARCHAR(255) NOT NULL,
    annual_rate NUMERIC(18, 2) NOT NULL,
    billing_cycle VARCHAR(50) NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    next_renewal_date TIMESTAMPTZ NOT NULL,
    status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL,
    plan_config JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ
);
CREATE INDEX ix_subscriptions_customer ON subscriptions(customer_id, status);
CREATE INDEX ix_subscriptions_renewal ON subscriptions(next_renewal_date);
```

### Table 11: `audit_logs`
```sql
CREATE TABLE audit_logs (
    id VARCHAR(50) PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    performed_by VARCHAR(100),
    reason TEXT,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX ix_audit_logs_lookup ON audit_logs(entity_type, entity_id, timestamp);
```

---

## 3. Backward Compatibility SQL Views
```sql
-- 1. Brands View
CREATE VIEW v_brands AS
SELECT DISTINCT 
    brand_code AS id, 
    brand_name AS name, 
    brand_code AS code,
    'ACTIVE' AS status
FROM catalog_items 
WHERE brand_name IS NOT NULL;

-- 2. Products View
CREATE VIEW v_products AS
SELECT * FROM catalog_items WHERE item_type = 'PRODUCT';

-- 3. Services View
CREATE VIEW v_services AS
SELECT * FROM catalog_items WHERE item_type = 'SERVICE';

-- 4. Product Variants View
CREATE VIEW v_product_variants AS
SELECT 
    v.id,
    v.catalog_item_id AS product_id,
    v.sku,
    v.name,
    v.attributes->>'cpu' AS cpu,
    v.attributes->>'ram' AS ram,
    v.attributes->>'storage' AS storage,
    v.attributes->>'gpu' AS gpu,
    v.attributes->>'screen_size' AS screen_size,
    v.cost_price,
    v.selling_price,
    v.extra_price,
    v.barcode,
    v.status,
    c.name AS product_name,
    c.code AS product_code
FROM variants v
JOIN catalog_items c ON v.catalog_item_id = c.id;

-- 5. Quotations View
CREATE VIEW v_quotations AS
SELECT * FROM sales_documents WHERE document_type = 'QUOTATION';

-- 6. Orders View
CREATE VIEW v_orders AS
SELECT * FROM sales_documents WHERE document_type = 'ORDER';

-- 7. Invoices View
CREATE VIEW v_invoices AS
SELECT * FROM sales_documents WHERE document_type = 'INVOICE';

-- 8. Quotation Lines View
CREATE VIEW v_quotation_lines AS
SELECT 
    dl.*, 
    dl.document_id AS quotation_id,
    d.document_number AS quotation_number
FROM document_lines dl
JOIN sales_documents d ON dl.document_id = d.id
WHERE d.document_type = 'QUOTATION';

-- 9. Invoice Lines View
CREATE VIEW v_invoice_lines AS
SELECT 
    dl.*, 
    dl.document_id AS invoice_id,
    d.document_number AS invoice_number
FROM document_lines dl
JOIN sales_documents d ON dl.document_id = d.id
WHERE d.document_type = 'INVOICE';

-- 10. Warehouse Allocations View
CREATE VIEW v_warehouse_allocations AS
SELECT 
    id,
    document_id AS quotation_id,
    id AS quotation_line_id,
    variant_id,
    warehouse_id,
    allocated_quantity,
    fulfillment_status AS status,
    created_at AS allocated_at
FROM document_lines 
WHERE allocated_quantity > 0;

-- 11. Price Lists View
CREATE VIEW v_price_lists AS
SELECT * FROM pricing_rules WHERE rule_type = 'PRICE_LIST';

-- 12. Discount Rules View
CREATE VIEW v_discount_rules AS
SELECT * FROM pricing_rules WHERE rule_type = 'DISCOUNT_LIMIT';

-- 13. Negotiations View
CREATE VIEW v_negotiations AS
SELECT 
    id,
    document_id AS quotation_id,
    id AS quotation_line_id,
    (negotiation_data->>'requested_discount')::NUMERIC(5,2) AS requested_discount_percent,
    (negotiation_data->>'customer_message') AS customer_message,
    (negotiation_data->>'status') AS status,
    created_at AS submitted_at
FROM document_lines 
WHERE negotiation_data != '{}'::jsonb;

-- 14. Deal Health View
CREATE VIEW v_deal_health AS
SELECT 
    id AS quotation_id,
    (deal_health->>'overall_score')::FLOAT AS overall_health_score,
    (deal_health->>'status') AS health_status,
    (deal_health->>'recommended_action') AS recommended_action,
    updated_at AS last_evaluated_at
FROM sales_documents 
WHERE document_type = 'QUOTATION';
```
