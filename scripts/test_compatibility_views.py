"""
Validation script to test all 14 compatibility views in the compressed database.
"""

import sqlite3

conn = sqlite3.connect("dealflow360_compressed.db")
cur = conn.cursor()

views_expected = {
    "v_brands": 34, # distinct brands
    "v_products": 361,
    "v_services": 41,
    "v_product_variants": 652,
    "v_quotations": 180,
    "v_orders": 45,
    "v_invoices": 56,
    "v_quotation_lines": 455,
    "v_invoice_lines": 260,
    "v_warehouse_allocations": 392,
    "v_price_lists": 4,
    "v_discount_rules": 28,
    "v_negotiations": 36,
    "v_deal_health": 100
}

print("=================================================================")
print("  TESTING 14 COMPATIBILITY VIEWS")
print("=================================================================")

all_passed = True
for view_name, expected_count in views_expected.items():
    try:
        cur.execute(f"SELECT COUNT(*) FROM {view_name};")
        count = cur.fetchone()[0]
        status = "PASSED" if count == expected_count else "FAILED"
        if count != expected_count:
            all_passed = False
        print(f"  [{status}] {view_name:<26} -> Count: {count:<4} (Expected: {expected_count})")
    except Exception as e:
        all_passed = False
        print(f"  [ERROR] {view_name:<26} -> Error: {e}")

print("=================================================================")
if all_passed:
    print("  ALL 14 COMPATIBILITY VIEWS RETURN 100% EXPECTED COUNTS!")
else:
    print("  SOME VIEWS FAILED VALIDATION.")
print("=================================================================")

conn.close()
