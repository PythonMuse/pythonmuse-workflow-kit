"""
run_analysis.py
Checks raw CSV files and reports data readiness by month.
Usage:
    python src/run_analysis.py              # check all months
    python src/run_analysis.py --month 2025-11  # check a specific month
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from datetime import date, datetime

# Ensure Unicode symbols print correctly on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR      = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
REVENUE_FILE = os.path.join(RAW_DIR, 'pythonmuse_orders_revenue.csv')
COSTS_FILE   = os.path.join(RAW_DIR, 'pythonmuse_orders_costs.csv')

LINE = '=' * 62


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def month_range(start_ym, end_ym):
    """Yield (year, month) tuples from start_ym to end_ym inclusive."""
    y, m = start_ym
    ey, em = end_ym
    while (y, m) <= (ey, em):
        yield (y, m)
        m += 1
        if m > 12:
            m = 1
            y += 1


def fmt_month(y, m):
    return f'{y}-{m:02d}'


def check_files():
    """Verify source files exist. Return (ok, messages)."""
    issues = []
    for label, path in [('Revenue', REVENUE_FILE), ('Costs', COSTS_FILE)]:
        if not os.path.isfile(path):
            rel = os.path.relpath(path, os.path.join(os.path.dirname(__file__), '..'))
            issues.append(f'  MISSING  {rel}  — {label} file not found')
    return issues


def load_data():
    revenue_rows = read_csv(REVENUE_FILE)
    costs_rows   = read_csv(COSTS_FILE)
    costs_by_id  = {r['order_id']: r for r in costs_rows}
    return revenue_rows, costs_by_id, len(costs_rows)


def build_monthly_summary(revenue_rows, costs_by_id):
    """
    Returns:
        by_month  : {(y, m): [row, ...]}
        unmatched : [order_id, ...]
        date_range: (min_date, max_date) as (y, m) tuples
    """
    by_month  = defaultdict(list)
    unmatched = []

    for row in revenue_rows:
        d = datetime.strptime(row['order_date'], '%Y-%m-%d')
        by_month[(d.year, d.month)].append(row)
        if row['order_id'] not in costs_by_id:
            unmatched.append(row['order_id'])

    if not by_month:
        return by_month, unmatched, None

    min_ym = min(by_month)
    max_ym = max(by_month)
    return by_month, unmatched, (min_ym, max_ym)


def classify_month(ym, by_month, costs_by_id):
    """Return (status_char, orders, revenue, matched, total) for a month."""
    rows = by_month.get(ym, [])
    if not rows:
        return ('x', 0, 0.0, 0, 0)

    total   = len(rows)
    matched = sum(1 for r in rows if r['order_id'] in costs_by_id)
    revenue = sum(float(r['total_revenue']) for r in rows)

    if matched == total:
        status = 'ok'
    elif matched == 0:
        status = 'warn'
    else:
        status = 'partial'

    return (status, total, revenue, matched, total)


def find_recommended(by_month, costs_by_id, date_range):
    """Return the most recent fully-ready (y, m) or None."""
    if not date_range:
        return None
    start_ym, end_ym = date_range
    best = None
    for ym in month_range(start_ym, end_ym):
        status, total, revenue, matched, _ = classify_month(ym, by_month, costs_by_id)
        if status == 'ok':
            best = ym
    return best


def print_report(revenue_rows, costs_by_id, num_cost_rows, target_month=None):
    today = date.today().isoformat()

    print(LINE)
    print(f' PythonMuse Workflow \u2014 Data Readiness Check')
    print(f' Run date: {today}')
    print(LINE)

    # --- source files ---
    rev_rel  = os.path.relpath(REVENUE_FILE, os.path.join(os.path.dirname(__file__), '..'))
    cost_rel = os.path.relpath(COSTS_FILE,   os.path.join(os.path.dirname(__file__), '..'))
    print()
    print('Source files')
    print(f'  \u2713  {rev_rel:<50} ({len(revenue_rows)} orders)')
    print(f'  \u2713  {cost_rel:<50} ({num_cost_rows} rows)')

    by_month, unmatched, date_range = build_monthly_summary(revenue_rows, costs_by_id)

    if not date_range:
        print()
        print('  No data found in revenue file.')
        print(LINE)
        return

    start_ym, end_ym = date_range
    all_months = list(month_range(start_ym, end_ym))

    # --- if --month supplied, report only that month ---
    if target_month:
        try:
            ty, tm = int(target_month[:4]), int(target_month[5:7])
        except (ValueError, IndexError):
            print(f'\n  ERROR: --month must be in YYYY-MM format (got "{target_month}")')
            print(LINE)
            sys.exit(1)

        ym = (ty, tm)
        status, total, revenue, matched, _ = classify_month(ym, by_month, costs_by_id)

        print()
        print(f'Month requested: {target_month}')
        print()
        if status == 'ok':
            print(f'  \u2713  {target_month} is READY')
            print(f'     Orders:      {total}')
            print(f'     Revenue:     ${revenue:,.0f}')
            print(f'     Cost match:  {matched}/{total}')
            print()
            print('Next steps')
            print(f'  \u2192 Run full analysis:  python src/gross_margin_analysis.py')
            print(f'  \u2192 Generate charts:    python src/gross_margin_charts.py')
        elif status == 'x':
            print(f'  \u2717  {target_month} has NO data')
            print()
            print('Action required')
            print(f'  \u2022 Add revenue orders to {rev_rel}  with order_date in {target_month}')
            print(f'  \u2022 Add matching cost rows to {cost_rel}  for the same order_ids')
        else:
            print(f'  \u26a0  {target_month} is PARTIAL ({matched}/{total} orders have cost records)')
            print(f'     Revenue:  ${revenue:,.0f}')
            print()
            missing_ids = [r['order_id'] for r in by_month[ym] if r['order_id'] not in costs_by_id]
            print('Action required')
            print(f'  \u2022 Add cost rows to {cost_rel}  for order_id(s): {", ".join(missing_ids)}')

        print(LINE)
        return

    # --- full monthly coverage table ---
    ok_months      = []
    gap_months     = []
    partial_months = []

    print()
    print('Monthly coverage')
    for ym in all_months:
        ym_str = fmt_month(*ym)
        status, total, revenue, matched, _ = classify_month(ym, by_month, costs_by_id)

        if status == 'ok':
            ok_months.append(ym)
            print(f'  {ym_str}  \u2713  {total} order{"s" if total != 1 else ""}   '
                  f'revenue ${revenue:>8,.0f}   cost match: {matched}/{total}')
        elif status == 'x':
            gap_months.append(ym)
            print(f'  {ym_str}  \u2717  No revenue data')
        elif status in ('warn', 'partial'):
            partial_months.append(ym)
            print(f'  {ym_str}  \u26a0  {total} order{"s" if total != 1 else ""}   '
                  f'revenue ${revenue:>8,.0f}   cost match: {matched}/{total}  (PARTIAL)')

    # --- summary ---
    total_months = len(all_months)
    recommended  = find_recommended(by_month, costs_by_id, date_range)

    print()
    print('Summary')
    print(f'  Months with data:   {len(ok_months) + len(partial_months)} of {total_months}')
    print(f'  Unmatched orders:   {len(unmatched)}')
    if gap_months:
        gap_strs = ', '.join(fmt_month(*ym) for ym in gap_months)
        print(f'  Gaps in data:       {len(gap_months)} month{"s" if len(gap_months) != 1 else ""} ({gap_strs})')
    else:
        print(f'  Gaps in data:       none')

    print()
    if recommended:
        print(f'Recommended analysis period:  {fmt_month(*recommended)}  (most recent complete month)')
    else:
        print('Recommended analysis period:  none — no fully matched month found')

    print()
    print('Next steps')
    print(f'  \u2192 To check a specific month:  python src/run_analysis.py --month YYYY-MM')
    print(f'  \u2192 To run full analysis:        python src/gross_margin_analysis.py')
    print(f'  \u2192 To generate charts:          python src/gross_margin_charts.py')

    # --- action required ---
    action_items = []
    if gap_months:
        gap_strs = ', '.join(fmt_month(*ym) for ym in gap_months)
        action_items.append(
            f'Add revenue orders to {rev_rel} for: {gap_strs}'
        )
        action_items.append(
            f'Add matching cost rows to {cost_rel} for the same periods'
        )
    if partial_months:
        for ym in partial_months:
            missing_ids = [r['order_id'] for r in by_month[ym] if r['order_id'] not in costs_by_id]
            action_items.append(
                f'{fmt_month(*ym)}: add cost rows for order_id(s): {", ".join(missing_ids)}'
            )
    if unmatched:
        action_items.append(
            f'Revenue orders with no cost record at all: {", ".join(unmatched)}'
        )

    if action_items:
        print()
        print('Action required')
        for item in action_items:
            print(f'  \u2022 {item}')

    print(LINE)


def main():
    parser = argparse.ArgumentParser(
        description='Check raw CSV data readiness for gross margin analysis.'
    )
    parser.add_argument(
        '--month', metavar='YYYY-MM',
        help='Check readiness for a specific month only'
    )
    args = parser.parse_args()

    # file presence check
    issues = check_files()
    if issues:
        print(LINE)
        print(' PythonMuse Workflow \u2014 Data Readiness Check')
        print(LINE)
        print()
        print('ERROR: Required source files are missing:')
        for msg in issues:
            print(msg)
        print()
        print('Please add the files to data/raw/ and re-run.')
        print(LINE)
        sys.exit(1)

    revenue_rows, costs_by_id, num_cost_rows = load_data()
    print_report(revenue_rows, costs_by_id, num_cost_rows, target_month=args.month)


if __name__ == '__main__':
    main()
