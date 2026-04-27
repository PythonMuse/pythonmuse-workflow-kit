"""
data_masking_gate.py
--------------------
PreToolUse hook — intercepts Bash tool calls before execution.

Claude Code invokes this script (via the PreToolUse hook in .claude/settings.json)
with the proposed command passed on stdin as JSON:

    {"tool_name": "Bash", "tool_input": {"command": "<shell command>"}}

Exit codes:
    0  — approved, execution may proceed
    1  — blocked, execution must not proceed (message printed to stderr)

Approval token:
    A file-based token (data/processed/.db_approval_token) grants a 5-minute
    window so the reviewer is not re-prompted on rapid successive executions.

What is checked:
    1. Does the command or referenced script contain data-access patterns?
       (pyodbc, sqlite3, psycopg2, sqlalchemy, pd.read_sql, pd.read_csv,
        open(...), requests.get, urllib)
    2. If yes — does the script also call DataMasker before any output step?
    3. Is there a valid (non-expired) approval token on disk?

If data access is detected but masking is absent or unapproved, the gate
blocks and prompts the reviewer at the terminal.
"""

import json
import sys
import os
import re
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOKEN_PATH = Path("data/processed/.db_approval_token")
TOKEN_TTL_SECONDS = 300  # 5 minutes

# Patterns that indicate a script is reaching out for data
DATA_ACCESS_PATTERNS = [
    r"pyodbc",
    r"psycopg2",
    r"sqlite3",
    r"sqlalchemy",
    r"pd\.read_sql",
    r"pd\.read_csv",
    r"pd\.read_excel",
    r"pd\.read_parquet",
    r"open\s*\(",
    r"requests\.(get|post|put)",
    r"urllib\.request",
    r"boto3",          # AWS S3
    r"google\.cloud",  # GCS
]

# Masking must be called before cloud/chat output
MASKING_PRESENT_PATTERNS = [
    r"DataMasker",
    r"mask_dataframe",
    r"from data_masking import",
    r"import data_masking",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_stdin_payload() -> dict:
    """Read the JSON payload Claude Code sends on stdin."""
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _extract_script_path(command: str) -> Path | None:
    """Pull a .py filename out of a shell command string, if present."""
    match = re.search(r"([\w./\\-]+\.py)", command)
    if match:
        candidate = Path(match.group(1))
        if candidate.exists():
            return candidate
    return None


def _read_script_source(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _has_pattern(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text) for p in patterns)


def _token_valid() -> bool:
    if not TOKEN_PATH.exists():
        return False
    age = time.time() - TOKEN_PATH.stat().st_mtime
    return age < TOKEN_TTL_SECONDS


def _write_token() -> None:
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.touch()


def _prompt_reviewer(command: str, has_masking: bool) -> bool:
    """
    Prompt the reviewer at the terminal.
    Returns True if approved, False if denied.
    """
    print("\n" + "=" * 70, file=sys.stderr)
    print("  DATA ACCESS GATE — Human Review Required", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(f"\n  Command:\n    {command[:200]}", file=sys.stderr)

    if not has_masking:
        print("\n  WARNING: DataMasker not detected in this script.", file=sys.stderr)
        print("  Sensitive data may reach the AI model unmasked.", file=sys.stderr)
    else:
        print("\n  DataMasker usage detected. OK.", file=sys.stderr)

    print("\n  Before approving, confirm:", file=sys.stderr)
    print("    [1] The query scope is limited to what this task requires.", file=sys.stderr)
    print("    [2] DataMasker will run before any data is sent to the AI.", file=sys.stderr)
    print("    [3] No raw sensitive values will appear in chat responses.", file=sys.stderr)

    print("\n  Approve execution? [y/N]: ", end="", file=sys.stderr)
    try:
        answer = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        answer = "n"

    return answer == "y"


# ---------------------------------------------------------------------------
# Main gate logic
# ---------------------------------------------------------------------------

def main() -> int:
    payload = _read_stdin_payload()
    command: str = payload.get("tool_input", {}).get("command", "")

    if not command:
        # No command to inspect — let it pass
        return 0

    # Combine command text + referenced script source for analysis
    script_source = ""
    script_path = _extract_script_path(command)
    if script_path:
        script_source = _read_script_source(script_path)

    combined_text = command + "\n" + script_source

    # Check 1: does this touch data?
    if not _has_pattern(combined_text, DATA_ACCESS_PATTERNS):
        return 0  # No data access — pass through silently

    # Check 2: is masking present?
    has_masking = _has_pattern(combined_text, MASKING_PRESENT_PATTERNS)

    # Check 3: valid approval token within TTL window?
    if has_masking and _token_valid():
        return 0  # Already approved recently — pass through

    # --- Gate triggered: prompt reviewer ---
    approved = _prompt_reviewer(command, has_masking)

    if approved:
        _write_token()
        print("\n  Approved. Proceeding.\n", file=sys.stderr)
        return 0
    else:
        print("\n  Denied. Execution blocked.\n", file=sys.stderr)
        print("GATE_BLOCKED: Reviewer denied execution.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
