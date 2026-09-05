"""
DealFlow360 Complete Seed Data Generator
Target: Ahmedabad Enterprise Distribution Center (AMD-DC-01)
Generates 16 relational CSV files strictly adhering to DealFlow360 specifications.
"""

import os
import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # Deterministic generation

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed-data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating full DealFlow360 seed data into: {OUTPUT_DIR}")

# ==============================================================================
# 1. BRANDS
# ==============================================================================
BRANDS = [
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

# ==============================================================================
# 2. CATEGORIES
# ==============================================================================
CATEGORIES = [
    ("CAT-COMP", "Computing", "", "Enterprise commercial computing hardware and personal systems", "ACTIVE"),
    ("CAT-INFRA", "Infrastructure", "", "Data center, server, enterprise networking and power systems", "ACTIVE"),
    ("CAT-MOB", "Mobility", "", "Enterprise cellular devices, tablets and workforce mobile endpoints", "ACTIVE"),
    ("CAT-PERIPH", "Peripherals & Collaboration", "", "Displays, unified communication and workplace accessories", "ACTIVE"),

    ("CAT-LAP", "Business Laptops", "CAT-COMP", "Enterprise-grade commercial ultrabooks, laptops and mobile workstations", "ACTIVE"),
    ("CAT-DSK", "Business Desktops", "CAT-COMP", "Enterprise towers, small-form-factor and micro commercial desktops", "ACTIVE"),
    ("CAT-WKS", "Workstations", "CAT-COMP", "High-performance workstations for CAD, 3D, engineering, data science and AI", "ACTIVE"),

    ("CAT-SRV", "Servers", "CAT-INFRA", "Rack, tower, virtualization, high-density compute and storage servers", "ACTIVE"),
    ("CAT-NET", "Networking", "CAT-INFRA", "Enterprise core/access switches, firewalls, routers and wireless controllers", "ACTIVE"),
    ("CAT-STO", "Storage", "CAT-INFRA", "Network attached storage (NAS), SAN arrays, enterprise SSDs and HDDs", "ACTIVE"),
    ("CAT-UPS", "UPS & Power", "CAT-INFRA", "Line-interactive and online double-conversion enterprise UPS systems and PDUs", "ACTIVE"),

    ("CAT-SMP", "Smartphones", "CAT-MOB", "Enterprise smartphones with Knox/MDM and 5G connectivity", "ACTIVE"),
    ("CAT-TAB", "Tablets", "CAT-MOB", "Enterprise, rugged field and executive commercial tablets", "ACTIVE"),

    ("CAT-MON", "Monitors", "CAT-PERIPH", "Commercial FHD, QHD, 4K and USB-C productivity displays", "ACTIVE"),
    ("CAT-PRN", "Printers", "CAT-PERIPH", "Enterprise monochrome and color network laser multifunction printers", "ACTIVE"),
    ("CAT-ACC", "Accessories", "CAT-PERIPH", "Docking stations, input devices, security locks, adapters and bags", "ACTIVE"),
    ("CAT-COL", "Collaboration Equipment", "CAT-PERIPH", "Video conferencing bars, conference room cameras and speakerphones", "ACTIVE"),
    ("CAT-SEC", "Enterprise Cabling & Optics", "CAT-PERIPH", "SFP+ 10G/25G optics, DAC cables, server rail kits and patch panels", "ACTIVE")
]

# ==============================================================================
# 3. WAREHOUSES
# ==============================================================================
WAREHOUSES = [
    ("WH-001", "AMD-DC-01", "Ahmedabad Enterprise Distribution Center", "Ahmedabad", "Gujarat", "India", "CENTRAL_DISTRIBUTION_CENTER", "Rajesh Patel", 75000, "ACTIVE"),
    ("WH-002", "BOM-DC-01", "Mumbai Western Regional Logistics Hub", "Mumbai", "Maharashtra", "India", "REGIONAL_WAREHOUSE", "Vikram Deshmukh", 90000, "ACTIVE"),
    ("WH-003", "BLR-DC-01", "Bengaluru Tech Fulfillment Depot", "Bengaluru", "Karnataka", "India", "REGIONAL_WAREHOUSE", "Ananya Rao", 65000, "ACTIVE"),
    ("WH-004", "DEL-DC-01", "Delhi NCR Enterprise Supply Hub", "Gurugram", "Haryana", "India", "REGIONAL_WAREHOUSE", "Amit Sharma", 80000, "ACTIVE"),
    ("WH-005", "HYD-DC-01", "Hyderabad Cyber Logistics Center", "Hyderabad", "Telangana", "India", "REGIONAL_WAREHOUSE", "Srinivas Reddy", 50000, "ACTIVE")
]

# ==============================================================================
# 4. SERVICES
# ==============================================================================
SERVICES = [
    ("SRV-001", "SRV-INS-RACK", "Enterprise Server & Rack Installation", "HARDWARE_DEPLOYMENT", "Mounting server in 19-inch rack, dual PDU cabling, cable dressing, and power-on verification", 4500.0, 7500.0, 18.0, 35.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-002", "SRV-DEP-HYPER", "Hypervisor & OS Provisioning", "INFRASTRUCTURE_CONFIGURATION", "Installation and hardening of VMware ESXi, Proxmox, or Windows Server 2022 with base clustering", 8000.0, 14500.0, 18.0, 40.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-003", "SRV-NET-VLAN", "L2/L3 Network & VLAN Setup", "NETWORK_ENGINEERING", "VLAN segmentation, trunking, spanning-tree protocol, inter-VLAN routing and ACL configuration", 7000.0, 12000.0, 18.0, 38.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-004", "SRV-FW-SEC", "Next-Gen Firewall Policy & VPN Setup", "CYBERSECURITY", "Deployment of Fortinet/Cisco firewall, IPsec site-to-site VPN, SSL-VPN and UTM threat filtering", 11000.0, 19500.0, 18.0, 42.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-005", "SRV-LAP-DEP", "Enterprise Laptop Zero-Touch Imaging", "ENDPOINT_DEPLOYMENT", "Pre-provisioning with corporate Gold Master image, domain join, BitLocker encryption and asset tagging", 650.0, 1200.0, 18.0, 45.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-006", "SRV-MIG-DATA", "Enterprise Storage & Data Migration", "STORAGE_SERVICES", "Block-level or file-level replication and cutover to new NAS/SAN array with minimal downtime", 18000.0, 32000.0, 18.0, 40.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-007", "SRV-WIFI-SURV", "Wi-Fi Site Survey & Heatmap Tuning", "WIRELESS_SERVICES", "Physical RF spectrum analysis, AP placement verification, channel bonding and signal optimization", 12000.0, 22000.0, 18.0, 42.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-008", "SRV-TRN-ADMIN", "Enterprise Admin Systems Training", "TRAINING_ENABLEMENT", "Half-day specialized administrator training on hardware monitoring, iDRAC/iLO and troubleshooting", 6000.0, 11000.0, 18.0, 45.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-009", "SRV-PM-SEMI", "Semi-Annual Preventive Maintenance", "MAINTENANCE", "Bi-annual on-site inspection, chassis de-dusting, fan testing, thermal paste check and firmware review", 5000.0, 9000.0, 18.0, 40.0, True, "SEMI_ANNUALLY", "ACTIVE"),
    ("SRV-010", "SRV-ONS-ENG", "Dedicated L2 Field Support Engineer", "MANAGED_STAFFING", "Certified on-site technical engineer for full 8-hour dispatch (hardware swap, troubleshooting)", 3500.0, 6500.0, 18.0, 45.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-011", "SRV-SAN-LUN", "Storage SAN/NAS LUN Provisioning", "STORAGE_SERVICES", "RAID array layout, iSCSI/NFS target mapping, MPIO setup and snapshot schedule configuration", 9500.0, 16800.0, 18.0, 40.0, False, "ONE_TIME", "ACTIVE"),
    ("SRV-012", "SRV-AUD-FIRM", "Firmware & Security Compliance Audit", "AUDIT_SERVICES", "Full hardware audit, BIOS/IPMI vulnerability scanning and automated remediation roadmap", 15000.0, 26000.0, 18.0, 42.0, False, "ONE_TIME", "ACTIVE")
]

# ==============================================================================
# 5. SUBSCRIPTION PLANS
# ==============================================================================
SUBSCRIPTION_PLANS = [
    ("SUB-001", "SUB-AMC-CMP", "Comprehensive Enterprise AMC (4hr SLA)", "ANNUALLY", 1, 48000.0, 5000.0, True, "30_DAYS_WRITTEN_NOTICE", "PRORATED_REFUND", "ACTIVE"),
    ("SUB-002", "SUB-AMC-NCMP", "Non-Comprehensive AMC (Labour Only)", "ANNUALLY", 1, 22000.0, 2500.0, True, "30_DAYS_WRITTEN_NOTICE", "PRORATED_REFUND", "ACTIVE"),
    ("SUB-003", "SUB-NOC-247", "24x7 Enterprise Infrastructure NOC Monitoring", "MONTHLY", 1, 8500.0, 3000.0, True, "IMMEDIATE_END_OF_CYCLE", "NO_REFUND", "ACTIVE"),
    ("SUB-004", "SUB-BAAS-1TB", "Managed Cloud Backup BaaS - 1 TB", "MONTHLY", 1, 1800.0, 1000.0, True, "IMMEDIATE_END_OF_CYCLE", "NO_REFUND", "ACTIVE"),
    ("SUB-005", "SUB-BAAS-10TB", "Enterprise Cloud Backup BaaS - 10 TB", "MONTHLY", 1, 14000.0, 3500.0, True, "30_DAYS_WRITTEN_NOTICE", "PRORATED_REFUND", "ACTIVE"),
    ("SUB-006", "SUB-MDM-SEAT", "Cloud Endpoint Mobility Management (Per Seat)", "ANNUALLY", 1, 2400.0, 0.0, True, "IMMEDIATE_END_OF_CYCLE", "NO_REFUND", "ACTIVE"),
    ("SUB-007", "SUB-EDR-SEAT", "Enterprise Endpoint Detection & Response (Per Seat)", "ANNUALLY", 1, 3800.0, 0.0, True, "IMMEDIATE_END_OF_CYCLE", "NO_REFUND", "ACTIVE"),
    ("SUB-008", "SUB-SOC-SRV", "Managed SOC Threat Hunting (Per Server Node)", "MONTHLY", 1, 4200.0, 2000.0, True, "30_DAYS_WRITTEN_NOTICE", "PRORATED_REFUND", "ACTIVE")
]

# ==============================================================================
# 6. DISCOUNT RULES
# ==============================================================================
DISCOUNT_RULES = [
    # Strategic Tier (Highest leeway)
    ("DR-001", "Strategic", "CAT-COMP", 22.0, 8.0, "L3_VP_COMMERCIAL", "MEDIUM", True),
    ("DR-002", "Strategic", "CAT-INFRA", 18.0, 10.0, "L3_VP_COMMERCIAL", "MEDIUM", True),
    ("DR-003", "Strategic", "CAT-MOB", 12.0, 6.0, "L2_SALES_DIRECTOR", "LOW", True),
    ("DR-004", "Strategic", "CAT-PERIPH", 20.0, 12.0, "L2_SALES_DIRECTOR", "LOW", True),
    ("DR-005", "Strategic", "CAT-LAP", 22.0, 8.0, "L3_VP_COMMERCIAL", "MEDIUM", True),
    ("DR-006", "Strategic", "CAT-SRV", 18.0, 10.0, "L3_VP_COMMERCIAL", "HIGH", True),
    ("DR-007", "Strategic", "CAT-NET", 18.0, 11.0, "L2_SALES_DIRECTOR", "LOW", True),
    ("DR-008", "Strategic", "CAT-ACC", 25.0, 15.0, "L1_SALES_LEAD", "LOW", True),

    # Enterprise Tier
    ("DR-009", "Enterprise", "CAT-COMP", 15.0, 11.0, "L2_SALES_DIRECTOR", "MEDIUM", True),
    ("DR-010", "Enterprise", "CAT-INFRA", 14.0, 12.0, "L2_SALES_DIRECTOR", "MEDIUM", True),
    ("DR-011", "Enterprise", "CAT-MOB", 8.0, 7.0, "L2_SALES_DIRECTOR", "MEDIUM", True),
    ("DR-012", "Enterprise", "CAT-PERIPH", 12.0, 15.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-013", "Enterprise", "CAT-LAP", 15.0, 11.0, "L2_SALES_DIRECTOR", "MEDIUM", True),
    ("DR-014", "Enterprise", "CAT-SRV", 14.0, 12.0, "L2_SALES_DIRECTOR", "HIGH", True),
    ("DR-015", "Enterprise", "CAT-NET", 12.0, 13.0, "L2_SALES_DIRECTOR", "LOW", True),
    ("DR-016", "Enterprise", "CAT-ACC", 15.0, 18.0, "L1_SALES_LEAD", "LOW", True),

    # SMB Tier
    ("DR-017", "SMB", "CAT-COMP", 8.0, 14.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-018", "SMB", "CAT-INFRA", 7.0, 15.0, "L2_SALES_DIRECTOR", "MEDIUM", True),
    ("DR-019", "SMB", "CAT-MOB", 5.0, 8.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-020", "SMB", "CAT-PERIPH", 8.0, 18.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-021", "SMB", "CAT-LAP", 8.0, 14.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-022", "SMB", "CAT-SRV", 7.0, 15.0, "L2_SALES_DIRECTOR", "HIGH", True),
    ("DR-023", "SMB", "CAT-NET", 8.0, 16.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-024", "SMB", "CAT-ACC", 10.0, 20.0, "L1_SALES_LEAD", "LOW", True),

    # Standard Tier (Default/List price baseline)
    ("DR-025", "Standard", "CAT-COMP", 3.0, 16.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-026", "Standard", "CAT-INFRA", 3.0, 17.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-027", "Standard", "CAT-MOB", 2.0, 10.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-028", "Standard", "CAT-PERIPH", 4.0, 20.0, "L1_SALES_LEAD", "LOW", True)
]

# ==============================================================================
# 7. CUSTOMERS (35-45 Indian Enterprise B2B Customers)
# ==============================================================================
CUSTOMERS_DATA = [
    # Strategic Tier
    ("CUST-001", "AIS-IND-01", "Arvind Industrial Systems Pvt Ltd", "Manufacturing", "Enterprise", "Ahmedabad", "Gujarat", "India", "Plot 42, Naroda GIDC Phase II, Ahmedabad 382330", "Plot 42, Naroda GIDC Phase II, Ahmedabad 382330", 50000000.0, 60, "Kavita Sharma", "ACTIVE"),
    ("CUST-002", "GPE-ENG-02", "Gujarat Precision Engineering Pvt Ltd", "Manufacturing", "Enterprise", "Vadodara", "Gujarat", "India", "Survey 118, Makarpura Industrial Estate, Vadodara 390010", "Survey 118, Makarpura Industrial Estate, Vadodara 390010", 35000000.0, 45, "Manish Mehta", "ACTIVE"),
    ("CUST-003", "SLS-LOG-03", "Sabarmati Logistics & Supply Chain Ltd", "Logistics", "Enterprise", "Ahmedabad", "Gujarat", "India", "Logistics Park, Aslali Bypass, Ahmedabad 382427", "Logistics Park, Aslali Bypass, Ahmedabad 382427", 40000000.0, 45, "Kavita Sharma", "ACTIVE"),
    ("CUST-004", "WGT-INF-04", "Western Grid Technologies Pvt Ltd", "IT Services", "Strategic", "Gandhinagar", "Gujarat", "India", "Block 9, Infocity Superstructure, Gandhinagar 382007", "Block 9, Infocity Superstructure, Gandhinagar 382007", 80000000.0, 60, "Rahul Verma", "ACTIVE"),
    ("CUST-005", "THS-PHR-05", "Torrential Health Sciences Pvt Ltd", "Pharma", "Strategic", "Ahmedabad", "Gujarat", "India", "Pharma SEZ, Changodar Highway, Ahmedabad 382213", "Pharma SEZ, Changodar Highway, Ahmedabad 382213", 100000000.0, 90, "Rahul Verma", "ACTIVE"),
    ("CUST-006", "ZBA-BIO-06", "Zydus Bio-Analytics Systems", "Pharma", "Enterprise", "Ahmedabad", "Gujarat", "India", "Sarkhej-Bavla Road, Moraiya, Ahmedabad 382210", "Sarkhej-Bavla Road, Moraiya, Ahmedabad 382210", 60000000.0, 60, "Kavita Sharma", "ACTIVE"),
    ("CUST-007", "NIP-PET-07", "Narmada Infrastructure & Petrochem Ltd", "Manufacturing", "Enterprise", "Bharuch", "Gujarat", "India", "Dahej SEZ Part 1, Vagra Taluka, Bharuch 392130", "Dahej SEZ Part 1, Vagra Taluka, Bharuch 392130", 45000000.0, 45, "Manish Mehta", "ACTIVE"),
    ("CUST-008", "MGD-SRV-08", "Maru Gujarat Digital Services Pvt Ltd", "IT Services", "SMB", "Surat", "Gujarat", "India", "Ring Road Diamond Point, Surat 395002", "Ring Road Diamond Point, Surat 395002", 15000000.0, 30, "Pooja Desai", "ACTIVE"),
    ("CUST-009", "AGB-BPO-09", "Apex Global BPO Solutions Pvt Ltd", "IT Services", "Enterprise", "Mumbai", "Maharashtra", "India", "Mindspace IT Park, Malad West, Mumbai 400064", "Mindspace IT Park, Malad West, Mumbai 400064", 75000000.0, 60, "Sunil Joshi", "ACTIVE"),
    ("CUST-010", "BFA-FIN-10", "Bharat Financial Analytics Ltd", "BFSI", "Strategic", "Mumbai", "Maharashtra", "India", "Bandra Kurla Complex, G-Block, Mumbai 400051", "Bandra Kurla Complex, G-Block, Mumbai 400051", 120000000.0, 60, "Sunil Joshi", "ACTIVE"),
    ("CUST-011", "DHI-INF-11", "Deccan Horizon InfoTech Pvt Ltd", "IT Services", "Enterprise", "Pune", "Maharashtra", "India", "Hinjawadi Phase 2, Rajiv Gandhi Infotech Park, Pune 411057", "Hinjawadi Phase 2, Rajiv Gandhi Infotech Park, Pune 411057", 55000000.0, 45, "Sunil Joshi", "ACTIVE"),
    ("CUST-012", "SMF-COR-12", "Sterling Micro-Fintech Corp", "BFSI", "Enterprise", "Mumbai", "Maharashtra", "India", "Naman Chambers, C-32 G Block BKC, Mumbai 400051", "Naman Chambers, C-32 G Block BKC, Mumbai 400051", 50000000.0, 45, "Sunil Joshi", "ACTIVE"),
    ("CUST-013", "KLW-LOG-13", "Kalinga Logistics & Warehousing Pvt Ltd", "Logistics", "SMB", "Navi Mumbai", "Maharashtra", "India", "Taloja MIDC Sector 14, Navi Mumbai 410208", "Taloja MIDC Sector 14, Navi Mumbai 410208", 20000000.0, 30, "Pooja Desai", "ACTIVE"),
    ("CUST-014", "KTP-OPS-14", "Karnavati Tech Park Operations Pvt Ltd", "Real Estate", "SMB", "Ahmedabad", "Gujarat", "India", "SG Highway, Makarba, Ahmedabad 380051", "SG Highway, Makarba, Ahmedabad 380051", 18000000.0, 30, "Pooja Desai", "ACTIVE"),
    ("CUST-015", "MHS-HLT-15", "Meridian Healthcare Systems Ltd", "Healthcare", "Strategic", "Bengaluru", "Karnataka", "India", "Electronic City Phase 1, Hosur Road, Bengaluru 560100", "Electronic City Phase 1, Hosur Road, Bengaluru 560100", 90000000.0, 60, "Deepak Nair", "ACTIVE"),
    ("CUST-016", "CCT-CLD-16", "Cauvery Cloud Technologies Pvt Ltd", "IT Services", "Enterprise", "Bengaluru", "Karnataka", "India", "Whitefield Main Road, EPIP Zone, Bengaluru 560066", "Whitefield Main Road, EPIP Zone, Bengaluru 560066", 65000000.0, 45, "Deepak Nair", "ACTIVE"),
    ("CUST-017", "SSE-EMB-17", "Silicon South Embedded Labs", "IT Services", "SMB", "Bengaluru", "Karnataka", "India", "Outer Ring Road, Bellandur, Bengaluru 560103", "Outer Ring Road, Bellandur, Bengaluru 560103", 25000000.0, 30, "Deepak Nair", "ACTIVE"),
    ("CUST-018", "TCG-CYB-18", "Telengana Cyber Grid Solutions", "IT Services", "Enterprise", "Hyderabad", "Telangana", "India", "Hitec City, Madhapur, Hyderabad 500081", "Hitec City, Madhapur, Hyderabad 500081", 60000000.0, 60, "Vikram Sen", "ACTIVE"),
    ("CUST-019", "NFS-SOL-19", "Nizami FinServe Solutions Pvt Ltd", "BFSI", "SMB", "Hyderabad", "Telangana", "India", "Financial District, Nanakramguda, Hyderabad 500032", "Financial District, Nanakramguda, Hyderabad 500032", 30000000.0, 30, "Vikram Sen", "ACTIVE"),
    ("CUST-020", "GAT-AGR-20", "Godavari AgriTech Solutions Pvt Ltd", "Logistics", "SMB", "Rajahmundry", "Andhra Pradesh", "India", "Industrial Corridor, Morampudi, Rajahmundry 533107", "Industrial Corridor, Morampudi, Rajahmundry 533107", 12000000.0, 30, "Vikram Sen", "ACTIVE"),
    ("CUST-021", "IPC-CON-21", "Indraprastha IT Consulting LLP", "IT Services", "Enterprise", "Gurugram", "Haryana", "India", "Cyber City Building 10, DLF Phase 2, Gurugram 122002", "Cyber City Building 10, DLF Phase 2, Gurugram 122002", 70000000.0, 45, "Siddharth Khanna", "ACTIVE"),
    ("CUST-022", "DCH-NET-22", "Delhi Capital Hospital Network", "Healthcare", "Enterprise", "New Delhi", "Delhi", "India", "Institutional Area, Saket, New Delhi 110017", "Institutional Area, Saket, New Delhi 110017", 55000000.0, 45, "Siddharth Khanna", "ACTIVE"),
    ("CUST-023", "NPR-ROB-23", "Noida Precision Robotics Pvt Ltd", "Manufacturing", "SMB", "Noida", "Uttar Pradesh", "India", "Sector 62 Institutional Area, Noida 201309", "Sector 62 Institutional Area, Noida 201309", 22000000.0, 30, "Siddharth Khanna", "ACTIVE"),
    ("CUST-024", "HAL-AGR-24", "Haryana Agro Logistics Corp", "Logistics", "SMB", "Faridabad", "Haryana", "India", "Mathura Road, Sector 31, Faridabad 121003", "Mathura Road, Sector 31, Faridabad 121003", 15000000.0, 30, "Siddharth Khanna", "ACTIVE"),
    ("CUST-025", "CMS-MAR-25", "Coromandel Maritime Solutions Ltd", "Logistics", "Enterprise", "Chennai", "Tamil Nadu", "India", "Rajiv Gandhi Salai, OMR, Sholinganallur, Chennai 600119", "Rajiv Gandhi Salai, OMR, Sholinganallur, Chennai 600119", 48000000.0, 45, "Deepak Nair", "ACTIVE"),
    ("CUST-026", "CFA-FIN-26", "Chola Financial Advisory Services", "BFSI", "SMB", "Chennai", "Tamil Nadu", "India", "Anna Salai, Mount Road, Chennai 600002", "Anna Salai, Mount Road, Chennai 600002", 18000000.0, 30, "Deepak Nair", "ACTIVE"),
    ("CUST-027", "ROH-HSP-27", "Royal Orchid Hospitality Group", "Hospitality", "Enterprise", "Jaipur", "Rajasthan", "India", "Tonk Road, Durgapura, Jaipur 302018", "Tonk Road, Durgapura, Jaipur 302018", 32000000.0, 45, "Manish Mehta", "ACTIVE"),
    ("CUST-028", "MHE-ENG-28", "Mewar Heavy Engineering Ltd", "Manufacturing", "Enterprise", "Udaipur", "Rajasthan", "India", "Sukher Industrial Area, Udaipur 313004", "Sukher Industrial Area, Udaipur 313004", 42000000.0, 45, "Manish Mehta", "ACTIVE"),
    ("CUST-029", "KPW-LOG-29", "Kolkata Port Warehousing Services", "Logistics", "SMB", "Kolkata", "West Bengal", "India", "Strand Road, Fairlie Place, Kolkata 700001", "Strand Road, Fairlie Place, Kolkata 700001", 16000000.0, 30, "Siddharth Khanna", "ACTIVE"),
    ("CUST-030", "EPD-POW-30", "Eastern Power Distribution Equipment Ltd", "Manufacturing", "Strategic", "Durgapur", "West Bengal", "India", "Muchipara Industrial Zone, Durgapur 713212", "Muchipara Industrial Zone, Durgapur 713212", 85000000.0, 60, "Siddharth Khanna", "ACTIVE"),
    ("CUST-031", "SVI-INF-31", "Saurashtra Valves & Instruments Ltd", "Manufacturing", "SMB", "Rajkot", "Gujarat", "India", "Aji GIDC Industrial Estate, Rajkot 360003", "Aji GIDC Industrial Estate, Rajkot 360003", 14000000.0, 30, "Pooja Desai", "ACTIVE"),
    ("CUST-032", "KCR-CER-32", "Kutch Ceramics & Tiles Consortium", "Manufacturing", "Enterprise", "Morbi", "Gujarat", "India", "National Highway 8A, Trajpar, Morbi 363642", "National Highway 8A, Trajpar, Morbi 363642", 38000000.0, 45, "Manish Mehta", "ACTIVE"),
    ("CUST-033", "AEC-EDU-33", "Ahmedabad Education City Foundation", "Education", "Enterprise", "Ahmedabad", "Gujarat", "India", "Drive-In Road, Thaltej, Ahmedabad 380054", "Drive-In Road, Thaltej, Ahmedabad 380054", 30000000.0, 45, "Kavita Sharma", "ACTIVE"),
    ("CUST-034", "GEC-GOV-34", "Gujarat Energy Transmission Infra Corp", "Government", "Strategic", "Vadodara", "Gujarat", "India", "Sardar Patel Vidyut Bhavan, Race Course, Vadodara 390007", "Sardar Patel Vidyut Bhavan, Race Course, Vadodara 390007", 150000000.0, 90, "Rahul Verma", "ACTIVE"),
    ("CUST-035", "VMD-MED-35", "Vallabh Medical Diagnostic Centers", "Healthcare", "SMB", "Surat", "Gujarat", "India", "Majura Gate, Ring Road, Surat 395001", "Majura Gate, Ring Road, Surat 395001", 20000000.0, 30, "Pooja Desai", "ACTIVE"),
    ("CUST-036", "PLX-PHR-36", "Pinnacle Laboratories & Diagnostics", "Pharma", "Enterprise", "Ahmedabad", "Gujarat", "India", "Sanand GIDC Phase II, Ahmedabad 382110", "Sanand GIDC Phase II, Ahmedabad 382110", 42000000.0, 45, "Kavita Sharma", "ACTIVE"),
    ("CUST-037", "TRI-RET-37", "Trinity Retail Hypermarkets Pvt Ltd", "Retail", "Enterprise", "Mumbai", "Maharashtra", "India", "Kurla West, LBS Marg, Mumbai 400070", "Kurla West, LBS Marg, Mumbai 400070", 52000000.0, 45, "Sunil Joshi", "ACTIVE"),
    ("CUST-038", "BLS-LOG-38", "BlueLine Shipping & Container Yards", "Logistics", "Enterprise", "Kandla", "Gujarat", "India", "Port Road, New Kandla, Gandhidham 370210", "Port Road, New Kandla, Gandhidham 370210", 46000000.0, 45, "Manish Mehta", "ACTIVE"),
    ("CUST-039", "VSH-HSP-39", "Vanguard Star Hospitalities Pvt Ltd", "Hospitality", "SMB", "Goa", "Goa", "India", "Miramar Beach Road, Panaji 403001", "Miramar Beach Road, Panaji 403001", 16000000.0, 30, "Sunil Joshi", "ACTIVE"),
    ("CUST-040", "SBT-TEX-40", "Sabarmati Textiles & Weaving Mills", "Manufacturing", "Enterprise", "Ahmedabad", "Gujarat", "India", "Amraiwadi Industrial Estate, Ahmedabad 380026", "Amraiwadi Industrial Estate, Ahmedabad 380026", 36000000.0, 45, "Kavita Sharma", "ACTIVE")
]

print(f"Loaded {len(CUSTOMERS_DATA)} Indian enterprise customers.")
