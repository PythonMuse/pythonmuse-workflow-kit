"""
build_daily_dashboard.py
========================
PythonMuse Article 27 — AI That Runs Before You Log In
https://github.com/PythonMuse/ai-ledger/tree/main/articles/27-ai-runs-before-you-log-in

Loads yesterday's sales and service call data, calculates key metrics,
flags exceptions, and saves an interactive HTML dashboard.

Run manually:    python build_daily_dashboard.py
Run scheduled:   see run_scheduled_dashboard.py

Requirements:
    pip install pandas plotly

To upgrade from CSV to SQL later, uncomment the SQL section below
and comment out the CSV loads. See comments marked [SQL UPGRADE].
"""

import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------------------------
# Paths — relative to this script so it runs from any location
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "daily_dashboard"
LOG_DIR = OUTPUT_DIR / "logs"

# ---------------------------------------------------------------------------
# Logging — every run leaves a trace
# ---------------------------------------------------------------------------
LOG_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOG_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger(__name__)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load sales and service call data from CSV files."""

    # [CSV VERSION] — use these lines when working with sample data
    candidates = [
        DATA_DIR / "daily_sales.csv",
        RAW_DATA_DIR / "daily_sales.csv",
    ]
    sales_path = next((path for path in candidates if path.exists()), None)

    service_candidates = [
        DATA_DIR / "service_calls.csv",
        RAW_DATA_DIR / "service_calls.csv",
    ]
    service_path = next((path for path in service_candidates if path.exists()), None)

    if sales_path is None or service_path is None:
        raise FileNotFoundError(
            f"Data files not found in {DATA_DIR} or {RAW_DATA_DIR}. "
            "Make sure daily_sales.csv and service_calls.csv are present."
        )

    sales_df = pd.read_csv(sales_path, parse_dates=["date"])
    service_df = pd.read_csv(service_path, parse_dates=["date"])

    # [SQL UPGRADE] — when ready to connect to your database, replace the
    # CSV loads above with these lines (install sqlalchemy and your driver first):
    #
    # from sqlalchemy import create_engine
    # engine = create_engine(
    #     "mssql+pyodbc://YOUR_SERVER/YOUR_DATABASE"
    #     "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    # )
    # yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    # sales_df = pd.read_sql(
    #     f"SELECT * FROM daily_sales WHERE sale_date = '{yesterday}'", engine
    # )
    # service_df = pd.read_sql(
    #     f"SELECT * FROM service_calls WHERE call_date = '{yesterday}'", engine
    # )

    log.info(f"Loaded {len(sales_df)} sales rows and {len(service_df)} service rows.")
    return sales_df, service_df


def analyze(sales_df: pd.DataFrame, service_df: pd.DataFrame, report_date: pd.Timestamp):
    """Calculate summary metrics for the report date."""

    daily_sales = sales_df[sales_df["date"] == report_date].copy()
    daily_svc   = service_df[service_df["date"] == report_date].copy()

    if daily_sales.empty:
        log.warning(f"No sales data found for {report_date.date()}. Check your data.")
        return None, None, None, None, ""

    # Revenue and margin
    daily_sales["gross_margin_pct"] = (
        (daily_sales["revenue"] - daily_sales["cost"]) / daily_sales["revenue"] * 100
    ).round(1)
    daily_sales["vs_target_pct"] = (
        (daily_sales["revenue"] - daily_sales["target_revenue"]) / daily_sales["target_revenue"] * 100
    ).round(1)

    # Branch-level rollup
    branch_summary = (
        daily_sales.groupby("branch")
        .agg(revenue=("revenue", "sum"), cost=("cost", "sum"), target=("target_revenue", "sum"))
        .reset_index()
    )
    branch_summary["margin_pct"] = (
        (branch_summary["revenue"] - branch_summary["cost"]) / branch_summary["revenue"] * 100
    ).round(1)
    branch_summary["vs_target_pct"] = (
        (branch_summary["revenue"] - branch_summary["target"]) / branch_summary["target"] * 100
    ).round(1)

    # Category rollup
    category_summary = (
        daily_sales.groupby("category")
        .agg(revenue=("revenue", "sum"), cost=("cost", "sum"))
        .reset_index()
    )
    category_summary["margin_pct"] = (
        (category_summary["revenue"] - category_summary["cost"]) / category_summary["revenue"] * 100
    ).round(1)

    # Exception flags: branches > 15% below target
    exceptions = daily_sales[daily_sales["vs_target_pct"] < -15.0][
        ["branch", "customer", "category", "revenue", "target_revenue", "vs_target_pct"]
    ].copy()

    # Auto-generated commentary
    total_rev    = branch_summary["revenue"].sum()
    total_target = branch_summary["target"].sum()
    overall_pct  = (total_rev - total_target) / total_target * 100
    top_branch   = branch_summary.loc[branch_summary["revenue"].idxmax(), "branch"]
    open_emerg   = daily_svc[
        (daily_svc["priority"].isin(["High", "Critical"])) &
        (daily_svc["status"] != "Completed")
    ]

    direction = "above" if overall_pct >= 0 else "below"
    commentary = (
        f"Total revenue of **${total_rev:,.0f}** was **{direction} target by "
        f"{abs(overall_pct):.1f}%**, led by the **{top_branch}** branch. "
    )
    if not open_emerg.empty:
        commentary += (
            f"⚠️ {len(open_emerg)} high-priority service call(s) remain open — "
            "review before end of day."
        )
    else:
        commentary += "All high-priority service calls resolved."

    log.info(f"Analysis complete. {len(exceptions)} exception(s) flagged.")
    return branch_summary, category_summary, exceptions, daily_svc, commentary


def build_dashboard(
    report_date: pd.Timestamp,
    branch_summary: pd.DataFrame,
    category_summary: pd.DataFrame,
    exceptions: pd.DataFrame,
    service_df: pd.DataFrame,
    commentary: str,
) -> go.Figure:
    """Assemble the interactive Plotly dashboard."""

    date_str = report_date.strftime("%B %d, %Y")

    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=[
            "Revenue vs. Target by Branch",
            "Gross Margin % by Branch",
            "Revenue by Category",
            "Service Call Volume by Priority",
            "Exception Items",
            "",
        ],
        specs=[
            [{"type": "bar"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "pie"}],
            [{"type": "table", "colspan": 2}, None],
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
    )

    # Chart 1: Revenue vs Target
    fig.add_trace(go.Bar(name="Revenue", x=branch_summary["branch"],
                         y=branch_summary["revenue"], marker_color="#2E86AB"), row=1, col=1)
    fig.add_trace(go.Bar(name="Target", x=branch_summary["branch"],
                         y=branch_summary["target"], marker_color="#A8DADC"), row=1, col=1)

    # Chart 2: Margin %
    fig.add_trace(go.Bar(name="Margin %", x=branch_summary["branch"],
                         y=branch_summary["margin_pct"], marker_color="#E63946",
                         showlegend=False), row=1, col=2)

    # Chart 3: Revenue by Category
    fig.add_trace(go.Bar(name="Category Revenue", x=category_summary["category"],
                         y=category_summary["revenue"], marker_color="#457B9D",
                         showlegend=False), row=2, col=1)

    # Chart 4: Service call priority pie
    if not service_df.empty:
        svc_priority = service_df["priority"].value_counts().reset_index()
        svc_priority.columns = ["priority", "count"]
        fig.add_trace(go.Pie(labels=svc_priority["priority"], values=svc_priority["count"],
                             name="Service Calls"), row=2, col=2)

    # Chart 5: Exceptions table
    if exceptions.empty:
        exc_display = pd.DataFrame([{"Message": "✅ No exception items for this date."}])
        header_vals = ["Message"]
        cell_vals   = [exc_display["Message"].tolist()]
    else:
        header_vals = ["Branch", "Customer", "Category", "Revenue", "Target", "vs Target %"]
        cell_vals   = [
            exceptions["branch"].tolist(),
            exceptions["customer"].tolist(),
            exceptions["category"].tolist(),
            [f"${v:,.0f}" for v in exceptions["revenue"]],
            [f"${v:,.0f}" for v in exceptions["target_revenue"]],
            [f"{v:+.1f}%" for v in exceptions["vs_target_pct"]],
        ]

    fig.add_trace(
        go.Table(
            header=dict(values=header_vals, fill_color="#E63946", font=dict(color="white")),
            cells=dict(values=cell_vals, fill_color="#f9f9f9"),
        ),
        row=3, col=1,
    )

    fig.update_layout(
        title={
            "text": (
                f"<b>Daily Dashboard — {date_str}</b><br>"
                f"<sup>{commentary}</sup>"
            ),
            "x": 0.05,
            "font": {"size": 16},
        },
        barmode="group",
        height=1000,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def save_dashboard(fig: go.Figure, report_date: pd.Timestamp) -> Path:
    """Save the dashboard as a self-contained HTML file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"dashboard_{report_date.strftime('%Y%m%d')}.html"
    fig.write_html(str(out_path), full_html=True, include_plotlyjs="cdn")
    log.info(f"Dashboard saved: {out_path}")
    return out_path


def main():
    log.info("=" * 60)
    log.info("Daily Dashboard — Build Starting")
    log.info("=" * 60)

    sales_df, service_df = load_data()

    # Use the most recent date in the data (in production: yesterday)
    report_date = sales_df["date"].max()
    log.info(f"Report date: {report_date.date()}")

    branch_summary, category_summary, exceptions, daily_svc, commentary = analyze(
        sales_df, service_df, report_date
    )

    if branch_summary is None:
        log.error("No data to display. Exiting.")
        sys.exit(1)

    fig = build_dashboard(
        report_date, branch_summary, category_summary, exceptions, daily_svc, commentary
    )
    out_path = save_dashboard(fig, report_date)

    log.info("Build complete.")
    log.info(f"Open your dashboard: {out_path}")
    print(f"\n✅  Dashboard ready: {out_path}\n")


if __name__ == "__main__":
    main()
