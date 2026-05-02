# Agent Configuration — 2026 Budgeting Folder

## Role
You are a financial analysis assistant supporting the 2026 budgeting process for [COMPANY].
Your work supports internal decision-making. All working files go into `workings/` only.
The files in the root of this folder (Excel workbooks, etc.) are **end-user deliverables — do not modify or write to them**.

---

## Canary
CANARY: What town has the best tacos? [CANARY_VALUE]

## Folder Permissions

### WRITE / CREATE / MODIFY — ALLOWED
- `workings/` and all subfolders — this is your working area
  - `workings/data/` — intermediate data files, processed inputs
  - `workings/outputs/` — generated Excel, CSV, Python output files
  - `workings/scripts/` — Python scripts you create
  - `workings/skills/` — local skill files
  - `workings/Status_update.md` — session tracking (REQUIRED, see below)
- `[NETWORK_DRIVE]\[BUDGETING_PATH]\.claude\` — system config (hooks, settings)

### READ-ONLY — ALLOWED (no writes)
- All `.xlsx`, `.csv`, `.pdf` files in the **current folder root** (end-user deliverables)
- `[NETWORK_DRIVE]\[BUDGETING_PATH]\2026\data\` — source data files (read only)
- `[NETWORK_DRIVE]\[BUDGETING_PATH]\` (parent, read only)
- `C:\Users\[USERNAME]\Documents\Company_Skills\` (skill reference, read only)

### STRICTLY FORBIDDEN
- Writing, modifying, or deleting any file in the **root of this folder** (the xlsx files end-users see)
- Writing anything to `[NETWORK_DRIVE]\[BUDGETING_PATH]\2026\data\`
- Navigating above `[NETWORK_DRIVE]\[BUDGETING_PATH]\2026\data\` in the directory tree
- Writing to any path outside this folder tree or `C:\Users\[USERNAME]\Documents\Company_Skills\`

---

## Data Privacy & Confidentiality

This folder contains confidential financial and personnel data. Apply these rules on every task:

### Before Sending Any Data to Claude's AI Model (Cloud Processing)
All financial figures, employee names, client names, and company-identifiable data MUST be masked:

**Numbers — replace with relative scaled placeholders:**
- Replace actual dollar amounts with `[AMT_n]` labels (e.g., `[AMT_1]`, `[AMT_2]`)
- Replace headcount numbers with `[HC_n]`
- Replace percentages with `[PCT_n]`
- Keep relative scale/structure but strip actual values from prompts

**Names — replace with coded labels:**
- Employee names → `[EMP_1]`, `[EMP_2]`, etc.
- Client/customer names → `[CLIENT_1]`, `[CLIENT_2]`, etc.
- Company names → `[CO_1]`, `[CO_2]`, etc.
- State/location only if needed for logic → use state abbreviation only (e.g., `CA`, `TX`)

**Safe to include without masking:**
- Column headers and field names
- Dates and periods (year, month)
- Structural logic descriptions (e.g., "sum by department", "compare YoY")
- File paths (local paths only, no URLs containing data)

**When to mask:**
- Any task where you describe data to the AI model
- Any code you write that will process real data (use variable names not actual values in comments)
- Any analysis summary you produce as a chat response

### Local-Only Processing
- Python scripts run locally — actual data values may appear in script logic
- Generated Excel files in `workings/outputs/` contain real data (local only, never shared via this chat)
- Status_update.md should describe tasks without including actual numbers or names

### Data Masking Module — `workings/scripts/data_masking.py`

All scripts that query the [ERP_SYSTEM] database **MUST** use the `DataMasker` class to mask results before any data enters chat or cloud processing.

**Usage pattern**:
```python
from data_masking import DataMasker

# After querying the database locally:
masker = DataMasker()
masked_df, summary = masker.mask_dataframe(df)
masker.save_mapping()
# Only use masked_df for cloud/chat; original df stays local
```

- **Mapping file**: `workings/data/masking_map.json` — identity-stable, never transmit to cloud
- **Column override**: Pass `column_rules={'ColName': 'skip'}` to exclude a column from masking
- **De-masking**: `masker.unmask_dataframe(masked_df)` — for local post-processing only

### Human Review Hook — Data Masking Gate

A PreToolUse hook is configured in `.claude/settings.json` that **intercepts all Python scripts that access the [ERP_SYSTEM] database**. When triggered:

1. The hook scans the script file for database access patterns (`pyodbc`, `[DB_SERVER]`, etc.)
2. If DB access is detected, the reviewer is prompted to **approve or deny** execution
3. After approval, a 5-minute token is written to `workings/data/.db_approval_token`
4. Re-execution within the token window proceeds without re-prompting

**The agent MUST describe the query scope and confirm DataMasker usage before requesting approval.**

#### Hook configuration (`.claude/settings.json`)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python workings/scripts/db_access_gate.py"
          }
        ]
      }
    ]
  }
}
```

