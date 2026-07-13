# Workflow Examples

This folder contains sample YAML workflow files — the kind an AI co-pilot generates when you ask it to build an automated process.

These are **not meant to run as-is**. They are meant to be read.

Because that is the point.

---

## What Is a Workflow File?

A YAML workflow file is a structured configuration that describes:

- **What starts the process** (the trigger)
- **What happens and in what order** (the steps)
- **What the workflow is allowed to touch** (permissions)
- **What happens if something fails** (retry rules)
- **Whether a human must approve before outputs are distributed** (the approval gate)

Think of it as a written SOP — except computers can execute it.

---

## The Exercise

Open `invoice-to-dashboard.yaml`.

Before reading the code, answer these five questions from memory:

1. What should start this process?
2. In what order should the steps run?
3. What folders should this workflow be allowed to touch?
4. What should happen if it fails mid-way?
5. Should a human review the output before it goes to the team?

Now read the file.

Does the workflow match your answers?

If anything surprises you — that is the review.

---

## Why This Matters

AI can generate a workflow like this in seconds.

The hard part is not generating it.

The hard part is understanding what it is about to do before you click Run.

In the AI era, "I didn't write the code" will not be enough of a control explanation.

---

## Related Reading

[Article 29 — The Magic Loop](https://github.com/PythonMuse/ai-ledger/tree/main/articles/29-loops-the-automation-that-feels-magical)

**PythonMuse LLC** | pythonmuse.com
