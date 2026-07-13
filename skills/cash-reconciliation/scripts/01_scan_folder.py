"""
01_scan_folder.py — Generate a starter input manifest by scanning the skill folder.

Run this script first. It creates input_manifest.csv with all files marked
'needs_review'. Then open the CSV and apply your judgment:

  - Set status to: final / approved / draft / superseded / do_not_use
  - Set approved_for_ai to: yes / no
  - Set data_classification to: Confidential / Internal / Public

After reviewing the manifest, run 02_validate_manifest.py to check it
before any AI-assisted analysis begins.

Article 31: https://github.com/PythonMuse/ai-ledger/tree/main/articles/31-metadata-is-the-label-maker
"""

from pathlib import Path
import pandas as pd

SKILL_DIR = Path(__file__).parent.parent
MANIFEST_PATH = SKILL_DIR / "input_manifest.csv"

records = []

for file in SKILL_DIR.rglob("*"):
    if file.is_file() and file.suffix in {".csv", ".xlsx", ".xls", ".pdf", ".md", ".txt"}:
        records.append({
            "file_name": file.name,
            "folder": file.parent.name,
            "file_type": file.suffix,
            "file_path": str(file.relative_to(SKILL_DIR)),
            "status": "needs_review",
            "approved_for_ai": "needs_review",
            "data_classification": "needs_review",
            "purpose": "",
        })

if not records:
    print("No files found to inventory.")
else:
    metadata = pd.DataFrame(records)
    metadata.to_csv(MANIFEST_PATH, index=False)
    print(f"Starter manifest created: {MANIFEST_PATH}")
    print(f"  {len(records)} file(s) found.")
    print()
    print("Next step: open input_manifest.csv and fill in:")
    print("  status            → final / approved / draft / superseded / do_not_use")
    print("  approved_for_ai   → yes / no")
    print("  data_classification → Confidential / Internal / Public")
    print()
    print("Then run: python scripts/02_validate_manifest.py")
