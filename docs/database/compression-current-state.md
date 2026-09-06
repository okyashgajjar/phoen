# DealFlow360 Database: Current State Architectural Audit

## Executive Summary
This document provides an exhaustive inventory of the existing database schema prior to table compression. 
- **Total Physical Tables**: 25
- **Total Records Across All Tables**: 5,269 rows
- **Total Single-Column Indexes**: 48
- **Average Join Depth for Quote-to-Invoice**: 7–9 tables
- **Storage Profile**: ~1.52 MB unindexed/sparse data in SQLite / ~4.8 MB in PostgreSQL (due to page fragmentation and unoptimized TEXT/VARCHAR(50) primary keys)

---

## Complete Table Inventory

| Table Name | Category | Row Count | Column Count | Foreign Keys | Read / Write Ratio | Primary Purpose & Usage Pattern |
|---|---|---|---|---|---|---|
| `customers` | Master | 100 | 14 | 0 | Very High / Low | Customer accounts, credit limits, tiers, contact information. Frequently queried by sales rep and portal. |
| `brands` | Master | 34 | 6 | 0 | High / Rare | IT Hardware brands (Dell, Apple, HP, Lenovo). Lookup only. Highly redundant as a separate table. |
| `categories` | Master | 20 | 5 | 1 | High / Rare | Hierarchical category taxonomy (Laptops, Desktops, Peripherals, Networking, Servers). |
| `products` | Master | 361 | 19 | 3 | High / Low | Master catalog item definition for physical hardware. Links to brand, category, subcategory. |
| `services` | Master | 41 | 12 | 0 | High / Low | Professional services, warranties, SLA packages. Shares 80% attributes with products. |
| `product_variants` | Master / SKU | 652 | 21 | 1 | Very High / Low | Sellable SKUs with hardware spec columns (CPU, RAM, GPU, storage). High column sparsity. |
| `warehouses` | Master | 5 | 10 | 0 | High / Rare | Fulfillment centers (Ahmedabad, Bangalore, Mumbai, Delhi, Hyderabad). |
| `inventory` | Transactional | 1,063 | 15 | 2 | Very High / High | Current stock balances, reserved stock, safety thresholds per warehouse and SKU. |
| `warehouse_allocations` | Transactional | 392 | 8 | 4 | High / High | Temporary quote-line reservations per warehouse. 1:1 or 1:N with quotation lines. |
| `price_lists` | Master / Config | 4 | 10 | 1 | High / Rare | Tier-based price lists (Tier 1, Tier 2, Tier 3, Retail). |
| `customer_price_lists` | Junction | 100 | 6 | 2 | High / Rare | Assigns a price list to each customer. In practice, 1:1 relationship with customers. |
| `discount_rules` | Config | 28 | 8 | 1 | High / Rare | Max allowable discounts and margin floor thresholds per tier and category. |
| `approval_chains` | Config | 5 | 8 | 0 | Medium / Rare | Multi-tier discount approval threshold configuration (Sales Rep, Manager, Director, VP). |
| `quotations` | Transactional | 180 | 16 | 1 | Very High / High | Sales proposals with totals, statuses, validity dates, deal health scores. |
| `quotation_lines` | Transactional | 455 | 18 | 3 | Very High / High | Line items for quotations (SKU, quantity, unit price, discounts, taxes). |
| `orders` | Transactional | 45 | 11 | 3 | High / Medium | Post-approval confirmed purchase orders. Duplicates quote metadata and customer info. |
| `invoices` | Transactional | 56 | 13 | 2 | High / Medium | Accounts receivable billing documents. Duplicates financial totals and customer info. |
| `invoice_lines` | Transactional | 260 | 15 | 2 | High / Medium | Line items for invoices. 90% identical structure to quotation_lines. |
| `subscription_plans` | Master / Config | 22 | 11 | 0 | High / Rare | Recurring SaaS / Support plan templates (Monthly, Annual, Gold, Platinum). |
| `subscriptions` | Transactional | 26 | 10 | 3 | High / Low | Customer active subscriptions with billing cycles and renewal dates. |
| `deal_health` | Derived / Analytics | 100 | 11 | 1 | High / Medium | Inactivity days, discount anomalies, delivery risks. Computed snapshot. |
| `negotiations` | Transactional | 36 | 10 | 3 | Medium / Medium | Discount counter-offers submitted by customers against specific quotation lines. |
| `product_recommendations` | Derived / Cache | 744 | 12 | 2 | High / Low | Rule-based co-purchase and upsell pairings with confidence scores. |
| `product_service_rules` | Junction / Rule | 375 | 6 | 2 | High / Rare | Pairing physical products with required or recommended warranty services. |
| `audit_logs` | Audit | 165 | 9 | 0 | Low / High (Append) | Event logs recording changes to quotations, approvals, and system state. |

