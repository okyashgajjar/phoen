# Table Consolidation Matrix

## Methodology & Architectural Rules
Every existing physical table in the database was evaluated against the **Compression Hierarchy**:
$$\text{MERGE} \longrightarrow \text{EMBED} \longrightarrow \text{VIEW} \longrightarrow \text{MATERIALIZED VIEW} \longrightarrow \text{JSONB} \longrightarrow \text{TABLE EXTENSION} \longrightarrow \text{NEW TABLE (LAST RESORT)}$$

Each table was evaluated on whether it is an independent business entity, a simple relationship, configuration, derived data, or an artifact of over-normalization.

---

## Complete Table Consolidation Matrix

| # | Existing Table | Current Purpose | Can Merge? | Merge Target | Can Embed? | Can Become View? | Can Become JSONB? | Keep Physical? | Architectural Justification |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `customers` | Master record of B2B client organizations | No | N/A | No | No | Optional metadata | **YES (Retained)** | Core identity entity. Has independent lifecycle, strict foreign key references, and high read frequency. |
| 2 | `categories` | Hierarchical product taxonomy | No | N/A | No | No | No | **YES (Retained)** | Essential recursive tree hierarchy (`parent_id`). High-speed integer/short string indexable taxonomy. |
| 3 | `brands` | Hardware manufacturer metadata | **Yes** | `catalog_items` | **Yes** | **Yes (`v_brands`)** | Yes | **NO (Merged)** | Low-cardinality lookup (34 rows). Storing brand code and name directly in `catalog_items` eliminates an unnecessary join across all catalog queries. |
| 4 | `products` | Physical hardware master catalog | **Yes** | `catalog_items` | No | **Yes (`v_products`)** | Optional attributes | **YES (as `catalog_items`)** | Merged with `services` into unified `catalog_items` table with `item_type = 'PRODUCT'`. |
| 5 | `services` | Professional services & SLAs | **Yes** | `catalog_items` | No | **Yes (`v_services`)** | Service SLA terms | **NO (Merged)** | Services share 85% of their schema with products (name, code, category, base cost, base price, tax rate, status). Differentiated by `item_type = 'SERVICE'`. |
| 6 | `product_variants` | Sellable SKUs with hardware specs | No | N/A | No | **Yes (`v_product_variants`)** | **Yes (hardware specs)** | **YES (as `variants`)** | Sellable SKU configurations must remain a distinct relational table to support barcode lookups, warehouse stock foreign keys, and line item references. Hardware specs move to indexed JSONB. |
| 7 | `warehouses` | Physical storage & fulfillment depots | No | N/A | No | No | Address details | **YES (Retained)** | Core physical entity required for multi-city inventory tracking, dispatch routing, and tax calculations. |
| 8 | `inventory` | Stock balances per SKU per warehouse | **Yes** | `inventory` | No | No | No | **YES (Retained)** | Transactional state entity. Merges allocation totals (`allocated_quantity`, `reserved_quantity`) with stock tracking. |
| 9 | `warehouse_allocations` | Per-quotation warehouse reservation | **Yes** | `document_lines` | **Yes** | **Yes (`v_warehouse_allocations`)** | No | **NO (Merged)** | Line allocations are simply attributes of the quote line being fulfilled (`warehouse_id`, `allocated_quantity`, `fulfillment_status`). Merged into `document_lines`. |
| 10 | `price_lists` | Tiered pricing rules | **Yes** | `pricing_rules` | No | **Yes (`v_price_lists`)** | Tier rules | **NO (Merged)** | Merged into unified `pricing_rules` table with `rule_type = 'PRICE_LIST'`. |
| 11 | `customer_price_lists` | Customer-to-pricelist mapping | **Yes** | `pricing_rules` / `customers` | **Yes** | **Yes (`v_customer_price_lists`)** | Customer pricing config | **NO (Merged)** | Artificial junction table (100 rows for 100 customers). Scoped directly by `customer_id` in `pricing_rules` or embedded in `customers.pricing_config`. |
| 12 | `discount_rules` | Discount ceilings & approval thresholds | **Yes** | `pricing_rules` | No | **Yes (`v_discount_rules`)** | Yes | **NO (Merged)** | Merged into unified `pricing_rules` with `rule_type = 'DISCOUNT_LIMIT'`. |
| 13 | `approval_chains` | Discount approval hierarchy tiers | **Yes** | `pricing_rules` | **Yes** | **Yes (`v_approval_chains`)** | **Yes (`approval_config`)** | **NO (Merged)** | Static config table (5 rows). Stored as structured configuration in `pricing_rules.approval_config` or exposed via a backward-compatible view. |
| 14 | `quotations` | Sales proposal documents | **Yes** | `sales_documents` | No | **Yes (`v_quotations`)** | Health & approval state | **YES (as `sales_documents`)** | Core transactional document header. Unified with `orders` and `invoices` into `sales_documents` typed by `document_type = 'QUOTATION'`. |
| 15 | `orders` | Confirmed customer purchase orders | **Yes** | `sales_documents` | No | **Yes (`v_orders`)** | Logistics info | **NO (Merged)** | 1:1 post-approval continuation of quotation. Represented as `sales_documents` with `document_type = 'ORDER'` and `parent_document_id = quote_id`. |
| 16 | `invoices` | Accounts receivable financial records | **Yes** | `sales_documents` | No | **Yes (`v_invoices`)** | Payment notes | **NO (Merged)** | Downstream financial document. Represented as `sales_documents` with `document_type = 'INVOICE'` and `parent_document_id = order_id`. |
| 17 | `quotation_lines` | Line items for quotation | **Yes** | `document_lines` | No | **Yes (`v_quotation_lines`)** | Negotiation details | **YES (as `document_lines`)** | Unified line table serving quotes, orders, and invoices. Eliminates schema duplication. |
| 18 | `invoice_lines` | Line items for invoices | **Yes** | `document_lines` | No | **Yes (`v_invoice_lines`)** | Billing notes | **NO (Merged)** | Structurally identical to quotation lines. Consolidated into `document_lines`. |
| 19 | `subscription_plans` | SaaS/Warranty plan templates | **Yes** | `catalog_items` / `subscriptions` | **Yes** | **Yes (`v_subscription_plans`)** | **Yes (`plan_config`)** | **NO (Merged)** | Plan templates are stored as catalog items (`item_type = 'SUBSCRIPTION_PLAN'`), and terms are embedded in `subscriptions.plan_config`. |
| 20 | `subscriptions` | Active customer subscriptions | No | N/A | No | No | Embedded plan terms | **YES (Retained)** | Core recurring revenue tracking entity. Links customer, document, and renewal dates. |
| 21 | `deal_health` | Machine learning deal risk snapshot | **Yes** | `sales_documents` | **Yes** | **Yes (`v_deal_health`)** | **Yes (`deal_health` JSONB)** | **NO (Converted to View/JSONB)** | Derived algorithmic score. Stored as JSONB snapshot in `sales_documents.deal_health` and exposed via view `v_deal_health`. |
| 22 | `negotiations` | Customer discount counter-proposals | **Yes** | `document_lines` | **Yes** | **Yes (`v_negotiations`)** | **Yes (`negotiation_data` JSONB)** | **NO (Merged)** | Counter-offers are line-item modifications. Embedded directly in `document_lines.negotiation_data` JSONB. |
| 23 | `product_recommendations` | Cross-sell and upsell pairs | **Yes** | `catalog_items` | **Yes** | **Yes (`v_product_recommendations`)** | **Yes (`recommendations` JSONB)** | **NO (Converted to View/JSONB)** | Dynamic algorithmic pairs. Evaluated on-demand via PostgreSQL view `v_product_recommendations` or cached in `catalog_items.metadata`. |
| 24 | `product_service_rules` | Mandatory/recommended service links | **Yes** | `catalog_items` | **Yes** | **Yes (`v_product_service_rules`)** | **Yes (`service_rules` JSONB)** | **NO (Merged into JSONB)** | Static association rules stored in `catalog_items.metadata->'service_rules'`. |
| 25 | `audit_logs` | System-wide audit event ledger | No | N/A | No | No | Old/New state snapshots | **YES (Retained)** | Unified append-only compliance audit trail. |

---

## Consolidation Summary

- **Total Existing Physical Tables**: 25
- **Physical Tables Retained / Redesigned**: **11**
  1. `customers`
  2. `categories`
  3. `catalog_items` (replaces `products`, `services`, `subscription_plans`, `brands`)
  4. `variants` (replaces `product_variants` with JSONB attributes)
  5. `warehouses`
  6. `inventory` (replaces `inventory` and absorbs allocation metrics)
  7. `pricing_rules` (replaces `price_lists`, `customer_price_lists`, `discount_rules`, `approval_chains`)
  8. `sales_documents` (replaces `quotations`, `orders`, `invoices`)
  9. `document_lines` (replaces `quotation_lines`, `invoice_lines`, `warehouse_allocations`, `negotiations`)
  10. `subscriptions` (absorbs `subscription_plans` config)
  11. `audit_logs`
- **Physical Tables Eliminated**: **14** (56% reduction)
- **New Physical Tables Created**: **0** (Strict compliance with Table Minimization Rule)
- **Compatibility SQL Views**: **14** (100% backward query compatibility)
