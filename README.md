# PythonMuse Workflow Kit

A ready-to-use project template for AI-assisted accounting workflows. Clone it, fill in your plan, drop in your data, and start working.

Built on the [PythonMuse](https://github.com/PythonMuse/ai-ledger) methodology for controlled, repeatable, and audit-ready AI workflows.

---

## Use This Template

On GitHub, click **"Use this template"** to create your own copy. Or clone it directly:

```bash
git clone https://github.com/PythonMuse/pythonmuse-workflow-kit.git my-project
cd my-project
code .
```

---

## What Is Inside

```
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
