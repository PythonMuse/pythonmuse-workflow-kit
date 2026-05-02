---
name: "Step 08 - Promote Charting to Skill"
description: "Demo Step 8: Convert the Step 7 chart-producing logic into a reusable skill at /skills/visualize-margin/SKILL.md following existing skill format."
agent: agent
model: "Claude Sonnet 4.5 (copilot)"
---

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

> Rule: Read the existing skills in /skills/ first to match the exact format before writing.
> Rule: A skill is the smallest unit of repeatability -- once this exists, any future session can invoke it by name.

After creating the skill, update status_update.md.
