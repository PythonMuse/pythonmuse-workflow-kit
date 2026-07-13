"""
02_validate_manifest.py — Validate input_manifest.csv before AI-assisted analysis.

This script enforces the governance rules defined in SKILL.md:
  - Only files with status: final or approved may be used
  - Only files with approved_for_ai: yes may be used
  - Files in blocked folders are flagged regardless of status

Run this before starting any AI-assisted reconciliation analysis.
If the script raises an error, resolve the flagged files before proceeding.

Article 31: https://github.com/PythonMuse/ai-ledger/tree/main/articles/31-metadata-is-the-label-maker
"""

from pathlib import Path
import pandas as pd
import sys
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
MANIFEST_PATH = SKILL_DIR / "input_manifest.csv"
EVIDENCE_DIR = SKILL_DIR.parent.parent / "evidence" / "run-logs"

ALLOWED_STATUSES = {"final", "approved"}
BLOCKED_STATUSES = {"draft", "superseded", "do_not_use"}
BLOCKED_FOLDERS  = {"working", "archive", "raw_sensitive"}

def validate():
    if not MANIFEST_PATH.exists():
        print("ERROR: input_manifest.csv not found.")
        print("Run scripts/01_scan_folder.py first.")
        sys.exit(1)

    manifest = pd.read_csv(MANIFEST_PATH)

    needs_review = manifest[
        (manifest["status"] == "needs_review") |
        (manifest["approved_for_ai"] == "needs_review") |
        (manifest["data_classification"] == "needs_review")
    ]

    blocked_status = manifest[manifest["status"].isin(BLOCKED_STATUSES)]

    blocked_folder = manifest[manifest["folder"].isin(BLOCKED_FOLDERS)]

    not_approved = manifest[
        (manifest["approved_for_ai"] != "yes") &
        (~manifest["status"].isin(BLOCKED_STATUSES)) &
        (manifest["status"] != "needs_review")
    ]

    approved_files = manifest[
        (manifest["approved_for_ai"] == "yes") &
        (manifest["status"].isin(ALLOWED_STATUSES))
    ]

    print("=" * 60)
    print("MANIFEST VALIDATION — Cash Reconciliation Skill")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    issues = []

    if not needs_review.empty:
        issues.append(f"{len(needs_review)} file(s) still marked 'needs_review'")
        print(f"\n[NEEDS REVIEW] {len(needs_review)} file(s) require accountant sign-off:")
        for _, row in needs_review.iterrows():
            print(f"  - {row['file_name']}  (folder: {row['folder']})")

    if not blocked_status.empty:
        issues.append(f"{len(blocked_status)} file(s) have a blocked status")
        print(f"\n[BLOCKED STATUS] {len(blocked_status)} file(s) are not approved for use:")
        for _, row in blocked_status.iterrows():
            print(f"  - {row['file_name']}  status: {row['status']}")

    if not blocked_folder.empty:
        issues.append(f"{len(blocked_folder)} file(s) are in blocked folders")
        print(f"\n[BLOCKED FOLDER] {len(blocked_folder)} file(s) are in restricted folders:")
        for _, row in blocked_folder.iterrows():
            print(f"  - {row['file_name']}  folder: {row['folder']}")

    if not not_approved.empty:
        issues.append(f"{len(not_approved)} file(s) not approved for AI")
        print(f"\n[NOT APPROVED] {len(not_approved)} file(s) are not approved for AI use:")
        for _, row in not_approved.iterrows():
            print(f"  - {row['file_name']}  approved_for_ai: {row['approved_for_ai']}")

    print(f"\n[APPROVED] {len(approved_files)} file(s) are approved for AI-assisted analysis:")
    for _, row in approved_files.iterrows():
        print(f"  + {row['file_name']}  ({row['status']}, {row['data_classification']})")

    # Save evidence log
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    log_path = EVIDENCE_DIR / f"{datetime.now().strftime('%Y-%m-%d')}_manifest-validation.md"
    with open(log_path, "w") as f:
        f.write(f"# Manifest Validation Log\n\n")
        f.write(f"**Run at:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        f.write(f"**Skill:** cash-reconciliation  \n")
        f.write(f"**Manifest:** {MANIFEST_PATH.name}  \n\n")
        f.write(f"## Approved files ({len(approved_files)})\n\n")
        for _, row in approved_files.iterrows():
            f.write(f"- {row['file_name']}  ({row['status']}, {row['data_classification']})\n")
        if issues:
            f.write(f"\n## Issues flagged ({len(issues)})\n\n")
            for issue in issues:
                f.write(f"- {issue}\n")
        f.write(f"\n## Result\n\n")
        f.write("PASSED\n" if not issues else "BLOCKED — resolve issues before proceeding\n")

    print(f"\nEvidence log saved: {log_path}")
    print("=" * 60)

    if issues:
        print(f"\nWORKFLOW BLOCKED — {len(issues)} issue(s) must be resolved.")
        print("Update input_manifest.csv and re-run this script.")
        sys.exit(1)
    else:
        print("\nVALIDATION PASSED — Manifest is ready for AI-assisted analysis.")

if __name__ == "__main__":
    validate()
