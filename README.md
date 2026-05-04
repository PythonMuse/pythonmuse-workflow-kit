# PythonMuse Workflow Kit

A ready-to-use project template for AI-assisted accounting workflows. Clone it, fill in your plan, drop in your data, and start working.

Built on the [PythonMuse](https://github.com/PythonMuse/ai-ledger) methodology for controlled, repeatable, and audit-ready AI workflows.

---

## Use This Template

On GitHub, click **"Use this template"** to create your own copy. Or clone it directly:

**Windows (PowerShell):**
```powershell
git clone https://github.com/PythonMuse/pythonmuse-workflow-kit.git ~\Documents\my-project
cd ~\Documents\my-project
code .
```

**Mac / Linux / Git Bash:**
```bash
git clone https://github.com/PythonMuse/pythonmuse-workflow-kit.git ~/Documents/my-project
cd ~/Documents/my-project
code .
```

## 🎥 Video Walkthrough

Prefer to watch instead of read? Full walkthrough below:

https://youtu.be/O1E1mMKWp2s

---

## What Is Inside

```bash
pythonmuse-workflow-kit/
  .vscode/
    extensions.json         recommended VS Code extensions
    settings.json           workspace settings

  CLAUDE.md                 instructions for AI (rules, data locations, tone)
  plan.md                   project blueprint (fill this in first)
  status_update.md          rolling progress tracker

  data/
    raw/                    original source files (never modified)
    processed/              cleaned or transformed data

  src/                      scripts and logic files

  outputs/                  generated reports and results

  evidence/
    run-logs/               saved AI run logs for audit trail

  skills/
    bank-reconciliation/
      SKILL.md              reusable bank reconciliation workflow
    margin-analysis/
      SKILL.md              reusable margin analysis workflow
    pdf-extract/
      SKILL.md              PDF-to-Markdown extraction workflow

  docs/                     notes, memos, reference material
```

---

## How It Works

1. **Edit `plan.md`** -- describe your objective, source data, steps, and assumptions
2. **Drop data into `/data/raw/`** -- masked or sample data only
3. **Start an AI session** -- point it at `plan.md` and `CLAUDE.md`
4. **AI follows the plan** -- proposes steps, waits for approval, saves outputs
5. **Review and document** -- AI updates `status_update.md` when done

The folder structure is not just organization. It is the context that makes AI effective.

**Your folder structure is your prompt.**

---

## Using This with GitHub Copilot

GitHub Copilot reads your project structure, file names, and Markdown files to understand context. This template is designed to give Copilot everything it needs.

### Quick Start Prompts

**Set up a new project:**

> "I just cloned the PythonMuse Workflow Kit. Read CLAUDE.md and plan.md. Help me fill in plan.md for a bank reconciliation for March 2026."

**Import the structure into an existing project:**

> "Look at the PythonMuse Workflow Kit at github.com/PythonMuse/pythonmuse-workflow-kit. Set up the same folder structure and template files in my current workspace."

**Use a skill:**

> "Read the bank reconciliation skill in /skills/bank-reconciliation/SKILL.md. Apply it to the files in /data/raw/ and save results to /outputs/."

**Start a new session (after a break):**

> "Read plan.md and status_update.md. Summarize where we left off and confirm the next step."

**Save progress before ending:**

> "Update status_update.md with what was completed, where files are saved, any issues, and next steps."

### Why This Works with Copilot

Copilot prioritizes what it can see in your workspace:

| What Copilot Reads | What It Learns |
|--------------------|---------------|
| Folder names (`/data/raw/`, `/outputs/`) | Where to find and save files |
| `CLAUDE.md` | Rules and constraints to follow |
| `plan.md` | What the project is trying to accomplish |
| `status_update.md` | Where things stand right now |
| `skills/*.md` | How to execute specific workflow types |

A well-structured project replaces dozens of repeated prompts.

---

## Try the Demo

This kit ships with the two sample CSVs from [Article 01: AI Co-Pilot for Accounting](https://github.com/PythonMuse/ai-ledger/tree/main/articles/01-ai-copilot-for-accounting) already in [data/raw/](data/raw/). You can reproduce the entire margin-analysis story from the article without bringing your own data.

**Walk through it:** open [docs/demo-prompts.md](docs/demo-prompts.md) and run the prompts in order in Copilot Chat with Claude selected.

| Step | What you'll prompt | What you'll get |
|------|-------------------|----------------|
| 1 | Orient on the data | Structural read of both files |
| 2 | Calculate margin per order | Low-margin orders flagged |
| 3 | Show formulas, tie to source | Validation you can defend |
| 4 | Export joined dataset to Excel | Workpaper for manual review |
| 5 | Compare 2024 vs 2025 | YoY margin compression view |
| 6 | Rank reps, vendors, labor | Concentration and inflation patterns |
| 7 | Visualize the story | The five article charts as PNGs |
| 8 | Promote charting to a skill | Reusable `/skills/visualize-margin/` |
| 9 | Strategic summary | 5-point CFO-ready memo |
| 10 | Explain it back | Reproducible narrative |
| 11 | Validate before repeating | AI validation report + human sign-off |
| 12 | **Convert to a repeatable script** | Production Python in `/src/` |

Step 11 is the gate -- do not script anything you cannot defend by hand. Step 12 is the inflection point: once validated, you prompt Claude to turn the conversation into a versioned, commented, human-editable script -- with a CONFIG block, `# >>> HUMAN INPUT NEEDED:` markers, input validation, and a paired runbook. See the full prompts in [docs/demo-prompts.md](docs/demo-prompts.md).

> **Real client data?** The demo prompts are deliberately short. Before running this flow on anything sensitive, read the *Before You Start -- Real-World Safety Note* at the top of [docs/demo-prompts.md](docs/demo-prompts.md). Mask first, state materiality and period explicitly, and forbid silent assumptions.

### From One-Time to Repeatable

A script is the first level of automation, not the last. After Step 9, here is the maturity ladder you can climb -- pick the next move that solves your real pain:

1. **Promote to a Skill** -- move the logic into `/skills/<name>/SKILL.md` so any future session can invoke it by name.
2. **Pin the prompt** -- version-control the prompt sequence under `docs/prompts/` so it survives sessions.
3. **Externalize config** -- lift the CONFIG block out of Python into `config.yaml` so non-coders own the settings.
4. **Add a smoke test** -- have Claude diff this run's totals against last month's approved output.
5. **Add a CLI wrapper** -- `python -m src.<script> --period 2025-Q4` so it can be scheduled.
6. **Generate the runbook** -- ask Claude to produce `RUNBOOK.md` next to the script, not just the code.
7. **Lock the contract** -- a schema check that fails loudly when next month's file format drifts.
8. **Capture a golden output** -- save one approved run as `/evidence/golden/` and diff future runs against it.

Full prompts for each move are in [docs/demo-prompts.md](docs/demo-prompts.md) under *Beyond the Script*.

For the underlying methodology see [Article 11: From One-Time to Repeatable Workflows](https://github.com/PythonMuse/ai-ledger/tree/main/articles/11-one-time-to-repeatable-workflows/).

---

## Using This with Claude Code

If you use Claude Code (inside VS Code), the experience is similar. Claude reads `CLAUDE.md` automatically and uses `plan.md` and `status_update.md` as project context.

Start a session with:

> "Read plan.md and status_update.md. Summarize current state and confirm next step."

---

## Included Skills

| Skill | Use Case ID | Description |
|-------|-------------|-------------|
| [Bank Reconciliation](skills/bank-reconciliation/SKILL.md) | UC-001 | Match bank to GL, classify exceptions, produce audit-ready summary |
| [Margin Analysis](skills/margin-analysis/SKILL.md) | UC-003 | Gross margin by segment, period comparison, concentration risk flags |
| [PDF Extract](skills/pdf-extract/SKILL.md) | UC-004 | Convert PDF to Markdown, mask sensitive data, extract structured fields |

To add your own skill, create a new folder under `/skills/` with a `SKILL.md` following the same format.

---

## The Three Memory Files

| File | Purpose | When to Update |
|------|---------|----------------|
| `CLAUDE.md` | Instructions for how AI should behave | At project start; adjust as needed |
| `plan.md` | Defines the project scope, rules, and steps | At project start; revise as scope changes |
| `status_update.md` | Tracks completed work, outputs, issues, next steps | After each major milestone |

---

## Learn More

This template is part of the [PythonMuse AI Ledger](https://github.com/PythonMuse/ai-ledger) series -- practical Python, AI, and automation for accounting and finance teams.

- [Article 01: AI Co-Pilot for Accounting](https://github.com/PythonMuse/ai-ledger/tree/main/articles/01-ai-copilot-for-accounting) -- the worked example reproduced by the demo prompts in this kit
- [Article 08: Why Claude "Forgets"](https://github.com/PythonMuse/ai-ledger/tree/main/articles/08-why-claude-forgets/) -- why these three files matter
- [Article 11: From One-Time to Repeatable Workflows](https://github.com/PythonMuse/ai-ledger/tree/main/articles/11-one-time-to-repeatable-workflows/) -- the nine-step workflow pattern
- [Article 14: Stop Using One AI Like It Is Excel](https://github.com/PythonMuse/ai-ledger/tree/main/articles/14-ai-team-for-accountants/) -- how to use Claude, ChatGPT, and Copilot together
- [Article 16: The PDF Token Trap](https://github.com/PythonMuse/ai-ledger/tree/main/articles/16-pdf-token-trap/) -- why PDF-to-Markdown saves tokens and how the pdf-extract skill works
- [AI Accounting Framework](https://github.com/PythonMuse/pythonmuse-ai-accounting-framework) -- the full 13-section learning framework

---

## Contributing

Found a useful skill? Built a workflow template? Contributions are welcome.

See [CONTRIBUTING.md](https://github.com/PythonMuse/ai-ledger/blob/main/CONTRIBUTING.md) for details.

---

*From [PythonMuse](https://github.com/PythonMuse/ai-ledger) -- Practical Python, AI, and automation for accounting and finance teams.*
