---
name: bank-reconciliation
description: Reconcile bank statement transactions against general ledger entries and identify unmatched items
---

# Approved Use Case

Use Case ID: UC-001

---

# Purpose

This skill assists finance teams with bank reconciliation in a controlled way.

It is designed to:
- compare bank statement transactions to general ledger entries
- match transactions by amount, date, and reference
- identify unmatched items on both sides
- flag timing differences vs. true discrepancies
- produce a reconciliation summary with clear exception detail

This skill is **assistive only**.

It does **not** approve adjusting entries, clear reconciling items, or replace reviewer signoff.

---

# Allowed Inputs

Use only approved source files such as:

- bank statement export (CSV or Excel)
- general ledger detail or trial balance export
- prior period reconciliation (for comparison)
- masked or sample transaction data

All files should be located in the approved project directory (e.g., `/data/raw/`).

---

# Prohibited Inputs

Never process:

- real bank account numbers (must be masked)
- SSNs or tax IDs
- login credentials or tokens
- unmasked customer or vendor names in production data
- files outside the approved project directory

If prohibited data is detected, stop and ask for a masked or approved version.

---

# Required Working Method

1. Confirm the workflow is approved under Use Case ID UC-001.
2. Confirm all files are sample, masked, or approved internal finance data.
3. Read bank statement and GL files.
4. Standardize date formats and amount signs across both sources.
5. Match transactions using the following priority:
   - exact amount + date match
   - exact amount within a date tolerance (default: 3 business days)
   - partial matches flagged for review
6. Classify unmatched items:
   - **timing differences** (likely to clear next period)
   - **true exceptions** (require investigation)
   - **bank fees/charges** (matched to GL fee accounts)
7. Calculate reconciling balance: GL balance + timing items should equal bank balance.
8. Produce output in the format below.
9. Save all outputs to the designated evidence folder.

---

# Output Format

Return the result using the following structure:

## Reconciliation Summary

| Item | Amount |
|------|--------|
| Bank statement ending balance | $X |
| Less: outstanding checks | ($X) |
| Plus: deposits in transit | $X |
| Adjusted bank balance | $X |
| GL ending balance | $X |
| Difference | $X |

## Matched Transactions

- count of matched items
- total dollar value matched

## Unmatched Items -- Bank Side

| Date | Reference | Amount | Classification |
|------|-----------|--------|---------------|
| ... | ... | ... | timing / exception |

## Unmatched Items -- GL Side

| Date | Reference | Amount | Classification |
|------|-----------|--------|---------------|
| ... | ... | ... | timing / exception |

## Items Requiring Review
- bullet list of true exceptions or unexplained differences

## Assumptions
- list assumptions made (date tolerance, matching logic, etc.)

## Reviewer Checklist
- confirm source files match the period under review
- confirm matching logic is appropriate
- confirm all exceptions have been investigated
- confirm adjusted balances reconcile
- confirm no posting action has been taken

---

# Style Rules

- Write in clear, factual language suitable for workpaper documentation
- State amounts precisely (do not round unless instructed)
- Distinguish timing differences from true discrepancies
- Flag any items that appear in both unmatched lists at similar amounts
- Keep the summary concise and audit-ready

---

# Example Invocation

Use this skill when the user provides bank and GL files and asks for help reconciling.

Example prompt:

"Use the bank-reconciliation skill on the bank statement and GL export in /data/raw. Match transactions, identify exceptions, and save the reconciliation to /outputs."

---

# Evidence

Save outputs to:

`evidence/run-logs/`

Suggested file naming pattern:

`YYYY-MM-DD_UC-001_bank-reconciliation.md`

---

# Human Review

Required reviewer:
- Controller
- Accounting Manager
- Senior Accountant (if delegated)

All output must be reviewed and signed off before reconciling items are cleared or adjusting entries are posted. This output documents what AI found -- it does not authorize any action.
