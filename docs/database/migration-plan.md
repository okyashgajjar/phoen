# Zero-Loss Database Migration Plan: 25 to 11 Tables

## 1. Migration Strategy Principles
1. **Zero Data Loss Guarantee**: Every single row of the 5,269 records currently in the database will be preserved, verified, and mapped.
2. **Deterministic Financial Parity**: Total financial balances (`grand_total`, `tax_total`, `discount_total`) must match with zero variance.
3. **Non-Destructive Shadow Migration**: The compressed schema is built and populated alongside or in a new database/schema before switching application pointers.
4. **Instant Rollback Availability**: The original schema and database snapshot are retained until full validation passes.

---

## 2. Step-by-Step 12-Phase Migration Execution

### Phase 1: Database Pre-Migration Snapshot & Backup
- Generate full binary and SQL dumps:
  - SQLite: `cp dealflow360.db dealflow360_pre_migration_backup.db`
  - PostgreSQL: `pg_dump -Fc -v -f dealflow360_backup_$(date +%Y%m%d_%H%M%S).dump dealflow360`
  - Export all 25 tables to JSON archive in `backup/pre_migration_dump/`.

### Phase 2: DDL Deployment (Compressed Core + Views)
- Execute the DDL for the 11 physical tables in strict dependency order:
  1. `customers`
  2. `categories`
  3. `catalog_items`
  4. `variants`
  5. `warehouses`
  6. `inventory`
  7. `pricing_rules`
  8. `sales_documents`
  9. `document_lines`
  10. `subscriptions`
  11. `audit_logs`
- Deploy the 14 PostgreSQL backward-compatibility views.

### Phase 3: Automated ETL Data Migration
Run the Python migration pipeline (`scripts/migrate_to_compressed_schema.py`):
1. **Migrate Customers**: Copy all 100 rows into `customers`.
2. **Migrate Categories**: Copy all 20 rows into `categories`.
3. **Migrate Catalog Items**:
   - Ingest 361 products with `item_type = 'PRODUCT'`, populating `brand_name` and `brand_code` from `brands`.
   - Ingest 41 services with `item_type = 'SERVICE'`.
   - Ingest 22 subscription plans with `item_type = 'SUBSCRIPTION_PLAN'`.
   - Total rows in `catalog_items`: 424.
4. **Migrate Variants**:
   - Ingest 652 variants into `variants`, packing `cpu`, `ram`, `storage`, `gpu`, `screen_size`, `resolution`, `color`, `connectivity`, `operating_system`, `form_factor` into `attributes JSONB`.
5. **Migrate Warehouses & Inventory**:
   - Copy 5 warehouses into `warehouses`.
   - Copy 1,063 inventory rows into `inventory`.
6. **Migrate Pricing Rules**:
   - Ingest 4 price lists (`rule_type = 'PRICE_LIST'`).
   - Ingest 100 customer price assignments (`rule_type = 'CUSTOMER_OVERRIDE'`).
   - Ingest 28 discount rules (`rule_type = 'DISCOUNT_LIMIT'`).
   - Ingest 5 approval chain tiers.
   - Total rows in `pricing_rules`: 137.
7. **Migrate Sales Documents**:
   - Ingest 180 quotations with `document_type = 'QUOTATION'`, embedding `deal_health` scores from `deal_health`.
   - Ingest 45 orders with `document_type = 'ORDER'` and `parent_document_id = quotation_id`.
   - Ingest 56 invoices with `document_type = 'INVOICE'` and `parent_document_id = quotation_id`.
   - Total rows in `sales_documents`: 281.
8. **Migrate Document Lines**:
   - Ingest 455 quotation lines into `document_lines`, embedding `negotiations` counter-offers and `warehouse_allocations` allocation quantities.
   - Ingest 260 invoice lines into `document_lines`.
   - Total rows in `document_lines`: 715.
9. **Migrate Subscriptions**:
   - Copy 26 subscriptions into `subscriptions`, embedding active plan parameters.
10. **Migrate Audit Logs**:
    - Copy 165 audit logs into `audit_logs`.

### Phase 4: Automated Data Validation Audit
- Run verification script `scripts/verify_compression_migration.py`:
  - Verify record count parity across every entity.
  - Verify `SUM(grand_total)` of quotations: exact match.
  - Verify `SUM(grand_total)` of invoices: exact match.
  - Verify foreign key integrity across all 11 tables.

### Phase 5: Functional Compatibility Verification
- Query all 14 compatibility views to ensure legacy queries return expected results without alteration.

### Phase 6: Performance Benchmarking
- Execute the 16 critical query paths against both schemas and log latency comparisons.

### Phase 7: Backend Code Adaptation
- Update SQLAlchemy ORM models in `database/models.py`.
- Update FastAPI router endpoints to interact with `sales_documents` and `catalog_items`.

### Phase 8: Integration & End-to-End Testing
- Execute pytest test suites covering quote creation, discount approval, order conversion, and invoice generation.

### Phase 9: Application Cutover
- Point application connection string (`DATABASE_URL`) to the compressed database schema.

### Phase 10: Parallel Run & Shadow Window
- Keep the legacy backup accessible for 14 days during production stabilization.

### Phase 11: Final Validation Audit
- Verify zero errors and zero integrity violations during active usage.

### Phase 12: Deprecate & Archive Legacy Tables
- Archive legacy database snapshot into cold storage.
