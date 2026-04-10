"""
Generate a synthetic bank statement PDF for demo purposes.

Creates a realistic-looking bank statement with:
- Account holder (synthetic name)
- Statement period
- Opening and closing balances
- Transaction table with dates, descriptions, amounts, and running balances

All data is synthetic -- no real PII. Safe to commit.

Usage:
    python src/generate_sample_pdf.py

Output:
    data/raw/sample_bank_statement.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(PROJECT_DIR, "data", "raw")
os.makedirs(OUT_DIR, exist_ok=True)

OUT_PATH = os.path.join(OUT_DIR, "sample_bank_statement.pdf")


def generate():
    doc = SimpleDocTemplate(
        OUT_PATH,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "BankTitle",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "BankSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=12,
    )
    normal = styles["Normal"]

    elements = []

    # Header
    elements.append(Paragraph("Acme National Bank", title_style))
    elements.append(Paragraph("123 Finance Street, Anytown, ST 00000", subtitle_style))
    elements.append(Spacer(1, 12))

    # Account info
    account_info = [
        ["Account Holder:", "Customer_001 (Maple Creek Consulting LLC)"],
        ["Account Number:", "XXXX-XXXX-5678"],
        ["Statement Period:", "March 1, 2026 -- March 31, 2026"],
        ["Opening Balance:", "$24,150.00"],
        ["Closing Balance:", "$27,385.50"],
    ]
    info_table = Table(account_info, colWidths=[2 * inch, 4.5 * inch])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 18))

    # Transaction table
    elements.append(Paragraph("Transaction Detail", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    transactions = [
        ["Date", "Description", "Amount", "Balance"],
        ["03/01", "Opening Balance", "", "$24,150.00"],
        ["03/02", "ACH Deposit -- Client_A Invoice #1042", "$5,200.00", "$29,350.00"],
        ["03/03", "Check #4501 -- Vendor_B Office Supplies", "($325.00)", "$29,025.00"],
        ["03/05", "Wire Transfer -- Client_C Retainer", "$3,500.00", "$32,525.00"],
        ["03/07", "ACH Payment -- Vendor_D Software License", "($1,200.00)", "$31,325.00"],
        ["03/10", "POS Purchase -- Office Depot", "($89.50)", "$31,235.50"],
        ["03/12", "ACH Deposit -- Client_E Project Payment", "$4,750.00", "$35,985.50"],
        ["03/14", "Check #4502 -- Vendor_F Consulting Fees", "($2,500.00)", "$33,485.50"],
        ["03/15", "Monthly Service Fee", "($25.00)", "$33,460.50"],
        ["03/17", "ACH Payment -- Vendor_G Insurance Premium", "($875.00)", "$32,585.50"],
        ["03/19", "Wire Transfer -- Client_H Milestone Payment", "$6,300.00", "$38,885.50"],
        ["03/21", "Check #4503 -- Vendor_J Equipment Lease", "($1,500.00)", "$37,385.50"],
        ["03/23", "ACH Payment -- Payroll Processing", "($8,250.00)", "$29,135.50"],
        ["03/25", "ACH Deposit -- Client_K Final Payment", "$2,100.00", "$31,235.50"],
        ["03/27", "POS Purchase -- Staples", "($45.00)", "$31,190.50"],
        ["03/28", "Wire Transfer -- Client_A Invoice #1043", "$3,800.00", "$34,990.50"],
        ["03/29", "ACH Payment -- Vendor_L Cloud Hosting", "($450.00)", "$34,540.50"],
        ["03/30", "Check #4504 -- Vendor_M Legal Services", "($5,200.00)", "$29,340.50"],
        ["03/31", "Interest Earned", "$45.00", "$29,385.50"],
        ["03/31", "ACH Payment -- Vendor_N Marketing", "($2,000.00)", "$27,385.50"],
    ]

    tx_table = Table(
        transactions,
        colWidths=[0.8 * inch, 3.5 * inch, 1.3 * inch, 1.3 * inch],
    )
    tx_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003144")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        # Body
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (2, 0), (3, -1), "RIGHT"),
        # Alternating rows
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
        # Grid
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.HexColor("#003144")),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.grey),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(tx_table)
    elements.append(Spacer(1, 18))

    # Footer
    elements.append(Paragraph(
        "This is a synthetic bank statement generated for demonstration purposes. "
        "All names, account numbers, and transactions are fictional.",
        ParagraphStyle("Footer", parent=normal, fontSize=8, textColor=colors.grey),
    ))

    doc.build(elements)
    print(f"[OK] Generated: {OUT_PATH}")


if __name__ == "__main__":
    generate()
