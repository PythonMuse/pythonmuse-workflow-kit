---
name: Daily Sales & Service Dashboard
description: >
  Loads daily sales and service call data from CSV (or SQL), calculates
  revenue vs. target, gross margin, and exception flags, then generates
  an interactive HTML dashboard using Plotly. Designed to run on a
  scheduled trigger before business hours.
article: https://github.com/PythonMuse/ai-ledger/tree/main/articles/18-ai-runs-before-you-log-in
author: PythonMuse LLC
---

# SKILL: Scheduled Daily Dashboard

## Purpose

Build a daily sales and service dashboard that runs automatically on a schedule
and saves an interactive HTML file before the team arrives for work.

## When to Use This Skill

- You have daily sales or transaction data that needs to be reviewed each morning
- You want to move a recurring Excel report into an automated workflow
- You are learning how scheduled AI workflows fit into accounting processes

## Data Requirements

Place your data files in `/data/raw/` before running:

| File | Required Columns |
|------|-----------------|
| `daily_sales.csv` | `date`, `branch`, `rep_name`, `customer`, `category`, `revenue`, `cost`, `target_revenue` |
| `service_calls.csv` | `date`, `ticket_id`, `branch`, `technician`, `customer`, `call_type`, `priority`, `duration_hours`, `status` |

Sample files are included in `/data/raw/`. Replace with your own data (masked or anonymized).

## Instructions

### Step 1 — Set Up

```
pip install pandas plotly
```

### Step 2 — Run the Dashboard Builder

```
python src/build_daily_dashboard.py
```

Output lands in `outputs/daily_dashboard/dashboard_YYYYMMDD.html`.

Open the HTML file in any browser. No server required.

### Step 3 — Review the Output

Before sharing, verify:
- [ ] Revenue totals match your source system for the report date
- [ ] Exception flags are accurate (not false positives)
- [ ] Commentary makes sense in context
- [ ] No data from wrong date range appears

### Step 4 — Schedule It

**Windows Task Scheduler (simplest):**
1. Task Scheduler → Create Basic Task
2. Trigger: Daily, 7:00 AM, Mon–Fri
3. Action: `python` → `C:\your\path\src\run_scheduled_dashboard.py`

**GitHub Actions:**
See `.github/workflows/` in the workflow kit for a ready-to-use YAML template.

### Step 5 — Upgrade to SQL (when ready)

In `src/build_daily_dashboard.py`, find the `[SQL UPGRADE]` comments.
Uncomment the SQL lines and update your connection string.

Supported databases: SQL Server, PostgreSQL, MySQL, SQLite.

## Governance Checklist

Before using this in a production environment:

- [ ] Calculation logic reviewed and approved by a senior accountant
- [ ] Tested against at least two weeks of historical data
- [ ] Exception thresholds documented (current default: 15% below target)
- [ ] Run logs retained in `outputs/daily_dashboard/logs/`
- [ ] Human review process defined before results are shared externally
- [ ] Data masking applied if working with real customer names or amounts

## Customization

Common modifications (ask AI to help with each):

- Change the exception threshold from 15% to a number that fits your business
- Add a new chart (e.g., top 10 customers by revenue)
- Add an email step using Python's `smtplib` or `sendgrid`
- Add a second report date comparison (yesterday vs. same day last week)
- Export a PDF summary alongside the HTML dashboard

## Prompts That Built This

These are the actual prompts used to generate the scripts in this skill:

> "Build a Python script that loads a CSV of daily sales data with columns: date, branch, rep_name, customer, category, revenue, cost, target_revenue. Calculate revenue by branch vs. target, gross margin %, and flag any branches more than 15% below target. Save an interactive HTML dashboard using Plotly. Add comments showing where I could replace the CSV load with a SQL query later."

> "Now add a second data source: service_calls.csv with columns: date, ticket_id, branch, technician, customer, call_type, priority, duration_hours, status. Add a pie chart of call volume by priority and flag any open high-priority calls."

> "Wrap this in a run_scheduled_dashboard.py file with error handling and logging. Add comments showing how to schedule this with Windows Task Scheduler, GitHub Actions, and Linux cron."

---

*Part of the [PythonMuse Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit)*
*Article: [AI That Runs Before You Log In](https://github.com/PythonMuse/ai-ledger/tree/main/articles/18-ai-runs-before-you-log-in)*
