---
name: "Step 04 - Export to Excel"
description: "Demo Step 4: Export the full joined dataset with calculations to a dated Excel file in /outputs/ for manual review."
agent: agent
model: "Claude Sonnet 4.5 (copilot)"
---

Export the full joined dataset with all calculations to an Excel file
in /outputs/ using the dated filename pattern from CLAUDE.md.
Include a header row identifying preparer, date prepared, and source files.

> Rule: Save to /outputs/ only. Use a dated filename. Never overwrite an existing file.
> Rule: Do not modify anything in /data/raw/.

After saving, print the full file path and row count so I can tie out.
Update status_update.md.
