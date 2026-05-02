# Status Update

## Last Updated

2026-04-24

## Current State

| Item | Status |
|------|--------|
| Data loaded | Complete |
| Analysis run | Complete |
| Output saved | Complete |
| Review | Pending |

## What Was Done

- Read and summarized two raw CSV files: `pythonmuse_orders_revenue.csv` (20 orders, Jan 2024–Nov 2025) and `pythonmuse_orders_costs.csv` (20 orders, matching IDs)
- Joined files on `order_id` — all 20 orders matched, no gaps
- Calculated `gross_profit = total_revenue - total_cogs` and `margin_pct = gross_profit / total_revenue × 100`
- Sorted results by margin % ascending (lowest first)
- Wrote script to `/src/gross_margin_analysis.py`
- Saved CSV and markdown outputs to `/outputs/`
- Generated three charts (bar by order, box by product, TensorTurtle trend) via `/src/gross_margin_charts.py`
- Verified all 20 rows and totals tie exactly to source files ($0.00 diff on revenue and COGS)
- Exported full joined dataset to Excel (`/src/export_excel.py`) with live formulas, currency formatting, and conditional color scale on margin %
- Created reusable data readiness checker (`/src/run_analysis.py`): validates raw CSVs, reports monthly coverage, flags missing months and unmatched cost records, recommends analysis period; supports `--month YYYY-MM` flag for targeted checks

## Output Files

| File | Location | Description |
|------|----------|-------------|
| gross_margin_by_order.csv | /outputs/ | Joined order data with gross profit and margin %, sorted by lowest margin first |
| gross_margin_by_order.md | /outputs/ | Same data in markdown table format with totals summary |
| chart_margin_by_order.png | /outputs/ | Bar chart — margin % per order, colored by product |
| chart_margin_by_product.png | /outputs/ | Box plot — margin % distribution by product |
| chart_tensorturtule_trend.png | /outputs/ | TensorTurtle margin % over time |
| gross_margin_analysis.xlsx | /outputs/ | Full joined dataset with live Excel formulas, formatting, and conditional color scale |
| run_analysis.py | /src/ | Reusable readiness checker — validates raw CSVs, reports coverage by month, flags gaps; run with optional --month YYYY-MM |

## Issues or Questions

- `plan.md` is an unfilled template — no formal objective, period, or reviewer is defined. Results are based on verbal instructions from the user only.

## Next Steps

- [ ] Reviewer approval of gross margin output
- [ ] Drill into TensorTurtle COGS: material vs. labour split for 2024 vs. 2025
- [ ] Confirm whether unit pricing has kept pace with cost increases
- [ ] Determine if TensorTurtle volume growth is intentional given deteriorating margin
