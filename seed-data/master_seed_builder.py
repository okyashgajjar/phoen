"""
DealFlow360 Master Seed Data Builder
Orchestrates generation of all 16 CSV files for Ahmedabad Enterprise Distribution Center (AMD-DC-01)
Guarantees 100% relational integrity, authentic pricing, varied inventory, and scenario coverage.
"""

import os
import sys
import csv
import random
from datetime import datetime, timedelta

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import build_base
import build_catalog

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

def run():
    print("==================================================")
    print("DEALFLOW360 SEED DATA GENERATOR")
    print("==================================================")

    # 1. Base entities
    brands = build_base.BRANDS
    categories = build_base.CATEGORIES
    warehouses = build_base.WAREHOUSES
    services = build_base.SERVICES
    subscriptions = build_base.SUBSCRIPTION_PLANS
    discount_rules = build_base.DISCOUNT_RULES
    customers = build_base.CUSTOMERS_DATA

    # 2. Catalog (Products & Variants)
    products, base_variants = build_catalog.generate_catalog()

    # Expand variants to ensure between 250 and 400 sellable SKUs
    # Let's add realistic spec configurations for products that have 1 variant
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
        p_brand = p[3]
        subcat = p[5]
        base_cost = float(p[10])
        base_price = float(p[11])
        existing_vars = var_by_prod.get(pid, [])

        # Add 1 or 2 more variants if only 1 exists, depending on category
        if len(existing_vars) == 1:
            ev = existing_vars[0]
            if subcat in ["CAT-LAP", "CAT-DSK"]:
                # 32GB RAM / 1TB SSD upgrade
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-WKS":
                # High-memory / GPU expansion
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SRV":
                # Dual CPU & 256GB ECC RAM
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SMP":
                # Storage & color variant
                v_id = f"VAR-{v_idx:04d}"
                v_idx += 1
                sku = f"{ev[2]}-512G-SIL"
                vname = f"{ev[3].split(' / ')[0]} 512GB Silver 5G Enterprise"
                extra = round(base_price * 0.18, 2)
                cost = round(base_cost + extra * 0.85, 2)
                price = round(base_price + extra, 2)
                new_v = [
                    v_id, pid, sku, vname, ev[4], ev[5], "512GB", ev[7], ev[8], ev[9], ev[10],
                    "Silver", ev[12], ev[13], ev[14], ev[15], f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}",
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-TAB":
                # 5G Cellular + 256GB option
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-MON":
                # Daisy-chain / Ergo arm bundle
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-NET":
                # Redundant Dual Power Supply (RPS) version
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-STO":
                # Pre-populated high-capacity drives
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-UPS":
                # External Battery Pack (EBM) extended runtime bundle
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-PRN":
                # High-yield extra toner + 500-sheet second paper tray bundle
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-ACC":
                # Color or interface option (e.g. Platinum Silver or 2m Cable length)
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-COL":
                # Bundled table expansion mic pod
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

            elif subcat == "CAT-SEC":
                # 5m length or 24-Pack option
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
                    f"8907100{v_idx:06d}", "ACTIVE"
                ]
                variants.append(new_v)
                var_by_prod[pid].append(new_v)

    print(f"Final Products Count: {len(products)}")
    print(f"Final Sellable Variants Count: {len(variants)}")

    # Variant lookup
    var_dict = {v[0]: v for v in variants}
    sku_to_vid = {v[2]: v[0] for v in variants}
    prod_dict = {p[0]: p for p in products}

    # Identify special target variants for demo scenarios
    # 1. Scenario 1 & 2 Laptop: Latitude 5440 or ThinkPad T14
    var_lap_5440 = sku_to_vid.get("LAP-DEL-5440-I5-16-512", variants[0][0])
    var_dock_wd19s = sku_to_vid.get("VAR-ACC-DEL-WD19S-01")
    var_mon_p2422h = sku_to_vid.get("VAR-MON-DEL-P2422H-01")

    # Scenario 2: ThinkPad T14 Gen 4
    var_lap_t14 = sku_to_vid.get("LAP-LEN-T14-01")

    # Scenario 3: Dell PowerEdge R760
    var_srv_r760 = sku_to_vid.get("VAR-SRV-DEL-R760-01")

    # Scenario 4: HP EliteBook 840 G10 & HP E24 G4
    var_lap_eb840 = sku_to_vid.get("VAR-LAP-HP-EB840-01")
    var_mon_e24g4 = sku_to_vid.get("VAR-MON-HP-E24G4-01")

    # Scenario 5: Samsung Tab Active4 Pro
    var_tab_act4 = sku_to_vid.get("VAR-TAB-SAM-ACT4-01")

    # Demo G: Cisco 9200L 48P
    var_net_c9200l = sku_to_vid.get("VAR-NET-CIS-C9200L-48-01")

    # --------------------------------------------------------------------------
    # 3. INVENTORY (Warehouse inventory records)
    # --------------------------------------------------------------------------
    # Primary warehouse: WH-001 (AMD-DC-01)
    # Secondary warehouses: WH-002 (BOM-DC-01), WH-003 (BLR-DC-01), WH-004 (DEL-DC-01)
    inventory = []
    inv_idx = 1

    # Populate AMD-DC-01 (WH-001) for all variants
    for v in variants:
        vid = v[0]
        pid = v[1]
        p_obj = prod_dict[pid]
        subcat = p_obj[5]
        selling_price = float(v[18])

        # Default quantities based on product value & tier
        if vid == var_lap_t14:
            # Scenario 2 requirement: Ahmedabad has 60 available, 60 reserved
            avail = 60
            res = 60
            alloc = 60
            backorder = 0
            reorder_lvl = 30
            reorder_qty = 80
            safety = 20
            incoming = 50
            avg_demand = 8.5
            status = "IN_STOCK"
        elif vid == var_srv_r760:
            # Scenario 3 requirement: Ahmedabad available = 8, incoming = 20, backorder = 22
            avail = 8
            res = 8
            alloc = 8
            backorder = 22
            reorder_lvl = 10
            reorder_qty = 25
            safety = 5
            incoming = 20
            avg_demand = 1.8
            status = "BACKORDER"
        elif vid == var_lap_5440:
            # High inventory for Scenario 1
            avail = 145
            res = 100
            alloc = 100
            backorder = 0
            reorder_lvl = 40
            reorder_qty = 120
            safety = 25
            incoming = 80
            avg_demand = 12.0
            status = "IN_STOCK"
        elif vid == var_dock_wd19s:
            avail = 320
            res = 100
            alloc = 100
            backorder = 0
            reorder_lvl = 50
            reorder_qty = 200
            safety = 40
            incoming = 150
            avg_demand = 22.0
            status = "IN_STOCK"
        elif vid == var_mon_p2422h:
            avail = 180
            res = 20
            alloc = 20
            backorder = 0
            reorder_lvl = 35
            reorder_qty = 100
            safety = 20
            incoming = 60
            avg_demand = 14.5
            status = "IN_STOCK"
        elif subcat == "CAT-SRV":
            # High-end servers: 1 - 15 units
            avail = random.randint(1, 14)
            res = random.randint(0, min(avail, 3))
            alloc = res
            backorder = random.choice([0, 0, 0, 2, 4])
            reorder_lvl = 4
            reorder_qty = 10
            safety = 2
            incoming = random.choice([0, 5, 10])
            avg_demand = round(random.uniform(0.3, 1.5), 1)
            status = "LOW_STOCK" if avail <= 3 else "IN_STOCK"
        elif subcat == "CAT-WKS":
            # Workstations: 2 - 12 units
            avail = random.randint(2, 12)
            res = random.randint(0, 2)
            alloc = res
            backorder = 0
            reorder_lvl = 4
            reorder_qty = 10
            safety = 2
            incoming = random.choice([0, 4, 8])
            avg_demand = round(random.uniform(0.5, 2.0), 1)
            status = "LOW_STOCK" if avail <= 3 else "IN_STOCK"
        elif subcat in ["CAT-LAP", "CAT-DSK"]:
            # Laptops & Desktops: 20 - 150 units
            avail = random.randint(25, 140)
            res = random.randint(5, 25)
            alloc = res
            backorder = 0
            reorder_lvl = 30
            reorder_qty = 60
            safety = 15
            incoming = random.choice([20, 40, 60])
            avg_demand = round(random.uniform(3.0, 10.0), 1)
            status = "IN_STOCK"
        elif subcat in ["CAT-SMP", "CAT-TAB"]:
            # Mobility: 5 - 80 units
            avail = random.randint(8, 75)
            res = random.randint(2, 15)
            alloc = res
            backorder = 0
            reorder_lvl = 15
            reorder_qty = 40
            safety = 8
            incoming = random.choice([15, 30])
            avg_demand = round(random.uniform(1.5, 6.0), 1)
            status = "IN_STOCK"
        elif subcat == "CAT-NET":
            # Enterprise Networking: 3 - 35 units
            avail = random.randint(3, 32)
            res = random.randint(1, 6)
            alloc = res
            backorder = 0
            reorder_lvl = 8
            reorder_qty = 20
            safety = 4
            incoming = random.choice([5, 15])
            avg_demand = round(random.uniform(0.8, 3.5), 1)
            status = "LOW_STOCK" if avail <= 5 else "IN_STOCK"
        elif subcat == "CAT-ACC":
            # Accessories: 50 - 500 units
            avail = random.randint(60, 450)
            res = random.randint(10, 50)
            alloc = res
            backorder = 0
            reorder_lvl = 50
            reorder_qty = 150
            safety = 30
            incoming = random.choice([50, 100, 200])
            avg_demand = round(random.uniform(8.0, 35.0), 1)
            status = "IN_STOCK"
        else:
            # Monitors, Printers, Collaboration, UPS, Storage: 5 - 60 units
            avail = random.randint(6, 55)
            res = random.randint(1, 10)
            alloc = res
            backorder = 0
            reorder_lvl = 10
            reorder_qty = 25
            safety = 5
            incoming = random.choice([10, 20])
            avg_demand = round(random.uniform(1.0, 5.0), 1)
            status = "LOW_STOCK" if avail <= 8 else "IN_STOCK"

        # Mark occasional stock variations
        if inv_idx in [17, 39, 88]:
            avail = 0
            status = "OUT_OF_STOCK"
        elif inv_idx in [23, 67, 114]:
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

    # Add secondary warehouse records for multi-warehouse allocation
    # 1. Scenario 2: BOM-DC-01 has 40 units of var_lap_t14
    inv_id = f"INV-{inv_idx:05d}"
    inv_idx += 1
    inventory.append([
        inv_id, "WH-002", var_lap_t14, 40, 40, 40, 0,
        25, 60, 15, 30, 6.0, "IN_STOCK", "2026-02-18T11:00:00Z", "2026-03-25T11:00:00Z"
    ])

    # 2. Add inventory in BOM-DC-01, BLR-DC-01, DEL-DC-01 for popular hardware models
    multi_wh_targets = [var_lap_5440, var_lap_eb840, var_mon_p2422h, var_dock_wd19s, var_net_c9200l, var_srv_r760]
    for mvid in multi_wh_targets:
        for wh in ["WH-002", "WH-003", "WH-004"]:
            if mvid == var_lap_t14 and wh == "WH-002":
                continue # already added above
            inv_id = f"INV-{inv_idx:05d}"
            inv_idx += 1
            inventory.append([
                inv_id, wh, mvid, random.randint(15, 60), random.randint(2, 10), random.randint(2, 10), 0,
                15, 40, 10, 20, 3.5, "IN_STOCK", "2026-02-10T10:00:00Z", "2026-03-22T10:00:00Z"
            ])

    print(f"Generated {len(inventory)} Inventory records across warehouses.")

    # --------------------------------------------------------------------------
    # 4. PRICE LISTS (Standard, SMB, Enterprise, Strategic)
    # --------------------------------------------------------------------------
    price_lists = []
    pl_idx = 1
    # Customer Tiers: Standard (base), SMB (4-7% discount), Enterprise (9-14%), Strategic (16-22%)
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
            # Realistic price variation per tier
            if tier == "Standard":
                unit_price = std_price
            else:
                # varied discount per category
                subcat = prod_dict[v[1]][5]
                if subcat == "CAT-ACC":
                    tier_disc = discount_factor * 1.25  # higher discount on accessories
                elif subcat in ["CAT-SRV", "CAT-WKS"]:
                    tier_disc = discount_factor * 0.90  # tighter discount on heavy compute
                else:
                    tier_disc = discount_factor
                unit_price = round(std_price * (1.0 - tier_disc), 2)

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
    # 6. PRODUCT RECOMMENDATIONS (Upsell / Cross-Sell Rules)
    # --------------------------------------------------------------------------
    # Generate 180+ meaningful business recommendations
    recommendations = []
    rec_idx = 1

    # Pre-select key accessory products for recommendation mapping
    dock_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Dock" in p[2]]
    monitor_prods = [p[0] for p in products if p[5] == "CAT-MON"]
    bag_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Backpack" in p[2]]
    mouse_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Mouse" in p[2] or "Combo" in p[2]]
    headset_prods = [p[0] for p in products if p[5] == "CAT-ACC" and "Headset" in p[2]]
    ups_prods = [p[0] for p in products if p[5] == "CAT-UPS"]
    server_rack_acc = [p[0] for p in products if p[5] == "CAT-SEC" and "Rail" in p[2] or "CMA" in p[2]]
    optics_prods = [p[0] for p in products if p[5] == "CAT-SEC" and "SFP" in p[2] or "DAC" in p[2]]
    cable_prods = [p[0] for p in products if p[5] == "CAT-SEC" and "Patch Cable" in p[2]]
    storage_drives = [p[0] for p in products if p[5] == "CAT-STO" and ("SSD" in p[2] or "HDD" in p[2])]

    for p in products:
        pid = p[0]
        subcat = p[5]

        if subcat == "CAT-LAP":
            # Laptop -> Docking Station
            if dock_prods:
                target = random.choice(dock_prods)
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, target, "CROSS_SELL", 0.88, 0.74, 8.5, 1, True, 20.0,
                    "Frequently purchased together with corporate laptops to enable multi-display desktop workstations", "ACTIVE"
                ])
                rec_idx += 1

            # Laptop -> Monitor
            if monitor_prods:
                target = random.choice(monitor_prods)
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, target, "ATTACHMENT", 0.82, 0.65, 6.2, 2, True, 18.0,
                    "Recommended dual-display pairing for corporate productivity enhancement", "ACTIVE"
                ])
                rec_idx += 1

            # Laptop -> Backpack / Sleeve
            if bag_prods:
                target = random.choice(bag_prods)
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, target, "CROSS_SELL", 0.91, 0.82, 12.0, 3, True, 25.0,
                    "Essential protective transport gear for distributed enterprise workforce", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-WKS":
            # Workstation -> 4K Color Monitor
            hi_res_monitors = [m for m in monitor_prods if "4K" in prod_dict[m][2] or "U27" in prod_dict[m][1]]
            if hi_res_monitors:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(hi_res_monitors), "UPSELL", 0.94, 0.86, 9.4, 1, True, 22.0,
                    "Factory color-calibrated display essential for CAD, 3D visualization and simulation workloads", "ACTIVE"
                ])
                rec_idx += 1

            # Workstation -> Online UPS
            if ups_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(ups_prods[:3]), "ATTACHMENT", 0.89, 0.71, 7.8, 2, True, 18.0,
                    "Pure sine-wave power backup protects high-power compute rigs against power spikes and brownouts", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-SRV":
            # Server -> Rackmount UPS
            rack_ups = [u for u in ups_prods if "RT" in prod_dict[u][1] or "SRT" in prod_dict[u][1]]
            if rack_ups:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(rack_ups), "ATTACHMENT", 0.95, 0.88, 8.0, 1, True, 18.0,
                    "Mission-critical online double-conversion power conditioning required for enterprise SLA compliance", "ACTIVE"
                ])
                rec_idx += 1

            # Server -> Rail Kit / Rack Cable Arm
            if server_rack_acc:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(server_rack_acc), "ATTACHMENT", 0.98, 0.92, 14.5, 2, True, 25.0,
                    "Toolless sliding rail kit required for mounting in standard 19-inch 4-post enterprise server racks", "ACTIVE"
                ])
                rec_idx += 1

            # Server -> 10G Optics / DAC
            if optics_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(optics_prods), "CROSS_SELL", 0.87, 0.76, 15.0, 3, True, 25.0,
                    "High-speed 10Gbps optical uplink connectivity for top-of-rack switch integration", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-NET":
            # Switch -> DAC / Optics
            if optics_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(optics_prods), "ATTACHMENT", 0.96, 0.90, 18.0, 1, True, 30.0,
                    "Certified SFP+ optical transceiver or DAC cable for core distribution and stack interconnect", "ACTIVE"
                ])
                rec_idx += 1

            # Switch -> Cat6A Patch Cables
            if cable_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, random.choice(cable_prods), "CROSS_SELL", 0.92, 0.85, 22.0, 2, True, 35.0,
                    "Snagless 10-Gigabit certified patch cords for high-density patch panel to switch patching", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-SMP":
            # Smartphone -> GaN Charger
            chargers = [c[0] for c in products if c[5] == "CAT-ACC" and "Charger" in c[2]]
            if chargers:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, chargers[0], "CROSS_SELL", 0.89, 0.81, 16.5, 1, True, 25.0,
                    "120W multi-device fast charger simultaneously powers executive smartphone and ultrabook", "ACTIVE"
                ])
                rec_idx += 1

        elif subcat == "CAT-PRN":
            # Printer -> Cat6 Patch Cable
            if cable_prods:
                recommendations.append([
                    f"REC-{rec_idx:04d}", pid, cable_prods[0], "ATTACHMENT", 0.85, 0.72, 20.0, 1, True, 30.0,
                    "Shielded Ethernet cabling ensures stable Gigabit network print queue communication", "ACTIVE"
                ])
                rec_idx += 1

    print(f"Generated {len(recommendations)} Product Recommendations (Upsell & Cross-Sell).")

    # --------------------------------------------------------------------------
    # 7. PRODUCT SERVICE RULES
    # --------------------------------------------------------------------------
    product_service_rules = []
    psr_idx = 1

    for p in products:
        pid = p[0]
        subcat = p[5]

        if subcat == "CAT-SRV":
            # Server & Rack Installation
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-001", True, False, 1])
            psr_idx += 1
            # Hypervisor OS Provisioning
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-002", True, False, 2])
            psr_idx += 1
        elif subcat == "CAT-NET":
            # L2/L3 Network Setup
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-003", True, False, 1])
            psr_idx += 1
            if "Firewall" in p[2]:
                product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-004", True, True, 1])
                psr_idx += 1
        elif subcat in ["CAT-LAP", "CAT-DSK"]:
            # Laptop zero-touch deployment
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-005", True, False, 1])
            psr_idx += 1
        elif subcat == "CAT-STO":
            # Data migration
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-006", True, False, 1])
            psr_idx += 1
            product_service_rules.append([f"PSR-{psr_idx:04d}", pid, "SRV-011", True, False, 2])
            psr_idx += 1

    print(f"Generated {len(product_service_rules)} Product-Service Attachment Rules.")

    # --------------------------------------------------------------------------
    # 8. QUOTATIONS & QUOTATION LINES
    # --------------------------------------------------------------------------
    quotations = []
    quotation_lines = []
    q_idx = 1
    ql_idx = 1

    # Helper function to construct quotation lines and total up
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

            itype = spec["item_type"] # PRODUCT, SERVICE, SUBSCRIPTION
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
    # SPECIAL DEMO SCENARIOS
    # --------------------------------------------------------------------------

    # Scenario 1 / Demo A: Excessive Discount -> Approval Required
    # Enterprise customer purchases 100 laptops, 100 docks, 20 monitors, installation
    # Discount applied = 22% (Enterprise Hardware max allowed is 15%)
    p_lap_price = float(var_dict[var_lap_5440][18])
    p_dock_price = float(var_dict[var_dock_wd19s][18])
    p_mon_price = float(var_dict[var_mon_p2422h][18])
    create_quotation(
        "QT-2026-0001", "CUST-001", "2026-02-28", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_5440, "description": var_dict[var_lap_5440][3], "qty": 100, "unit_price": p_lap_price, "discount_pct": 22.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_dock_wd19s, "description": var_dict[var_dock_wd19s][3], "qty": 100, "unit_price": p_dock_price, "discount_pct": 18.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_mon_p2422h, "description": var_dict[var_mon_p2422h][3], "qty": 20, "unit_price": p_mon_price, "discount_pct": 15.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise Laptop Zero-Touch Imaging & Domain Join", "qty": 100, "unit_price": 1200.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Pending Approval", approval_status="Pending L2_SALES_DIRECTOR Approval", deal_health="Action Required",
        notes="Demo A Scenario: Enterprise fleet refresh. 22.0% requested discount on Laptops exceeds 15.0% tier ceiling. Requires Sales Director commercial signoff."
    )

    # Scenario 2 / Demo C: Multi-Warehouse Split Fulfillment
    # Customer requests 100 ThinkPad T14. Ahmedabad has 60, Mumbai has 40.
    p_t14_price = float(var_dict[var_lap_t14][18])
    create_quotation(
        "QT-2026-0002", "CUST-004", "2026-02-25", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_t14, "description": f"{var_dict[var_lap_t14][3]} (Fulfillment: Ahmedabad DC)", "qty": 60, "unit_price": p_t14_price, "discount_pct": 12.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_lap_t14, "description": f"{var_dict[var_lap_t14][3]} (Fulfillment: Mumbai Hub Split)", "qty": 40, "unit_price": p_t14_price, "discount_pct": 12.0, "wh_id": "WH-002", "fulfillment_status": "PARTIAL_SPLIT", "billing_type": "ONE_TIME"}
        ],
        status="Approved", approval_status="Approved", deal_health="Healthy",
        notes="Demo C Scenario: Multi-warehouse split allocated. 60 units fulfilled from Ahmedabad Central (AMD-DC-01) and 40 units from Mumbai Hub (BOM-DC-01)."
    )

    # Scenario 3: Backorder
    # Customer requests 50 enterprise servers. Ahmedabad has 8 avail, 20 incoming, 22 backorder.
    p_r760_price = float(var_dict[var_srv_r760][18])
    create_quotation(
        "QT-2026-0003", "CUST-010", "2026-02-20", 45,
        [
            {"item_type": "PRODUCT", "variant_id": var_srv_r760, "description": var_dict[var_srv_r760][3], "qty": 50, "unit_price": p_r760_price, "discount_pct": 14.0, "wh_id": "WH-001", "fulfillment_status": "BACKORDERED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-001", "description": "Enterprise Server & Rack Installation", "qty": 50, "unit_price": 7500.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Confirmed", approval_status="Approved", deal_health="Monitored",
        notes="Demo Backorder Scenario: 50x PowerEdge R760. 8 units allocated from stock, 20 from shipment ETA 7 days, 22 on manufacturer factory backorder."
    )

    # Scenario 4 / Demo D: Hybrid Billing (Hardware + AMC + SaaS)
    # 20 laptops, 20 monitors, Installation, 3-Year Comprehensive AMC, Cloud Backup
    p_eb840_price = float(var_dict[var_lap_eb840][18])
    p_e24_price = float(var_dict[var_mon_e24g4][18])
    create_quotation(
        "QT-2026-0004", "CUST-002", "2026-02-22", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_lap_eb840, "description": var_dict[var_lap_eb840][3], "qty": 20, "unit_price": p_eb840_price, "discount_pct": 10.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "PRODUCT", "variant_id": var_mon_e24g4, "description": var_dict[var_mon_e24g4][3], "qty": 20, "unit_price": p_e24_price, "discount_pct": 8.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Enterprise Laptop Zero-Touch Imaging", "qty": 20, "unit_price": 1200.0, "discount_pct": 5.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"},
            {"item_type": "SUBSCRIPTION", "subscription_id": "SUB-001", "description": "Comprehensive Enterprise AMC (4hr SLA) - Annual", "qty": 1, "unit_price": 48000.0, "discount_pct": 0.0, "billing_type": "RECURRING", "fulfillment_status": "PENDING"},
            {"item_type": "SUBSCRIPTION", "subscription_id": "SUB-004", "description": "Managed Cloud Backup BaaS - 1 TB - Monthly", "qty": 1, "unit_price": 1800.0, "discount_pct": 0.0, "billing_type": "RECURRING", "fulfillment_status": "PENDING"}
        ],
        status="Approved", approval_status="Approved", deal_health="Healthy",
        notes="Demo D Scenario: Hybrid enterprise order combining One-Time hardware & deployment with recurring Annual AMC and Monthly Cloud Backup."
    )

    # Scenario 5 / Demo E: Customer Negotiation Threshold Breach
    # Customer in Under Negotiation requests 18.5% discount on rugged tablets (limit is 8%)
    p_act4_price = float(var_dict[var_tab_act4][18])
    create_quotation(
        "QT-2026-0005", "CUST-003", "2026-02-18", 20,
        [
            {"item_type": "PRODUCT", "variant_id": var_tab_act4, "description": var_dict[var_tab_act4][3], "qty": 35, "unit_price": p_act4_price, "discount_pct": 18.5, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-005", "description": "Field Tablet MDM Enrollment & Kiosk Mode Lockdown", "qty": 35, "unit_price": 1200.0, "discount_pct": 10.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Under Negotiation", approval_status="Pending Approval", deal_health="Attention Needed",
        notes="Demo E Scenario: Customer counter-proposal requested 18.5% discount on field tablets (exceeds 8.0% Mobility ceiling). Approval flow restarted."
    )

    # Demo F: Stalled Inactive Quote -> Deal Health = At Risk
    create_quotation(
        "QT-2026-0006", "CUST-027", "2026-01-12", 30,
        [
            {"item_type": "PRODUCT", "variant_id": variants[25][0], "description": variants[25][3], "qty": 15, "unit_price": float(variants[25][18]), "discount_pct": 5.0, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"}
        ],
        status="Sent", approval_status="Not Required", deal_health="At Risk",
        notes="Demo F Scenario: Deal Health: At Risk. Stalled quotation. No customer engagement recorded for 45+ days following proposal delivery."
    )

    # Demo G: Sales Rep Discount Anomaly Flagged
    p_c9200_price = float(var_dict[var_net_c9200l][18])
    create_quotation(
        "QT-2026-0007", "CUST-014", "2026-02-27", 30,
        [
            {"item_type": "PRODUCT", "variant_id": var_net_c9200l, "description": var_dict[var_net_c9200l][3], "qty": 15, "unit_price": p_c9200_price, "discount_pct": 28.5, "wh_id": "WH-001", "fulfillment_status": "ALLOCATED", "billing_type": "ONE_TIME"},
            {"item_type": "SERVICE", "service_id": "SRV-003", "description": "L2/L3 Network & VLAN Setup", "qty": 1, "unit_price": 12000.0, "discount_pct": 15.0, "billing_type": "ONE_TIME", "fulfillment_status": "PENDING"}
        ],
        status="Pending Approval", approval_status="Flagged - Discount Anomaly", deal_health="Review Required",
        notes="Demo G Scenario: Discount Anomaly detected. 28.5% requested discount on Cisco Enterprise Networking exceeds historical peer median (6.5%) by 22.0%."
    )

    # --------------------------------------------------------------------------
    # Generate 35+ more realistic operational quotations
    # --------------------------------------------------------------------------
    quote_statuses = ["Draft", "Sent", "Under Negotiation", "Pending Approval", "Approved", "Rejected", "Confirmed", "Expired"]

    for i in range(8, 45):
        q_code = f"QT-2026-{i:04d}"
        cust = customers[i % len(customers)]
        cust_id = cust[0]
        cust_tier = cust[4]

        # Generate realistic lines
        num_items = random.randint(2, 4)
        sampled_vars = random.sample(variants, num_items)
        lines_spec = []

        for sv in sampled_vars:
            qty = random.choice([2, 5, 10, 15, 25, 40])
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

        # Add optional service or subscription
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

        status = quote_statuses[i % len(quote_statuses)]
        app_status = "Approved" if status in ["Approved", "Confirmed"] else ("Pending Approval" if status == "Pending Approval" else "Not Required")
        d_health = "At Risk" if status == "Expired" else ("Healthy" if status in ["Approved", "Confirmed"] else "Under Review")

        # Set date in Jan/Feb 2026
        day = (i * 3) % 28 + 1
        month = 1 if i < 20 else 2
        q_date = f"2026-{month:02d}-{day:02d}"

        create_quotation(
            q_code, cust_id, q_date, 30, lines_spec,
            status=status, approval_status=app_status, deal_health=d_health,
            notes=f"Commercial proposal for {cust[2]} covering IT hardware procurement and SLA services."
        )

    print(f"Generated {len(quotations)} Quotations with {len(quotation_lines)} Quotation Lines.")

    # --------------------------------------------------------------------------
    # WRITE ALL 16 CSV FILES
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
        ("quotation_lines.csv", ["line_id", "quotation_id", "line_number", "item_type", "product_variant_id", "service_id", "subscription_plan_id", "description", "quantity", "unit_price", "discount_percent", "discount_amount", "tax_rate", "tax_amount", "line_total", "billing_type", "fulfillment_warehouse_id", "fulfillment_status"], quotation_lines)
    ]

    for fname, headers, rows in files_to_write:
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"Successfully generated {fname:<28} : {len(rows):>6} records")

    print("==================================================")
    print("ALL 16 CSV FILES GENERATED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run()
