# DealFlow360 — Bangalore Enterprise IT Hardware & Technology Procurement Dataset

A production-grade, relationally consistent enterprise synthetic dataset tailored for **DealFlow360**, a B2B Sales Operations, CPQ (Configure, Price, Quote), and Deal Management platform.

This dataset models a Tier-1 Indian technology distributor headquartered in **Bangalore, Karnataka, India**, serving global GCCs (Global Capability Centers), tech giants, unicorn startups, BFSI centers, and enterprise system integrators across Bangalore's premier technology corridors.

---

## 1. Dataset Overview & Metric Summary

All 21 relational CSV files are synchronized with 100% referential integrity and validated via `validate_seed_data.py`:

| File | Records | Key Business Role |
| :--- | :---: | :--- |
| `brands.csv` | **32** | Global Tier-1 IT hardware & enterprise software OEMs |
| `categories.csv` | **18** | 4 primary technology domains + 14 specialized leaf subcategories |
| `warehouses.csv` | **5** | Primary Bangalore DC (`BLR-DC-01`) + 4 national regional logistics hubs |
| `products.csv` | **265** | Enterprise hardware catalog (laptops, servers, storage, networking) |
| `product_variants.csv` | **532** | Configured sellable SKUs with CPU, RAM, storage, GPU, OS, extra prices |
| `inventory.csv` | **1,072** | Multi-warehouse stock (available, reserved, allocated, backordered, safety) |
| `price_lists.csv` | **2,128** | 4 customer pricing tiers x 532 variants with strict margin floors |
| `customer_price_lists.csv` | **80** | Explicit customer-to-tier commercial mapping |
| `discount_rules.csv` | **28** | Multi-level approval thresholds and gross margin constraints |
| `customers.csv` | **80** | Authentic Bangalore technology enterprise accounts with GSTINs and corridors |
| `product_recommendations.csv` | **421** | Machine learning and CPQ rules (Upsell, Cross-Sell, Attachment) |
| `services.csv` | **12** | Enterprise professional IT deployment, imaging, cabling & rack services |
| `subscription_plans.csv` | **8** | Recurring SLA, 24x7 AMC, Cloud MDM, and security subscriptions |
| `product_service_rules.csv` | **132** | Mandatory and recommended hardware service attachments |
| `quotations.csv` | **80** | Enterprise commercial proposals spanning standard and edge-case deals |
| `quotation_lines.csv` | **302** | Line items covering hardware CAPEX, services, and recurring subscriptions |
| `negotiations.csv` | **30** | Customer discount counter-offers, business justifications, and statuses |
| `deal_health.csv` | **80** | AI-driven deal health assessments (inactivity, anomaly, delivery, approval risk) |
| `audit_logs.csv` | **156** | Immutable governance audit trail of price changes, approvals, and allocations |
| `invoices.csv` | **44** | Commercial tax invoices across ONE_TIME, RECURRING, and HYBRID models |
| `invoice_lines.csv` | **172** | Itemized invoice lines with GST tax breakdowns and line totals |

---

## 2. Supply Chain & Distribution Center Network

The dataset is anchored around **Bangalore Central Distribution Center (`BLR-DC-01`)** with strategic regional fulfillment hubs across India:

| Warehouse ID | Code | Name | City | State | Capacity | Operational Role |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `WH-001` | **`BLR-DC-01`** | **Bangalore Enterprise Technology DC** | **Bengaluru** | **Karnataka** | **150,000** | **Primary Regional Mega-Hub & Fast-Fulfillment Center** |
| `WH-002` | `AMD-DC-01` | Ahmedabad Commercial Logistics Hub | Ahmedabad | Gujarat | 60,000 | Western regional backup & edge distribution |
| `WH-003` | `MUM-DC-01` | Mumbai Port Logistics Center | Navi Mumbai | Maharashtra | 120,000 | Sea import gateway & enterprise staging facility |
| `WH-004` | `DEL-DC-01` | Delhi NCR Technology Warehouse | Gurugram | Haryana | 90,000 | North India enterprise fulfillment center |
| `WH-005` | `HYD-DC-01` | Hyderabad IT Fulfillment Center | Hyderabad | Telangana | 75,000 | Deccan tech-corridor overflow & support hub |

