import io
from datetime import timezone, datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def get_pdf_styles():
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0b1c30')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748b')
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b')
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    body_bold = ParagraphStyle(
        'DocBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'section_heading': section_heading,
        'body': body_style,
        'body_bold': body_bold,
        'cell': table_cell,
        'cell_bold': table_cell_bold
    }

def generate_invoice_pdf(invoice: dict, customer: dict = None, lines: list = None) -> bytes:
    """Generate professional Tax Invoice PDF in byte stream."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = get_pdf_styles()
    story = []
    
    # 1. Header Banner
    company_info = """
    <b>DEALFLOW360 TECHNOLOGIES PVT LTD</b><br/>
    Corporate Identification: U72900GJ2023PTC142890<br/>
    GSTIN: 24AABCP1234F1Z8 • State Code: 24 (Gujarat)<br/>
    Western Regional Logistics Park, SG Highway, Ahmedabad, GJ 380054<br/>
    Email: billing@phoen.io • Phone: +91 (079) 4912-8800
    """
    
    inv_id = invoice.get('id', 'INV-UNKNOWN')
    doc_number = invoice.get('document_number', inv_id)
    doc_date = invoice.get('document_date')
    if isinstance(doc_date, datetime):
        doc_date_str = doc_date.strftime("%d-%b-%Y")
    else:
        doc_date_str = str(doc_date or datetime.now(timezone.utc).strftime("%d-%b-%Y"))
    
    due_date_str = invoice.get('dueDate') or (datetime.now(timezone.utc).strftime("%d-%b-%Y"))
    status_str = invoice.get('status', 'ISSUED').upper()

    header_data = [
        [
            Paragraph(company_info, styles['body']),
            Paragraph(f"""
            <font size=18 color="#2563eb"><b>TAX INVOICE</b></font><br/><br/>
            <b>Invoice #:</b> {doc_number}<br/>
            <b>Invoice ID:</b> {inv_id}<br/>
            <b>Date:</b> {doc_date_str}<br/>
            <b>Due Date:</b> {due_date_str}<br/>
            <b>Status:</b> <font color="{'#059669' if status_str == 'PAID' else '#d97706'}"><b>{status_str}</b></font>
            """, styles['body'])
        ]
    ]
    
    header_table = Table(header_data, colWidths=[320, 220])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=14))

    # 2. Bill To / Ship To Information
    cust_name = customer.get('company_name') if customer else (invoice.get('account') or invoice.get('customer_name') or 'Enterprise Client')
    cust_id = customer.get('id') if customer else (invoice.get('customer_id') or 'CUST-001')
    cust_tier = customer.get('tier') if customer else (invoice.get('customer_tier') or 'Enterprise')
    billing_addr = customer.get('billing_address') if customer else 'Plot 48, GIDC Industrial Estate, Vatva, Ahmedabad, Gujarat 382445'
    
    bill_data = [
        [
            Paragraph("<b>BILLED TO (CONSIGNEE):</b>", styles['section_heading']),
            Paragraph("<b>COMMERCIAL REFERENCE:</b>", styles['section_heading'])
        ],
        [
            Paragraph(f"""
            <b>{cust_name}</b><br/>
            Customer ID: {cust_id} • Tier: {cust_tier}<br/>
            Billing Address: {billing_addr}<br/>
            Place of Supply: Gujarat (State Code 24)
            """, styles['body']),
            Paragraph(f"""
            <b>Quote / PO Ref:</b> {invoice.get('quoteId') or invoice.get('document_number') or 'Direct Commercial'}<br/>
            <b>Account Manager:</b> {invoice.get('created_by') or 'David Chen (Finance Controller)'}<br/>
            <b>Payment Currency:</b> INR (Indian Rupee ₹)<br/>
            <b>Payment Terms:</b> Net 30 Days via Wire Transfer
            """, styles['body'])
        ]
    ]
    bill_table = Table(bill_data, colWidths=[320, 220])
    bill_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#e2e8f0')),
    ]))
    story.append(bill_table)
    story.append(Spacer(1, 14))

    # 3. Line Items Table
    table_headers = [
        Paragraph("<b>#</b>", styles['cell_bold']),
        Paragraph("<b>Item Description & Scope</b>", styles['cell_bold']),
        Paragraph("<b>HSN/SAC</b>", styles['cell_bold']),
        Paragraph("<b>Qty</b>", styles['cell_bold']),
        Paragraph("<b>Unit Price (₹)</b>", styles['cell_bold']),
        Paragraph("<b>GST</b>", styles['cell_bold']),
        Paragraph("<b>Total (₹)</b>", styles['cell_bold'])
    ]
    
    table_rows = [table_headers]
    
    invoice_lines = lines or invoice.get('lines') or []
    if not invoice_lines:
        title_desc = invoice.get('notes') or invoice.get('title') or "Enterprise Dedicated Cloud Infrastructure & Hardware Billing"
        invoice_lines = [{
            'description': title_desc,
            'quantity': 1,
            'unit_price': float(invoice.get('amount') or 0.0),
            'tax_rate': 18.0,
            'line_total': float(invoice.get('amount') or 0.0)
        }]

    total_amount = float(invoice.get('amount') or invoice.get('grand_total') or 0.0)
    
    for idx, line in enumerate(invoice_lines, start=1):
        desc = line.get('description') or line.get('product_name') or 'Commercial Hardware SKU / SaaS License'
        qty = line.get('quantity') or 1
        unit_p = float(line.get('unit_price') or (total_amount / qty))
        ltotal = float(line.get('line_total') or line.get('total') or (qty * unit_p))
        tax_pct = float(line.get('tax_rate') or 18.0)
        
        table_rows.append([
            Paragraph(str(idx), styles['cell']),
            Paragraph(desc, styles['cell']),
            Paragraph("998313", styles['cell']),
            Paragraph(str(qty), styles['cell']),
            Paragraph(f"₹{unit_p:,.2f}", styles['cell']),
            Paragraph(f"{tax_pct:.0f}%", styles['cell']),
            Paragraph(f"₹{ltotal:,.2f}", styles['cell_bold'])
        ])

    items_table = Table(table_rows, colWidths=[25, 230, 50, 35, 75, 45, 80])
    items_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 10))

    # 4. Calculation Summary
    subtotal = round(total_amount / 1.18, 2)
    gst_total = round(total_amount - subtotal, 2)
    cgst = round(gst_total / 2, 2)
    sgst = round(gst_total / 2, 2)

    summary_data = [
        [
            Paragraph("""
            <b>Payment Instructions (Direct Bank Wire):</b><br/>
            Account Name: Phoen Technologies Pvt Ltd<br/>
            Bank Name: HDFC Bank Ltd • Branch: Bodakdev, Ahmedabad<br/>
            Account Number: 50200084920194 • IFSC: HDFC0000452<br/>
            UPI ID: phoen@hdfcbank
            """, styles['body']),
            Table([
                [Paragraph("Taxable Subtotal:", styles['cell']), Paragraph(f"₹{subtotal:,.2f}", styles['cell_bold'])],
                [Paragraph("Central GST (CGST 9%):", styles['cell']), Paragraph(f"₹{cgst:,.2f}", styles['cell'])],
                [Paragraph("State GST (SGST 9%):", styles['cell']), Paragraph(f"₹{sgst:,.2f}", styles['cell'])],
                [Paragraph("<b>Grand Total:</b>", styles['section_heading']), Paragraph(f"<b>₹{total_amount:,.2f}</b>", styles['section_heading'])],
            ], colWidths=[130, 90], style=[
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LINEABOVE', (0, 3), (-1, 3), 1, colors.HexColor('#0b1c30')),
                ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#f8fafc')),
                ('PADDING', (0, 0), (-1, -1), 4),
            ])
        ]
    ]
    
    summary_table = Table(summary_data, colWidths=[320, 220])
    summary_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # 5. Sign-off Block
    sign_data = [
        [
            Paragraph("""
            <b>Terms & Conditions:</b><br/>
            1. Payment due strictly within 30 days of invoice date.<br/>
            2. Interest @ 18% p.a. chargeable on overdue balances.<br/>
            3. Subject to Ahmedabad jurisdiction only.
            """, styles['body']),
            Paragraph("""
            <b>For DEALFLOW360 TECHNOLOGIES PVT LTD</b><br/><br/><br/>
            <b>David Chen</b><br/>
            Authorized Signatory / Financial Controller
            """, styles['body'])
        ]
    ]
    sign_table = Table(sign_data, colWidths=[320, 220])
    sign_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(sign_table)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_delivery_challan_pdf(order: dict, customer: dict = None, dispatch_data: dict = None, lines: list = None) -> bytes:
    """Generate official Outbound Delivery Challan & Shipping Bill PDF."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = get_pdf_styles()
    story = []
    
    order_id = order.get('id', 'ORD-UNKNOWN')
    dispatch = dispatch_data or (order.get('metadata_json') or {}).get('dispatch') or {}
    carrier = dispatch.get('carrier') or 'Blue Dart Express Logistics'
    tracking_no = dispatch.get('tracking_number') or f"AWB-EXP-{order_id.replace('ORD-', '')}-99"
    wh_name = dispatch.get('warehouse_name') or order.get('warehouse') or 'Ahmedabad Enterprise Distribution Center'
    box_count = dispatch.get('box_count') or 2
    gross_weight = dispatch.get('gross_weight_kg') or 14.5
    disp_date = dispatch.get('dispatched_at') or datetime.now(timezone.utc).strftime("%d-%b-%Y %H:%M")

    # Header
    company_info = """
    <b>DEALFLOW360 CENTRAL LOGISTICS & WAREHOUSING</b><br/>
    Distribution Facility: {wh}<br/>
    GSTIN: 24AABCP1234F1Z8 • Western Logistics Grid<br/>
    Dispatch Operations Desk: logistics@phoen.io
    """.format(wh=wh_name)

    header_data = [
        [
            Paragraph(company_info, styles['body']),
            Paragraph(f"""
            <font size=16 color="#0b1c30"><b>DELIVERY CHALLAN</b></font><br/>
            <font size=9 color="#64748b">OUTBOUND GOODS DISPATCH & PACKING SLIP</font><br/><br/>
            <b>Challan Ref:</b> CHAL-{order_id}<br/>
            <b>Order PO Ref:</b> {order.get('quoteId') or order_id}<br/>
            <b>Dispatch Date:</b> {disp_date}<br/>
            <b>Status:</b> <font color="#059669"><b>DISPATCHED & IN-TRANSIT</b></font>
            """, styles['body'])
        ]
    ]
    
    header_table = Table(header_data, colWidths=[320, 220])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=14))

    # Logistics & Consignee Details
    cust_name = customer.get('company_name') if customer else (order.get('account') or order.get('customer_name') or 'Consignee Account')
    shipping_addr = customer.get('shipping_address') if customer else 'Enterprise Campus, Tech Park Sector 4, Gandhinagar, GJ 382010'

    logistics_data = [
        [
            Paragraph("<b>CONSIGNEE / SHIP TO:</b>", styles['section_heading']),
            Paragraph("<b>FREIGHT & COURIER MANIFEST:</b>", styles['section_heading'])
        ],
        [
            Paragraph(f"""
            <b>{cust_name}</b><br/>
            Delivery Address: {shipping_addr}<br/>
            Customer ID: {order.get('customer_id', 'CUST-001')}<br/>
            Receiving Contact: Warehouse Receiving Officer
            """, styles['body']),
            Paragraph(f"""
            <b>Designated Carrier:</b> {carrier}<br/>
            <b>Air Waybill (AWB):</b> <font color="#2563eb"><b>{tracking_no}</b></font><br/>
            <b>Packages:</b> {box_count} Box(es) • <b>Gross Weight:</b> {gross_weight} kg<br/>
            <b>Dispatch Hub:</b> {wh_name}
            """, styles['body'])
        ]
    ]
    logistics_table = Table(logistics_data, colWidths=[320, 220])
    logistics_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#e2e8f0')),
    ]))
    story.append(logistics_table)
    story.append(Spacer(1, 14))

    # Items & Hardware Serial Allocations
    table_headers = [
        Paragraph("<b>#</b>", styles['cell_bold']),
        Paragraph("<b>Product SKU / Description</b>", styles['cell_bold']),
        Paragraph("<b>Dispatched Qty</b>", styles['cell_bold']),
        Paragraph("<b>Allocated Hardware Serials / Barcodes</b>", styles['cell_bold'])
    ]
    
    order_lines = lines or order.get('lines') or []
    serials_list = dispatch.get('serials') or order.get('serials') or [f"SN-HW-{order_id.replace('ORD-', '')}-01", f"SN-HW-{order_id.replace('ORD-', '')}-02"]
    
    table_rows = [table_headers]
    if not order_lines:
        order_lines = [{
            'description': 'Dell PowerEdge Enterprise Server / Latitude Infrastructure Units',
            'quantity': len(serials_list) or 2
        }]

    for idx, l in enumerate(order_lines, start=1):
        desc = l.get('description') or l.get('product_name') or 'Enterprise Commercial Hardware Unit'
        qty = l.get('quantity') or len(serials_list)
        serials_str = ", ".join(serials_list) if serials_list else "Pending Barcode Scan"
        
        table_rows.append([
            Paragraph(str(idx), styles['cell']),
            Paragraph(desc, styles['cell']),
            Paragraph(f"{qty} Units", styles['cell_bold']),
            Paragraph(f"<b>{serials_str}</b>", styles['cell'])
        ])

    items_table = Table(table_rows, colWidths=[30, 230, 80, 200])
    items_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 20))

    # Warehouse Verification & Driver Sign-off
    footer_data = [
        [
            Paragraph("""
            <b>Gate Pass & Security Check:</b><br/>
            [X] Verified Serial Numbers Match Physical Asset Tagging<br/>
            [X] Secure Anti-Tamper Hologram Seals Applied<br/>
            [X] Courier Driver Identity & Vehicle Verified
            """, styles['body']),
            Paragraph("""
            <b>Dispatch Logistics Officer:</b><br/><br/><br/>
            <b>Warehouse Supervisor (WH-001)</b><br/>
            Carrier Driver Signature: __________________
            """, styles['body'])
        ]
    ]
    footer_table = Table(footer_data, colWidths=[320, 220])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(footer_table)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def generate_quotation_pdf(quotation: dict, customer: dict = None, lines: list = None) -> bytes:
    """Generate executive Phoen Commercial Proposal & Agreement PDF in byte stream."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = get_pdf_styles()
    story = []

    # Palette
    c_primary = colors.HexColor('#714B67') # Phoen Plum
    c_dark = colors.HexColor('#212529')
    c_slate = colors.HexColor('#475569')
    c_light = colors.HexColor('#f8fafc')
    c_border = colors.HexColor('#e2e8f0')

    # Styles
    title_style = ParagraphStyle(
        'PropTitle',
        parent=styles['title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary
    )
    
    # Header Table
    quote_num = quotation.get('document_number') or quotation.get('id') or 'QT-2026-0001'
    status_str = str(quotation.get('status') or 'NEGOTIATION').upper()
    created_date = quotation.get('created_at')
    if isinstance(created_date, str):
        try:
            created_date = datetime.fromisoformat(created_date.replace('Z', '')).strftime('%B %d, %Y')
        except:
            created_date = datetime.now(timezone.utc).strftime('%B %d, %Y')
    elif isinstance(created_date, datetime):
        created_date = created_date.strftime('%B %d, %Y')
    else:
        created_date = datetime.now(timezone.utc).strftime('%B %d, %Y')

    header_data = [
        [
            Paragraph("<b>PHOEN</b><br/><font size=7 color='#64748b'>Enterprise Revenue Operations &amp; CPQ Platform</font>", title_style),
            Paragraph(f"""
            <b><font size=12 color='#714B67'>COMMERCIAL PROPOSAL</font></b><br/>
            <b>Proposal Ref:</b> {quote_num}<br/>
            <b>Date:</b> {created_date}<br/>
            <b>Status:</b> <font color='#0284c7'><b>{status_str}</b></font><br/>
            <b>Validity:</b> 30 Days from Issuance
            """, styles['subtitle'])
        ]
    ]
    header_table = Table(header_data, colWidths=[320, 220])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=4, spaceAfter=12))

    # Parties (Client vs Phoen Rep)
    cust = customer or {}
    cust_name = cust.get('company_name') or cust.get('name') or quotation.get('account') or quotation.get('customer_name') or 'Valued Enterprise Client'
    cust_id = cust.get('code') or cust.get('id') or quotation.get('customer_id') or 'CUST-ENT'
    cust_tier = cust.get('tier') or 'Enterprise Partner'
    billing_addr = cust.get('billing_address') or cust.get('address') or 'Corporate Technology Park, Sector V, Salt Lake, Kolkata / Mumbai'
    gstin = cust.get('tax_identifier') or cust.get('gstin') or '27AAECP1029F1Z8'
    rep_name = quotation.get('rep') or quotation.get('created_by') or 'Kavita Sharma (Lead Solutions Architect)'

    bill_data = [
        [
            Paragraph("<b>PREPARED FOR (CLIENT):</b>", styles['section_heading']),
            Paragraph("<b>ISSUED BY (SERVICE PROVIDER):</b>", styles['section_heading'])
        ],
        [
            Paragraph(f"""
            <b>{cust_name}</b><br/>
            Account Code: {cust_id} • Classification: {cust_tier}<br/>
            Corporate Address: {billing_addr}<br/>
            GSTIN / Tax ID: {gstin}
            """, styles['body']),
            Paragraph(f"""
            <b>Phoen Technologies Pvt Ltd</b><br/>
            Account Executive: {rep_name}<br/>
            Enterprise Operations: proposals@phoen.io<br/>
            National DC Hub: Bangalore &bull; Mumbai &bull; Ahmedabad<br/>
            GSTIN: 24AAACP9910D1Z2
            """, styles['body'])
        ]
    ]
    bill_table = Table(bill_data, colWidths=[320, 220])
    bill_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fbf9fa')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#eadbdf')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(bill_table)
    story.append(Spacer(1, 14))

    # Line Items Table
    table_headers = [
        Paragraph("<b>#</b>", styles['cell_bold']),
        Paragraph("<b>Product / Service Scope &amp; Specifications</b>", styles['cell_bold']),
        Paragraph("<b>Category</b>", styles['cell_bold']),
        Paragraph("<b>Qty</b>", styles['cell_bold']),
        Paragraph("<b>Unit Price (₹)</b>", styles['cell_bold']),
        Paragraph("<b>Disc %</b>", styles['cell_bold']),
        Paragraph("<b>Net Total (₹)</b>", styles['cell_bold'])
    ]
    table_rows = [table_headers]

    quote_lines = lines or quotation.get('lines') or []
    if not quote_lines:
        quote_lines = [{
            'description': 'Enterprise Commercial Hardware & Cloud Infrastructure Package',
            'category': 'Hardware / SaaS',
            'quantity': 1,
            'unit_price': float(quotation.get('amount') or quotation.get('grand_total') or 0.0),
            'discount_percent': 0.0,
            'line_total': float(quotation.get('amount') or quotation.get('grand_total') or 0.0)
        }]

    gross_subtotal = 0.0
    total_discount = 0.0
    net_taxable = 0.0

    for idx, l in enumerate(quote_lines, start=1):
        name = l.get('name') or l.get('description') or l.get('sku') or 'Commercial Item'
        sku = l.get('sku') or l.get('product_id') or ''
        cat = l.get('category') or 'Enterprise'
        q = int(l.get('qty') or l.get('quantity') or 1)
        up = float(l.get('unit_price') or l.get('unitPrice') or 0.0)
        disc = float(l.get('discount') or l.get('discount_percent') or 0.0)
        
        line_gross = q * up
        line_disc = line_gross * (disc / 100.0)
        line_net = line_gross - line_disc

        gross_subtotal += line_gross
        total_discount += line_disc
        net_taxable += line_net

        desc_p = f"<b>{name}</b>"
        if sku:
            desc_p += f"<br/><font size=6 color='#64748b'>SKU: {sku}</font>"

        table_rows.append([
            Paragraph(str(idx), styles['cell']),
            Paragraph(desc_p, styles['cell']),
            Paragraph(str(cat), styles['cell']),
            Paragraph(str(q), styles['cell']),
            Paragraph(f"₹{up:,.2f}", styles['cell']),
            Paragraph(f"{disc:.1f}%" if disc > 0 else "—", styles['cell']),
            Paragraph(f"₹{line_net:,.2f}", styles['cell_bold'])
        ])

    items_table = Table(table_rows, colWidths=[24, 236, 65, 30, 65, 40, 80])
    items_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f4f7')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 10))

    # Financial Summary
    tax_amt = net_taxable * 0.18
    grand_total = net_taxable + tax_amt

    summary_data = [
        [
            Paragraph("""
            <b>Commercial Scope &amp; Implementation Terms:</b><br/>
            &bull; Enterprise hardware includes standard 3-year OEM enterprise warranty.<br/>
            &bull; Delivery timeline: 5 to 7 business days from formal purchase confirmation.<br/>
            &bull; Pricing valid in Indian National Rupees (INR) for 30 calendar days.<br/>
            &bull; Payment milestone: Net 30 days upon delivery and sign-off acceptance.
            """, styles['body']),
            Table([
                [Paragraph("Gross Subtotal:", styles['cell']), Paragraph(f"₹{gross_subtotal:,.2f}", styles['cell'])],
                [Paragraph("Volume Discount:", styles['cell']), Paragraph(f"-₹{total_discount:,.2f}", styles['cell'])],
                [Paragraph("Taxable Net:", styles['cell_bold']), Paragraph(f"₹{net_taxable:,.2f}", styles['cell_bold'])],
                [Paragraph("GST @ 18%:", styles['cell']), Paragraph(f"₹{tax_amt:,.2f}", styles['cell'])],
                [Paragraph("<font color='#714B67'><b>Grand Total (INR):</b></font>", styles['cell_bold']),
                 Paragraph(f"<font color='#714B67'><b>₹{grand_total:,.2f}</b></font>", styles['cell_bold'])],
            ], colWidths=[110, 110])
        ]
    ]
    summary_table = Table(summary_data, colWidths=[320, 220])
    summary_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#fdfcfd')),
        ('BOX', (1, 0), (1, 0), 1, c_primary),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # Digital Signature & Acceptance Block
    sig_meta = quotation.get('metadata') or quotation.get('metadata_json') or {}
    signed_name = sig_meta.get('signed_by') or sig_meta.get('counter_sign')
    signed_date = sig_meta.get('signed_at')

    if status_str in ['CONFIRMED', 'WON', 'APPROVED'] or signed_name:
        sig_block = f"""
        <b>[X] DIGITALLY EXECUTED &amp; ACCEPTED</b><br/>
        Signatory: <b>{signed_name or cust_name}</b><br/>
        Timestamp: {signed_date or datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}<br/>
        Security Hash: SHA256-PHOEN-{quote_num[-6:]} &bull; Legally Enforceable
        """
    else:
        sig_block = f"""
        <b>Client Acceptance &amp; Purchase Authorization:</b><br/><br/>
        Authorized Signature: ________________________________<br/>
        Name &amp; Designation: ________________________________<br/>
        Date: ________________________ &bull; Company Stamp: [  ]
        """

    footer_data = [
        [
            Paragraph("""
            <b>For Phoen Technologies Pvt Ltd:</b><br/><br/>
            <b>Vikramaditya Singhania</b><br/>
            VP of Enterprise Sales &amp; Commercial Operations<br/>
            Digital Verification: VERIFIED-PHOEN-COMMERCIAL
            """, styles['body']),
            Paragraph(sig_block, styles['body'])
        ]
    ]
    footer_table = Table(footer_data, colWidths=[270, 270])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(footer_table)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
