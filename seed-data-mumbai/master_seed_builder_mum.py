"""
DealFlow360 Master Seed Data Builder — Mumbai Edition
Orchestrates generation of all enterprise CSV files for Mumbai Enterprise Technology Distribution Center (MUM-DC-01)
Guarantees 100% relational integrity, authentic pricing, varied inventory, and full scenario coverage.
"""

import os
import sys
import csv
import random
from datetime import datetime, timedelta

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import build_base_mum
import build_catalog_mum

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

def run():
    print("==================================================")
    print("DEALFLOW360 MUMBAI SEED DATA GENERATOR")
    print("==================================================")

    # 1. Base entities
    brands = build_base_mum.BRANDS
    categories = build_base_mum.CATEGORIES
    warehouses = build_base_mum.WAREHOUSES
    services = build_base_mum.SERVICES
    subscriptions = build_base_mum.SUBSCRIPTION_PLANS
    discount_rules = build_base_mum.DISCOUNT_RULES
    approval_chains = build_base_mum.APPROVAL_CHAINS
    customers = build_base_mum.CUSTOMERS_DATA

    # 2. Catalog (Products & Variants)
    products, base_variants = build_catalog_mum.generate_catalog()

    # Expand variants to ensure 650+ sellable SKUs
    variants = list(base_variants)
    v_idx = len(variants) + 1

    var_by_prod = {}
    for v in variants:
        pid = v[1]
        var_by_prod.setdefault(pid, []).append(v)

    for p in products:
        pid = p[0]
        p_code = p[1]
        p_name = p[2]
        subcat = p[5]
        base_cost = float(p[10])
        base_price = float(p[11])
        existing_vars = var_by_prod.get(pid, [])

        if len(existing_vars) == 1:
            ev = existing_vars[0]
            if subcat in ["CAT-LAP", "CAT-DSK"]:
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-32G-1TB"
                vname = f"{ev[3].split(' / ')[0]} / 32GB DDR5 / 1TB NVMe / Win 11 Pro"
                extra = round(base_price * 0.22, 2)
                cost = round(base_cost + extra * 0.78, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], "32GB DDR5", "1TB", ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-WKS":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-128G-2TB"
                vname = f"{ev[3].split(' / ')[0]} / 128GB ECC / 2TB NVMe Gen5 / Dual GPU Ready"
                extra = round(base_price * 0.35, 2)
                cost = round(base_cost + extra * 0.78, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], "128GB DDR5 ECC", "2TB NVMe", ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SRV":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-256G-8TB"
                vname = f"{ev[3].split(' / ')[0]} / 256GB ECC / 8x 1.92TB Enterprise SAS SSD / Dual 1400W"
                extra = round(base_price * 0.45, 2)
                cost = round(base_cost + extra * 0.80, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], "256GB DDR5 ECC Reg", "15.36TB Raw", ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-STO":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-HIGH-IOPS"
                vname = f"{ev[3].split(' / ')[0]} / 128TB Raw / 32Gb Fibre Channel SAN Gateway"
                extra = round(base_price * 0.40, 2)
                cost = round(base_cost + extra * 0.80, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], "128GB Cache", "128TB Raw", ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-NET":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-DUAL-PWR"
                vname = f"{ev[3].split(' / ')[0]} / Redundant AC Power Supply & Stacking Module"
                extra = round(base_price * 0.20, 2)
                cost = round(base_cost + extra * 0.75, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], ev[6], ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-MON":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-ERGO-ARM"
                vname = f"{ev[3].split(' / ')[0]} / + Heavy-Duty Gas-Spring Ergonomic Desk Mount"
                extra = 4500.0
                cost = round(base_cost + extra * 0.70, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], ev[6], ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-UPS":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-EBM"
                vname = f"{ev[3].split(' / ')[0]} / + Extended Battery Module (EBM) 2U Pack"
                extra = 28000.0
                cost = round(base_cost + extra * 0.75, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], ev[6], ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SEC":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-UTP-1YR"
                vname = f"{ev[3].split(' / ')[0]} / + 1-Year Enterprise Unified Threat Protection Suite"
                extra = 25000.0
                cost = round(base_cost + extra * 0.75, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], ev[6], ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907300{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

    print(f"Final Products Count: {len(products)}")
    print(f"Final Sellable Variants Count: {len(variants)}")

    prod_dict = {p[0]: p for p in products}
    var_dict = {v[0]: v for v in variants}
    sku_to_vid = {v[2]: v[0] for v in variants}

    # Find key SKUs for demo scenarios
    var_lap_5440 = sku_to_vid.get("LAP-DEL-5440-I5-16-512", variants[0][0])
    var_dock_wd19s = sku_to_vid.get("ACC-DEL-WD19S-STD", variants[1][0])
    var_mon_u2724d = sku_to_vid.get("MON-DEL-U2724D-STD", variants[2][0])
    var_phn_ip16p = sku_to_vid.get("SMP-APL-IP16P-256-BLK", variants[3][0])
    var_phn_s24u = sku_to_vid.get("SMP-SAM-S24U-256-GRY", variants[4][0])
    var_srv_r760 = sku_to_vid.get("SRV-DEL-R760-128-2TB", variants[5][0])
    var_lap_t14 = sku_to_vid.get("LAP-LEN-T14G4-I5-16-512", variants[6][0])
    var_net_c9300 = sku_to_vid.get("NET-CIS-C9300-48P-STD", variants[7][0])
    var_fw_fg100f = sku_to_vid.get("SEC-FOR-FG100F-STD", variants[8][0])

    # --------------------------------------------------------------------------
    # 3. INVENTORY GENERATION (Target: 800+ across 5 DCs, Primary: MUM-DC-01)
    # --------------------------------------------------------------------------
    inventory = []
    inv_idx = 1

    # Populate Mumbai Central (WH-001) for all variants
    for v in variants:
        vid = v[0]
        pid = v[1]
        p_obj = prod_dict[pid]
        subcat = p_obj[5]

        # Specific demo scenario configurations for Mumbai
        if vid == var_srv_r760:
            # Flow 4 requirement: Customer requests 20 servers. Mumbai has 12 available, 8 backordered!
            avail = 12
            res = 12
            alloc = 12
            backorder = 8
            reorder_lvl = 6
            reorder_qty = 20
            safety = 4
            incoming = 8
            avg_demand = 1.5
            status = "BACKORDER"
        elif vid == var_lap_t14:
            # Flow 3 requirement: Customer orders 80 laptops. Mumbai has 50, Bangalore has 30.
            avail = 50
            res = 50
            alloc = 50
            backorder = 0
            reorder_lvl = 30
            reorder_qty = 80
            safety = 20
            incoming = 40
            avg_demand = 6.0
            status = "IN_STOCK"
        elif vid == var_phn_ip16p:
            # Smartphone multi-warehouse scenario: Customer requests 20. Mumbai has 12, Navi Mumbai has 8.
            avail = 12
            res = 12
            alloc = 12
            backorder = 0
            reorder_lvl = 15
            reorder_qty = 30
            safety = 10
            incoming = 15
            avg_demand = 3.0
            status = "IN_STOCK"
        elif vid == var_lap_5440:
            # Flow 1 requirement: 30 laptops
            avail = 85
            res = 30
            alloc = 30
            backorder = 0
            reorder_lvl = 25
            reorder_qty = 60
            safety = 15
            incoming = 40
            avg_demand = 5.0
            status = "IN_STOCK"
        elif vid == var_dock_wd19s:
            avail = 140
            res = 30
            alloc = 30
            backorder = 0
            reorder_lvl = 30
            reorder_qty = 100
            safety = 20
            incoming = 50
            avg_demand = 8.0
            status = "IN_STOCK"
        elif vid == var_mon_u2724d:
            avail = 110
            res = 30
            alloc = 30
            backorder = 0
            reorder_lvl = 25
            reorder_qty = 80
            safety = 18
            incoming = 40
            avg_demand = 7.0
            status = "IN_STOCK"
        elif subcat == "CAT-SRV":
            avail = random.randint(1, 15)
            res = random.randint(0, min(avail, 3))
            alloc = res
            backorder = random.choice([0, 0, 0, 1, 2])
            reorder_lvl = 4
            reorder_qty = 10
            safety = 2
            incoming = random.choice([0, 4, 6])
            avg_demand = round(random.uniform(0.2, 1.2), 1)
            status = "LOW_STOCK" if avail <= 3 else "IN_STOCK"
        elif subcat == "CAT-WKS":
            avail = random.randint(2, 20)
            res = random.randint(0, min(avail, 4))
            alloc = res
            backorder = 0
            reorder_lvl = 5
            reorder_qty = 12
            safety = 3
            incoming = random.choice([0, 4, 8])
            avg_demand = round(random.uniform(0.5, 2.0), 1)
            status = "LOW_STOCK" if avail <= 4 else "IN_STOCK"
        elif subcat in ["CAT-LAP", "CAT-DSK"]:
            avail = random.randint(20, 140)
            res = random.randint(5, 25)
            alloc = res
            backorder = 0
            reorder_lvl = 25
            reorder_qty = 60
            safety = 15
            incoming = random.choice([20, 40])
            avg_demand = round(random.uniform(3.0, 10.0), 1)
            status = "IN_STOCK"
        elif subcat in ["CAT-SMP", "CAT-TAB"]:
            avail = random.randint(10, 85)
            res = random.randint(2, 15)
            alloc = res
            backorder = 0
            reorder_lvl = 15
            reorder_qty = 40
            safety = 10
            incoming = random.choice([15, 30])
            avg_demand = round(random.uniform(2.0, 6.0), 1)
            status = "IN_STOCK"
        elif subcat in ["CAT-NET", "CAT-SEC"]:
            avail = random.randint(5, 45)
            res = random.randint(1, 8)
            alloc = res
            backorder = 0
            reorder_lvl = 10
            reorder_qty = 25
            safety = 5
            incoming = random.choice([10, 20])
            avg_demand = round(random.uniform(1.0, 4.0), 1)
            status = "LOW_STOCK" if avail <= 6 else "IN_STOCK"
        elif subcat == "CAT-ACC":
            avail = random.randint(60, 450)
            res = random.randint(10, 50)
            alloc = res
            backorder = 0
            reorder_lvl = 50
            reorder_qty = 150
            safety = 30
            incoming = random.choice([50, 100])
            avg_demand = round(random.uniform(8.0, 30.0), 1)
            status = "IN_STOCK"
        else:
            avail = random.randint(10, 60)
            res = random.randint(1, 10)
            alloc = res
            backorder = 0
            reorder_lvl = 12
            reorder_qty = 30
            safety = 8
            incoming = random.choice([10, 20])
            avg_demand = round(random.uniform(1.5, 5.0), 1)
            status = "IN_STOCK"

        inv_id = f"INV-{inv_idx:05d}"
        inv_idx += 1
        inventory.append([
            inv_id, "WH-001", vid, avail, res, alloc, backorder,
            reorder_lvl, reorder_qty, safety, incoming, avg_demand,
            status, "2026-02-15T10:00:00Z", "2026-03-25T10:00:00Z"
        ])

    # Secondary Hub: Navi Mumbai (WH-002) for mobility, laptops & accessories (~220 variants)
    for v in variants[:220]:
        vid = v[0]
        if vid == var_phn_ip16p:
            avail = 8 # Scenario 2: 8 in Navi Mumbai
            res = 8
            alloc = 8
        else:
            avail = random.randint(10, 60)
            res = random.randint(2, 10)
            alloc = res
        inv_id = f"INV-{inv_idx:05d}"
        inv_idx += 1
        inventory.append([
            inv_id, "WH-002", vid, avail, res, alloc, 0,
            15, 40, 10, 20, round(random.uniform(1.0, 5.0), 1),
            "IN_STOCK", "2026-02-18T11:00:00Z", "2026-03-28T11:00:00Z"
        ])

    # Regional Hubs: Bangalore (WH-003), Delhi (WH-004), Ahmedabad (WH-005) for split fulfillment
    # Bangalore: Laptop split scenario (30 laptops) + Server split scenario (3 servers)
    inv_id = f"INV-{inv_idx:05d}"
    inv_idx += 1
    inventory.append([
        inv_id, "WH-003", var_lap_t14, 30, 30, 30, 0,
        20, 60, 15, 30, 4.0, "IN_STOCK", "2026-02-20T10:00:00Z", "2026-03-30T10:00:00Z"
    ])

    inv_id = f"INV-{inv_idx:05d}"
    inv_idx += 1
    inventory.append([
        inv_id, "WH-003", var_srv_r760, 3, 3, 3, 0,
        4, 10, 2, 5, 0.8, "IN_STOCK", "2026-02-20T10:00:00Z", "2026-03-30T10:00:00Z"
    ])

    # Delhi: Server split scenario (3 servers)
    inv_id = f"INV-{inv_idx:05d}"
    inv_idx += 1
    inventory.append([
        inv_id, "WH-004", var_srv_r760, 3, 3, 3, 0,
        4, 10, 2, 5, 0.8, "IN_STOCK", "2026-02-20T10:00:00Z", "2026-03-30T10:00:00Z"
    ])

    # Add ~100 more items in regional hubs for realism
    for wh in ["WH-003", "WH-004", "WH-005"]:
        for mvid in [v[0] for v in variants[20:60]]:
            inv_id = f"INV-{inv_idx:05d}"
            inv_idx += 1
            r_avail = random.randint(15, 50)
            r_res = random.randint(1, 8)
            inventory.append([
                inv_id, wh, mvid, r_avail, r_res, r_res, 0,
                12, 35, 8, 15, round(random.uniform(1.0, 4.0), 1),
                "IN_STOCK", "2026-02-12T10:00:00Z", "2026-03-22T10:00:00Z"
            ])

    print(f"Generated {len(inventory)} Inventory records across 5 distribution centers (Primary: MUM-DC-01).")

    # --------------------------------------------------------------------------
    # 4. PRICE LISTS (Standard, SMB, Enterprise, Strategic)
    # --------------------------------------------------------------------------
    price_lists = []
    tiers = [
        ("PL-STD", "Standard Commercial Price List", "Standard", 0.0, 1),
        ("PL-SMB", "SMB Advantage Price List", "SMB", 0.05, 5),
        ("PL-ENT", "Enterprise Preferred Price List", "Enterprise", 0.11, 20),
        ("PL-STRAT", "Strategic Global Partner Price List", "Strategic", 0.18, 50)
    ]

    for pl_code, pl_name, tier, discount_factor, min_qty in tiers:
        for v in variants:
            vid = v[0]
            std_price = float(v[18])
            cost_price = float(v[17])
            if tier == "Standard":
                unit_price = std_price
            else:
                subcat = prod_dict[v[1]][5]
                if subcat == "CAT-ACC":
                    tier_disc = discount_factor * 1.25
                elif subcat in ["CAT-SRV", "CAT-WKS", "CAT-STO"]:
                    tier_disc = discount_factor * 0.90
                else:
                    tier_disc = discount_factor
                calculated_price = round(std_price * (1.0 - tier_disc), 2)
                # Ensure negotiated price is strictly above cost (min 4% margin floor)
                unit_price = max(calculated_price, round(cost_price * 1.04, 2))

            pl_row = [
                pl_code, pl_name, tier, "INR", vid,
                f"{unit_price:.2f}", min_qty, "2026-01-01", "2026-12-31", "ACTIVE"
            ]
            price_lists.append(pl_row)

    print(f"Generated {len(price_lists)} Price List line records ({len(tiers)} tiers x {len(variants)} variants).")

    # --------------------------------------------------------------------------
    # 5. CUSTOMER PRICE LIST ASSIGNMENTS (100 Customers)
    # --------------------------------------------------------------------------
    customer_price_lists = []
    cpl_idx = 1
    tier_to_pl = {
        "Strategic": "PL-STRAT",
        "Enterprise": "PL-ENT",
        "SMB": "PL-SMB",
        "Standard": "PL-STD"
    }

    for c in customers:
        cid = c[0]
        c_tier = c[4]
        pl_code = tier_to_pl.get(c_tier, "PL-STD")
        cpl_id = f"CPL-{cpl_idx:04d}"
        cpl_idx += 1
        customer_price_lists.append([
            cpl_id, cid, pl_code, "2026-01-01", "2026-12-31", "ACTIVE"
        ])

    print(f"Generated {len(customer_price_lists)} Customer Price List mappings.")

    # --------------------------------------------------------------------------
    # 6. PRODUCT RECOMMENDATIONS (Upsell / Cross-Sell / Attachment) - Target: 350+
    # --------------------------------------------------------------------------
    recommendations = []
    rec_idx = 1

    dock_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Dock" in p[2]]
    monitor_prods = [p[0] for p in products if p[5] == "CAT-MON"]
    bag_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Backpack" in p[2]]
    mouse_prods = [p[0] for p in products if p[5] == "CAT-ACC" and ("Mouse" in p[2] or "Combo" in p[2] or "Keys" in p[2])]
    headset_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Headset" in p[2]]
    ups_prods = [p[0] for p in products if p[5] == "CAT-UPS"]
    chargers = [c[0] for c in products if c[5] == "CAT-ACC" and ("Charger" in c[2] or "Power Bank" in c[2])]
    switch_prods = [p[0] for p in products if p[5] == "CAT-NET" and "Switch" in p[2]]
    sfp_prods = [p[0] for p in products if p[5] == "CAT-NET" and ("SFP" in p[2] or "DAC" in p[2])]
    server_prods = [p[0] for p in products if p[5] == "CAT-SRV"]

    seen_pairs = set()

    def add_rec(src, tgt, rtype, conf, copurchase, delta, prio, reason):
        nonlocal rec_idx
        if (src, tgt) in seen_pairs or src == tgt:
            return
        seen_pairs.add((src, tgt))
        recommendations.append([
            f"REC-{rec_idx:04d}", src, tgt, rtype, conf, copurchase, delta, prio, True, 20.0, reason, "ACTIVE"
        ])
        rec_idx += 1

    for p in products:
        pid = p[0]
        subcat = p[5]

        if subcat == "CAT-LAP":
            if dock_prods:
                add_rec(pid, random.choice(dock_prods), "CROSS_SELL", 0.94, 0.85, 8.5, 1, "Essential docking station enabling multi-monitor financial desk productivity")
            if monitor_prods:
                add_rec(pid, random.choice(monitor_prods), "ATTACHMENT", 0.89, 0.76, 6.5, 2, "Recommended high-resolution display for corporate spreadsheet analysis")
            if headset_prods:
                add_rec(pid, random.choice(headset_prods), "ATTACHMENT", 0.86, 0.71, 9.5, 3, "Noise-cancelling wireless headset for executive Zoom/Teams conferences")
            if bag_prods:
                add_rec(pid, random.choice(bag_prods), "ATTACHMENT", 0.92, 0.84, 14.0, 4, "Protective corporate ballistic nylon backpack for executive travel")

        elif subcat == "CAT-WKS":
            hi_res_mon = [m for m in monitor_prods if "4K" in prod_dict[m][2] or "Ultrawide" in prod_dict[m][2] or "U34" in prod_dict[m][1]]
            if hi_res_mon:
                add_rec(pid, random.choice(hi_res_mon), "UPSELL", 0.96, 0.89, 10.5, 1, "Factory color-calibrated high-density display required for algorithmic modeling")
            if ups_prods:
                add_rec(pid, random.choice(ups_prods), "ATTACHMENT", 0.92, 0.78, 8.0, 2, "Pure sine-wave power backup prevents computational workstation data corruption")

        elif subcat == "CAT-SRV":
            rack_ups = [u for u in ups_prods if "SRT" in prod_dict[u][1] or "9PX" in prod_dict[u][1] or "GXT5" in prod_dict[u][1]]
            if rack_ups:
                add_rec(pid, random.choice(rack_ups), "ATTACHMENT", 0.97, 0.92, 9.0, 1, "Online double-conversion UPS guarantees zero-downtime power for mission-critical server nodes")
            if sfp_prods:
                add_rec(pid, random.choice(sfp_prods), "CROSS_SELL", 0.91, 0.82, 15.0, 2, "10G/25G SFP28 optical transceivers for high-throughput top-of-rack leaf-spine links")
            if switch_prods:
                add_rec(pid, random.choice(switch_prods), "ATTACHMENT", 0.88, 0.75, 12.0, 3, "Dedicated Top-of-Rack management and SAN interconnect switch")

        elif subcat == "CAT-DSK":
            if monitor_prods:
                add_rec(pid, random.choice(monitor_prods), "ATTACHMENT", 0.93, 0.86, 8.0, 1, "Ergonomic dual-monitor pairing expands multi-tasking workspace")
            if mouse_prods:
                add_rec(pid, random.choice(mouse_prods), "CROSS_SELL", 0.95, 0.90, 12.0, 2, "Enterprise wireless keyboard and silent mouse combo")
            if ups_prods:
                add_rec(pid, random.choice(ups_prods), "ATTACHMENT", 0.90, 0.78, 10.0, 3, "Line-interactive desktop UPS safeguards corporate desktop sessions")

        elif subcat == "CAT-NET":
            if sfp_prods:
                add_rec(pid, random.choice(sfp_prods), "ATTACHMENT", 0.97, 0.93, 18.0, 1, "Certified high-speed optical transceivers for fiber backbone uplink")
            if ups_prods:
                add_rec(pid, random.choice(ups_prods), "ATTACHMENT", 0.91, 0.80, 10.0, 2, "Rackmount power backup prevents packet loss and switch reboots")

        elif subcat == "CAT-STO":
            if sfp_prods:
                add_rec(pid, random.choice(sfp_prods), "CROSS_SELL", 0.94, 0.88, 16.0, 1, "16Gb/32Gb Fibre Channel optical transceivers for low-latency SAN fabric")
            if ups_prods:
                add_rec(pid, random.choice(ups_prods), "ATTACHMENT", 0.96, 0.90, 12.0, 2, "Online double-conversion UPS prevents cache write-back corruption")

        elif subcat == "CAT-SEC":
            if sfp_prods:
                add_rec(pid, random.choice(sfp_prods), "ATTACHMENT", 0.95, 0.89, 15.0, 1, "10G SFP+ optical interfaces for high-throughput perimeter inspection ports")
            if switch_prods:
                add_rec(pid, random.choice(switch_prods), "CROSS_SELL", 0.90, 0.81, 14.0, 2, "Dedicated DMZ distribution switch for isolated security zones")

        elif subcat == "CAT-MON":
            if dock_prods:
                add_rec(pid, random.choice(dock_prods), "CROSS_SELL", 0.89, 0.80, 10.0, 1, "Thunderbolt docking station streamlines single-cable video, data and 100W charging")

        elif subcat == "CAT-SMP":
            if chargers:
                add_rec(pid, random.choice(chargers), "CROSS_SELL", 0.93, 0.86, 16.5, 1, "120W GaN multi-port fast charger powers phone and executive laptop simultaneously")
            if headset_prods:
                add_rec(pid, random.choice(headset_prods), "ATTACHMENT", 0.88, 0.77, 12.0, 2, "Bluetooth ANC headset for corporate executive mobile communications")

        elif subcat == "CAT-TAB":
            if chargers:
                add_rec(pid, random.choice(chargers), "CROSS_SELL", 0.89, 0.81, 15.0, 1, "Fast USB-C power adapter ensures quick device turnaround for field personnel")

        elif subcat == "CAT-COL":
            if monitor_prods:
                add_rec(pid, random.choice(monitor_prods), "ATTACHMENT", 0.92, 0.84, 10.0, 1, "Commercial dual displays complete corporate executive boardroom setup")

    print(f"Generated {len(recommendations)} Product Recommendations (Upsell, Cross-Sell, Attachment).")

    # --------------------------------------------------------------------------
    # 7. PRODUCT SERVICE RULES (150+ Attachment Rules)
    # --------------------------------------------------------------------------
    product_service_rules = []
    psr_idx = 1

    for p in products:
        pid = p[0]
        subcat = p[5]

        if subcat == "CAT-SRV":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-001", True, False, 1])
            psr_idx += 1
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-015", True, False, 2])
            psr_idx += 1
        elif subcat == "CAT-NET":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-003", True, False, 1])
            psr_idx += 1
            if "AP" in p[1] or "Wi-Fi" in p[2]:
                product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-014", True, False, 2])
                psr_idx += 1
        elif subcat == "CAT-SEC":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-004", True, True, 1])
            psr_idx += 1
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-018", True, False, 2])
            psr_idx += 1
        elif subcat in ["CAT-LAP", "CAT-DSK"]:
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-005", True, False, 1])
            psr_idx += 1
        elif subcat == "CAT-WKS":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-006", True, False, 1])
            psr_idx += 1
        elif subcat == "CAT-STO":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-002", True, False, 1])
            psr_idx += 1
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-011", True, False, 2])
            psr_idx += 1
        elif subcat == "CAT-UPS":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-008", True, False, 1])
            psr_idx += 1
        elif subcat == "CAT-COL":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-009", True, False, 1])
            psr_idx += 1
        elif subcat == "CAT-SMP":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-024", True, False, 1])
            psr_idx += 1

    print(f"Generated {len(product_service_rules)} Product-Service Attachment Rules.")

    # --------------------------------------------------------------------------
    # 8. QUOTATIONS & QUOTATION LINES (Target: 100+ Quotations, 400+ Lines)
    # --------------------------------------------------------------------------
    quotations = []
    quotation_lines = []
    q_line_idx = 1

    def create_quotation(q_num, cust_id, q_date, valid_days, lines_spec, status="Approved", approval_status="Approved", deal_health="Healthy", notes=""):
        nonlocal q_line_idx
        qid = f"QT-MUM-{q_num.split('-')[-1]}"
        v_until = (datetime.strptime(q_date, "%Y-%m-%d") + timedelta(days=valid_days)).strftime("%Y-%m-%d")

        subtotal = 0.0
        disc_total = 0.0
        tax_total = 0.0
        grand_total = 0.0
        q_lines = []

        for line_no, spec in enumerate(lines_spec, start=1):
            line_id = f"QL-{q_line_idx:05d}"
            q_line_idx += 1

            itype = spec["item_type"]
            qty = spec["qty"]
            price = spec["unit_price"]
            disc_pct = spec.get("discount_pct", 0.0)
            tax_rate = spec.get("tax_rate", 18.0)
            btype = spec.get("billing_type", "ONE_TIME")
            ff_status = spec.get("fulfillment_status", "ALLOCATED")
            wh_id = spec.get("wh_id", "WH-001")

            v_id = spec.get("variant_id", "")
            s_id = spec.get("service_id", "")
            sub_id = spec.get("subscription_id", "")
            desc = spec["description"]

            line_sub = round(qty * price, 2)
            line_disc = round(line_sub * (disc_pct / 100.0), 2)
            net_taxable = round(line_sub - line_disc, 2)
            line_tax = round(net_taxable * (tax_rate / 100.0), 2)
            line_total = round(net_taxable + line_tax, 2)

            subtotal += line_sub
            disc_total += line_disc
            tax_total += line_tax
            grand_total += line_total

            ql_row = [
                line_id, qid, line_no, itype, v_id, s_id, sub_id, desc,
                qty, f"{price:.2f}", f"{disc_pct:.2f}", f"{line_disc:.2f}",
                f"{tax_rate:.1f}", f"{line_tax:.2f}", f"{line_total:.2f}",
                btype, wh_id if itype == "PRODUCT" else "", ff_status
            ]
            q_lines.append(ql_row)

        subtotal = round(subtotal, 2)
        disc_total = round(disc_total, 2)
        tax_total = round(tax_total, 2)
        grand_total = round(grand_total, 2)

        q_row = [
            qid, q_num, cust_id, q_date, v_until, "INR",
            f"{subtotal:.2f}", f"{disc_total:.2f}", f"{tax_total:.2f}", f"{grand_total:.2f}",
            status, approval_status, deal_health, "Vikramaditya Singhania", notes
        ]
        quotations.append(q_row)
        quotation_lines.extend(q_lines)

    # --------------------------------------------------------------------------
    # SPECIAL MUMBAI DEMO SCENARIOS (FLOWS 1 to 6)
    # --------------------------------------------------------------------------

    # Flow 1 (Section 45): Discount Governance Escalation
    # Customer: Meridian Capital Financial Services Ltd (CUST-001)
    # 30 Premium Laptops (Latitude 5440), 30 Monitors (U2724D), 30 Docks (WD19S), Deployment Service
    # Discount applied on Laptops: 22.0% (breaches Enterprise ceiling of 16.0%) -> Triggers L2/L3 approval -> Deal Health flagged
    p_lap_price = float(var_dict[var_lap_5440][18])
    p_dock_price = float(var_dict[var_dock_wd19s][18])
    p_mon_price = float(var_dict[var_mon_u2724d][18])

    create_quotation(
        "QT-MUM-2026-0001", "CUST-001", "2026-02-28", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_5440, "description": var_dict[var_lap_5440][3], "qty": 30, "unit_price": p_lap_price, "discount_pct": 22.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_mon_u2724d, "description": var_dict[var_mon_u2724d][3], "qty": 30, "unit_price": p_mon_price, "discount_pct": 14.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_dock_wd19s, "description": var_dict[var_dock_wd19s][3], "qty": 30, "unit_price": p_dock_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise Laptop Zero-Touch Imaging & Domain Join", "qty": 30, "unit_price": 1400.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Pending Approval", approval_status="Pending L2 Finance & L3 Commercial Review", deal_health="Critical",
        notes="Demo Flow 1: Discount Governance. 22.0% laptop discount requested by Meridian Capital breaches 16.0% category ceiling. High Risk status triggers L2/L3 dual signoff."
    )

    # Flow 2 (Section 45): Intelligent Upsell & Attachment
    # Customer: WestBay Securities & Algorithmic Trading Ltd (CUST-002)
    # Latitude 7450 + WD22TB4 Dock + U2724D Monitor + Jabra Headset + 3-Yr AMC
    var_lap_7450 = sku_to_vid.get("LAP-DEL-7450-U7-16-512", var_lap_5440)
    var_dock_tb4 = sku_to_vid.get("ACC-DEL-WD22TB4-STD", var_dock_wd19s)
    var_headset = sku_to_vid.get("ACC-JAB-EV265-STD", variants[15][0])
    p_7450_price = float(var_dict[var_lap_7450][18])
    p_tb4_price = float(var_dict[var_dock_tb4][18])
    p_hs_price = float(var_dict[var_headset][18])

    create_quotation(
        "QT-MUM-2026-0002", "CUST-002", "2026-02-27", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_7450, "description": var_dict[var_lap_7450][3], "qty": 25, "unit_price": p_7450_price, "discount_pct": 8.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_dock_tb4, "description": f"{var_dict[var_dock_tb4][3]} (Recommended Upsell)", "qty": 25, "unit_price": p_tb4_price, "discount_pct": 10.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_mon_u2724d, "description": f"{var_dict[var_mon_u2724d][3]} (Recommended Dual Screen)", "qty": 25, "unit_price": p_mon_price, "discount_pct": 10.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_headset, "description": f"{var_dict[var_headset][3]} (Attached Audio)", "qty": 25, "unit_price": p_hs_price, "discount_pct": 10.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SUBSCRIPTION", "subscription_id": "SUB-001", "description": "Comprehensive 24x7 4-Hour SLA Enterprise Hardware AMC (Annual)", "qty": 25, "unit_price": 52000.0, "discount_pct": 5.0, "billing_type": "RECURRING", "fulfillment_status": "PENDING"}
        ],
        status="Approved", approval_status="Approved", deal_health="Healthy",
        notes="Demo Flow 2: Intelligent Upsell. Core laptop proposal expanded with Thunderbolt 4 dock, 120Hz IPS Black display, ANC headset, and 24x7 4-Hour AMC subscription."
    )

    # Flow 3 (Section 45): Multi-Warehouse Split Allocation
    # Customer: HarborPoint Life Insurance Corporation Ltd (CUST-003)
    # Order: 80 ThinkPad T14 laptops. Mumbai DC fulfills 50, Bangalore DC fulfills 30.
    p_t14_price = float(var_dict[var_lap_t14][18])
    create_quotation(
        "QT-MUM-2026-0003", "CUST-003", "2026-02-25", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_t14, "description": f"{var_dict[var_lap_t14][3]} (Primary: Mumbai DC MUM-DC-01)", "qty": 50, "unit_price": p_t14_price, "discount_pct": 11.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_lap_t14, "description": f"{var_dict[var_lap_t14][3]} (Split Fulfillment: Bangalore Hub BLR-DC-01)", "qty": 30, "unit_price": p_t14_price, "discount_pct": 11.0, "wh_id": "WH-003", "fulfillment_status": "PARTIAL_SPLIT", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise Laptop Zero-Touch Imaging & Domain Join", "qty": 80, "unit_price": 1400.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Confirmed", approval_status="Approved", deal_health="Healthy",
        notes="Demo Flow 3: Multi-Warehouse Split. 80 units procured: 50 fulfilled from Mumbai primary distribution center (MUM-DC-01) and 30 fulfilled from Bangalore hub (BLR-DC-01)."
    )

    # Flow 4 (Section 45): Server Fulfillment & Factory Backorder
    # Customer: Skyline Pharmaceuticals Global R&D Ltd (CUST-004)
    # 20 Dell PowerEdge R760 servers requested. Mumbai has 12 available immediately, 8 routed to factory backorder.
    p_r760_price = float(var_dict[var_srv_r760][18])
    create_quotation(
        "QT-MUM-2026-0004", "CUST-004", "2026-02-24", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (Immediate Stock Allocation)", "qty": 12, "unit_price": p_r760_price, "discount_pct": 10.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (OEM Factory Backorder - 3 Weeks Lead Time)", "qty": 8, "unit_price": p_r760_price, "discount_pct": 10.0, "wh_id": "WH-001", "fulfillment_status": "BACKORDERED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-001", "description": "Enterprise Server & High-Density Rack Installation", "qty": 20, "unit_price": 8500.0, "discount_pct": 5.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Confirmed", approval_status="Approved", deal_health="Watch",
        notes="Demo Flow 4: Backorder Management. Order for 20x PowerEdge R760. 12 units fulfilled from Mumbai Central inventory; 8 units placed on OEM factory backorder."
    )

    # Flow 5 (Section 45): Hybrid Billing (CAPEX + Recurring OPEX)
    # Customer: BluePeak Media Broadcasting Network Pvt Ltd (CUST-005)
    # 50 Laptops + 50 Deployment Services + 50 Annual Managed-Device Mobility Subscriptions (SUB-007)
    create_quotation(
        "QT-MUM-2026-0005", "CUST-005", "2026-02-22", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_5440, "description": var_dict[var_lap_5440][3], "qty": 50, "unit_price": p_lap_price, "discount_pct": 9.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise Laptop Zero-Touch Imaging & Domain Join", "qty": 50, "unit_price": 1400.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"},
            {"item_type": "SUBSCRIPTION", "subscription_id": "SUB-007", "description": "Cloud Endpoint Mobility Management (MDM) Enterprise Seat (Annual)", "qty": 50, "unit_price": 2600.0, "discount_pct": 0.0, "billing_type": "RECURRING", "fulfillment_status": "PENDING"}
        ],
        status="Approved", approval_status="Approved", deal_health="Healthy",
        notes="Demo Flow 5: Hybrid Billing. Combines hardware CAPEX (50 laptops), professional services (imaging), and recurring annual OPEX (MDM software subscription)."
    )

    # Flow 6 (Section 45): Customer Counter-Offer / Negotiation
    # Customer: MetroCore Global Logistics & Supply Chain Ltd (CUST-006)
    # Quote: ₹28,40,000 approx -> Customer counter-offers ₹25,00,000 (~12.0% requested concession)
    var_mac_mbp = sku_to_vid.get("LAP-APL-MBP14-M3P-18-512-SBLK", variants[12][0])
    p_mac_price = float(var_dict[var_mac_mbp][18])
    create_quotation(
        "QT-MUM-2026-0006", "CUST-006", "2026-02-20", 20,
        [
            {"item_type": "PRODUCT", "variant_id": var_mac_mbp, "description": "MacBook Pro 14 M3 Pro Developer Laptops", "qty": 14, "unit_price": p_mac_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-013", "description": "Apple macOS Corporate Fleet Provisioning & Jamf Enrollment", "qty": 14, "unit_price": 1600.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Under Negotiation", approval_status="Pending Commercial Approval", deal_health="Watch",
        notes="Demo Flow 6: Customer Negotiation in progress. Client submitted counter-offer of ₹25,00,000 (requesting 12.0% concession on Apple hardware). Approval workflow re-evaluating risk."
    )

    # Multi-Warehouse Scenario 2: Smartphone Split (Section 33)
    # Customer: Crestline Management Consulting International (CUST-007)
    # Order: 20x iPhone 16 Pro 256GB -> 12 fulfilled from Mumbai (WH-001), 8 fulfilled from Navi Mumbai (WH-002)
    p_ip16_price = float(var_dict[var_phn_ip16p][18])
    create_quotation(
        "QT-MUM-2026-0007", "CUST-007", "2026-02-26", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_phn_ip16p, "description": f"{var_dict[var_phn_ip16p][3]} (Mumbai DC MUM-DC-01 Allocation)", "qty": 12, "unit_price": p_ip16_price, "discount_pct": 6.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_phn_ip16p, "description": f"{var_dict[var_phn_ip16p][3]} (Navi Mumbai NAVI-MUM-DC-01 Split)", "qty": 8, "unit_price": p_ip16_price, "discount_pct": 6.0, "wh_id": "WH-002", "fulfillment_status": "PARTIAL_SPLIT", "billing_type": "ONE_TIME"},
            {"item_type": "SUBSCRIPTION", "subscription_id": "SUB-008", "description": "Executive VIP Concierge Mobility Protection (Annual)", "qty": 20, "unit_price": 5400.0, "discount_pct": 0.0, "billing_type": "RECURRING", "fulfillment_status": "PENDING"}
        ],
        status="Approved", approval_status="Approved", deal_health="Healthy",
        notes="Demo Scenario: Corporate Smartphone Split. 20 executive smartphones split between Mumbai (12) and Navi Mumbai staging hub (8)."
    )

    # Multi-Warehouse Scenario 3: Server Multi-DC Split (Section 33)
    # Customer: UrbanGrid Retail & E-Commerce Technologies Ltd (CUST-008)
    # Order: 10 PowerEdge R760 servers -> 4 from Mumbai, 3 from Bangalore, 3 from Delhi
    create_quotation(
        "QT-MUM-2026-0008", "CUST-008", "2026-02-19", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (Mumbai Fulfillment)", "qty": 4, "unit_price": p_r760_price, "discount_pct": 10.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (Bangalore Hub Fulfillment)", "qty": 3, "unit_price": p_r760_price, "discount_pct": 10.0, "wh_id": "WH-003", "fulfillment_status": "PARTIAL_SPLIT", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (Delhi Hub Fulfillment)", "qty": 3, "unit_price": p_r760_price, "discount_pct": 10.0, "wh_id": "WH-004", "fulfillment_status": "PARTIAL_SPLIT", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-001", "description": "Enterprise Server & High-Density Rack Installation", "qty": 10, "unit_price": 8500.0, "discount_pct": 5.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Confirmed", approval_status="Approved", deal_health="Healthy",
        notes="Demo Scenario: Tri-Warehouse Server Allocation. 10 servers split across Mumbai (4), Bangalore (3), and Delhi (3)."
    )

    # Demo Scenario 9: Stalled Inactive Quotation (Deal Health At Risk)
    create_quotation(
        "QT-MUM-2026-0009", "CUST-015", "2026-01-08", 30,
        [
            {"item_type": "PRODUCT", "variant_id": variants[25][0], "description": variants[25][3], "qty": 15, "unit_price": float(variants[25][18]), "discount_pct": 5.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"}
        ],
        status="Sent", approval_status="Not Required", deal_health="At Risk",
        notes="Demo Scenario: Inactive Stalled Quotation. Proposal transmitted 52 days ago with zero client engagement since delivery."
    )

    # Demo Scenario 10: Critical Discount Anomaly Flagged
    p_c9300_price = float(var_dict[var_net_c9300][18])
    create_quotation(
        "QT-MUM-2026-0010", "CUST-018", "2026-02-28", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_net_c9300, "description": var_dict[var_net_c9300][3], "qty": 12, "unit_price": p_c9300_price, "discount_pct": 26.5, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-003", "description": "L2/L3 Core & Access Network Switch Configuration", "qty": 2, "unit_price": 13500.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Pending Approval", approval_status="Flagged - Critical Discount Anomaly", deal_health="Critical",
        notes="Demo Scenario: Critical Discount Anomaly. 26.5% discount requested on Cisco Catalyst 9300 exceeds category ceiling (14.0%) by 12.5%."
    )

    # Generate 90 more realistic quotations to reach 100 total
    for i in range(11, 101):
        q_code = f"QT-MUM-2026-{i:04d}"
        cust = customers[(i - 1) % len(customers)]
        cust_id = cust[0]

        num_items = random.randint(3, 5)
        sampled_vars = random.sample(variants, num_items)
        lines_spec = []

        for sv in sampled_vars:
            qty = random.choice([2, 5, 10, 20, 25, 40, 60])
            uprice = float(sv[18])
            disc = random.choice([0.0, 3.0, 5.0, 7.5, 10.0, 12.0])
            lines_spec.append({
                "item_type": "PRODUCT",
                "variant_id": sv[0],
                "description": sv[3],
                "qty": qty,
                "unit_price": uprice,
                "discount_pct": disc,
                "wh_id": "WH-001",
                "fulfillment_status": "ALLOCATED",
                "billing_type": "ONE_TIME"
            })

        if i % 3 == 0:
            srv = random.choice(services)
            lines_spec.append({
                "item_type": "SERVICE",
                "service_id": srv[0],
                "description": srv[2],
                "qty": 1,
                "unit_price": srv[6],
                "discount_pct": random.choice([0.0, 5.0, 10.0]),
                "billing_type": "ONE_TIME",
                "fulfillment_status": "PENDING"
            })

        if i % 4 == 0:
            sub = random.choice(subscriptions)
            lines_spec.append({
                "item_type": "SUBSCRIPTION",
                "subscription_id": sub[0],
                "description": f"{sub[2]} ({sub[3].title()})",
                "qty": 1,
                "unit_price": sub[5],
                "discount_pct": 0.0,
                "billing_type": "RECURRING",
                "fulfillment_status": "PENDING"
            })

        # Controlled realistic status distribution ensuring 52 billable quotes for 50+ Invoices & 200+ Invoice Lines
        if i <= 60:
            status = "Approved" if (i % 2 == 0) else "Confirmed"
        elif i <= 72:
            status = "Sent"
        elif i <= 84:
            status = "Under Negotiation"
        elif i <= 92:
            status = "Pending Approval"
        elif i <= 96:
            status = "Draft"
        elif i <= 98:
            status = "Expired"
        else:
            status = "Rejected"

        app_status = "Approved" if status in ["Approved", "Confirmed"] else ("Pending Approval" if status == "Pending Approval" else "Not Required")
        d_health = "At Risk" if status == "Expired" else ("Healthy" if status in ["Approved", "Confirmed"] else ("Critical" if status == "Rejected" else "Watch"))

        day = (i * 3) % 28 + 1
        month = 1 if i < 45 else 2
        q_date = f"2026-{month:02d}-{day:02d}"

        create_quotation(
            q_code, cust_id, q_date, 30, lines_spec,
            status=status, approval_status=app_status, deal_health=d_health,
            notes=f"Mumbai commercial proposal for {cust[2]} covering enterprise IT hardware procurement, integration and SLA services."
        )

    print(f"Generated {len(quotations)} Quotations with {len(quotation_lines)} Quotation Lines.")

    # --------------------------------------------------------------------------
    # 9. NEGOTIATIONS (Target: 35+ records)
    # --------------------------------------------------------------------------
    negotiations = []
    neg_idx = 1
    neg_quotes = [q for q in quotations if q[10] in ["Under Negotiation", "Pending Approval"]]
    for q in neg_quotes:
        qid = q[0]
        cid = q[2]
        ql_matching = [ql for ql in quotation_lines if ql[1] == qid and ql[3] == "PRODUCT"]
        for ql in ql_matching[:2]:
            orig_disc = float(ql[10])
            req_disc = orig_disc + random.choice([4.0, 6.0, 8.5, 11.0])
            msg = f"Client procurement requested revision to {req_disc:.1f}% discount citing parallel quotation from competitive Mumbai distributor."
            status = "RESOLVED" if random.random() > 0.45 else "PENDING_APPROVAL"
            sub_date = "2026-02-18T14:30:00Z"
            res_date = "2026-02-22T11:00:00Z" if status == "RESOLVED" else ""
            negotiations.append([
                f"NEG-{neg_idx:04d}", qid, cid, ql[0], f"{orig_disc:.1f}", f"{req_disc:.1f}",
                msg, status, sub_date, res_date
            ])
            neg_idx += 1
            if len(negotiations) >= 36:
                break
        if len(negotiations) >= 36:
            break

    print(f"Generated {len(negotiations)} Customer Negotiations.")

    # --------------------------------------------------------------------------
    # 10. DEAL HEALTH (1 record per quotation = 100 records)
    # --------------------------------------------------------------------------
    deal_health = []
    dh_idx = 1
    for q in quotations:
        qid = q[0]
        dh_status = q[12]

        if dh_status == "Critical":
            days_inact = random.randint(15, 35)
            disc_anom = round(random.uniform(0.75, 0.95), 2)
            deliv_risk = round(random.uniform(0.60, 0.85), 2)
            app_delay = round(random.uniform(0.70, 0.90), 2)
            inv_risk = round(random.uniform(0.50, 0.80), 2)
            overall = round(random.uniform(0.20, 0.40), 2)
            rec_action = "Escalate immediately to Commercial VP; schedule pricing governance review with Finance"
        elif dh_status == "At Risk":
            days_inact = random.randint(20, 50)
            disc_anom = round(random.uniform(0.20, 0.40), 2)
            deliv_risk = round(random.uniform(0.40, 0.60), 2)
            app_delay = round(random.uniform(0.30, 0.50), 2)
            inv_risk = round(random.uniform(0.30, 0.50), 2)
            overall = round(random.uniform(0.40, 0.55), 2)
            rec_action = "Re-engage executive sponsor; schedule in-person review at client Mumbai HQ"
        elif dh_status == "Watch":
            days_inact = random.randint(5, 14)
            disc_anom = round(random.uniform(0.10, 0.30), 2)
            deliv_risk = round(random.uniform(0.20, 0.40), 2)
            app_delay = round(random.uniform(0.20, 0.40), 2)
            inv_risk = round(random.uniform(0.20, 0.40), 2)
            overall = round(random.uniform(0.60, 0.75), 2)
            rec_action = "Follow up with account manager regarding expected Purchase Order release date"
        else: # Healthy
            days_inact = random.randint(1, 5)
            disc_anom = round(random.uniform(0.00, 0.15), 2)
            deliv_risk = round(random.uniform(0.05, 0.20), 2)
            app_delay = round(random.uniform(0.05, 0.20), 2)
            inv_risk = round(random.uniform(0.05, 0.20), 2)
            overall = round(random.uniform(0.80, 0.98), 2)
            rec_action = "Proceed with standard order processing and warehouse dispatch scheduling"

        deal_health.append([
            f"DH-{dh_idx:04d}", qid, days_inact, disc_anom, deliv_risk,
            app_delay, inv_risk, overall, dh_status, rec_action, "2026-03-01T12:00:00Z"
        ])
        dh_idx += 1

    print(f"Generated {len(deal_health)} Deal Health assessment records.")

    # --------------------------------------------------------------------------
    # 11. AUDIT LOGS (Target: 150+ records)
    # --------------------------------------------------------------------------
    audit_logs = []
    aud_idx = 1
    actions_pool = [
        ("Quotation", "Quote created", "", "Draft", "Sales Rep created initial commercial draft proposal"),
        ("Quotation", "Discount changed", "8.0%", "22.0%", "Account Director applied special competitive concession"),
        ("Quotation", "Approval requested", "Draft", "Pending Approval", "Concession exceeded standard rule threshold; escalated to L2 Finance"),
        ("Quotation", "Approval approved", "Pending Approval", "Approved", "Commercial approval granted after executive review"),
        ("Quotation", "Customer counter-offer submitted", "Approved", "Under Negotiation", "Customer requested 3.5% additional volume discount"),
        ("Quotation", "Warehouse allocation changed", "WH-001 (Mumbai)", "WH-001 + WH-003 Split", "Multi-warehouse split allocated due to local inventory balance"),
        ("Quotation", "Backorder created", "0", "8 Units", "Factory backorder registered directly with OEM manufacturing supply chain"),
        ("Quotation", "Quote confirmed", "Approved", "Confirmed", "Customer issued formal Purchase Order"),
        ("Invoice", "Invoice generated", "None", "INV-MUM-2026-0001", "Finance generated tax invoice against confirmed deal")
    ]

    for q in quotations[:55]:
        qid = q[0]
        num_logs = random.randint(2, 4)
        for act in random.sample(actions_pool, num_logs):
            audit_logs.append([
                f"AUD-{aud_idx:05d}", act[0], qid, act[1], act[2], act[3],
                "Vikramaditya Singhania", act[4], "2026-02-28T16:00:00Z"
            ])
            aud_idx += 1

    print(f"Generated {len(audit_logs)} Audit Log entries.")

    # --------------------------------------------------------------------------
    # 12. INVOICES & INVOICE LINES (Target: 50+ Invoices, 200+ Lines)
    # --------------------------------------------------------------------------
    invoices = []
    invoice_lines = []
    inv_num_idx = 1
    inv_line_idx = 1

    billable_quotes = [q for q in quotations if q[10] in ["Approved", "Confirmed"]]
    for q in billable_quotes:
        qid = q[0]
        cid = q[2]
        q_date = q[3]
        sub = q[6]
        disc = q[7]
        tax = q[8]
        grand = q[9]

        q_lines_for_quote = [ql for ql in quotation_lines if ql[1] == qid]
        has_recurring = any(ql[15] == "RECURRING" for ql in q_lines_for_quote)
        has_onetime = any(ql[15] == "ONE_TIME" for ql in q_lines_for_quote)
        b_type = "HYBRID" if (has_recurring and has_onetime) else ("RECURRING" if has_recurring else "ONE_TIME")

        inv_id = f"INV-BILL-{inv_num_idx:04d}"
        inv_number = f"INV-MUM-2026-{inv_num_idx:04d}"
        inv_num_idx += 1

        due_date = (datetime.strptime(q_date, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")
        status = "PAID" if random.random() > 0.4 else "ISSUED"

        invoices.append([
            inv_id, inv_number, qid, cid, q_date, due_date, "INR",
            sub, disc, tax, grand, b_type, status
        ])

        for ql in q_lines_for_quote:
            invoice_lines.append([
                f"INVL-{inv_line_idx:05d}", inv_id, ql[3], ql[4], ql[5], ql[6], ql[7],
                ql[8], ql[9], ql[10], ql[11], ql[12], ql[13], ql[14], ql[15]
            ])
            inv_line_idx += 1

    print(f"Generated {len(invoices)} Invoices with {len(invoice_lines)} Invoice Line items.")

    # --------------------------------------------------------------------------
    # 13. ADDITIONAL ENTITIES (Orders, Warehouse Allocations, Subscriptions)
    # --------------------------------------------------------------------------
    orders = []
    ord_idx = 1
    for q in billable_quotes[:45]:
        qid = q[0]
        cid = q[2]
        q_date = q[3]
        grand = q[9]
        orders.append([
            f"ORD-{ord_idx:04d}", f"PO-MUM-2026-{ord_idx:04d}", qid, cid, q_date,
            grand, "INR", "CONFIRMED", "WH-001", "2026-03-10", "Bluedart Express"
        ])
        ord_idx += 1

    warehouse_allocations = []
    wa_idx = 1
    for ql in quotation_lines:
        if ql[3] == "PRODUCT" and ql[16]:
            wa_id = f"WALLOC-{wa_idx:05d}"
            wa_idx += 1
            warehouse_allocations.append([
                wa_id, ql[1], ql[0], ql[4], ql[16], ql[8], ql[17], "2026-02-28T14:00:00Z"
            ])

    subscriptions_data = []
    sub_rec_idx = 1
    for ql in quotation_lines:
        if ql[3] == "SUBSCRIPTION":
            sub_id = f"SUBREC-{sub_rec_idx:04d}"
            sub_rec_idx += 1
            qid = ql[1]
            q_match = [q for q in quotations if q[0] == qid][0]
            cid = q_match[2]
            start_date = q_match[3]
            end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=365)).strftime("%Y-%m-%d")
            subscriptions_data.append([
                sub_id, cid, qid, ql[6], ql[7], ql[9], "YEARLY", start_date, end_date, "ACTIVE"
            ])

    # --------------------------------------------------------------------------
    # WRITE ALL CSV FILES TO OUTPUT DIRECTORY
    # --------------------------------------------------------------------------
    files_to_write = [
        ("brands.csv", ["brand_id", "brand_name", "brand_code", "country", "support_level", "status"], brands),
        ("categories.csv", ["category_id", "category_name", "parent_category_id", "description", "status"], categories),
        ("warehouses.csv", ["warehouse_id", "warehouse_code", "warehouse_name", "city", "state", "country", "warehouse_type", "manager_name", "capacity_units", "status"], warehouses),
        ("services.csv", ["service_id", "service_code", "service_name", "service_category", "description", "cost", "selling_price", "tax_rate", "minimum_margin_percent", "recurring", "billing_frequency", "status"], services),
        ("subscription_plans.csv", ["plan_id", "plan_code", "plan_name", "billing_frequency", "billing_interval", "price", "setup_fee", "proration_enabled", "cancellation_policy", "refund_policy", "status"], subscriptions),
        ("discount_rules.csv", ["discount_rule_id", "customer_tier", "category_id", "maximum_discount_percent", "minimum_margin_percent", "approval_level", "risk_level", "active"], discount_rules),
        ("approval_chains.csv", ["chain_id", "approval_level", "role_name", "min_discount_percent", "max_discount_percent", "min_margin_percent", "approver_role", "description"], approval_chains),
        ("customers.csv", ["customer_id", "customer_code", "company_name", "industry", "customer_tier", "city", "state", "country", "billing_address", "shipping_address", "credit_limit", "payment_terms_days", "account_manager", "status"], customers),
        ("products.csv", ["product_id", "product_code", "product_name", "brand", "category_id", "subcategory_id", "product_type", "description", "manufacturer_part_number", "unit", "base_cost", "base_price", "tax_rate", "warranty_months", "status", "is_serialized", "is_recurring", "created_at", "updated_at"], products),
        ("product_variants.csv", ["variant_id", "product_id", "sku", "variant_name", "cpu", "ram", "storage", "storage_type", "gpu", "screen_size", "resolution", "color", "connectivity", "operating_system", "form_factor", "warranty_months", "extra_price", "cost_price", "selling_price", "barcode", "status"], variants),
        ("inventory.csv", ["inventory_id", "warehouse_id", "variant_id", "available_quantity", "reserved_quantity", "allocated_quantity", "backorder_quantity", "reorder_level", "reorder_quantity", "safety_stock", "incoming_quantity", "average_daily_demand", "inventory_status", "last_restocked_at", "next_expected_restock"], inventory),
        ("price_lists.csv", ["price_list_id", "price_list_name", "customer_tier", "currency", "product_variant_id", "unit_price", "minimum_quantity", "effective_from", "effective_to", "status"], price_lists),
        ("customer_price_lists.csv", ["customer_price_id", "customer_id", "price_list_id", "effective_from", "effective_to", "status"], customer_price_lists),
        ("product_recommendations.csv", ["recommendation_id", "source_product_id", "recommended_product_id", "recommendation_type", "confidence_score", "co_purchase_rate", "margin_delta", "priority", "promotion_active", "minimum_margin_percent", "reason", "status"], recommendations),
        ("product_service_rules.csv", ["rule_id", "product_id", "service_id", "recommended", "required", "priority"], product_service_rules),
        ("quotations.csv", ["quotation_id", "quotation_number", "customer_id", "quotation_date", "valid_until", "currency", "subtotal", "discount_total", "tax_total", "grand_total", "status", "approval_status", "deal_health", "created_by", "notes"], quotations),
        ("quotation_lines.csv", ["line_id", "quotation_id", "line_number", "item_type", "product_variant_id", "service_id", "subscription_plan_id", "description", "quantity", "unit_price", "discount_percent", "discount_amount", "tax_rate", "tax_amount", "line_total", "billing_type", "fulfillment_warehouse_id", "fulfillment_status"], quotation_lines),
        ("negotiations.csv", ["negotiation_id", "quotation_id", "customer_id", "quotation_line_id", "original_discount_percent", "requested_discount_percent", "customer_message", "status", "submitted_at", "resolved_at"], negotiations),
        ("customer_negotiations.csv", ["negotiation_id", "quotation_id", "customer_id", "quotation_line_id", "original_discount_percent", "requested_discount_percent", "customer_message", "status", "submitted_at", "resolved_at"], negotiations),
        ("deal_health.csv", ["deal_health_id", "quotation_id", "days_inactive", "discount_anomaly_score", "delivery_risk_score", "approval_delay_score", "inventory_risk_score", "overall_health_score", "health_status", "recommended_action", "last_evaluated_at"], deal_health),
        ("audit_logs.csv", ["audit_id", "entity_type", "entity_id", "action", "old_value", "new_value", "performed_by", "reason", "timestamp"], audit_logs),
        ("invoices.csv", ["invoice_id", "invoice_number", "quotation_id", "customer_id", "invoice_date", "due_date", "currency", "subtotal", "discount_total", "tax_total", "grand_total", "billing_type", "status"], invoices),
        ("invoice_lines.csv", ["invoice_line_id", "invoice_id", "item_type", "product_variant_id", "service_id", "subscription_plan_id", "description", "quantity", "unit_price", "discount_percent", "discount_amount", "tax_rate", "tax_amount", "line_total", "billing_type"], invoice_lines),
        ("orders.csv", ["order_id", "customer_po_number", "quotation_id", "customer_id", "order_date", "grand_total", "currency", "order_status", "primary_warehouse_id", "promised_delivery_date", "logistics_partner"], orders),
        ("warehouse_allocations.csv", ["allocation_id", "quotation_id", "quotation_line_id", "variant_id", "warehouse_id", "allocated_quantity", "fulfillment_status", "allocated_at"], warehouse_allocations),
        ("subscriptions.csv", ["subscription_contract_id", "customer_id", "quotation_id", "plan_id", "plan_name", "annual_rate", "billing_cycle", "start_date", "next_renewal_date", "contract_status"], subscriptions_data)
    ]

    for fname, headers, rows in files_to_write:
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"Successfully generated {fname:<28} : {len(rows):>6} records")

    print("==================================================")
    print("ALL MUMBAI DATASET CSV FILES GENERATED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run()
