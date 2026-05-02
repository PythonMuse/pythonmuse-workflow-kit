---
name: "Step 12 - Convert to Repeatable Script"
description: "Demo Step 12: Convert the validated analysis into a single production Python script in /src/ with CONFIG block, HUMAN INPUT NEEDED markers, input validation, run summary, audit log, dry-run flag, and a paired RUNBOOK.md."
agent: agent
model: "Claude Sonnet 4.5 (copilot)"
---

Take the analysis performed in Steps 1-11 and convert it into a single,
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

> Rule: Run the script once on the existing CSVs after writing it and confirm the totals match the chat-based analysis from Steps 2-6 before declaring it complete.
> Rule: Save to /src/ and /outputs/ only per CLAUDE.md. Update status_update.md when done.