### Operational Inventory Mechanics
- **Complete SKU Coverage**: All 532 sellable variants are stocked in `BLR-DC-01`.
- **High-Velocity Multi-DC Stocking**: Key infrastructure SKUs (servers, enterprise switches, top corporate laptops, docks) are distributed across `MUM-DC-01`, `DEL-DC-01`, `HYD-DC-01`, and `AMD-DC-01`.
- **Status Distribution**: Real-world statuses including `IN_STOCK`, `LOW_STOCK`, `BACKORDER`, and `OUT_OF_STOCK`.
- **Relational Stock Balancing**: Every record tracks available quantity, reserved stock, allocated stock, backorders, reorder levels, safety stock, incoming transit shipments, and average daily consumption velocity.

---

## 3. Product Catalog & Variant Architecture

The catalog features **265 products** across 14 leaf categories and **532 variants**:

### Product Categories
1. **Commercial Laptops (`CAT-LAP`)**: 45 products (ThinkPad X1/T14, Latitude 5440/7440, EliteBook 840/1040, MacBook Pro/Air, ASUS ExpertBook).
2. **Enterprise Desktops (`CAT-DSK`)**: 30 products (OptiPlex 7010 Micro/SFF, ThinkCentre M70q/M90q Tiny, ProDesk/EliteDesk 800 Mini, iMac, Mac Studio).
3. **High-Performance Workstations (`CAT-WKS`)**: 25 products (Dell Precision 3660/5820/7920, Lenovo ThinkStation P3/P5, HP Z2/Z4/Z8, Mac Pro).
4. **Rack & Blade Servers (`CAT-SRV`)**: 25 products (PowerEdge R660/R760/R760xs, ProLiant DL360/DL380 Gen11, ThinkSystem SR630/SR650 V3, Cisco UCS).
5. **Enterprise Storage Systems (`CAT-STO`)**: 20 products (PowerStore 1000T/3000T, NetApp AFF A250/FAS2820, Synology FlashStation/RackStation, QNAP TS Enterprise).
6. **Enterprise Networking (`CAT-NET`)**: 30 products (Cisco Catalyst 9200L/9300, Aruba CX 6200F/6300M, Juniper EX4400, Cisco Meraki MX/MS, Ubiquiti UniFi Pro/Enterprise).
7. **Cybersecurity & Firewalls (`CAT-SEC`)**: 20 products (Fortinet FortiGate 70F/100F/200F, Palo Alto PA-440/PA-1410, Sophos XGS 2100, Check Point Quantum Spark).
8. **Enterprise Displays & Monitors (`CAT-MON`)**: 25 products (Dell UltraSharp U2724D/U3223QE/P2422H, HP E24/E27, Lenovo ThinkVision, ViewSonic ColorPro, LG UltraFine).
9. **Power Backup & Rack UPS (`CAT-UPS`)**: 15 products (APC Smart-UPS On-Line SRT 3kVA/5kVA, Eaton 9PX 3000/6000, Vertiv Liebert GXT5).
10. **Enterprise Smartphones (`CAT-SMP`)**: 15 products (Galaxy S24/S24 Ultra/Z Fold5, iPhone 15/15 Pro/15 Pro Max, Google Pixel 8 Pro).
11. **Enterprise Tablets (`CAT-TAB`)**: 10 products (iPad Pro 11/12.9, iPad Air, Galaxy Tab S9, Microsoft Surface Pro 9).
12. **Printers & Document Solutions (`CAT-PRN`)**: 5 products (HP LaserJet Enterprise MFP, Canon imageRUNNER, Xerox VersaLink).
13. **Collaboration & Video Conferencing (`CAT-COL`)**: 5 products (Logitech Rally Plus / MeetUp, Poly Studio X50, Cisco Room Kit).
14. **Corporate Accessories & Docks (`CAT-ACC`)**: 15 products (Dell WD19S/WD22TB4, ThinkPad Thunderbolt 4 Docks, Anker 737 GaN Chargers, Jabra Evolve2 Headsets, Dell EcoLoop Backpacks).

