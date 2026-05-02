# Demo Prompts -- AI Co-Pilot for Accounting

A guided, copy-paste demo that mirrors the worked example in
[Article 01: AI Co-Pilot for Accounting](https://github.com/PythonMuse/ai-ledger/tree/main/articles/01-ai-copilot-for-accounting).

You will use the two CSVs already shipped in this kit:

- `data/raw/pythonmuse_orders_revenue.csv`
- `data/raw/pythonmuse_orders_costs.csv`

## How to use this file

1. Open this folder in VS Code and start a Copilot Chat session with **Claude** selected.
2. Run the prompts **in order**, one at a time. Each builds on the last.
3. Claude will propose a plan first per the rules in [CLAUDE.md](../CLAUDE.md) -- review, then approve.
4. After Step 10 you'll have a CFO-ready story. Step 11 validates it. Step 12 turns it into a **repeatable script**.

> Every step assumes Claude follows the project rules in `CLAUDE.md`: propose before executing, save outputs to `/outputs/` with dated filenames, update `status_update.md` after each milestone.

---

## Before You Start -- Real-World Safety Note

This demo uses **fictional sample data** (CodeCritters Inc.). The prompts below are written for that case and are intentionally short.

**With real client data, you must prompt differently.** Before running this flow on anything sensitive:

- **Mask first, prompt second.** Replace names, account numbers, tax IDs, vendor and employee names, and any other identifiers with the placeholder patterns in [CLAUDE.md](../CLAUDE.md) (`[CLIENT_1]`, `[ACCT_1]`, `[EMP_1]`, ...). Keep the mapping key local. Never send the unmasked file to the model.
- **Confirm where the data is going.** Cloud models process whatever you paste. If your engagement does not allow cloud processing, do not run the demo on real data -- run it on masked extracts only, or use a locally hosted model.
- **State materiality up front.** Real prompts should specify the engagement's materiality threshold instead of letting the model assume one. Add: *"Use a materiality threshold of $X. Do not flag or suppress items based on any other threshold."*
- **Lock the period.** Real prompts should include the exact period under review and reject any inference. Add: *"The period under review is YYYY-MM-DD to YYYY-MM-DD. Do not include data outside this window."*
- **Forbid silent assumptions.** Real prompts should add: *"Do not assume account mappings, classifications, or business rules. Stop and ask if unclear."*
- **Demand traceability.** Real prompts should add: *"Every number in the output must be traceable to a source file, tab, and cell range."*
- **Be explicit about outputs.** Real prompts should specify the deliverable format and whether it leaves the workspace. Add: *"Save outputs to /outputs/ only. Do not paste figures into chat unless masked."*

The demo prompts in this file are deliberately stripped down so the flow is readable. In production, layer these guardrails into every prompt -- or move them into `plan.md` so they apply to the whole session.

---

## Step 1 -- Orient

**Purpose:** Get a structural read of the data before any math.

```text
Read the two CSV files in data/raw/ and summarize what we're working with --
time period, products, salespeople, vendors, and how the files relate.
```

> Note: Claude will propose a read-only plan first per `CLAUDE.md`.

**Validate:** Confirm the row counts and date range match what you see when you open the files manually.

---

## Step 2 -- Margin Analysis

**Purpose:** Find the orders that are bleeding margin.

```text
Join the revenue and cost data on order_id.
Calculate gross profit and margin percentage.
Sort by lowest margin first and flag anything below 20%.
```

> Note: Ask Claude to confirm the materiality / flag threshold before running -- `CLAUDE.md` forbids assumed thresholds.

**Validate:** Recalculate one row by hand. Margin = (Revenue - Cost) / Revenue.

---

## Step 3 -- Validate the Math

**Purpose:** Trust but verify. This is where accountants stay accountants.

```text
Show the exact formulas used for gross profit and margin.
Confirm totals tie back to the source files (sum of detail = header).
List any rounding differences >= $1.
```

> Note: This step is required before any number leaves the workspace.

---

## Step 4 -- Export for Manual Review

**Purpose:** Put the joined dataset into a workbook you can spot-check.

```text
Export the full joined dataset with all calculations to an Excel file
in /outputs/ using the dated filename pattern from CLAUDE.md.
Include a header row identifying preparer, date prepared, and source files.
```

> Note: Claude must save to `/outputs/` only -- never overwrite existing files.

---

## Step 5 -- Year-over-Year Compression Check

**Purpose:** Surface the story revenue alone hides.

```text
Compare 2024 vs 2025: total revenue, total COGS, gross profit, and
gross margin percentage. Is margin compressing? Show the deltas in
both dollars and percentage points.
```

**Validate:** Sum revenue by year directly in the source file and tie to Claude's totals.

---

## Step 6 -- Salesperson and Vendor Patterns

**Purpose:** Move from "what" to "who" and "where."

```text
Three things, in order:
1. Rank salespeople by gross profit and margin %. Flag concentration risk
   for anyone above 30% of total revenue.
2. Compare 2024 vs 2025 average material cost per vendor. Show YoY % change.
3. Calculate labor hours per unit by year. Did production efficiency change?
```

**Validate:** Claude should reference specific columns it used. If it can't, ask it to show its work.

---

## Step 7 -- Visualize the Story

**Purpose:** Turn the numbers from Steps 2, 5, and 6 into the same five charts the article uses. A picture catches a pattern faster than a table.

```text
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
```

> Note: Claude should propose a single Python script to produce all five charts so the work is reproducible -- not five ad-hoc renderings.

**Validate:** Open one PNG and tie at least one labeled value back to the source CSV.

---

## Step 8 -- Promote Charting to a Skill

**Purpose:** Capture the charting work as reusable infrastructure before you forget how you got it right.

```text
Convert the chart-producing logic from Step 7 into a reusable skill at
/skills/visualize-margin/SKILL.md. Follow the format of the existing
skills in this repo (bank-reconciliation, margin-analysis, pdf-extract).

The SKILL.md must include:
- Use case and when to apply it
- Required input columns (revenue file + cost file)
- The five chart specifications, each with: purpose, x/y, sort order,
  highlight rule (e.g., red below 20%), and required labels
- Output naming convention and folder
- Validation steps the human should perform before sharing
- A short "do not" list (no silent rounding, no inferred thresholds,
  no hardcoded periods)
```

> Note: A skill is the smallest unit of repeatability. Once this exists, any future session can produce these charts on a new dataset by referencing the skill -- no need to re-derive the prompts.

**Validate:** Start a fresh chat, point Claude at the new skill, and ask it to render the five charts on the same data. The output should match Step 7.

---

## Step 9 -- Strategic Summary

**Purpose:** Produce the advisory output -- not just the bookkeeping output.

```text
Based on everything analyzed in Steps 1-6, write a 5-point executive
summary with recommended actions. Each point should cite the figure
that supports it and tie back to the source data.
```

> Note: This is a draft for human review, not a deliverable. Edit before sending.

---

## Step 10 -- Explain It Back

**Purpose:** Force the work to be reproducible and teachable.

```text
Walk me through what you did across Steps 1-9, line by line, in plain English.
Identify any place you made an assumption I did not explicitly approve.
```

> Note: Use this output as the seed for `status_update.md` and the runbook in Step 12.

---

## Step 11 -- Validate Before Repeating

**Purpose:** This is the gate. Do not script anything you cannot defend. Before turning the workflow into code, both Claude and the human must independently confirm the output is correct.

### 11a. Ask Claude to self-validate

```text
Before I convert this work into a script, run a full validation pass on
Steps 1-10 and produce a validation report saved to /outputs/ with a
dated filename. The report must answer:

1. TIE-OUT. Does the sum of detail equal the header in every table
   produced? List any difference, however small. Flag anything >= $1.
2. SOURCE TRACE. For every figure in the strategic summary (Step 9),
   cite the source file, column, and rows that produced it.
3. ASSUMPTIONS. List every assumption you made -- materiality, period,
   classification, joins, exclusions -- and mark each one as either
   APPROVED BY USER or NOT EXPLICITLY APPROVED.
4. ROUNDING. Identify any place rounding was applied. Show the rule
   used. There should be no silent rounding.
5. CHART CONSISTENCY. Confirm each chart in Step 7 uses the same totals
   confirmed in Step 3. Flag any divergence.
6. SCOPE LEAKS. List any record that was filtered in or out without
   explicit instruction.
7. UNKNOWNS. List anything you would want a human to confirm before
   trusting this for an external deliverable.

Do not proceed to scripting until I review this report and approve.
```

### 11b. Human validation checklist

Before moving to Step 12, the human (you) confirms each of the following. **Do not delegate this to the model.**

- [ ] **Open the source CSVs** and spot-check at least three rows against the joined dataset from Step 4.
- [ ] **Recalculate one margin by hand** and confirm it matches the value in the workpaper.
- [ ] **Re-sum revenue and COGS by year** in the source file and tie to the YoY table from Step 5.
- [ ] **Pick one chart label and trace it** to a row in the CSV.
- [ ] **Read every "NOT EXPLICITLY APPROVED" assumption** from 11a. Approve, reject, or fix each one. Re-run the affected step if you change anything.
- [ ] **Confirm output filenames are dated** and nothing in `/data/raw/` was modified.
- [ ] **For real engagements:** confirm no unmasked sensitive value appears in any output, log, or chat transcript.
- [ ] **Sign off in `status_update.md`** with reviewer name, date, and the validation report filename.

> If any item above fails, **do not advance to Step 12**. Fix the underlying step, regenerate, and revalidate. Repeatable code built on unvalidated logic is just faster mistakes.

---

## Step 12 -- Convert One-Time Work into a Repeatable Script

You've now done the analysis once and you trust it. This step graduates the work from
"a conversation" to "infrastructure."

```text
Take the analysis you just performed in Steps 1-11 and convert it into a single,
reusable Python script saved to /src/.

Requirements:

1. CONFIG BLOCK AT THE TOP. Put every value a human will need to change between
   runs in one clearly marked block:
       # === CONFIG: EDIT THESE BEFORE EACH RUN ===
   Include at minimum: period start/end, input file paths, output folder,
   materiality threshold, low-margin flag %, and the preparer name.
   Each variable gets a one-line comment explaining what it controls.

2. PLAIN-ENGLISH BLOCK COMMENTS. Every logical section starts with a comment
   block written for an accountant, not a developer. Explain WHAT the block
   does and WHY -- not just the code mechanics.

3. HUMAN-INPUT MARKERS. Anywhere a judgment call lives (materiality,
   classification rules, account mappings, exception handling), insert:
       # >>> HUMAN INPUT NEEDED: <what to decide>
   so a future user can find every decision point with a single search.

4. INPUT VALIDATION. Before doing any work, the script must:
   - Confirm the input files exist and are readable
   - Check that expected columns are present and dtypes match
   - Refuse to run and print a clear error if anything is off

5. RUN SUMMARY. At the end, print:
   - Rows in, rows out
   - Total revenue, total COGS, gross profit, margin %
   - Full path of every file written
   so the human can tie out without opening the outputs.

6. AUDIT LOG. Also write /outputs/<YYYY-MM-DD>_run-log.md capturing:
   inputs used, outputs written, row counts, totals, and the config values
   in effect for this run.

7. SAFE TO RE-RUN. Use dated filenames per CLAUDE.md. Never overwrite.
   Support a --dry-run flag that validates inputs and prints what WOULD be
   written, without writing anything.

8. NO HIDDEN MAGIC. No silent rounding, no assumed thresholds, no implicit
   account mappings. Every transformation must be traceable to a line of code
   the human can read.

After writing the script, also produce /src/<script_name>_RUNBOOK.md with:
prerequisites, how to run, how to validate the output, what each CONFIG
value means, and what to do when the script fails.
```

> Note: Read the script back and run it once on the existing CSVs to prove parity with the chat-based analysis before relying on it.

---

## Beyond the Script -- Maturity Ladder

Once you have a working script, here are additional ways to harden the workflow.
Pick the next one that solves your real pain, not all at once.

| # | Move | Prompt to Claude |
|---|------|-----------------|
| 1 | **Promote to a Skill** | "Convert the logic in `/src/<script>.py` into a reusable skill at `/skills/<name>/SKILL.md` following the format of the existing skills in this repo." |
| 2 | **Pin the prompt** | "Save the working prompt sequence from this session to `docs/prompts/<name>.md` so future sessions can replay it." |
| 3 | **Externalize config** | "Move the CONFIG block out of the script into `config.yaml`. Update the script to load from YAML so non-coders can edit settings without touching Python." |
| 4 | **Add a smoke test** | "Generate a smoke test that runs the script against last month's approved outputs and prints a diff of totals. Fail loudly on any difference > $1." |
| 5 | **CLI wrapper** | "Wrap the script with argparse so I can run `python -m src.<script> --period 2025-Q4 --raw <path>`. Document the flags in the runbook." |
| 6 | **Write the runbook** | "Generate `RUNBOOK.md` for this script: prerequisites, how to run, how to validate, what each config value means, and what to do when it fails." |
| 7 | **Schema contract** | "Add a schema check that fails loudly if next month's input file has new columns, missing columns, or changed dtypes." |
| 8 | **Golden output** | "Save the current approved output as `/evidence/golden/<date>_<name>/`. Add a check that future runs diff against it and report differences." |

> The goal is the same one named in the article: move from spreadsheet operator to automation architect -- one repeatable workflow at a time.

---

## Where this maps in the article

| Demo Step | Article Section |
|-----------|----------------|
| 1 | The First Question: Orientation |
| 2 | Margin Analysis |
| 3 | Before You Trust It: Validate |
| 4 | Exporting Without Abandoning Excel |
| 5 | The Number That Should Worry the CEO |
| 6 | Sales & Vendor Patterns |
| 7 | Figures 1-5 (visuals folder in the article repo) |
| 8 | The Real Skill Being Built (skill capture) |
| 9 | Asking the Strategic Question |
| 10 | The Real Skill Being Built (narrative) |
| 11 | Before You Trust It: Validate (gate before automating) |
| 12 | When to Stop Chatting and Start Building / Build Your Own Agent |
