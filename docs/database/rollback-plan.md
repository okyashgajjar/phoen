# Database Rollback & Disaster Recovery Plan

## 1. Rollback Philosophy & Objectives
The rollback strategy ensures that in the unlikely event of migration failures, data corruption, query timeouts, or unexpected API incompatibility, the platform can be returned to the exact pre-migration state in **under 3 minutes** with **zero data loss**.

---

## 2. Rollback Triggers
An immediate rollback must be initiated if:
1. Data validation fails during Phase 4 (e.g. any record count mismatch or financial total divergence $> 0.00$).
2. Any critical business workflow (e.g., Quotation Creation, Invoice Generation, Inventory Reservation) fails during Phase 8.
3. Query latency on any critical path exceeds $2\times$ the baseline threshold.
4. Unrecoverable constraint violation occurs during active ETL transformation.

---

## 3. Step-by-Step Rollback Procedures

### Scenario A: Rollback During Migration Execution (Phases 1–6)
Since the original database is preserved in untouched read-only state during migration:
1. **Abort the ETL script**:
   ```bash
   # Terminate running migration process
   kill -9 <migration_pid>
   ```
2. **Drop the newly created compressed tables & views**:
   ```sql
   DROP VIEW IF EXISTS v_deal_health, v_negotiations, v_discount_rules, v_price_lists, 
                        v_warehouse_allocations, v_invoice_lines, v_quotation_lines, 
                        v_invoices, v_orders, v_quotations, v_product_variants, 
                        v_services, v_products, v_brands CASCADE;

   DROP TABLE IF EXISTS audit_logs, subscriptions, document_lines, sales_documents, 
                        pricing_rules, inventory, warehouses, variants, catalog_items, 
                        categories, customers CASCADE;
   ```
3. **Restore pre-migration database snapshot**:
   - SQLite:
     ```bash
     cp dealflow360_pre_migration_backup.db dealflow360.db
     ```
   - PostgreSQL:
     ```bash
     dropdb dealflow360
     createdb dealflow360
     pg_restore -d dealflow360 dealflow360_backup_pre_migration.dump
     ```
4. **Log the failure reason** in `docs/database/final-database-decision-log.md` with stack trace and offending record ID.

### Scenario B: Post-Cutover Rollback (Phases 9–10)
If an issue is detected after the application has been pointed to the compressed database:
1. **Redirect Application Connection String**:
   - Revert `.env` setting `DATABASE_URL` to point to the legacy database instance.
   - Restart FastAPI application service:
     ```bash
     uvicorn backend.main:app --reload
     ```
2. **Reconcile Delta Transactions**:
   - If any new quotations, orders, or invoices were written to `sales_documents` during the live cutover window:
     - Run `scripts/reconcile_delta_transactions.py` to backport new records from `sales_documents` and `document_lines` into `quotations`, `orders`, and `invoices`.
3. **Notify Platform Administrators**:
   - Confirm application status is green on legacy schema.
   - Document root cause and issue resolution plan.

---

## 4. Rollback Verification Checklist
- [ ] Database connectivity verified on original schema.
- [ ] Record count check confirms 5,269 rows present.
- [ ] Quotation creation test succeeds.
- [ ] Invoice lookup test succeeds.
- [ ] Inventory balance test matches original counts.
- [ ] Rollback event logged with timestamp and operator name.
