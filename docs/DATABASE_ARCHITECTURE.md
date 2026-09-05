# DealFlow360 Database Architecture

## 1. Overview
The DealFlow360 Enterprise Database is a highly normalized (3NF), centralized PostgreSQL database designed to serve multiple regional locations (Ahmedabad, Bangalore, Mumbai) through a unified schema. It replaces fragmented flat-file data sources with relational integrity and enforces strict constraints, concurrent-safe transactions, and robust data isolation.

## 2. Core Domains & Architecture

### A. Organization & Master Data
- **Brands, Categories, Customers**: Maintained as unified global records.
- **Warehouses**: Distinguish inventory per physical location.

### B. Catalog & Products
- **Products**: Represent the core abstract item.
- **ProductVariants**: Represent the specific sellable/trackable SKUs associated with the product.

### C. Inventory Management
- **Inventory**: Contains quantities (`available`, `reserved`, `allocated`, `backorder`) specific to a `(warehouse_id, variant_id)` pair.
- Inventory movements are handled through strictly transaction-bound SQL updates to prevent overselling.

### D. Pricing & Discount Governance
- **PriceLists**: Support tiered pricing and minimum quantities.
- **DiscountRules**: Automatically evaluate maximum allowable discounts based on `customer_tier` and `category_id`. Require `approval_level` evaluation for excessive discounts.

### E. Quoting, Negotiation, & Ordering
- **Quotations**: Contain snapshot information of the deal. Lines can represent Products, Services, or Subscriptions.
- **Negotiations**: Capture historical back-and-forth counter-offers.
- **Orders & WarehouseAllocations**: Map approved quotations into multi-warehouse fulfillment records.

### F. Hybrid Billing
- **Invoices**: Consolidate one-time charges (hardware) and recurring charges (subscriptions) into unified billing records.

### G. Security & Audit
- **AuditLogs**: Capture immutable records of critical mutations (e.g. discount changes, stock allocation).
- **Customer Isolation**: Managed via Application-layer parameterized queries filtering strictly by `customer_id`.

## 3. Scaling Strategy
- The database is heavily indexed on foreign keys to support large-scale joins.
- Composite unique constraints exist to prevent silent data duplication (e.g. `warehouse_id` + `variant_id` on Inventory).
- Future partitioning can be applied to `audit_logs` and `quotation_lines` by date or region if the table sizes exceed 100M rows.

## 4. Transactional Rules
All operations involving Inventory (reserving stock, allocating stock) and Financials (Invoice creation, Payment allocation) must be wrapped in `BEGIN ... COMMIT` blocks using `SERIALIZABLE` or `READ COMMITTED` isolation to prevent race conditions.
