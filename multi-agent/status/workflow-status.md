# Workflow Status — Month-End Close

## Current Status

```
STATUS: NOT STARTED
Period: [fill in close month/year]
Started: [date]
Last updated: [date/time]
```

---

## Step Tracker

| Step | Agent | Status | Output File | Notes |
|------|-------|--------|-------------|-------|
| 1 — GL Validation | GL Agent | Not started | outputs/gl-validated.xlsx | |
| 2 — Bank Reconciliation | Bank Rec Agent | Not started | outputs/bank-rec-complete.xlsx | Depends on Step 1 |
| 3 — Variance Commentary | Variance Agent | Not started | outputs/variance-commentary.md | Depends on Step 1 |
| 4 — Human Review | Human | Not started | — | Depends on Steps 2 and 3 |

---

## Handoff Log

*Each agent updates this section when it completes its step.*

### GL Agent
```
Completed: [date/time]
Source rows: [count]
Output rows: [count]
GL balances: [yes / no]
Anomalies flagged: [count and description, or "none"]
```

### Bank Rec Agent
```
Completed: [date/time]
Bank ending balance: $[amount]
GL cash balance: $[amount]
Reconciling difference: $[amount]
Unmatched items: [count]
Items flagged for human review: [count and description, or "none"]
```

### Variance Agent
```
Completed: [date/time]
Accounts analyzed: [count]
Significant variances: [count]
Items flagged for human review: [count and description, or "none"]
```

---

## Open Items — Human Review Required

*Orchestrator populates this section before presenting to human reviewer.*

| # | Source | Description | Action Required |
|---|--------|-------------|-----------------|
| 1 | | | |

---

## Human Approval

```
Reviewed by: [name]
Date: [date]
Decision: [ ] Approved  [ ] Requires revision  [ ] Escalated

Notes:
[reviewer comments here]
```

---

*This is a demo status file from the [PythonMuse Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit). Adapt for your close process.*