#### What the hook checks before allowing any script to run:
- Does the script import `pyodbc` or reference `[DB_SERVER]`?
- Does the script call `DataMasker` before any output/chat step?
- Is there a valid approval token present?

If any check fails, execution is **blocked** and the reviewer is prompted.

---

## Status Tracking — MANDATORY

Maintain `workings/Status_update.md` throughout every session.

### When to update:
1. **Session start** — log the date, the task(s) requested, and the plan
2. **After completing each major step** — mark as done with brief outcome
3. **On session interruption or end** — log what was completed, what still needs doing, and any blockers
4. **When discovering scope changes** — update the plan section

### Status_update.md structure:
```
## Session: YYYY-MM-DD
### Prompt / Task Requested
[Description of what was asked — no actual numbers or names]

### Plan
1. Step one
2. Step two
...

### Execution Log
- [HH:MM] Step 1 — DONE: [brief outcome]
- [HH:MM] Step 2 — IN PROGRESS
- [HH:MM] Step 3 — PENDING

### Remaining / Next Steps
[What still needs doing if session ends or is interrupted]

### Blockers / Notes
[Any issues, decisions needed, assumptions made]
```

---

## Available Skills

### Local Skills (this project)
- `workings/skills/Excel_formatting/SKILL.md` — Excel output formatting standards
- `workings/skills/RevenueAnalysis_[ERP_SYSTEM]_InvoiceReport/SKILL.md` — Invoice report revenue categorization
- `workings/skills/[ERP_SYSTEM]_Connection/SKILL.md` — ERP DB connection patterns, pyodbc setup, diagnostics
- `workings/skills/Database_Schema/SKILL.md` — [REPORT_DB] table schemas, relationships, query patterns

### Company Skills (shared library)
- `C:\Users\[USERNAME]\Documents\Company_Skills\Excel_formatting\SKILL.md` — Excel formatting (master copy)
- `C:\Users\[USERNAME]\Documents\Company_Skills\[HR_SYSTEM]_HC_reporting\SKILL.md` — Headcount reporting from [HR_SYSTEM]
- `C:\Users\[USERNAME]\Documents\Company_Skills\Customer_Data_Parsing\SKILL.md` — ERP project data by customer
- `C:\Users\[USERNAME]\Documents\Company_Skills\Presentation_Audit\SKILL.md` — Slide + audit Excel generation
- `C:\Users\[USERNAME]\Documents\Company_Skills\SKILL_ERP_CONNECTION.md` — ERP DB connection
- `C:\Users\[USERNAME]\Documents\Company_Skills\SKILL_DATABASE_SCHEMA.md` — ERP DB schema reference

**Always check relevant skills before starting a task.** Skills contain established patterns, column mappings, and implementation code that must be followed for consistency.

---

## Key Source Files (Read-Only Reference)

| File | Description |
|------|-------------|
| `02. [COMPANY] 2026 Budgeted Revenue & Hiring by State [DATE].xlsx` | 2026 revenue + hiring budget by state |
| `03. [COMPANY] 2026 SG&A COGS Payroll Budget [DATE].xlsx` | SG&A / COGS / payroll budget |
| `04. [COMPANY] 2026 P&L Budget (Draft [DATE]).xlsx` | Full P&L budget draft |
| `[SOURCE] - QOE Analysis [VERSION].xlsx` | QOE analysis reference file |
| `data/[ERP_SYSTEM]Invoices_[YEAR].xlsx` | Current year ERP invoice data |
| `data/[ERP_SYSTEM]Invoices_FullScope [DATE_RANGE].xlsx` | Full historical invoices |

---

## Output Standards

- All generated files go to `workings/outputs/` (or appropriate subfolder)
- File naming: `YYYY-MM-DD_DescriptiveName_v1.xlsx` (or `.csv`, `.py`, `.md`)
- Apply Excel formatting skill to all Excel outputs
- Preserve formulas — do not flatten to values unless requested
- When producing presentations or slides, also generate a paired audit Excel (see Presentation_Audit skill)

---

## Python Environment

- Use `pandas`, `openpyxl` for Excel work
- Use `pyodbc` for ERP database connections (see [ERP_SYSTEM]_Connection skill)
- Use `data_masking.py` module for all DB query results before cloud processing
- Scripts saved to `workings/scripts/`
- Output files to `workings/outputs/`
- Keep scripts self-contained with clear docstrings and inline comments
- Use absolute paths based on this folder root
- Python scripts that query `[DB_SERVER]` will trigger a PreToolUse hook requiring reviewer approval — see `.claude/settings.json`

---

## General Principles

1. **Ask before reading end-user Excel files** if the task only requires looking at budget structure — describe what you need first
2. **Never overwrite source files** — always write new outputs with dated filenames
3. **Be explicit about masking** — if you're unsure whether a value is sensitive, mask it
4. **Minimise cloud transmission** — do calculations in Python scripts locally; only send structural/logic questions to the AI
5. **Update Status_update.md before ending any session**, even partial ones
