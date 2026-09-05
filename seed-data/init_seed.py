"""
DealFlow360 Seed Data Generator
Enterprise IT Hardware & Technology Procurement
Target: Ahmedabad Enterprise Distribution Center (AMD-DC-01)
Generates 16 relational CSV files adhering strictly to the DealFlow360 enterprise data requirements.
"""

import os
import csv
import json
import random
from datetime import datetime, timedelta

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed-data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating DealFlow360 seed data into: {OUTPUT_DIR}")

# ==============================================================================
# 1. BRANDS
# ==============================================================================
BRANDS_DATA = [
    ("BRD-001", "Dell Technologies", "DELL", "USA", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-002", "Hewlett Packard Enterprise", "HPE", "USA", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-003", "HP Inc.", "HP", "USA", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-004", "Lenovo Group Ltd", "LENOVO", "Hong Kong", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-005", "Apple Inc.", "APPLE", "USA", "ENTERPRISE_GOLD", "ACTIVE"),
    ("BRD-006", "Cisco Systems", "CISCO", "USA", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-007", "Aruba Networks (HPE)", "ARUBA", "USA", "ENTERPRISE_GOLD", "ACTIVE"),
    ("BRD-008", "Ubiquiti Networks", "UBIQUITI", "USA", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-009", "Fortinet Inc.", "FORTINET", "USA", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-010", "TP-Link Technologies", "TPLINK", "China", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-011", "Synology Inc.", "SYNOLOGY", "Taiwan", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-012", "QNAP Systems", "QNAP", "Taiwan", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-013", "Samsung Electronics", "SAMSUNG", "South Korea", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-014", "Western Digital", "WD", "USA", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-015", "Kingston Technology", "KINGSTON", "USA", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-016", "LG Electronics", "LG", "South Korea", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-017", "Schneider Electric (APC)", "APC", "France", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-018", "Eaton Corporation", "EATON", "USA", "ENTERPRISE_GOLD", "ACTIVE"),
    ("BRD-019", "Vertiv Holdings", "VERTIV", "USA", "ENTERPRISE_PLATINUM", "ACTIVE"),
    ("BRD-020", "Canon Inc.", "CANON", "Japan", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-021", "Epson Corporation", "EPSON", "Japan", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-022", "Brother Industries", "BROTHER", "Japan", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-023", "Google LLC", "GOOGLE", "USA", "COMMERCIAL_GOLD", "ACTIVE"),
    ("BRD-024", "OnePlus Technology", "ONEPLUS", "China", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-025", "ASUS Commercial", "ASUS", "Taiwan", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-026", "Acer Commercial", "ACER", "Taiwan", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-027", "Logitech International", "LOGITECH", "Switzerland", "ENTERPRISE_GOLD", "ACTIVE"),
    ("BRD-028", "Jabra (GN Audio)", "JABRA", "Denmark", "ENTERPRISE_GOLD", "ACTIVE"),
    ("BRD-029", "Poly (HP Poly)", "POLY", "USA", "ENTERPRISE_GOLD", "ACTIVE"),
    ("BRD-030", "Netgear Enterprise", "NETGEAR", "USA", "COMMERCIAL_SILVER", "ACTIVE")
]

def write_brands():
    path = os.path.join(OUTPUT_DIR, "brands.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["brand_id", "brand_name", "brand_code", "country", "support_level", "status"])
        for b in BRANDS_DATA:
            writer.writerow(b)
    print(f"Written brands.csv ({len(BRANDS_DATA)} rows)")

# ==============================================================================
# 2. CATEGORIES
# ==============================================================================
CATEGORIES_DATA = [
    # Top-level
    ("CAT-COMP", "Computing", "", "Enterprise commercial computing hardware and personal systems", "ACTIVE"),
    ("CAT-INFRA", "Infrastructure", "", "Data center, server, enterprise networking and power systems", "ACTIVE"),
    ("CAT-MOB", "Mobility", "", "Enterprise cellular devices, tablets and workforce mobile endpoints", "ACTIVE"),
    ("CAT-PERIPH", "Peripherals & Collaboration", "", "Displays, unified communication and workplace accessories", "ACTIVE"),

    # Subcategories under Computing
    ("CAT-LAP", "Business Laptops", "CAT-COMP", "Enterprise-grade commercial ultrabooks, laptops and mobile workstations", "ACTIVE"),
    ("CAT-DSK", "Business Desktops", "CAT-COMP", "Enterprise towers, small-form-factor and micro commercial desktops", "ACTIVE"),
    ("CAT-WKS", "Workstations", "CAT-COMP", "High-performance workstations for CAD, 3D, engineering, data science and AI", "ACTIVE"),

    # Subcategories under Infrastructure
    ("CAT-SRV", "Servers", "CAT-INFRA", "Rack, tower, virtualization, high-density compute and storage servers", "ACTIVE"),
    ("CAT-NET", "Networking", "CAT-INFRA", "Enterprise core/access switches, firewalls, routers and wireless controllers", "ACTIVE"),
    ("CAT-STO", "Storage", "CAT-INFRA", "Network attached storage (NAS), SAN arrays, enterprise SSDs and HDDs", "ACTIVE"),
    ("CAT-UPS", "UPS & Power", "CAT-INFRA", "Line-interactive and online double-conversion enterprise UPS systems and PDUs", "ACTIVE"),

    # Subcategories under Mobility
    ("CAT-SMP", "Smartphones", "CAT-MOB", "Enterprise smartphones with Knox/MDM and 5G connectivity", "ACTIVE"),
    ("CAT-TAB", "Tablets", "CAT-MOB", "Enterprise, rugged field and executive commercial tablets", "ACTIVE"),

    # Subcategories under Peripherals & Collaboration
    ("CAT-MON", "Monitors", "CAT-PERIPH", "Commercial FHD, QHD, 4K and USB-C productivity displays", "ACTIVE"),
    ("CAT-PRN", "Printers", "CAT-PERIPH", "Enterprise monochrome and color network laser multifunction printers", "ACTIVE"),
    ("CAT-ACC", "Accessories", "CAT-PERIPH", "Docking stations, input devices, security locks, adapters and bags", "ACTIVE"),
    ("CAT-COL", "Collaboration Equipment", "CAT-PERIPH", "Video conferencing bars, conference room cameras and speakerphones", "ACTIVE"),
    ("CAT-SEC", "Enterprise Cabling & Optics", "CAT-PERIPH", "SFP+ 10G/25G optics, DAC cables, server rail kits and patch panels", "ACTIVE")
]

def write_categories():
    path = os.path.join(OUTPUT_DIR, "categories.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category_id", "category_name", "parent_category_id", "description", "status"])
        for c in CATEGORIES_DATA:
            writer.writerow(c)
    print(f"Written categories.csv ({len(CATEGORIES_DATA)} rows)")

# ==============================================================================
# 3. WAREHOUSES
# ==============================================================================
WAREHOUSES_DATA = [
    ("WH-001", "AMD-DC-01", "Ahmedabad Enterprise Distribution Center", "Ahmedabad", "Gujarat", "India", "CENTRAL_DISTRIBUTION_CENTER", "Rajesh Patel", 75000, "ACTIVE"),
    ("WH-002", "BOM-DC-01", "Mumbai Western Regional Logistics Hub", "Mumbai", "Maharashtra", "India", "REGIONAL_WAREHOUSE", "Vikram Deshmukh", 90000, "ACTIVE"),
    ("WH-003", "BLR-DC-01", "Bengaluru Tech Fulfillment Depot", "Bengaluru", "Karnataka", "India", "REGIONAL_WAREHOUSE", "Ananya Rao", 65000, "ACTIVE"),
    ("WH-004", "DEL-DC-01", "Delhi NCR Enterprise Supply Hub", "Gurugram", "Haryana", "India", "REGIONAL_WAREHOUSE", "Amit Sharma", 80000, "ACTIVE"),
    ("WH-005", "HYD-DC-01", "Hyderabad Cyber Logistics Center", "Hyderabad", "Telangana", "India", "REGIONAL_WAREHOUSE", "Srinivas Reddy", 50000, "ACTIVE")
]

def write_warehouses():
    path = os.path.join(OUTPUT_DIR, "warehouses.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["warehouse_id", "warehouse_code", "warehouse_name", "city", "state", "country", "warehouse_type", "manager_name", "capacity_units", "status"])
        for w in WAREHOUSES_DATA:
            writer.writerow(w)
    print(f"Written warehouses.csv ({len(WAREHOUSES_DATA)} rows)")

if __name__ == "__main__":
    write_brands()
    write_categories()
    write_warehouses()
