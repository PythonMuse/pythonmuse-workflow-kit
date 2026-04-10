"""
Convert a PDF to structured Markdown.

Uses pdfplumber for text and table extraction. Tables are converted to
Markdown tables; remaining text is preserved as paragraphs.

Usage:
    python src/pdf_to_markdown.py data/raw/sample_bank_statement.pdf

Output:
    data/processed/sample_bank_statement.md

Requirements:
    pip install pdfplumber
"""

import os
import sys

try:
    import pdfplumber
except ImportError:
    print("pdfplumber is required. Install it with:")
    print("  pip install pdfplumber")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PROCESSED_DIR = os.path.join(PROJECT_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)


def table_to_markdown(table):
    """Convert a pdfplumber table (list of lists) to a Markdown table."""
    if not table or not table[0]:
        return ""

    # Clean cells
    clean = []
    for row in table:
        clean.append([str(cell).strip() if cell else "" for cell in row])

    # Build markdown
    header = clean[0]
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in clean[1:]:
        # Pad row if shorter than header
        padded = row + [""] * (len(header) - len(row))
        lines.append("| " + " | ".join(padded[:len(header)]) + " |")

    return "\n".join(lines)


def convert(pdf_path):
    """Convert a PDF file to Markdown and save to data/processed/."""
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    out_path = os.path.join(PROCESSED_DIR, f"{basename}.md")

    md_parts = [f"# {basename.replace('_', ' ').title()}\n"]
    md_parts.append(f"*Converted from: {os.path.basename(pdf_path)}*\n")

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if len(pdf.pages) > 1:
                md_parts.append(f"\n## Page {i + 1}\n")

            # Extract tables first
            tables = page.extract_tables()
            table_text_regions = set()

            for table in tables:
                md_table = table_to_markdown(table)
                if md_table:
                    md_parts.append(md_table)
                    md_parts.append("")
                    # Track text that belongs to tables to avoid duplication
                    for row in table:
                        for cell in row:
                            if cell:
                                table_text_regions.add(cell.strip())

            # Extract remaining text (non-table)
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    stripped = line.strip()
                    if stripped and stripped not in table_text_regions:
                        md_parts.append(stripped)
                md_parts.append("")

    markdown = "\n".join(md_parts)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"[OK] Converted: {pdf_path}")
    print(f"     Output:    {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/pdf_to_markdown.py <path-to-pdf>")
        print("Example: python src/pdf_to_markdown.py data/raw/sample_bank_statement.pdf")
        sys.exit(1)

    convert(sys.argv[1])
