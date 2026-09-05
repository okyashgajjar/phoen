"""
DealFlow360 Master Seed Data Builder — Bangalore Edition
Orchestrates generation of all 21 CSV files for Bangalore Enterprise Technology Distribution Center (BLR-DC-01)
Guarantees 100% relational integrity, authentic pricing, varied inventory, and scenario coverage.
"""

import os
import sys
import csv
import random
from datetime import datetime, timedelta

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import build_base_blr
import build_catalog_blr

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

def run():
    print("==================================================")
    print("DEALFLOW360 BANGALORE SEED DATA GENERATOR")
    print("==================================================")

    # 1. Base entities
    brands = build_base_blr.BRANDS
    categories = build_base_blr.CATEGORIES
    warehouses = build_base_blr.WAREHOUSES
    services = build_base_blr.SERVICES
    subscriptions = build_base_blr.SUBSCRIPTION_PLANS
    discount_rules = build_base_blr.DISCOUNT_RULES
    customers = build_base_blr.CUSTOMERS_DATA

    # 2. Catalog (Products & Variants)
    products, base_variants = build_catalog_blr.generate_catalog()

    # Expand variants to ensure 520+ sellable SKUs
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
                vname = f"{ev[3].split(' / ')[0]} / 32GB / 1TB SSD / Win 11 Pro"
                extra = round(base_price * 0.22, 2)
                cost = round(base_cost + extra * 0.78, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], "32GB DDR5", "1TB", ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-WKS":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-128G-2TB"
                vname = f"{ev[3].split(' / ')[0]} / 128GB ECC / 2TB SSD / Dual GPU Ready"
                extra = round(base_price * 0.35, 2)
                cost = round(base_cost + extra * 0.78, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], "128GB DDR5 ECC", "2TB NVMe", ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SRV":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-2X-256G-8TB"
                vname = f"{ev[3].split(' / ')[0]} / 256GB ECC / 8x 1.92TB SSD / Redundant PSU"
                extra = round(base_price * 0.45, 2)
                cost = round(base_cost + extra * 0.80, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], "256GB DDR5 ECC RDIMM", "15.3TB (8x 1.92TB SAS SSD)", ev[7], ev[8], ev[9], ev[10],
                    ev[11], ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SMP":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-512G-SIL"
                vname = f"{ev[3].split(' / ')[0]} 512GB Titanium Silver 5G Enterprise"
                extra = round(base_price * 0.18, 2)
                cost = round(base_cost + extra * 0.85, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], "512GB", ev[7], ev[8], ev[9], ev[10],
                    "Silver Titanium", ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-TAB":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-256G-5G"
                vname = f"{ev[3].split(' / ')[0]} 256GB 5G Cellular Enterprise Edition"
                extra = round(base_price * 0.25, 2)
                cost = round(base_cost + extra * 0.80, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], "256GB", ev[7], ev[8], ev[9], ev[10],
                    ev[11], "5G Cellular + Wi-Fi 6E", ev[13], "Cellular Tablet", ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-MON":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-DUALARM"
                vname = f"{ev[3].split(' / ')[0]} with Premium Dual-Monitor Desk Arm Bundle"
                extra = 4500.0
                cost = round(base_cost + 3200.0, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, "", "", "", "", "", ev[9], ev[10],
                    ev[11], ev[12], "", "Monitor + Heavy Ergo Arm", ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-NET":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-DUALPSU"
                vname = f"{ev[3].split(' / ')[0]} with Dual Redundant Power Supplies (1+1 RPS)"
                extra = round(base_price * 0.20, 2)
                cost = round(base_cost + extra * 0.75, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, "", "", "", "", "", "", "",
                    ev[11], ev[12], ev[13], "1U Dual PSU Rackmount", ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-STO":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-64TB-RAID"
                vname = f"{ev[3].split(' / ')[0]} Populated with 64TB Enterprise Storage (4x 16TB)"
                extra = 104000.0
                cost = round(base_cost + 82000.0, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], "64TB Raw", "Enterprise SAS/SATA RAID6", "", "", "",
                    ev[11], "10GbE SFP+ / 2.5GbE", ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-UPS":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-EXTBATT"
                vname = f"{ev[3].split(' / ')[0]} bundled with External Extended Run Battery Pack (EBM)"
                extra = round(base_price * 0.50, 2)
                cost = round(base_cost + extra * 0.75, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, "", "", "", "", "", "", "",
                    ev[11], ev[12], "", "UPS + Extended Battery Module", ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-PRN":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-TRAY2"
                vname = f"{ev[3].split(' / ')[0]} with Additional 550-Sheet Paper Feeder Tray"
                extra = 12000.0
                cost = round(base_cost + 8500.0, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, "", "", "", "", "", "", "",
                    ev[11], ev[12], "", "Printer with 2nd Feeder Cassette", ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-ACC":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-WHT"
                vname = f"{ev[3].split(' / ')[0]} - Arctic White / Silver Edition"
                extra = 500.0
                cost = round(base_cost + 350.0, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, "", "", "", "", "", "", "",
                    "Arctic White", ev[12], "", ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-COL":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-MICPOD"
                vname = f"{ev[3].split(' / ')[0]} bundled with Additional Table Microphone Pod"
                extra = 28000.0
                cost = round(base_cost + 21000.0, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, "", "", "", "", "", "", ev[10],
                    ev[11], ev[12], ev[13], "Video Bar + Expansion Mic Pod", ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SEC":
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-5M"
                vname = f"{ev[3].split(' / ')[0]} (5-Meter Extended Reach)"
                extra = 1800.0
                cost = round(base_cost + 1100.0, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, "", "", "", "", "", "", "",
                    ev[11], ev[12], "", ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907200{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

    print(f"Final Products Count: {len(products)}")
    print(f"Final Sellable Variants Count: {len(variants)}")

    var_dict = {v[0]: v for v in variants}
    sku_to_vid = {v[2]: v[0] for v in variants}
    prod_dict = {p[0]: p for p in products}

    # Identify special target variants for Bangalore demo scenarios
    var_lap_5440 = sku_to_vid.get("LAP-DEL-LAT-5440-U5-16-512", variants[0][0])
    var_dock_wd19s = sku_to_vid.get("VAR-ACC-DEL-WD19S-01", variants[80][0])
    var_mon_p2422h = sku_to_vid.get("MON-DEL-P2422H-BASE", variants[67][0])
    var_net_c9200l = sku_to_vid.get("NET-CIS-C9200L-24P-4G", variants[48][0])
    var_net_ap515 = sku_to_vid.get("NET-ARU-AP515-STANDALONE", variants[55][0])
    var_srv_r660 = sku_to_vid.get("SRV-DEL-R660-1X-64G-1.92T", variants[26][0])

    # Scenario 2 Smartphone target: Galaxy S24 & iPhone 15 Pro
    var_phn_s24 = sku_to_vid.get("PHN-SAM-S24-128-BLK", variants[37][0])
    var_phn_ip15p = sku_to_vid.get("PHN-APL-IP15P-128-BLK", variants[32][0])
    var_chg_anker = sku_to_vid.get("VAR-ACC-ANK-GAN120-01", variants[93][0])

    # Scenario 3 Server Fulfillment target: Dell PowerEdge R760
    var_srv_r760 = sku_to_vid.get("SRV-DEL-R760-2X-128G-7.68T", variants[27][0])

    # Scenario 4 Multi-warehouse target: ThinkPad T14 Gen 4
    var_lap_t14 = sku_to_vid.get("LAP-LEN-T14-I5-16-512", variants[4][0])

    # --------------------------------------------------------------------------
    # 3. INVENTORY (Warehouse Inventory Records) - Target: 1,000+ records
    # --------------------------------------------------------------------------
    # Primary: WH-001 (BLR-DC-01) - Bangalore Central
    # Supporting: WH-002 (AMD-DC-01), WH-003 (MUM-DC-01), WH-004 (DEL-DC-01), WH-005 (HYD-DC-01)
    inventory = []
    inv_idx = 1

    # Populate Bangalore Central (WH-001) for all variants
    for v in variants:
        vid = v[0]
        pid = v[1]
        p_obj = prod_dict[pid]
        subcat = p_obj[5]

        # Specific demo scenario configurations for Bangalore
        if vid == var_srv_r760:
            # Scenario 3 requirement: Customer requires 12. Bangalore has 7 available, 3 incoming, 2 backordered!
            avail = 7
            res = 7
            alloc = 7
            backorder = 2
            reorder_lvl = 6
            reorder_qty = 15
            safety = 3
            incoming = 3
            avg_demand = 1.2
            status = "BACKORDER"
        elif vid == var_lap_t14:
            # Scenario 4 requirement: Customer requests 150. Bangalore has 100 available.
            avail = 100
            res = 100
            alloc = 100
            backorder = 0
            reorder_lvl = 40
            reorder_qty = 120
            safety = 25
            incoming = 50
            avg_demand = 8.0
            status = "IN_STOCK"
        elif vid == var_lap_5440:
            # Scenario 1 fleet refresh
            avail = 250
            res = 200
            alloc = 200
            backorder = 0
            reorder_lvl = 50
            reorder_qty = 200
            safety = 30
            incoming = 100
            avg_demand = 15.0
            status = "IN_STOCK"
        elif vid == var_dock_wd19s:
            avail = 380
            res = 200
            alloc = 200
            backorder = 0
            reorder_lvl = 60
            reorder_qty = 250
            safety = 40
            incoming = 150
            avg_demand = 22.0
            status = "IN_STOCK"
        elif vid == var_mon_p2422h:
            avail = 320
            res = 200
            alloc = 200
            backorder = 0
            reorder_lvl = 50
            reorder_qty = 200
            safety = 35
            incoming = 100
            avg_demand = 18.0
            status = "IN_STOCK"
        elif vid == var_phn_s24:
            # Scenario 2 target
            avail = 85
            res = 50
            alloc = 50
            backorder = 0
            reorder_lvl = 20
            reorder_qty = 60
            safety = 12
            incoming = 40
            avg_demand = 4.5
            status = "IN_STOCK"
        elif subcat == "CAT-SRV":
            # High-end servers: 1 - 15 units
            avail = random.randint(1, 14)
            res = random.randint(0, min(avail, 3))
            alloc = res
            backorder = random.choice([0, 0, 0, 1, 3])
            reorder_lvl = 4
            reorder_qty = 10
            safety = 2
            incoming = random.choice([0, 4, 8])
            avg_demand = round(random.uniform(0.2, 1.2), 1)
            status = "LOW_STOCK" if avail <= 3 else "IN_STOCK"
        elif subcat == "CAT-WKS":
            # Workstations: 2 - 20 units
            avail = random.randint(2, 18)
            res = random.randint(0, min(avail, 4))
            alloc = res
            backorder = 0
            reorder_lvl = 5
            reorder_qty = 12
            safety = 3
            incoming = random.choice([0, 5, 10])
            avg_demand = round(random.uniform(0.6, 2.5), 1)
            status = "LOW_STOCK" if avail <= 4 else "IN_STOCK"
        elif subcat in ["CAT-LAP", "CAT-DSK"]:
            # Laptops & Desktops: 10 - 150 units
            avail = random.randint(25, 145)
            res = random.randint(5, 30)
            alloc = res
            backorder = 0
            reorder_lvl = 30
            reorder_qty = 60
            safety = 15
            incoming = random.choice([20, 40, 60])
            avg_demand = round(random.uniform(4.0, 12.0), 1)
            status = "IN_STOCK"
        elif subcat in ["CAT-SMP", "CAT-TAB"]:
            # Mobility: 5 - 100 units
            avail = random.randint(10, 85)
            res = random.randint(2, 20)
            alloc = res
            backorder = 0
            reorder_lvl = 18
            reorder_qty = 45
            safety = 10
            incoming = random.choice([15, 35])
            avg_demand = round(random.uniform(2.0, 7.5), 1)
            status = "IN_STOCK"
        elif subcat == "CAT-NET":
            # Networking: 5 - 50 units
            avail = random.randint(5, 45)
            res = random.randint(1, 8)
            alloc = res
            backorder = 0
            reorder_lvl = 10
            reorder_qty = 25
            safety = 5
            incoming = random.choice([10, 20])
            avg_demand = round(random.uniform(1.0, 4.5), 1)
            status = "LOW_STOCK" if avail <= 6 else "IN_STOCK"
        elif subcat == "CAT-ACC":
            # Accessories: 50 - 500+ units
            avail = random.randint(80, 480)
            res = random.randint(15, 60)
            alloc = res
            backorder = 0
            reorder_lvl = 60
            reorder_qty = 180
            safety = 40
            incoming = random.choice([50, 150, 250])
            avg_demand = round(random.uniform(10.0, 40.0), 1)
            status = "IN_STOCK"
        else:
            # Monitors, Printers, Storage, UPS: 10 - 100 units
            avail = random.randint(12, 85)
            res = random.randint(2, 15)
            alloc = res
            backorder = 0
            reorder_lvl = 15
            reorder_qty = 35
            safety = 8
            incoming = random.choice([15, 30])
            avg_demand = round(random.uniform(1.5, 6.0), 1)
            status = "LOW_STOCK" if avail <= 12 else "IN_STOCK"

        # Inject realistic stock health variations
        if inv_idx in [19, 43, 91, 155, 230]:
            avail = 0
            status = "OUT_OF_STOCK"
        elif inv_idx in [27, 73, 118, 184, 275]:
            status = "REPLENISHMENT_REQUIRED"

        inv_id = f"INV-{inv_idx:05d}"
        inv_idx += 1
        last_restocked = "2026-02-15T09:30:00Z"
        next_restock = "2026-03-20T14:00:00Z"
        inventory.append([
            inv_id, "WH-001", vid, avail, res, alloc, backorder,
            reorder_lvl, reorder_qty, safety, incoming, avg_demand,
            status, last_restocked, next_restock
        ])

    # Multi-warehouse allocation records:
    # Scenario 4: Mumbai (WH-003 / MUM-DC-01) has 50 units of ThinkPad T14 Gen 4
    inv_id = f"INV-{inv_idx:05d}"
    inv_idx += 1
    inventory.append([
        inv_id, "WH-003", var_lap_t14, 50, 50, 50, 0,
        25, 60, 15, 30, 6.0, "IN_STOCK", "2026-02-18T11:00:00Z", "2026-03-25T11:00:00Z"
    ])

    # Populate 120-150 regional warehouse records per hub to demonstrate distributed enterprise inventory
    # and guarantee 1,000+ total inventory records
    regional_wh_list = ["WH-002", "WH-003", "WH-004", "WH-005"]
    sampled_for_regional = variants[:135] # top 135 fast-moving enterprise hardware models
    for mvid in [v[0] for v in sampled_for_regional]:
        for wh in regional_wh_list:
            if mvid == var_lap_t14 and wh == "WH-003":
                continue # already created above
            inv_id = f"INV-{inv_idx:05d}"
            inv_idx += 1
            r_avail = random.randint(15, 65)
            r_res = random.randint(2, 12)
            inventory.append([
                inv_id, wh, mvid, r_avail, r_res, r_res, 0,
                15, 40, 10, 20, round(random.uniform(1.0, 5.0), 1),
                "IN_STOCK", "2026-02-12T10:00:00Z", "2026-03-22T10:00:00Z"
            ])

    print(f"Generated {len(inventory)} Inventory records across 5 distribution centers (Primary: BLR-DC-01).")

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
                elif subcat in ["CAT-SRV", "CAT-WKS"]:
                    tier_disc = discount_factor * 0.90
                else:
                    tier_disc = discount_factor
                calculated_price = round(std_price * (1.0 - tier_disc), 2)
                # Ensure negotiated price is never below cost
                unit_price = max(calculated_price, round(cost_price * 1.04, 2))

            pl_row = [
                pl_code, pl_name, tier, "INR", vid,
                f"{unit_price:.2f}", min_qty, "2026-01-01", "2026-12-31", "ACTIVE"
            ]
            price_lists.append(pl_row)

    print(f"Generated {len(price_lists)} Price List line records ({len(tiers)} tiers x {len(variants)} variants).")

    # --------------------------------------------------------------------------
    # 5. CUSTOMER PRICE LIST ASSIGNMENTS
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
    # 6. PRODUCT RECOMMENDATIONS (Upsell / Cross-Sell Rules) - Target: 250+
    # --------------------------------------------------------------------------
    recommendations = []
    rec_idx = 1

    dock_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Dock" in p[2]]
    monitor_prods = [p[0] for p in products if p[5] == "CAT-MON"]
    bag_prods = [p[0] for p in products if p[5] == "CAT-ACC" and ("Backpack" in p[2] or "Briefcase" in p[2])]
    mouse_prods = [p[0] for p in products if p[5] == "CAT-ACC" and ("Mouse" in p[2] or "Combo" in p[2] or "Keyboard" in p[2])]
    headset_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Headset" in p[2]]
    ups_prods = [p[0] for p in products if p[5] == "CAT-UPS"]
    rack_acc_prods = [p[0] for p in products if p[5] == "CAT-SEC" and ("Rail" in p[2] or "PDU" in p[2] or "Rack" in p[2])]
    optics_prods = [p[0] for p in products if p[5] == "CAT-SEC" and ("SFP" in p[2] or "DAC" in p[2] or "Optical" in p[2])]
    cable_prods = [p[0] for p in products if p[5] == "CAT-SEC" and ("Patch" in p[2] or "Cable" in p[2])]
    chargers = [c[0] for c in products if c[5] == "CAT-ACC" and ("Charger" in c[2] or "Adapter" in c[2])]
    switch_prods = [p[0] for p in products if p[5] == "CAT-NET" and "Switch" in p[2]]

    for p in products:
        pid = p[0]
        subcat = p[5]

        if subcat == "CAT-LAP":
            if dock_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(dock_prods), "CROSS_SELL", 0.92, 0.82, 8.5, 1, True, 20.0,
                    "Frequently purchased with corporate laptops to enable multi-display workstation connectivity", "ACTIVE"
                ])
                rec_idx += 1
            if monitor_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(monitor_prods), "ATTACHMENT", 0.88, 0.74, 6.2, 2, True, 18.0,
                    "Recommended dual-display pairing for software development productivity enhancement", "ACTIVE"
                ])
                rec_idx += 1
            if headset_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(headset_prods), "ATTACHMENT", 0.85, 0.69, 9.5, 3, True, 22.0,
                    "Essential noise-cancelling headset for open-office and hybrid remote communication", "ACTIVE"
                ])
                rec_idx += 1
            if bag_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(bag_prods), "ATTACHMENT", 0.94, 0.88, 14.0, 4, True, 25.0,
                    "Durable business travel backpack protects mobile workstation assets during Bangalore transit", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-WKS":
            hi_res_monitors = [m for m in monitor_prods if "4K" in prod_dict[m][2] or "U27" in prod_dict[m][1] or "PD" in prod_dict[m][1]]
            if hi_res_monitors:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(hi_res_monitors), "UPSELL", 0.95, 0.88, 9.4, 1, True, 22.0,
                    "Factory color-calibrated display essential for CAD, 3D visualization, and ML simulation", "ACTIVE"
                ])
                rec_idx += 1
            if ups_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(ups_prods), "ATTACHMENT", 0.91, 0.75, 8.0, 2, True, 18.0,
                    "Pure sine-wave power backup protects high-value compute workstations against brownouts", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-SRV":
            rack_ups = [u for u in ups_prods if "RT" in prod_dict[u][1] or "SRT" in prod_dict[u][1] or "9PX" in prod_dict[u][1]]
            if rack_ups:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(rack_ups), "ATTACHMENT", 0.96, 0.90, 8.5, 1, True, 18.0,
                    "Mission-critical online double-conversion power required for enterprise server SLA compliance", "ACTIVE"
                ])
                rec_idx += 1
            if rack_acc_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(rack_acc_prods), "ATTACHMENT", 0.98, 0.93, 14.0, 2, True, 25.0,
                    "Toolless sliding rail kit and cable arm required for mounting in standard 19-inch racks", "ACTIVE"
                ])
                rec_idx += 1
            if optics_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(optics_prods), "CROSS_SELL", 0.89, 0.79, 15.0, 3, True, 25.0,
                    "High-speed 10G/25G optical transceiver for top-of-rack leaf-spine switch uplinks", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-DSK":
            if monitor_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(monitor_prods), "ATTACHMENT", 0.92, 0.85, 8.0, 1, True, 20.0,
                    "Dual desktop displays significantly expand operational workspace for productivity", "ACTIVE"
                ])
                rec_idx += 1
            if mouse_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(mouse_prods), "CROSS_SELL", 0.94, 0.89, 12.0, 2, True, 25.0,
                    "Commercial wireless keyboard and mouse combo with quiet keys and long battery life", "ACTIVE"
                ])
                rec_idx += 1
            if ups_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(ups_prods), "ATTACHMENT", 0.89, 0.78, 10.5, 3, True, 20.0,
                    "Line-interactive desktop UPS provides uninterrupted clean power during campus grid spikes", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-NET":
            if optics_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(optics_prods), "ATTACHMENT", 0.96, 0.91, 18.0, 1, True, 30.0,
                    "Certified SFP+ optical transceiver or DAC cable for core distribution interconnect", "ACTIVE"
                ])
                rec_idx += 1
            if cable_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(cable_prods), "CROSS_SELL", 0.93, 0.86, 22.0, 2, True, 35.0,
                    "Snagless 10-Gigabit certified patch cords for high-density patch panel patching", "ACTIVE"
                ])
                rec_idx += 1
            if ups_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(ups_prods), "ATTACHMENT", 0.90, 0.78, 10.0, 3, True, 20.0,
                    "Rackmount power backup prevents network downtime and packet loss during power fluctuations", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-STO":
            if rack_acc_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(rack_acc_prods), "ATTACHMENT", 0.95, 0.88, 12.0, 1, True, 22.0,
                    "Enterprise sliding rail kit engineered for heavy SAN/NAS storage chassis installations", "ACTIVE"
                ])
                rec_idx += 1
            if optics_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(optics_prods), "CROSS_SELL", 0.91, 0.83, 16.0, 2, True, 25.0,
                    "Short-wave 16Gb/32Gb Fibre Channel optical transceivers for low-latency SAN fabric", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-SEC":
            if optics_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(optics_prods), "ATTACHMENT", 0.94, 0.87, 14.5, 1, True, 25.0,
                    "Certified 10G SFP+ optical transceivers for wire-speed perimeter firewall inspection ports", "ACTIVE"
                ])
                rec_idx += 1
            if cable_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(cable_prods), "CROSS_SELL", 0.91, 0.82, 19.0, 2, True, 30.0,
                    "Category 6A shielded patch cabling ensures interference-free security appliance uplinks", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-MON":
            if dock_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(dock_prods), "CROSS_SELL", 0.88, 0.78, 10.0, 1, True, 20.0,
                    "Thunderbolt/USB-C docking hub connects monitor, ethernet, and high-wattage charging", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-SMP":
            if chargers:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(chargers), "CROSS_SELL", 0.92, 0.84, 16.5, 1, True, 25.0,
                    "120W multi-device fast charger simultaneously powers executive smartphone and laptop", "ACTIVE"
                ])
                rec_idx += 1
            if headset_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(headset_prods), "ATTACHMENT", 0.87, 0.75, 12.0, 2, True, 22.0,
                    "Enterprise wireless bluetooth headset for mobile executive communications", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-TAB":
            if chargers:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(chargers), "CROSS_SELL", 0.88, 0.80, 15.0, 1, True, 25.0,
                    "Fast USB-C wall charger supports quick turnaround for field service workforce", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-PRN":
            if cable_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, cable_prods[0], "ATTACHMENT", 0.86, 0.74, 20.0, 1, True, 30.0,
                    "Shielded Gigabit Ethernet cabling ensures uninterrupted network print queue flow", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-COL":
            if monitor_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(monitor_prods), "ATTACHMENT", 0.91, 0.82, 10.0, 1, True, 20.0,
                    "Large format commercial display completes the meeting room video conference setup", "ACTIVE"
                ])
                rec_idx += 1

    print(f"Generated {len(recommendations)} Product Recommendations (Upsell, Cross-Sell, Attachment).")

    # --------------------------------------------------------------------------
    # 7. PRODUCT SERVICE RULES
    # --------------------------------------------------------------------------
    product_service_rules = []
    psr_idx = 1

    for p in products:
        pid = p[0]
        subcat = p[5]

        if subcat == "CAT-SRV":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-001", True, False, 1])
            psr_idx += 1
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-002", True, False, 2])
            psr_idx += 1
        elif subcat == "CAT-NET":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-003", True, False, 1])
            psr_idx += 1
            if "Firewall" in p[2] or "FG" in p[1]:
                product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-004", True, True, 1])
                psr_idx += 1
            if "Access Point" in p[2] or "AP" in p[1]:
                product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-007", True, False, 2])
                psr_idx += 1
        elif subcat in ["CAT-LAP", "CAT-DSK"]:
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-005", True, False, 1])
            psr_idx += 1
        elif subcat == "CAT-STO":
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-006", True, False, 1])
            psr_idx += 1
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-011", True, False, 2])
            psr_idx += 1

    print(f"Generated {len(product_service_rules)} Product-Service Attachment Rules.")

    # --------------------------------------------------------------------------
    # 8. QUOTATIONS & QUOTATION LINES (Target: 75+ Quotations)
    # --------------------------------------------------------------------------
    quotations = []
    quotation_lines = []
    q_idx = 1
    ql_idx = 1

    def create_quotation(q_num, cust_id, q_date, valid_days, lines_spec, status="Draft", approval_status="Not Required", deal_health="Healthy", notes=""):
        nonlocal q_idx, ql_idx
        qid = f"QT-{q_idx:04d}"
        q_idx += 1

        date_obj = datetime.strptime(q_date, "%Y-%m-%d")
        valid_until = (date_obj + timedelta(days=valid_days)).strftime("%Y-%m-%d")

        subtotal = 0.0
        disc_total = 0.0
        tax_total = 0.0
        grand_total = 0.0

        q_lines = []
        for line_no, spec in enumerate(lines_spec, start=1):
            line_id = f"QL-{ql_idx:05d}"
            ql_idx += 1

            itype = spec["item_type"]
            qty = spec["qty"]
            price = spec["unit_price"]
            disc_pct = spec.get("discount_pct", 0.0)
            tax_rate = spec.get("tax_rate", 18.0)
            wh_id = spec.get("wh_id", "WH-001")
            ff_status = spec.get("fulfillment_status", "ALLOCATED")
            btype = spec.get("billing_type", "ONE_TIME")

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
            qid, q_num, cust_id, q_date, valid_until, "INR",
            f"{subtotal:.2f}", f"{disc_total:.2f}", f"{tax_total:.2f}", f"{grand_total:.2f}",
            status, approval_status, deal_health, "Kavita Sharma", notes
        ]
        quotations.append(q_row)
        quotation_lines.extend(q_lines)

    # --------------------------------------------------------------------------
    # SPECIAL BANGALORE DEMO SCENARIOS
    # --------------------------------------------------------------------------

    # Demo Scenario 1 (Section 33): Large Bangalore IT Procurement
    # Fictional large customer: VertexGrid Technologies Pvt Ltd (CUST-001)
    # 200 Business Laptops, 200 Docks, 200 Monitors, 20 Switches, 10 APs, 4 Servers, Installation, 3-Year AMC
    # Discount applied on Laptops: 24.0% (exceeds Enterprise Hardware allowed ceiling of 15.0%) -> HIGH RISK -> Dual Approval Required
    p_lap_price = float(var_dict[var_lap_5440][18])
    p_dock_price = float(var_dict[var_dock_wd19s][18])
    p_mon_price = float(var_dict[var_mon_p2422h][18])
    p_sw_price = float(var_dict[var_net_c9200l][18])
    p_ap_price = float(var_dict[var_net_ap515][18])
    p_srv_price = float(var_dict[var_srv_r660][18])

    create_quotation(
        "QT-2026-0001", "CUST-001", "2026-02-28", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_5440, "description": var_dict[var_lap_5440][3], "qty": 200, "unit_price": p_lap_price, "discount_pct": 24.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_dock_wd19s, "description": var_dict[var_dock_wd19s][3], "qty": 200, "unit_price": p_dock_price, "discount_pct": 18.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_mon_p2422h, "description": var_dict[var_mon_p2422h][3], "qty": 200, "unit_price": p_mon_price, "discount_pct": 15.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_net_c9200l, "description": var_dict[var_net_c9200l][3], "qty": 20, "unit_price": p_sw_price, "discount_pct": 16.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_net_ap515, "description": var_dict[var_net_ap515][3], "qty": 10, "unit_price": p_ap_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_srv_r660, "description": var_dict[var_srv_r660][3], "qty": 4, "unit_price": p_srv_price, "discount_pct": 14.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise Laptop Zero-Touch Imaging & Domain Join", "qty": 200, "unit_price": 1200.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"},
            {"item_type": "SUBSCRIPTION", "subscription_id": "SUB-001", "description": "Comprehensive Enterprise AMC (4hr SLA) - 3-Year Coverage", "qty": 3, "unit_price": 48000.0, "discount_pct": 0.0, "billing_type": "RECURRING", "fulfillment_status": "PENDING"}
        ],
        status="Pending Approval", approval_status="Pending Sales Manager & Finance Approval", deal_health="Critical",
        notes="Demo Scenario 1: Bangalore Mega Tech Refresh for VertexGrid Technologies. 24.0% requested discount on laptops breaches 15.0% threshold. Status: HIGH RISK. Requires Sales Manager and Finance VP signoff."
    )

    # Demo Scenario 2 (Section 34): Smartphone Procurement + MDM Upsell
    # Customer: Bengaluru Cloud Systems Pvt Ltd (CUST-002)
    # 50 Enterprise Smartphones, 50 Charging Accessories, 50 Protective Cases, Enterprise Device Management
    p_phn_price = float(var_dict[var_phn_s24][18])
    p_chg_price = float(var_dict[var_chg_anker][18])
    create_quotation(
        "QT-2026-0002", "CUST-002", "2026-02-26", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_phn_s24, "description": var_dict[var_phn_s24][3], "qty": 50, "unit_price": p_phn_price, "discount_pct": 8.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_chg_anker, "description": var_dict[var_chg_anker][3], "qty": 50, "unit_price": p_chg_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SUBSCRIPTION", "subscription_id": "SUB-006", "description": "Cloud Endpoint Mobility Management (Per Seat) - Annual MDM", "qty": 50, "unit_price": 2400.0, "discount_pct": 0.0, "billing_type": "RECURRING", "fulfillment_status": "PENDING"}
        ],
        status="Approved", approval_status="Approved", deal_health="Healthy",
        notes="Demo Scenario 2: Bangalore Smartphone Procurement. 50x Galaxy S24 with GaN fast chargers and Enterprise Cloud Mobility Management (MDM) recurring subscription attached."
    )

    # Demo Scenario 3 (Section 35): Server Fulfillment / Backorder
    # Customer: BlueOrbit FinTech Solutions Ltd (CUST-003)
    # Requires 12 PowerEdge R760 servers. Bangalore DC has 7 available, 3 incoming, 2 backordered.
    p_r760_price = float(var_dict[var_srv_r760][18])
    create_quotation(
        "QT-2026-0003", "CUST-003", "2026-02-22", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (Bangalore DC Immediate Stock)", "qty": 7, "unit_price": p_r760_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (Incoming Shipment Allocation - ETA 5 Days)", "qty": 3, "unit_price": p_r760_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "INCOMING_ALLOCATION", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": f"{var_dict[var_srv_r760][3]} (Factory Backorder - Lead Time 3 Weeks)", "qty": 2, "unit_price": p_r760_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "BACKORDERED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-001", "description": "Enterprise Server & Rack Installation", "qty": 12, "unit_price": 7500.0, "discount_pct": 5.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Confirmed", approval_status="Approved", deal_health="Watch",
        notes="Demo Scenario 3: Server Fulfillment & Backorder. Order for 12x PowerEdge R760. 7 allocated immediately from Bangalore DC, 3 allocated from incoming transit, and 2 routed to factory backorder."
    )

    # Demo Scenario 4 (Section 36): Multi-Warehouse Allocation Split
    # Customer: QuantumForge Technologies (CUST-004)
    # Requires 150 ThinkPad T14 Gen 4 laptops. Bangalore fulfills 100, Mumbai fulfills 50.
    p_t14_price = float(var_dict[var_lap_t14][18])
    create_quotation(
        "QT-2026-0004", "CUST-004", "2026-02-25", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_t14, "description": f"{var_dict[var_lap_t14][3]} (Fulfillment: Bangalore Central BLR-DC-01)", "qty": 100, "unit_price": p_t14_price, "discount_pct": 11.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_lap_t14, "description": f"{var_dict[var_lap_t14][3]} (Fulfillment: Mumbai Hub Split MUM-DC-01)", "qty": 50, "unit_price": p_t14_price, "discount_pct": 11.0, "wh_id": "WH-003", "fulfillment_status": "PARTIAL_SPLIT", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise Laptop Zero-Touch Imaging", "qty": 150, "unit_price": 1200.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Approved", approval_status="Approved", deal_health="Healthy",
        notes="Demo Scenario 4: Multi-Warehouse Split. 150 laptops procured: 100 units fulfilled from Bangalore primary distribution center (BLR-DC-01) and 50 units fulfilled from Mumbai logistics hub (MUM-DC-01)."
    )

    # Demo Scenario 5 (Section 37): Customer Counter-Offer / Negotiation
    # Customer: SiliconArc Systems (CUST-005) requests 19.0% discount (breaching threshold)
    p_mac_price = float(var_dict[sku_to_vid.get("LAP-APL-MBP14-M3P-18-512-SBLK", variants[10][0])][18])
    create_quotation(
        "QT-2026-0005", "CUST-005", "2026-02-18", 20,
        [
            {"item_type": "PRODUCT", "variant_id": sku_to_vid.get("LAP-APL-MBP14-M3P-18-512-SBLK", variants[10][0]), "description": "MacBook Pro 14 M3 Pro Developer Laptops", "qty": 35, "unit_price": p_mac_price, "discount_pct": 19.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise macOS Gold Master Provisioning", "qty": 35, "unit_price": 1200.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Under Negotiation", approval_status="Pending Commercial Approval", deal_health="Watch",
        notes="Demo Scenario 5: Customer Negotiation in progress. Customer submitted counter-offer requesting 19.0% discount on Apple hardware (ceiling is 12.0%). Requires Commercial VP approval."
    )

    # Demo Scenario 6: Stalled Inactive Deal -> At Risk
    create_quotation(
        "QT-2026-0006", "CUST-012", "2026-01-10", 30,
        [
            {"item_type": "PRODUCT", "variant_id": variants[15][0], "description": variants[15][3], "qty": 25, "unit_price": float(variants[15][18]), "discount_pct": 6.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"}
        ],
        status="Sent", approval_status="Not Required", deal_health="At Risk",
        notes="Demo Scenario 6: Deal Health At Risk. Quotation delivered 48 days ago with zero client engagement since transmission."
    )

    # Demo Scenario 7: Discount Anomaly Flagged
    create_quotation(
        "QT-2026-0007", "CUST-015", "2026-02-27", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_net_c9200l, "description": var_dict[var_net_c9200l][3], "qty": 15, "unit_price": p_sw_price, "discount_pct": 27.5, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-003", "description": "L2/L3 Network & VLAN Setup", "qty": 1, "unit_price": 12000.0, "discount_pct": 15.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Pending Approval", approval_status="Flagged - Discount Anomaly", deal_health="Critical",
        notes="Demo Scenario 7: Discount Anomaly detected. 27.5% requested discount on Cisco Enterprise Networking exceeds historical peer median (6.5%) by 21.0%."
    )

    # Generate 73 more realistic operational quotations to reach 80 total
    quote_statuses = ["Draft", "Sent", "Under Negotiation", "Pending Approval", "Approved", "Rejected", "Confirmed", "Expired"]

    for i in range(8, 81):
        q_code = f"QT-2026-{i:04d}"
        cust = customers[(i - 1) % len(customers)]
        cust_id = cust[0]

        num_items = random.randint(2, 5)
        sampled_vars = random.sample(variants, num_items)
        lines_spec = []

        for sv in sampled_vars:
            qty = random.choice([2, 5, 10, 20, 30, 50, 75])
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

        # Controlled realistic status distribution ensuring 44 billable quotes for 40+ Invoices & 150+ Invoice Lines
        if i <= 48:
            status = "Approved" if (i % 2 == 0) else "Confirmed"
        elif i <= 58:
            status = "Sent"
        elif i <= 68:
            status = "Under Negotiation"
        elif i <= 74:
            status = "Pending Approval"
        elif i <= 77:
            status = "Draft"
        elif i <= 79:
            status = "Expired"
        else:
            status = "Rejected"

        app_status = "Approved" if status in ["Approved", "Confirmed"] else ("Pending Approval" if status == "Pending Approval" else "Not Required")
        d_health = "At Risk" if status == "Expired" else ("Healthy" if status in ["Approved", "Confirmed"] else ("Critical" if status == "Rejected" else "Watch"))

        day = (i * 3) % 28 + 1
        month = 1 if i < 35 else 2
        q_date = f"2026-{month:02d}-{day:02d}"

        create_quotation(
            q_code, cust_id, q_date, 30, lines_spec,
            status=status, approval_status=app_status, deal_health=d_health,
            notes=f"Bangalore commercial proposal for {cust[2]} covering enterprise IT hardware procurement and SLA services."
        )

    print(f"Generated {len(quotations)} Quotations with {len(quotation_lines)} Quotation Lines.")

    # --------------------------------------------------------------------------
    # 9. NEGOTIATIONS (Section 37) - Target: 25+ records
    # --------------------------------------------------------------------------
    negotiations = []
    neg_idx = 1
    # Find quotation lines in 'Under Negotiation' or 'Pending Approval' quotes
    neg_quotes = [q for q in quotations if q[10] in ["Under Negotiation", "Pending Approval"]]
    for q in neg_quotes:
        qid = q[0]
        cid = q[2]
        ql_matching = [ql for ql in quotation_lines if ql[1] == qid and ql[3] == "PRODUCT"]
        for ql in ql_matching[:2]:
            orig_disc = float(ql[10])
            req_disc = orig_disc + random.choice([5.0, 7.5, 10.0, 12.0])
            msg = f"Client requested commercial discount adjustment to {req_disc:.1f}% due to competitive OEM quote from alternate vendor."
            status = "RESOLVED" if random.random() > 0.5 else "PENDING_APPROVAL"
            sub_date = "2026-02-18T14:30:00Z"
            res_date = "2026-02-21T11:00:00Z" if status == "RESOLVED" else ""
            negotiations.append([
                f"NEG-{neg_idx:04d}", qid, cid, ql[0], f"{orig_disc:.1f}", f"{req_disc:.1f}",
                msg, status, sub_date, res_date
            ])
            neg_idx += 1
            if len(negotiations) >= 30:
                break
        if len(negotiations) >= 30:
            break

    print(f"Generated {len(negotiations)} Customer Negotiations.")

    # --------------------------------------------------------------------------
    # 10. DEAL HEALTH (Section 38) - 1 record per quotation
    # --------------------------------------------------------------------------
    deal_health = []
    dh_idx = 1
    for q in quotations:
        qid = q[0]
        q_status = q[10]
        dh_status = q[12]

        if dh_status == "Critical":
            days_inact = random.randint(15, 35)
            disc_anom = round(random.uniform(0.75, 0.95), 2)
            deliv_risk = round(random.uniform(0.60, 0.85), 2)
            app_delay = round(random.uniform(0.70, 0.90), 2)
            inv_risk = round(random.uniform(0.50, 0.80), 2)
            overall = round(random.uniform(0.20, 0.40), 2)
            rec_action = "Escalate immediately to Commercial Director; review requested margins with Finance"
        elif dh_status == "At Risk":
            days_inact = random.randint(20, 45)
            disc_anom = round(random.uniform(0.20, 0.40), 2)
            deliv_risk = round(random.uniform(0.40, 0.60), 2)
            app_delay = round(random.uniform(0.30, 0.50), 2)
            inv_risk = round(random.uniform(0.30, 0.50), 2)
            overall = round(random.uniform(0.40, 0.55), 2)
            rec_action = "Schedule executive sponsor review with customer procurement team"
        elif dh_status == "Watch":
            days_inact = random.randint(5, 14)
            disc_anom = round(random.uniform(0.10, 0.30), 2)
            deliv_risk = round(random.uniform(0.20, 0.40), 2)
            app_delay = round(random.uniform(0.20, 0.40), 2)
            inv_risk = round(random.uniform(0.20, 0.40), 2)
            overall = round(random.uniform(0.60, 0.75), 2)
            rec_action = "Follow up with account manager regarding expected PO release date"
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
    # 11. AUDIT LOGS (Section 39) - Target: 120+ records
    # --------------------------------------------------------------------------
    audit_logs = []
    aud_idx = 1
    actions_pool = [
        ("Quotation", "Quote created", "", "Draft", "Sales Rep created initial commercial draft proposal"),
        ("Quotation", "Discount changed", "10.0%", "24.0%", "Sales Lead applied competitive strategic discount"),
        ("Quotation", "Approval requested", "Draft", "Pending Approval", "Discount exceeded category limit; routed to L2 Sales Director"),
        ("Quotation", "Approval approved", "Pending Approval", "Approved", "Commercial approval granted after executive review"),
        ("Quotation", "Customer counter-offer submitted", "Approved", "Under Negotiation", "Customer requested 3% additional concession"),
        ("Quotation", "Warehouse allocation changed", "WH-001 (Bangalore)", "WH-001 + WH-003 Split", "Multi-warehouse split allocated due to local inventory balance"),
        ("Quotation", "Backorder created", "0", "2 Units", "Factory backorder created with OEM supply chain"),
        ("Quotation", "Quote confirmed", "Approved", "Confirmed", "Customer issued formal Purchase Order"),
        ("Invoice", "Invoice generated", "None", "INV-2026-0001", "Finance generated tax invoice against confirmed deal")
    ]

    for q in quotations[:50]:
        qid = q[0]
        # Generate 3-4 log entries per quotation
        num_logs = random.randint(2, 4)
        for act in random.sample(actions_pool, num_logs):
            audit_logs.append([
                f"AUD-{aud_idx:05d}", act[0], qid, act[1], act[2], act[3],
                "Kavita Sharma", act[4], "2026-02-28T16:00:00Z"
            ])
            aud_idx += 1

    print(f"Generated {len(audit_logs)} Audit Log entries.")

    # --------------------------------------------------------------------------
    # 12. INVOICES & INVOICE LINES (Section 40) - Target: 40+ Invoices
    # --------------------------------------------------------------------------
    invoices = []
    invoice_lines = []
    inv_num_idx = 1
    inv_line_idx = 1

    # Invoices generated for Approved & Confirmed quotations
    billable_quotes = [q for q in quotations if q[10] in ["Approved", "Confirmed"]]
    for q in billable_quotes:
        qid = q[0]
        q_code = q[1]
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
        inv_number = f"INV-2026-{inv_num_idx:04d}"
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
    # WRITE ALL 21 CSV FILES
    # --------------------------------------------------------------------------
    files_to_write = [
        ("brands.csv", ["brand_id", "brand_name", "brand_code", "country", "support_level", "status"], brands),
        ("categories.csv", ["category_id", "category_name", "parent_category_id", "description", "status"], categories),
        ("warehouses.csv", ["warehouse_id", "warehouse_code", "warehouse_name", "city", "state", "country", "warehouse_type", "manager_name", "capacity_units", "status"], warehouses),
        ("services.csv", ["service_id", "service_code", "service_name", "service_category", "description", "cost", "selling_price", "tax_rate", "minimum_margin_percent", "recurring", "billing_frequency", "status"], services),
        ("subscription_plans.csv", ["plan_id", "plan_code", "plan_name", "billing_frequency", "billing_interval", "price", "setup_fee", "proration_enabled", "cancellation_policy", "refund_policy", "status"], subscriptions),
        ("discount_rules.csv", ["discount_rule_id", "customer_tier", "category_id", "maximum_discount_percent", "minimum_margin_percent", "approval_level", "risk_level", "active"], discount_rules),
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
        ("deal_health.csv", ["deal_health_id", "quotation_id", "days_inactive", "discount_anomaly_score", "delivery_risk_score", "approval_delay_score", "inventory_risk_score", "overall_health_score", "health_status", "recommended_action", "last_evaluated_at"], deal_health),
        ("audit_logs.csv", ["audit_id", "entity_type", "entity_id", "action", "old_value", "new_value", "performed_by", "reason", "timestamp"], audit_logs),
        ("invoices.csv", ["invoice_id", "invoice_number", "quotation_id", "customer_id", "invoice_date", "due_date", "currency", "subtotal", "discount_total", "tax_total", "grand_total", "billing_type", "status"], invoices),
        ("invoice_lines.csv", ["invoice_line_id", "invoice_id", "item_type", "product_variant_id", "service_id", "subscription_plan_id", "description", "quantity", "unit_price", "discount_percent", "discount_amount", "tax_rate", "tax_amount", "line_total", "billing_type"], invoice_lines)
    ]

    for fname, headers, rows in files_to_write:
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"Successfully generated {fname:<28} : {len(rows):>6} records")

    print("==================================================")
    print("ALL 21 CSV FILES GENERATED SUCCESSFULLY IN BANGALORE DATASET!")
    print("==================================================")

if __name__ == "__main__":
    run()