### Sellable Variant Engineering
Variants include realistic component matrices:
- **CPUs**: Intel Core i5/i7/i9 13th & 14th Gen, Core Ultra 7, AMD Ryzen Pro 7000/8000, Intel Xeon Silver/Gold/Platinum 4th/5th Gen, AMD EPYC 9004, Apple M3/M3 Pro/M3 Max.
- **RAM**: 16GB DDR5, 32GB DDR5, 64GB DDR5, 128GB ECC, 256GB ECC, 512GB Registered ECC.
- **Storage**: 512GB NVMe Gen4, 1TB NVMe, 2TB Enterprise PCIe 4.0, 8x 1.92TB SAS/SATA Enterprise SSD arrays.
- **Barcodes & GS1 Format**: GS1-13 compatible EAN barcodes (`8907200XXXXXX`).

---

## 4. Customer Landscape — Bangalore Tech Corridors

The customer base comprises **80 authentic Bangalore corporate entities** distributed across Bangalore's iconic tech clusters:

| Technology Cluster / Corridor | Sample Customer Profiles | Primary Segments |
| :--- | :--- | :--- |
| **Outer Ring Road (ORR)**<br>*(Bellandur, Marathahalli, Kadubeesanahalli)* | VertexGrid Technologies, BlueOrbit FinTech, Infosurge Data Labs, NexaCore Bangalore | Global Capability Centers (GCCs), SaaS, Data Analytics |
| **Whitefield**<br>*(ITPB, EPIP Zone, Hoodi)* | Bengaluru Cloud Systems, CloudScale Bangalore Pvt Ltd, TechPulse Whitefield | Cloud Engineering, Enterprise Testing, MNC Centers |
| **Electronic City**<br>*(Phase 1, Phase 2, Hosur Road)* | Hyperion Cyber Defense, TitanEdge Solutions, IndusSemicon Systems | Embedded Systems, Hardware Engineering, Telecom |
| **Manyata Tech Park**<br>*(Hebbal, Outer Ring Road North)* | NordicEdge Technologies, Quantico Infotech, ApexData Cloud Services | Cloud Security, Network Operations, FinTech |
| **Koramangala & Indiranagar**<br>*(Startups & Innovation Hubs)* | LeapScale Commerce, SwiftPay FinTech, AI Labs Bangalore, UrbanStack Technologies | Unicorn Startups, High-Growth SaaS, AI R&D |
| **Bagmane Tech Park**<br>*(CV Raman Nagar, Marathahalli)* | QuantumForge Technologies, SiliconArc Systems, Aeroflex Avionics Labs | Aerospace & Defense R&D, Semi-conductors, High-Compute |

### Customer Tiers & Credit Governance
- **Strategic (10 Accounts)**: ₹1.00 Cr – ₹3.50 Cr credit limits, 60-90 day payment terms, assigned to Commercial VP / Senior Enterprise Account Directors.
- **Enterprise (28 Accounts)**: ₹30 Lakh – ₹90 Lakh credit limits, 45-60 day terms.
- **SMB (26 Accounts)**: ₹10 Lakh – ₹30 Lakh credit limits, 30 day terms.
- **Standard (16 Accounts)**: ₹2 Lakh – ₹10 Lakh credit limits, 15-30 day terms.

---

## 5. Pricing Architecture & Discount Governance

### 4-Tier Price List Matrix
1. `PL-STD` (**Standard Commercial Price List**): Base commercial catalogue price, MOQ = 1.
2. `PL-SMB` (**SMB Advantage Price List**): ~5% base discount, MOQ = 5.
3. `PL-ENT` (**Enterprise Preferred Price List**): ~11% base discount, MOQ = 20.
4. `PL-STRAT` (**Strategic Global Partner Price List**): ~18% base discount, MOQ = 50.

> **Margin Protection Floor**: The master builder algorithm guarantees that every price list line satisfies `unit_price >= cost_price * 1.04` (minimum 4% gross margin safety cushion). There are zero below-cost entries.

