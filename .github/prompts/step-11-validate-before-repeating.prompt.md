---
name: "Step 11 - Validate Before Repeating"
description: "Demo Step 11: Run a full validation pass on Steps 1-10 and produce a dated validation report in /outputs/ covering tie-out, source trace, assumptions, rounding, chart consistency, scope leaks, and unknowns."
agent: agent
model: "Claude Sonnet 4.5 (copilot)"
---

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

> Rule: Do not proceed to Step 12 -- stop after producing this report and wait for my review and explicit approval.
> Rule: Save to /outputs/ with a dated filename per CLAUDE.md. Never overwrite.

After saving the report, print the full file path and update status_update.md.

---

**Human checklist before approving Step 12** (not for Claude -- for you):

- [ ] Open source CSVs and spot-check at least three rows against the Step 4 workpaper
- [ ] Recalculate one margin by hand and confirm it matches
- [ ] Re-sum revenue and COGS by year and tie to the Step 5 YoY table
- [ ] Pick one chart label and trace it to a row in the CSV
- [ ] Read every "NOT EXPLICITLY APPROVED" assumption -- approve, reject, or fix each one
- [ ] Confirm output filenames are dated and nothing in /data/raw/ was modified
- [ ] For real engagements: confirm no unmasked sensitive value appears in any output or chat transcript
- [ ] Sign off in status_update.md with your name, date, and the validation report filename
