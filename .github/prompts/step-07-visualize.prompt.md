---
name: "Step 07 - Visualize the Story"
description: "Demo Step 7: Produce the five article charts as dated PNG files in /outputs/ -- margin by order, YoY comparison, salesperson GP, revenue concentration, vendor cost inflation."
agent: agent
model: "Claude Sonnet 4.5 (copilot)"
---

Using the analyses from Steps 2, 5, and 6, produce these five charts as
PNG files in /outputs/ with dated filenames:

1. Gross margin % by order, sorted ascending. Bars below 20% in red,
   the rest in a neutral color.
2. Year-over-year comparison: revenue, COGS, gross profit, gross margin %
   for 2024 vs 2025.
3. Salesperson ranking by gross profit, with margin % shown as a label.
4. Revenue concentration by salesperson (% of total). Flag anyone
   above 30%.
5. Vendor cost inflation: average material cost per vendor, 2024 vs 2025,
   with YoY % change labeled on each bar.

Rules:
- Every chart must cite its source columns and the row count it used.
- No silent rounding. Use the same totals confirmed in Step 3.
- Save each chart with a self-describing filename and write a one-line
  caption file alongside it.

> Rule: Propose a single Python script to produce all five charts -- not five ad-hoc renderings.
> Rule: Save to /outputs/ only with dated filenames per CLAUDE.md.

After saving, print the full path of every file written. Update status_update.md.
