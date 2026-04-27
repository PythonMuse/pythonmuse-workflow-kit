"""
data_masking.py
---------------
DataMasker: masks sensitive values in DataFrames before any cloud/chat output.

Usage:
    masker = DataMasker()
    masked_df, summary = masker.mask_dataframe(df)
    masker.save_mapping()
    # Use masked_df for cloud/chat only. Original df stays local.
    # To recover original values locally:
    #   original_df = masker.unmask_dataframe(masked_df)

Mapping file: data/processed/masking_map.json
"""

import json
import re
from pathlib import Path

import pandas as pd


# Column name patterns that signal sensitive content
_SENSITIVE_PATTERNS = {
    "amount":     (r"(amount|amt|revenue|cost|price|salary|wage|budget|total|balance|payment|fee)", "[AMT_{n}]"),
    "headcount":  (r"(headcount|hc|fte|employees?|staff|count)",                                   "[HC_{n}]"),
    "percent":    (r"(percent|pct|rate|ratio|margin)",                                              "[PCT_{n}]"),
    "employee":   (r"(employee|emp|name|worker|staff_name|person)",                                 "[EMP_{n}]"),
    "client":     (r"(client|customer|vendor|supplier|partner)",                                    "[CLIENT_{n}]"),
    "company":    (r"(company|co|entity|org|organization|firm)",                                    "[CO_{n}]"),
    "tax_id":     (r"(ssn|tax_id|ein|tin|id_number|identifier)",                                   "[ID_{n}]"),
    "account":    (r"(account|acct|bank|routing|iban|swift)",                                       "[ACCT_{n}]"),
}

_SAFE_DTYPES = {"datetime64[ns]", "datetime64[ns, UTC]"}


class DataMasker:
    """
    Replaces sensitive values with stable coded placeholders.

    Identifiers are identity-stable within a session: the same original value
    always maps to the same placeholder (e.g., the same employee always gets
    [EMP_1]).  The mapping is written to data/processed/masking_map.json for
    local-only reference — never transmit this file to the cloud.
    """

    _MAP_PATH = Path("data/processed/masking_map.json")

    def __init__(self, map_path: str | None = None):
        self._map_path = Path(map_path) if map_path else self._MAP_PATH
        # {category: {original_value: placeholder}}
        self._forward: dict[str, dict[str, str]] = {}
        # {placeholder: original_value}  (flat, for unmasking)
        self._reverse: dict[str, str] = {}
        self._counters: dict[str, int] = {}

        if self._map_path.exists():
            self._load_mapping()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def mask_dataframe(
        self,
        df: pd.DataFrame,
        column_rules: dict[str, str] | None = None,
    ) -> tuple[pd.DataFrame, dict]:
        """
        Mask a DataFrame in-place on a copy.

        Parameters
        ----------
        df : pd.DataFrame
            Input data (never modified).
        column_rules : dict, optional
            Per-column overrides, e.g. {'GL_Code': 'skip'} to leave a column
            unmasked, or {'Notes': 'employee'} to force a masking category.

        Returns
        -------
        masked_df : pd.DataFrame
            Copy with sensitive values replaced.
        summary : dict
            {col: {'category': ..., 'unique_values_masked': n}} for masked cols.
        """
        column_rules = column_rules or {}
        masked = df.copy()
        summary: dict[str, dict] = {}

        for col in masked.columns:
            rule = column_rules.get(col)
            if rule == "skip":
                continue

            category = rule or self._detect_category(col)
            if category is None:
                continue

            template = _SENSITIVE_PATTERNS[category][1]
            n_masked = 0
            for idx in masked.index:
                raw = masked.at[idx, col]
                if pd.isna(raw) or str(raw).strip() == "":
                    continue
                masked.at[idx, col] = self._get_or_create(category, str(raw), template)
                n_masked += 1

            if n_masked:
                summary[col] = {"category": category, "unique_values_masked": n_masked}

        return masked, summary

    def unmask_dataframe(self, masked_df: pd.DataFrame) -> pd.DataFrame:
        """Reverse a previously masked DataFrame (local post-processing only)."""
        df = masked_df.copy()
        for col in df.columns:
            df[col] = df[col].apply(
                lambda v: self._reverse.get(str(v), v) if pd.notna(v) else v
            )
        return df

    def mask_value(self, value: str, category: str) -> str:
        """Mask a single scalar value given an explicit category."""
        if category not in _SENSITIVE_PATTERNS:
            raise ValueError(f"Unknown category: {category}. "
                             f"Valid: {list(_SENSITIVE_PATTERNS)}")
        template = _SENSITIVE_PATTERNS[category][1]
        return self._get_or_create(category, str(value), template)

    def save_mapping(self) -> Path:
        """Persist the forward mapping to data/processed/masking_map.json."""
        self._map_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._map_path, "w") as f:
            json.dump(self._forward, f, indent=2)
        return self._map_path

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _detect_category(self, col_name: str) -> str | None:
        lower = col_name.lower()
        for category, (pattern, _) in _SENSITIVE_PATTERNS.items():
            if re.search(pattern, lower):
                return category
        return None

    def _get_or_create(self, category: str, original: str, template: str) -> str:
        bucket = self._forward.setdefault(category, {})
        if original not in bucket:
            self._counters[category] = self._counters.get(category, 0) + 1
            placeholder = template.replace("{n}", str(self._counters[category]))
            bucket[original] = placeholder
            self._reverse[placeholder] = original
        return bucket[original]

    def _load_mapping(self) -> None:
        with open(self._map_path) as f:
            self._forward = json.load(f)
        for category, bucket in self._forward.items():
            for original, placeholder in bucket.items():
                self._reverse[placeholder] = original
            # Restore counters so new values extend the existing sequence
            nums = [
                int(re.search(r"_(\d+)\]", p).group(1))
                for p in bucket.values()
                if re.search(r"_(\d+)\]", p)
            ]
            if nums:
                self._counters[category] = max(nums)
