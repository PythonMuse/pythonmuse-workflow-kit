---
name: loop-review
description: Review an AI-generated workflow file (YAML or similar) before it is run — translating each section into plain accounting language and confirming controls are in place
---

# Approved Use Case

Use Case ID: UC-006

---

# Purpose

This skill helps accounting and finance professionals review AI-generated workflow files before approving them for execution.

When AI generates a loop or automated workflow, it produces YAML configuration files, Python scripts, and supporting files. This skill walks through those files and answers five governance questions in plain English:

1. What starts this process?
2. What does it do, and in what order?
3. What systems and folders can it access?
4. What happens if something fails?
5. Does a human review the output before it is distributed?

This skill is **explanatory and governance-focused only**.

It does **not** run the workflow, approve it for production, or certify that it is error-free.

Human sign-off is required before any workflow is run on production data.

---

# Allowed Inputs

- YAML workflow files (.yaml or .yml)
- Python scripts that a workflow calls (.py files in /src/)
- Workflow documentation files (.md)
- Files located in the approved project directory

---

# Prohibited Inputs

Never review workflow files that:

- connect to production databases without explicit IT authorization
- include hardcoded credentials, API keys, or passwords
- send data to external systems not approved by IT governance
- access unmasked PII, employee IDs, or bank account numbers

If prohibited content is detected, stop and ask for a sanitized version.

---

# Required Working Method

1. Confirm the workflow file is from an approved project directory.
2. Open the YAML file and locate each of the five governance sections.
3. For each section, produce a plain-English description using the output format below.
4. Flag any section that is missing, ambiguous, or potentially unsafe.
5. Produce a sign-off checklist for the reviewer.
6. Do not run the workflow.

---

# Output Format

## Workflow Review Summary

**File:** `workflow-name.yaml`
**Reviewed by:** AI (loop-review skill, UC-006)
**Requires human sign-off:** Yes

---

## What This Workflow Does

One paragraph, plain English. What business process does this automate? What accounting task does it support?

---

## Governance Review

| Section | YAML Key | Plain-English Description | Status |
|---|---|---|---|
| Trigger | `trigger:` | What event starts this process | Review |
| Sequence | `steps:` | Steps in order, plain English | Review |
| Permissions | `permissions:` | What folders and systems it can touch | Review |
| Retry Rules | `retry:` | What happens on failure | Review |
| Human Gate | `approval:` | Whether a human must approve before distribution | Review |

---

## Trigger

**YAML:**
```yaml
trigger: [paste trigger block here]
```

**Plain English:**
This workflow starts when [describe trigger in one sentence].

**Review question:** Could this trigger fire accidentally? Could it fire more than once?

- [ ] Trigger is limited to the correct source
- [ ] Trigger cannot fire from test or external emails
- [ ] Confirmed by reviewer

---

## Sequence

**Steps in order:**

| Step | What it does |
|---|---|
| 1. `step_name` | Plain-English description |

**Review question:** Does this sequence make sense? Is notification gated after validation?

- [ ] Steps are in the correct order
- [ ] No step runs before its dependency is validated
- [ ] Confirmed by reviewer

---

## Permissions

**What this workflow can touch:**

| Area | Access Level | Notes |
|---|---|---|
| data/raw/ | Read only | Source files — must not be overwritten |
| outputs/ | Read/write | Generated files |
| evidence/ | None | Audit trail — automation must not write here |

**Review question:** Is raw data protected? Can this workflow overwrite source files?

- [ ] Raw data folders are read-only
- [ ] Scope is limited to approved folders
- [ ] Confirmed by reviewer

---

## Retry Rules

**Plain English:** If the workflow fails, it will retry [N] times with [X] second delays.

**Review question:** Could retries create duplicate outputs, double notifications, or re-run calculations on already-processed data?

- [ ] Retry logic cannot create duplicates
- [ ] Duplicate trigger protection is in place
- [ ] Confirmed by reviewer

---

## Human Gate

**Plain English:** Before outputs are distributed, a [role] must approve. If no response within [N] hours, the workflow [holds/auto-distributes].

**Review question:** Who is the approver? What happens if they are unavailable?

- [ ] Approval is required before distribution
- [ ] Timeout behavior is set to hold (not auto-distribute)
- [ ] Confirmed by reviewer

---

## Overall Sign-Off

- [ ] All five governance sections reviewed
- [ ] No prohibited data or systems accessed
- [ ] Logic matches the intended business process
- [ ] Human approver is identified and available
- [ ] Reviewer has signed off before workflow is run in production

---

# Style Rules

- Write in plain English — no YAML syntax in the summary narrative
- Use accounting vocabulary: reconciliation, approval gate, audit trail, sign-off
- Flag any missing governance section as a hard stop
- Keep the summary concise enough to attach to a workpaper

---

# Example Invocation

Use this skill when a team member has used AI to generate a workflow and needs to understand and sign off on it before running it.

Example prompt:

"Use the loop-review skill on `workflows/invoice-to-dashboard.yaml` and produce a plain-English sign-off document I can attach to my close checklist."

---

# Evidence

Save the review output to:

`evidence/run-logs/`

Suggested file naming pattern:

`YYYY-MM-DD_UC-006_loop-review_workflow-name.md`

---

# Human Review

Required reviewer:
- Controller
- Accounting Manager
- Senior Accountant (if delegated)

The review output documents what the workflow does and confirms controls are in place. It does not authorize the workflow to run. Human sign-off is required before any workflow executes on production data or as part of an audit-ready process.

---

# Related Reading

[Article 29 — The Magic Loop](https://github.com/PythonMuse/ai-ledger/tree/main/articles/29-loops-the-automation-that-feels-magical)
[Article 17 — Skills and Agents for Accountants](https://github.com/PythonMuse/ai-ledger/tree/main/articles/17-skills-and-agents-for-accountants)

**PythonMuse LLC** | pythonmuse.com
