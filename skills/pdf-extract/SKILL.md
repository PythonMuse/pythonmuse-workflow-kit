---
name: pdf-extract
description: Convert PDF documents to structured Markdown and extract data fields using a repeatable, token-efficient workflow
---

# Approved Use Case

Use Case ID: UC-004

---

# Purpose

This skill helps finance teams extract structured data from PDF documents without wasting tokens on repeated interpretation.

It is designed to:
- convert a PDF to structured Markdown (one-time conversion)
- mask sensitive data before AI processing
- extract defined fields from the Markdown using a consistent schema
- produce structured output (JSON or CSV)
- eliminate repeated token-heavy PDF parsing

This skill is **assistive only**.

It does **not** approve journal entries, validate extracted data against source systems, or replace reviewer signoff.

---

# Allowed Inputs

Use only approved source files such as:

- PDF documents stored in `/data/raw/`
- Markdown files converted from PDFs stored in `/data/processed/`
- prior period extractions (for comparison)
- masked or sample financial documents

All files should be located in the approved project directory.

---

# Prohibited Inputs

Never process:

- unmasked bank account numbers
- SSNs or tax IDs
- login credentials or tokens
- unmasked customer or vendor names in production data
- files outside the approved project directory

If prohibited data is detected, stop and ask for a masked or approved version.

---

# Required Working Method

1. Confirm the workflow is approved under Use Case ID UC-004.
2. Confirm the PDF has been converted to Markdown and saved in `/data/processed/`.
   - If only a PDF exists in `/data/raw/`, run conversion first using `src/pdf_to_markdown.py` or a one-time Claude conversation.
3. Confirm sensitive data has been masked in the Markdown file.
4. Read the Markdown file.
5. Extract fields according to the defined schema (see Output Format below).
6. Validate extracted data:
   - all required fields populated
   - amounts parse as numbers
   - dates parse as valid dates
7. Produce output in the format below.
8. Save all outputs to `/outputs/`.
9. Log the extraction to `evidence/run-logs/`.

---

# Output Format

Return the result using the following structure:

## Extraction Summary

| Field | Value |
|-------|-------|
| Source document | (filename) |
| Document type | (invoice / bank statement / trial balance / other) |
| Extraction date | (today) |
| Fields extracted | (count) |

## Extracted Data

For **invoices**:

```json
{
  "invoice_number": "",
  "vendor": "",
  "date": "",
  "due_date": "",
  "total": 0.00,
  "line_items": [
    {
      "description": "",
      "quantity": 0,
      "unit_price": 0.00,
      "total": 0.00
    }
  ]
}
```

For **bank statements**:

```json
{
  "account_holder": "",
  "statement_period": "",
  "opening_balance": 0.00,
  "closing_balance": 0.00,
  "transactions": [
    {
      "date": "",
      "description": "",
      "amount": 0.00,
      "balance": 0.00
    }
  ]
}
```

Adapt the schema to the document type. The key principle: output should be structured, consistent, and machine-readable.

## Assumptions

- list assumptions made (field mapping, date format, currency, etc.)

## Items Requiring Review

- bullet list of ambiguous fields, unreadable sections, or values that could not be confidently extracted

## Reviewer Checklist

- confirm source PDF matches the Markdown file
- confirm sensitive data has been masked
- confirm extracted fields match the source document
- confirm output format is correct
- confirm no posting action has been taken

---

# Style Rules

- Write in clear, factual language suitable for workpaper documentation
- State amounts precisely (do not round unless instructed)
- Flag any fields that could not be confidently extracted
- Keep the summary concise and audit-ready
- Always note whether the source was a full document or a partial section

---

# Example Invocation

Use this skill when the user provides a PDF (or its Markdown conversion) and asks for structured data extraction.

Example prompt:

"Use the pdf-extract skill on the bank statement Markdown in /data/processed/sample_bank_statement.md. Extract all transactions and save the output to /outputs/."

---

# Evidence

Save outputs to:

`evidence/run-logs/`

Suggested file naming pattern:

`YYYY-MM-DD_UC-004_pdf-extract.md`

---

# Human Review

Required reviewer:
- Controller
- Accounting Manager
- Senior Accountant (if delegated)

All output must be reviewed and signed off before extracted data is used in journal entries, reconciliations, or reports. This output documents what AI extracted -- it does not authorize any action.