### Discount Governance Rules (`discount_rules.csv`)
28 strict threshold rules govern maximum permitted discounts and approval levels:
- **Standard Tier**: Max 8.0% discount, Min 15.0% margin -> `L1_SALES_LEAD` approval.
- **SMB Tier**: Max 12.0% discount, Min 12.0% margin -> `L1_SALES_LEAD` approval.
- **Enterprise Tier**: Max 16.0% discount, Min 10.0% margin -> `L2_SALES_DIRECTOR` approval.
- **Strategic Tier**: Max 22.0% discount, Min 8.0% margin -> `L3_FINANCE_DIRECTOR` / `COMMERCIAL_VP` approval.

---

## 6. Enterprise Services & Hybrid Recurring Billing

The platform models hybrid B2B quoting combining one-time hardware CAPEX with professional services and recurring subscriptions:

### Professional IT Services (`services.csv`)
- `SRV-001`: Enterprise Server & Rack Installation (₹7,500 / unit)
- `SRV-002`: SAN/NAS Storage Array Configuration & Zoning (₹15,000 / array)
- `SRV-003`: L2/L3 Enterprise Network Switch & VLAN Configuration (₹12,000 / switch stack)
- `SRV-004`: Next-Gen Firewall Installation & Threat Hardening (₹18,000 / cluster)
- `SRV-005`: Enterprise Laptop Zero-Touch Imaging & Domain Join (₹1,200 / laptop)
- `SRV-006`: Enterprise Workstation CAD/GPU Benchmark & Setup (₹2,500 / workstation)
- `SRV-007`: Structured Cat6A Network Cabling & Patch Panel Termination (₹6,500 / 24-ports)
- `SRV-008`: Rackmount UPS Electrical Integration & Calibration (₹4,500 / unit)
- `SRV-009`: Executive Boardroom Video Conference Setup & Acoustic Tuning (₹14,000 / room)
- `SRV-010`: Enterprise Asset Tagging, Barcode Scanning & CMDB Registration (₹350 / device)
- `SRV-011`: Data Migration & RAID Array Volume Initialization (₹9,500 / server)
- `SRV-012`: Emergency Onsite 4-Hour Response IT Support Ticket (₹3,000 / incident)

### Recurring Subscriptions (`subscription_plans.csv`)
- `SUB-001`: Comprehensive Enterprise Hardware AMC (24x7 4hr SLA) — ₹48,000 / year
- `SUB-002`: Next-Business-Day (NBD) Hardware Support AMC — ₹22,000 / year
- `SUB-003`: Cloud Network Monitoring & Firmware Management (NOC) — ₹1,800 / switch / month
- `SUB-004`: Managed Firewall Security Operations & Threat Feeds (SOC) — ₹8,500 / month
- `SUB-005`: High-Priority SLA Helpdesk Support (Per Seat) — ₹650 / user / month
- `SUB-006`: Cloud Endpoint Mobility Management (MDM / EMM Per Seat) — ₹2,400 / seat / year
- `SUB-007`: Proactive SAN/Storage Health & Remote Monitoring — ₹3,500 / month
- `SUB-008`: Boardroom AV Video Collaboration Managed Service — ₹4,200 / room / month

---

## 7. Featured Enterprise Demo Scenarios

The dataset includes dedicated operational scenarios designed for enterprise demonstrations and testing:

### Scenario 1: Bangalore Mega Tech Refresh (`QT-2026-0001`)
- **Customer**: VertexGrid Technologies Pvt Ltd (`CUST-001`), Kadubeesanahalli, ORR.
- **Order Volume**: 200 Latitude 5440 laptops, 200 WD19S docks, 200 P2422H monitors, 20 Cisco switches, 10 Aruba APs, 4 PowerEdge R660 servers, Zero-Touch Imaging, and 3-Year 24x7 Enterprise AMC.
- **Governance Breach**: Requested laptop discount is **24.0%** (exceeds the 15.0% Enterprise ceiling).
- **Workflow State**: Status: `Pending Approval`, Approval Status: `Pending Sales Manager & Finance Approval`, Deal Health: `Critical` (Dual approval workflow triggered).

### Scenario 2: Executive Smartphone Fleet + MDM Recurring Billing (`QT-2026-0002`)
- **Customer**: Bengaluru Cloud Systems Pvt Ltd (`CUST-002`), EPIP Zone, Whitefield.
- **Order Volume**: 50 Samsung Galaxy S24 smartphones, 50 Anker 737 GaN fast chargers, 50 Cloud Endpoint Mobility Management (MDM) annual subscriptions (`SUB-006`).
- **Workflow State**: Status: `Approved`, Billing Type: `HYBRID` (hardware one-time + annual subscription MRR).

