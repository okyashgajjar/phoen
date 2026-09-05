"""
DealFlow360 Catalog Generator — Mumbai Edition
Generates 361 Enterprise IT Hardware Products and 520+ Base Variants across 14 leaf categories.
Tailored for Mumbai's BFSI, trading, corporate mobility, infrastructure, storage, and security markets.
"""

import sys
import os

def generate_catalog():
    products = []
    variants = []

    p_idx = 1
    v_idx = 1

    def add_p(code, name, brand, subcat, desc, mpn, cost, price, tax=18.0, warranty=36, serialized=True, recurring=False):
        nonlocal p_idx
        pid = f"PROD-{p_idx:04d}"
        p_idx += 1
        # Map subcategory to parent category
        if subcat in ["CAT-LAP", "CAT-DSK", "CAT-WKS", "CAT-SRV"]:
            cat_id = "CAT-COMP"
        elif subcat in ["CAT-STO", "CAT-NET", "CAT-SEC"]:
            cat_id = "CAT-INFRA"
        elif subcat in ["CAT-MON", "CAT-SMP", "CAT-TAB", "CAT-ACC"]:
            cat_id = "CAT-WORK"
        else:
            cat_id = "CAT-PWR"

        p_row = [
            pid, code, name, brand, cat_id, subcat, "PHYSICAL", desc, mpn, "UNIT",
            f"{cost:.2f}", f"{price:.2f}", f"{tax:.1f}", warranty, "ACTIVE", serialized, recurring,
            "2026-01-15T09:00:00Z", "2026-02-28T18:00:00Z"
        ]
        products.append(p_row)
        return pid

    def add_v(pid, sku, vname, cpu, ram, storage, stype, gpu, screen, res, color, conn, os_name, form, warranty, extra, cost, price):
        nonlocal v_idx
        vid = f"VAR-{v_idx:04d}"
        barcode = f"8907300{v_idx:06d}"
        v_idx += 1
        v_row = [
            vid, pid, sku, vname, cpu, ram, storage, stype, gpu, screen, res, color, conn,
            os_name, form, warranty, f"{extra:.2f}", f"{cost:.2f}", f"{price:.2f}", barcode, "ACTIVE"
        ]
        variants.append(v_row)
        return vid

    # --------------------------------------------------------------------------
    # 1. COMMERCIAL & EXECUTIVE LAPTOPS (CAT-LAP) - 55 Products
    # --------------------------------------------------------------------------
    laptops_data = [
        # Dell Latitude Series
        ("LAP-DEL-5440", "Dell Latitude 5440 14-inch Business Laptop", "Dell Technologies", "Intel Core i5-1335U, 14.0 FHD, Carbon Neutral Chassis", "LAT5440-BASE", 68000.0, 82000.0,
         [("LAP-DEL-5440-I5-16-512", "Core i5-1335U / 16GB / 512GB SSD / Win 11 Pro", "Intel Core i5-1335U", "16GB DDR4", "512GB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1080 FHD", "Titan Grey", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell", 36, 0.0, 68000.0, 82000.0),
          ("LAP-DEL-5440-I7-32-1TB", "Core i7-1365U / 32GB / 1TB SSD / Win 11 Pro", "Intel Core i7-1365U", "32GB DDR4", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1080 FHD", "Titan Grey", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell", 36, 18000.0, 83000.0, 100000.0)]),
        ("LAP-DEL-5540", "Dell Latitude 5540 15.6-inch Numeric Business Laptop", "Dell Technologies", "Intel Core i7-1355U, 15.6 FHD, Dedicated Numeric Keypad", "LAT5540-BASE", 74000.0, 89000.0,
         [("LAP-DEL-5540-I7-16-512", "Core i7-1355U / 16GB / 512GB SSD / Win 11 Pro", "Intel Core i7-1355U", "16GB DDR5", "512GB", "NVMe PCIe 4.0", "Intel Iris Xe", "15.6\"", "1920x1080 FHD", "Titan Grey", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell", 36, 0.0, 74000.0, 89000.0)]),
        ("LAP-DEL-7440", "Dell Latitude 7440 Ultralight Magnesium Laptop", "Dell Technologies", "Intel Core i7-1365U vPro, 14.0 QHD+ 16:10, 1.05kg Featherweight", "LAT7440-BASE", 98000.0, 118000.0,
         [("LAP-DEL-7440-I7-16-512", "Core i7-1365U / 16GB / 512GB SSD / Win 11 Pro", "Intel Core i7-1365U vPro", "16GB LPDDR5", "512GB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 QHD+", "River Magnesium", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Ultrabook", 36, 0.0, 98000.0, 118000.0),
          ("LAP-DEL-7440-I7-32-1TB", "Core i7-1365U / 32GB / 1TB SSD / Win 11 Pro", "Intel Core i7-1365U vPro", "32GB LPDDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 QHD+", "River Magnesium", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Ultrabook", 36, 22000.0, 116000.0, 140000.0)]),
        ("LAP-DEL-7450", "Dell Latitude 7450 AI-Ready Core Ultra Laptop", "Dell Technologies", "Intel Core Ultra 7 165U with NPU, 14.0 FHD+, On-Device AI", "LAT7450-BASE", 115000.0, 138000.0,
         [("LAP-DEL-7450-U7-16-512", "Core Ultra 7 / 16GB / 512GB SSD / Win 11 Pro", "Intel Core Ultra 7 165U", "16GB LPDDR5x", "512GB", "NVMe Gen4", "Intel Graphics", "14.0\"", "1920x1200 FHD+", "Titan Grey", "Wi-Fi 7 + BT 5.4", "Windows 11 Pro", "Ultrabook", 36, 0.0, 115000.0, 138000.0),
          ("LAP-DEL-7450-U7-32-1TB", "Core Ultra 7 / 32GB / 1TB SSD / Win 11 Pro", "Intel Core Ultra 7 165U", "32GB LPDDR5x", "1TB", "NVMe Gen4", "Intel Graphics", "14.0\"", "1920x1200 FHD+", "Titan Grey", "Wi-Fi 7 + BT 5.4", "Windows 11 Pro", "Ultrabook", 36, 25000.0, 136000.0, 163000.0)]),
        ("LAP-DEL-9440", "Dell Latitude 9440 2-in-1 Executive CNC Aluminum", "Dell Technologies", "Intel Core i7-1370P vPro, Zero-Lattice Keyboard, Haptic Touchpad", "LAT9440-BASE", 155000.0, 185000.0,
         [("LAP-DEL-9440-I7-32-1TB", "Core i7-1370P / 32GB / 1TB SSD / QHD+ Touch", "Intel Core i7-1370P vPro", "32GB LPDDR5x", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "2560x1600 QHD+ Touch", "Graphite CNC", "Wi-Fi 6E + 5G LTE", "Windows 11 Pro", "Convertible", 36, 0.0, 155000.0, 185000.0)]),
        ("LAP-DEL-XPS14", "Dell XPS 14 9440 High-Performance Executive", "Dell Technologies", "Intel Core Ultra 7 155H, RTX 4050 6GB, 3.2K OLED InfinityEdge", "XPS14-9440", 175000.0, 210000.0,
         [("LAP-DEL-XPS14-U7-32-1TB", "Core Ultra 7 / 32GB / 1TB / RTX 4050 / 3.2K OLED", "Intel Core Ultra 7 155H", "32GB LPDDR5x", "1TB", "NVMe Gen4", "NVIDIA RTX 4050 6GB", "14.5\"", "3200x2000 3.2K OLED", "Platinum Silver", "Wi-Fi 7 + BT 5.4", "Windows 11 Pro", "Ultrabook", 36, 0.0, 175000.0, 210000.0)]),
        ("LAP-DEL-XPS16", "Dell XPS 16 9640 Power Executive Flagship", "Dell Technologies", "Intel Core Ultra 9 185H, RTX 4070 8GB, 4K+ OLED Touch", "XPS16-9640", 225000.0, 270000.0,
         [("LAP-DEL-XPS16-U9-64-2TB", "Core Ultra 9 / 64GB / 2TB / RTX 4070 / 4K+ OLED", "Intel Core Ultra 9 185H", "64GB LPDDR5x", "2TB", "NVMe Gen4", "NVIDIA RTX 4070 8GB", "16.3\"", "3840x2400 4K+ OLED", "Graphite", "Wi-Fi 7 + BT 5.4", "Windows 11 Pro", "Workstation", 36, 0.0, 225000.0, 270000.0)]),

        # Lenovo ThinkPad Series
        ("LAP-LEN-T14G4", "Lenovo ThinkPad T14 Gen 4 Enterprise Workhorse", "Lenovo Enterprise", "Intel Core i5-1335U, 14.0 WUXGA 16:10, Spill-Resistant Keyboard", "21HD001EIG", 72000.0, 86000.0,
         [("LAP-LEN-T14G4-I5-16-512", "Core i5-1335U / 16GB / 512GB SSD / Win 11 Pro", "Intel Core i5-1335U", "16GB DDR5", "512GB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA", "Thunder Black", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell", 36, 0.0, 72000.0, 86000.0),
          ("LAP-LEN-T14G4-I7-32-1TB", "Core i7-1355U / 32GB / 1TB SSD / Win 11 Pro", "Intel Core i7-1355U", "32GB DDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA", "Thunder Black", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell", 36, 20000.0, 88000.0, 106000.0)]),
        ("LAP-LEN-T14S", "Lenovo ThinkPad T14s Gen 4 Ultralight Enterprise", "Lenovo Enterprise", "Intel Core i7-1365U vPro, 1.25kg Carbon Fiber Top, 57Wh Battery", "21F6003RIG", 92000.0, 110000.0,
         [("LAP-LEN-T14S-I7-16-512", "Core i7-1365U / 16GB / 512GB SSD / Win 11 Pro", "Intel Core i7-1365U vPro", "16GB LPDDR5x", "512GB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 Low Power", "Deep Black", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Ultrabook", 36, 0.0, 92000.0, 110000.0),
          ("LAP-LEN-T14S-I7-32-1TB", "Core i7-1365U / 32GB / 1TB SSD / Win 11 Pro", "Intel Core i7-1365U vPro", "32GB LPDDR5x", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 Low Power", "Deep Black", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Ultrabook", 36, 21000.0, 110000.0, 131000.0)]),
        ("LAP-LEN-X1C11", "Lenovo ThinkPad X1 Carbon Gen 11 Flagship", "Lenovo Enterprise", "Intel Core i7-1365U vPro, 2.8K OLED, Sub-1kg Carbon Weave", "21HM004RIG", 145000.0, 175000.0,
         [("LAP-LEN-X1C11-I7-32-1TB", "Core i7-1365U / 32GB / 1TB SSD / 2.8K OLED", "Intel Core i7-1365U vPro", "32GB LPDDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "2880x1800 2.8K OLED", "Carbon Fiber Weave", "Wi-Fi 6E + 4G LTE", "Windows 11 Pro", "Ultrabook", 36, 0.0, 145000.0, 175000.0)]),
        ("LAP-LEN-X1C12", "Lenovo ThinkPad X1 Carbon Gen 12 Core Ultra", "Lenovo Enterprise", "Intel Core Ultra 7 165H with NPU, Communications Bar, 120Hz OLED", "21KC0027IG", 168000.0, 202000.0,
         [("LAP-LEN-X1C12-U7-32-1TB", "Core Ultra 7 / 32GB / 1TB SSD / 120Hz OLED", "Intel Core Ultra 7 165H", "32GB LPDDR5x", "1TB", "NVMe Gen4", "Intel Arc Graphics", "14.0\"", "2880x1800 120Hz OLED", "Black Eclipse", "Wi-Fi 7 + BT 5.4", "Windows 11 Pro", "Ultrabook", 36, 0.0, 168000.0, 202000.0)]),
        ("LAP-LEN-X1Y8", "Lenovo ThinkPad X1 Yoga Gen 8 2-in-1 Executive", "Lenovo Enterprise", "Intel Core i7-1370P vPro, 360-degree Hinge, Integrated Garaged Pen", "21HQ0031IG", 152000.0, 182000.0,
         [("LAP-LEN-X1Y8-I7-32-1TB", "Core i7-1370P / 32GB / 1TB SSD / 4K OLED Pen", "Intel Core i7-1370P vPro", "32GB LPDDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "3840x2400 4K OLED Touch", "Storm Grey CNC", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Convertible", 36, 0.0, 152000.0, 182000.0)]),
        ("LAP-LEN-P14S", "Lenovo ThinkPad P14s Gen 4 Mobile Workstation", "Lenovo Enterprise", "AMD Ryzen 7 Pro 7840U, 14.0 OLED, ISV Certified Financial CAD", "21K5001UIG", 105000.0, 126000.0,
         [("LAP-LEN-P14S-R7-32-1TB", "Ryzen 7 Pro / 32GB / 1TB / Radeon 780M / OLED", "AMD Ryzen 7 Pro 7840U", "32GB LPDDR5x", "1TB", "NVMe PCIe 4.0", "AMD Radeon 780M", "14.0\"", "2880x1800 2.8K OLED", "Thunder Black", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Mobile Workstation", 36, 0.0, 105000.0, 126000.0)]),
        ("LAP-LEN-P1G6", "Lenovo ThinkPad P1 Gen 6 Powerhouse Workstation", "Lenovo Enterprise", "Intel Core i9-13900H, RTX 4080 12GB, 16.0 165Hz WQXGA Liquid Metal", "21FV002FIG", 240000.0, 288000.0,
         [("LAP-LEN-P1G6-I9-64-2TB", "Core i9-13900H / 64GB / 2TB / RTX 4080 / WQXGA", "Intel Core i9-13900H", "64GB DDR5 5600", "2TB", "NVMe Gen4 Performance", "NVIDIA RTX 4080 12GB", "16.0\"", "2560x1600 165Hz", "Carbon Fiber Weave", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Workstation", 36, 0.0, 240000.0, 288000.0)]),

        # HP EliteBook Series
        ("LAP-HP-EB840G10", "HP EliteBook 840 G10 Enterprise Laptop", "HP Inc.", "Intel Core i5-1335U, 14.0 WUXGA, HP Sure Start Gen7 Hardware Security", "8A4X6PA", 71000.0, 85000.0,
         [("LAP-HP-EB840G10-I5-16-512", "Core i5-1335U / 16GB / 512GB SSD / Win 11 Pro", "Intel Core i5-1335U", "16GB DDR5", "512GB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 WUXGA", "Natural Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Clamshell", 36, 0.0, 71000.0, 85000.0)]),
        ("LAP-HP-EB840G11", "HP EliteBook 840 G11 AI Core Ultra Laptop", "HP Inc.", "Intel Core Ultra 7 155H, 14.0 2.5K 120Hz, Poly Studio 5MP AI Camera", "9E8Y2PA", 118000.0, 142000.0,
         [("LAP-HP-EB840G11-U7-32-1TB", "Core Ultra 7 / 32GB / 1TB SSD / 2.5K 120Hz", "Intel Core Ultra 7 155H", "32GB LPDDR5x", "1TB", "NVMe Gen4", "Intel Arc Graphics", "14.0\"", "2560x1600 2.5K 120Hz", "Pike Silver", "Wi-Fi 7 + BT 5.4", "Windows 11 Pro", "Ultrabook", 36, 0.0, 118000.0, 142000.0)]),
        ("LAP-HP-EB1040G10", "HP EliteBook 1040 G10 Executive Magnesium", "HP Inc.", "Intel Core i7-1365U vPro, 14.0 WUXGA Sure View Privacy, 1.18kg", "7N0C4PA", 125000.0, 150000.0,
         [("LAP-HP-EB1040G10-I7-32-1TB", "Core i7-1365U / 32GB / 1TB SSD / SureView", "Intel Core i7-1365U vPro", "32GB LPDDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "1920x1200 Privacy Screen", "Pike Silver", "Wi-Fi 6E + 4G LTE", "Windows 11 Pro", "Ultrabook", 36, 0.0, 125000.0, 150000.0)]),
        ("LAP-HP-DFLYG4", "HP Dragonfly G4 Executive Ultra-Premium", "HP Inc.", "Intel Core i7-1365U vPro, 13.5 3:2 OLED 1000-nit, 0.99kg Weight", "8B1F8PA", 160000.0, 192000.0,
         [("LAP-HP-DFLYG4-I7-32-1TB", "Core i7-1365U / 32GB / 1TB SSD / 3:2 OLED", "Intel Core i7-1365U vPro", "32GB LPDDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "13.5\"", "3000x2000 3:2 OLED", "Slate Blue Magnesium", "Wi-Fi 6E + 5G LTE", "Windows 11 Pro", "Ultrabook", 36, 0.0, 160000.0, 192000.0)]),
        ("LAP-HP-ZBOOK16G10", "HP ZBook Power G10 Mobile Studio Workstation", "HP Inc.", "Intel Core i7-13800H vPro, RTX 2000 Ada 8GB, ISV Financial Modeling", "8D8W9PA", 165000.0, 198000.0,
         [("LAP-HP-ZBOOK16G10-I7-32-1TB", "Core i7-13800H / 32GB / 1TB / RTX 2000 Ada", "Intel Core i7-13800H vPro", "32GB DDR5 5200", "1TB", "NVMe Gen4", "NVIDIA RTX 2000 Ada 8GB", "16.0\"", "2560x1600 QHD+", "Dark Ash Silver", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Workstation", 36, 0.0, 165000.0, 198000.0)]),

        # Apple MacBooks
        ("LAP-APL-MBA13-M3", "Apple MacBook Air 13-inch M3 Chip", "Apple Inc.", "Apple M3 8-Core CPU, 10-Core GPU, 13.6 Liquid Retina, Fanless Silence", "MRXV3HN/A", 105000.0, 124900.0,
         [("LAP-APL-MBA13-M3-16-512-MID", "M3 / 16GB Unified / 512GB SSD / Midnight", "Apple M3 (8C CPU / 10C GPU)", "16GB Unified", "512GB", "Apple Unified NVMe", "Apple 10-Core GPU", "13.6\"", "2560x1664 Retina", "Midnight", "Wi-Fi 6E + MagSafe 3", "macOS Sonoma", "Ultrabook", 36, 0.0, 105000.0, 124900.0),
          ("LAP-APL-MBA13-M3-24-512-SLV", "M3 / 24GB Unified / 512GB SSD / Silver", "Apple M3 (8C CPU / 10C GPU)", "24GB Unified", "512GB", "Apple Unified NVMe", "Apple 10-Core GPU", "13.6\"", "2560x1664 Retina", "Silver", "Wi-Fi 6E + MagSafe 3", "macOS Sonoma", "Ultrabook", 36, 18000.0, 120000.0, 142900.0)]),
        ("LAP-APL-MBA15-M3", "Apple MacBook Air 15-inch M3 Large Display", "Apple Inc.", "Apple M3 8-Core CPU, 10-Core GPU, 15.3 Liquid Retina, Six-Speaker Sound", "MXD13HN/A", 125000.0, 144900.0,
         [("LAP-APL-MBA15-M3-16-512-SGR", "M3 / 16GB Unified / 512GB SSD / Space Grey", "Apple M3 (8C CPU / 10C GPU)", "16GB Unified", "512GB", "Apple Unified NVMe", "Apple 10-Core GPU", "15.3\"", "2880x1864 Retina", "Space Grey", "Wi-Fi 6E + MagSafe 3", "macOS Sonoma", "Ultrabook", 36, 0.0, 125000.0, 144900.0)]),
        ("LAP-APL-MBP14-M3P", "Apple MacBook Pro 14-inch M3 Pro Developer Flagship", "Apple Inc.", "Apple M3 Pro 11-Core CPU, 14-Core GPU, Liquid Retina XDR 120Hz", "MRX33HN/A", 168000.0, 199900.0,
         [("LAP-APL-MBP14-M3P-18-512-SBLK", "M3 Pro / 18GB Unified / 512GB SSD / Space Black", "Apple M3 Pro (11C CPU / 14C GPU)", "18GB Unified", "512GB", "Apple Unified NVMe", "Apple 14-Core GPU", "14.2\"", "3024x1964 XDR 120Hz", "Space Black", "Wi-Fi 6E + HDMI + SDXC", "macOS Sonoma", "Ultrabook", 36, 0.0, 168000.0, 199900.0),
          ("LAP-APL-MBP14-M3P-36-1TB-SBLK", "M3 Pro / 36GB Unified / 1TB SSD / Space Black", "Apple M3 Pro (12C CPU / 18C GPU)", "36GB Unified", "1TB", "Apple Unified NVMe", "Apple 18-Core GPU", "14.2\"", "3024x1964 XDR 120Hz", "Space Black", "Wi-Fi 6E + HDMI + SDXC", "macOS Sonoma", "Ultrabook", 36, 35000.0, 198000.0, 234900.0)]),
        ("LAP-APL-MBP16-M3M", "Apple MacBook Pro 16-inch M3 Max Quantitative Model", "Apple Inc.", "Apple M3 Max 14-Core CPU, 30-Core GPU, Liquid Retina XDR, Up to 128GB", "MUW63HN/A", 295000.0, 349900.0,
         [("LAP-APL-MBP16-M3M-36-1TB-SBLK", "M3 Max / 36GB Unified / 1TB SSD / Space Black", "Apple M3 Max (14C CPU / 30C GPU)", "36GB Unified", "1TB", "Apple Unified NVMe", "Apple 30-Core GPU", "16.2\"", "3456x2234 XDR 120Hz", "Space Black", "Wi-Fi 6E + HDMI + SDXC", "macOS Sonoma", "Mobile Workstation", 36, 0.0, 295000.0, 349900.0),
          ("LAP-APL-MBP16-M3M-64-2TB-SBLK", "M3 Max / 64GB Unified / 2TB SSD / Space Black", "Apple M3 Max (16C CPU / 40C GPU)", "64GB Unified", "2TB", "Apple Unified NVMe", "Apple 40-Core GPU", "16.2\"", "3456x2234 XDR 120Hz", "Space Black", "Wi-Fi 6E + HDMI + SDXC", "macOS Sonoma", "Mobile Workstation", 36, 65000.0, 350000.0, 414900.0)]),

        # ASUS & Acer Commercial Laptops
        ("LAP-ASUS-B9403", "ASUS ExpertBook B9 OLED Executive Ultralight", "ASUS Commercial", "Intel Core i7-1355U vPro, 14.0 2.8K OLED, 990g Ultralight Magnesium", "B9403CVA-KM0145X", 132000.0, 158000.0,
         [("LAP-ASUS-B9403-I7-32-1TB", "Core i7-1355U / 32GB / 1TB SSD / 2.8K OLED", "Intel Core i7-1355U vPro", "32GB LPDDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "2880x1800 2.8K OLED", "Star Black", "Wi-Fi 6E + BT 5.3", "Windows 11 Pro", "Ultrabook", 36, 0.0, 132000.0, 158000.0)]),
        ("LAP-ACER-TMP6", "Acer TravelMate P6 14 Business Executive", "Acer Enterprise", "Intel Core i7-1355U, 14.0 OLED 16:10, 1kg Durable Chassis, MIL-STD 810H", "TMP614-53-74TL", 95000.0, 114000.0,
         [("LAP-ACER-TMP6-I7-16-1TB", "Core i7-1355U / 16GB / 1TB SSD / OLED / Win 11 Pro", "Intel Core i7-1355U", "16GB LPDDR5", "1TB", "NVMe PCIe 4.0", "Intel Iris Xe", "14.0\"", "2880x1800 OLED", "Iron Black", "Wi-Fi 6E + 5G", "Windows 11 Pro", "Ultrabook", 36, 0.0, 95000.0, 114000.0)])
    ]

    # Generate 55 laptops total (replicate across corporate generations and AMD/Intel configs)
    for row in laptops_data:
        pid = add_p(row[0], row[1], row[2], "CAT-LAP", row[3], row[4], row[5], row[6])
        for v in row[7]:
            add_v(pid, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15], v[16])

    # Extend to 55 models with realistic corporate sub-configurations
    ext_lap_specs = [
        ("LAP-DEL-5340", "Dell Latitude 5340 13.3-inch Ultra-Portable", "Dell Technologies", 65000.0, 78000.0),
        ("LAP-DEL-5450", "Dell Latitude 5450 Core Ultra 5 Mainstream", "Dell Technologies", 76000.0, 91000.0),
        ("LAP-DEL-7340", "Dell Latitude 7340 13.3-inch Executive Lightweight", "Dell Technologies", 94000.0, 113000.0),
        ("LAP-DEL-7650", "Dell Latitude 7650 16-inch Executive Spreadsheets", "Dell Technologies", 108000.0, 130000.0),
        ("LAP-LEN-E14G5", "Lenovo ThinkPad E14 Gen 5 SMB Corporate", "Lenovo Enterprise", 52000.0, 62000.0),
        ("LAP-LEN-E16G1", "Lenovo ThinkPad E16 Gen 1 Finance Desktop Alternative", "Lenovo Enterprise", 56000.0, 67000.0),
        ("LAP-LEN-L14G4", "Lenovo ThinkPad L14 Gen 4 Enterprise Deployment", "Lenovo Enterprise", 62000.0, 74000.0),
        ("LAP-LEN-T16G2", "Lenovo ThinkPad T16 Gen 2 16.0 Large Screen", "Lenovo Enterprise", 82000.0, 98000.0),
        ("LAP-LEN-P16SG2", "Lenovo ThinkPad P16s Gen 2 Mobile CAD Workstation", "Lenovo Enterprise", 112000.0, 134000.0),
        ("LAP-LEN-Z13G2", "Lenovo ThinkPad Z13 Gen 2 Sustainable Bronze", "Lenovo Enterprise", 125000.0, 150000.0),
        ("LAP-HP-EB860G10", "HP EliteBook 860 G10 16.0 Corporate Numeric", "HP Inc.", 78000.0, 94000.0),
        ("LAP-HP-PB440G10", "HP ProBook 440 G10 Commercial Fleet Notebook", "HP Inc.", 54000.0, 65000.0),
        ("LAP-HP-PB450G10", "HP ProBook 450 G10 15.6 Mainstream Business", "HP Inc.", 58000.0, 70000.0),
        ("LAP-HP-ZBSTUDIO", "HP ZBook Studio G10 Thin Creative Workstation", "HP Inc.", 195000.0, 235000.0),
        ("LAP-HP-ZBFURY", "HP ZBook Fury 16 G10 Desktop Replacement", "HP Inc.", 260000.0, 312000.0),
        ("LAP-APL-MBP14-M3B", "Apple MacBook Pro 14-inch Base M3 Chip", "Apple Inc.", 142000.0, 169900.0),
        ("LAP-ASUS-B5402", "ASUS ExpertBook B5 Flip 14-inch Convertible", "ASUS Commercial", 88000.0, 105000.0),
        ("LAP-ASUS-B7402", "ASUS ExpertBook B7 5G Enterprise Mobility", "ASUS Commercial", 115000.0, 138000.0),
        ("LAP-ACER-TMP4", "Acer TravelMate P4 14 Commercial Fleet", "Acer Enterprise", 58000.0, 69000.0),
        ("LAP-MS-SL6-13", "Microsoft Surface Laptop 6 13.5 Core Ultra 5", "Microsoft Surface", 108000.0, 129999.0),
        ("LAP-MS-SL6-15", "Microsoft Surface Laptop 6 15.0 Core Ultra 7", "Microsoft Surface", 135000.0, 162999.0),
        ("LAP-MS-SLS2", "Microsoft Surface Laptop Studio 2 Dynamic Woven Hinge", "Microsoft Surface", 185000.0, 222999.0),
        ("LAP-DEL-LAT3440", "Dell Latitude 3440 Entry Commercial Laptop", "Dell Technologies", 48000.0, 58000.0),
        ("LAP-DEL-LAT3540", "Dell Latitude 3540 15.6 Entry Commercial", "Dell Technologies", 51000.0, 61000.0),
        ("LAP-LEN-V15G4", "Lenovo V15 Gen 4 Cost-Effective Commercial", "Lenovo Enterprise", 38000.0, 46000.0),
        ("LAP-HP-240G9", "HP 240 G9 Essential Business Notebook", "HP Inc.", 39000.0, 47000.0),
        ("LAP-DEL-PR3580", "Dell Precision 3580 Affordable Mobile CAD Workstation", "Dell Technologies", 98000.0, 118000.0),
        ("LAP-DEL-PR5680", "Dell Precision 5680 16-inch Creator Workstation", "Dell Technologies", 210000.0, 252000.0),
        ("LAP-LEN-T14G4-AMD", "Lenovo ThinkPad T14 Gen 4 AMD Ryzen 5 Pro", "Lenovo Enterprise", 69000.0, 83000.0),
        ("LAP-HP-EB845G10", "HP EliteBook 845 G10 AMD Ryzen 7 Pro 7840U", "HP Inc.", 82000.0, 98000.0)
    ]

    for code, name, brd, cost, price in ext_lap_specs:
        pid = add_p(code, name, brd, "CAT-LAP", f"{name}, Enterprise fleet security and docking support", f"{code}-BASE", cost, price)
        add_v(pid, f"{code}-16-512", f"{name} / 16GB RAM / 512GB SSD / Win 11 Pro", "Intel/AMD Multi-Core", "16GB DDR5", "512GB", "NVMe Gen4", "Integrated", "14.0\"", "1920x1200 FHD+", "Matte Black/Silver", "Wi-Fi 6E + BT", "Windows 11 Pro", "Clamshell", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 2. ENTERPRISE DESKTOPS & MINI PCS (CAT-DSK) - 35 Products
    # --------------------------------------------------------------------------
    desktops_data = [
        ("DSK-DEL-7010M", "Dell OptiPlex 7010 Micro Form Factor", "Dell Technologies", 48000.0, 58000.0),
        ("DSK-DEL-7010S", "Dell OptiPlex 7010 Small Form Factor", "Dell Technologies", 52000.0, 62000.0),
        ("DSK-DEL-7010T", "Dell OptiPlex 7010 Mini Tower Desktop", "Dell Technologies", 56000.0, 67000.0),
        ("DSK-DEL-7410AIO", "Dell OptiPlex 7410 24-inch All-in-One", "Dell Technologies", 68000.0, 82000.0),
        ("DSK-DEL-7020M", "Dell OptiPlex Micro Plus 7020 Core i7 vPro", "Dell Technologies", 62000.0, 75000.0),
        ("DSK-LEN-M70Q", "Lenovo ThinkCentre M70q Gen 4 Tiny PC", "Lenovo Enterprise", 46000.0, 55000.0),
        ("DSK-LEN-M80Q", "Lenovo ThinkCentre M80q Gen 4 High Security", "Lenovo Enterprise", 54000.0, 65000.0),
        ("DSK-LEN-M90Q", "Lenovo ThinkCentre M90q Gen 4 Tiny Desktop", "Lenovo Enterprise", 65000.0, 78000.0),
        ("DSK-LEN-NEO50S", "Lenovo ThinkCentre Neo 50s Gen 4 SFF", "Lenovo Enterprise", 42000.0, 50000.0),
        ("DSK-LEN-M70A", "Lenovo ThinkCentre M70a Gen 3 21.5 AIO", "Lenovo Enterprise", 64000.0, 77000.0),
        ("DSK-HP-PD400G9", "HP ProDesk 400 G9 Mini Desktop PC", "HP Inc.", 45000.0, 54000.0),
        ("DSK-HP-ED800G9M", "HP EliteDesk 800 G9 Desktop Mini PC", "HP Inc.", 58000.0, 70000.0),
        ("DSK-HP-ED800G9S", "HP EliteDesk 800 G9 Small Form Factor", "HP Inc.", 62000.0, 75000.0),
        ("DSK-HP-ED800G9T", "HP EliteDesk 800 G9 Tower High Expandability", "HP Inc.", 66000.0, 79000.0),
        ("DSK-HP-EL800AIO", "HP EliteOne 800 G9 27-inch 4K All-in-One", "HP Inc.", 98000.0, 118000.0),
        ("DSK-APL-MM-M2", "Apple Mac mini M2 8-Core CPU 10-Core GPU", "Apple Inc.", 52000.0, 59900.0),
        ("DSK-APL-MM-M2P", "Apple Mac mini M2 Pro 10-Core CPU 16-Core GPU", "Apple Inc.", 108000.0, 129900.0),
        ("DSK-APL-MS-M2M", "Apple Mac Studio M2 Max 12-Core CPU 30-Core GPU", "Apple Inc.", 175000.0, 209900.0),
        ("DSK-APL-MS-M2U", "Apple Mac Studio M2 Ultra 24-Core CPU 60-Core GPU", "Apple Inc.", 345000.0, 414900.0),
        ("DSK-APL-IMAC-M3", "Apple iMac 24-inch M3 4.5K Retina All-in-One", "Apple Inc.", 115000.0, 134900.0),
        ("DSK-ASUS-D700", "ASUS ExpertCenter D7 SFF Compact Business", "ASUS Commercial", 44000.0, 53000.0),
        ("DSK-ASUS-D900", "ASUS ExpertCenter D9 Mini Tower Enterprise", "ASUS Commercial", 59000.0, 71000.0),
        ("DSK-ACER-VM469", "Acer Veriton M4690G Tower Corporate", "Acer Enterprise", 41000.0, 49000.0),
        ("DSK-ACER-VX269", "Acer Veriton X2690G Small Form Factor", "Acer Enterprise", 39000.0, 47000.0),
        ("DSK-DEL-3000TC", "Dell OptiPlex 3000 Thin Client Dual 4K", "Dell Technologies", 32000.0, 39000.0),
        ("DSK-HP-T640TC", "HP t640 Quad-Core Enterprise Thin Client", "HP Inc.", 34000.0, 41000.0),
        ("DSK-HP-T740TC", "HP t740 High-Performance Quad 4K Thin Client", "HP Inc.", 48000.0, 58000.0),
        ("DSK-LEN-M75Q", "Lenovo ThinkCentre M75q Gen 2 AMD Tiny", "Lenovo Enterprise", 47000.0, 56000.0),
        ("DSK-DEL-7010S-I7", "Dell OptiPlex 7010 SFF Intel Core i7 32GB", "Dell Technologies", 68000.0, 82000.0),
        ("DSK-HP-ED805G9", "HP EliteDesk 805 G9 AMD Ryzen Pro Mini", "HP Inc.", 57000.0, 68000.0),
        ("DSK-LEN-NEO30A", "Lenovo ThinkCentre Neo 30a 24-inch AIO", "Lenovo Enterprise", 52000.0, 62000.0),
        ("DSK-DEL-5400AIO", "Dell OptiPlex 5400 All-in-One 23.8 FHD", "Dell Technologies", 61000.0, 73000.0),
        ("DSK-HP-PRO400S", "HP Pro SFF 400 G9 Compact Desktop", "HP Inc.", 46000.0, 55000.0),
        ("DSK-LEN-M90A", "Lenovo ThinkCentre M90a Pro Gen 4 27 QHD AIO", "Lenovo Enterprise", 88000.0, 105000.0),
        ("DSK-ASUS-PB62", "ASUS Mini PC PB62 Rugged Enterprise Mini", "ASUS Commercial", 42000.0, 51000.0)
    ]

    for code, name, brd, cost, price in desktops_data:
        pid = add_p(code, name, brd, "CAT-DSK", f"{name}, Enterprise workplace productivity desktop", f"{code}-BASE", cost, price)
        add_v(pid, f"{code}-16-512", f"{name} / 16GB RAM / 512GB NVMe / Win 11 Pro", "Intel Core i5 / AMD", "16GB DDR4/5", "512GB", "NVMe PCIe", "Integrated Graphics", "N/A", "N/A", "Black", "Gigabit Ethernet + Wi-Fi", "Windows 11 Pro", "Micro / SFF", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 3. FINANCIAL & ENGINEERING WORKSTATIONS (CAT-WKS) - 30 Products
    # --------------------------------------------------------------------------
    workstations_data = [
        ("WKS-DEL-PR3660", "Dell Precision 3660 Tower Financial Workstation", "Dell Technologies", 98000.0, 118000.0),
        ("WKS-DEL-PR5820", "Dell Precision 5820 Intel Xeon W High-Frequency Trading", "Dell Technologies", 165000.0, 198000.0),
        ("WKS-DEL-PR7920", "Dell Precision 7920 Dual Xeon Scalable Compute Workstation", "Dell Technologies", 280000.0, 336000.0),
        ("WKS-DEL-PR3460", "Dell Precision 3460 Small Form Factor Trading Workstation", "Dell Technologies", 88000.0, 106000.0),
        ("WKS-DEL-PR7960", "Dell Precision 7960 Rackmount 2U Remote Workstation", "Dell Technologies", 340000.0, 408000.0),
        ("WKS-LEN-P3TINY", "Lenovo ThinkStation P3 Tiny Micro Trading Rig", "Lenovo Enterprise", 82000.0, 99000.0),
        ("WKS-LEN-P3TOWER", "Lenovo ThinkStation P3 Tower Quantitative Rig", "Lenovo Enterprise", 105000.0, 126000.0),
        ("WKS-LEN-P5", "Lenovo ThinkStation P5 Aston Martin Co-Designed Workstation", "Lenovo Enterprise", 195000.0, 234000.0),
        ("WKS-LEN-P7", "Lenovo ThinkStation P7 Single-Socket Intel Xeon W-3400", "Lenovo Enterprise", 290000.0, 348000.0),
        ("WKS-LEN-PX", "Lenovo ThinkStation PX Dual Xeon Platinum 120-Core Rig", "Lenovo Enterprise", 480000.0, 576000.0),
        ("WKS-HP-Z2MINI", "HP Z2 Mini G9 Micro Engineering Workstation", "HP Inc.", 86000.0, 103000.0),
        ("WKS-HP-Z2SFF", "HP Z2 SFF G9 Compact Multi-Display Trading Desk", "HP Inc.", 92000.0, 110000.0),
        ("WKS-HP-Z2TWR", "HP Z2 Tower G9 CAD & Computational Finance Rig", "HP Inc.", 110000.0, 132000.0),
        ("WKS-HP-Z4G5", "HP Z4 G5 Intel Xeon W Mainstream High-Compute", "HP Inc.", 185000.0, 222000.0),
        ("WKS-HP-Z6G5", "HP Z6 G5 A AMD Threadripper PRO 96-Core Compute", "HP Inc.", 320000.0, 384000.0),
        ("WKS-HP-Z8G5", "HP Z8 G5 Dual Xeon Scalable AI Deep Learning Rig", "HP Inc.", 460000.0, 552000.0),
        ("WKS-APL-MP-M2U", "Apple Mac Pro M2 Ultra Tower PCIe Expansion", "Apple Inc.", 590000.0, 729900.0),
        ("WKS-APL-MP-RCK", "Apple Mac Pro M2 Ultra 5U Rackmount Enclosure", "Apple Inc.", 640000.0, 779900.0),
        ("WKS-ASUS-E900", "ASUS ESC700 G4 High-Performance GPU Workstation", "ASUS Commercial", 210000.0, 252000.0),
        ("WKS-ASUS-PROART", "ASUS ProArt Station PD5 Professional Compute Rig", "ASUS Commercial", 145000.0, 174000.0),
        ("WKS-DEL-PR3260", "Dell Precision 3260 Compact Financial Algo Node", "Dell Technologies", 78000.0, 94000.0),
        ("WKS-HP-Z240S", "HP Z2 SFF Entry Trading Screen Station", "HP Inc.", 74000.0, 89000.0),
        ("WKS-LEN-P360T", "Lenovo ThinkStation P360 Tiny Quad Display Hub", "Lenovo Enterprise", 79000.0, 95000.0),
        ("WKS-DEL-PR5860", "Dell Precision 5860 Tower Intel Xeon W-2400", "Dell Technologies", 225000.0, 270000.0),
        ("WKS-HP-Z4T-ADV", "HP Z4 Tower Advanced ISV Certified Modeling", "HP Inc.", 198000.0, 238000.0),
        ("WKS-LEN-P3U-TRD", "Lenovo ThinkStation P3 Ultra Dual GPU Trading", "Lenovo Enterprise", 135000.0, 162000.0),
        ("WKS-DEL-PR3680", "Dell Precision 3680 Tower 14th Gen Intel Core i9", "Dell Technologies", 128000.0, 154000.0),
        ("WKS-HP-Z2G9-TRD", "HP Z2 Mini G9 Dedicated Dual LAN Trading Node", "HP Inc.", 96000.0, 115000.0),
        ("WKS-LEN-P620", "Lenovo ThinkStation P620 AMD Threadripper PRO 64C", "Lenovo Enterprise", 270000.0, 324000.0),
        ("WKS-ASUS-E500", "ASUS ExpertCenter E500 G9 Intel Xeon Tower", "ASUS Commercial", 115000.0, 138000.0)
    ]

    for code, name, brd, cost, price in workstations_data:
        pid = add_p(code, name, brd, "CAT-WKS", f"{name}, High-frequency financial modeling, multi-screen display and CAD compute", f"{code}-BASE", cost, price)
        add_v(pid, f"{code}-64-1TB", f"{name} / 64GB ECC RAM / 1TB NVMe / NVIDIA Quadro/RTX", "Intel Xeon W / Core i9", "64GB DDR5 ECC", "1TB", "PCIe 4.0 Enterprise NVMe", "NVIDIA RTX A2000 12GB", "N/A", "N/A", "Black Metallic", "Dual 10GbE LAN + PCIe Gen5", "Windows 11 Pro for Workstations", "Tower / SFF", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 4. ENTERPRISE RACK & BLADE SERVERS (CAT-SRV) - 32 Products
    # --------------------------------------------------------------------------
    servers_data = [
        ("SRV-DEL-R250", "Dell PowerEdge R250 1U Single-Socket Entry Server", "Dell Technologies", 110000.0, 132000.0),
        ("SRV-DEL-R350", "Dell PowerEdge R350 1U Redundant Power Server", "Dell Technologies", 145000.0, 174000.0),
        ("SRV-DEL-R450", "Dell PowerEdge R450 1U Dual-Socket Dense Compute", "Dell Technologies", 195000.0, 234000.0),
        ("SRV-DEL-R550", "Dell PowerEdge R550 2U Storage-Optimized Server", "Dell Technologies", 240000.0, 288000.0),
        ("SRV-DEL-R660", "Dell PowerEdge R660 1U Ultra-Dense Dual 4th/5th Gen Xeon", "Dell Technologies", 320000.0, 384000.0),
        ("SRV-DEL-R760", "Dell PowerEdge R760 2U Enterprise Workhorse Flagship", "Dell Technologies", 420000.0, 504000.0),
        ("SRV-DEL-R760XS", "Dell PowerEdge R760xs 2U Cloud Scale Optimized", "Dell Technologies", 360000.0, 432000.0),
        ("SRV-DEL-R860", "Dell PowerEdge R860 2U 4-Socket Dense Enterprise Core", "Dell Technologies", 720000.0, 864000.0),
        ("SRV-DEL-R960", "Dell PowerEdge R960 4U 4-Socket Mission-Critical DB", "Dell Technologies", 980000.0, 1176000.0),
        ("SRV-HPE-DL20", "HPE ProLiant DL20 Gen11 1U Short-Depth Edge Server", "Hewlett Packard Enterprise", 118000.0, 142000.0),
        ("SRV-HPE-DL320", "HPE ProLiant DL320 Gen11 1U Single-Socket Compute", "Hewlett Packard Enterprise", 180000.0, 216000.0),
        ("SRV-HPE-DL360", "HPE ProLiant DL360 Gen11 1U Dual Intel Xeon Scalable", "Hewlett Packard Enterprise", 330000.0, 396000.0),
        ("SRV-HPE-DL380", "HPE ProLiant DL380 Gen11 2U 2P World Best-Selling Server", "Hewlett Packard Enterprise", 435000.0, 522000.0),
        ("SRV-HPE-DL385", "HPE ProLiant DL385 Gen11 2U Dual AMD EPYC 9004", "Hewlett Packard Enterprise", 450000.0, 540000.0),
        ("SRV-HPE-ML350", "HPE ProLiant ML350 Gen11 4U Tower Enterprise Expandable", "Hewlett Packard Enterprise", 290000.0, 348000.0),
        ("SRV-HPE-DL560", "HPE ProLiant DL560 Gen11 2U 4-Socket High-Density", "Hewlett Packard Enterprise", 780000.0, 936000.0),
        ("SRV-LEN-SR250", "Lenovo ThinkSystem SR250 V2 1U Compact Rack Server", "Lenovo Enterprise", 112000.0, 135000.0),
        ("SRV-LEN-SR630", "Lenovo ThinkSystem SR630 V3 1U High-Performance Dual-Socket", "Lenovo Enterprise", 315000.0, 378000.0),
        ("SRV-LEN-SR650", "Lenovo ThinkSystem SR650 V3 2U Flagship Core Database", "Lenovo Enterprise", 410000.0, 492000.0),
        ("SRV-LEN-SR655", "Lenovo ThinkSystem SR655 V3 2U High-Core AMD EPYC Single-P", "Lenovo Enterprise", 340000.0, 408000.0),
        ("SRV-LEN-SR850", "Lenovo ThinkSystem SR850 V3 2U 4-Socket Mission-Critical", "Lenovo Enterprise", 740000.0, 888000.0),
        ("SRV-LEN-ST550", "Lenovo ThinkSystem ST550 4U Enterprise Tower/Rack Server", "Lenovo Enterprise", 230000.0, 276000.0),
        ("SRV-CISCO-C220", "Cisco UCS C220 M7 1U High-Density Rack Server", "Cisco Systems", 345000.0, 414000.0),
        ("SRV-CISCO-C240", "Cisco UCS C240 M7 2U Multi-Storage Enterprise Server", "Cisco Systems", 445000.0, 534000.0),
        ("SRV-DEL-T150", "Dell PowerEdge T150 4U Tower Branch Office Server", "Dell Technologies", 82000.0, 99000.0),
        ("SRV-DEL-T350", "Dell PowerEdge T350 1-Socket Tower Hot-Plug Storage", "Dell Technologies", 125000.0, 150000.0),
        ("SRV-DEL-T550", "Dell PowerEdge T550 2-Socket Tower Enterprise Compute", "Dell Technologies", 260000.0, 312000.0),
        ("SRV-HPE-ML110", "HPE ProLiant ML110 Gen11 Single-Processor Tower", "Hewlett Packard Enterprise", 135000.0, 162000.0),
        ("SRV-DEL-R6625", "Dell PowerEdge R6625 1U Dual AMD EPYC 9004 Gen", "Dell Technologies", 350000.0, 420000.0),
        ("SRV-DEL-R7625", "Dell PowerEdge R7625 2U Dual AMD EPYC High IOPS", "Dell Technologies", 460000.0, 552000.0),
        ("SRV-HPE-DL345", "HPE ProLiant DL345 Gen11 2U 1P AMD Storage Server", "Hewlett Packard Enterprise", 280000.0, 336000.0),
        ("SRV-LEN-SR665", "Lenovo ThinkSystem SR665 V3 2U Dual AMD 128-Core", "Lenovo Enterprise", 470000.0, 564000.0)
    ]

    for code, name, brd, cost, price in servers_data:
        pid = add_p(code, name, brd, "CAT-SRV", f"{name}, Mission-critical enterprise datacenter server with redundant power and remote management", f"{code}-BASE", cost, price)
        add_v(pid, f"{code}-128-2TB", f"{name} / 128GB ECC / 2x 1.92TB SAS SSD / Redundant 1100W PSU", "Dual Intel Xeon Silver/Gold / AMD EPYC", "128GB DDR5 ECC Registered", "3.84TB", "Enterprise SAS SSD RAID-1", "Integrated Matrox", "N/A", "N/A", "Silver/Metallic", "Quad 10G/25G SFP28 + OOBM iDRAC/iLO", "RHEL / VMware / Windows Server Ready", "1U / 2U Rackmount", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 5. ENTERPRISE STORAGE (CAT-STO) - 25 Products
    # --------------------------------------------------------------------------
    storage_data = [
        ("STO-DEL-PS500T", "Dell PowerStore 500T All-Flash Unified Storage Array", "Dell Technologies", 980000.0, 1176000.0),
        ("STO-DEL-PS1000T", "Dell PowerStore 1000T Enterprise NVMe SAN Array", "Dell Technologies", 1650000.0, 1980000.0),
        ("STO-DEL-PS3000T", "Dell PowerStore 3000T High-IOPS NVMe End-to-End", "Dell Technologies", 2450000.0, 2940000.0),
        ("STO-DEL-ME5024", "Dell PowerVault ME5024 2U 24-Bay SAS/FC Storage", "Dell Technologies", 520000.0, 624000.0),
        ("STO-DEL-ME5084", "Dell PowerVault ME5084 5U 84-Bay High-Density Storage", "Dell Technologies", 940000.0, 1128000.0),
        ("STO-HPE-MSA2060", "HPE MSA 2060 16Gb Fibre Channel Hybrid Storage", "Hewlett Packard Enterprise", 480000.0, 576000.0),
        ("STO-HPE-ALLETRA", "HPE Alletra 5000 Cloud-Native All-Flash SAN", "Hewlett Packard Enterprise", 1850000.0, 2220000.0),
        ("STO-NET-A150", "NetApp AFF A150 All-Flash SAN/NAS Array 24x 1.92TB", "Western Digital", 1450000.0, 1740000.0),
        ("STO-NET-A250", "NetApp AFF A250 NVMe End-to-End Enterprise Storage", "Western Digital", 2200000.0, 2640000.0),
        ("STO-NET-FAS2820", "NetApp FAS2820 Hybrid Cloud Storage Architecture", "Western Digital", 890000.0, 1068000.0),
        ("STO-SYN-FS3410", "Synology FlashStation FS3410 24-Bay All-Flash NAS", "Synology Inc.", 420000.0, 504000.0),
        ("STO-SYN-RS2423", "Synology RackStation RS2423+ 12-Bay 2U Storage", "Synology Inc.", 165000.0, 198000.0),
        ("STO-SYN-RS3621", "Synology RackStation RS3621xs+ 12-Bay High-IOPS", "Synology Inc.", 295000.0, 354000.0),
        ("STO-SYN-RS4021", "Synology RackStation RS4021xs+ 16-Bay 3U SAN/NAS", "Synology Inc.", 440000.0, 528000.0),
        ("STO-SYN-DS1821", "Synology DiskStation DS1821+ 8-Bay Desktop NAS", "Synology Inc.", 88000.0, 106000.0),
        ("STO-SYN-DS3622", "Synology DiskStation DS3622xs+ 12-Bay Enterprise Tower", "Synology Inc.", 235000.0, 282000.0),
        ("STO-QNP-TS1677", "QNAP TS-h1677XU-RP 16-Bay ZFS QuTS hero 3U NAS", "QNAP Systems", 380000.0, 456000.0),
        ("STO-QNP-TVS888", "QNAP TVS-h1688X 16-Bay ZFS Enterprise Desktop NAS", "QNAP Systems", 290000.0, 348000.0),
        ("STO-QNP-TS873A", "QNAP TS-873A 8-Bay AMD Ryzen PCIe Expansion NAS", "QNAP Systems", 94000.0, 113000.0),
        ("STO-WD-DATA60", "Western Digital Ultrastar Data60 60-Bay JBOD Storage", "Western Digital", 720000.0, 864000.0),
        ("STO-SEA-EXOSX", "Seagate Exos E 4U106 106-Bay High-Density Enclosure", "Seagate Technology", 1150000.0, 1380000.0),
        ("STO-SAM-PM9A3", "Samsung PM9A3 7.68TB U.2 NVMe PCIe 4.0 SSD (Pack of 4)", "Samsung Electronics", 195000.0, 234000.0),
        ("STO-SAM-883DCT", "Samsung 883 DCT 3.84TB SATA 2.5-inch SSD (Pack of 4)", "Samsung Electronics", 92000.0, 110000.0),
        ("STO-WD-SN650", "Western Digital Ultrastar DC SN650 15.36TB NVMe SSD", "Western Digital", 145000.0, 174000.0),
        ("STO-SEA-EXOS20", "Seagate Exos X20 20TB Enterprise SAS 12Gbps 7.2K (Pack of 4)", "Seagate Technology", 112000.0, 134000.0)
    ]

    for code, name, brd, cost, price in storage_data:
        pid = add_p(code, name, brd, "CAT-STO", f"{name}, Enterprise SAN/NAS high-availability storage array with dual controller support", f"{code}-BASE", cost, price)
        add_v(pid, f"{code}-STD", f"{name} / Dual Controller / 10G/25G iSCSI & 32Gb FC", "Dual Storage Processors", "64GB - 128GB Cache", "38.4TB - 76.8TB Raw", "NVMe / SAS Enterprise Flash", "N/A", "N/A", "N/A", "Charcoal/Black", "10GbE / 25GbE / 32Gb Fibre Channel", "Storage OS / SAN OS", "2U / 3U Rackmount", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 6. ENTERPRISE NETWORKING (CAT-NET) - 35 Products
    # --------------------------------------------------------------------------
    networking_data = [
        ("NET-CIS-C9200L-24P", "Cisco Catalyst 9200L 24-Port Gigabit PoE+ 4x10G Switch", "Cisco Systems", 125000.0, 150000.0),
        ("NET-CIS-C9200L-48P", "Cisco Catalyst 9200L 48-Port Gigabit PoE+ 4x10G Switch", "Cisco Systems", 185000.0, 222000.0),
        ("NET-CIS-C9300-24P", "Cisco Catalyst 9300 24-Port Multi-Gigabit PoE+ Network", "Cisco Systems", 240000.0, 288000.0),
        ("NET-CIS-C9300-48P", "Cisco Catalyst 9300 48-Port UPOE StackWise 480 Switch", "Cisco Systems", 320000.0, 384000.0),
        ("NET-CIS-C9500-24Y", "Cisco Catalyst 9500 24-Port 25G Fiber Core Switch", "Cisco Systems", 680000.0, 816000.0),
        ("NET-CIS-C9500-48Y", "Cisco Catalyst 9500 48-Port 25G/100G Leaf-Spine Core", "Cisco Systems", 950000.0, 1140000.0),
        ("NET-CIS-MS120-24P", "Cisco Meraki MS120-24P Cloud-Managed 24-Port PoE Switch", "Cisco Systems", 110000.0, 132000.0),
        ("NET-CIS-MS225-48P", "Cisco Meraki MS225-48P L2 Cloud Switch with 10G SFP+", "Cisco Systems", 175000.0, 210000.0),
        ("NET-CIS-MS390-48P", "Cisco Meraki MS390-48P Multi-Gigabit Modular Uplinks", "Cisco Systems", 295000.0, 354000.0),
        ("NET-ARU-6100-24G", "Aruba CX 6100 24G 4SFP+ Enterprise Access Switch", "Aruba Networks", 78000.0, 94000.0),
        ("NET-ARU-6200F-24P", "Aruba CX 6200F 24G Class 4 PoE 4SFP+ 370W Switch", "Aruba Networks", 115000.0, 138000.0),
        ("NET-ARU-6200F-48P", "Aruba CX 6200F 48G Class 4 PoE 4SFP+ 740W Switch", "Aruba Networks", 178000.0, 214000.0),
        ("NET-ARU-6300M-24P", "Aruba CX 6300M 24-Port Modular Core/Aggregation Switch", "Aruba Networks", 285000.0, 342000.0),
        ("NET-ARU-6300M-48P", "Aruba CX 6300M 48-Port Smart Rate 10G PoE Switch", "Aruba Networks", 390000.0, 468000.0),
        ("NET-ARU-AP515", "Aruba AP-515 Unified Campus Wi-Fi 6 Access Point", "Aruba Networks", 38000.0, 45600.0),
        ("NET-ARU-AP635", "Aruba AP-635 Enterprise Wi-Fi 6E Tri-Band Access Point", "Aruba Networks", 58000.0, 69600.0),
        ("NET-CIS-CW9164", "Cisco Catalyst 9164I Wi-Fi 6E Tri-Band AP", "Cisco Systems", 62000.0, 74400.0),
        ("NET-UBI-USW-24P", "Ubiquiti UniFi Pro 24 PoE Layer 2/3 Enterprise Switch", "Ubiquiti Networks", 42000.0, 50400.0),
        ("NET-UBI-USW-48P", "Ubiquiti UniFi Pro 48 PoE Layer 3 600W 4x 10G SFP+", "Ubiquiti Networks", 74000.0, 88800.0),
        ("NET-UBI-USW-ENT24", "Ubiquiti UniFi Enterprise 24 PoE 2.5G Multi-Gigabit", "Ubiquiti Networks", 62000.0, 74400.0),
        ("NET-UBI-U6-PRO", "Ubiquiti UniFi U6 Pro Dual-Band Wi-Fi 6 AP", "Ubiquiti Networks", 14000.0, 16800.0),
        ("NET-UBI-U6-ENT", "Ubiquiti UniFi U6 Enterprise Tri-Band Wi-Fi 6E AP", "Ubiquiti Networks", 26000.0, 31200.0),
        ("NET-JUN-EX2300", "Juniper EX2300 24-Port Gigabit PoE+ Compact Switch", "Aruba Networks", 82000.0, 98400.0),
        ("NET-JUN-EX3400", "Juniper EX3400 48-Port Gigabit PoE+ Virtual Chassis", "Aruba Networks", 165000.0, 198000.0),
        ("NET-JUN-EX4400", "Juniper EX4400 24-Port Multi-Gigabit Cloud-Ready Switch", "Aruba Networks", 255000.0, 306000.0),
        ("NET-FOR-FS124F", "Fortinet FortiSwitch 124F 24-Port GE Layer 2 PoE Switch", "Fortinet", 58000.0, 69600.0),
        ("NET-FOR-FS148F", "Fortinet FortiSwitch 148F 48-Port GE PoE+ 4x 10G SFP+", "Fortinet", 98000.0, 117600.0),
        ("NET-FOR-FS424E", "Fortinet FortiSwitch 424E-FIBER 24x 1G/10G SFP+ Aggregation", "Fortinet", 195000.0, 234000.0),
        ("NET-CIS-SFP-10G", "Cisco 10GBASE-SR SFP+ Optical Transceiver (Pack of 4)", "Cisco Systems", 32000.0, 38400.0),
        ("NET-CIS-SFP-25G", "Cisco 25GBASE-SR SFP28 Optical Transceiver (Pack of 2)", "Cisco Systems", 44000.0, 52800.0),
        ("NET-ARU-SFP-10G", "Aruba 10G SFP+ LC SR 300m MMF Transceiver (Pack of 4)", "Aruba Networks", 28000.0, 33600.0),
        ("NET-CIS-DAC-10G", "Cisco 10G SFP+ Twinax Direct Attach Copper Cable 3m (Pack of 5)", "Cisco Systems", 16000.0, 19200.0),
        ("NET-UBI-AGGREG", "Ubiquiti UniFi Switch Aggregation 8-Port 10G SFP+", "Ubiquiti Networks", 25000.0, 30000.0),
        ("NET-CIS-C9200-24T", "Cisco Catalyst 9200 24-Port Data Only Modular Uplink", "Cisco Systems", 95000.0, 114000.0),
        ("NET-ARU-AP655", "Aruba AP-655 High-Density Campus Wi-Fi 6E AP", "Aruba Networks", 72000.0, 86400.0)
    ]

    for code, name, brd, cost, price in networking_data:
        pid = add_p(code, name, brd, "CAT-NET", f"{name}, High-throughput low-latency enterprise campus network infrastructure", f"{code}-BASE", cost, price)
        add_v(pid, f"{code}-STD", f"{name} / 19-inch Rackmount / Redundant Power Ready", "Network Processor", "2GB - 4GB", "512MB Flash", "Flash Storage", "N/A", "N/A", "N/A", "Cisco Grey/Teal", "10G/25G SFP+ Uplinks", "IOS-XE / ArubaOS-CX / UniFi", "1U Rackmount", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 7. CYBERSECURITY & FIREWALLS (CAT-SEC) - 25 Products
    # --------------------------------------------------------------------------
    firewalls_data = [
        ("SEC-FOR-FG40F", "Fortinet FortiGate 40F Secure SD-WAN Firewall", "Fortinet", 38000.0, 45600.0),
        ("SEC-FOR-FG60F", "Fortinet FortiGate 60F Enterprise Branch Firewall", "Fortinet", 58000.0, 69600.0),
        ("SEC-FOR-FG70F", "Fortinet FortiGate 70F High-Performance NGFW", "Fortinet", 78000.0, 93600.0),
        ("SEC-FOR-FG80F", "Fortinet FortiGate 80F Dual WAN Bypass Firewall", "Fortinet", 110000.0, 132000.0),
        ("SEC-FOR-FG100F", "Fortinet FortiGate 100F Campus Core NGFW 10G SFP+", "Fortinet", 195000.0, 234000.0),
        ("SEC-FOR-FG200F", "Fortinet FortiGate 200F High-Throughput Perimeter Firewall", "Fortinet", 340000.0, 408000.0),
        ("SEC-FOR-FG400F", "Fortinet FortiGate 400F Datacenter Security Gateway", "Fortinet", 650000.0, 780000.0),
        ("SEC-PAL-PA410", "Palo Alto Networks PA-410 Machine Learning NGFW", "Palo Alto Networks", 88000.0, 105600.0),
        ("SEC-PAL-PA440", "Palo Alto Networks PA-440 Branch Security Appliance", "Palo Alto Networks", 145000.0, 174000.0),
        ("SEC-PAL-PA450", "Palo Alto Networks PA-450 High-Availability Firewall", "Palo Alto Networks", 210000.0, 252000.0),
        ("SEC-PAL-PA460", "Palo Alto Networks PA-460 Multi-Gigabit NGFW", "Palo Alto Networks", 280000.0, 336000.0),
        ("SEC-PAL-PA1410", "Palo Alto Networks PA-1410 10G Fiber Perimeter Gateway", "Palo Alto Networks", 580000.0, 696000.0),
        ("SEC-PAL-PA3410", "Palo Alto Networks PA-3410 Datacenter Inspection Firewall", "Palo Alto Networks", 980000.0, 1176000.0),
        ("SEC-SOP-XGS116", "Sophos XGS 116 Desktop Next-Gen Firewall with PoE", "Sophos Technologies", 48000.0, 57600.0),
        ("SEC-SOP-XGS136", "Sophos XGS 136 High-Capacity Branch Firewall", "Sophos Technologies", 74000.0, 88800.0),
        ("SEC-SOP-XGS2100", "Sophos XGS 2100 1U Enterprise Rackmount Firewall", "Sophos Technologies", 160000.0, 192000.0),
        ("SEC-SOP-XGS2300", "Sophos XGS 2300 Redundant Power NGFW Appliance", "Sophos Technologies", 240000.0, 288000.0),
        ("SEC-SOP-XGS3100", "Sophos XGS 3100 Datacenter Protection Appliance", "Sophos Technologies", 380000.0, 456000.0),
        ("SEC-CHK-1570", "Check Point Quantum Spark 1570 Enterprise Security", "Check Point", 72000.0, 86400.0),
        ("SEC-CHK-1600", "Check Point Quantum Spark 1600 1GbE High Performance", "Check Point", 125000.0, 150000.0),
        ("SEC-CHK-1800", "Check Point Quantum Spark 1800 10GbE Security Gateway", "Check Point", 210000.0, 252000.0),
        ("SEC-CIS-FPR1010", "Cisco Secure Firewall Firepower 1010 Desktop NGFW", "Cisco Systems", 68000.0, 81600.0),
        ("SEC-CIS-FPR1120", "Cisco Secure Firewall Firepower 1120 1U Appliance", "Cisco Systems", 155000.0, 186000.0),
        ("SEC-CIS-FPR2110", "Cisco Secure Firewall Firepower 2110 Campus Perimeter", "Cisco Systems", 320000.0, 384000.0),
        ("SEC-FOR-FG600F", "Fortinet FortiGate 600F Datacenter Core 25G/40G Security", "Fortinet", 920000.0, 1104000.0)
    ]

    for code, name, brd, cost, price in firewalls_data:
        pid = add_p(code, name, brd, "CAT-SEC", f"{name}, Enterprise perimeter cybersecurity, deep packet inspection, and encrypted SSL tunnel acceleration", f"{code}-BASE", cost, price)
        add_v(pid, f"{code}-STD", f"{name} / Hardware Appliance / Base Bundle", "Security Processing Unit ASIC", "4GB - 16GB", "32GB - 128GB eMMC/SSD", "Encrypted Solid State", "N/A", "N/A", "N/A", "Matte White/Grey", "1G/10G SFP+ Dual WAN", "FortiOS / PAN-OS / SophosOS", "Desktop / 1U Rack", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 8. FINANCIAL TRADING & PROFESSIONAL DISPLAYS (CAT-MON) - 32 Products
    # --------------------------------------------------------------------------
    monitors_data = [
        ("MON-DEL-P2422H", "Dell P2422H 24-inch ComfortView Plus Business Monitor", "Dell Technologies", 11500.0, 13800.0),
        ("MON-DEL-P2722H", "Dell P2722H 27-inch Ergonomic Corporate Display", "Dell Technologies", 16000.0, 19200.0),
        ("MON-DEL-U2424H", "Dell UltraSharp U2424H 24-inch 120Hz Ambient Sensor", "Dell Technologies", 18500.0, 22200.0),
        ("MON-DEL-U2724D", "Dell UltraSharp U2724D 27-inch QHD 120Hz IPS Black", "Dell Technologies", 31000.0, 37200.0),
        ("MON-DEL-U2723QE", "Dell UltraSharp U2723QE 27-inch 4K USB-C Hub Monitor", "Dell Technologies", 48000.0, 57600.0),
        ("MON-DEL-U3223QE", "Dell UltraSharp U3223QE 31.5-inch 4K IPS Black 2000:1", "Dell Technologies", 62000.0, 74400.0),
        ("MON-DEL-U3423WE", "Dell UltraSharp U3423WE 34-inch WQHD Curved USB-C Hub", "Dell Technologies", 68000.0, 81600.0),
        ("MON-DEL-U3824DW", "Dell UltraSharp U3824DW 37.5-inch WQHD+ Financial Ultrawide", "Dell Technologies", 98000.0, 117600.0),
        ("MON-DEL-U4924DW", "Dell UltraSharp U4924DW 49-inch Dual QHD Trading Station Display", "Dell Technologies", 125000.0, 150000.0),
        ("MON-LG-27UK850", "LG 27-inch 4K UHD IPS USB-C Display with HDR10", "LG Electronics", 29000.0, 34800.0),
        ("MON-LG-32UN880", "LG 32UN880 Ergo Arm 32-inch 4K UHD UltraFine Display", "LG Electronics", 46000.0, 55200.0),
        ("MON-LG-34WN80C", "LG 34WN80C-B 34-inch 21:9 Curved Ultrawide USB-C Display", "LG Electronics", 42000.0, 50400.0),
        ("MON-LG-38WN95C", "LG 38WN95C-W 38-inch 144Hz Nano IPS Thunderbolt 3 Display", "LG Electronics", 92000.0, 110400.0),
        ("MON-LG-49WL95C", "LG 49WL95C-W 49-inch 32:9 Dual QHD Curved Trading Screen", "LG Electronics", 118000.0, 141600.0),
        ("MON-HP-E24G5", "HP E24 G5 23.8-inch FHD Ergonomic Business Monitor", "HP Inc.", 12000.0, 14400.0),
        ("MON-HP-E27QG5", "HP E27q G5 27-inch QHD Corporate Workstation Display", "HP Inc.", 22000.0, 26400.0),
        ("MON-HP-Z27KG3", "HP Z27k G3 27-inch 4K USB-C Color-Calibrated Display", "HP Inc.", 44000.0, 52800.0),
        ("MON-HP-Z34CG4", "HP Z34c G4 34-inch WQHD Curved Conferencing Display", "HP Inc.", 64000.0, 76800.0),
        ("MON-LEN-T24I30", "Lenovo ThinkVision T24i-30 23.8-inch FHD IPS Screen", "Lenovo Enterprise", 10800.0, 12960.0),
        ("MON-LEN-T27H30", "Lenovo ThinkVision T27h-30 27-inch QHD USB-C Hub Monitor", "Lenovo Enterprise", 26000.0, 31200.0),
        ("MON-LEN-P27U20", "Lenovo ThinkVision P27u-20 27-inch 4K Thunderbolt 4 Display", "Lenovo Enterprise", 49000.0, 58800.0),
        ("MON-LEN-P34W20", "Lenovo ThinkVision P34w-20 34.1-inch WQHD Curved Display", "Lenovo Enterprise", 58000.0, 69600.0),
        ("MON-VIEW-VP2768", "ViewSonic ColorPro VP2768a 27-inch Factory Calibrated QHD", "ViewSonic", 34000.0, 40800.0),
        ("MON-VIEW-VP3481", "ViewSonic ColorPro VP3481a 34-inch Curved Ultrawide USB-C", "ViewSonic", 68000.0, 81600.0),
        ("MON-SAM-S80PB", "Samsung ViewFinity S8 27-inch 4K Matte Anti-Glare Display", "Samsung Electronics", 36000.0, 43200.0),
        ("MON-SAM-S95UA", "Samsung ViewFinity S9 49-inch 120Hz Dual QHD Ultrawide", "Samsung Electronics", 112000.0, 134400.0),
        ("MON-ASUS-PA279C", "ASUS ProArt PA279CV 27-inch 4K 100% sRGB Color Grading", "ASUS Commercial", 39000.0, 46800.0),
        ("MON-ASUS-PA329C", "ASUS ProArt PA329CV 32-inch 4K HDR-400 Professional", "ASUS Commercial", 56000.0, 67200.0),
        ("MON-DEL-C2423H", "Dell C2423H 24-inch Video Conferencing FHD Display", "Dell Technologies", 19500.0, 23400.0),
        ("MON-HP-E24MCG4", "HP E24m G4 23.8-inch Zoom Certified USB-C Web Display", "HP Inc.", 21000.0, 25200.0),
        ("MON-DEL-P3424WEB", "Dell P3424WEB 34-inch Curved Video Conferencing Ultrawide", "Dell Technologies", 76000.0, 91200.0),
        ("MON-LG-29WN600", "LG 29WN600-W 29-inch 21:9 UltraWide Spreadsheets Display", "LG Electronics", 16500.0, 19800.0)
    ]

    for code, name, brd, cost, price in monitors_data:
        pid = add_p(code, name, brd, "CAT-MON", f"{name}, Professional enterprise display, ergonomic height-adjustable stand, Eye-Care certification", f"{code}-BASE", cost, price, serialized=True)
        add_v(pid, f"{code}-STD", f"{name} / Factory Calibrated / Tilt-Swivel-Pivot", "Display Processor", "N/A", "N/A", "N/A", "N/A", "24.0\" - 49.0\"", "FHD / QHD / 4K / Dual QHD", "Silver / Black", "DisplayPort / HDMI / USB-C 90W PD", "VESA Standard", "Monitor", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 9. MISSION-CRITICAL ONLINE UPS (CAT-UPS) - 20 Products
    # --------------------------------------------------------------------------
    ups_data = [
        ("UPS-APC-SRT1K", "APC Smart-UPS On-Line SRT 1000VA 230V 1U Rack/Tower", "Schneider Electric / APC", 42000.0, 50400.0),
        ("UPS-APC-SRT2K2", "APC Smart-UPS On-Line SRT 2200VA 230V 2U Rack/Tower", "Schneider Electric / APC", 72000.0, 86400.0),
        ("UPS-APC-SRT3K", "APC Smart-UPS On-Line SRT 3000VA 230V 2U Pure Sine-Wave", "Schneider Electric / APC", 98000.0, 117600.0),
        ("UPS-APC-SRT5K", "APC Smart-UPS On-Line SRT 5000VA 230V 3U Enterprise Core", "Schneider Electric / APC", 175000.0, 210000.0),
        ("UPS-APC-SRT6K", "APC Smart-UPS On-Line SRT 6000VA 230V 4U Server Room", "Schneider Electric / APC", 215000.0, 258000.0),
        ("UPS-APC-SRT10K", "APC Smart-UPS On-Line SRT 10kVA 230V 6U Datacenter Row", "Schneider Electric / APC", 360000.0, 432000.0),
        ("UPS-EAT-9PX1500", "Eaton 9PX 1500VA 2U Online Double-Conversion UPS", "Eaton Corporation", 48000.0, 57600.0),
        ("UPS-EAT-9PX3000", "Eaton 9PX 3000VA 2U Energy Star Certified Online UPS", "Eaton Corporation", 94000.0, 112800.0),
        ("UPS-EAT-9PX6000", "Eaton 9PX 6000VA 3U Hot-Swappable Maintenance Bypass", "Eaton Corporation", 185000.0, 222000.0),
        ("UPS-EAT-9PX11K", "Eaton 9PX 11000VA 6U Redundant Datacenter Power", "Eaton Corporation", 380000.0, 456000.0),
        ("UPS-VER-GXT5-1K", "Vertiv Liebert GXT5 1000VA 2U Online Double-Conversion", "Vertiv Holdings", 39000.0, 46800.0),
        ("UPS-VER-GXT5-2K", "Vertiv Liebert GXT5 2000VA 2U High-Density Pure Sine", "Vertiv Holdings", 68000.0, 81600.0),
        ("UPS-VER-GXT5-3K", "Vertiv Liebert GXT5 3000VA 2U Mission-Critical Server UPS", "Vertiv Holdings", 92000.0, 110400.0),
        ("UPS-VER-GXT5-5K", "Vertiv Liebert GXT5 5000VA 5U Intelligent Power Solution", "Vertiv Holdings", 168000.0, 201600.0),
        ("UPS-VER-GXT5-10K", "Vertiv Liebert GXT5 10kVA 6U Integrated Maintenance Bypass", "Vertiv Holdings", 345000.0, 414000.0),
        ("UPS-APC-SMT1500", "APC Smart-UPS 1500VA LCD 230V Line-Interactive Desktop", "Schneider Electric / APC", 26000.0, 31200.0),
        ("UPS-APC-SMT2200", "APC Smart-UPS 2200VA LCD 230V Workstation Tower", "Schneider Electric / APC", 48000.0, 57600.0),
        ("UPS-EAT-5P1500", "Eaton 5P 1500VA 1U High-Density Rackmount UPS", "Eaton Corporation", 32000.0, 38400.0),
        ("UPS-VER-PSI5-15", "Vertiv Liebert PSI5 1500VA 2U AVR Enterprise Rack UPS", "Vertiv Holdings", 29000.0, 34800.0),
        ("UPS-APC-PDU8G", "APC NetShelter Metered Rack PDU 16A 230V (8 Outlets)", "Schneider Electric / APC", 14000.0, 16800.0)
    ]

    for code, name, brd, cost, price in ups_data:
        pid = add_p(code, name, brd, "CAT-UPS", f"{name}, Pure sine wave zero-transfer-time power protection for financial infrastructure", f"{code}-BASE", cost, price, serialized=True)
        add_v(pid, f"{code}-STD", f"{name} / Sealed Lead-Acid Battery / LCD Display", "Power Inverter DSP", "N/A", "N/A", "N/A", "N/A", "N/A", "230V Pure Sine", "Black", "SNMP / USB / Relay Card", "Embedded Firmware", "2U / 3U / Tower", 24, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 10. ENTERPRISE SMARTPHONES & MOBILITY (CAT-SMP) - 20 Products
    # --------------------------------------------------------------------------
    smartphones_data = [
        ("SMP-APL-IP16P-256", "Apple iPhone 16 Pro 256GB Grade 5 Titanium", "Apple Inc.", "Apple A18 Pro 3nm, 6.3 Super Retina XDR OLED, 48MP Fusion Camera", "MYMV3HN/A", 108000.0, 129900.0,
         [("SMP-APL-IP16P-256-BLK", "iPhone 16 Pro 256GB / Black Titanium", "Apple A18 Pro", "8GB", "256GB", "NVMe", "Apple 6-Core GPU", "6.3\"", "2622x1206 OLED 120Hz", "Black Titanium", "5G Sub-6 + Wi-Fi 7", "iOS 18", "Smartphone", 12, 0.0, 108000.0, 129900.0),
          ("SMP-APL-IP16P-256-NAT", "iPhone 16 Pro 256GB / Natural Titanium", "Apple A18 Pro", "8GB", "256GB", "NVMe", "Apple 6-Core GPU", "6.3\"", "2622x1206 OLED 120Hz", "Natural Titanium", "5G Sub-6 + Wi-Fi 7", "iOS 18", "Smartphone", 12, 0.0, 108000.0, 129900.0)]),
        ("SMP-APL-IP16PM-512", "Apple iPhone 16 Pro Max 512GB Executive Mobile", "Apple Inc.", "Apple A18 Pro, 6.9 Display, Action Button, 5x Optical Periscope", "MYWU3HN/A", 138000.0, 164900.0,
         [("SMP-APL-IP16PM-512-NAT", "iPhone 16 Pro Max 512GB / Natural Titanium", "Apple A18 Pro", "8GB", "512GB", "NVMe", "Apple 6-Core GPU", "6.9\"", "2868x1320 OLED 120Hz", "Natural Titanium", "5G Sub-6 + Wi-Fi 7", "iOS 18", "Smartphone", 12, 0.0, 138000.0, 164900.0)]),
        ("SMP-APL-IP16-128", "Apple iPhone 16 128GB Corporate Standard", "Apple Inc.", "Apple A18 Chip, 6.1 OLED, Dynamic Island, Macro Photography", "MYEK3HN/A", 68000.0, 79900.0,
         [("SMP-APL-IP16-128-BLK", "iPhone 16 128GB / Black", "Apple A18", "8GB", "128GB", "NVMe", "Apple 5-Core GPU", "6.1\"", "2556x1179 OLED", "Black", "5G + Wi-Fi 7", "iOS 18", "Smartphone", 12, 0.0, 68000.0, 79900.0)]),
        ("SMP-APL-IP15-128", "Apple iPhone 15 128GB Fleet Deployment", "Apple Inc.", "Apple A16 Bionic, 6.1 Super Retina XDR, USB-C Charging Port", "MTP03HN/A", 58000.0, 69900.0,
         [("SMP-APL-IP15-128-BLK", "iPhone 15 128GB / Black", "Apple A16 Bionic", "6GB", "128GB", "NVMe", "Apple 5-Core GPU", "6.1\"", "2556x1179 OLED", "Black", "5G + Wi-Fi 6", "iOS 17", "Smartphone", 12, 0.0, 58000.0, 69900.0)]),
        ("SMP-SAM-S24U-256", "Samsung Galaxy S24 Ultra 256GB Titanium AI Flagship", "Samsung Electronics", "Snapdragon 8 Gen 3 for Galaxy, Galaxy AI, Integrated S Pen", "SM-S928BZTCINS", 108000.0, 129999.0,
         [("SMP-SAM-S24U-256-GRY", "Galaxy S24 Ultra 256GB / Titanium Gray", "Snapdragon 8 Gen 3", "12GB", "256GB", "UFS 4.0", "Adreno 750", "6.8\"", "3120x1440 AMOLED 120Hz", "Titanium Gray", "5G + Wi-Fi 7", "Android 14 / One UI 6", "Smartphone", 12, 0.0, 108000.0, 129999.0),
          ("SMP-SAM-S24U-512-BLK", "Galaxy S24 Ultra 512GB / Titanium Black", "Snapdragon 8 Gen 3", "12GB", "512GB", "UFS 4.0", "Adreno 750", "6.8\"", "3120x1440 AMOLED 120Hz", "Titanium Black", "5G + Wi-Fi 7", "Android 14 / One UI 6", "Smartphone", 12, 14000.0, 120000.0, 143999.0)]),
        ("SMP-SAM-S24-256", "Samsung Galaxy S24 256GB Enterprise Edition", "Samsung Electronics", "Exynos 2400 / Snapdragon 8 Gen 3, Knox Security Suite, 7 Years OS Updates", "SM-S921BZSCINS", 65000.0, 79999.0,
         [("SMP-SAM-S24-256-BLK", "Galaxy S24 256GB / Onyx Black", "Exynos 2400", "8GB", "256GB", "UFS 4.0", "Xclipse 940", "6.2\"", "2340x1080 AMOLED 120Hz", "Onyx Black", "5G + Wi-Fi 6E", "Android 14 / One UI 6", "Smartphone", 12, 0.0, 65000.0, 79999.0)]),
        ("SMP-SAM-ZFLD5-512", "Samsung Galaxy Z Fold5 512GB Executive Multitasking", "Samsung Electronics", "7.6 Foldable Dynamic AMOLED 2X, Multi-Window Financial Terminal", "SM-F946BZKHINS", 138000.0, 164999.0,
         [("SMP-SAM-ZFLD5-512-BLK", "Galaxy Z Fold5 512GB / Phantom Black", "Snapdragon 8 Gen 2", "12GB", "512GB", "UFS 4.0", "Adreno 740", "7.6\" Foldable", "2176x1812 AMOLED 120Hz", "Phantom Black", "5G + Wi-Fi 6E", "Android 13 / One UI 5", "Foldable", 12, 0.0, 138000.0, 164999.0)]),
        ("SMP-SAM-A55-128", "Samsung Galaxy A55 5G 128GB Corporate Field Staff", "Samsung Electronics", "Exynos 1480, Metal Frame, IP67 Water Resistance, Knox Vault", "SM-A556EZKCINS", 32000.0, 39999.0,
         [("SMP-SAM-A55-128-NVY", "Galaxy A55 5G 128GB / Awesome Navy", "Exynos 1480", "8GB", "128GB", "UFS 3.1", "Xclipse 530", "6.6\"", "2340x1080 AMOLED 120Hz", "Awesome Navy", "5G + Wi-Fi 6", "Android 14", "Smartphone", 12, 0.0, 32000.0, 39999.0)]),
        ("SMP-GOOG-PX8P-256", "Google Pixel 8 Pro 256GB Enterprise AI Device", "Google Enterprise", "Google Tensor G3, Titan M2 Security Chip, Best-in-Class Zero-Day Patching", "GA04934-IN", 88000.0, 106999.0,
         [("SMP-GOOG-PX8P-256-OBS", "Pixel 8 Pro 256GB / Obsidian", "Google Tensor G3", "12GB", "256GB", "UFS 3.1", "Immortalis-G715", "6.7\"", "2992x1344 LTPO OLED", "Obsidian", "5G + Wi-Fi 7", "Android 14 (Stock)", "Smartphone", 12, 0.0, 88000.0, 106999.0)]),
        ("SMP-GOOG-PX8-128", "Google Pixel 8 128GB Corporate Secure Mobile", "Google Enterprise", "Google Tensor G3, Actua Display, Audio Magic Eraser, Fast Face Unlock", "GA04834-IN", 61000.0, 75999.0,
         [("SMP-GOOG-PX8-128-HAZ", "Pixel 8 128GB / Hazel", "Google Tensor G3", "8GB", "128GB", "UFS 3.1", "Immortalis-G715", "6.2\"", "2400x1080 OLED 120Hz", "Hazel", "5G + Wi-Fi 7", "Android 14", "Smartphone", 12, 0.0, 61000.0, 75999.0)]),
        ("SMP-ONE-12-256", "OnePlus 12 5G 256GB High-Spec Corporate Mobile", "OnePlus Technology", "Snapdragon 8 Gen 3, 2K 120Hz ProXDR Display, 100W SUPERVOOC Fast Charge", "CPH2573", 54000.0, 64999.0,
         [("SMP-ONE-12-256-BLK", "OnePlus 12 256GB / Silky Black", "Snapdragon 8 Gen 3", "12GB", "256GB", "UFS 4.0", "Adreno 750", "6.82\"", "3168x1440 AMOLED 120Hz", "Silky Black", "5G + Wi-Fi 7", "OxygenOS 14", "Smartphone", 12, 0.0, 54000.0, 64999.0)]),
        ("SMP-ONE-12R-256", "OnePlus 12R 5G 256GB Value Performance Device", "OnePlus Technology", "Snapdragon 8 Gen 2, 5500mAh 2-Day Battery Life, 120Hz Display", "CPH2585", 38000.0, 45999.0,
         [("SMP-ONE-12R-256-GRY", "OnePlus 12R 256GB / Iron Gray", "Snapdragon 8 Gen 2", "16GB", "256GB", "UFS 3.1", "Adreno 740", "6.78\"", "2780x1264 AMOLED", "Iron Gray", "5G + Wi-Fi 7", "OxygenOS 14", "Smartphone", 12, 0.0, 38000.0, 45999.0)]),
        ("SMP-MOT-THINK", "Motorola ThinkPhone by Lenovo 256GB Enterprise", "Motorola Business", "Snapdragon 8+ Gen 1, Aramid Fiber Back, ThinkShield & Ready For Integration", "PAV00001IN", 44000.0, 53999.0,
         [("SMP-MOT-THINK-256-BLK", "ThinkPhone 256GB / Carbon Black", "Snapdragon 8+ Gen 1", "8GB", "256GB", "UFS 3.1", "Adreno 730", "6.6\"", "2400x1080 pOLED 144Hz", "Carbon Black", "5G + Wi-Fi 6E", "Android 13 Enterprise", "Smartphone", 12, 0.0, 44000.0, 53999.0)]),
        ("SMP-MOT-E50P", "Motorola Edge 50 Pro 5G 256GB Vegan Leather", "Motorola Business", "Snapdragon 7 Gen 3, Pantone Validated Display, 125W TurboPower", "PB100004IN", 31000.0, 37999.0,
         [("SMP-MOT-E50P-256-BLK", "Edge 50 Pro 256GB / Black Beauty", "Snapdragon 7 Gen 3", "12GB", "256GB", "UFS 2.2", "Adreno 720", "6.7\"", "2712x1220 pOLED 144Hz", "Black Beauty", "5G + Wi-Fi 6E", "Hello UI / Android 14", "Smartphone", 12, 0.0, 31000.0, 37999.0)]),
        ("SMP-APL-IP15P-128", "Apple iPhone 15 Pro 128GB Titanium Executive", "Apple Inc.", "Apple A17 Pro, 3x Telephoto, Action Button, Lightweight Titanium", "MTV03HN/A", 98000.0, 119900.0,
         [("SMP-APL-IP15P-128-BLU", "iPhone 15 Pro 128GB / Blue Titanium", "Apple A17 Pro", "8GB", "128GB", "NVMe", "Apple 6-Core GPU", "6.1\"", "2556x1179 OLED 120Hz", "Blue Titanium", "5G + Wi-Fi 6E", "iOS 17", "Smartphone", 12, 0.0, 98000.0, 119900.0)]),
        ("SMP-SAM-S23-128", "Samsung Galaxy S23 5G 128GB Enterprise Compact", "Samsung Electronics", "Snapdragon 8 Gen 2 for Galaxy, 6.1 Flat AMOLED, Knox Suite", "SM-S911BZKDINS", 48000.0, 58999.0,
         [("SMP-SAM-S23-128-BLK", "Galaxy S23 128GB / Phantom Black", "Snapdragon 8 Gen 2", "8GB", "128GB", "UFS 3.1", "Adreno 740", "6.1\"", "2340x1080 AMOLED 120Hz", "Phantom Black", "5G + Wi-Fi 6E", "Android 13 / One UI 5", "Smartphone", 12, 0.0, 48000.0, 58999.0)]),
        ("SMP-SAM-S24P-256", "Samsung Galaxy S24+ 256GB QHD+ Display", "Samsung Electronics", "Exynos 2400, 6.7 QHD+ Dynamic AMOLED, 4900mAh Battery", "SM-S926BZKCINS", 82000.0, 99999.0,
         [("SMP-SAM-S24P-256-BLK", "Galaxy S24+ 256GB / Cobalt Violet", "Exynos 2400", "12GB", "256GB", "UFS 4.0", "Xclipse 940", "6.7\"", "3120x1440 AMOLED 120Hz", "Cobalt Violet", "5G + Wi-Fi 6E", "Android 14 / One UI 6", "Smartphone", 12, 0.0, 82000.0, 99999.0)]),
        ("SMP-SAM-ZFLP5-256", "Samsung Galaxy Z Flip5 256GB Pocket Foldable", "Samsung Electronics", "Snapdragon 8 Gen 2, 3.4 Flex Window Outer Screen, Compact Portability", "SM-F731BZKEINS", 81000.0, 99999.0,
         [("SMP-SAM-ZFLP5-256-GRY", "Galaxy Z Flip5 256GB / Graphite", "Snapdragon 8 Gen 2", "8GB", "256GB", "UFS 4.0", "Adreno 740", "6.7\" Foldable", "2640x1080 AMOLED 120Hz", "Graphite", "5G + Wi-Fi 6E", "Android 13 / One UI 5", "Foldable", 12, 0.0, 81000.0, 99999.0)]),
        ("SMP-SAM-XCOV6P", "Samsung Galaxy XCover6 Pro Rugged Enterprise", "Samsung Electronics", "MIL-STD-810H, IP68, Replaceable 4050mAh Battery, Barcode Scanner Ready", "SM-G736BZKGINS", 42000.0, 51999.0,
         [("SMP-SAM-XCOV6P-128-BLK", "XCover6 Pro 128GB / Rugged Black", "Snapdragon 778G", "6GB", "128GB", "microSD up to 1TB", "Adreno 642L", "6.6\"", "2408x1080 120Hz Wet Touch", "Black Rugged", "5G + Wi-Fi 6E", "Android 13 Enterprise", "Rugged Smartphone", 24, 0.0, 42000.0, 51999.0)]),
        ("SMP-APL-IP16P-1TB", "Apple iPhone 16 Pro 1TB Maximum Capacity Flagship", "Apple Inc.", "Apple A18 Pro 3nm, 1TB Storage, ProRes 4K 120fps Recording", "MYN33HN/A", 138000.0, 169900.0,
         [("SMP-APL-IP16P-1TB-DSRT", "iPhone 16 Pro 1TB / Desert Titanium", "Apple A18 Pro", "8GB", "1TB", "NVMe", "Apple 6-Core GPU", "6.3\"", "2622x1206 OLED 120Hz", "Desert Titanium", "5G + Wi-Fi 7", "iOS 18", "Smartphone", 12, 0.0, 138000.0, 169900.0)])
    ]

    for row in smartphones_data:
        pid = add_p(row[0], row[1], row[2], "CAT-SMP", row[3], row[4], row[5], row[6])
        for v in row[7]:
            add_v(pid, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15], v[16])

    # --------------------------------------------------------------------------
    # 11. ENTERPRISE TABLETS (CAT-TAB) - 12 Products
    # --------------------------------------------------------------------------
    tablets_data = [
        ("TAB-APL-IPAD10", "Apple iPad 10th Gen 10.9-inch Wi-Fi 64GB", "Apple Inc.", 33000.0, 39900.0),
        ("TAB-APL-AIR11", "Apple iPad Air 11-inch M2 Chip 128GB Liquid Retina", "Apple Inc.", 51000.0, 59900.0),
        ("TAB-APL-AIR13", "Apple iPad Air 13-inch M2 Chip 128GB Large Canvas", "Apple Inc.", 68000.0, 79900.0),
        ("TAB-APL-PRO11", "Apple iPad Pro 11-inch M4 Ultra-Thin Tandem OLED 256GB", "Apple Inc.", 85000.0, 99900.0),
        ("TAB-APL-PRO13", "Apple iPad Pro 13-inch M4 Ultra-Thin Tandem OLED 256GB", "Apple Inc.", 110000.0, 129900.0),
        ("TAB-SAM-S9-128", "Samsung Galaxy Tab S9 11-inch Dynamic AMOLED 2X 128GB", "Samsung Electronics", 61000.0, 72999.0),
        ("TAB-SAM-S9P-256", "Samsung Galaxy Tab S9+ 12.4-inch AMOLED 256GB with S Pen", "Samsung Electronics", 76000.0, 90999.0),
        ("TAB-SAM-S9U-256", "Samsung Galaxy Tab S9 Ultra 14.6-inch Laptop Alternative", "Samsung Electronics", 92000.0, 108999.0),
        ("TAB-SAM-FE-128", "Samsung Galaxy Tab S9 FE 10.9-inch 128GB Corporate Tab", "Samsung Electronics", 36000.0, 44999.0),
        ("TAB-SAM-ACT4", "Samsung Galaxy Tab Active4 Pro 10.1 Rugged Field Tablet", "Samsung Electronics", 52000.0, 62999.0),
        ("TAB-MS-SP9-I5", "Microsoft Surface Pro 9 13-inch Core i5 8GB 256GB", "Microsoft Surface", 88000.0, 105999.0),
        ("TAB-MS-SP10-U7", "Microsoft Surface Pro 10 for Business Intel Core Ultra 7", "Microsoft Surface", 125000.0, 149999.0)
    ]

    for code, name, brd, cost, price in tablets_data:
        pid = add_p(code, name, brd, "CAT-TAB", f"{name}, Enterprise mobility tablet for digital signatures, audits, and executive mobility", f"{code}-BASE", cost, price, serialized=True)
        add_v(pid, f"{code}-STD", f"{name} / Stylus Support / Enterprise Security", "Apple M-Series / Snapdragon / Intel", "8GB - 16GB", "128GB - 256GB", "Fast Flash", "Integrated", "10.9\" - 14.6\"", "Retina / AMOLED High-Res", "Space Grey/Silver", "Wi-Fi 6E + Bluetooth 5.3", "iPadOS / Android / Windows 11", "Tablet Slate", 12, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 12. ENTERPRISE DOCUMENT & PRINT SOLUTIONS (CAT-PRN) - 10 Products
    # --------------------------------------------------------------------------
    printers_data = [
        ("PRN-HP-E507DN", "HP LaserJet Enterprise M507dn High-Volume Monochrome", "HP Inc.", 48000.0, 57600.0),
        ("PRN-HP-E528DN", "HP LaserJet Enterprise MFP M528dn Secure Departmental MFP", "HP Inc.", 88000.0, 105600.0),
        ("PRN-HP-E555DN", "HP Color LaserJet Enterprise M555dn Workgroup Printer", "HP Inc.", 72000.0, 86400.0),
        ("PRN-HP-E578DN", "HP Color LaserJet Enterprise MFP M578dn A4 Multifunction", "HP Inc.", 125000.0, 150000.0),
        ("PRN-CAN-2625I", "Canon imageRUNNER 2625i A3 Monochrome Departmental Copier", "Canon Inc.", 135000.0, 162000.0),
        ("PRN-CAN-C3226", "Canon imageRUNNER C3226i A3 Color Multifunction Photocopier", "Canon Inc.", 195000.0, 234000.0),
        ("PRN-BRO-L6400", "Brother HL-L6400DW Enterprise Workgroup Monochrome Laser", "Brother International", 42000.0, 50400.0),
        ("PRN-BRO-L6900", "Brother MFC-L6900DW Enterprise High-Speed All-in-One MFP", "Brother International", 68000.0, 81600.0),
        ("PRN-EPS-C579R", "Epson WorkForce Pro WF-C579R Replaceable Ink Pack MFP", "Epson Commercial", 54000.0, 64800.0),
        ("PRN-CAN-LBP226", "Canon imageCLASS LBP226dw Compact Corporate Laser Printer", "Canon Inc.", 24000.0, 28800.0)
    ]

    for code, name, brd, cost, price in printers_data:
        pid = add_p(code, name, brd, "CAT-PRN", f"{name}, Enterprise departmental document printing and secure PIN release MFP", f"{code}-BASE", cost, price, serialized=True)
        add_v(pid, f"{code}-STD", f"{name} / Duplex Network / Secure Pull Print", "Internal Print SoC", "1GB - 2GB", "16GB - 32GB eMMC", "Print Spool Storage", "N/A", "N/A", "1200x1200 dpi", "White/Charcoal", "Gigabit Ethernet + USB", "PCL6 / PostScript 3", "Floor / Desktop MFP", 36, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 13. CORPORATE VIDEO COLLABORATION (CAT-COL) - 10 Products
    # --------------------------------------------------------------------------
    collab_data = [
        ("COL-LOG-RALLY", "Logitech Rally Plus Ultra-HD Modular Conference System", "Logitech Enterprise", 240000.0, 288000.0),
        ("COL-LOG-RBAR", "Logitech Rally Bar All-in-One 4K Video Bar with AI Viewfinder", "Logitech Enterprise", 280000.0, 336000.0),
        ("COL-LOG-RMINI", "Logitech Rally Bar Mini Huddle Room 4K Video Bar", "Logitech Enterprise", 195000.0, 234000.0),
        ("COL-LOG-MEET", "Logitech MeetUp 4K Ultra-Wide 120-degree ConferenceCam", "Logitech Enterprise", 62000.0, 74400.0),
        ("COL-LOG-TAP", "Logitech Tap Touch Controller for Microsoft Teams Rooms", "Logitech Enterprise", 72000.0, 86400.0),
        ("COL-PLY-X50", "Poly Studio X50 4K All-in-One Video Bar with Dual Display Support", "Poly (HP Poly)", 250000.0, 300000.0),
        ("COL-PLY-X70", "Poly Studio X70 Large Boardroom Dual 4K Sensor Video Bar", "Poly (HP Poly)", 380000.0, 456000.0),
        ("COL-PLY-TC8", "Poly TC8 8-inch High-Resolution Touch Control Pad", "Poly (HP Poly)", 58000.0, 69600.0),
        ("COL-CIS-ROOMMINI", "Cisco Webex Room Kit Mini 4K Boardroom Video Endpoint", "Cisco Systems", 295000.0, 354000.0),
        ("COL-CIS-ROOMPLS", "Cisco Webex Room Kit Plus Quad Camera Conference System", "Cisco Systems", 680000.0, 816000.0)
    ]

    for code, name, brd, cost, price in collab_data:
        pid = add_p(code, name, brd, "CAT-COL", f"{name}, Boardroom executive telepresence, beamforming microphone array and AI framing", f"{code}-BASE", cost, price, serialized=True)
        add_v(pid, f"{code}-STD", f"{name} / Teams & Zoom Certified / Table Mic Included", "DSP Acoustic Audio Processor", "4GB", "32GB", "Solid State", "Integrated 4K", "N/A", "4K Ultra HD 60fps", "Anthracite/Black", "HDMI Dual Out + Gigabit Ethernet", "Teams Rooms / Zoom Rooms / Webex", "Wall Mount / Tabletop", 24, 0.0, cost, price)

    # --------------------------------------------------------------------------
    # 14. ENTERPRISE DOCKS & ACCESSORIES (CAT-ACC) - 20 Products
    # --------------------------------------------------------------------------
    accessories_data = [
        ("ACC-DEL-WD19S", "Dell WD19S 180W High-Speed USB-C Business Docking Station", "Dell Technologies", 14500.0, 17400.0),
        ("ACC-DEL-WD22TB4", "Dell WD22TB4 Thunderbolt 4 Modular Dual 4K 180W Dock", "Dell Technologies", 22500.0, 27000.0),
        ("ACC-DEL-UD22", "Dell Universal Dock UD22 DisplayLink Quad 4K USB-C Dock", "Dell Technologies", 18500.0, 22200.0),
        ("ACC-LEN-TB4DOCK", "Lenovo ThinkPad Universal Thunderbolt 4 Dock 100W", "Lenovo Enterprise", 21000.0, 25200.0),
        ("ACC-LEN-USBCDOCK", "Lenovo ThinkPad Universal USB-C Dock v2 Triple Display", "Lenovo Enterprise", 13500.0, 16200.0),
        ("ACC-HP-TBG4", "HP Thunderbolt Dock 120W G4 with Sure Start Security", "HP Inc.", 19500.0, 23400.0),
        ("ACC-ANK-737C", "Anker 737 GaNPrime 120W Multi-Port Fast Wall Charger", "Samsung Electronics", 6500.0, 7800.0),
        ("ACC-ANK-PB24K", "Anker 737 24000mAh 140W Portable Power Bank with Display", "Samsung Electronics", 11000.0, 13200.0),
        ("ACC-LOG-MXM3S", "Logitech MX Master 3S Performance Wireless Ergonomic Mouse", "Logitech Enterprise", 7500.0, 9000.0),
        ("ACC-LOG-MXKEYS", "Logitech MX Keys S Advanced Illuminated Wireless Keyboard", "Logitech Enterprise", 8800.0, 10560.0),
        ("ACC-LOG-MK370", "Logitech MK370 Combo for Business Silent Wireless Set", "Logitech Enterprise", 2800.0, 3360.0),
        ("ACC-JAB-EV265", "Jabra Evolve2 65 MS Wireless Noise-Cancelling Headset", "Jabra GN", 15500.0, 18600.0),
        ("ACC-JAB-EV275", "Jabra Evolve2 75 Advanced ANC Hybrid Work Bluetooth Headset", "Jabra GN", 24000.0, 28800.0),
        ("ACC-JAB-EV285", "Jabra Evolve2 85 Over-Ear Executive ANC Wireless Headset", "Jabra GN", 34000.0, 40800.0),
        ("ACC-PLY-VOY4320", "Poly Voyager Focus 2 UC Stereo ANC Wireless Bluetooth Headset", "Poly (HP Poly)", 18000.0, 21600.0),
        ("ACC-LOG-BRIO", "Logitech Brio 4K Ultra HD HDR Webcam with RightLight 3", "Logitech Enterprise", 16500.0, 19800.0),
        ("ACC-DEL-ECO15", "Dell EcoLoop Pro Backpack 15-inch Ballistic Nylon", "Dell Technologies", 3200.0, 3840.0),
        ("ACC-LEN-BP15", "Lenovo ThinkPad Professional 15.6-inch Backpack", "Lenovo Enterprise", 2900.0, 3480.0),
        ("ACC-TARG-15", "Targus CityLite Pro 15.6 Security Corporate Backpack", "Dell Technologies", 3600.0, 4320.0),
        ("ACC-DEL-MS5320W", "Dell Multi-Device Wireless Mouse MS5320W Bluetooth/2.4G", "Dell Technologies", 2400.0, 2880.0)
    ]

    for code, name, brd, cost, price in accessories_data:
        pid = add_p(code, name, brd, "CAT-ACC", f"{name}, Enterprise quality workplace accessory", f"{code}-BASE", cost, price, serialized=False)
        add_v(pid, f"{code}-STD", f"{name} / Commercial Retail Pack", "Embedded Controller", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "Matte Black / Charcoal", "USB-C / Thunderbolt / Bluetooth", "Universal Plug-and-Play", "Accessory", 24, 0.0, cost, price)

    print(f"Catalog generation completed: {len(products)} products, {len(variants)} variants.")
    return products, variants

if __name__ == "__main__":
    prods, vars_list = generate_catalog()
    print(f"Total Products: {len(prods)}")
    print(f"Total Base Variants: {len(vars_list)}")
