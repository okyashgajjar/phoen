"""
DealFlow360 Enterprise Data Validation Script — Mumbai Edition
Validates all CSV seed files for relational integrity, pricing consistency,
inventory validity, date formats, SKU uniqueness, margins, and business logic.
Prints comprehensive validation banner and data quality score.
"""

import os
import csv
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SEED_DIR = os.path.dirname(os.path.abspath(__file__))

def load_csv(filename):
    filepath = os.path.join(SEED_DIR, filename)
    if not os.path.exists(filepath):
        return [], []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return [], []
        rows = [row for row in reader if row]
    return headers, rows

def validate():
    fk_errors = 0
    duplicate_ids = 0
    duplicate_skus = 0
    invalid_prices = 0
    invalid_inventory = 0
    invalid_dates = 0
    invalid_discounts = 0
    invalid_taxes = 0
    invalid_tiers = 0
    invalid_categories = 0
    invalid_margins = 0

    error_log = []

    # 1. Brands
    b_head, b_rows = load_csv("brands.csv")
    brand_ids = set()
    for r in b_rows:
        bid = r[0]
        if bid in brand_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate brand_id: {bid}")
        brand_ids.add(bid)

    # 2. Categories
    c_head, c_rows = load_csv("categories.csv")
    cat_ids = set()
    parent_ids_to_check = []
    for r in c_rows:
        cid = r[0]
        if cid in cat_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate category_id: {cid}")
        cat_ids.add(cid)
        if r[2]: # parent_category_id
            parent_ids_to_check.append((cid, r[2]))

    for cid, pid in parent_ids_to_check:
        if pid not in cat_ids:
            fk_errors += 1
            invalid_categories += 1
            error_log.append(f"Broken parent_category_id: {pid} in category {cid}")

    # 3. Warehouses
    w_head, w_rows = load_csv("warehouses.csv")
    wh_ids = set()
    for r in w_rows:
        wid = r[0]
        if wid in wh_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate warehouse_id: {wid}")
        wh_ids.add(wid)

    # 4. Products
    p_head, p_rows = load_csv("products.csv")
    product_ids = set()
    for r in p_rows:
        pid = r[0]
        if pid in product_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate product_id: {pid}")
        product_ids.add(pid)

        cid = r[4]
        subcid = r[5]
        if cid not in cat_ids:
            fk_errors += 1
            invalid_categories += 1
            error_log.append(f"Invalid category_id {cid} in product {pid}")
        if subcid not in cat_ids:
            fk_errors += 1
            invalid_categories += 1
            error_log.append(f"Invalid subcategory_id {subcid} in product {pid}")

        try:
            cost = float(r[10])
            price = float(r[11])
            tax = float(r[12])
            if cost < 0 or price < 0:
                invalid_prices += 1
                error_log.append(f"Negative price/cost in product {pid}")
            if cost > price:
                invalid_margins += 1
                error_log.append(f"Cost ({cost}) > Price ({price}) in product {pid}")
            if tax < 0 or tax > 100:
                invalid_taxes += 1
                error_log.append(f"Invalid tax rate {tax} in product {pid}")
        except ValueError as e:
            invalid_prices += 1
            error_log.append(f"Non-numeric price/cost in product {pid}: {e}")

    # 5. Product Variants
    pv_head, pv_rows = load_csv("product_variants.csv")
    variant_ids = set()
    var_costs = {}
    var_prices = {}
    skus = set()
    for r in pv_rows:
        vid = r[0]
        pid = r[1]
        sku = r[2]

        if vid in variant_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate variant_id: {vid}")
        variant_ids.add(vid)

        if sku in skus:
            duplicate_skus += 1
            error_log.append(f"Duplicate SKU: {sku}")
        skus.add(sku)

        if pid not in product_ids:
            fk_errors += 1
            error_log.append(f"Broken product_id {pid} in variant {vid}")

        try:
            extra = float(r[16])
            cost = float(r[17])
            price = float(r[18])
            var_costs[vid] = cost
            var_prices[vid] = price

            if cost < 0 or price < 0 or extra < 0:
                invalid_prices += 1
                error_log.append(f"Negative price/cost in variant {vid}")
            if cost > price:
                invalid_margins += 1
                error_log.append(f"Cost ({cost}) > Price ({price}) in variant {vid}")
        except ValueError as e:
            invalid_prices += 1
            error_log.append(f"Non-numeric price in variant {vid}: {e}")

    # 6. Services
    srv_head, srv_rows = load_csv("services.csv")
    service_ids = set()
    for r in srv_rows:
        sid = r[0]
        if sid in service_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate service_id: {sid}")
        service_ids.add(sid)
        try:
            cost = float(r[5])
            price = float(r[6])
            tax = float(r[7])
            if cost < 0 or price < 0:
                invalid_prices += 1
            if cost > price:
                invalid_margins += 1
            if tax < 0 or tax > 100:
                invalid_taxes += 1
        except ValueError:
            invalid_prices += 1

    # 7. Subscription Plans
    sub_head, sub_rows = load_csv("subscription_plans.csv")
    subscription_ids = set()
    for r in sub_rows:
        sid = r[0]
        if sid in subscription_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate plan_id: {sid}")
        subscription_ids.add(sid)
        try:
            price = float(r[5])
            if price < 0:
                invalid_prices += 1
        except ValueError:
            invalid_prices += 1

    # 8. Discount Rules
    dr_head, dr_rows = load_csv("discount_rules.csv")
    valid_tiers = {"Standard", "SMB", "Enterprise", "Strategic"}
    discount_rule_ids = set()
    for r in dr_rows:
        drid = r[0]
        tier = r[1]
        cid = r[2]
        if drid in discount_rule_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate discount_rule_id: {drid}")
        discount_rule_ids.add(drid)

        if tier not in valid_tiers:
            invalid_tiers += 1
            error_log.append(f"Invalid tier {tier} in discount rule {drid}")
        if cid not in cat_ids:
            invalid_categories += 1
            fk_errors += 1
            error_log.append(f"Invalid category {cid} in discount rule {drid}")

        try:
            max_disc = float(r[3])
            min_margin = float(r[4])
            if max_disc < 0 or max_disc > 100 or min_margin < 0 or min_margin > 100:
                invalid_discounts += 1
                error_log.append(f"Invalid discount/margin % in rule {drid}")
        except ValueError:
            invalid_discounts += 1

    # 9. Customers
    cust_head, cust_rows = load_csv("customers.csv")
    customer_ids = set()
    for r in cust_rows:
        cid = r[0]
        tier = r[4]
        if cid in customer_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate customer_id: {cid}")
        customer_ids.add(cid)

        if tier not in valid_tiers:
            invalid_tiers += 1
            error_log.append(f"Invalid customer tier {tier} in customer {cid}")

        try:
            credit = float(r[10])
            terms = int(r[11])
            if credit < 0 or terms < 0:
                error_log.append(f"Negative credit limit/terms in customer {cid}")
        except ValueError:
            error_log.append(f"Invalid numeric values in customer {cid}")

    # 10. Customer Price Lists
    cpl_head, cpl_rows = load_csv("customer_price_lists.csv")
    cpl_ids = set()
    for r in cpl_rows:
        cpl_id = r[0]
        cid = r[1]
        if cpl_id in cpl_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate customer_price_id: {cpl_id}")
        cpl_ids.add(cpl_id)

        if cid not in customer_ids:
            fk_errors += 1
            error_log.append(f"Broken customer_id {cid} in customer_price_lists {cpl_id}")

    # 11. Inventory
    inv_head, inv_rows = load_csv("inventory.csv")
    inventory_ids = set()
    for r in inv_rows:
        iid = r[0]
        wid = r[1]
        vid = r[2]
        if iid in inventory_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate inventory_id: {iid}")
        inventory_ids.add(iid)

        if wid not in wh_ids:
            fk_errors += 1
            error_log.append(f"Broken warehouse_id {wid} in inventory {iid}")
        if vid not in variant_ids:
            fk_errors += 1
            error_log.append(f"Broken variant_id {vid} in inventory {iid}")

        try:
            avail = int(r[3])
            res = int(r[4])
            alloc = int(r[5])
            backorder = int(r[6])
            if avail < 0 or res < 0 or alloc < 0 or backorder < 0:
                invalid_inventory += 1
                error_log.append(f"Negative quantity in inventory {iid}")
        except ValueError:
            invalid_inventory += 1
            error_log.append(f"Non-integer inventory count in {iid}")

    # 12. Price Lists
    pl_head, pl_rows = load_csv("price_lists.csv")
    for r in pl_rows:
        tier = r[2]
        vid = r[4]
        if tier not in valid_tiers:
            invalid_tiers += 1
            error_log.append(f"Invalid tier {tier} in price_lists")
        if vid not in variant_ids:
            fk_errors += 1
            error_log.append(f"Broken variant_id {vid} in price_lists")
        try:
            uprice = float(r[5])
            if uprice < 0:
                invalid_prices += 1
            cost = var_costs.get(vid, 0.0)
            if uprice < cost:
                invalid_margins += 1
                error_log.append(f"Price list unit price {uprice} below cost {cost} for variant {vid}")
        except ValueError:
            invalid_prices += 1

    # 13. Recommendations
    rec_head, rec_rows = load_csv("product_recommendations.csv")
    rec_ids = set()
    for r in rec_rows:
        rid = r[0]
        spid = r[1]
        rpid = r[2]
        if rid in rec_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate recommendation_id: {rid}")
        rec_ids.add(rid)

        if spid not in product_ids:
            fk_errors += 1
            error_log.append(f"Broken source_product_id {spid} in recommendation {rid}")
        if rpid not in product_ids:
            fk_errors += 1
            error_log.append(f"Broken recommended_product_id {rpid} in recommendation {rid}")

    # 14. Product Service Rules
    psr_head, psr_rows = load_csv("product_service_rules.csv")
    psr_ids = set()
    for r in psr_rows:
        rule_id = r[0]
        pid = r[1]
        sid = r[2]
        if rule_id in psr_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate rule_id: {rule_id}")
        psr_ids.add(rule_id)

        if pid not in product_ids:
            fk_errors += 1
            error_log.append(f"Broken product_id {pid} in product_service_rules {rule_id}")
        if sid not in service_ids:
            fk_errors += 1
            error_log.append(f"Broken service_id {sid} in product_service_rules {rule_id}")

    # 15. Quotations
    q_head, q_rows = load_csv("quotations.csv")
    quotation_ids = set()
    for r in q_rows:
        qid = r[0]
        cid = r[2]
        if qid in quotation_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate quotation_id: {qid}")
        quotation_ids.add(qid)

        if cid not in customer_ids:
            fk_errors += 1
            error_log.append(f"Broken customer_id {cid} in quotation {qid}")

        try:
            datetime.strptime(r[3], "%Y-%m-%d")
            datetime.strptime(r[4], "%Y-%m-%d")
        except ValueError:
            invalid_dates += 1
            error_log.append(f"Invalid date format in quotation {qid}")

        try:
            sub = float(r[6])
            disc = float(r[7])
            tax = float(r[8])
            grand = float(r[9])
            if sub < 0 or disc < 0 or tax < 0 or grand < 0:
                invalid_prices += 1
                error_log.append(f"Negative amount in quotation {qid}")
        except ValueError:
            invalid_prices += 1

    # 16. Quotation Lines
    ql_head, ql_rows = load_csv("quotation_lines.csv")
    ql_ids = set()
    for r in ql_rows:
        ql_id = r[0]
        qid = r[1]
        itype = r[3]
        vid = r[4]
        sid = r[5]
        subid = r[6]
        wh_id = r[16]

        if ql_id in ql_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate line_id: {ql_id}")
        ql_ids.add(ql_id)

        if qid not in quotation_ids:
            fk_errors += 1
            error_log.append(f"Broken quotation_id {qid} in line {ql_id}")

        if itype == "PRODUCT":
            if vid not in variant_ids:
                fk_errors += 1
                error_log.append(f"Broken variant_id {vid} in line {ql_id}")
            if wh_id and wh_id not in wh_ids:
                fk_errors += 1
                error_log.append(f"Broken warehouse_id {wh_id} in line {ql_id}")
        elif itype == "SERVICE":
            if sid not in service_ids:
                fk_errors += 1
                error_log.append(f"Broken service_id {sid} in line {ql_id}")
        elif itype == "SUBSCRIPTION":
            if subid not in subscription_ids:
                fk_errors += 1
                error_log.append(f"Broken subscription_plan_id {subid} in line {ql_id}")

        try:
            qty = float(r[8])
            price = float(r[9])
            disc_pct = float(r[10])
            disc_amt = float(r[11])
            tax_rate = float(r[12])
            tax_amt = float(r[13])
            line_tot = float(r[14])
            if qty <= 0 or price < 0 or disc_pct < 0 or line_tot < 0:
                invalid_prices += 1
                error_log.append(f"Invalid quantity/price in line {ql_id}")
        except ValueError:
            invalid_prices += 1

    # 17. Negotiations
    neg_head, neg_rows = load_csv("negotiations.csv")
    neg_ids = set()
    for r in neg_rows:
        nid = r[0]
        qid = r[1]
        cid = r[2]
        qlid = r[3]
        if nid in neg_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate negotiation_id: {nid}")
        neg_ids.add(nid)

        if qid not in quotation_ids:
            fk_errors += 1
            error_log.append(f"Broken quotation_id {qid} in negotiation {nid}")
        if cid not in customer_ids:
            fk_errors += 1
            error_log.append(f"Broken customer_id {cid} in negotiation {nid}")
        if qlid not in ql_ids:
            fk_errors += 1
            error_log.append(f"Broken quotation_line_id {qlid} in negotiation {nid}")

    # 18. Deal Health
    dh_head, dh_rows = load_csv("deal_health.csv")
    dh_ids = set()
    for r in dh_rows:
        dhid = r[0]
        qid = r[1]
        if dhid in dh_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate deal_health_id: {dhid}")
        dh_ids.add(dhid)

        if qid not in quotation_ids:
            fk_errors += 1
            error_log.append(f"Broken quotation_id {qid} in deal_health {dhid}")

    # 19. Audit Logs
    aud_head, aud_rows = load_csv("audit_logs.csv")
    aud_ids = set()
    for r in aud_rows:
        aid = r[0]
        if aid in aud_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate audit_id: {aid}")
        aud_ids.add(aid)

    # 20. Invoices
    invc_head, invc_rows = load_csv("invoices.csv")
    invc_ids = set()
    invc_nums = set()
    for r in invc_rows:
        invid = r[0]
        invnum = r[1]
        qid = r[2]
        cid = r[3]
        if invid in invc_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate invoice_id: {invid}")
        invc_ids.add(invid)

        if invnum in invc_nums:
            duplicate_ids += 1
            error_log.append(f"Duplicate invoice_number: {invnum}")
        invc_nums.add(invnum)

        if qid not in quotation_ids:
            fk_errors += 1
            error_log.append(f"Broken quotation_id {qid} in invoice {invid}")
        if cid not in customer_ids:
            fk_errors += 1
            error_log.append(f"Broken customer_id {cid} in invoice {invid}")

    # 21. Invoice Lines
    invcl_head, invcl_rows = load_csv("invoice_lines.csv")
    invcl_ids = set()
    for r in invcl_rows:
        lid = r[0]
        invid = r[1]
        if lid in invcl_ids:
            duplicate_ids += 1
            error_log.append(f"Duplicate invoice_line_id: {lid}")
        invcl_ids.add(lid)

        if invid not in invc_ids:
            fk_errors += 1
            error_log.append(f"Broken invoice_id {invid} in invoice_line {lid}")

    total_issues = (
        fk_errors + duplicate_ids + duplicate_skus + invalid_prices +
        invalid_inventory + invalid_dates + invalid_discounts +
        invalid_taxes + invalid_tiers + invalid_categories + invalid_margins
    )

    print("==========================================")
    print("DEALFLOW360 — MUMBAI DATA VALIDATION")
    print("==========================================")
    print(f"Products:                 {len(p_rows):>3}")
    print(f"Variants:                 {len(pv_rows):>3}")
    print(f"Customers:                {len(cust_rows):>3}")
    print(f"Warehouses:               {len(w_rows):>3}")
    print(f"Inventory Records:        {len(inv_rows):>3}")
    print(f"Quotations:               {len(q_rows):>3}")
    print(f"Quotation Lines:          {len(ql_rows):>3}")
    print(f"Recommendations:          {len(rec_rows):>3}")
    print(f"Negotiations:             {len(neg_rows):>3}")
    print(f"Invoices:                 {len(invc_rows):>3}")
    print(f"Invoice Lines:            {len(invcl_rows):>3}")
    print("")
    print(f"Foreign Key Errors:       {fk_errors:>3}")
    print(f"Duplicate IDs:            {duplicate_ids:>3}")
    print(f"Duplicate SKUs:           {duplicate_skus:>3}")
    print(f"Invalid Prices:           {invalid_prices:>3}")
    print(f"Invalid Inventory:        {invalid_inventory:>3}")
    print(f"Invalid Margins:          {invalid_margins:>3}")
    print(f"Invalid Dates:            {invalid_dates:>3}")
    print(f"Invalid Discounts:        {invalid_discounts:>3}")
    print("")
    status_str = "PASS" if total_issues == 0 else f"FAIL ({total_issues} issues)"
    print(f"STATUS: {status_str}")
    if total_issues == 0:
        print("DATA QUALITY: 100%")
    print("==========================================")

    if error_log:
        print("\nFIRST 20 DETECTED ISSUES:")
        for err in error_log[:20]:
            print(f" - {err}")
        return False
    return True

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
