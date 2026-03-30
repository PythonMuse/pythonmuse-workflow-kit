---
name: margin-analysis
description: Analyze gross margin and contribution margin by product, customer, or segment and identify trends requiring attention
---

# Approved Use Case

Use Case ID: UC-003

---

# Purpose

This skill assists finance teams with margin analysis in a controlled way.

It is designed to:
- calculate gross margin and contribution margin by segment (product, customer, department, or region)
- compare current period margins to prior period or budget
- identify segments with declining, negative, or anomalous margins
- rank segments by absolute margin contribution
- draft concise commentary for management review

This skill is **assistive only**.

It does **not** approve pricing changes, reclassify revenue, or replace management judgment on margin drivers.

---

# Allowed Inputs

Use only approved source files such as:

- revenue detail by segment (CSV or Excel)
- cost of goods sold or cost of revenue detail
- budget or prior period comparison files
- masked or sample transaction data
- approved product/customer master lists

All files should be located in the approved project directory (e.g., `/data/raw/`).

---

# Prohibited Inputs

Never process:

- customer SSNs, tax IDs, or bank account numbers
- proprietary pricing agreements (unless masked)
- login credentials or tokens
- unmasked customer names in production data
- files outside the approved project directory

If prohibited data is detected, stop and ask for a masked or approved version.

---

# Required Working Method

1. Confirm the workflow is approved under Use Case ID UC-003.
2. Confirm all files are sample, masked, or approved internal finance data.
3. Read revenue and cost files.
4. Align segments across revenue and cost sources (product, customer, region, etc.).
5. Calculate the following for each segment:
   - revenue
   - cost of goods sold / cost of revenue
   - gross margin (dollars and percentage)
   - contribution margin (if variable costs are provided)
6. Compare to prior period or budget:
   - margin change in dollars and percentage points
   - flag segments where margin declined by more than the materiality threshold
7. Rank segments by:
   - absolute margin contribution (largest to smallest)
   - margin percentage (highest to lowest)
   - margin change (most deteriorated to most improved)
8. Identify and flag:
   - segments with negative margins
   - segments with margins below a minimum threshold
   - revenue concentration risks (any segment greater than 20% of total)
9. Produce output in the format below.
10. Save all outputs to the designated evidence folder.

---

# Materiality Guidance

Unless the user provides a different approved threshold, apply this default drafting logic:

Flag a margin change when either is true:
- absolute margin change is greater than or equal to $25,000
- margin percentage changed by more than 3 percentage points

If the user provides an approved threshold for a specific workflow, use that instead.

---

# Output Format

Return the result using the following structure:

## Margin Analysis Summary

| Segment | Revenue | COGS | Gross Margin $ | Gross Margin % | Prior GM % | Change (pp) |
|---------|---------|------|----------------|---------------|------------|-------------|
| ... | ... | ... | ... | ... | ... | ... |
| **Total** | ... | ... | ... | ... | ... | ... |

## Top Margin Contributors
- ranked list of segments by absolute margin dollars

## Segments Requiring Attention
- segments with negative or declining margins
- segments exceeding concentration thresholds

## Period-over-Period Commentary
- concise commentary on material margin changes

## Assumptions
- list assumptions made (segment mapping, cost allocation, etc.)

## Reviewer Checklist
- confirm source files match the period under review
- confirm segment mapping is accurate
- confirm materiality threshold applied
- confirm commentary is factually accurate
- confirm no pricing or reclassification action is implied

---

# Style Rules

- Write in clear controller-friendly language
- State margins as both dollar amounts and percentages
- Distinguish mix-driven changes from rate-driven changes where possible
- Flag one-time items that distort margins
- Keep commentary concise and usable for monthly or quarterly reporting

---

# Example Invocation

Use this skill when the user provides revenue and cost data and asks for help analyzing margins.

Example prompt:

"Use the margin-analysis skill on the product revenue and COGS files in /data/raw. Compare to prior quarter, identify segments with declining margins, and save results to /outputs."

---

# Evidence

Save outputs to:

`evidence/run-logs/`

Suggested file naming pattern:

`YYYY-MM-DD_UC-003_margin-analysis.md`

---

# Human Review

Required reviewer:
- Controller
- FP&A lead
- CFO (if included in board or lender reporting)

All output must be reviewed before it is included in a management package, investor update, or pricing discussion. This output documents what AI found -- it does not authorize any action.
