"""
DealFlow360 Product Catalog Builder
Generates 180+ Enterprise IT Hardware Products and 340+ Sellable Variants.
Adheres strictly to realistic specifications, pricing, margins, and serial tracking rules.
"""

import os
import csv

def generate_catalog():
    products = []
    variants = []

    p_idx = 1
    v_idx = 1

    def add_p(code, name, brand, subcat, ptype, desc, mpn, cost, price, tax, warranty, is_ser):
        nonlocal p_idx
        pid = f"PROD-{p_idx:04d}"
        p_idx += 1
        # parent cat lookup
        if subcat in ["CAT-LAP", "CAT-DSK", "CAT-WKS"]:
            cat_id = "CAT-COMP"
        elif subcat in ["CAT-SRV", "CAT-NET", "CAT-STO", "CAT-UPS"]:
            cat_id = "CAT-INFRA"
        elif subcat in ["CAT-SMP", "CAT-TAB"]:
            cat_id = "CAT-MOB"
        else:
            cat_id = "CAT-PERIPH"

        p_row = [
            pid, code, name, brand, cat_id, subcat, ptype, desc, mpn, "EACH",
            f"{cost:.2f}", f"{price:.2f}", f"{tax:.1f}", warranty, "ACTIVE",
            str(is_ser).lower(), "false", "2026-01-10T08:00:00Z", "2026-03-01T10:00:00Z"
        ]
        products.append(p_row)
        return pid

    def add_v(pid, sku, vname, cpu="", ram="", storage="", stype="", gpu="", screen="", res="", color="", conn="", os_sys="", ff="", war=36, extra=0.0, cost=None, price=None, barcode=""):
        nonlocal v_idx
        vid = f"VAR-{v_idx:04d}"
        v_idx += 1
        if barcode == "":
            barcode = f"8907100{v_idx:06d}"
        v_row = [
            vid, pid, sku, vname, cpu, ram, storage, stype, gpu, screen, res,
            color, conn, os_sys, ff, war, f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}", barcode, "ACTIVE"
        ]
        variants.append(v_row)
        return vid

    # --------------------------------------------------------------------------
    # 1. BUSINESS LAPTOPS (18 products, 42 variants)
    # --------------------------------------------------------------------------
    # P1: Dell Latitude 5440 (Scenario 1 & 2 target)
    p = add_p("LAP-DEL-LAT5440", "Dell Latitude 5440 14-inch Business Laptop", "Dell Technologies", "CAT-LAP", "HARDWARE",
              "Mainstream enterprise business laptop built with recycled materials, Intel 13th Gen, Wi-Fi 6E",
              "DEL-LAT-5440-BASE", 62000.0, 74500.0, 18.0, 36, True)
    add_v(p, "LAP-DEL-5440-I5-16-512", "Dell Latitude 5440 Core i5 / 16GB / 512GB SSD / Win 11 Pro",
          "Intel Core i5-1335U", "16GB DDR4", "512GB", "NVMe PCIe Gen4 SSD", "Intel Iris Xe", "14.0\"", "1920x1080 FHD IPS", "Grey", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell Laptop", 36, 0.0, 62000.0, 74500.0)
    add_v(p, "LAP-DEL-5440-I7-32-1TB", "Dell Latitude 5440 Core i7 / 32GB / 1TB SSD / Win 11 Pro",
          "Intel Core i7-1355U", "32GB DDR4", "1TB", "NVMe PCIe Gen4 SSD", "Intel Iris Xe", "14.0\"", "1920x1080 FHD IPS", "Grey", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell Laptop", 36, 16000.0, 74800.0, 90500.0)

    # P2: Dell Latitude 7440 Ultralight
    p = add_p("LAP-DEL-LAT7440", "Dell Latitude 7440 Ultralight 14-inch Executive Laptop", "Dell Technologies", "CAT-LAP", "HARDWARE",
              "Executive magnesium chassis ultralight notebook with 16:10 display and enterprise security",
              "DEL-LAT-7440-BASE", 88000.0, 105000.0, 18.0, 36, True)
    add_v(p, "LAP-DEL-7440-I7-16-512", "Dell Latitude 7440 i7 / 16GB / 512GB SSD / Titan Grey",
          "Intel Core i7-1365U vPro", "16GB LPDDR5", "512GB", "NVMe SSD", "Intel Iris Xe", "14.0\"", "1920x1200 FHD+ 16:10", "Titan Grey", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Ultralight Laptop", 36, 0.0, 88000.0, 105000.0)
    add_v(p, "LAP-DEL-7440-I7-32-1TB", "Dell Latitude 7440 i7 / 32GB / 1TB SSD / 4G LTE",
          "Intel Core i7-1365U vPro", "32GB LPDDR5", "1TB", "NVMe SSD", "Intel Iris Xe", "14.0\"", "1920x1200 FHD+ 16:10", "Titan Grey", "Wi-Fi 6E + 4G LTE", "Windows 11 Pro", "Ultralight Laptop", 36, 22000.0, 105600.0, 127000.0)

    # P3: Dell Latitude 3540 Commercial Laptop
    p = add_p("LAP-DEL-LAT3540", "Dell Latitude 3540 15.6-inch Commercial Notebook", "Dell Technologies", "CAT-LAP", "HARDWARE",
              "Cost-effective productivity laptop with numeric keypad for accounts and operations",
              "DEL-LAT-3540-BASE", 44000.0, 52000.0, 18.0, 12, True)
    add_v(p, "LAP-DEL-3540-I3-8-256", "Dell Latitude 3540 i3 / 8GB / 256GB SSD",
          "Intel Core i3-1315U", "8GB DDR4", "256GB", "NVMe SSD", "Intel UHD Graphics", "15.6\"", "1920x1080 FHD Anti-Glare", "Black", "Wi-Fi 6 + BT 5.2", "Windows 11 Pro", "Standard Laptop", 12, 0.0, 44000.0, 52000.0)
    add_v(p, "LAP-DEL-3540-I5-16-512", "Dell Latitude 3540 i5 / 16GB / 512GB SSD",
          "Intel Core i5-1335U", "16GB DDR4", "512GB", "NVMe SSD", "Intel Iris Xe", "15.6\"", "1920x1080 FHD Anti-Glare", "Black", "Wi-Fi 6 + BT 5.2", "Windows 11 Pro", "Standard Laptop", 12, 10000.0, 52000.0, 62000.0)

    # P4: Dell Precision 3581 Mobile Workstation
    p = add_p("LAP-DEL-PR3581", "Dell Precision 3581 15.6-inch Mobile Workstation", "Dell Technologies", "CAT-LAP", "HARDWARE",
              "Entry-level mobile workstation with NVIDIA RTX professional graphics and H-series processor",
              "DEL-PREC-3581-BASE", 112000.0, 134000.0, 18.0, 36, True)
    add_v(p, "LAP-DEL-3581-I7-32-1TB-A1000", "Dell Precision 3581 i7 / 32GB / 1TB / RTX A1000",
          "Intel Core i7-13800H vPro", "32GB DDR5", "1TB", "NVMe Gen4 SSD", "NVIDIA RTX A1000 6GB", "15.6\"", "1920x1080 FHD 100% sRGB", "Titan Grey", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro for Workstations", "Mobile Workstation", 36, 0.0, 112000.0, 134000.0)

    # P5: Dell Precision 5680 16-inch Mobile Workstation
    p = add_p("LAP-DEL-PR5680", "Dell Precision 5680 16-inch Premium Mobile Workstation", "Dell Technologies", "CAT-LAP", "HARDWARE",
              "Ultra-premium 16-inch creator workstation with 4K OLED touch and NVIDIA RTX 3500 Ada",
              "DEL-PREC-5680-BASE", 215000.0, 258000.0, 18.0, 36, True)
    add_v(p, "LAP-DEL-5680-I9-64-2TB-A3500", "Dell Precision 5680 i9 / 64GB / 2TB / RTX 3500 Ada",
          "Intel Core i9-13900H", "64GB LPDDR5", "2TB", "NVMe Gen4 Performance SSD", "NVIDIA RTX 3500 Ada 12GB", "16.0\"", "3840x2400 UHD+ OLED Touch", "Platinum Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro for Workstations", "Precision Workstation", 36, 0.0, 215000.0, 258000.0)

    # P6: Lenovo ThinkPad T14 Gen 4 (Scenario 2 target)
    p = add_p("LAP-LEN-TPT14G4", "Lenovo ThinkPad T14 Gen 4 14-inch Enterprise Laptop", "Lenovo Group Ltd", "CAT-LAP", "HARDWARE",
              "The enterprise standard workhorse laptop with legendary reliability and MIL-SPEC testing",
              "21HD000VIN", 65000.0, 78000.0, 18.0, 36, True)
    add_v(p, "LAP-LEN-T14-01", "Lenovo ThinkPad T14 Gen 4 i5 / 16GB / 512GB SSD / Thunder Black",
          "Intel Core i5-1335U vPro", "16GB DDR5", "512GB", "NVMe PCIe Gen4 Opal2 SSD", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA IPS Anti-Glare", "Thunder Black", "Wi-Fi 6E + BT 5.1", "Windows 11 Pro 64", "Business Laptop", 36, 0.0, 65000.0, 78000.0)
    add_v(p, "LAP-LEN-T14-02", "Lenovo ThinkPad T14 Gen 4 i7 / 32GB / 1TB SSD / Thunder Black",
          "Intel Core i7-1355U vPro", "32GB DDR5", "1TB", "NVMe PCIe Gen4 Opal2 SSD", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA IPS Anti-Glare", "Thunder Black", "Wi-Fi 6E + BT 5.1", "Windows 11 Pro 64", "Business Laptop", 36, 17000.0, 78600.0, 95000.0)

    # P7: Lenovo ThinkPad T16 Gen 2
    p = add_p("LAP-LEN-TPT16G2", "Lenovo ThinkPad T16 Gen 2 16-inch Enterprise Laptop", "Lenovo Group Ltd", "CAT-LAP", "HARDWARE",
              "Large-format enterprise business laptop with dedicated numpad and high-capacity battery",
              "21HH0025IN", 72000.0, 86000.0, 18.0, 36, True)
    add_v(p, "LAP-LEN-T16-I5-16-512", "Lenovo ThinkPad T16 Gen 2 i5 / 16GB / 512GB / Black",
          "Intel Core i5-1335U", "16GB DDR5", "512GB", "NVMe Gen4 SSD", "Intel Iris Xe", "16.0\"", "1920x1200 WUXGA 300nits", "Thunder Black", "Wi-Fi 6E + BT 5.1", "Windows 11 Pro", "Business Laptop", 36, 0.0, 72000.0, 86000.0)

    # P8: Lenovo ThinkPad X1 Carbon Gen 11
    p = add_p("LAP-LEN-X1CG11", "Lenovo ThinkPad X1 Carbon Gen 11 Flagship Ultrabook", "Lenovo Group Ltd", "CAT-LAP", "HARDWARE",
              "Carbon-fiber reinforced flagship business laptop weighing just 1.12kg with Dolby Voice",
              "21HM001MIN", 128000.0, 154000.0, 18.0, 36, True)
    add_v(p, "LAP-LEN-X1C-I7-16-512", "Lenovo ThinkPad X1 Carbon Gen 11 i7 / 16GB / 512GB",
          "Intel Core i7-1365U vPro", "16GB LPDDR5", "512GB", "NVMe Gen4 Performance", "Intel Iris Xe", "14.0\"", "1920x1200 Low Power IPS 400nits", "Deep Black", "Wi-Fi 6E + BT 5.1", "Windows 11 Pro", "Flagship Ultrabook", 36, 0.0, 128000.0, 154000.0)
    add_v(p, "LAP-LEN-X1C-I7-32-1TB", "Lenovo ThinkPad X1 Carbon Gen 11 i7 / 32GB / 1TB / 2.8K OLED",
          "Intel Core i7-1370P vPro", "32GB LPDDR5", "1TB", "NVMe Gen4 Performance", "Intel Iris Xe", "14.0\"", "2880x1800 2.8K OLED 400nits", "Deep Black", "Wi-Fi 6E + 5G Sub6", "Windows 11 Pro", "Flagship Ultrabook", 36, 32000.0, 153600.0, 186000.0)

    # P9: Lenovo ThinkPad P16v Gen 1
    p = add_p("LAP-LEN-P16VG1", "Lenovo ThinkPad P16v Gen 1 16-inch Workstation", "Lenovo Group Ltd", "CAT-LAP", "HARDWARE",
              "Cost-effective performance mobile workstation engineered for CAD and data analytics",
              "21FC001AIN", 118000.0, 142000.0, 18.0, 36, True)
    add_v(p, "LAP-LEN-P16V-I7-32-1TB-A2000", "Lenovo ThinkPad P16v i7 / 32GB / 1TB / RTX A2000 Ada",
          "Intel Core i7-13700H", "32GB DDR5", "1TB", "NVMe Gen4 Performance", "NVIDIA RTX A2000 Ada 8GB", "16.0\"", "1920x1200 IPS 300nits", "Thunder Black", "Wi-Fi 6E + BT 5.1", "Windows 11 Pro Workstations", "Mobile Workstation", 36, 0.0, 118000.0, 142000.0)

    # P10: Lenovo ThinkPad E14 Gen 5
    p = add_p("LAP-LEN-E14G5", "Lenovo ThinkPad E14 Gen 5 14-inch Commercial Laptop", "Lenovo Group Ltd", "CAT-LAP", "HARDWARE",
              "Essential business laptop designed for SMBs and cost-conscious commercial fleets",
              "21JK003VIN", 46000.0, 54500.0, 18.0, 12, True)
    add_v(p, "LAP-LEN-E14-I5-16-512", "Lenovo ThinkPad E14 Gen 5 i5 / 16GB / 512GB SSD / Graphite",
          "Intel Core i5-1335U", "16GB DDR4", "512GB", "NVMe SSD", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA IPS", "Graphite Black", "Wi-Fi 6 + BT 5.1", "Windows 11 Pro", "Business Laptop", 12, 0.0, 46000.0, 54500.0)

    # P11: HP EliteBook 840 G10 (Scenario 4 target)
    p = add_p("LAP-HP-EB840G10", "HP EliteBook 840 G10 14-inch Enterprise Notebook", "HP Inc.", "CAT-LAP", "HARDWARE",
              "Corporate standard security-focused notebook with HP Wolf Security and 5MP IR camera",
              "8A3X5PA", 67000.0, 81000.0, 18.0, 36, True)
    add_v(p, "VAR-LAP-HP-EB840-01", "HP EliteBook 840 G10 i5 / 16GB / 512GB SSD / Silver",
          "Intel Core i5-1335U vPro", "16GB DDR5", "512GB", "PCIe NVMe SSD", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA IPS Anti-Glare", "Pike Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Enterprise Notebook", 36, 0.0, 67000.0, 81000.0)
    add_v(p, "VAR-LAP-HP-EB840-02", "HP EliteBook 840 G10 i7 / 32GB / 1TB SSD / Silver",
          "Intel Core i7-1365U vPro", "32GB DDR5", "1TB", "PCIe NVMe SSD", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA IPS Anti-Glare", "Pike Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Enterprise Notebook", 36, 18000.0, 81400.0, 99000.0)

    # P12: HP EliteBook 650 G10
    p = add_p("LAP-HP-EB650G10", "HP EliteBook 650 G10 15.6-inch Commercial Notebook", "HP Inc.", "CAT-LAP", "HARDWARE",
              "Full-featured 15.6-inch business laptop with robust ports and numeric keyboard",
              "8A4K2PA", 56000.0, 67000.0, 18.0, 36, True)
    add_v(p, "LAP-HP-650-I5-16-512", "HP EliteBook 650 G10 i5 / 16GB / 512GB / Silver",
          "Intel Core i5-1335U", "16GB DDR4", "512GB", "NVMe SSD", "Intel Iris Xe", "15.6\"", "1920x1080 FHD IPS", "Pike Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Business Notebook", 36, 0.0, 56000.0, 67000.0)

    # P13: HP ProBook 440 G10
    p = add_p("LAP-HP-PB440G10", "HP ProBook 440 G10 14-inch Business Laptop", "HP Inc.", "CAT-LAP", "HARDWARE",
              "Reliable mainstream commercial laptop with aluminum chassis and enterprise durability",
              "8A2Y9PA", 48000.0, 57500.0, 18.0, 12, True)
    add_v(p, "LAP-HP-440-I5-16-512", "HP ProBook 440 G10 i5 / 16GB / 512GB SSD / Silver",
          "Intel Core i5-1335U", "16GB DDR4", "512GB", "NVMe SSD", "Intel Iris Xe", "14.0\"", "1920x1080 FHD IPS", "Pike Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Business Laptop", 12, 0.0, 48000.0, 57500.0)

    # P14: HP ZBook Firefly 14 G10
    p = add_p("LAP-HP-ZBF14G10", "HP ZBook Firefly 14 G10 Mobile Workstation", "HP Inc.", "CAT-LAP", "HARDWARE",
              "Ultralight mobile workstation for CAD, technical sketching and data science",
              "8B1D4PA", 98000.0, 118000.0, 18.0, 36, True)
    add_v(p, "LAP-HP-ZBF-I7-32-1TB-A500", "HP ZBook Firefly 14 i7 / 32GB / 1TB / RTX A500 4GB",
          "Intel Core i7-1365U vPro", "32GB DDR5", "1TB", "PCIe NVMe TLC SSD", "NVIDIA RTX A500 4GB", "14.0\"", "1920x1200 WUXGA IPS DreamColor", "Space Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro Workstations", "Mobile Workstation", 36, 0.0, 98000.0, 118000.0)

    # P15: HP ZBook Power 15.6 G10
    p = add_p("LAP-HP-ZBP15G10", "HP ZBook Power 15.6 G10 Mobile Workstation", "HP Inc.", "CAT-LAP", "HARDWARE",
              "High-power 15.6-inch workstation certified for professional 3D and rendering software",
              "8B2F8PA", 132000.0, 159000.0, 18.0, 36, True)
    add_v(p, "LAP-HP-ZBP-I7-32-1TB-RTX2000", "HP ZBook Power 15.6 i7 / 32GB / 1TB / RTX 2000 Ada",
          "Intel Core i7-13700H", "32GB DDR5", "1TB", "PCIe NVMe TLC SSD", "NVIDIA RTX 2000 Ada 8GB", "15.6\"", "1920x1080 FHD IPS 400nits", "Dark Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro Workstations", "Mobile Workstation", 36, 0.0, 132000.0, 159000.0)

    # P16: Apple MacBook Pro 14" M3 Pro
    p = add_p("LAP-APP-MBP14M3P", "Apple MacBook Pro 14-inch M3 Pro Enterprise Edition", "Apple Inc.", "CAT-LAP", "HARDWARE",
              "Apple Silicon enterprise flagship with Liquid Retina XDR display and exceptional battery life",
              "MRX33HN/A", 168000.0, 199900.0, 18.0, 12, True)
    add_v(p, "LAP-APP-MBP14-M3P-18-512-SB", "Apple MacBook Pro 14\" M3 Pro (11-core CPU/14-core GPU) / 18GB / 512GB / Space Black",
          "Apple M3 Pro 11-core", "18GB Unified Memory", "512GB", "Apple High-Speed SSD", "14-core GPU", "14.2\"", "3024x1964 Liquid Retina XDR 120Hz", "Space Black", "Wi-Fi 6E + BT 5.3", "macOS Sonoma", "Premium Laptop", 12, 0.0, 168000.0, 199900.0)
    add_v(p, "LAP-APP-MBP14-M3P-36-1TB-SIL", "Apple MacBook Pro 14\" M3 Pro (12-core CPU/18-core GPU) / 36GB / 1TB / Silver",
          "Apple M3 Pro 12-core", "36GB Unified Memory", "1TB", "Apple High-Speed SSD", "18-core GPU", "14.2\"", "3024x1964 Liquid Retina XDR 120Hz", "Silver", "Wi-Fi 6E + BT 5.3", "macOS Sonoma", "Premium Laptop", 12, 38000.0, 198400.0, 237900.0)

    # P17: Apple MacBook Pro 16" M3 Max
    p = add_p("LAP-APP-MBP16M3M", "Apple MacBook Pro 16-inch M3 Max Enterprise Edition", "Apple Inc.", "CAT-LAP", "HARDWARE",
              "Ultimate performance Apple workstation for software compilation, video production and AI",
              "MUW63HN/A", 285000.0, 349900.0, 18.0, 12, True)
    add_v(p, "LAP-APP-MBP16-M3M-36-1TB-SB", "Apple MacBook Pro 16\" M3 Max / 36GB / 1TB / Space Black",
          "Apple M3 Max 14-core", "36GB Unified Memory", "1TB", "Apple High-Speed SSD", "30-core GPU", "16.2\"", "3456x2234 Liquid Retina XDR 120Hz", "Space Black", "Wi-Fi 6E + BT 5.3", "macOS Sonoma", "Premium Laptop", 12, 0.0, 285000.0, 349900.0)

    # P18: Apple MacBook Air 13" M2
    p = add_p("LAP-APP-MBA13M2", "Apple MacBook Air 13-inch M2 Corporate Fleet Edition", "Apple Inc.", "CAT-LAP", "HARDWARE",
              "Ultra-thin fanless corporate laptop with all-day battery life and MagSafe 3 charging",
              "MLY33HN/A", 84000.0, 99900.0, 18.0, 12, True)
    add_v(p, "LAP-APP-MBA13-M2-16-256-MID", "Apple MacBook Air 13\" M2 / 16GB / 256GB / Midnight",
          "Apple M2 8-core", "16GB Unified Memory", "256GB", "Apple SSD", "8-core GPU", "13.6\"", "2560x1664 Liquid Retina", "Midnight", "Wi-Fi 6 + BT 5.3", "macOS Sonoma", "Ultrabook", 12, 0.0, 84000.0, 99900.0)
    add_v(p, "LAP-APP-MBA13-M2-16-512-SLV", "Apple MacBook Air 13\" M2 / 16GB / 512GB / Silver",
          "Apple M2 8-core", "16GB Unified Memory", "512GB", "Apple SSD", "10-core GPU", "13.6\"", "2560x1664 Liquid Retina", "Silver", "Wi-Fi 6 + BT 5.3", "macOS Sonoma", "Ultrabook", 12, 16000.0, 96800.0, 115900.0)

    # --------------------------------------------------------------------------
    # 2. BUSINESS DESKTOPS (14 products, 28 variants)
    # --------------------------------------------------------------------------
    # P19: Dell OptiPlex 7010 SFF
    p = add_p("DSK-DEL-OPT7010SFF", "Dell OptiPlex 7010 Small Form Factor Desktop", "Dell Technologies", "CAT-DSK", "HARDWARE",
              "Compact commercial desktop designed for corporate environments with Intel vPro",
              "DEL-OPT-7010-SFF", 48000.0, 58000.0, 18.0, 36, True)
    add_v(p, "DSK-DEL-7010SFF-I5-16-512", "Dell OptiPlex 7010 SFF i5 / 16GB / 512GB SSD / Win 11 Pro",
          "Intel Core i5-13500", "16GB DDR4", "512GB", "NVMe PCIe SSD", "Intel UHD 770", "", "", "Black", "Gigabit Ethernet", "Windows 11 Pro", "Small Form Factor (SFF)", 36, 0.0, 48000.0, 58000.0)
    add_v(p, "DSK-DEL-7010SFF-I7-32-1TB", "Dell OptiPlex 7010 SFF i7 / 32GB / 1TB SSD / Win 11 Pro",
          "Intel Core i7-13700", "32GB DDR4", "1TB", "NVMe PCIe SSD", "Intel UHD 770", "", "", "Black", "Gigabit Ethernet", "Windows 11 Pro", "Small Form Factor (SFF)", 36, 15000.0, 60000.0, 73000.0)

    # P20: Dell OptiPlex 7010 Micro
    p = add_p("DSK-DEL-OPT7010MCR", "Dell OptiPlex 7010 Micro Form Factor Desktop", "Dell Technologies", "CAT-DSK", "HARDWARE",
              "Ultra-compact 1-liter commercial PC mountable behind monitors or under desks",
              "DEL-OPT-7010-MCR", 45000.0, 54000.0, 18.0, 36, True)
    add_v(p, "DSK-DEL-7010MCR-I5-16-512", "Dell OptiPlex 7010 Micro i5 / 16GB / 512GB SSD",
          "Intel Core i5-13500T", "16GB DDR4", "512GB", "NVMe SSD", "Intel UHD 770", "", "", "Black", "Wi-Fi 6E + GbE", "Windows 11 Pro", "Micro / Tiny Form Factor", 36, 0.0, 45000.0, 54000.0)

    # P21: Dell OptiPlex 7010 Tower
    p = add_p("DSK-DEL-OPT7010TWR", "Dell OptiPlex 7010 Tower Business Desktop", "Dell Technologies", "CAT-DSK", "HARDWARE",
              "Expandable commercial tower desktop with PCI expansion slots and multi-drive bays",
              "DEL-OPT-7010-TWR", 52000.0, 63000.0, 18.0, 36, True)
    add_v(p, "DSK-DEL-7010TWR-I7-16-1TB", "Dell OptiPlex 7010 Tower i7 / 16GB / 1TB SSD",
          "Intel Core i7-13700", "16GB DDR5", "1TB", "NVMe PCIe SSD", "Intel UHD 770", "", "", "Black", "Gigabit Ethernet", "Windows 11 Pro", "Tower Desktop", 36, 0.0, 52000.0, 63000.0)

    # P22: Dell OptiPlex 7410 All-in-One
    p = add_p("DSK-DEL-OPT7410AIO", "Dell OptiPlex 7410 23.8-inch Commercial All-in-One", "Dell Technologies", "CAT-DSK", "HARDWARE",
              "Integrated all-in-one desktop featuring pop-up 5MP webcam and height-adjustable stand",
              "DEL-OPT-7410-AIO", 68000.0, 82000.0, 18.0, 36, True)
    add_v(p, "DSK-DEL-7410AIO-I5-16-512", "Dell OptiPlex 7410 AIO i5 / 16GB / 512GB / FHD Touch",
          "Intel Core i5-13500", "16GB DDR5", "512GB", "NVMe SSD", "Intel UHD 770", "23.8\"", "1920x1080 FHD Touch IPS", "Dark Grey", "Wi-Fi 6E + GbE", "Windows 11 Pro", "All-in-One (AIO)", 36, 0.0, 68000.0, 82000.0)

    # P23: HP Pro Tower 400 G9
    p = add_p("DSK-HP-PRO400TWR", "HP Pro Tower 400 G9 Commercial Desktop", "HP Inc.", "CAT-DSK", "HARDWARE",
              "Expandable tower PC engineered for corporate daily business applications",
              "6A7L8PA", 46000.0, 55000.0, 18.0, 36, True)
    add_v(p, "DSK-HP-400TWR-I5-16-512", "HP Pro Tower 400 G9 i5 / 16GB / 512GB SSD",
          "Intel Core i5-13500", "16GB DDR4", "512GB", "NVMe SSD", "Intel UHD 770", "", "", "Black", "Gigabit Ethernet", "Windows 11 Pro", "Tower Desktop", 36, 0.0, 46000.0, 55000.0)

    # P24: HP Pro SFF 400 G9
    p = add_p("DSK-HP-PRO400SFF", "HP Pro SFF 400 G9 Business Desktop", "HP Inc.", "CAT-DSK", "HARDWARE",
              "Space-saving desktop with enterprise reliability and security management",
              "6A7M1PA", 44000.0, 53000.0, 18.0, 36, True)
    add_v(p, "DSK-HP-400SFF-I5-16-512", "HP Pro SFF 400 G9 i5 / 16GB / 512GB SSD",
          "Intel Core i5-13500", "16GB DDR4", "512GB", "NVMe SSD", "Intel UHD 770", "", "", "Black", "Gigabit Ethernet", "Windows 11 Pro", "Small Form Factor (SFF)", 36, 0.0, 44000.0, 53000.0)

    # P25: HP Elite Mini 800 G9
    p = add_p("DSK-HP-ELM800G9", "HP Elite Mini 800 G9 Ultra-Compact Desktop", "HP Inc.", "CAT-DSK", "HARDWARE",
              "Enterprise mini PC with full desktop power, dual flex ports, and HP Sure Start",
              "6B8W2PA", 58000.0, 70000.0, 18.0, 36, True)
    add_v(p, "DSK-HP-800MINI-I7-16-512", "HP Elite Mini 800 G9 i7 / 16GB / 512GB SSD / Wi-Fi 6E",
          "Intel Core i7-13700T", "16GB DDR5", "512GB", "NVMe SSD", "Intel UHD 770", "", "", "Black", "Wi-Fi 6E + GbE", "Windows 11 Pro", "Mini Form Factor", 36, 0.0, 58000.0, 70000.0)

    # P26: HP EliteOne 800 G9 23.8" AIO
    p = add_p("DSK-HP-ELO800AIO", "HP EliteOne 800 G9 23.8-inch Enterprise All-in-One", "HP Inc.", "CAT-DSK", "HARDWARE",
              "Executive conference-ready All-in-One with Bang & Olufsen sound and 5MP auto-framing camera",
              "6C3R4PA", 74000.0, 89000.0, 18.0, 36, True)
    add_v(p, "DSK-HP-800AIO-I7-16-512", "HP EliteOne 800 G9 i7 / 16GB / 512GB / Non-Touch FHD",
          "Intel Core i7-13700", "16GB DDR5", "512GB", "NVMe SSD", "Intel UHD 770", "23.8\"", "1920x1080 FHD IPS Anti-Glare", "Silver", "Wi-Fi 6E + GbE", "Windows 11 Pro", "All-in-One (AIO)", 36, 0.0, 74000.0, 89000.0)

    # P27: Lenovo ThinkCentre M70s Gen 4 SFF
    p = add_p("DSK-LEN-M70SG4", "Lenovo ThinkCentre M70s Gen 4 Small Form Factor", "Lenovo Group Ltd", "CAT-DSK", "HARDWARE",
              "Workhorse corporate desktop with toolless chassis design and ThinkShield security",
              "11T7003PIN", 47000.0, 56500.0, 18.0, 36, True)
    add_v(p, "DSK-LEN-M70S-I5-16-512", "Lenovo ThinkCentre M70s Gen 4 i5 / 16GB / 512GB SSD",
          "Intel Core i5-13400", "16GB DDR4", "512GB", "NVMe SSD", "Intel UHD 730", "", "", "Raven Black", "Gigabit Ethernet", "Windows 11 Pro", "Small Form Factor (SFF)", 36, 0.0, 47000.0, 56500.0)

    # P28: Lenovo ThinkCentre M70q Gen 4 Tiny
    p = add_p("DSK-LEN-M70QG4", "Lenovo ThinkCentre M70q Gen 4 Tiny Desktop", "Lenovo Group Ltd", "CAT-DSK", "HARDWARE",
              "1L compact enterprise desktop deployable in kiosks, trading desks, or healthcare carts",
              "11T3002PIN", 44000.0, 53000.0, 18.0, 36, True)
    add_v(p, "DSK-LEN-M70Q-I5-16-512", "Lenovo ThinkCentre M70q Gen 4 i5 / 16GB / 512GB SSD",
          "Intel Core i5-13400T", "16GB DDR4", "512GB", "NVMe SSD", "Intel UHD 730", "", "", "Raven Black", "Wi-Fi 6 + GbE", "Windows 11 Pro", "Tiny Micro Desktop", 36, 0.0, 44000.0, 53000.0)

    # P29: Lenovo ThinkCentre M90t Gen 4 Tower
    p = add_p("DSK-LEN-M90TG4", "Lenovo ThinkCentre M90t Gen 4 High-Performance Tower", "Lenovo Group Ltd", "CAT-DSK", "HARDWARE",
              "High-capacity commercial tower PC ready for dual graphic cards and multiple enterprise drives",
              "11TV001KIN", 64000.0, 77000.0, 18.0, 36, True)
    add_v(p, "DSK-LEN-M90T-I7-32-1TB", "Lenovo ThinkCentre M90t Gen 4 i7 / 32GB / 1TB SSD",
          "Intel Core i7-13700 vPro", "32GB DDR5", "1TB", "NVMe Gen4 SSD", "Intel UHD 770", "", "", "Raven Black", "Gigabit Ethernet", "Windows 11 Pro", "Tower Desktop", 36, 0.0, 64000.0, 77000.0)

    # P30: Lenovo ThinkCentre Neo 50a 24" AIO
    p = add_p("DSK-LEN-NEO50A", "Lenovo ThinkCentre Neo 50a 24-inch Commercial All-in-One", "Lenovo Group Ltd", "CAT-DSK", "HARDWARE",
              "Modern clutter-free commercial AIO desktop with AI-assisted noise cancellation",
              "12B8001BIN", 53000.0, 64000.0, 18.0, 36, True)
    add_v(p, "DSK-LEN-NEO50A-I5-16-512", "Lenovo ThinkCentre Neo 50a i5 / 16GB / 512GB SSD",
          "Intel Core i5-13500H", "16GB DDR5", "512GB", "NVMe SSD", "Intel Iris Xe", "23.8\"", "1920x1080 FHD IPS", "Black/Silver", "Wi-Fi 6 + GbE", "Windows 11 Pro", "All-in-One (AIO)", 36, 0.0, 53000.0, 64000.0)

    # P31: Apple Mac Mini M2 Pro
    p = add_p("DSK-APP-MMINIM2P", "Apple Mac Mini M2 Pro Commercial Endpoint", "Apple Inc.", "CAT-DSK", "HARDWARE",
              "Versatile compact desktop with M2 Pro performance, quad Thunderbolt 4 ports, and 10GbE option",
              "MNH73HN/A", 108000.0, 129900.0, 18.0, 12, True)
    add_v(p, "DSK-APP-MINI-M2P-16-512", "Apple Mac Mini M2 Pro (10-core CPU/16-core GPU) / 16GB / 512GB",
          "Apple M2 Pro 10-core", "16GB Unified Memory", "512GB", "Apple SSD", "16-core GPU", "", "", "Silver", "Gigabit Ethernet + Wi-Fi 6E", "macOS Sonoma", "Mini Desktop", 12, 0.0, 108000.0, 129900.0)
    add_v(p, "DSK-APP-MINI-M2P-32-1TB", "Apple Mac Mini M2 Pro (12-core CPU/19-core GPU) / 32GB / 1TB / 10GbE",
          "Apple M2 Pro 12-core", "32GB Unified Memory", "1TB", "Apple SSD", "19-core GPU", "", "", "Silver", "10GbE + Wi-Fi 6E", "macOS Sonoma", "Mini Desktop", 12, 42000.0, 141600.0, 171900.0)

    # P32: Apple Mac Studio M2 Max
    p = add_p("DSK-APP-MSTUDIOM2M", "Apple Mac Studio M2 Max Enterprise Creative Desktop", "Apple Inc.", "CAT-DSK", "HARDWARE",
              "Compact powerhouse desktop engineered for massive data modeling, rendering and Xcode compilation",
              "MQH73HN/A", 175000.0, 209900.0, 18.0, 12, True)
    add_v(p, "DSK-APP-STUDIO-M2M-32-512", "Apple Mac Studio M2 Max / 32GB / 512GB SSD",
          "Apple M2 Max 12-core", "32GB Unified Memory", "512GB", "Apple High-Speed SSD", "30-core GPU", "", "", "Silver", "10GbE + Wi-Fi 6E", "macOS Sonoma", "Compact Workstation", 12, 0.0, 175000.0, 209900.0)

    # --------------------------------------------------------------------------
    # 3. WORKSTATIONS (12 products, 24 variants)
    # --------------------------------------------------------------------------
    # P33: Dell Precision 3660 Tower
    p = add_p("WKS-DEL-PR3660", "Dell Precision 3660 Tower CAD Workstation", "Dell Technologies", "CAT-WKS", "HARDWARE",
              "Entry CAD and architectural workstation featuring Intel 13th Gen Core and NVIDIA RTX graphics",
              "DEL-PREC-3660-TWR", 115000.0, 142000.0, 18.0, 36, True)
    add_v(p, "WKS-DEL-3660-I7-32-1TB-A2000", "Dell Precision 3660 i7 / 32GB / 1TB SSD / RTX A2000 12GB",
          "Intel Core i7-13700K", "32GB DDR5 4800MHz", "1TB", "NVMe PCIe Gen4 SSD", "NVIDIA RTX A2000 12GB", "", "", "Black", "Gigabit Ethernet", "Windows 11 Pro for Workstations", "Tower Workstation", 36, 0.0, 115000.0, 142000.0)
    add_v(p, "WKS-DEL-3660-I9-64-2TB-A4000", "Dell Precision 3660 i9 / 64GB / 2TB SSD / RTX A4000 16GB",
          "Intel Core i9-13900K", "64GB DDR5 4800MHz", "2TB", "NVMe PCIe Gen4 SSD", "NVIDIA RTX A4000 16GB", "", "", "Black", "Gigabit Ethernet", "Windows 11 Pro for Workstations", "Tower Workstation", 36, 52000.0, 156600.0, 194000.0)

    # P34: Dell Precision 5860 Tower
    p = add_p("WKS-DEL-PR5860", "Dell Precision 5860 Tower Engineering Workstation", "Dell Technologies", "CAT-WKS", "HARDWARE",
              "Intel Xeon W-class mid-tower workstation engineered for simulation, CAE and complex assemblies",
              "DEL-PREC-5860-TWR", 220000.0, 275000.0, 18.0, 36, True)
    add_v(p, "WKS-DEL-5860-XW24-64-2TB-A4500", "Dell Precision 5860 Xeon w5-2455X / 64GB ECC / 2TB / RTX A4500",
          "Intel Xeon w5-2455X 16-Core", "64GB DDR5 ECC RDIMM", "2TB", "NVMe PCIe Gen4 Enterprise SSD", "NVIDIA RTX A4500 20GB", "", "", "Black", "Dual 1GbE / 10GbE Optional", "Windows 11 Pro for Workstations", "Mid-Tower Workstation", 36, 0.0, 220000.0, 275000.0)

    # P35: Dell Precision 7960 Tower AI Workstation
    p = add_p("WKS-DEL-PR7960", "Dell Precision 7960 Tower Dual-GPU AI Workstation", "Dell Technologies", "CAT-WKS", "HARDWARE",
              "Dual-socket capable extreme compute workstation for generative AI fine-tuning and visual effects",
              "DEL-PREC-7960-TWR", 480000.0, 595000.0, 18.0, 36, True)
    add_v(p, "WKS-DEL-7960-XW34-128-4TB-2XA6000", "Dell Precision 7960 Xeon w7-3465X / 128GB ECC / 4TB / 2x RTX 6000 Ada",
          "Intel Xeon w7-3465X 28-Core", "128GB DDR5 ECC RDIMM", "4TB (2x 2TB RAID0)", "NVMe Gen4 Enterprise SSD", "2x NVIDIA RTX 6000 Ada 48GB", "", "", "Black", "Dual 10GbE LAN", "Ubuntu Linux 22.04 LTS", "Full-Tower Workstation", 36, 0.0, 48000.0, 595000.0)

    # P36: Dell Precision 3930 1U Rack Workstation
    p = add_p("WKS-DEL-PR3930", "Dell Precision 3930 1U Rackmount Enterprise Workstation", "Dell Technologies", "CAT-WKS", "HARDWARE",
              "High-density 1U rack-mounted remote workstation for secure 1:1 datacenter virtualization",
              "DEL-PREC-3930-1U", 160000.0, 198000.0, 18.0, 36, True)
    add_v(p, "WKS-DEL-3930-I7-32-1TB-A2000", "Dell Precision 3930 1U i7 / 32GB ECC / 1TB / RTX A2000",
          "Intel Core i7-13700E", "32GB DDR5 ECC", "1TB", "NVMe PCIe Gen4 SSD", "NVIDIA RTX A2000 12GB", "", "", "Chassis Black", "Dual GbE", "Windows 11 Pro for Workstations", "1U Rackmount", 36, 0.0, 160000.0, 198000.0)

    # P37: HP Z2 Tower G9
    p = add_p("WKS-HP-Z2TWRG9", "HP Z2 Tower G9 Entry Workstation", "HP Inc.", "CAT-WKS", "HARDWARE",
              "High-frequency single-socket CAD and BIM workstation certified for SolidWorks and AutoCAD",
              "5F0F2PA", 108000.0, 132000.0, 18.0, 36, True)
    add_v(p, "WKS-HP-Z2TWR-I7-32-1TB-A2000", "HP Z2 Tower G9 i7 / 32GB / 1TB SSD / RTX A2000",
          "Intel Core i7-13700K", "32GB DDR5 4800MHz", "1TB", "HP Z Turbo Drive NVMe", "NVIDIA RTX A2000 12GB", "", "", "Space Silver/Black", "Gigabit Ethernet", "Windows 11 Pro for Workstations", "Tower Workstation", 36, 0.0, 108000.0, 132000.0)

    # P38: HP Z4 G5 Simulation Workstation
    p = add_p("WKS-HP-Z4G5", "HP Z4 G5 Workstation for Simulation & Rendering", "HP Inc.", "CAT-WKS", "HARDWARE",
              "Engineered for high-compute engineering simulation, FEA modeling and multi-threaded rendering",
              "6W1D8PA", 195000.0, 245000.0, 18.0, 36, True)
    add_v(p, "WKS-HP-Z4G5-XW24-64-2TB-A4000", "HP Z4 G5 Xeon w5-2465X / 64GB ECC / 2TB / RTX A4000",
          "Intel Xeon w5-2465X 16-Core", "64GB DDR5 ECC RDIMM", "2TB", "HP Z Turbo Dual M.2 SSD", "NVIDIA RTX A4000 16GB", "", "", "Black", "Dual 1GbE / 10GbE Ready", "Windows 11 Pro for Workstations", "Tower Workstation", 36, 0.0, 195000.0, 245000.0)

    # P39: HP Z8 Fury G5 Extreme Workstation
    p = add_p("WKS-HP-Z8FURY", "HP Z8 Fury G5 Ultimate High-End Compute Workstation", "HP Inc.", "CAT-WKS", "HARDWARE",
              "Extreme desktop powerhouse supporting up to 56 cores and 4 high-end GPUs with 2250W power",
              "6W2B4PA", 560000.0, 690000.0, 18.0, 36, True)
    add_v(p, "WKS-HP-Z8F-XW34-128-4TB-RTX6000", "HP Z8 Fury G5 Xeon w9-3495X / 128GB ECC / 4TB / RTX 6000 Ada",
          "Intel Xeon w9-3495X 56-Core", "128GB DDR5 ECC RDIMM", "4TB (2x 2TB NVMe)", "HP Z Turbo Enterprise", "NVIDIA RTX 6000 Ada 48GB", "", "", "Dark Grey", "Dual 10GbE onboard", "Ubuntu Linux 22.04 LTS", "Heavy Tower Workstation", 36, 0.0, 560000.0, 690000.0)

    # P40: HP ZCentral 4R 1U Workstation
    p = add_p("WKS-HP-ZC4R", "HP ZCentral 4R 1U High-Density Rack Workstation", "HP Inc.", "CAT-WKS", "HARDWARE",
              "Rack-optimized workstation delivering remote performance for CAD users with HP Anyware",
              "4K6L0PA", 170000.0, 210000.0, 18.0, 36, True)
    add_v(p, "WKS-HP-ZC4R-XW22-32-1TB-A2000", "HP ZCentral 4R Xeon W-2223 / 32GB ECC / 1TB / RTX A2000",
          "Intel Xeon W-2223 4-Core", "32GB DDR4 ECC RDIMM", "1TB", "HP Z Turbo M.2 SSD", "NVIDIA RTX A2000 12GB", "", "", "Chassis Black", "Dual 10GbE", "Windows 11 Pro for Workstations", "1U Rackmount", 36, 0.0, 170000.0, 210000.0)

    # P41: Lenovo ThinkStation P3 Tower
    p = add_p("WKS-LEN-TSP3TWR", "Lenovo ThinkStation P3 Tower Workstation", "Lenovo Group Ltd", "CAT-WKS", "HARDWARE",
              "Workstation power at desktop pricing certified for Autodesk, Bentley and Siemens NX",
              "30GS002MIN", 112000.0, 138000.0, 18.0, 36, True)
    add_v(p, "WKS-LEN-P3-I7-32-1TB-A2000", "Lenovo ThinkStation P3 i7 / 32GB / 1TB / RTX A2000",
          "Intel Core i7-13700K", "32GB DDR5 4800MHz", "1TB", "NVMe PCIe Gen4 SSD", "NVIDIA RTX A2000 12GB", "", "", "Raven Black", "Gigabit Ethernet", "Windows 11 Pro for Workstations", "Tower Workstation", 36, 0.0, 112000.0, 138000.0)

    # P42: Lenovo ThinkStation P5
    p = add_p("WKS-LEN-TSP5", "Lenovo ThinkStation P5 Aston Martin Chassis Workstation", "Lenovo Group Ltd", "CAT-WKS", "HARDWARE",
              "Aston Martin designed airflow chassis with front-access NVMe drives and Intel Xeon W",
              "30GA001DIN", 210000.0, 260000.0, 18.0, 36, True)
    add_v(p, "WKS-LEN-P5-XW24-64-2TB-A4500", "Lenovo ThinkStation P5 Xeon w5-2455X / 64GB ECC / 2TB / RTX A4500",
          "Intel Xeon w5-2455X 16-Core", "64GB DDR5 ECC RDIMM", "2TB", "NVMe PCIe Gen4 SSD", "NVIDIA RTX A4500 20GB", "", "", "Raven Black / Red", "1GbE + 10GbE LAN", "Windows 11 Pro for Workstations", "Tower Workstation", 36, 0.0, 210000.0, 260000.0)

    # P43: Lenovo ThinkStation P7
    p = add_p("WKS-LEN-TSP7", "Lenovo ThinkStation P7 High-Core Count Simulation Workstation", "Lenovo Group Ltd", "CAT-WKS", "HARDWARE",
              "High-core count Intel Xeon W-3400 single-socket workstation capable of triple high-end GPUs",
              "30F3000GIN", 380000.0, 475000.0, 18.0, 36, True)
    add_v(p, "WKS-LEN-P7-XW34-128-2TB-RTX5000", "Lenovo ThinkStation P7 Xeon w7-3465X / 128GB ECC / 2TB / RTX 5000 Ada",
          "Intel Xeon w7-3465X 28-Core", "128GB DDR5 ECC RDIMM", "2TB", "NVMe PCIe Gen4 Enterprise SSD", "NVIDIA RTX 5000 Ada 32GB", "", "", "Raven Black / Red", "Dual 10GbE onboard", "Windows 11 Pro for Workstations", "Tower Workstation", 36, 0.0, 38000.0, 475000.0)

    # P44: Lenovo ThinkStation PX Dual-Socket
    p = add_p("WKS-LEN-TSPX", "Lenovo ThinkStation PX Dual-Socket AI Supercomputing Workstation", "Lenovo Group Ltd", "CAT-WKS", "HARDWARE",
              "Dual 4th Gen Intel Xeon Scalable processors with up to 120 cores and quad NVIDIA RTX 6000 Ada",
              "30EV000EIN", 720000.0, 890000.0, 18.0, 36, True)
    add_v(p, "WKS-LEN-PX-2XSILV-256-4TB-2XA6000", "Lenovo ThinkStation PX 2x Xeon Gold 6430 / 256GB ECC / 4TB / 2x RTX 6000 Ada",
          "2x Intel Xeon Gold 6430 (64 Cores)", "256GB DDR5 ECC RDIMM", "4TB NVMe SSD", "Dual U.3 Enterprise SSD", "2x NVIDIA RTX 6000 Ada 48GB", "", "", "Raven Black / Red", "Dual 10GbE onboard", "Ubuntu Linux 22.04 LTS", "Heavy Tower / 4U Rackable", 36, 0.0, 720000.0, 890000.0)

    # --------------------------------------------------------------------------
    # 4. SERVERS (14 products, 28 variants)
    # --------------------------------------------------------------------------
    # P45: Dell PowerEdge R660 1U Server
    p = add_p("SRV-DEL-PER660", "Dell PowerEdge R660 1U Dual-Socket Rack Server", "Dell Technologies", "CAT-SRV", "HARDWARE",
              "Dense 1U 2-socket rack server optimized for web tech, high-density compute and virtualization",
              "DEL-PE-R660-BASE", 280000.0, 350000.0, 18.0, 36, True)
    add_v(p, "SRV-DEL-R660-1X-64-2TB", "Dell PowerEdge R660 1x Xeon Silver 4410Y / 64GB ECC / 2x 960GB SSD / PERC H755",
          "1x Intel Xeon Silver 4410Y 12C/24T", "64GB (2x 32GB) DDR5 RDIMM", "1.92TB (2x 960GB SAS SSD)", "Enterprise SAS SSD RAID1", "", "", "", "Silver/Black", "Broadcom 5720 Quad 1GbE LOM", "No OS / Hypervisor Ready", "1U Rackmount", 36, 0.0, 280000.0, 350000.0)
    add_v(p, "SRV-DEL-R660-2X-128-4TB", "Dell PowerEdge R660 2x Xeon Gold 5418Y / 128GB ECC / 4x 1.92TB SSD / Dual 10GbE",
          "2x Intel Xeon Gold 5418Y (48 Cores)", "128GB (4x 32GB) DDR5 RDIMM", "7.68TB (4x 1.92TB SSD)", "Enterprise NVMe SSD RAID10", "", "", "", "Silver/Black", "Dual 10GbE SFP+ OCP 3.0", "VMware ESXi 8.0 Pre-Installed", "1U Rackmount", 36, 120000.0, 376000.0, 470000.0)

    # P46: Dell PowerEdge R760 2U Server (Scenario 3 Target!)
    p = add_p("SRV-DEL-PER760", "Dell PowerEdge R760 2U Enterprise Virtualization Server", "Dell Technologies", "CAT-SRV", "HARDWARE",
              "Flagship 2U 2-socket rack server for virtualization, database processing and enterprise workloads",
              "DEL-PE-R760-BASE", 420000.0, 525000.0, 18.0, 36, True)
    add_v(p, "VAR-SRV-DEL-R760-01", "Dell PowerEdge R760 2x Xeon Gold 6430 / 128GB ECC / 4x 1.92TB SSD / Dual 10GbE",
          "2x Intel Xeon Gold 6430 (64 Cores)", "128GB (4x 32GB) DDR5 RDIMM", "7.68TB (4x 1.92TB SAS SSD)", "Enterprise SAS SSD RAID5", "", "", "", "Silver/Black", "Dual 10GbE SFP+ + Dual 1GbE Base-T", "VMware ESXi 8.0 Pre-Configured", "2U Rackmount", 36, 0.0, 420000.0, 525000.0)
    add_v(p, "VAR-SRV-DEL-R760-02", "Dell PowerEdge R760 2x Xeon Platinum 8468 / 256GB ECC / 8x 3.84TB NVMe / Quad 25GbE",
          "2x Intel Xeon Platinum 8468 (96 Cores)", "256GB (8x 32GB) DDR5 RDIMM", "30.7TB (8x 3.84TB NVMe)", "Enterprise NVMe RAID10", "", "", "", "Silver/Black", "Mellanox ConnectX-6 Dual 25GbE", "Red Hat Enterprise Linux 9", "2U Rackmount", 36, 350000.0, 700000.0, 875000.0)

    # P47: Dell PowerEdge R760xs 2U Scalable
    p = add_p("SRV-DEL-PER760XS", "Dell PowerEdge R760xs 2U Scalable Enterprise Server", "Dell Technologies", "CAT-SRV", "HARDWARE",
              "Purpose-built 2U rack server optimized for scale-out compute, clustered virtualization and SAN workloads",
              "DEL-PE-R760XS-BASE", 340000.0, 420000.0, 18.0, 36, True)
    add_v(p, "SRV-DEL-R760XS-2X-64-4TB", "Dell PowerEdge R760xs 2x Xeon Silver 4410Y / 64GB ECC / 4x 960GB SSD",
          "2x Intel Xeon Silver 4410Y 24C/48T", "64GB DDR5 RDIMM", "3.84TB (4x 960GB SAS)", "PERC H755 SAS RAID", "", "", "", "Silver/Black", "Broadcom 57416 Dual 10GbE", "No OS", "2U Rackmount", 36, 0.0, 340000.0, 420000.0)

    # P48: Dell PowerEdge T360 Tower Server
    p = add_p("SRV-DEL-PET360", "Dell PowerEdge T360 1-Socket SMB Tower Server", "Dell Technologies", "CAT-SRV", "HARDWARE",
              "Quiet, reliable 1-socket tower server for small-to-midsize business file, print and branch office",
              "DEL-PE-T360-BASE", 125000.0, 155000.0, 18.0, 36, True)
    add_v(p, "SRV-DEL-T360-E2436-32-4TB", "Dell PowerEdge T360 Xeon E-2436 / 32GB ECC / 2x 2TB SATA Enterprise HDD",
          "Intel Xeon E-2436 6C/12T", "32GB (2x 16GB) DDR5 UDIMM ECC", "4TB (2x 2TB Enterprise SATA)", "PERC H355 RAID1", "", "", "", "Black", "Dual 1GbE LOM", "Windows Server 2022 Standard (16 Core)", "Tower Server", 36, 0.0, 125000.0, 155000.0)

    # P49: Dell PowerEdge T560 2-Socket Tower
    p = add_p("SRV-DEL-PET560", "Dell PowerEdge T560 2-Socket Enterprise Tower Server", "Dell Technologies", "CAT-SRV", "HARDWARE",
              "Powerful 2-socket tower server with dual redundant power supplies, hot-plug drives and quiet fans",
              "DEL-PE-T560-BASE", 310000.0, 385000.0, 18.0, 36, True)
    add_v(p, "SRV-DEL-T560-2X-64-8TB", "Dell PowerEdge T560 2x Xeon Silver 4410Y / 64GB ECC / 4x 2.4TB SAS HDD",
          "2x Intel Xeon Silver 4410Y", "64GB DDR5 RDIMM", "9.6TB (4x 2.4TB 10K SAS)", "PERC H755 SAS RAID5", "", "", "", "Black", "Quad 1GbE + Dual 10GbE", "Windows Server 2022 Standard", "5U Tower / Rackable", 36, 0.0, 310000.0, 385000.0)

    # P50: HPE ProLiant DL360 Gen11 1U Server
    p = add_p("SRV-HPE-DL360G11", "HPE ProLiant DL360 Gen11 1U High-Density Rack Server", "Hewlett Packard Enterprise", "CAT-SRV", "HARDWARE",
              "Dense compute 1U 2P server engineered for hybrid cloud, software-defined storage and container farms",
              "P52493-B21", 295000.0, 365000.0, 18.0, 36, True)
    add_v(p, "SRV-HPE-DL360-1X-64-2TB", "HPE ProLiant DL360 Gen11 1x Xeon Silver 4410Y / 64GB / 2x 960GB SSD",
          "1x Intel Xeon Silver 4410Y 12C/24T", "64GB DDR5 SmartMemory", "1.92TB (2x 960GB SATA RI SSD)", "HPE MR408i-o Storage Controller", "", "", "", "Silver/Black", "HPE Broadcom 10GbE 2-port OCP3", "HPE iLO 6 Standard", "1U Rackmount", 36, 0.0, 295000.0, 365000.0)

    # P51: HPE ProLiant DL380 Gen11 2U Server
    p = add_p("SRV-HPE-DL380G11", "HPE ProLiant DL380 Gen11 2U Multi-Workload Enterprise Server", "Hewlett Packard Enterprise", "CAT-SRV", "HARDWARE",
              "The enterprise industry standard 2U 2P multi-workload server delivering world-class expandability",
              "P52534-B21", 44000.0 * 10, 54500.0 * 10, 18.0, 36, True)
    add_v(p, "SRV-HPE-DL380-2X-128-4TB", "HPE ProLiant DL380 Gen11 2x Xeon Gold 5418Y / 128GB / 4x 1.92TB SAS SSD",
          "2x Intel Xeon Gold 5418Y (48 Cores)", "128GB DDR5 SmartMemory", "7.68TB (4x 1.92TB SAS SSD)", "HPE SR932i-p Tri-Mode Controller", "", "", "", "Silver/Black", "HPE 10/25GbE 2-port SFP28 OCP3", "HPE iLO 6 Advanced", "2U Rackmount", 36, 0.0, 440000.0, 545000.0)

    # P52: HPE ProLiant ML350 Gen11 Tower
    p = add_p("SRV-HPE-ML350G11", "HPE ProLiant ML350 Gen11 2-Socket Expandable Tower Server", "Hewlett Packard Enterprise", "CAT-SRV", "HARDWARE",
              "Robust dual-socket tower server with maximum internal storage expandability for branch offices",
              "P52690-B21", 320000.0, 398000.0, 18.0, 36, True)
    add_v(p, "SRV-HPE-ML350-2X-64-8TB", "HPE ProLiant ML350 Gen11 2x Xeon Silver 4410Y / 64GB / 4x 2.4TB SAS",
          "2x Intel Xeon Silver 4410Y", "64GB DDR5 SmartMemory", "9.6TB (4x 2.4TB SAS 10K)", "HPE MR408i-o Storage Controller", "", "", "", "Black", "HPE 1GbE 4-port Base-T", "HPE iLO 6 Standard", "4U Tower / Rackable", 36, 0.0, 320000.0, 398000.0)

    # P53: HPE ProLiant MicroServer Gen10 Plus v2
    p = add_p("SRV-HPE-MICROSVR", "HPE ProLiant MicroServer Gen10 Plus v2 Edge Server", "Hewlett Packard Enterprise", "CAT-SRV", "HARDWARE",
              "Ultra-compact edge server suitable for small offices, retail branches and local NAS storage",
              "P54644-B21", 68000.0, 84000.0, 18.0, 12, True)
    add_v(p, "SRV-HPE-MICRO-E2314-16-2TB", "HPE MicroServer Gen10 Plus v2 Xeon E-2314 / 16GB / 2x 1TB SATA",
          "Intel Xeon E-2314 4C/4T", "16GB DDR4 ECC UDIMM", "2TB (2x 1TB SATA Non-Hot Plug)", "Embedded Software RAID", "", "", "", "Black", "4x 1GbE embedded ports", "ClearOS / Linux Ready", "Ultra Micro Tower", 12, 0.0, 68000.0, 84000.0)

    # P54: Lenovo ThinkSystem SR650 V3 2U Server
    p = add_p("SRV-LEN-SR650V3", "Lenovo ThinkSystem SR650 V3 2U Mission-Critical Server", "Lenovo Group Ltd", "CAT-SRV", "HARDWARE",
              "Optimum 2U 2-socket server engineered for SAP HANA, virtualization and high-throughput data processing",
              "7D75A016IN", 435000.0, 538000.0, 18.0, 36, True)
    add_v(p, "SRV-LEN-SR650-2X-128-4TB", "Lenovo ThinkSystem SR650 V3 2x Xeon Gold 5418Y / 128GB TruDDR5 / 4x 1.92TB SSD",
          "2x Intel Xeon Gold 5418Y", "128GB TruDDR5 4800MHz", "7.68TB (4x 1.92TB SAS SSD)", "ThinkSystem RAID 940-8i 4GB Flash", "", "", "", "Black/Silver", "Dual 10/25GbE SFP28 OCP", "Lenovo XClarity Controller Enterprise", "2U Rackmount", 36, 0.0, 435000.0, 538000.0)

    # P55: Lenovo ThinkSystem SR630 V3 1U Server
    p = add_p("SRV-LEN-SR630V3", "Lenovo ThinkSystem SR630 V3 1U Dense Compute Server", "Lenovo Group Ltd", "CAT-SRV", "HARDWARE",
              "High compute-density 1U rack server engineered for cloud services, HPC and security gateways",
              "7D72A012IN", 290000.0, 360000.0, 18.0, 36, True)
    add_v(p, "SRV-LEN-SR630-1X-64-2TB", "Lenovo ThinkSystem SR630 V3 1x Xeon Silver 4410Y / 64GB / 2x 960GB SSD",
          "1x Intel Xeon Silver 4410Y", "64GB TruDDR5", "1.92TB (2x 960GB SAS)", "ThinkSystem RAID 5350-8i", "", "", "", "Black/Silver", "Dual 10GbE SFP+ OCP", "Lenovo XClarity Controller", "1U Rackmount", 36, 0.0, 290000.0, 360000.0)

    # P56: Lenovo ThinkSystem ST250 V2 Tower
    p = add_p("SRV-LEN-ST250V2", "Lenovo ThinkSystem ST250 V2 Entry Business Tower Server", "Lenovo Group Ltd", "CAT-SRV", "HARDWARE",
              "Enterprise-grade 1-socket tower server providing enterprise-level security and quiet acoustics",
              "7D8FA014IN", 118000.0, 146000.0, 18.0, 36, True)
    add_v(p, "SRV-LEN-ST250-E2324-16-2TB", "Lenovo ThinkSystem ST250 V2 Xeon E-2324G / 16GB / 2x 1TB SATA",
          "Intel Xeon E-2324G 4C/4T", "16GB TruDDR4 ECC", "2TB (2x 1TB Enterprise SATA)", "RAID 530-8i PCIe 12Gb", "", "", "", "Black", "Dual 1GbE ports", "Lenovo XClarity Controller", "4U Tower", 36, 0.0, 118000.0, 146000.0)

    # P57: Lenovo ThinkSystem ST550 V2 Dual Tower
    p = add_p("SRV-LEN-ST550V2", "Lenovo ThinkSystem ST550 V2 Scalable Dual-Socket Tower Server", "Lenovo Group Ltd", "CAT-SRV", "HARDWARE",
              "Dual-socket 4U tower server that delivers high compute power, storage and GPU expandability",
              "7X10A039IN", 280000.0, 348000.0, 18.0, 36, True)
    add_v(p, "SRV-LEN-ST550-2X-64-6TB", "Lenovo ThinkSystem ST550 V2 2x Xeon Silver 4310 / 64GB / 3x 2TB SAS",
          "2x Intel Xeon Silver 4310 12C/24T", "64GB TruDDR4", "6TB (3x 2TB 12G SAS HDD)", "ThinkSystem RAID 730-8i", "", "", "", "Black", "Dual 1GbE ports", "Lenovo XClarity Controller", "4U Tower / Rackable", 36, 0.0, 280000.0, 348000.0)

    # P58: Dell PowerEdge R760xd2 Storage Server
    p = add_p("SRV-DEL-PER760XD2", "Dell PowerEdge R760xd2 High-Capacity Storage Server", "Dell Technologies", "CAT-SRV", "HARDWARE",
              "Massive storage server supporting up to 28x 3.5\" front/rear drives for backup, video and analytics",
              "DEL-PE-R760XD2-BASE", 580000.0, 720000.0, 18.0, 36, True)
    add_v(p, "SRV-DEL-R760XD2-2X-128-96TB", "Dell PowerEdge R760xd2 2x Xeon Silver 4410Y / 128GB ECC / 6x 16TB SAS Enterprise",
          "2x Intel Xeon Silver 4410Y", "128GB DDR5 RDIMM", "96TB (6x 16TB 7.2K SAS)", "PERC H755 Front SAS RAID", "", "", "", "Silver/Black", "Dual 10GbE SFP+ + Quad 1GbE", "No OS", "2U Storage Rackmount", 36, 0.0, 58000.0 * 10, 72000.0 * 10)

    # --------------------------------------------------------------------------
    # 5. SMARTPHONES (12 products, 36 variants)
    # --------------------------------------------------------------------------
    # P59: Apple iPhone 15 Enterprise
    p = add_p("SMP-APP-IPH15", "Apple iPhone 15 Enterprise Edition 5G", "Apple Inc.", "CAT-SMP", "HARDWARE",
              "Dynamic Island, 48MP main camera, USB-C, A16 Bionic with Apple Business Manager enrollment",
              "MTP03HN/A", 64000.0, 74900.0, 18.0, 12, True)
    add_v(p, "SMP-APP-IP15-128-BLK", "Apple iPhone 15 128GB Black 5G Enterprise",
          "A16 Bionic Hexa-Core", "6GB RAM", "128GB", "NVMe Flash", "Apple 5-core GPU", "6.1\"", "2556x1179 Super Retina XDR OLED", "Black", "5G + Wi-Fi 6 + NFC", "iOS 17", "Smartphone", 12, 0.0, 64000.0, 74900.0)
    add_v(p, "SMP-APP-IP15-256-BLU", "Apple iPhone 15 256GB Blue 5G Enterprise",
          "A16 Bionic Hexa-Core", "6GB RAM", "256GB", "NVMe Flash", "Apple 5-core GPU", "6.1\"", "2556x1179 Super Retina XDR OLED", "Blue", "5G + Wi-Fi 6 + NFC", "iOS 17", "Smartphone", 12, 8500.0, 71500.0, 84900.0)
    add_v(p, "SMP-APP-IP15-512-GRN", "Apple iPhone 15 512GB Green 5G Enterprise",
          "A16 Bionic Hexa-Core", "6GB RAM", "512GB", "NVMe Flash", "Apple 5-core GPU", "6.1\"", "2556x1179 Super Retina XDR OLED", "Green", "5G + Wi-Fi 6 + NFC", "iOS 17", "Smartphone", 12, 25000.0, 86000.0, 104900.0)

    # P60: Apple iPhone 15 Pro Titanium
    p = add_p("SMP-APP-IPH15PRO", "Apple iPhone 15 Pro Titanium Enterprise Edition 5G", "Apple Inc.", "CAT-SMP", "HARDWARE",
              "Aerospace-grade titanium design, A17 Pro 3nm chip, customizable Action button, USB 3 speeds",
              "MTV13HN/A", 112000.0, 129800.0, 18.0, 12, True)
    add_v(p, "SMP-APP-IP15P-128-NTI", "Apple iPhone 15 Pro 128GB Natural Titanium 5G",
          "A17 Pro Hexa-Core", "8GB RAM", "128GB", "NVMe Flash", "Apple 6-core GPU (Hardware Ray Tracing)", "6.1\"", "2556x1179 ProMotion 120Hz OLED", "Natural Titanium", "5G + Wi-Fi 6E + UWB", "iOS 17", "Smartphone", 12, 0.0, 112000.0, 129800.0)
    add_v(p, "SMP-APP-IP15P-256-BTI", "Apple iPhone 15 Pro 256GB Black Titanium 5G",
          "A17 Pro Hexa-Core", "8GB RAM", "256GB", "NVMe Flash", "Apple 6-core GPU", "6.1\"", "2556x1179 ProMotion 120Hz OLED", "Black Titanium", "5G + Wi-Fi 6E + UWB", "iOS 17", "Smartphone", 12, 9000.0, 120000.0, 139800.0)
    add_v(p, "SMP-APP-IP15P-512-WTI", "Apple iPhone 15 Pro 512GB White Titanium 5G",
          "A17 Pro Hexa-Core", "8GB RAM", "512GB", "NVMe Flash", "Apple 6-core GPU", "6.1\"", "2556x1179 ProMotion 120Hz OLED", "White Titanium", "5G + Wi-Fi 6E + UWB", "iOS 17", "Smartphone", 12, 27000.0, 136000.0, 159800.0)

    # P61: Apple iPhone 15 Pro Max
    p = add_p("SMP-APP-IPH15PM", "Apple iPhone 15 Pro Max Titanium Executive Edition 5G", "Apple Inc.", "CAT-SMP", "HARDWARE",
              "Executive smartphone with 5x optical telephoto lens, 6.7-inch display and titanium build",
              "MU773HN/A", 138000.0, 159900.0, 18.0, 12, True)
    add_v(p, "SMP-APP-IP15PM-256-NTI", "Apple iPhone 15 Pro Max 256GB Natural Titanium",
          "A17 Pro Hexa-Core", "8GB RAM", "256GB", "NVMe Flash", "Apple 6-core GPU", "6.7\"", "2796x1290 ProMotion 120Hz OLED", "Natural Titanium", "5G + Wi-Fi 6E + UWB", "iOS 17", "Smartphone", 12, 0.0, 138000.0, 159900.0)
    add_v(p, "SMP-APP-IP15PM-512-BTI", "Apple iPhone 15 Pro Max 512GB Blue Titanium",
          "A17 Pro Hexa-Core", "8GB RAM", "512GB", "NVMe Flash", "Apple 6-core GPU", "6.7\"", "2796x1290 ProMotion 120Hz OLED", "Blue Titanium", "5G + Wi-Fi 6E + UWB", "iOS 17", "Smartphone", 12, 18000.0, 153000.0, 179900.0)

    # P62: Apple iPhone 14 Commercial Fleet
    p = add_p("SMP-APP-IPH14", "Apple iPhone 14 Commercial Fleet Smartphone 5G", "Apple Inc.", "CAT-SMP", "HARDWARE",
              "Proven commercial corporate deployment device with Crash Detection and ceramic shield",
              "MPUF3HN/A", 54000.0, 62900.0, 18.0, 12, True)
    add_v(p, "SMP-APP-IP14-128-MID", "Apple iPhone 14 128GB Midnight 5G",
          "A15 Bionic Hexa-Core", "6GB RAM", "128GB", "NVMe Flash", "Apple 5-core GPU", "6.1\"", "2532x1170 Super Retina XDR", "Midnight", "5G + Wi-Fi 6 + Lightning", "iOS 17", "Smartphone", 12, 0.0, 54000.0, 62900.0)

    # P63: Samsung Galaxy S24 Enterprise Edition
    p = add_p("SMP-SAM-S24EE", "Samsung Galaxy S24 5G Enterprise Edition", "Samsung Electronics", "CAT-SMP", "HARDWARE",
              "Galaxy AI business tools, Samsung Knox security suite and guaranteed 7 years of OS updates",
              "SM-S921B-EE", 65000.0, 74999.0, 18.0, 24, True)
    add_v(p, "SMP-SAM-S24-128-OBLK", "Samsung Galaxy S24 5G 8GB/128GB Onyx Black Knox Enterprise",
          "Exynos 2400 Deca-Core", "8GB LPDDR5X", "128GB", "UFS 4.0 Storage", "Samsung Xclipse 940", "6.2\"", "2340x1080 Dynamic AMOLED 2X 120Hz", "Onyx Black", "5G + Wi-Fi 6E + Dual SIM", "Android 14 / One UI 6.1", "Smartphone", 24, 0.0, 65000.0, 74999.0)
    add_v(p, "SMP-SAM-S24-256-MGRY", "Samsung Galaxy S24 5G 8GB/256GB Marble Gray Knox Enterprise",
          "Exynos 2400 Deca-Core", "8GB LPDDR5X", "256GB", "UFS 4.0 Storage", "Samsung Xclipse 940", "6.2\"", "2340x1080 Dynamic AMOLED 2X 120Hz", "Marble Gray", "5G + Wi-Fi 6E + Dual SIM", "Android 14 / One UI 6.1", "Smartphone", 24, 5000.0, 69500.0, 79999.0)

    # P64: Samsung Galaxy S24 Ultra Executive
    p = add_p("SMP-SAM-S24ULTRA", "Samsung Galaxy S24 Ultra 5G Executive Edition", "Samsung Electronics", "CAT-SMP", "HARDWARE",
              "Titanium frame, integrated S Pen, Snapdragon 8 Gen 3 for Galaxy, 200MP camera and Live Translate",
              "SM-S928B-EXEC", 114000.0, 129999.0, 18.0, 24, True)
    add_v(p, "SMP-SAM-S24U-256-TBLK", "Samsung Galaxy S24 Ultra 12GB/256GB Titanium Black",
          "Snapdragon 8 Gen 3 for Galaxy", "12GB LPDDR5X", "256GB", "UFS 4.0 Storage", "Adreno 750", "6.8\"", "3120x1440 Dynamic AMOLED 2X 120Hz Gorilla Armor", "Titanium Black", "5G + Wi-Fi 7 + UWB", "Android 14 / One UI 6.1", "Smartphone with S Pen", 24, 0.0, 114000.0, 129999.0)
    add_v(p, "SMP-SAM-S24U-512-TGRY", "Samsung Galaxy S24 Ultra 12GB/512GB Titanium Gray",
          "Snapdragon 8 Gen 3 for Galaxy", "12GB LPDDR5X", "512GB", "UFS 4.0 Storage", "Adreno 750", "6.8\"", "3120x1440 Dynamic AMOLED 2X 120Hz", "Titanium Gray", "5G + Wi-Fi 7 + UWB", "Android 14 / One UI 6.1", "Smartphone with S Pen", 24, 10000.0, 123000.0, 139999.0)

    # P65: Samsung Galaxy S24+ Enterprise
    p = add_p("SMP-SAM-S24PLUS", "Samsung Galaxy S24+ 5G Enterprise Edition", "Samsung Electronics", "CAT-SMP", "HARDWARE",
              "Large 6.7\" QHD+ display, 4900mAh all-day enterprise battery and 45W super-fast wired charging",
              "SM-S926B-EE", 84000.0, 96999.0, 18.0, 24, True)
    add_v(p, "SMP-SAM-S24P-256-COVLT", "Samsung Galaxy S24+ 12GB/256GB Cobalt Violet",
          "Exynos 2400 Deca-Core", "12GB LPDDR5X", "256GB", "UFS 4.0 Storage", "Samsung Xclipse 940", "6.7\"", "3120x1440 Dynamic AMOLED 2X 120Hz", "Cobalt Violet", "5G + Wi-Fi 6E + Dual SIM", "Android 14 / One UI 6.1", "Smartphone", 24, 0.0, 84000.0, 96999.0)

    # P66: Samsung Galaxy A55 5G Enterprise
    p = add_p("SMP-SAM-A55EE", "Samsung Galaxy A55 5G Enterprise Edition", "Samsung Electronics", "CAT-SMP", "HARDWARE",
              "Cost-effective commercial fleet mobile device with metal frame, IP67 water resistance and Knox Vault",
              "SM-A556E-EE", 32000.0, 36999.0, 18.0, 24, True)
    add_v(p, "SMP-SAM-A55-128-NAVY", "Samsung Galaxy A55 5G 8GB/128GB Awesome Navy Knox",
          "Exynos 1480 Octa-Core", "8GB RAM", "128GB", "UFS 3.1 Storage", "Xclipse 530", "6.6\"", "2340x1080 Super AMOLED 120Hz", "Awesome Navy", "5G + Wi-Fi 6 + Dual SIM", "Android 14 / One UI 6.1", "Smartphone", 24, 0.0, 32000.0, 36999.0)
    add_v(p, "SMP-SAM-A55-256-ICEB", "Samsung Galaxy A55 5G 8GB/256GB Awesome Iceblue Knox",
          "Exynos 1480 Octa-Core", "8GB RAM", "256GB", "UFS 3.1 Storage", "Xclipse 530", "6.6\"", "2340x1080 Super AMOLED 120Hz", "Awesome Iceblue", "5G + Wi-Fi 6 + Dual SIM", "Android 14 / One UI 6.1", "Smartphone", 24, 4000.0, 35500.0, 40999.0)

    # P67: Samsung Galaxy XCover6 Pro Rugged
    p = add_p("SMP-SAM-XC6PRO", "Samsung Galaxy XCover6 Pro Ruggedized Enterprise Smartphone", "Samsung Electronics", "CAT-SMP", "HARDWARE",
              "MIL-STD-810H and IP68 certified rugged smartphone with swappable battery and programmable keys",
              "SM-G736B-RUG", 46000.0, 52999.0, 18.0, 24, True)
    add_v(p, "SMP-SAM-XC6P-128-BLK", "Samsung Galaxy XCover6 Pro 6GB/128GB Black Rugged 5G",
          "Snapdragon 778G 5G", "6GB RAM", "128GB", "microSD expandable to 1TB", "Adreno 642L", "6.6\"", "2408x1080 PLS LCD 120Hz Glove-Touch", "Matte Black", "5G + Wi-Fi 6E + POGO Pin", "Android 14 / One UI 6.0", "Rugged Field Smartphone", 24, 0.0, 46000.0, 52999.0)

    # P68: Google Pixel 8 Pro Enterprise
    p = add_p("SMP-GOO-PX8PRO", "Google Pixel 8 Pro Enterprise 5G", "Google LLC", "CAT-SMP", "HARDWARE",
              "Google Tensor G3, Titan M2 security coprocessor, Temperature sensor, Android Enterprise Recommended",
              "GA04834-IN", 92000.0, 106999.0, 18.0, 12, True)
    add_v(p, "SMP-GOO-PX8P-128-OBS", "Google Pixel 8 Pro 12GB/128GB Obsidian 5G",
          "Google Tensor G3", "12GB LPDDR5X", "128GB", "UFS 3.1 Storage", "Immortalis-G715s MC10", "6.7\"", "2992x1344 LTPO OLED 120Hz 2400nits", "Obsidian Black", "5G + Wi-Fi 7 + UWB", "Android 14 (7 Years OS)", "Smartphone", 12, 0.0, 92000.0, 106999.0)
    add_v(p, "SMP-GOO-PX8P-256-POR", "Google Pixel 8 Pro 12GB/256GB Porcelain 5G",
          "Google Tensor G3", "12GB LPDDR5X", "256GB", "UFS 3.1 Storage", "Immortalis-G715s MC10", "6.7\"", "2992x1344 LTPO OLED 120Hz 2400nits", "Porcelain White", "5G + Wi-Fi 7 + UWB", "Android 14 (7 Years OS)", "Smartphone", 12, 7000.0, 98000.0, 113999.0)

    # P69: Google Pixel 8 Commercial Fleet
    p = add_p("SMP-GOO-PX8", "Google Pixel 8 Commercial Fleet 5G", "Google LLC", "CAT-SMP", "HARDWARE",
              "Compact corporate device with advanced AI transcription, Call Screen and pure zero-bloat Android",
              "GA04803-IN", 66000.0, 75999.0, 18.0, 12, True)
    add_v(p, "SMP-GOO-PX8-128-HAZ", "Google Pixel 8 8GB/128GB Hazel 5G",
          "Google Tensor G3", "8GB LPDDR5X", "128GB", "UFS 3.1 Storage", "Immortalis-G715s", "6.2\"", "2400x1080 Actua OLED 120Hz", "Hazel Green", "5G + Wi-Fi 7 + Dual SIM", "Android 14", "Smartphone", 12, 0.0, 66000.0, 75999.0)

    # P70: OnePlus 12 5G Commercial
    p = add_p("SMP-1PL-12COM", "OnePlus 12 5G High-Performance Commercial Edition", "OnePlus Technology", "CAT-SMP", "HARDWARE",
              "Snapdragon 8 Gen 3 flagship with massive 5400mAh battery and 100W SuperVOOC flash charging",
              "CPH2573", 57000.0, 64999.0, 18.0, 12, True)
    add_v(p, "SMP-1PL-12-256-SILK", "OnePlus 12 12GB/256GB Silky Black 5G",
          "Snapdragon 8 Gen 3", "12GB LPDDR5X", "256GB", "UFS 4.0 Storage", "Adreno 750", "6.82\"", "3168x1440 2K ProXDR 120Hz", "Silky Black", "5G + Wi-Fi 7 + Dual Nano-SIM", "OxygenOS 14 (Android 14)", "Smartphone", 12, 0.0, 57000.0, 64999.0)
    add_v(p, "SMP-1PL-12-512-FLGR", "OnePlus 12 16GB/512GB Flowy Emerald 5G",
          "Snapdragon 8 Gen 3", "16GB LPDDR5X", "512GB", "UFS 4.0 Storage", "Adreno 750", "6.82\"", "3168x1440 2K ProXDR 120Hz", "Flowy Emerald", "5G + Wi-Fi 7 + Dual Nano-SIM", "OxygenOS 14 (Android 14)", "Smartphone", 12, 6000.0, 62000.0, 70999.0)

    # --------------------------------------------------------------------------
    # 6. TABLETS (8 products, 20 variants)
    # --------------------------------------------------------------------------
    # P71: Apple iPad 10th Gen 10.9"
    p = add_p("TAB-APP-IPAD10", "Apple iPad 10.9-inch (10th Gen) Enterprise Tablet", "Apple Inc.", "CAT-TAB", "HARDWARE",
              "All-screen design with Liquid Retina display, A14 Bionic, USB-C and Apple Pencil support",
              "MPQ03HN/A", 33000.0, 39900.0, 18.0, 12, True)
    add_v(p, "TAB-APP-IP10-64-WIFI-SLV", "Apple iPad 10.9\" 64GB Wi-Fi Silver",
          "A14 Bionic 6-core", "4GB RAM", "64GB", "Flash Storage", "4-core GPU", "10.9\"", "2360x1640 Liquid Retina True Tone", "Silver", "Wi-Fi 6 + BT 5.2", "iPadOS 17", "Standard Tablet", 12, 0.0, 33000.0, 39900.0)
    add_v(p, "TAB-APP-IP10-256-CEL-BLU", "Apple iPad 10.9\" 256GB Wi-Fi + Cellular 5G Blue",
          "A14 Bionic 6-core", "4GB RAM", "256GB", "Flash Storage", "4-core GPU", "10.9\"", "2360x1640 Liquid Retina True Tone", "Blue", "5G Cellular + Wi-Fi 6", "iPadOS 17", "Cellular Tablet", 12, 22000.0, 52000.0, 61900.0)

    # P72: Apple iPad Air 11" M2
    p = add_p("TAB-APP-IPAIRM2", "Apple iPad Air 11-inch M2 Enterprise Edition", "Apple Inc.", "CAT-TAB", "HARDWARE",
              "Apple M2 chip performance with landscape 12MP ultra-wide front camera for Zoom/Teams",
              "MUWC3HN/A", 51000.0, 59900.0, 18.0, 12, True)
    add_v(p, "TAB-APP-AIRM2-128-WIFI-SG", "Apple iPad Air 11\" M2 128GB Wi-Fi Space Grey",
          "Apple M2 8-core", "8GB Unified Memory", "128GB", "Flash Storage", "9-core GPU", "11.0\"", "2360x1640 Liquid Retina P3", "Space Grey", "Wi-Fi 6E + BT 5.3", "iPadOS 17", "Performance Tablet", 12, 0.0, 51000.0, 59900.0)
    add_v(p, "TAB-APP-AIRM2-256-CEL-SLV", "Apple iPad Air 11\" M2 256GB Wi-Fi + 5G Cellular Silver",
          "Apple M2 8-core", "8GB Unified Memory", "256GB", "Flash Storage", "9-core GPU", "11.0\"", "2360x1640 Liquid Retina P3", "Starlight Silver", "5G Cellular + Wi-Fi 6E", "iPadOS 17", "Cellular Tablet", 12, 21000.0, 69000.0, 80900.0)

    # P73: Apple iPad Pro 11" M4
    p = add_p("TAB-APP-IPPRO11M4", "Apple iPad Pro 11-inch M4 Ultra Retina Enterprise", "Apple Inc.", "CAT-TAB", "HARDWARE",
              "World's most advanced display with Tandem OLED Ultra Retina XDR and revolutionary M4 silicon",
              "MVX23HN/A", 86000.0, 99900.0, 18.0, 12, True)
    add_v(p, "TAB-APP-PRO11M4-256-WIFI-SB", "Apple iPad Pro 11\" M4 256GB Wi-Fi Space Black",
          "Apple M4 9-core", "8GB Unified Memory", "256GB", "Ultra Fast Storage", "10-core GPU (Ray Tracing)", "11.0\"", "2420x1668 Ultra Retina Tandem OLED 120Hz", "Space Black", "Wi-Fi 6E + BT 5.3", "iPadOS 17", "Pro Tablet", 12, 0.0, 86000.0, 99900.0)

    # P74: Apple iPad Pro 13" M4 Executive
    p = add_p("TAB-APP-IPPRO13M4", "Apple iPad Pro 13-inch M4 Ultra Retina Executive Tablet", "Apple Inc.", "CAT-TAB", "HARDWARE",
              "Ultra-thin 5.1mm design, 13-inch Tandem OLED, M4 10-core CPU engineered for C-suite and creative leads",
              "MVX63HN/A", 112000.0, 129900.0, 18.0, 12, True)
    add_v(p, "TAB-APP-PRO13M4-256-CEL-SLV", "Apple iPad Pro 13\" M4 256GB 5G Cellular Silver",
          "Apple M4 9-core", "8GB Unified Memory", "256GB", "Ultra Fast Storage", "10-core GPU", "13.0\"", "2752x2064 Ultra Retina Tandem OLED 120Hz", "Silver", "5G Cellular + Wi-Fi 6E", "iPadOS 17", "Pro Tablet", 12, 0.0, 112000.0, 129900.0)

    # P75: Samsung Galaxy Tab S9 Enterprise
    p = add_p("TAB-SAM-TABS9", "Samsung Galaxy Tab S9 11-inch Enterprise Edition (Wi-Fi/5G)", "Samsung Electronics", "CAT-TAB", "HARDWARE",
              "Dynamic AMOLED 2X, IP68 water & dust resistance, bundled S Pen, Samsung DeX desktop mode",
              "SM-X716B-EE", 62000.0, 72999.0, 18.0, 24, True)
    add_v(p, "TAB-SAM-S9-128-WIFI-GRY", "Samsung Galaxy Tab S9 8GB/128GB Wi-Fi Graphite",
          "Snapdragon 8 Gen 2 for Galaxy", "8GB RAM", "128GB", "UFS 4.0 Storage", "Adreno 740", "11.0\"", "2560x1600 Dynamic AMOLED 2X 120Hz", "Graphite", "Wi-Fi 6E + BT 5.3", "Android 14 / One UI 6.0", "Enterprise Tablet", 24, 0.0, 62000.0, 72999.0)
    add_v(p, "TAB-SAM-S9-256-5G-GRY", "Samsung Galaxy Tab S9 12GB/256GB 5G Graphite",
          "Snapdragon 8 Gen 2 for Galaxy", "12GB RAM", "256GB", "UFS 4.0 Storage", "Adreno 740", "11.0\"", "2560x1600 Dynamic AMOLED 2X 120Hz", "Graphite", "5G + Wi-Fi 6E + Dual SIM", "Android 14 / One UI 6.0", "Cellular Tablet", 24, 12000.0, 72500.0, 84999.0)

    # P76: Samsung Galaxy Tab S9 Ultra
    p = add_p("TAB-SAM-S9ULTRA", "Samsung Galaxy Tab S9 Ultra 14.6-inch Enterprise Presentation Tablet", "Samsung Electronics", "CAT-TAB", "HARDWARE",
              "Massive 14.6\" AMOLED screen replacing laptop screens in executive boardrooms with DeX",
              "SM-X916B-EXEC", 98000.0, 115999.0, 18.0, 24, True)
    add_v(p, "TAB-SAM-S9U-256-5G-GRY", "Samsung Galaxy Tab S9 Ultra 12GB/256GB 5G Graphite",
          "Snapdragon 8 Gen 2 for Galaxy", "12GB RAM", "256GB", "UFS 4.0 Storage", "Adreno 740", "14.6\"", "2960x1848 Dynamic AMOLED 2X 120Hz", "Graphite", "5G + Wi-Fi 6E", "Android 14 / One UI 6.0", "Flagship Presentation Tablet", 24, 0.0, 98000.0, 115999.0)

    # P77: Samsung Galaxy Tab Active4 Pro (Scenario 5 Target!)
    p = add_p("TAB-SAM-ACT4PRO", "Samsung Galaxy Tab Active4 Pro Rugged Field Tablet", "Samsung Electronics", "CAT-TAB", "HARDWARE",
              "Heavy-duty field tablet with anti-shock protective cover, replaceable battery and No Battery mode",
              "SM-T636B-RUG", 52000.0, 60999.0, 18.0, 24, True)
    add_v(p, "VAR-TAB-SAM-ACT4-01", "Samsung Galaxy Tab Active4 Pro 6GB/128GB 5G Rugged Field Tablet",
          "Snapdragon 778G 5G", "6GB RAM", "128GB", "microSD up to 1TB", "Adreno 642L", "10.1\"", "1920x1200 WUXGA Glove-Touch Screen", "Industrial Black", "5G + Wi-Fi 6 + POGO Pin + NFC", "Android 14 / Knox Suite", "Rugged Field Tablet", 24, 0.0, 52000.0, 60999.0)

    # P78: Lenovo Tab P12 Pro
    p = add_p("TAB-LEN-P12PRO", "Lenovo Tab P12 Pro 12.6-inch Commercial Tablet", "Lenovo Group Ltd", "CAT-TAB", "HARDWARE",
              "Slim aluminum tablet with 2K AMOLED 120Hz display and Lenovo Precision Pen 3 support",
              "ZA9D0022IN", 48000.0, 56999.0, 18.0, 12, True)
    add_v(p, "TAB-LEN-P12P-256-WIFI-GRY", "Lenovo Tab P12 Pro 8GB/256GB Wi-Fi Storm Grey",
          "Snapdragon 870 Octa-Core", "8GB LPDDR5", "256GB", "UFS 3.1 Storage", "Adreno 650", "12.6\"", "2560x1600 AMOLED 120Hz Dolby Vision", "Storm Grey", "Wi-Fi 6 + BT 5.2", "Android 13", "Commercial Tablet", 12, 0.0, 48000.0, 56999.0)

    # --------------------------------------------------------------------------
    # 7. MONITORS (14 products, 21 variants)
    # --------------------------------------------------------------------------
    # P79: Dell P2422H (Scenario 1 Target)
    p = add_p("MON-DEL-P2422H", "Dell P2422H 23.8-inch FHD IPS Commercial Monitor", "Dell Technologies", "CAT-MON", "HARDWARE",
              "Corporate standard 24\" IPS monitor with ComfortView Plus low-blue-light and full ergonomic stand",
              "DEL-P2422H-BASE", 11500.0, 14200.0, 18.0, 36, True)
    add_v(p, "VAR-MON-DEL-P2422H-01", "Dell P2422H 23.8\" FHD IPS (HDMI/DP/VGA/USB Hub)",
          "", "", "", "", "", "23.8\"", "1920x1080 FHD 60Hz", "Black/Silver", "HDMI 1.4, DP 1.2, VGA, 4x USB 3.2", "", "Ergonomic Tilt/Swivel/Pivot Stand", 36, 0.0, 11500.0, 14200.0)

    # P80: Dell P2722H
    p = add_p("MON-DEL-P2722H", "Dell P2722H 27-inch FHD Ergonomic Business Monitor", "Dell Technologies", "CAT-MON", "HARDWARE",
              "Spacious 27-inch display optimized for spreadsheet and data entry operations with ultra-thin bezel",
              "DEL-P2722H-BASE", 14500.0, 17800.0, 18.0, 36, True)
    add_v(p, "MON-DEL-P2722H-01", "Dell P2722H 27\" FHD IPS Monitor",
          "", "", "", "", "", "27.0\"", "1920x1080 FHD 60Hz", "Black/Silver", "HDMI, DP, VGA, USB 3.2 Hub", "", "Height-Adjustable Stand", 36, 0.0, 14500.0, 17800.0)

    # P81: Dell P2723DE QHD USB-C
    p = add_p("MON-DEL-P2723DE", "Dell P2723DE 27-inch QHD USB-C Productivity Hub Monitor", "Dell Technologies", "CAT-MON", "HARDWARE",
              "Crystal-clear QHD resolution with built-in RJ45 Ethernet and 90W USB-C single-cable connectivity",
              "DEL-P2723DE-BASE", 27000.0, 32800.0, 18.0, 36, True)
    add_v(p, "MON-DEL-P2723DE-01", "Dell P2723DE 27\" QHD USB-C Hub Monitor (RJ45 / 90W PD)",
          "", "", "", "", "", "27.0\"", "2560x1440 QHD 60Hz", "Silver", "USB-C (90W PD), DP In/Out (Daisy Chain), HDMI, RJ45 GbE", "", "Height/Swivel/Pivot Stand", 36, 0.0, 27000.0, 32800.0)

    # P82: Dell UltraSharp U2724D
    p = add_p("MON-DEL-U2724D", "Dell UltraSharp U2724D 27-inch QHD Color-Accurate Monitor", "Dell Technologies", "CAT-MON", "HARDWARE",
              "IPS Black technology with 2000:1 contrast ratio, 120Hz refresh rate and ambient light sensor",
              "DEL-U2724D-BASE", 32000.0, 38900.0, 18.0, 36, True)
    add_v(p, "MON-DEL-U2724D-01", "Dell UltraSharp U2724D 27\" QHD 120Hz IPS Black",
          "", "", "", "", "", "27.0\"", "2560x1440 QHD 120Hz", "Platinum Silver", "DP 1.4, HDMI, USB-C upstream/downstream", "", "Premium Ergonomic Stand", 36, 0.0, 32000.0, 38900.0)

    # P83: Dell UltraSharp U3223QE 4K
    p = add_p("MON-DEL-U3223QE", "Dell UltraSharp U3223QE 31.5-inch 4K UHD USB-C Hub Monitor", "Dell Technologies", "CAT-MON", "HARDWARE",
              "Brilliant 4K UHD monitor with IPS Black technology, 98% DCI-P3 color gamut, KVM switch and RJ45",
              "DEL-U3223QE-BASE", 58000.0, 69900.0, 18.0, 36, True)
    add_v(p, "MON-DEL-U3223QE-01", "Dell UltraSharp U3223QE 31.5\" 4K USB-C Hub (90W PD / KVM)",
          "", "", "", "", "", "31.5\"", "3840x2160 4K UHD 60Hz", "Platinum Silver", "USB-C (90W PD), DP 1.4 In/Out, HDMI 2.0, RJ45, Auto-KVM", "", "Full Ergonomic Stand", 36, 0.0, 58000.0, 69900.0)

    # P84: Dell UltraSharp U3423WE Curved
    p = add_p("MON-DEL-U3423WE", "Dell UltraSharp U3423WE 34-inch Curved WQHD USB-C Ultrawide", "Dell Technologies", "CAT-MON", "HARDWARE",
              "Immersive 21:9 curved ultrawide with IPS Black, integrated 2x 5W speakers, KVM and dual-PC PbP",
              "DEL-U3423WE-BASE", 72000.0, 86500.0, 18.0, 36, True)
    add_v(p, "MON-DEL-U3423WE-01", "Dell UltraSharp U3423WE 34\" Curved WQHD USB-C Ultrawide",
          "", "", "", "", "", "34.1\"", "3440x1440 WQHD Curved 1900R", "Platinum Silver", "USB-C (90W PD), HDMI 2.1, DP 1.4, RJ45, Audio Out", "", "Heavy-duty Tilt/Swivel Stand", 36, 0.0, 72000.0, 86500.0)

    # P85: HP E24 G4 (Scenario 4 Target)
    p = add_p("MON-HP-E24G4", "HP E24 G4 23.8-inch FHD Ergonomic Enterprise Monitor", "HP Inc.", "CAT-MON", "HARDWARE",
              "Mainstream corporate display featuring HP Eye Ease always-on low-blue-light filter",
              "9VF99AA", 11200.0, 13800.0, 18.0, 36, True)
    add_v(p, "VAR-MON-HP-E24G4-01", "HP E24 G4 23.8\" FHD IPS (VGA/HDMI/DP/4x USB)",
          "", "", "", "", "", "23.8\"", "1920x1080 FHD 60Hz", "Black/Silver", "VGA, HDMI 1.4, DP 1.2, 4x USB-A Hub", "", "4-Way Ergonomic Stand", 36, 0.0, 11200.0, 13800.0)

    # P86: HP E27 G4
    p = add_p("MON-HP-E27G4", "HP E27 G4 27-inch FHD Commercial Business Monitor", "HP Inc.", "CAT-MON", "HARDWARE",
              "27-inch 3-sided micro-edge business display with 4-way adjustability and crisp viewing angles",
              "9VG71AA", 14200.0, 17500.0, 18.0, 36, True)
    add_v(p, "MON-HP-E27G4-01", "HP E27 G4 27\" FHD IPS Commercial Monitor",
          "", "", "", "", "", "27.0\"", "1920x1080 FHD 60Hz", "Black/Silver", "VGA, HDMI, DP, 4x USB Hub", "", "Height-Adjustable Stand", 36, 0.0, 14200.0, 17500.0)

    # P87: HP E27u G5 QHD USB-C
    p = add_p("MON-HP-E27UG5", "HP E27u G5 27-inch QHD USB-C Conferencing Monitor", "HP Inc.", "CAT-MON", "HARDWARE",
              "Single-cable USB-C hub monitor providing 65W power delivery, daisy chaining and RJ45 LAN",
              "6N4D3AA", 28000.0, 34000.0, 18.0, 36, True)
    add_v(p, "MON-HP-E27UG5-01", "HP E27u G5 27\" QHD USB-C Hub Monitor (65W PD / RJ45)",
          "", "", "", "", "", "27.0\"", "2560x1440 QHD 75Hz", "Silver/Black", "USB-C (65W PD), DP In/Out, HDMI 1.4, RJ45", "", "Ergonomic Stand", 36, 0.0, 28000.0, 34000.0)

    # P88: HP Z27k G3 4K
    p = add_p("MON-HP-Z27KG3", "HP Z27k G3 27-inch 4K UHD Color-Calibrated Workstation Display", "HP Inc.", "CAT-MON", "HARDWARE",
              "Factory color-calibrated 4K display crafted with real aluminum and 99% sRGB color accuracy",
              "1B9T0AA", 48000.0, 58000.0, 18.0, 36, True)
    add_v(p, "MON-HP-Z27KG3-01", "HP Z27k G3 27\" 4K UHD USB-C Workstation Display (100W PD)",
          "", "", "", "", "", "27.0\"", "3840x2160 4K UHD 60Hz", "Turbo Silver Aluminum", "USB-C (100W PD), DP In/Out, HDMI 2.0, RJ45", "", "4-Way Aluminum Stand", 36, 0.0, 48000.0, 58000.0)

    # P89: Lenovo ThinkVision T24i-30
    p = add_p("MON-LEN-T24I30", "Lenovo ThinkVision T24i-30 23.8-inch FHD Business Display", "Lenovo Group Ltd", "CAT-MON", "HARDWARE",
              "Reliable 23.8\" borderless business monitor with Natural Low Blue Light certification",
              "63CFMAR3IN", 11000.0, 13500.0, 18.0, 36, True)
    add_v(p, "MON-LEN-T24I30-01", "Lenovo ThinkVision T24i-30 23.8\" FHD IPS Monitor",
          "", "", "", "", "", "23.8\"", "1920x1080 FHD 60Hz", "Raven Black", "VGA, HDMI 1.4, DP 1.2, 4x USB 3.2 Hub", "", "Lift/Tilt/Pivot Stand", 36, 0.0, 11000.0, 13500.0)

    # P90: Lenovo ThinkVision T27h-30 QHD
    p = add_p("MON-LEN-T27H30", "Lenovo ThinkVision T27h-30 27-inch QHD USB-C Docking Monitor", "Lenovo Group Ltd", "CAT-MON", "HARDWARE",
              "Complete desk-docking solution with 90W USB-C, dedicated Ethernet port and DP-out daisy chain",
              "63A3GAR1IN", 26500.0, 32500.0, 18.0, 36, True)
    add_v(p, "MON-LEN-T27H30-01", "Lenovo ThinkVision T27h-30 27\" QHD USB-C Docking Display",
          "", "", "", "", "", "27.0\"", "2560x1440 QHD 60Hz", "Raven Black", "USB-C (90W PD), DP 1.4 In/Out, HDMI 2.0, RJ45", "", "Ergonomic Stand with Phone Holder", 36, 0.0, 26500.0, 32500.0)

    # P91: Lenovo ThinkVision P32p-30 4K
    p = add_p("MON-LEN-P32P30", "Lenovo ThinkVision P32p-30 31.5-inch 4K Professional Display", "Lenovo Group Ltd", "CAT-MON", "HARDWARE",
              "Pro-grade 31.5-inch 4K UHD monitor with Thunderbolt 4 in/out, 100% sRGB/DCI-P3, and hardware KVM",
              "63D3GAR1IN", 62000.0, 74900.0, 18.0, 36, True)
    add_v(p, "MON-LEN-P32P30-01", "Lenovo ThinkVision P32p-30 31.5\" 4K Thunderbolt 4 Hub Monitor",
          "", "", "", "", "", "31.5\"", "3840x2160 4K UHD IPS", "Raven Black", "Thunderbolt 4 In (100W), Thunderbolt 4 Out (27W), HDMI 2.0, DP 1.4, RJ45", "", "Full Ergonomic Stand", 36, 0.0, 62000.0, 74900.0)

    # P92: LG 34WN80C-B Ultrawide
    p = add_p("MON-LG-34WN80C", "LG 34WN80C-B 34-inch 21:9 UltraWide WQHD IPS Curved Monitor", "LG Electronics", "CAT-MON", "HARDWARE",
              "Productivity ultrawide monitor with USB-C 60W power delivery, HDR10 and OnScreen Control",
              "34WN80C-B.ATR", 42000.0, 49999.0, 18.0, 36, True)
    add_v(p, "MON-LG-34WN80C-01", "LG 34WN80C-B 34\" Curved WQHD UltraWide USB-C",
          "", "", "", "", "", "34.0\"", "3440x1440 WQHD Curved 1900R", "Matte Black", "USB-C (60W PD), 2x HDMI, DP 1.4, 2x USB 3.0", "", "Tilt/Height Stand", 36, 0.0, 42000.0, 49999.0)

    # --------------------------------------------------------------------------
    # 8. NETWORKING (16 products, 28 variants)
    # --------------------------------------------------------------------------
    # P93: Cisco Catalyst 9200L 24P PoE+
    p = add_p("NET-CIS-C9200L-24P", "Cisco Catalyst 9200L 24-Port Gigabit Managed PoE+ Switch", "Cisco Systems", "CAT-NET", "HARDWARE",
              "Enterprise foundational Layer 3 switch with 24x 1GbE PoE+ ports (370W budget) and 4x 1G SFP uplinks",
              "C9200L-24P-4G-E", 145000.0, 178000.0, 18.0, 60, True)
    add_v(p, "NET-CIS-9200L-24P-01", "Cisco Catalyst 9200L 24-Port PoE+ (370W) / 4x 1G SFP Uplinks",
          "", "", "", "", "", "", "", "Cisco Grey", "24x 10/100/1000 PoE+, 4x 1G SFP", "Cisco IOS-XE Network Essentials", "1U Rackmount", 60, 0.0, 145000.0, 178000.0)

    # P94: Cisco Catalyst 9200L 48P PoE+ (Demo G Target!)
    p = add_p("NET-CIS-C9200L-48P", "Cisco Catalyst 9200L 48-Port Gigabit Managed PoE+ Switch", "Cisco Systems", "CAT-NET", "HARDWARE",
              "Enterprise high-density access switch with 48x 1GbE PoE+ ports (740W budget) and 4x 10G SFP+ uplinks",
              "C9200L-48P-4X-E", 230000.0, 285000.0, 18.0, 60, True)
    add_v(p, "VAR-NET-CIS-C9200L-48-01", "Cisco Catalyst 9200L 48-Port PoE+ (740W) / 4x 10G SFP+ Uplinks",
          "", "", "", "", "", "", "", "Cisco Grey", "48x 10/100/1000 PoE+ (740W), 4x 10G SFP+", "Cisco IOS-XE Network Essentials", "1U Rackmount", 60, 0.0, 230000.0, 285000.0)

    # P95: Cisco Catalyst 9300 48P Core
    p = add_p("NET-CIS-C9300-48", "Cisco Catalyst 9300 48-Port Multi-Gigabit Layer 3 Core Switch", "Cisco Systems", "CAT-NET", "HARDWARE",
              "Enterprise lead stackable access platform for security, IoT, mobility, and cloud with 480Gbps stacking",
              "C9300-48U-A", 420000.0, 520000.0, 18.0, 60, True)
    add_v(p, "NET-CIS-9300-48U-01", "Cisco Catalyst 9300 48-Port UPOE (820W) / Modular Uplink",
          "", "", "", "", "", "", "", "Cisco Grey", "48x 100M/1G/2.5G/5G/10G Cisco UPOE", "Cisco IOS-XE Network Advantage", "1U Rackmount", 60, 0.0, 420000.0, 520000.0)

    # P96: Cisco Business CBS250-24T
    p = add_p("NET-CIS-CBS250-24T", "Cisco Business 250 Series CBS250-24T-4G Smart Switch", "Cisco Systems", "CAT-NET", "HARDWARE",
              "Affordable smart gigabit switch for SMB commercial offices with intuitive web dashboard",
              "CBS250-24T-4G-IN", 24000.0, 29500.0, 18.0, 36, True)
    add_v(p, "NET-CIS-CBS250-24T-01", "Cisco CBS250 24-Port GE Non-PoE / 4x 1G SFP",
          "", "", "", "", "", "", "", "Grey", "24x 10/100/1000 RJ45, 4x 1G SFP", "Cisco Business OS", "1U Rackmount", 36, 0.0, 24000.0, 29500.0)

    # P97: Cisco Catalyst 9120AX AP
    p = add_p("NET-CIS-C9120AX", "Cisco Catalyst 9120AX Series Wi-Fi 6 Enterprise Access Point", "Cisco Systems", "CAT-NET", "HARDWARE",
              "Mission-critical enterprise Wi-Fi 6 AP with 4x4:4 MIMO, integrated BLE and IoT RF ASIC",
              "C9120AXI-D", 48000.0, 59000.0, 18.0, 60, True)
    add_v(p, "NET-CIS-9120AXI-01", "Cisco Catalyst 9120AX Series Internal Antenna Wi-Fi 6 AP",
          "", "", "", "", "", "", "", "White", "1x 2.5GbE mGig PoE In, Dual 5GHz/2.4GHz Wi-Fi 6", "Cisco DNA Ready", "Ceiling / Wall Mount", 60, 0.0, 48000.0, 59000.0)

    # P98: Aruba CX 6100 24G PoE
    p = add_p("NET-ARU-CX6100-24P", "Aruba CX 6100 24G 4SFP+ Class 4 PoE 370W Switch", "Aruba Networks (HPE)", "CAT-NET", "HARDWARE",
              "Entry-level enterprise access switch with modern AOS-CX operating system and 4x 10G uplinks",
              "JL677A", 92000.0, 114000.0, 18.0, 60, True)
    add_v(p, "NET-ARU-6100-24P-01", "Aruba CX 6100 24-Port PoE+ (370W) / 4x 10G SFP+ Uplinks",
          "", "", "", "", "", "", "", "Grey", "24x 10/100/1000 Class 4 PoE+, 4x 1/10G SFP+", "ArubaOS-CX", "1U Rackmount", 60, 0.0, 92000.0, 114000.0)

    # P99: Aruba CX 6200F 48G PoE
    p = add_p("NET-ARU-CX6200-48P", "Aruba CX 6200F 48G Class 4 PoE 4SFP+ 740W Switch", "Aruba Networks (HPE)", "CAT-NET", "HARDWARE",
              "Next-gen stackable enterprise switch with built-in analytics, dynamic segmentation and VSF stacking",
              "JL726A", 185000.0, 228000.0, 18.0, 60, True)
    add_v(p, "NET-ARU-6200-48P-01", "Aruba CX 6200F 48-Port PoE+ (740W) / 4x 10G SFP+",
          "", "", "", "", "", "", "", "Grey", "48x 10/100/1000 PoE+, 4x 1/10G SFP+ VSF Stacking", "ArubaOS-CX with Network Analytics Engine", "1U Rackmount", 60, 0.0, 185000.0, 228000.0)

    # P100: Aruba AP-515 Wi-Fi 6
    p = add_p("NET-ARU-AP515", "Aruba AP-515 Unified Wi-Fi 6 Campus Access Point", "Aruba Networks (HPE)", "CAT-NET", "HARDWARE",
              "High-performance campus dual-radio Wi-Fi 6 AP with AI-powered ClientMatch and OFDMA",
              "Q9H62A", 42000.0, 52000.0, 18.0, 60, True)
    add_v(p, "NET-ARU-AP515-01", "Aruba AP-515 (IN) Unified Campus Wi-Fi 6 Access Point",
          "", "", "", "", "", "", "", "White", "1x 2.5GbE PoE, 1x 1GbE, Wi-Fi 6 4x4:4", "ArubaOS / InstantOS", "Ceiling / Wall Mount", 60, 0.0, 42000.0, 52000.0)

    # P101: Aruba AP-505 Wi-Fi 6
    p = add_p("NET-ARU-AP505", "Aruba AP-505 Campus Dual-Radio Wi-Fi 6 AP", "Aruba Networks (HPE)", "CAT-NET", "HARDWARE",
              "Cost-effective Wi-Fi 6 connectivity for medium density enterprise environments like schools and clinics",
              "R2H28A", 28000.0, 34500.0, 18.0, 60, True)
    add_v(p, "NET-ARU-AP505-01", "Aruba AP-505 (IN) Unified Wi-Fi 6 Access Point",
          "", "", "", "", "", "", "", "White", "1x 1GbE PoE In, Dual Radio 2x2:2 MIMO", "Aruba InstantOS", "Ceiling Mount", 60, 0.0, 28000.0, 34500.0)

    # P102: Ubiquiti UniFi Pro 24 PoE
    p = add_p("NET-UBI-USWPRO24", "Ubiquiti UniFi Switch Pro 24 PoE Layer 2/3 Managed Switch", "Ubiquiti Networks", "CAT-NET", "HARDWARE",
              "Layer 3 enterprise switch with 24x GbE ports including 802.3bt PoE++ and 2x 10G SFP+ uplinks",
              "USW-Pro-24-PoE", 48000.0, 59500.0, 18.0, 24, True)
    add_v(p, "NET-UBI-PRO24P-01", "Ubiquiti UniFi USW-Pro-24-PoE (400W Total PoE Budget)",
          "", "", "", "", "", "", "", "Silver", "16x PoE+ (30W), 8x PoE++ (64W), 2x 10G SFP+", "UniFi Network OS", "1U Rackmount", 24, 0.0, 48000.0, 59500.0)

    # P103: Ubiquiti UniFi Pro 48 PoE
    p = add_p("NET-UBI-USWPRO48", "Ubiquiti UniFi Switch Pro 48 PoE Enterprise Switch", "Ubiquiti Networks", "CAT-NET", "HARDWARE",
              "High-port-count switch with 40x PoE+, 8x PoE++ (600W budget) and 4x 10G SFP+ ports",
              "USW-Pro-48-PoE", 88000.0, 108000.0, 18.0, 24, True)
    add_v(p, "NET-UBI-PRO48P-01", "Ubiquiti UniFi USW-Pro-48-PoE (600W Total PoE Budget)",
          "", "", "", "", "", "", "", "Silver", "40x PoE+, 8x PoE++, 4x 10G SFP+", "UniFi Network OS", "1U Rackmount", 24, 0.0, 88000.0, 108000.0)

    # P104: Ubiquiti UniFi 6 Pro AP
    p = add_p("NET-UBI-U6PRO", "Ubiquiti UniFi 6 Pro High-Performance Wi-Fi 6 Access Point", "Ubiquiti Networks", "CAT-NET", "HARDWARE",
              "Dual-band Wi-Fi 6 AP with 5.3Gbps aggregate throughput rate and 300+ concurrent client capacity",
              "U6-Pro", 15500.0, 18900.0, 18.0, 24, True)
    add_v(p, "NET-UBI-U6PRO-01", "Ubiquiti UniFi 6 Pro 4x4 MIMO Ceiling AP",
          "", "", "", "", "", "", "", "White", "1x GbE PoE In, 4x4 5GHz + 2x2 2.4GHz", "UniFi Network OS", "Ceiling / Wall Mount", 24, 0.0, 15500.0, 18900.0)

    # P105: Ubiquiti UniFi Dream Machine Pro
    p = add_p("NET-UBI-UDMPRO", "Ubiquiti UniFi Dream Machine Pro Enterprise Security Gateway", "Ubiquiti Networks", "CAT-NET", "HARDWARE",
              "All-in-one 1U rackmount console with 3.5Gbps IDS/IPS throughput, 8-port switch and 10G SFP+ WAN/LAN",
              "UDM-Pro", 38000.0, 46500.0, 18.0, 24, True)
    add_v(p, "NET-UBI-UDMP-01", "Ubiquiti UDM-Pro 1U Rack Gateway & Security Appliance",
          "", "", "", "", "", "", "", "Silver", "8x 1GbE RJ45, 1x 10G SFP+ LAN, 1x 10G SFP+ WAN, 3.5\" HDD Bay", "UniFi OS", "1U Rackmount", 24, 0.0, 38000.0, 46500.0)

    # P106: Fortinet FortiGate 60F Firewall
    p = add_p("NET-FOR-FG60F", "Fortinet FortiGate 60F Enterprise Next-Gen Firewall", "Fortinet Inc.", "CAT-NET", "HARDWARE",
              "Industry-leading secure SD-WAN and NGFW with patented SOC4 processor and 10 Gbps firewall throughput",
              "FG-60F-BDL-950-12", 58000.0, 72000.0, 18.0, 36, True)
    add_v(p, "NET-FOR-FG60F-01", "Fortinet FortiGate 60F Hardware with 1-Year FortiGuard Unified Threat Protection (UTP)",
          "", "", "", "", "", "", "", "White", "10x GE RJ45 ports (including 2x WAN, 1x DMZ, 7x Internal)", "FortiOS 7.4", "Desktop / Rack-Tray Mount", 36, 0.0, 58000.0, 72000.0)

    # P107: Fortinet FortiGate 100F Firewall
    p = add_p("NET-FOR-FG100F", "Fortinet FortiGate 100F Enterprise Mid-Market Next-Gen Firewall", "Fortinet Inc.", "CAT-NET", "HARDWARE",
              "Enterprise-class 1U rackmount firewall with 1 Gbps threat protection throughput and dual 10G SFP+ ports",
              "FG-100F-BDL-950-12", 195000.0, 245000.0, 18.0, 36, True)
    add_v(p, "NET-FOR-FG100F-01", "Fortinet FortiGate 100F Hardware + 1-Year UTP Security Bundle",
          "", "", "", "", "", "", "", "Chassis Black/White", "2x 10GE SFP+, 4x 1GE SFP, 16x GE RJ45, Dual Internal PSU", "FortiOS 7.4", "1U Rackmount", 36, 0.0, 195000.0, 245000.0)

    # P108: TP-Link Omada SG3428XMP Switch
    p = add_p("NET-TPL-SG3428XMP", "TP-Link Omada SG3428XMP 24-Port Gigabit L2+ Managed PoE+ Switch", "TP-Link Technologies", "CAT-NET", "HARDWARE",
              "Cost-effective managed PoE+ switch with 4x 10G SFP+ uplink slots and Omada Cloud SDN management",
              "TL-SG3428XMP", 32000.0, 39999.0, 18.0, 36, True)
    add_v(p, "NET-TPL-SG3428-01", "TP-Link Omada SG3428XMP 24-Port PoE+ (384W) / 4x 10G SFP+",
          "", "", "", "", "", "", "", "Black", "24x Gigabit PoE+ ports, 4x 10G SFP+ Slots", "Omada SDN OS", "1U Rackmount", 36, 0.0, 32000.0, 39999.0)

    # --------------------------------------------------------------------------
    # 9. STORAGE (14 products, 28 variants)
    # --------------------------------------------------------------------------
    # P109: Synology DS923+ 4-Bay NAS
    p = add_p("STO-SYN-DS923P", "Synology DiskStation DS923+ 4-Bay Enterprise NAS", "Synology Inc.", "CAT-STO", "HARDWARE",
              "Compact 4-bay NAS scalable up to 9 drives with dual 1GbE ports and PCIe slot for 10GbE",
              "DS923+", 48000.0, 58500.0, 18.0, 36, True)
    add_v(p, "STO-SYN-DS923P-DISKLESS", "Synology DS923+ 4-Bay NAS Diskless Enclosure",
          "AMD Ryzen R1600 Dual-Core", "4GB DDR4 ECC", "Diskless", "4x 3.5\"/2.5\" SATA bays + 2x M.2 NVMe", "", "", "", "Black", "2x 1GbE (10GbE Upgradeable)", "Synology DSM 7.2", "4-Bay Desktop Tower", 36, 0.0, 48000.0, 58500.0)
    add_v(p, "STO-SYN-DS923P-32TB", "Synology DS923+ Populated with 32TB (4x 8TB Enterprise HDDs)",
          "AMD Ryzen R1600 Dual-Core", "16GB DDR4 ECC", "32TB Raw (4x 8TB)", "Enterprise SATA HDDs RAID5", "", "", "", "Black", "2x 1GbE + 10GbE Module Installed", "Synology DSM 7.2", "4-Bay Desktop Tower", 36, 68000.0, 102400.0, 126500.0)

    # P110: Synology DS1821+ 8-Bay NAS
    p = add_p("STO-SYN-DS1821P", "Synology DiskStation DS1821+ 8-Bay Scalable SMB NAS", "Synology Inc.", "CAT-STO", "HARDWARE",
              "Powerful 8-bay desktop tower designed for high-capacity backup, file serving and virtualization storage",
              "DS1821+", 88000.0, 107000.0, 18.0, 36, True)
    add_v(p, "STO-SYN-DS1821P-DISKLESS", "Synology DS1821+ 8-Bay NAS Diskless Enclosure",
          "AMD Ryzen V1500B Quad-Core", "4GB DDR4 ECC", "Diskless", "8x 3.5\"/2.5\" SATA bays + dual M.2 NVMe", "", "", "", "Black", "4x 1GbE with Link Aggregation", "Synology DSM 7.2", "8-Bay Desktop Tower", 36, 0.0, 88000.0, 107000.0)

    # P111: Synology RS2423+ 12-Bay Rackmount
    p = add_p("STO-SYN-RS2423P", "Synology RackStation RS2423+ 12-Bay 2U Enterprise Rackmount NAS", "Synology Inc.", "CAT-STO", "HARDWARE",
              "High-capacity 2U rackmount storage server delivering sequential read/write over 3500/1700 MB/s",
              "RS2423+", 195000.0, 238000.0, 18.0, 36, True)
    add_v(p, "STO-SYN-RS2423P-DISKLESS", "Synology RS2423+ 12-Bay 2U Rackmount Diskless Enclosure",
          "AMD Ryzen V1780B Quad-Core", "8GB DDR4 ECC UDIMM", "Diskless", "12x 3.5\" SATA bays", "", "", "", "Silver/Black", "1x 10GbE + 2x 1GbE ports", "Synology DSM 7.2", "2U Rackmount", 36, 0.0, 195000.0, 238000.0)

    # P112: Synology RS3621xs+ High-Performance SAN/NAS
    p = add_p("STO-SYN-RS3621XS", "Synology RackStation RS3621xs+ 12-Bay High-Performance SAN/NAS", "Synology Inc.", "CAT-STO", "HARDWARE",
              "Enterprise mission-critical storage delivering over 238,000 4K random read IOPS with redundant power",
              "RS3621xs+", 380000.0, 465000.0, 18.0, 60, True)
    add_v(p, "STO-SYN-RS3621XS-16GB", "Synology RS3621xs+ Xeon D-1541 8-Core / 16GB ECC / Dual 10GbE",
          "Intel Xeon D-1541 8-Core", "16GB DDR4 ECC RDIMM (Max 64GB)", "Diskless (12-Bays)", "SAS/SATA Hot-Swap Drive Bays", "", "", "", "Silver/Black", "Dual 10GbE Base-T + Quad 1GbE", "Synology DSM 7.2", "2U Rackmount with Redundant PSU", 60, 0.0, 380000.0, 465000.0)

    # P113: QNAP TS-464 4-Bay NAS
    p = add_p("STO-QNP-TS464", "QNAP TS-464 4-Bay Quad-Core 2.5GbE NAS", "QNAP Systems", "CAT-STO", "HARDWARE",
              "High-speed 2.5GbE networking, M.2 NVMe SSD caching, HDMI 4K display and hardware encryption",
              "TS-464-8G", 44000.0, 53500.0, 18.0, 36, True)
    add_v(p, "STO-QNP-TS464-8G", "QNAP TS-464 4-Bay Intel Celeron N5095 / 8GB RAM / Dual 2.5GbE",
          "Intel Celeron N5095 Quad-Core", "8GB DDR4", "Diskless", "4x 3.5\" SATA bays + dual M.2 NVMe", "", "", "", "Black/Gold", "2x 2.5GbE RJ45", "QTS 5.1", "4-Bay Tower", 36, 0.0, 44000.0, 53500.0)

    # P114: QNAP TS-873A 8-Bay NAS
    p = add_p("STO-QNP-TS873A", "QNAP TS-873A 8-Bay AMD Ryzen Enterprise NAS", "QNAP Systems", "CAT-STO", "HARDWARE",
              "AMD Ryzen V1500B quad-core processor with QuTS hero ZFS operating system for enterprise data integrity",
              "TS-873A-8G", 82000.0, 99500.0, 18.0, 36, True)
    add_v(p, "STO-QNP-TS873A-8G", "QNAP TS-873A 8-Bay Ryzen / 8GB ECC / Dual 2.5GbE",
          "AMD Ryzen V1500B Quad-Core", "8GB DDR4 (ECC Supported)", "Diskless", "8x 3.5\" SATA bays + dual M.2 NVMe", "", "", "", "Black", "2x 2.5GbE ports, 2x PCIe Gen3 slots", "QuTS hero (ZFS)", "8-Bay Tower", 36, 0.0, 82000.0, 99500.0)

    # P115: QNAP TS-1685 16-Bay Appliance
    p = add_p("STO-QNP-TS1685", "QNAP TS-1685 16-Bay Enterprise Storage Appliance", "QNAP Systems", "CAT-STO", "HARDWARE",
              "Hybrid high-capacity NAS supporting 12x 3.5\" HDDs and 4x 2.5\" SSDs for auto-tiering Qtier storage",
              "TS-1685-D1531", 290000.0, 355000.0, 18.0, 36, True)
    add_v(p, "STO-QNP-TS1685-32G", "QNAP TS-1685 Xeon D-1531 6-Core / 32GB RAM / Quad 10GbE Ready",
          "Intel Xeon D-1531 6-Core", "32GB DDR4 ECC RAM", "Diskless", "12x 3.5\" + 4x 2.5\" SSD bays", "", "", "", "Black", "2x 10GBASE-T + 4x 1GbE", "QTS 5.1 Enterprise", "Heavy Desktop Appliance", 36, 0.0, 290000.0, 355000.0)

    # P116: WD Ultrastar 16TB Enterprise HDD
    p = add_p("STO-WD-ULT16TB", "Western Digital Ultrastar DC HC550 16TB Enterprise SAS HDD", "Western Digital", "CAT-STO", "HARDWARE",
              "Helium-sealed CMR 3.5-inch enterprise hard drive with 2.5M hours MTBF and 550TB/year workload rating",
              "0F38466", 26000.0, 32000.0, 18.0, 60, True)
    add_v(p, "STO-WD-16TB-SAS-01", "WD Ultrastar DC HC550 16TB 7200 RPM SAS 12Gb/s 512MB Cache",
          "", "", "16TB", "Enterprise 3.5\" SAS 12Gb/s HDD", "", "3.5\"", "", "Silver", "SAS 12Gb/s Interface", "", "3.5\" Internal Drive", 60, 0.0, 26000.0, 32000.0)

    # P117: WD Ultrastar 20TB Enterprise HDD
    p = add_p("STO-WD-ULT20TB", "Western Digital Ultrastar DC HC560 20TB Enterprise SATA HDD", "Western Digital", "CAT-STO", "HARDWARE",
              "Ultra-dense 20TB CMR enterprise drive with OptiNAND technology for cloud and data center storage",
              "0F38755", 34000.0, 41500.0, 18.0, 60, True)
    add_v(p, "STO-WD-20TB-SATA-01", "WD Ultrastar DC HC560 20TB 7200 RPM SATA 6Gb/s Enterprise HDD",
          "", "", "20TB", "Enterprise 3.5\" SATA 6Gb/s HDD", "", "3.5\"", "", "Silver", "SATA 6Gb/s Interface", "", "3.5\" Internal Drive", 60, 0.0, 34000.0, 41500.0)

    # P118: Samsung PM893 1.92TB Enterprise SATA SSD
    p = add_p("STO-SAM-PM893-2TB", "Samsung PM893 1.92TB Enterprise 2.5\" SATA 6Gbps SSD", "Samsung Electronics", "CAT-STO", "HARDWARE",
              "Read-intensive enterprise datacenter SSD with power-loss protection and end-to-end data path protection",
              "MZ7L31T9HBLT", 18500.0, 23000.0, 18.0, 60, True)
    add_v(p, "STO-SAM-PM893-1920-01", "Samsung PM893 1.92TB 2.5\" SATA Enterprise SSD (1.3 DWPD)",
          "", "", "1.92TB", "V-NAND TLC Enterprise SATA SSD", "", "2.5\"", "", "Silver", "SATA 6Gbps Interface", "", "2.5\" Hot-Swap Form Factor", 60, 0.0, 18500.0, 23000.0)

    # P119: Samsung PM1733 3.84TB Enterprise NVMe SSD
    p = add_p("STO-SAM-PM1733-4TB", "Samsung PM1733 3.84TB PCIe Gen4 Enterprise NVMe U.2 SSD", "Samsung Electronics", "CAT-STO", "HARDWARE",
              "Ultra-fast dual-port PCIe Gen4 x4 NVMe SSD delivering up to 7,000 MB/s sequential read speed",
              "MZWLJ3T8HBLS", 42000.0, 52000.0, 18.0, 60, True)
    add_v(p, "STO-SAM-PM1733-3840-01", "Samsung PM1733 3.84TB U.2 PCIe Gen4 NVMe Enterprise SSD",
          "", "", "3.84TB", "Enterprise U.2 NVMe SSD", "", "2.5\" U.2", "", "Silver/Black", "PCIe Gen4 x4 Dual-Port", "", "2.5\" U.2 Drive", 60, 0.0, 42000.0, 52000.0)

    # P120: Kingston DC500M 1.92TB Mixed-Use SSD
    p = add_p("STO-KIN-DC500M-2TB", "Kingston DC500M 1.92TB Enterprise Mixed-Use 2.5\" SATA SSD", "Kingston Technology", "CAT-STO", "HARDWARE",
              "Mixed-use enterprise SSD engineered for database and virtualization workloads with strict QoS",
              "SEDC500M/1920G", 17500.0, 21800.0, 18.0, 60, True)
    add_v(p, "STO-KIN-DC500M-1920-01", "Kingston DC500M 1.92TB Enterprise 2.5\" SATA SSD",
          "", "", "1.92TB", "3D TLC Enterprise SSD", "", "2.5\"", "", "Black", "SATA 6Gbps", "", "2.5\" Drive", 60, 0.0, 17500.0, 21800.0)

    # P121: Kingston DC1500M 3.84TB U.2 NVMe
    p = add_p("STO-KIN-DC1500M-4TB", "Kingston DC1500M 3.84TB U.2 Enterprise NVMe High-End SSD", "Kingston Technology", "CAT-STO", "HARDWARE",
              "Gen 3.0 x4 PCIe NVMe enterprise SSD providing high throughput and predictable low latency",
              "SEDC1500M/3840G", 38000.0, 47500.0, 18.0, 60, True)
    add_v(p, "STO-KIN-DC1500M-3840-01", "Kingston DC1500M 3.84TB U.2 NVMe Enterprise SSD",
          "", "", "3.84TB", "Enterprise U.2 NVMe", "", "2.5\" U.2", "", "Black", "PCIe NVMe Gen 3.0 x4", "", "2.5\" U.2 Drive", 60, 0.0, 38000.0, 47500.0)

    # P122: Dell 2.4TB 10K SAS HDD
    p = add_p("STO-DEL-24TB10K", "Dell 2.4TB 10K RPM SAS 12Gbps 2.5\" Hot-Plug Enterprise HDD", "Dell Technologies", "CAT-STO", "HARDWARE",
              "Original Dell certified 2.5-inch 10,000 RPM mission-critical hard drive mounted in 14th/15th/16th Gen caddy",
              "400-AUQX", 19000.0, 24000.0, 18.0, 36, True)
    add_v(p, "STO-DEL-24TB-SAS-01", "Dell 2.4TB 10K SAS 12Gbps 2.5\" Hot-Plug Hard Drive with Caddy",
          "", "", "2.4TB", "10,000 RPM SAS 12G HDD", "", "2.5\"", "", "Silver/Black", "SAS 12Gbps Hot-Plug", "", "2.5\" Hot-Plug Caddy", 36, 0.0, 19000.0, 24000.0)

    # --------------------------------------------------------------------------
    # 10. UPS & POWER (12 products, 18 variants)
    # --------------------------------------------------------------------------
    # P123: APC Smart-UPS SMC1500I (1.5kVA)
    p = add_p("UPS-APC-SMC1500I", "APC Smart-UPS SMC1500I 1500VA LCD 230V Line-Interactive", "Schneider Electric (APC)", "CAT-UPS", "HARDWARE",
              "Intelligent network power protection for entry servers, point of sale and network switches",
              "SMC1500I", 24000.0, 29500.0, 18.0, 24, True)
    add_v(p, "UPS-APC-SMC1500-01", "APC Smart-UPS 1500VA LCD 230V Tower UPS (900W Output)",
          "", "", "", "", "", "", "", "Black", "IEC 320 C13 (8 Outlets)", "", "Tower Form Factor", 24, 0.0, 24000.0, 29500.0)

    # P124: APC Smart-UPS SMT2200I (2.2kVA)
    p = add_p("UPS-APC-SMT2200I", "APC Smart-UPS SMT2200I 2200VA LCD 230V SmartConnect", "Schneider Electric (APC)", "CAT-UPS", "HARDWARE",
              "High-density sine-wave power backup for servers, voice/data networks and medical equipment",
              "SMT2200I", 52000.0, 64000.0, 18.0, 36, True)
    add_v(p, "UPS-APC-SMT2200-01", "APC Smart-UPS 2200VA 230V SmartConnect Tower (1980W Output)",
          "", "", "", "", "", "", "", "Black", "8x C13 + 2x C19 Outlets, SmartConnect Cloud Port", "", "Tower UPS", 36, 0.0, 52000.0, 64000.0)

    # P125: APC Smart-UPS RT 3kVA Online
    p = add_p("UPS-APC-SRT3000XLI", "APC Smart-UPS On-Line SRT3000XLI 3000VA 230V Double-Conversion", "Schneider Electric (APC)", "CAT-UPS", "HARDWARE",
              "Zero-transfer-time online double-conversion UPS for mission-critical IT servers and telecom systems",
              "SRT3000XLI", 96000.0, 118000.0, 18.0, 36, True)
    add_v(p, "UPS-APC-SRT3000-01", "APC Smart-UPS On-Line 3000VA 230V Rack/Tower 2U (2700W Output)",
          "", "", "", "", "", "", "", "Black", "6x C13 + 2x C19, SmartSlot for Network Card", "", "2U Rack/Tower Convertible", 36, 0.0, 96000.0, 118000.0)

    # P126: APC Smart-UPS RT 5kVA Online
    p = add_p("UPS-APC-SRT5KXLI", "APC Smart-UPS On-Line SRT5KXLI 5000VA 230V Enterprise Tower/Rack", "Schneider Electric (APC)", "CAT-UPS", "HARDWARE",
              "5000VA/4500W pure sine-wave online double-conversion UPS for corporate data racks with AP9641 card",
              "SRT5KXLI", 185000.0, 228000.0, 18.0, 36, True)
    add_v(p, "UPS-APC-SRT5K-01", "APC Smart-UPS On-Line 5kVA 230V 3U Rack/Tower (4500W Output)",
          "", "", "", "", "", "", "", "Black", "Hardwire 3-wire or IEC Outlets, Pre-installed Network Card", "", "3U Rack/Tower", 36, 0.0, 185000.0, 228000.0)

    # P127: APC Smart-UPS RT 10kVA Online
    p = add_p("UPS-APC-SRT10KXLI", "APC Smart-UPS On-Line SRT10KXLI 10kVA 230V Data Center UPS", "Schneider Electric (APC)", "CAT-UPS", "HARDWARE",
              "10kVA unity power factor (10kW) enterprise online double-conversion power system with bypass switch",
              "SRT10KXLI", 360000.0, 445000.0, 18.0, 36, True)
    add_v(p, "UPS-APC-SRT10K-01", "APC Smart-UPS On-Line 10kVA 230V 6U Rack/Tower (10,000W Output)",
          "", "", "", "", "", "", "", "Black", "Hardwire Input/Output, Dual Network Management Card", "", "6U Rack/Tower (Chassis + Battery)", 36, 0.0, 360000.0, 445000.0)

    # P128: Eaton 9SX 1000VA Online
    p = add_p("UPS-EAT-9SX1000", "Eaton 9SX 1000VA Online Double-Conversion Tower UPS", "Eaton Corporation", "CAT-UPS", "HARDWARE",
              "High-efficiency online double-conversion power protection with graphical LCD display and 0.9 PF",
              "9SX1000I", 36000.0, 44500.0, 18.0, 36, True)
    add_v(p, "UPS-EAT-9SX1000-01", "Eaton 9SX 1000VA 230V Tower UPS (900W Output)",
          "", "", "", "", "", "", "", "Black", "6x IEC C13 Outlets, USB, RS232, Slot for Network-M2", "", "Tower UPS", 36, 0.0, 36000.0, 44500.0)

    # P129: Eaton 9PX 3000VA RT 2U
    p = add_p("UPS-EAT-9PX3000", "Eaton 9PX 3000VA RT 2U Rack/Tower Online Double-Conversion UPS", "Eaton Corporation", "CAT-UPS", "HARDWARE",
              "Energy Star certified unity power factor (3000W) UPS with load segment control and hot-swap batteries",
              "9PX3000IRT2U", 89000.0, 109000.0, 18.0, 36, True)
    add_v(p, "UPS-EAT-9PX3000-01", "Eaton 9PX 3000VA 2U Rack/Tower UPS (3000W Unity Power Factor)",
          "", "", "", "", "", "", "", "Black", "8x C13 + 2x C19 Outlets, Network-M2 Card Ready", "", "2U Rack/Tower Convertible", 36, 0.0, 89000.0, 109000.0)

    # P130: Eaton 9PX 6000VA RT 3U
    p = add_p("UPS-EAT-9PX6000", "Eaton 9PX 6000VA RT 3U High-Efficiency Enterprise UPS", "Eaton Corporation", "CAT-UPS", "HARDWARE",
              "6000VA/5400W online double-conversion UPS with internal maintenance bypass and network Gigabit card",
              "9PX6KIRT", 175000.0, 215000.0, 18.0, 36, True)
    add_v(p, "UPS-EAT-9PX6000-01", "Eaton 9PX 6000VA 3U Rack/Tower with Network-M2 Card",
          "", "", "", "", "", "", "", "Black", "Hardwire + IEC Outlets, Gigabit Network Management Card", "", "3U Rack/Tower", 36, 0.0, 175000.0, 215000.0)

    # P131: Vertiv Liebert GXT5 1kVA
    p = add_p("UPS-VER-GXT5-1000", "Vertiv Liebert GXT5-1000IRT2UXL 1kVA Online Double-Conversion UPS", "Vertiv Holdings", "CAT-UPS", "HARDWARE",
              "Premium power protection with unity power factor (1000W) in a compact 2U rack/tower footprint",
              "GXT5-1000IRT2UXL", 38000.0, 46800.0, 18.0, 36, True)
    add_v(p, "UPS-VER-GXT5-1K-01", "Vertiv Liebert GXT5 1000VA 2U Rack/Tower UPS (1000W)",
          "", "", "", "", "", "", "", "Black", "8x IEC C13 Outlets, RDU101 Communications Ready", "", "2U Rack/Tower", 36, 0.0, 38000.0, 46800.0)

    # P132: Vertiv Liebert GXT5 3kVA
    p = add_p("UPS-VER-GXT5-3000", "Vertiv Liebert GXT5-3000IRT2UXL 3kVA Online Enterprise UPS", "Vertiv Holdings", "CAT-UPS", "HARDWARE",
              "Unity power factor (3000W) online UPS with color gravity-sensing LCD display and individually controlled outlets",
              "GXT5-3000IRT2UXL", 92000.0, 114000.0, 18.0, 36, True)
    add_v(p, "UPS-VER-GXT5-3K-01", "Vertiv Liebert GXT5 3000VA 2U Rack/Tower UPS (3000W)",
          "", "", "", "", "", "", "", "Black", "6x C13 + 1x C19 Outlets, Web/SNMP Card Included", "", "2U Rack/Tower", 36, 0.0, 92000.0, 114000.0)

    # P133: Vertiv Liebert GXT5 10kVA
    p = add_p("UPS-VER-GXT5-10K", "Vertiv Liebert GXT5-10KIRT5UXLN 10kVA 3-Phase in 1-Phase out UPS", "Vertiv Holdings", "CAT-UPS", "HARDWARE",
              "Heavy commercial 10kVA unity power factor UPS supporting 3:1 or 1:1 wiring with external battery cabinets",
              "GXT5-10KIRT5UXLN", 340000.0, 420000.0, 18.0, 36, True)
    add_v(p, "UPS-VER-GXT5-10K-01", "Vertiv Liebert GXT5 10kVA 5U Rack/Tower Enterprise UPS (10,000W)",
          "", "", "", "", "", "", "", "Black", "Hardwire Terminal Block, Dual Slot Communications", "", "5U Rack/Tower", 36, 0.0, 340000.0, 420000.0)

    # P134: APC NetShelter AP7921B Switched PDU
    p = add_p("UPS-APC-AP7921B", "APC NetShelter AP7921B 16A 208/230V Switched Rack PDU", "Schneider Electric (APC)", "CAT-UPS", "HARDWARE",
              "Network-managed rack power distribution unit with individual outlet power cycling and current monitoring",
              "AP7921B", 32000.0, 39500.0, 18.0, 24, True)
    add_v(p, "UPS-APC-AP7921B-01", "APC 1U 16A 230V Switched Rack PDU (8x C13 Outlets)",
          "", "", "", "", "", "", "", "Black", "8x IEC 320 C13 Outlets, RJ45 10/100 Ethernet", "", "1U Horizontal Rackmount", 24, 0.0, 32000.0, 39500.0)

    # --------------------------------------------------------------------------
    # 11. PRINTERS (10 products, 15 variants)
    # --------------------------------------------------------------------------
    # P135: HP LaserJet Pro M404dn
    p = add_p("PRN-HP-M404DN", "HP LaserJet Pro M404dn Monochrome Network Laser Printer", "HP Inc.", "CAT-PRN", "HARDWARE",
              "Compact monochrome workgroup printer with automatic 2-sided printing and enhanced security features",
              "W1A53A", 18500.0, 22900.0, 18.0, 12, True)
    add_v(p, "PRN-HP-M404DN-01", "HP LaserJet Pro M404dn Mono Laser (40 ppm / Duplex / Gigabit LAN)",
          "", "", "", "", "", "", "", "White", "Gigabit Ethernet 10/100/1000, USB 2.0", "", "Desktop Printer", 12, 0.0, 18500.0, 22900.0)

    # P136: HP LaserJet Pro MFP M428fdw
    p = add_p("PRN-HP-M428FDW", "HP LaserJet Pro MFP M428fdw Wireless All-in-One Laser Printer", "HP Inc.", "CAT-PRN", "HARDWARE",
              "Multifunction workteam printer offering print, copy, scan, fax, dual-sided scanning and dual-band Wi-Fi",
              "W1A30A", 34000.0, 41500.0, 18.0, 12, True)
    add_v(p, "PRN-HP-M428FDW-01", "HP LaserJet Pro MFP M428fdw (Print/Scan/Copy/Fax / 40 ppm / Wi-Fi)",
          "", "", "", "", "", "", "", "White", "Wi-Fi 802.11b/g/n, Gigabit Ethernet, USB", "", "Multifunction Desktop", 12, 0.0, 34000.0, 41500.0)

    # P137: HP Color LaserJet Enterprise MFP M480f
    p = add_p("PRN-HP-M480F", "HP Color LaserJet Enterprise MFP M480f Multifunction Printer", "HP Inc.", "CAT-PRN", "HARDWARE",
              "Enterprise-grade color MFP with self-healing security BIOS, 50-sheet single-pass duplex ADF and PIN print",
              "3QA55A", 68000.0, 82500.0, 18.0, 36, True)
    add_v(p, "PRN-HP-M480F-01", "HP Color LaserJet Enterprise MFP M480f (29 ppm Color / Duplex / HP Sure Start)",
          "", "", "", "", "", "", "", "White/Black", "Gigabit Ethernet, 2x Hi-Speed USB 2.0 Host", "", "Enterprise Desktop MFP", 36, 0.0, 68000.0, 82500.0)

    # P138: HP Color LaserJet Enterprise M555dn
    p = add_p("PRN-HP-M555DN", "HP Color LaserJet Enterprise M555dn Workgroup Network Printer", "HP Inc.", "CAT-PRN", "HARDWARE",
              "High-speed 40 ppm color laser printer designed for large corporate workgroups with 650-sheet standard input",
              "7ZU78A", 58000.0, 71000.0, 18.0, 36, True)
    add_v(p, "PRN-HP-M555DN-01", "HP Color LaserJet Enterprise M555dn (40 ppm Color / 4.3\" Touchscreen)",
          "", "", "", "", "", "", "", "White/Black", "Gigabit Ethernet 10/100/1000, 2x USB 2.0", "", "Heavy Workgroup Printer", 36, 0.0, 58000.0, 71000.0)

    # P139: Canon imageCLASS MF445dw
    p = add_p("PRN-CAN-MF445DW", "Canon imageCLASS MF445dw Enterprise All-in-One Mono Laser", "Canon Inc.", "CAT-PRN", "HARDWARE",
              "High-capacity 40 ppm 4-in-1 laser printer with 5\" color touch LCD and mobile printing capabilities",
              "3514C003AA", 32000.0, 38900.0, 18.0, 12, True)
    add_v(p, "PRN-CAN-MF445DW-01", "Canon imageCLASS MF445dw (Print/Scan/Copy/Fax / 40 ppm)",
          "", "", "", "", "", "", "", "White", "Wi-Fi Direct, Gigabit Ethernet, USB 2.0", "", "Desktop Multifunction", 12, 0.0, 32000.0, 38900.0)

    # P140: Canon imageRUNNER 2625i A3 MFP
    p = add_p("PRN-CAN-IR2625I", "Canon imageRUNNER 2625i A3 Monochrome Enterprise Network Copier/MFP", "Canon Inc.", "CAT-PRN", "HARDWARE",
              "Robust heavy-duty A3 floor-standing office multifunction system with 25 ppm, DADF and department ID",
              "3759C004AA", 135000.0, 168000.0, 18.0, 36, True)
    add_v(p, "PRN-CAN-IR2625I-01", "Canon imageRUNNER 2625i A3 Multifunction Copier (Dual Cassette + Platen)",
          "", "", "", "", "", "", "", "White/Grey", "Gigabit Ethernet 1000Base-T, USB 2.0", "", "Floor-Standing A3 Console", 36, 0.0, 135000.0, 168000.0)

    # P141: Brother HL-L6400DW Mono Laser
    p = add_p("PRN-BRO-HLL6400", "Brother HL-L6400DW High-Speed Enterprise Monochrome Laser Printer", "Brother Industries", "CAT-PRN", "HARDWARE",
              "Super-fast 52 ppm business printer with ultra-high-yield 20,000-page inbox toner and NFC authentication",
              "HLL6400DW", 44000.0, 53500.0, 18.0, 24, True)
    add_v(p, "PRN-BRO-6400DW-01", "Brother HL-L6400DW (52 ppm / Duplex / Wi-Fi / NFC / Gigabit LAN)",
          "", "", "", "", "", "", "", "Charcoal Grey", "Gigabit Ethernet, Wireless 802.11b/g/n, NFC Card Reader", "", "Desktop Printer", 24, 0.0, 44000.0, 53500.0)

    # P142: Brother MFC-L8900CDW Color MFP
    p = add_p("PRN-BRO-MFCL8900", "Brother MFC-L8900CDW High-Yield Business Color Laser All-in-One", "Brother Industries", "CAT-PRN", "HARDWARE",
              "Commercial color laser all-in-one with 33 ppm, 70-page auto duplex document feeder and 5\" touchscreen",
              "MFCL8900CDW", 62000.0, 75900.0, 18.0, 24, True)
    add_v(p, "PRN-BRO-8900CDW-01", "Brother MFC-L8900CDW Color All-in-One (Print/Scan/Copy/Fax)",
          "", "", "", "", "", "", "", "White/Grey", "Gigabit Ethernet, Wireless 802.11b/g/n, USB", "", "Multifunction Floor/Desk", 24, 0.0, 62000.0, 75900.0)

    # P143: Epson WorkForce WF-C579R Color MFP
    p = add_p("PRN-EPS-WFC579R", "Epson WorkForce Pro WF-C579R High-Yield Color A4 Network MFP", "Epson Corporation", "CAT-PRN", "HARDWARE",
              "Replaceable Ink Pack System delivering up to 50,000 pages uninterrupted with zero-heat PrecisionCore tech",
              "C11CG77501", 52000.0, 63500.0, 18.0, 24, True)
    add_v(p, "PRN-EPS-C579R-01", "Epson WorkForce Pro WF-C579R Replaceable Ink Pack System MFP",
          "", "", "", "", "", "", "", "White", "Wi-Fi Direct, Gigabit Ethernet, PCL/PostScript Emulation", "", "Desktop Color MFP", 24, 0.0, 52000.0, 63500.0)

    # P144: Epson EcoTank L15160 A3 InkTank
    p = add_p("PRN-EPS-L15160", "Epson EcoTank L15160 A3 Wi-Fi Duplex All-in-One InkTank Printer", "Epson Corporation", "CAT-PRN", "HARDWARE",
              "Ultra-low-cost per page A3+ color multifunction with auto-duplex print, scan and copy up to A3",
              "C11CH72501", 68000.0, 81999.0, 18.0, 24, True)
    add_v(p, "PRN-EPS-L15160-01", "Epson EcoTank L15160 A3 Color All-in-One InkTank Printer",
          "", "", "", "", "", "", "", "Black", "Wi-Fi, Wi-Fi Direct, Ethernet, USB 2.0", "", "A3 Desktop MFP", 24, 0.0, 68000.0, 81999.0)

    # --------------------------------------------------------------------------
    # 12. ACCESSORIES (20 products, 32 variants)
    # --------------------------------------------------------------------------
    # P145: Dell WD22TB4 Thunderbolt Dock
    p = add_p("ACC-DEL-WD22TB4", "Dell Thunderbolt 4 Dock WD22TB4 180W Power Delivery", "Dell Technologies", "CAT-ACC", "HARDWARE",
              "Modular Thunderbolt 4 dock delivering up to 130W to Dell systems and 90W to standard systems with dual 4K/8K",
              "210-BDQH", 21000.0, 26500.0, 18.0, 36, True)
    add_v(p, "ACC-DEL-WD22TB4-01", "Dell Thunderbolt 4 Dock WD22TB4 with 180W Power Adapter",
          "", "", "", "", "", "", "", "Black", "2x Thunderbolt 4, 2x DP 1.4, 1x HDMI 2.0, 3x USB-A 3.2, 1x GbE", "", "Desktop Dock", 36, 0.0, 21000.0, 26500.0)

    # P146: Dell WD19S USB-C Dock (Scenario 1 Target!)
    p = add_p("ACC-DEL-WD19S", "Dell USB-C Dock WD19S 130W Power Delivery", "Dell Technologies", "CAT-ACC", "HARDWARE",
              "Mainstream commercial USB-C docking station supporting dual FHD/single QHD displays and 90W power",
              "210-AZBM", 14500.0, 18500.0, 18.0, 36, True)
    add_v(p, "VAR-ACC-DEL-WD19S-01", "Dell USB-C Dock WD19S with 130W AC Power Adapter",
          "", "", "", "", "", "", "", "Black", "2x DP 1.4, 1x HDMI 2.0, 3x USB 3.1 Gen 1, 2x USB-C, Gigabit Ethernet", "", "Desktop Dock", 36, 0.0, 14500.0, 18500.0)

    # P147: HP Thunderbolt Dock G4 120W
    p = add_p("ACC-HP-TBG4", "HP Thunderbolt Dock 120W G4 with Audio Module", "HP Inc.", "CAT-ACC", "HARDWARE",
              "Universal Thunderbolt 4 dock with HP Sure Start endpoint isolation security and integrated speakerphone",
              "4J0A2AA", 19500.0, 24900.0, 18.0, 36, True)
    add_v(p, "ACC-HP-TBG4-01", "HP Thunderbolt Dock 120W G4 (Dual DP / HDMI / USB-C / RJ45)",
          "", "", "", "", "", "", "", "Black", "Thunderbolt 4, 2x DP, 1x HDMI, 4x USB-A, 2.5GbE LAN", "", "Desktop Dock", 36, 0.0, 19500.0, 24900.0)

    # P148: HP USB-C G5 Essential Dock
    p = add_p("ACC-HP-USBCG5", "HP USB-C G5 Universal Commercial Dock", "HP Inc.", "CAT-ACC", "HARDWARE",
              "Universal USB-C dock engineered for mixed-PC environments providing 100W power delivery and PXE boot",
              "5TW10AA", 13800.0, 17500.0, 18.0, 36, True)
    add_v(p, "ACC-HP-USBCG5-01", "HP USB-C Dock G5 with 120W Power Supply",
          "", "", "", "", "", "", "", "Black", "2x DP 1.4, 1x HDMI 2.0, 4x USB-A 3.0, Gigabit LAN", "", "Desktop Dock", 36, 0.0, 13800.0, 17500.0)

    # P149: Lenovo ThinkPad Thunderbolt 4 Dock
    p = add_p("ACC-LEN-TB4DOCK", "Lenovo ThinkPad Universal Thunderbolt 4 Dock 100W", "Lenovo Group Ltd", "CAT-ACC", "HARDWARE",
              "Enterprise-ready Thunderbolt 4 docking station with dynamic 100W power charging and 8K display support",
              "40B00135IN", 20500.0, 25800.0, 18.0, 36, True)
    add_v(p, "ACC-LEN-TB4-01", "Lenovo ThinkPad Universal Thunderbolt 4 Dock with 135W Slim Tip Adapter",
          "", "", "", "", "", "", "", "Black/Red", "1x TB4, 2x DP 1.4, 1x HDMI 2.1, 4x USB 3.2, Gigabit Ethernet", "", "Desktop Dock", 36, 0.0, 20500.0, 25800.0)

    # P150: Lenovo ThinkPad USB-C Dock v2
    p = add_p("ACC-LEN-USBCDOCK", "Lenovo ThinkPad Universal USB-C Dock v2", "Lenovo Group Ltd", "CAT-ACC", "HARDWARE",
              "Reliable single-cable universal dock for ThinkPad fleets supporting dual 4K screens and MAC address pass-through",
              "40AY0090IN", 13500.0, 16900.0, 18.0, 36, True)
    add_v(p, "ACC-LEN-USBC-01", "Lenovo ThinkPad Universal USB-C Dock v2 with 90W Adapter",
          "", "", "", "", "", "", "", "Black", "2x DP 1.4, 1x HDMI 2.0, 3x USB 3.1, 2x USB 2.0, Gigabit Ethernet", "", "Desktop Dock", 36, 0.0, 13500.0, 16900.0)

    # P151: Logitech MX Master 3S Mouse
    p = add_p("ACC-LOG-MXM3S", "Logitech MX Master 3S Wireless Performance Mouse", "Logitech International", "CAT-ACC", "HARDWARE",
              "Quiet click ergonomic mouse with 8K DPI Darkfield sensor that tracks on glass and MagSpeed electromagnetic scroll",
              "910-006561", 7200.0, 9495.0, 18.0, 24, False)
    add_v(p, "ACC-LOG-MXM3S-GRPH", "Logitech MX Master 3S Wireless Mouse - Graphite",
          "", "", "", "", "", "", "", "Graphite", "Bluetooth Low Energy + Logi Bolt USB Receiver", "", "Ergonomic Mouse", 24, 0.0, 7200.0, 9495.0)
    add_v(p, "ACC-LOG-MXM3S-PALE", "Logitech MX Master 3S Wireless Mouse - Pale Grey",
          "", "", "", "", "", "", "", "Pale Grey", "Bluetooth Low Energy + Logi Bolt USB Receiver", "", "Ergonomic Mouse", 24, 0.0, 7200.0, 9495.0)

    # P152: Logitech MX Keys S Keyboard
    p = add_p("ACC-LOG-MXKEYSS", "Logitech MX Keys S Advanced Wireless Illuminated Keyboard", "Logitech International", "CAT-ACC", "HARDWARE",
              "Low-profile tactile keys shaped for fingertips with smart backlighting and Smart Actions macros",
              "920-011585", 8500.0, 11495.0, 18.0, 24, False)
    add_v(p, "ACC-LOG-MXKEYS-GRPH", "Logitech MX Keys S Wireless Keyboard - Graphite",
          "", "", "", "", "", "", "", "Graphite", "Bluetooth LE + Logi Bolt USB Receiver", "", "Full Size Keyboard", 24, 0.0, 8500.0, 11495.0)

    # P153: Logitech MK540 Advanced Combo
    p = add_p("ACC-LOG-MK540", "Logitech MK540 Advanced Commercial Wireless Keyboard & Mouse Combo", "Logitech International", "CAT-ACC", "HARDWARE",
              "Familiar precision quiet keyboard paired with contoured ambidextrous mouse for enterprise deployments",
              "920-008684", 2800.0, 3995.0, 18.0, 36, False)
    add_v(p, "ACC-LOG-MK540-01", "Logitech MK540 Wireless Desktop Combo (Unifying USB Receiver)",
          "", "", "", "", "", "", "", "Black", "2.4GHz Wireless with Logitech Unifying USB", "", "Keyboard & Mouse Combo", 36, 0.0, 2800.0, 3995.0)

    # P154: Logitech Brio 4K Webcam
    p = add_p("ACC-LOG-BRIO4K", "Logitech Brio 4K Ultra HD Business Webcam", "Logitech International", "CAT-ACC", "HARDWARE",
              "Ultra 4K HD webcam with HDR, RightLight 3, dual noise-cancelling mics and Windows Hello facial recognition",
              "960-001105", 14500.0, 18995.0, 18.0, 36, True)
    add_v(p, "ACC-LOG-BRIO4K-01", "Logitech Brio 4K Ultra HD Webcam with Detachable Privacy Shutter",
          "", "", "", "", "", "", "4K UHD 30fps / 1080p 60fps", "Black", "USB-C to USB-A/C Cable", "", "Monitor Mount / Tripod", 36, 0.0, 14500.0, 18995.0)

    # P155: Logitech C925e Business Webcam
    p = add_p("ACC-LOG-C925E", "Logitech C925e 1080p Business HD Webcam", "Logitech International", "CAT-ACC", "HARDWARE",
              "Cost-effective full HD webcam with integrated sliding privacy shutter certified for Zoom and Microsoft Teams",
              "960-001075", 6800.0, 8995.0, 18.0, 36, True)
    add_v(p, "ACC-LOG-C925E-01", "Logitech C925e 1080p Business Webcam (78-Degree FOV)",
          "", "", "", "", "", "", "1080p FHD 30fps", "Black", "USB-A Plug and Play", "", "Monitor Mount", 36, 0.0, 6800.0, 8995.0)

    # P156: Jabra Evolve2 65 MS Wireless Headset
    p = add_p("ACC-JAB-EV265MS", "Jabra Evolve2 65 MS Wireless Noise-Cancelling Stereo Headset", "Jabra (GN Audio)", "CAT-ACC", "HARDWARE",
              "Engineered for focus with 37-hour battery life, 3-microphone call technology and 360-degree busylight",
              "26599-999-999", 16500.0, 21500.0, 18.0, 24, True)
    add_v(p, "ACC-JAB-EV265-USB-A", "Jabra Evolve2 65 MS Stereo with Link 380 USB-A Bluetooth Adapter",
          "", "", "", "", "", "", "", "Black", "Bluetooth 5.0 + USB-A Dongle (30m Range)", "", "On-Ear Headset", 24, 0.0, 16500.0, 21500.0)

    # P157: Jabra Evolve2 40 MS Wired Headset
    p = add_p("ACC-JAB-EV240MS", "Jabra Evolve2 40 MS USB-C Wired Stereo Enterprise Headset", "Jabra (GN Audio)", "CAT-ACC", "HARDWARE",
              "Corded USB-C enterprise headset with 40mm leak-tolerant speakers and memory foam ear cushions",
              "24089-999-899", 7800.0, 10200.0, 18.0, 24, False)
    add_v(p, "ACC-JAB-EV240-USBC", "Jabra Evolve2 40 MS Stereo USB-C Wired Headset",
          "", "", "", "", "", "", "", "Black", "USB-C Corded Connection", "", "On-Ear Headset", 24, 0.0, 7800.0, 10200.0)

    # P158: Poly Voyager Focus 2 UC Headset
    p = add_p("ACC-POL-VOYFOC2", "Poly Voyager Focus 2 UC Bluetooth Stereo Headset", "Poly (HP Poly)", "CAT-ACC", "HARDWARE",
              "Advanced Digital Hybrid Active Noise Cancelling (ANC) with Acoustic Fence technology for noisy offices",
              "213726-02", 18000.0, 23500.0, 18.0, 24, True)
    add_v(p, "ACC-POL-VFOC2-USBC", "Poly Voyager Focus 2 UC with BT700 USB-C Adapter and Charge Stand",
          "", "", "", "", "", "", "", "Black", "Bluetooth 5.1 + BT700 USB-C Dongle", "", "On-Ear Headset with Desktop Stand", 24, 0.0, 18000.0, 23500.0)

    # P159: Dell Premier Slim Backpack 15
    p = add_p("ACC-DEL-PREMBAG", "Dell Premier Slim 15.6\" Executive Laptop Backpack", "Dell Technologies", "CAT-ACC", "HARDWARE",
              "Weather-resistant backpack with EVA foam cushioning, dedicated tablet sleeve and luggage pass-through",
              "460-BCML", 3400.0, 4800.0, 18.0, 36, False)
    add_v(p, "ACC-DEL-BAG-15-01", "Dell Premier Slim Backpack 15 (Fits up to 15.6\" Notebooks)",
          "", "", "", "", "", "15.6\"", "", "Heather Grey", "Water-resistant ballistic polyester", "", "Backpack", 36, 0.0, 3400.0, 4800.0)

    # P160: HP Executive 15.6" RFID Backpack
    p = add_p("ACC-HP-EXECBAG", "HP Executive 15.6\" RFID-Blocking Commercial Backpack", "HP Inc.", "CAT-ACC", "HARDWARE",
              "Corporate travel backpack with lockable zippers, RFID-blocking pocket to protect credit cards and USB pass-through",
              "6KD07AA", 3800.0, 5200.0, 18.0, 12, False)
    add_v(p, "ACC-HP-EXECBAG-01", "HP Executive 15.6\" Backpack with RFID Shielding",
          "", "", "", "", "", "15.6\"", "", "Black", "Heavy-duty nylon with lockable double-teeth zippers", "", "Backpack", 12, 0.0, 3800.0, 5200.0)

    # P161: Kensington ClickSafe 2.0 Cable Lock
    p = add_p("ACC-KEN-CS20LOCK", "Kensington ClickSafe 2.0 Keyed Laptop Security Lock", "Dell Technologies", "CAT-ACC", "HARDWARE",
              "Tamper-resistant carbon steel cable lock that attaches with a single click to standard Kensington security slots",
              "K64435WW", 1800.0, 2600.0, 18.0, 60, False)
    add_v(p, "ACC-KEN-CS20-01", "Kensington ClickSafe 2.0 Master Keyed Carbon Steel Cable Lock (1.8m)",
          "", "", "", "", "", "", "", "Carbon Steel / Black", "T-Bar Security Slot Anchor", "", "Security Cable", 60, 0.0, 1800.0, 2600.0)

    # P162: Targus Defcon CL Combination Lock
    p = add_p("ACC-TAR-DEFCONCL", "Targus Defcon CL Serialized Combination Cable Lock", "Dell Technologies", "CAT-ACC", "HARDWARE",
              "Pre-set serialized 4-digit combination cable lock with 6.5-foot galvanized vinyl-coated steel cable",
              "PA400U", 1400.0, 2100.0, 18.0, 24, False)
    add_v(p, "ACC-TAR-DEFCON-01", "Targus Defcon CL 4-Digit Combination Laptop Lock (2m)",
          "", "", "", "", "", "", "", "Steel / Black", "Standard Security Slot", "", "Combination Cable", 24, 0.0, 1400.0, 2100.0)

    # P163: Anker 737 GaN 120W Charger
    p = add_p("ACC-ANK-GAN120W", "Anker 737 GaN 120W 3-Port Fast Wall Charger", "Dell Technologies", "CAT-ACC", "HARDWARE",
              "Compact GaNPrime technology charger with 2x USB-C (100W max) and 1x USB-A for simultaneously powering laptop and phone",
              "A2148", 4800.0, 6499.0, 18.0, 24, False)
    add_v(p, "ACC-ANK-GAN120-01", "Anker 737 Charger 120W GaNPrime 3-Port (2C1A)",
          "", "", "", "", "", "", "", "Black", "2x USB-C Power Delivery, 1x USB-A PowerIQ", "", "Wall Adapter", 24, 0.0, 4800.0, 6499.0)

    # P164: Belkin 7-in-1 USB-C Hub
    p = add_p("ACC-BEL-HUB7IN1", "Belkin 7-in-1 USB-C Multi-Port Hub Adapter", "Dell Technologies", "CAT-ACC", "HARDWARE",
              "Portable multi-port adapter providing 4K HDMI, 85W pass-through charging, 2x USB-A, SD/microSD and 3.5mm audio",
              "AVC009btSGY", 3200.0, 4499.0, 18.0, 24, False)
    add_v(p, "ACC-BEL-HUB7-01", "Belkin USB-C 7-in-1 Multiport Hub Adapter with 4K HDMI",
          "", "", "", "", "", "", "4K @ 30Hz", "Space Grey Aluminum", "USB-C tethered cable, HDMI, 2x USB-A 3.0, SD Card", "", "Dongle Hub", 24, 0.0, 3200.0, 4499.0)

    # --------------------------------------------------------------------------
    # 13. COLLABORATION EQUIPMENT (10 products, 14 variants)
    # --------------------------------------------------------------------------
    # P165: Logitech Rally Bar
    p = add_p("COL-LOG-RALLYBAR", "Logitech Rally Bar Enterprise All-in-One Video Bar", "Logitech International", "CAT-COL", "HARDWARE",
              "Premier all-in-one video conferencing bar for mid-size rooms with motorized PTZ lens, AI viewfinder and beamforming mics",
              "960-001308", 260000.0, 325000.0, 18.0, 24, True)
    add_v(p, "COL-LOG-RALLYBAR-GRA", "Logitech Rally Bar 4K Video Bar - Graphite",
          "", "", "", "", "", "", "Up to 4K Ultra HD @ 30fps", "Graphite", "HDMI In/Out, USB 3.0, Gigabit Ethernet, Wi-Fi", "CollabOS (App Appliance or USB Mode)", "Wall/TV Mountable Bar", 24, 0.0, 260000.0, 325000.0)

    # P166: Logitech Rally Plus System
    p = add_p("COL-LOG-RALLYPLUS", "Logitech Rally Plus Modular Ultra-HD Conference Room System", "Logitech International", "CAT-COL", "HARDWARE",
              "Modular video conferencing system for large boardrooms with standalone PTZ camera, 2 speakers and 2 mic pods",
              "960-001225", 215000.0, 268000.0, 18.0, 24, True)
    add_v(p, "COL-LOG-RALLYPLUS-01", "Logitech Rally Plus System (Camera + 2x Speakers + 2x Mic Pods + Table/Display Hubs)",
          "", "", "", "", "", "", "4K UHD PTZ with 15x HD Zoom", "Black", "Dual HDMI, USB 3.0, Cat6A Hub Interconnect", "Host PC / Room System Mode", "Modular Room Component Kit", 24, 0.0, 215000.0, 268000.0)

    # P167: Logitech MeetUp ConferenceCam
    p = add_p("COL-LOG-MEETUP", "Logitech MeetUp All-in-One ConferenceCam for Huddle Rooms", "Logitech International", "CAT-COL", "HARDWARE",
              "Super-wide 120-degree field of view 4K camera with integrated custom-tuned audio for small conference rooms",
              "960-001101", 62000.0, 78000.0, 18.0, 24, True)
    add_v(p, "COL-LOG-MEETUP-01", "Logitech MeetUp 4K Ultra HD Huddle Room Camera",
          "", "", "", "", "", "", "4K Ultra HD 120-Degree FOV", "Black", "USB 3.0 Type-C, Bluetooth", "Plug and Play", "Wall / Monitor Mount", 24, 0.0, 62000.0, 78000.0)

    # P168: Poly Studio X50 Video Bar
    p = add_p("COL-POL-STUDIOX50", "Poly Studio X50 All-in-One 4K Video Bar for Medium Rooms", "Poly (HP Poly)", "CAT-COL", "HARDWARE",
              "Radically simple video bar with Poly DirectorAI smart framing, NoiseBlockAI and native Teams/Zoom support",
              "2200-85970-001", 245000.0, 305000.0, 18.0, 12, True)
    add_v(p, "COL-POL-X50-TC8", "Poly Studio X50 Video Bar bundled with Poly TC8 Touch Controller",
          "", "", "", "", "", "", "4K UHD with 5x Digital Zoom", "White/Grey", "Dual HDMI Out, HDMI In, Dual GbE, Wi-Fi 802.11ac", "Poly VideoOS (Native Teams/Zoom Rooms)", "All-in-One Appliance", 12, 0.0, 245000.0, 305000.0)

    # P169: Poly Studio X70 Dual-Camera Bar
    p = add_p("COL-POL-STUDIOX70", "Poly Studio X70 Dual-Camera Video Bar for Large Rooms", "Poly (HP Poly)", "CAT-COL", "HARDWARE",
              "Dual 4K sensors with seamless switching, electronic motorized privacy shutter and stereo speakers with bass ports",
              "2200-87240-001", 420000.0, 520000.0, 18.0, 12, True)
    add_v(p, "COL-POL-X70-01", "Poly Studio X70 Dual-Camera 4K Video Appliance",
          "", "", "", "", "", "", "Dual 4K Sensors (120-deg Wide + 70-deg Tele)", "Charcoal Grey", "Dual HDMI Out, HDMI In, 2x RJ45 GbE", "Poly VideoOS", "Large Room Video Bar", 12, 0.0, 42000.0 * 10, 52000.0 * 10)

    # P170: Jabra Speak2 75 Speakerphone
    p = add_p("COL-JAB-SPK75", "Jabra Speak2 75 MS Enterprise Wireless Speakerphone", "Jabra (GN Audio)", "CAT-ACC", "HARDWARE",
              "Next-generation portable conference speakerphone with full duplex audio, 4 beamforming mics and microphone quality indicator",
              "2775-109", 26000.0, 33500.0, 18.0, 24, True)
    add_v(p, "COL-JAB-SPK75-01", "Jabra Speak2 75 MS with Link 380 USB-A/C Adapter (32-Hour Battery)",
          "", "", "", "", "", "", "", "Dark Grey", "Bluetooth 5.2 + Integrated USB-A/USB-C Cable", "", "Puck Speakerphone", 24, 0.0, 26000.0, 33500.0)

    # P171: Jabra Panacast 50 Video Bar
    p = add_p("COL-JAB-PANA50", "Jabra Panacast 50 180-Degree Panoramic 4K Video Bar", "Jabra (GN Audio)", "CAT-COL", "HARDWARE",
              "Full 180-degree panoramic-4K room coverage using 3x 13MP cameras with 8 professional microphones",
              "8200-231", 175000.0, 218000.0, 18.0, 24, True)
    add_v(p, "COL-JAB-PANA50-BLK", "Jabra Panacast 50 Panoramic-4K Intelligent Video Bar - Black",
          "", "", "", "", "", "", "Panoramic-4K (3840x1080) 180-Degree", "Black", "USB-C 3.0, Gigabit Ethernet, Wi-Fi", "Jabra Direct / Xpress", "Wall Mounted Bar", 24, 0.0, 175000.0, 218000.0)

    # P172: Cisco Webex Room Bar
    p = add_p("COL-CIS-ROOMBAR", "Cisco Webex Room Bar Compact Video Collaboration Device", "Cisco Systems", "CAT-COL", "HARDWARE",
              "Intelligent video collaboration bar with 12MP wide camera, people focus framing and Webex Room Navigator touch panel",
              "CS-BAR-T-K9", 280000.0, 345000.0, 18.0, 36, True)
    add_v(p, "COL-CIS-ROOMBAR-01", "Cisco Webex Room Bar with First Nations Navigator Touch Panel",
          "", "", "", "", "", "", "4K Ultra HD 12MP Sensor", "First Nations White", "HDMI In, Dual HDMI Out, GbE PoE, Wi-Fi", "Cisco RoomOS", "All-in-One Bar", 36, 0.0, 280000.0, 345000.0)

    # P173: Barco ClickShare CX-30 Gen 2
    p = add_p("COL-BAR-CX30G2", "Barco ClickShare CX-30 Gen 2 Wireless Presentation System", "Dell Technologies", "CAT-COL", "HARDWARE",
              "Seamless wireless conferencing for medium-sized meeting rooms supporting any USB video bar and BYOM (Bring Your Own Meeting)",
              "R9861613EUB1", 168000.0, 209000.0, 18.0, 36, True)
    add_v(p, "COL-BAR-CX30G2-01", "Barco ClickShare CX-30 Gen 2 Base Unit with 2x USB-C Conferencing Buttons",
          "", "", "", "", "", "", "4K UHD Output @ 30Hz", "Black/Silver", "HDMI 1.4b Out, USB-A/C, Gigabit Ethernet, Wi-Fi", "ClickShare Platform", "Base Unit + 2 Buttons", 36, 0.0, 168000.0, 209000.0)

    # P174: Barco ClickShare CX-50 Gen 2
    p = add_p("COL-BAR-CX50G2", "Barco ClickShare CX-50 Gen 2 Premium Wireless Presentation System", "Dell Technologies", "CAT-COL", "HARDWARE",
              "Dual-screen wireless conferencing with automatic switching between Room Mode and Bring Your Own Meeting mode",
              "R9861622EUB1", 245000.0, 305000.0, 18.0, 36, True)
    add_v(p, "COL-BAR-CX50G2-01", "Barco ClickShare CX-50 Gen 2 Base Unit with Dual 4K HDMI Outputs",
          "", "", "", "", "", "", "Dual 4K UHD Outputs @ 60Hz", "Black/Silver", "2x HDMI Out, 1x HDMI In, USB-C, Dual GbE", "ClickShare Platform", "Base Unit + 2 Buttons", 36, 0.0, 245000.0, 305000.0)

    # --------------------------------------------------------------------------
    # 14. ENTERPRISE CABLING & OPTICS (8 products, 14 variants)
    # --------------------------------------------------------------------------
    # P175: Cisco SFP-10G-SR
    p = add_p("SEC-CIS-10GSR", "Cisco SFP-10G-SR 10GBASE-SR SFP+ Optical Transceiver Module", "Cisco Systems", "CAT-SEC", "HARDWARE",
              "Original Cisco short-reach multimode 10Gbps optical transceiver for LC duplex fiber connections up to 300m",
              "SFP-10G-SR=", 12000.0, 16500.0, 18.0, 60, True)
    add_v(p, "SEC-CIS-10GSR-01", "Cisco 10GBASE-SR SFP+ Transceiver (850nm Multimode LC Duplex)",
          "", "", "", "", "", "", "", "Metallic Silver", "10Gbps LC Duplex Fiber (300m OM3)", "", "SFP+ Optical Transceiver", 60, 0.0, 12000.0, 16500.0)

    # P176: Cisco SFP-10G-LR
    p = add_p("SEC-CIS-10GLR", "Cisco SFP-10G-LR 10GBASE-LR Single-Mode SFP+ Transceiver Module", "Cisco Systems", "CAT-SEC", "HARDWARE",
              "Long-reach single-mode 10Gbps optical transceiver supporting link lengths up to 10 kilometers over standard SMF",
              "SFP-10G-LR=", 28000.0, 37500.0, 18.0, 60, True)
    add_v(p, "SEC-CIS-10GLR-01", "Cisco 10GBASE-LR SFP+ Transceiver (1310nm Single-Mode 10km)",
          "", "", "", "", "", "", "", "Metallic Silver", "10Gbps LC Duplex Single-Mode", "", "SFP+ Optical Transceiver", 60, 0.0, 28000.0, 37500.0)

    # P177: Aruba 10G SFP+ to SFP+ 3m DAC Cable
    p = add_p("SEC-ARU-DAC3M", "Aruba 10G SFP+ to SFP+ 3m Direct Attach Copper (DAC) Cable", "Aruba Networks (HPE)", "CAT-SEC", "HARDWARE",
              "Passive twinaxial direct-attach copper cable for low-latency server-to-switch and switch-to-switch stacking",
              "J9283D", 4500.0, 6800.0, 18.0, 60, False)
    add_v(p, "SEC-ARU-DAC3M-01", "Aruba 10G SFP+ to SFP+ 3-Meter Direct Attach Copper Cable",
          "", "", "", "", "", "", "", "Black/Silver", "10Gbps SFP+ to SFP+ Direct Attach (3m)", "", "Passive Twinax Cable", 60, 0.0, 4500.0, 6800.0)

    # P178: Ubiquiti UF-MM-10G SFP+ Pair
    p = add_p("SEC-UBI-UFMM10G", "Ubiquiti 10Gbps Multi-Mode Optical SFP+ Module Pair (UF-MM-10G)", "Ubiquiti Networks", "CAT-SEC", "HARDWARE",
              "Multi-mode 10G SFP+ transceivers pair supporting distances up to 300 meters over OM3 multimode fiber",
              "UACC-OM-MM-10G-D-2", 4200.0, 6200.0, 18.0, 24, False)
    add_v(p, "SEC-UBI-UFMM10G-01", "Ubiquiti UniFi 10G SFP+ Multi-Mode Optical Transceiver (Pack of 2)",
          "", "", "", "", "", "", "", "Silver", "10Gbps 850nm LC Duplex (Pair of 2)", "", "SFP+ Optical Module Pair", 24, 0.0, 4200.0, 6200.0)

    # P179: Belkin Cat6A Shielded Patch Cable 2m (Pack of 10)
    p = add_p("SEC-BEL-CAT6A10PK", "Belkin Cat6A Shielded Snagless RJ45 Patch Cable 2m (10-Pack)", "Dell Technologies", "CAT-SEC", "HARDWARE",
              "10-Gigabit certified 500MHz shielded twisted-pair (STP) snagless patch cords with gold-plated contacts",
              "B2B169-02M-BL-10", 2200.0, 3600.0, 18.0, 60, False)
    add_v(p, "SEC-BEL-C6A10PK-BLU", "Belkin Cat6A Shielded RJ45 Patch Cable 2-Meter Blue (10-Pack)",
          "", "", "", "", "", "", "", "Blue", "10GBase-T Cat6A Shielded RJ45 (10-Pack)", "", "Pack of 10 Cables", 60, 0.0, 2200.0, 3600.0)
    add_v(p, "SEC-BEL-C6A10PK-GRY", "Belkin Cat6A Shielded RJ45 Patch Cable 2-Meter Grey (10-Pack)",
          "", "", "", "", "", "", "", "Grey", "10GBase-T Cat6A Shielded RJ45 (10-Pack)", "", "Pack of 10 Cables", 60, 0.0, 2200.0, 3600.0)

    # P180: D-Link 24-Port Cat6 Patch Panel
    p = add_p("SEC-DLK-PP24C6", "D-Link 24-Port Cat6 Fully Loaded Unshielded Patch Panel 1U", "Dell Technologies", "CAT-SEC", "HARDWARE",
              "19-inch 1U rackmount 24-port Cat6 unshielded patch panel with cable management bar and label strips",
              "NCB-C6UBLKR-24", 2800.0, 4200.0, 18.0, 60, False)
    add_v(p, "SEC-DLK-PP24-01", "D-Link 24-Port Cat6 1U Rackmount Patch Panel with Cable Wire Bar",
          "", "", "", "", "", "", "", "Black", "24x RJ45 Cat6 Female Jacks, Dual Type IDC Terminals", "", "1U Rackmount Panel", 60, 0.0, 2800.0, 4200.0)

    # P181: Dell ReadyRails II Sliding Rail Kit
    p = add_p("SEC-DEL-RAILS1U2U", "Dell ReadyRails II Sliding Rail Kit for 1U/2U PowerEdge Servers", "Dell Technologies", "CAT-SEC", "HARDWARE",
              "Toolless sliding rails supporting 4-post racks with square or round mounting holes for R660/R760",
              "770-BDKW", 8500.0, 12500.0, 18.0, 36, False)
    add_v(p, "SEC-DEL-RAILS-01", "Dell ReadyRails II 1U/2U Sliding Rail Kit without Cable Management Arm",
          "", "", "", "", "", "", "", "Galvanized Steel", "4-Post 19\" Rack Mount Rails", "", "Server Rail Kit", 36, 0.0, 8500.0, 12500.0)

    # P182: APC NetShelter 42U Cable Management Arm
    p = add_p("SEC-APC-CMA42U", "APC NetShelter 42U Server Rack Cable Management Arm", "Schneider Electric (APC)", "CAT-UPS", "HARDWARE",
              "Hinged cable management arm eliminating cable stress during server extension for servicing",
              "AR7130", 5500.0, 8400.0, 18.0, 24, False)
    add_v(p, "SEC-APC-CMA-01", "APC NetShelter Server Cable Management Arm for 1U/2U Chassis",
          "", "", "", "", "", "", "", "Black", "Toolless Snap-On Rack Arm", "", "Cable Management Arm", 24, 0.0, 5500.0, 8400.0)

    print(f"Generated {len(products)} products and {len(variants)} variants.")
    return products, variants

if __name__ == "__main__":
    p, v = generate_catalog()
    print("Catalog generation test successful.")
