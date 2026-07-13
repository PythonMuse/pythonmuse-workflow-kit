---
name: cash_reconciliation_skill
description: Analyze cash reconciliation files using approved inputs only. Demonstrates the PythonMuse metadata governance model.
process_area: Cash
owner: Accounting
data_classification: Confidential
ai_allowed: true
cloud_ai_allowed: false
review_required: true
article_reference: "Article 31 — Metadata Is the Label Maker"
---

# Cash Reconciliation Skill

Use this skill when helping with monthly cash reconciliation.

This skill demonstrates the PythonMuse metadata governance model: `SKILL.md` orients the AI co-pilot, `input_manifest.csv` defines approved files, Python scripts validate the rules, and the evidence folder captures the audit trail.

> This framework works in any AI co-pilot environment — Claude via GitHub Copilot in VS Code, ChatGPT, Microsoft 365 Copilot, Gemini, or any tool your organization has approved. The rules travel with the workflow, not with the tool.

---

## Workflow Rules

```yaml
approved_folders:
  - inputs
  - outputs
  - evidence

blocked_folders:
  - working
  - archive
  - raw_sensitive

allowed_statuses:
  - final
  - approved

blocked_statuses:
  - draft
  - superseded
  - do_not_use
```

---

## Instructions for the AI Co-Pilot

* Before starting, read `input_manifest.csv` and identify which files are approved for AI.
* Do not use files marked `draft`, `superseded`, or `do_not_use`.
* Do not use files from blocked folders (`working`, `archive`, `raw_sensitive`).
* Ask for clarification if a file's status is unclear or missing.
* Cite the source file name in every summary and calculation.
* Do not modify original input files.
* Save all outputs to the `outputs/` folder with a dated filename (`YYYY-MM-DD_description_v1`).
* After completing a milestone, log the run summary to `evidence/run-logs/`.

---

## Allowed Inputs

Use only files listed in `input_manifest.csv` with `approved_for_ai: yes` and `status: final` or `approved`.

Typical approved inputs:
- Bank statement export (CSV or Excel)
- General ledger cash activity export (CSV or Excel)
- Prior period reconciliation summary (for comparison — read only)

All files must be located in the `inputs/` folder.

---

## Prohibited Inputs

Never process:
- Real bank account numbers (must be masked to last 4 digits)
- SSNs or tax IDs
- Login credentials or API tokens
- Unmasked customer or vendor names in production data
- Files in blocked folders or with blocked statuses

If prohibited data is detected, stop immediately and ask for a masked or approved version.

---

## Required Working Method

1. Run `scripts/02_validate_manifest.py` before starting any analysis.
2. Confirm all files to be used are in the approved list output by the validation script.
3. Read bank statement and GL cash activity files.
4. Standardize date formats and amount signs across both sources.
5. Match transactions using the following priority:
   - Exact amount + date match
   - Exact amount within a 3 business day date tolerance
   - Partial matches flagged for review
6. Classify unmatched items:
   - **Timing differences** — likely to clear next period
   - **True exceptions** — require investigation
   - **Bank fees/charges** — match to GL fee accounts
7. Calculate reconciling balance: GL balance + timing items should equal bank balance.
8. Produce output using the format below.
9. Save all outputs to `outputs/` and log the run to `evidence/run-logs/`.

---

## Output Format

Return the result using the following structure:

### Reconciliation Summary

| Item | Amount |
|------|--------|
| Bank statement ending balance | $X |
| Less: outstanding checks | ($X) |
| Plus: deposits in transit | $X |
| Adjusted bank balance | $X |
| GL ending balance | $X |
| Difference | $X |

### Matched Transactions
- Count of matched items
- Total dollar value matched

### Unmatched Items — Bank Side

| Date | Reference | Amount | Classification |
|------|-----------|--------|----------------|
| ...  | ...       | ...    | timing / exception |

### Unmatched Items — GL Side

| Date | Reference | Amount | Classification |
|------|-----------|--------|----------------|
| ...  | ...       | ...    | timing / exception |

### Items Requiring Review
- Bullet list of true exceptions or unexplained differences

### Assumptions
- List assumptions made (date tolerance, matching logic, rounding rules, etc.)

### Reviewer Checklist
- [ ] Source files match the period under review
- [ ] Matching logic is appropriate for this entity
- [ ] All exceptions have been investigated
- [ ] Adjusted balances reconcile
- [ ] No posting action has been taken based on this output alone

---

## Style Rules

- Write in clear, factual language suitable for workpaper documentation
- State amounts precisely — do not round unless instructed
- Distinguish timing differences from true discrepancies
- Flag any items appearing in both unmatched lists at similar amounts
- Keep the summary concise and audit-ready

---

## Evidence

Save run logs to: `evidence/run-logs/`

Suggested filename: `YYYY-MM-DD_UC-001_cash-reconciliation.md`

---

## Human Review

Required reviewer: Controller, Accounting Manager, or Senior Accountant (if delegated).

All output must be reviewed and signed off before reconciling items are cleared or adjusting entries are posted. This output documents what AI found — it does not authorize any action.

---

## Related Article

[Article 31 — Metadata Is the Label Maker](https://github.com/PythonMuse/ai-ledger/blob/main/articles/31-metadata-is-the-label-maker/README.md)