### Scenario 3: Server Fulfillment & Factory Backorder (`QT-2026-0003`)
- **Customer**: BlueOrbit FinTech Solutions Ltd (`CUST-003`), Bellandur, ORR.
- **Requirement**: 12x Dell PowerEdge R760 2U Rackmount Servers.
- **Fulfillment Allocation**:
  - **7 units**: Immediate allocation from Bangalore Central (`BLR-DC-01`).
  - **3 units**: In-transit allocation from incoming OEM shipment (ETA: 5 Days).
  - **2 units**: Factory backorder registered directly with Dell OEM manufacturing supply chain (Lead time: 3 Weeks).
- **Workflow State**: Status: `Confirmed`, Line Fulfillment Status: `ALLOCATED`, `INCOMING_ALLOCATION`, `BACKORDERED`.

### Scenario 4: Multi-Warehouse Split Allocation (`QT-2026-0004`)
- **Customer**: QuantumForge Technologies (`CUST-004`), Bagmane Tech Park.
- **Requirement**: 150 ThinkPad T14 Gen 4 laptops.
- **Fulfillment Split**:
  - **100 units**: Fulfilled immediately from Bangalore Central (`BLR-DC-01`).
  - **50 units**: Fulfilled from Mumbai Port Logistics Center (`MUM-DC-01`) to prevent local stock exhaustion.
- **Workflow State**: Status: `Approved`, Lines reflect dual warehouse fulfillment IDs (`WH-001` and `WH-003`).

### Scenario 5: Customer Discount Counter-Offer / Negotiation (`QT-2026-0005`)
- **Customer**: SiliconArc Systems (`CUST-005`), Bagmane Tech Park.
- **Details**: 35 MacBook Pro 14 M3 Pro laptops. Customer submitted counter-offer requesting 19.0% discount (ceiling is 12.0%).
- **Tracking**: Logged in `negotiations.csv` (`NEG-0001`) with original vs requested discount and business rationale.

### Scenario 6: Stalled Inactive Quotation (`QT-2026-0006`)
- **Customer**: `CUST-012`.
- **Details**: Commercial quote delivered 48 days ago with zero client engagement.
- **Tracking**: Flagged in `deal_health.csv` as `At Risk` (Inactivity score: 48 days).

### Scenario 7: Discount Anomaly Flagged (`QT-2026-0007`)
- **Customer**: `CUST-015`.
- **Details**: 27.5% requested discount on Cisco Enterprise Networking exceeds peer historical median (6.5%) by 21.0%.
- **Tracking**: Routed to Commercial VP with Deal Health `Critical`.

---

## 8. Validation & Verification

Run the comprehensive data validation script to verify all 21 files, relational keys, inventory consistency, and gross margins:

```bash
python validate_seed_data.py
```

### Expected Output Banner
```text
==========================================
DEALFLOW360 — BANGALORE DATA VALIDATION
==========================================
Products:                 265
Variants:                 532
Customers:                 80
Warehouses:                 5
Inventory Records:        1072
Quotations:                80
Quotation Lines:          302
Recommendations:          421
Negotiations:              30

Foreign Key Errors:         0
Duplicate IDs:              0
Duplicate SKUs:             0
Invalid Prices:             0
Invalid Inventory:          0
Invalid Margins:            0

STATUS: PASS
==========================================
```

---

## 9. Generation Scripts

The Bangalore dataset was created using three modular generator scripts:
1. `build_base_blr.py`: Builds brands, categories, warehouses, services, subscriptions, discount governance rules, and 80 authentic Bangalore customer profiles.
2. `build_catalog_blr.py`: Builds 265 enterprise products across 14 categories and 461 base variants.
3. `master_seed_builder_blr.py`: Orchestrates catalog expansion to 532 variants, generates 1,072 inventory rows, 2,128 price list lines, 421 recommendations, 132 service attachment rules, 80 quotations, 302 quotation lines, 30 negotiations, 80 deal health records, 156 audit logs, and 44 hybrid invoices with 172 invoice lines.
