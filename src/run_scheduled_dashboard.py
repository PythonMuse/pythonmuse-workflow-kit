"""
run_scheduled_dashboard.py
===========================
PythonMuse Article 27 — AI That Runs Before You Log In
https://github.com/PythonMuse/ai-ledger/tree/main/articles/27-ai-runs-before-you-log-in

Wrapper script for scheduled execution of the daily dashboard.
Configure this file as the entry point in your task scheduler.

SCHEDULING OPTIONS
------------------
1. Windows Task Scheduler (simplest for most accountants)
   - Open: Task Scheduler → Create Basic Task
   - Trigger: Daily, 7:00 AM, weekdays (Mon–Fri)
   - Action: Start a program
     - Program:   python
     - Arguments: "C:\\path\\to\\run_scheduled_dashboard.py"
   - Settings: Run whether user is logged on or not

2. GitHub Actions (if your project is in a GitHub repo)

   .github/workflows/daily_dashboard.yml:

   name: Daily Dashboard
   on:
     schedule:
       - cron: "0 11 * * 1-5"   # 7 AM ET = 11 AM UTC (adjust for your timezone)
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with: { python-version: "3.12" }
         - run: pip install pandas plotly
         - run: python run_scheduled_dashboard.py

3. Linux / Mac cron (if running on a server)
   Add to crontab with:  crontab -e
   Entry:  0 7 * * 1-5  /usr/bin/python3 /path/to/run_scheduled_dashboard.py

CALLOUT — Other Ways to Trigger This Workflow
----------------------------------------------
Time triggers are just one option. Future articles will cover:

- Email received  → watch inbox with a Python mail listener or Power Automate
- File dropped    → watchdog library monitors a folder and fires on new file
- API event       → webhook triggers the script when ERP posts data
- Agent loop      → AI agent checks a condition every hour and runs if threshold met
- Month-end step  → workflow orchestrator (Prefect, Airflow) runs as part of close checklist

Each of these is its own article. For now: pick a time and let it run.
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import from the scripts folder
sys.path.insert(0, str(Path(__file__).parent))

from build_daily_dashboard import load_data, analyze, build_dashboard, save_dashboard, log


def main():
    log.info("Scheduled run triggered at %s", datetime.now().isoformat())
    try:
        sales_df, service_df = load_data()
        report_date = sales_df["date"].max()
        branch_summary, category_summary, exceptions, daily_svc, commentary = analyze(
            sales_df, service_df, report_date
        )
        if branch_summary is None:
            log.error("No data available. Scheduled run aborted.")
            sys.exit(1)
        fig = build_dashboard(
            report_date, branch_summary, category_summary, exceptions, daily_svc, commentary
        )
        out_path = save_dashboard(fig, report_date)
        log.info("Scheduled run complete. Dashboard: %s", out_path)
    except Exception as exc:
        log.exception("Scheduled run failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