---

## Detailed Table Schema Audit

### 1. Master & Catalog Entities
- **`customers`**: PK `id VARCHAR(50)`. 14 columns. Missing NOT NULL on critical contact attributes. Credit limit stored as `NUMERIC(18,2)`.
- **`brands`**: PK `id VARCHAR(50)`. 6 columns. Low cardinality (34 rows). Only accessed to join brand name and code to products.
- **`categories`**: PK `id VARCHAR(50)`. 5 columns. Self-referencing FK `parent_id`. Clean taxonomy.
- **`products`**: PK `id VARCHAR(50)`. 19 columns. FKs to `brands.id`, `categories.id` (both category and subcategory).
- **`services`**: PK `id VARCHAR(50)`. 12 columns. Duplicates pricing, description, category, and tax logic from products.
- **`product_variants`**: PK `id VARCHAR(50)`. 21 columns. 10 hardcoded hardware spec columns (`cpu`, `ram`, `storage`, `gpu`, `screen_size`, `resolution`, `color`, `connectivity`, `operating_system`, `form_factor`). Completely inflexible for non-laptop hardware categories.

### 2. Transactional & Document Entities
- **`quotations`**, **`orders`**, **`invoices`**:
  - Three distinct tables representing the linear progression of the exact same business transaction:
    1. Negotiation stage: `quotations`
    2. Fulfillment stage: `orders`
    3. Billing stage: `invoices`
  - All three contain identical customer references, currency, subtotal, discount, tax, grand total, notes, and status lifecycle.
  - Invoices lack an explicit `order_id` link, only referencing `quotation_id`.
- **`quotation_lines`** & **`invoice_lines`**:
  - Two parallel line-item tables with identical schema: `item_type`, `variant_id`, `quantity`, `unit_price`, `discount_percent`, `discount_amount`, `tax_rate`, `tax_amount`, `line_total`.
  - Forces application code to maintain duplicate query and insertion logic.

### 3. Inventory & Fulfillment Entities
- **`warehouses`**: 5 rows. Physical fulfillment centers.
- **`inventory`**: 1,063 rows. Composite uniqueness on `(warehouse_id, variant_id)`. Tracks quantities: `available`, `reserved`, `allocated`, `backorder`, `incoming`.
- **`warehouse_allocations`**: 392 rows. Redundant reservation records tracking `quotation_line_id` $\rightarrow$ `variant_id` $\rightarrow$ `warehouse_id`. This information natively belongs on the document line itself.

### 4. Pricing, Discounts & Approvals
- **`price_lists`** (4 rows), **`customer_price_lists`** (100 rows), **`discount_rules`** (28 rows):
  - Fragmented into three separate tables.
  - `customer_price_lists` has exactly 100 rows for 100 customers, acting merely as a 1:1 foreign key assignment rather than a true many-to-many matrix.
  - `approval_chains` (5 rows): Static threshold lookup table storing min/max discount percentages and approver roles.

### 5. Derived & Algorithmic Entities
- **`deal_health`**: 100 rows. Algorithmic scores (`overall_health_score`, `discount_anomaly_score`, `delivery_risk_score`). Stores precomputed analytics that can be computed or held as a JSONB prediction snapshot.
- **`product_recommendations`** (744 rows) & **`product_service_rules`** (375 rows): Static recommendation pairs that consume over 1,100 table rows for simple deterministic rules.

---

## Current Physical Bottlenecks & Critical Issues
1. **Join Explosion**: Rendering a single completed invoice requires joining `invoices` $\rightarrow$ `invoice_lines` $\rightarrow$ `quotations` $\rightarrow$ `quotation_lines` $\rightarrow$ `customers` $\rightarrow$ `product_variants` $\rightarrow$ `products` $\rightarrow$ `brands` $\rightarrow$ `warehouses` (9 tables).
2. **Duplicated Line-Item Logic**: Any update to pricing, taxation, or discounting must be implemented twice (once for quotation lines, once for invoice lines).
3. **Table Proliferation**: 25 physical tables for an application with ~5,000 records adds connection pool overhead, migration burden, cache pollution, and schema management friction.
