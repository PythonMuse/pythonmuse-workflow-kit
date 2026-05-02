"""
gross_margin_analysis.py
Joins revenue and cost data, calculates gross profit and margin %, sorted by lowest margin first.
Output: /outputs/gross_margin_by_order.csv and /outputs/gross_margin_by_order.md
"""

import csv
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')

REVENUE_FILE = os.path.join(RAW_DIR, 'pythonmuse_orders_revenue.csv')
COSTS_FILE   = os.path.join(RAW_DIR, 'pythonmuse_orders_costs.csv')
OUT_CSV      = os.path.join(OUT_DIR, 'gross_margin_by_order.csv')
OUT_MD       = os.path.join(OUT_DIR, 'gross_margin_by_order.md')

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def main():
    revenue_rows = read_csv(REVENUE_FILE)
    costs_rows   = read_csv(COSTS_FILE)

    costs_by_id = {r['order_id']: r for r in costs_rows}

    results = []
    unmatched = []

    for rev in revenue_rows:
        oid = rev['order_id']
        cost = costs_by_id.get(oid)
        if cost is None:
            unmatched.append(oid)
            continue

        total_revenue = float(rev['total_revenue'])
        total_cogs    = float(cost['total_cogs'])
        gross_profit  = total_revenue - total_cogs
        margin_pct    = round((gross_profit / total_revenue) * 100, 2) if total_revenue else None

        results.append({
            'order_id':      oid,
            'order_date':    rev['order_date'],
            'product':       rev['product'],
            'salesperson':   rev['salesperson'],
            'total_revenue': total_revenue,
            'total_cogs':    total_cogs,
            'gross_profit':  gross_profit,
            'margin_pct':    margin_pct,
        })

    if unmatched:
        print(f"WARNING: {len(unmatched)} revenue order(s) had no matching cost record: {unmatched}")

    results.sort(key=lambda r: r['margin_pct'])

    # CSV output
    fieldnames = ['order_id', 'order_date', 'product', 'salesperson',
                  'total_revenue', 'total_cogs', 'gross_profit', 'margin_pct']
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Markdown output
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('# Gross Margin by Order\n\n')
        f.write(f'**Period:** Jan 2024 – Nov 2025  \n')
        f.write(f'**Orders:** {len(results)}  \n')
        f.write(f'**Generated:** 2026-04-13  \n\n')
        if unmatched:
            f.write(f'> WARNING: {len(unmatched)} unmatched order(s): {unmatched}\n\n')

        f.write('| Order ID | Date | Product | Salesperson | Revenue | COGS | Gross Profit | Margin % |\n')
        f.write('|----------|------|---------|-------------|--------:|-----:|-------------:|---------:|\n')
        for r in results:
            f.write(
                f"| {r['order_id']} | {r['order_date']} | {r['product']} | {r['salesperson']} "
                f"| ${r['total_revenue']:,.0f} | ${r['total_cogs']:,.0f} "
                f"| ${r['gross_profit']:,.0f} | {r['margin_pct']}% |\n"
            )

        total_rev  = sum(r['total_revenue'] for r in results)
        total_cogs = sum(r['total_cogs']    for r in results)
        total_gp   = total_rev - total_cogs
        total_mgn  = round((total_gp / total_rev) * 100, 2) if total_rev else 0

        f.write(f'\n**Total Revenue:** ${total_rev:,.0f}  \n')
        f.write(f'**Total COGS:** ${total_cogs:,.0f}  \n')
        f.write(f'**Total Gross Profit:** ${total_gp:,.0f}  \n')
        f.write(f'**Overall Margin:** {total_mgn}%  \n')

    print(f"Done. {len(results)} orders processed.")
    print(f"CSV:      {OUT_CSV}")
    print(f"Markdown: {OUT_MD}")

if __name__ == '__main__':
    main()
