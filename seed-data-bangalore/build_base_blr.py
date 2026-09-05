"""
DealFlow360 Bangalore Enterprise Base Data Definition
Target: Bangalore Enterprise Technology Distribution Center (BLR-DC-01)
Defines Brands, Categories, Warehouses, Services, Subscriptions, Discount Rules, and Customers.
"""

import os
import random

# ==============================================================================
# 1. BRANDS (32 Enterprise OEMs & Manufacturers)
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
    ("BRD-030", "Netgear Enterprise", "NETGEAR", "USA", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-031", "BenQ Commercial", "BENQ", "Taiwan", "COMMERCIAL_SILVER", "ACTIVE"),
    ("BRD-032", "Micron Technology", "MICRON", "USA", "COMMERCIAL_GOLD", "ACTIVE")
]

# ==============================================================================
# 2. CATEGORIES (4 Parent + 14 Leaf Categories)
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
# 3. WAREHOUSES (Bangalore Central Distribution Center + Regional Hubs)
# ==============================================================================
WAREHOUSES = [
    ("WH-001", "BLR-DC-01", "Bangalore Enterprise Technology Distribution Center", "Bangalore", "Karnataka", "India", "Enterprise Distribution Center", "Kiran Murthy", 100000, "ACTIVE"),
    ("WH-002", "AMD-DC-01", "Ahmedabad Enterprise Logistics Depot", "Ahmedabad", "Gujarat", "India", "REGIONAL_WAREHOUSE", "Rajesh Patel", 75000, "ACTIVE"),
    ("WH-003", "MUM-DC-01", "Mumbai Western Logistics Hub", "Mumbai", "Maharashtra", "India", "REGIONAL_WAREHOUSE", "Vikram Deshmukh", 90000, "ACTIVE"),
    ("WH-004", "DEL-DC-01", "Delhi NCR Tech Supply Hub", "Gurugram", "Haryana", "India", "REGIONAL_WAREHOUSE", "Amit Sharma", 80000, "ACTIVE"),
    ("WH-005", "HYD-DC-01", "Hyderabad Tech Logistics Center", "Hyderabad", "Telangana", "India", "REGIONAL_WAREHOUSE", "Srinivas Reddy", 60000, "ACTIVE")
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
# 6. DISCOUNT RULES (Tiered governance across customer tiers and categories)
# ==============================================================================
DISCOUNT_RULES = [
    # Strategic Tier
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

    # Standard Tier
    ("DR-025", "Standard", "CAT-COMP", 3.0, 16.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-026", "Standard", "CAT-INFRA", 3.0, 17.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-027", "Standard", "CAT-MOB", 2.0, 10.0, "L1_SALES_LEAD", "LOW", True),
    ("DR-028", "Standard", "CAT-PERIPH", 4.0, 20.0, "L1_SALES_LEAD", "LOW", True)
]

# ==============================================================================
# 7. BANGALORE ENTERPRISE CUSTOMERS (80 Authentic Fictional Accounts)
# ==============================================================================
CUSTOMERS_DATA = [
    # Strategic Tier (Mega Bangalore Tech & Enterprise Accounts)
    ("CUST-001", "VGT-BLR-01", "VertexGrid Technologies Pvt Ltd", "IT Services", "Strategic", "Bangalore", "Karnataka", "India", "Campus 4B, Ecospace Business Park, Outer Ring Road, Bellandur, Bangalore 560103", "Campus 4B, Ecospace Business Park, Outer Ring Road, Bellandur, Bangalore 560103", 150000000.0, 60, "Rohan Sengupta", "ACTIVE"),
    ("CUST-002", "BCS-CLD-02", "Bengaluru Cloud Systems Pvt Ltd", "SaaS", "Strategic", "Bangalore", "Karnataka", "India", "Block 7, Bagmane Tech Park, CV Raman Nagar, Bangalore 560093", "Block 7, Bagmane Tech Park, CV Raman Nagar, Bangalore 560093", 120000000.0, 60, "Priya Sundaram", "ACTIVE"),
    ("CUST-003", "BOF-FIN-03", "BlueOrbit FinTech Solutions Ltd", "FinTech", "Strategic", "Bangalore", "Karnataka", "India", "Prestige Tech Park IV, Marathahalli-Sarjapur Ring Road, Bangalore 560103", "Prestige Tech Park IV, Marathahalli-Sarjapur Ring Road, Bangalore 560103", 140000000.0, 60, "Rohan Sengupta", "ACTIVE"),
    ("CUST-004", "QFT-TEC-04", "QuantumForge Technologies India Pvt Ltd", "Semiconductor", "Strategic", "Bangalore", "Karnataka", "India", "Plot 18, Electronic City Phase 1, Hosur Road, Bangalore 560100", "Plot 18, Electronic City Phase 1, Hosur Road, Bangalore 560100", 160000000.0, 90, "Arun Kulkarni", "ACTIVE"),
    ("CUST-005", "SAS-SYS-05", "SiliconArc Systems India Pvt Ltd", "Electronics", "Strategic", "Bangalore", "Karnataka", "India", "EPIP Zone, Whitefield, Bangalore 560066", "EPIP Zone, Whitefield, Bangalore 560066", 110000000.0, 60, "Arun Kulkarni", "ACTIVE"),
    ("CUST-006", "NBX-ANA-06", "Nexabyte Analytics India Pvt Ltd", "Software", "Strategic", "Bangalore", "Karnataka", "India", "Manyata Embassy Business Park, Outer Ring Road, Nagavara, Bangalore 560045", "Manyata Embassy Business Park, Outer Ring Road, Nagavara, Bangalore 560045", 130000000.0, 60, "Priya Sundaram", "ACTIVE"),
    ("CUST-007", "CPD-SYS-07", "CedarPeak Digital Systems India", "IT Services", "Strategic", "Bangalore", "Karnataka", "India", "Cessna Business Park, Kadubeesanahalli, Bangalore 560103", "Cessna Business Park, Kadubeesanahalli, Bangalore 560103", 125000000.0, 60, "Rohan Sengupta", "ACTIVE"),
    ("CUST-008", "ZNT-BIO-08", "Zenith Bio-Informatics Labs Pvt Ltd", "Biotechnology", "Strategic", "Bangalore", "Karnataka", "India", "Helix Biotech Park, Electronic City Phase 1, Bangalore 560100", "Helix Biotech Park, Electronic City Phase 1, Bangalore 560100", 95000000.0, 60, "Divya Nambiar", "ACTIVE"),

    # Enterprise Tier (Mid-to-Large Bangalore Technology & Engineering Firms)
    ("CUST-009", "OSS-SFT-09", "OrionStack Software Solutions LLP", "Software", "Enterprise", "Bangalore", "Karnataka", "India", "Embassy GolfLinks Business Park, Domlur, Bangalore 560071", "Embassy GolfLinks Business Park, Domlur, Bangalore 560071", 75000000.0, 45, "Divya Nambiar", "ACTIVE"),
    ("CUST-010", "KRN-LOG-10", "Kavveri Logistics Intelligence Corp", "Logistics technology", "Enterprise", "Bangalore", "Karnataka", "India", "Nelamangala Logistics Hub, NH 48, Bangalore Rural 562123", "Nelamangala Logistics Hub, NH 48, Bangalore Rural 562123", 55000000.0, 45, "Karthik Iyer", "ACTIVE"),
    ("CUST-011", "MYS-MED-11", "Mysore MedTech Systems India", "Healthcare technology", "Enterprise", "Bangalore", "Karnataka", "India", "Kalyani Tech Park, Brookefield, Bangalore 560037", "Kalyani Tech Park, Brookefield, Bangalore 560037", 65000000.0, 45, "Divya Nambiar", "ACTIVE"),
    ("CUST-012", "PLR-ECM-12", "Polaris Omnichannel Retail Tech", "E-commerce", "Enterprise", "Bangalore", "Karnataka", "India", "Salarpuria Sattva Knowledge City, Bellandur, Bangalore 560103", "Salarpuria Sattva Knowledge City, Bellandur, Bangalore 560103", 85000000.0, 45, "Priya Sundaram", "ACTIVE"),
    ("CUST-013", "DGT-BNK-13", "Dravida Global Banking Solutions", "Banking", "Enterprise", "Bangalore", "Karnataka", "India", "RMZ Infinity, Old Madras Road, Bennigana Halli, Bangalore 560016", "RMZ Infinity, Old Madras Road, Bennigana Halli, Bangalore 560016", 90000000.0, 60, "Rohan Sengupta", "ACTIVE"),
    ("CUST-014", "AUR-ROB-14", "AuraRobotics Industrial Systems", "Manufacturing technology", "Enterprise", "Bangalore", "Karnataka", "India", "Peenya Industrial Area Phase 3, Bangalore 560058", "Peenya Industrial Area Phase 3, Bangalore 560058", 48000000.0, 45, "Karthik Iyer", "ACTIVE"),
    ("CUST-015", "APX-CON-15", "Apex Bangalore Consulting Partners", "Consulting", "Enterprise", "Bangalore", "Karnataka", "India", "UB City, Vittal Mallya Road, Bangalore 560001", "UB City, Vittal Mallya Road, Bangalore 560001", 60000000.0, 45, "Rohan Sengupta", "ACTIVE"),
    ("CUST-016", "STR-EDT-16", "StrataLearn EdTech India Pvt Ltd", "Education technology", "Enterprise", "Bangalore", "Karnataka", "India", "HSR Layout Sector 3, 27th Main Road, Bangalore 560102", "HSR Layout Sector 3, 27th Main Road, Bangalore 560102", 50000000.0, 30, "Priya Sundaram", "ACTIVE"),
    ("CUST-017", "NVX-MED-17", "Novax Streaming & Media Technologies", "Media technology", "Enterprise", "Bangalore", "Karnataka", "India", "Indiranagar 100 Feet Road, HAL 2nd Stage, Bangalore 560038", "Indiranagar 100 Feet Road, HAL 2nd Stage, Bangalore 560038", 52000000.0, 45, "Divya Nambiar", "ACTIVE"),
    ("CUST-018", "HEL-BIO-18", "Helios Genomic Therapeutics India", "Biotechnology", "Enterprise", "Bangalore", "Karnataka", "India", "Biocon Park, Bommasandra Industrial Area, Bangalore 560099", "Biocon Park, Bommasandra Industrial Area, Bangalore 560099", 70000000.0, 60, "Divya Nambiar", "ACTIVE"),
    ("CUST-019", "CUB-SFT-19", "Cubix Platform Engineering Labs", "Software", "Enterprise", "Bangalore", "Karnataka", "India", "Global Technology Park, Bellandur, Bangalore 560103", "Global Technology Park, Bellandur, Bangalore 560103", 62000000.0, 45, "Priya Sundaram", "ACTIVE"),
    ("CUST-020", "SYN-SEM-20", "Synapse VLSI Design Services Pvt Ltd", "Semiconductor", "Enterprise", "Bangalore", "Karnataka", "India", "Pritech Park SEZ, Bellandur, Bangalore 560103", "Pritech Park SEZ, Bellandur, Bangalore 560103", 80000000.0, 60, "Arun Kulkarni", "ACTIVE"),
    ("CUST-021", "INT-TEL-21", "Integra Cloud Telecom Solutions", "IT Services", "Enterprise", "Bangalore", "Karnataka", "India", "Brigade Tech Gardens, Brookefield, Bangalore 560037", "Brigade Tech Gardens, Brookefield, Bangalore 560037", 58000000.0, 45, "Rohan Sengupta", "ACTIVE"),
    ("CUST-022", "FLX-PAY-22", "FlexiPay India Digital Payments", "FinTech", "Enterprise", "Bangalore", "Karnataka", "India", "Koramangala 4th Block, 80 Feet Road, Bangalore 560034", "Koramangala 4th Block, 80 Feet Road, Bangalore 560034", 68000000.0, 45, "Rohan Sengupta", "ACTIVE"),
    ("CUST-023", "AER-DEF-23", "AeroDynamics Defence Electronics Ltd", "Electronics", "Enterprise", "Bangalore", "Karnataka", "India", "Aerospace SEZ, Devanahalli, Bangalore Rural 562110", "Aerospace SEZ, Devanahalli, Bangalore Rural 562110", 95000000.0, 60, "Arun Kulkarni", "ACTIVE"),
    ("CUST-024", "OPT-OPT-24", "Optima Supply Chain Automations", "Logistics technology", "Enterprise", "Bangalore", "Karnataka", "India", "Bommasandra Jigani Link Road, Bangalore 560105", "Bommasandra Jigani Link Road, Bangalore 560105", 42000000.0, 30, "Karthik Iyer", "ACTIVE"),
    ("CUST-025", "VRT-HLT-25", "Virtus Health Informatics Pvt Ltd", "Healthcare technology", "Enterprise", "Bangalore", "Karnataka", "India", "Divyasree Technopolis, Yemlur, Bangalore 560037", "Divyasree Technopolis, Yemlur, Bangalore 560037", 54000000.0, 45, "Divya Nambiar", "ACTIVE"),
    ("CUST-026", "CLD-KNT-26", "CloudKinetic Software India", "SaaS", "Enterprise", "Bangalore", "Karnataka", "India", "Koramangala 7th Block, Industrial Layout, Bangalore 560095", "Koramangala 7th Block, Industrial Layout, Bangalore 560095", 46000000.0, 30, "Priya Sundaram", "ACTIVE"),
    ("CUST-027", "AMB-SOL-27", "Amber Electric Vehicle Tech Systems", "Manufacturing technology", "Enterprise", "Bangalore", "Karnataka", "India", "Attibele Industrial Area, Anekal Taluk, Bangalore 562107", "Attibele Industrial Area, Anekal Taluk, Bangalore 562107", 64000000.0, 45, "Karthik Iyer", "ACTIVE"),
    ("CUST-028", "PRG-ADV-28", "Pragmatic Advisory & Tech Partners", "Consulting", "Enterprise", "Bangalore", "Karnataka", "India", "World Trade Center, Malleswaram West, Bangalore 560055", "World Trade Center, Malleswaram West, Bangalore 560055", 52000000.0, 45, "Rohan Sengupta", "ACTIVE"),
    ("CUST-029", "EDG-CMP-29", "EdgePulse Embedded Computing", "Semiconductor", "Enterprise", "Bangalore", "Karnataka", "India", "Salarpuria GR Tech Park, Whitefield, Bangalore 560066", "Salarpuria GR Tech Park, Whitefield, Bangalore 560066", 72000000.0, 60, "Arun Kulkarni", "ACTIVE"),
    ("CUST-030", "ZST-COM-30", "ZestCommerce Logistics Platform", "E-commerce", "Enterprise", "Bangalore", "Karnataka", "India", "Garuda Bhawan, Magrath Road, Bangalore 560025", "Garuda Bhawan, Magrath Road, Bangalore 560025", 48000000.0, 45, "Priya Sundaram", "ACTIVE"),
    ("CUST-031", "BLR-MED-31", "Bangalore Diagnostic AI Networks", "Healthcare technology", "Enterprise", "Bangalore", "Karnataka", "India", "Bannerghatta Main Road, Bilekahalli, Bangalore 560076", "Bannerghatta Main Road, Bilekahalli, Bangalore 560076", 50000000.0, 45, "Divya Nambiar", "ACTIVE"),
    ("CUST-032", "TRN-NET-32", "Tranzact Cloud Banking Infra", "Banking", "Enterprise", "Bangalore", "Karnataka", "India", "Prestige Trade Tower, Palace Road, Bangalore 560001", "Prestige Trade Tower, Palace Road, Bangalore 560001", 78000000.0, 60, "Rohan Sengupta", "ACTIVE"),

    # SMB Tier (Fast-growing Bangalore tech startups & specialized boutiques)
    ("CUST-033", "ALT-SFT-33", "Altair Edge Software Labs", "Software", "SMB", "Bangalore", "Karnataka", "India", "14th Main, HSR Layout Sector 4, Bangalore 560102", "14th Main, HSR Layout Sector 4, Bangalore 560102", 22000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-034", "PXL-CRF-34", "PixelCraft Game Studios Bangalore", "Media technology", "SMB", "Bangalore", "Karnataka", "India", "100 Feet Road, Indiranagar, Bangalore 560038", "100 Feet Road, Indiranagar, Bangalore 560038", 18000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-035", "SPK-IOT-35", "Sparklink IoT Solutions Pvt Ltd", "Electronics", "SMB", "Bangalore", "Karnataka", "India", "Veerasandra Industrial Area, Electronic City, Bangalore 560100", "Veerasandra Industrial Area, Electronic City, Bangalore 560100", 25000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-036", "FIN-BOT-36", "FinBots Robo-Advisory Labs", "FinTech", "SMB", "Bangalore", "Karnataka", "India", "12th Main, Koramangala 5th Block, Bangalore 560095", "12th Main, Koramangala 5th Block, Bangalore 560095", 28000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-037", "LGT-RTE-37", "LogiRoute Route Optimization AI", "Logistics technology", "SMB", "Bangalore", "Karnataka", "India", "Kudlu Gate, Hosur Road, Bangalore 560068", "Kudlu Gate, Hosur Road, Bangalore 560068", 16000000.0, 30, "Karthik Iyer", "ACTIVE"),
    ("CUST-038", "BIO-PRB-38", "BioProbe Diagnostics Bangalore", "Biotechnology", "SMB", "Bangalore", "Karnataka", "India", "Chikka Banavara, Hesaraghatta Main Road, Bangalore 560090", "Chikka Banavara, Hesaraghatta Main Road, Bangalore 560090", 24000000.0, 30, "Divya Nambiar", "ACTIVE"),
    ("CUST-039", "NEX-EDT-39", "NextGen Campus Learning Systems", "Education technology", "SMB", "Bangalore", "Karnataka", "India", "JP Nagar 7th Phase, Puttenahalli, Bangalore 560078", "JP Nagar 7th Phase, Puttenahalli, Bangalore 560078", 19000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-040", "APX-CLN-40", "ApexClean Smart Energy Tech", "Manufacturing technology", "SMB", "Bangalore", "Karnataka", "India", "Doddaballapur Industrial Area, Bangalore Rural 561203", "Doddaballapur Industrial Area, Bangalore Rural 561203", 26000000.0, 30, "Karthik Iyer", "ACTIVE"),
    ("CUST-041", "DAT-WEV-41", "DataWeave Analytics Partners", "Software", "SMB", "Bangalore", "Karnataka", "India", "Sarjapur Road, Kaikondrahalli, Bangalore 560035", "Sarjapur Road, Kaikondrahalli, Bangalore 560035", 20000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-042", "KRN-AUT-42", "Karnataka Automotive Controls LLP", "Manufacturing technology", "SMB", "Bangalore", "Karnataka", "India", "Bommasandra Industrial Area Phase 2, Bangalore 560099", "Bommasandra Industrial Area Phase 2, Bangalore 560099", 23000000.0, 30, "Karthik Iyer", "ACTIVE"),
    ("CUST-043", "BEE-HLT-43", "BeeHive Healthcare Telematics", "Healthcare technology", "SMB", "Bangalore", "Karnataka", "India", "Kasturi Nagar, Banaswadi, Bangalore 560043", "Kasturi Nagar, Banaswadi, Bangalore 560043", 17000000.0, 30, "Divya Nambiar", "ACTIVE"),
    ("CUST-044", "SCL-DEV-44", "ScaleOps Cloud Architecture LLP", "IT Services", "SMB", "Bangalore", "Karnataka", "India", "BTM Layout 2nd Stage, 7th Main, Bangalore 560076", "BTM Layout 2nd Stage, 7th Main, Bangalore 560076", 21000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-045", "PRM-PAY-45", "PrimeLend Micro-Credit Tech", "FinTech", "SMB", "Bangalore", "Karnataka", "India", "6th Block, Rajajinagar, Bangalore 560010", "6th Block, Rajajinagar, Bangalore 560010", 25000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-046", "URB-LOG-46", "UrbanHaul Freight Intelligence", "Logistics technology", "SMB", "Bangalore", "Karnataka", "India", "Yeshwanthpur Industrial Suburb, Bangalore 560022", "Yeshwanthpur Industrial Suburb, Bangalore 560022", 15000000.0, 30, "Karthik Iyer", "ACTIVE"),
    ("CUST-047", "CYB-GRD-47", "CyberGuard Security Consultants", "IT Services", "SMB", "Bangalore", "Karnataka", "India", "New BEL Road, RMV 2nd Stage, Bangalore 560054", "New BEL Road, RMV 2nd Stage, Bangalore 560054", 27000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-048", "GEN-AI-48", "Generative Vision Systems LLP", "Software", "SMB", "Bangalore", "Karnataka", "India", "Lavelle Road, Shanthala Nagar, Bangalore 560001", "Lavelle Road, Shanthala Nagar, Bangalore 560001", 30000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-049", "INS-MED-49", "Insight Diagnostics Labs", "Healthcare technology", "SMB", "Bangalore", "Karnataka", "India", "Sahakara Nagar, Bellary Road, Bangalore 560092", "Sahakara Nagar, Bellary Road, Bangalore 560092", 18000000.0, 30, "Divya Nambiar", "ACTIVE"),
    ("CUST-050", "ZEN-SEM-50", "Zenith Silicon Microchips", "Semiconductor", "SMB", "Bangalore", "Karnataka", "India", "Singasandra, Hosur Road, Bangalore 560068", "Singasandra, Hosur Road, Bangalore 560068", 32000000.0, 30, "Arun Kulkarni", "ACTIVE"),
    ("CUST-051", "AGR-CLD-51", "AgriGrow Data Farm Solutions", "Software", "SMB", "Bangalore", "Karnataka", "India", "Yelahanka New Town, Bangalore 560064", "Yelahanka New Town, Bangalore 560064", 16000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-052", "BLR-EXP-52", "Bangalore Express Delivery Network", "Logistics technology", "SMB", "Bangalore", "Karnataka", "India", "Hoskote Industrial Area, Bangalore Rural 562114", "Hoskote Industrial Area, Bangalore Rural 562114", 22000000.0, 30, "Karthik Iyer", "ACTIVE"),
    ("CUST-053", "STR-ECM-53", "StoreFront Direct D2C Tech", "E-commerce", "SMB", "Bangalore", "Karnataka", "India", "Jayanagar 4th Block, 11th Main, Bangalore 560011", "Jayanagar 4th Block, 11th Main, Bangalore 560011", 17000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-054", "DEV-OPS-54", "DevForge Systems Consultants", "IT Services", "SMB", "Bangalore", "Karnataka", "India", "Marathahalli Main Road, Munnekollal, Bangalore 560037", "Marathahalli Main Road, Munnekollal, Bangalore 560037", 20000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-055", "OPT-NET-55", "OptiMesh Wireless Engineering", "IT Services", "SMB", "Bangalore", "Karnataka", "India", "Kaggadasapura Main Road, CV Raman Nagar, Bangalore 560093", "Kaggadasapura Main Road, CV Raman Nagar, Bangalore 560093", 19000000.0, 30, "Suresh Hegde", "ACTIVE"),
    ("CUST-056", "VIB-MED-56", "Vibrant Sound & Acoustics Tech", "Media technology", "SMB", "Bangalore", "Karnataka", "India", "Koramangala 1st Block, Bangalore 560034", "Koramangala 1st Block, Bangalore 560034", 15000000.0, 30, "Suresh Hegde", "ACTIVE"),

    # Standard Tier (Early-stage startups, educational institutes, local branch offices)
    ("CUST-057", "BLR-UNI-57", "Bangalore Institute of Applied Science", "Education technology", "Standard", "Bangalore", "Karnataka", "India", "Jnana Bharathi Campus, Mysore Road, Bangalore 560056", "Jnana Bharathi Campus, Mysore Road, Bangalore 560056", 12000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-058", "SFT-LNK-58", "SoftLink Web Innovations LLP", "Software", "Standard", "Bangalore", "Karnataka", "India", "Malleshpalya Main Road, Bangalore 560075", "Malleshpalya Main Road, Bangalore 560075", 8000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-059", "KRN-PHR-59", "Karnad Bio Labs LLP", "Biotechnology", "Standard", "Bangalore", "Karnataka", "India", "Attibele-Anekal Road, Bangalore 562107", "Attibele-Anekal Road, Bangalore 562107", 10000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-060", "NXT-DSG-60", "NextLevel Product Designers LLP", "Consulting", "Standard", "Bangalore", "Karnataka", "India", "Cunningham Road, Vasanth Nagar, Bangalore 560052", "Cunningham Road, Vasanth Nagar, Bangalore 560052", 9000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-061", "ECH-PAY-61", "EchoPay Payments Integration", "FinTech", "Standard", "Bangalore", "Karnataka", "India", "HSR Layout Sector 1, 19th Main, Bangalore 560102", "HSR Layout Sector 1, 19th Main, Bangalore 560102", 11000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-062", "PRC-ROB-62", "Precision Motion Dynamics LLP", "Manufacturing technology", "Standard", "Bangalore", "Karnataka", "India", "Rajajinagar Industrial Town, Bangalore 560044", "Rajajinagar Industrial Town, Bangalore 560044", 10500000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-063", "MED-SYS-63", "Medicare Patient Records Solutions", "Healthcare technology", "Standard", "Bangalore", "Karnataka", "India", "Basavanagudi, DVG Road, Bangalore 560004", "Basavanagudi, DVG Road, Bangalore 560004", 8500000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-064", "SMT-LOG-64", "SmartFleet Sensor Telematics", "Logistics technology", "Standard", "Bangalore", "Karnataka", "India", "HBR Layout 2nd Block, Hennur Road, Bangalore 560043", "HBR Layout 2nd Block, Hennur Road, Bangalore 560043", 9500000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-065", "VTR-SFT-65", "VectorByte Systems Bangalore", "Software", "Standard", "Bangalore", "Karnataka", "India", "Banaswadi Main Road, Subbannapalaya, Bangalore 560033", "Banaswadi Main Road, Subbannapalaya, Bangalore 560033", 8000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-066", "RAD-ELC-66", "Radiant Embedded Boards LLP", "Electronics", "Standard", "Bangalore", "Karnataka", "India", "Kammanahalli Main Road, Bangalore 560084", "Kammanahalli Main Road, Bangalore 560084", 9000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-067", "GLO-MED-67", "Global Cast Media Production Hub", "Media technology", "Standard", "Bangalore", "Karnataka", "India", "Kalyan Nagar HRBR Layout, Bangalore 560043", "Kalyan Nagar HRBR Layout, Bangalore 560043", 7500000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-068", "ACD-TEC-68", "Academy of Modern Computing", "Education technology", "Standard", "Bangalore", "Karnataka", "India", "Seshadripuram Main Road, Bangalore 560020", "Seshadripuram Main Road, Bangalore 560020", 11500000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-069", "BLR-FIN-69", "Bengaluru Merchant Advisory LLP", "FinTech", "Standard", "Bangalore", "Karnataka", "India", "Commercial Street, Tasker Town, Bangalore 560001", "Commercial Street, Tasker Town, Bangalore 560001", 8500000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-070", "ZEN-OPS-70", "Zenith IT Infrastructure Care", "IT Services", "Standard", "Bangalore", "Karnataka", "India", "Vidyaranyapura Main Road, Bangalore 560097", "Vidyaranyapura Main Road, Bangalore 560097", 9200000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-071", "BLR-ENV-71", "GreenKarnataka Enviro Analytics", "Software", "Standard", "Bangalore", "Karnataka", "India", "Sanjay Nagar Main Road, Bangalore 560094", "Sanjay Nagar Main Road, Bangalore 560094", 7800000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-072", "AUT-DEV-72", "AutoCode Automation Systems LLP", "Software", "Standard", "Bangalore", "Karnataka", "India", "RT Nagar Main Road, Bangalore 560032", "RT Nagar Main Road, Bangalore 560032", 8200000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-073", "DIG-PRT-73", "DigitalPrint Enterprise Hub", "Media technology", "Standard", "Bangalore", "Karnataka", "India", "Shivajinagar, Broadway Road, Bangalore 560051", "Shivajinagar, Broadway Road, Bangalore 560051", 7000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-074", "SYN-LOG-74", "SyncroLog Warehouse Automation", "Logistics technology", "Standard", "Bangalore", "Karnataka", "India", "Kengeri Satellite Town, Bangalore 560060", "Kengeri Satellite Town, Bangalore 560060", 8800000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-075", "KRN-AGR-75", "Karnataka Precision AgriSystems", "Manufacturing technology", "Standard", "Bangalore", "Karnataka", "India", "Chikkabanavara Post, Bangalore 560090", "Chikkabanavara Post, Bangalore 560090", 9400000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-076", "NUX-SFT-76", "Nuxion Embedded Systems India", "Semiconductor", "Standard", "Bangalore", "Karnataka", "India", "Electronic City Phase 2, Bangalore 560100", "Electronic City Phase 2, Bangalore 560100", 11000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-077", "TRU-MED-77", "TrueScan Diagnostic Tele-Imaging", "Healthcare technology", "Standard", "Bangalore", "Karnataka", "India", "BTM Layout 1st Stage, Bangalore 560068", "BTM Layout 1st Stage, Bangalore 560068", 8500000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-078", "FLT-OPS-78", "FleetEdge Vehicle Sensors LLP", "Logistics technology", "Standard", "Bangalore", "Karnataka", "India", "Hoskote Malur Road, Bangalore Rural 562114", "Hoskote Malur Road, Bangalore Rural 562114", 9000000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-079", "COR-CON-79", "Coromandel Business Analysts Bangalore", "Consulting", "Standard", "Bangalore", "Karnataka", "India", "Richmond Town, Residency Road, Bangalore 560025", "Richmond Town, Residency Road, Bangalore 560025", 8200000.0, 15, "Meera Rao", "ACTIVE"),
    ("CUST-080", "APP-VNT-80", "AppVantage Venture Studio India", "Software", "Standard", "Bangalore", "Karnataka", "India", "Koramangala 3rd Block, Bangalore 560034", "Koramangala 3rd Block, Bangalore 560034", 9800000.0, 15, "Meera Rao", "ACTIVE")
]

print(f"Loaded {len(CUSTOMERS_DATA)} Bangalore enterprise accounts.")
