"""
gross_margin_charts.py
Generates three margin visualizations from gross_margin_by_order.csv.
Outputs: /outputs/chart_margin_by_order.png
         /outputs/chart_margin_by_product.png
         /outputs/chart_tensorsturtle_trend.png
"""

import csv
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'outputs')
CSV_PATH = os.path.join(OUT_DIR, 'gross_margin_by_order.csv')

PRODUCT_COLORS = {
    'TensorTurtle': '#d64040',
    'ByteBot':      '#f0a500',
    'PyPal':        '#3a7ebf',
}

def read_data():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r['total_revenue'] = float(r['total_revenue'])
        r['total_cogs']    = float(r['total_cogs'])
        r['gross_profit']  = float(r['gross_profit'])
        r['margin_pct']    = float(r['margin_pct'])
        r['order_date']    = datetime.strptime(r['order_date'], '%Y-%m-%d')
    return rows

# ── Chart 1: Margin % by order, sorted low→high, colored by product ──────────
def chart_margin_by_order(rows):
    sorted_rows = sorted(rows, key=lambda r: r['margin_pct'])
    labels  = [r['order_id'] for r in sorted_rows]
    margins = [r['margin_pct'] for r in sorted_rows]
    colors  = [PRODUCT_COLORS[r['product']] for r in sorted_rows]

    overall_avg = sum(margins) / len(margins)

    fig, ax = plt.subplots(figsize=(13, 5))
    bars = ax.bar(labels, margins, color=colors, edgecolor='white', linewidth=0.5)

    ax.axhline(overall_avg, color='#555', linestyle='--', linewidth=1.2,
               label=f'Overall avg {overall_avg:.1f}%')

    # value labels on bars
    for bar, val in zip(bars, margins):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=7.5)

    legend_patches = [mpatches.Patch(color=c, label=p)
                      for p, c in PRODUCT_COLORS.items()]
    legend_patches.append(plt.Line2D([0], [0], color='#555', linestyle='--',
                                     label=f'Avg {overall_avg:.1f}%'))
    ax.legend(handles=legend_patches, fontsize=9)

    ax.set_title('Gross Margin % by Order (sorted lowest → highest)', fontsize=13, pad=12)
    ax.set_xlabel('Order ID')
    ax.set_ylabel('Margin %')
    ax.set_ylim(0, max(margins) * 1.18)
    ax.tick_params(axis='x', labelsize=8)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'chart_margin_by_order.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f'Saved: {path}')

# ── Chart 2: Box plot — margin distribution by product ───────────────────────
def chart_margin_by_product(rows):
    products = ['PyPal', 'ByteBot', 'TensorTurtle']
    data     = [[r['margin_pct'] for r in rows if r['product'] == p] for p in products]
    colors   = [PRODUCT_COLORS[p] for p in products]

    fig, ax = plt.subplots(figsize=(7, 5))
    bp = ax.boxplot(data, patch_artist=True, widths=0.45,
                    medianprops=dict(color='white', linewidth=2))

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)

    # overlay individual points
    for i, (d, color) in enumerate(zip(data, colors), start=1):
        jitter = [i + (j % 3 - 1) * 0.08 for j in range(len(d))]
        ax.scatter(jitter, d, color=color, edgecolors='white',
                   linewidths=0.6, zorder=5, s=45)

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(products, fontsize=11)
    ax.set_ylabel('Margin %')
    ax.set_title('Gross Margin % Distribution by Product', fontsize=13, pad=12)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'chart_margin_by_product.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f'Saved: {path}')

# ── Chart 3: TensorTurtle margin over time ───────────────────────────────────
def chart_tensorturtule_trend(rows):
    tt = sorted([r for r in rows if r['product'] == 'TensorTurtle'],
                key=lambda r: r['order_date'])

    dates   = [r['order_date'] for r in tt]
    margins = [r['margin_pct'] for r in tt]
    labels  = [r['order_id'] for r in tt]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(dates, margins, color=PRODUCT_COLORS['TensorTurtle'],
            marker='o', linewidth=2, markersize=8, zorder=3)

    for d, m, lbl in zip(dates, margins, labels):
        ax.annotate(f'{lbl}\n{m:.1f}%', xy=(d, m),
                    xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=8.5,
                    color=PRODUCT_COLORS['TensorTurtle'])

    avg = sum(margins) / len(margins)
    ax.axhline(avg, color='#888', linestyle='--', linewidth=1,
               label=f'TensorTurtle avg {avg:.1f}%')

    ax.set_title('TensorTurtle — Gross Margin % Over Time', fontsize=13, pad=12)
    ax.set_ylabel('Margin %')
    ax.set_xlabel('Order Date')
    ax.set_ylim(0, max(margins) * 1.3)
    ax.legend(fontsize=9)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    fig.autofmt_xdate()
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'chart_tensorturtule_trend.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f'Saved: {path}')

if __name__ == '__main__':
    rows = read_data()
    chart_margin_by_order(rows)
    chart_margin_by_product(rows)
    chart_tensorturtule_trend(rows)
    print('All charts complete.')
