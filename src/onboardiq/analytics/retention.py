# """Retention analysis helpers."""

from __future__ import annotations

import pandas as pd


def analyze_retention(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize contributor retention by cohort."""

    if df.empty:
        return pd.DataFrame(columns=["cohort", "retention_rate"])

    cohort_df = df.copy()
    if "created_at" in cohort_df.columns:
        cohort_df["cohort"] = cohort_df["created_at"].dt.to_period("M").astype(str)
    else:
        cohort_df["cohort"] = "unknown"

    summary = (
        cohort_df.groupby("cohort").agg(retention_rate=("repeat_contributor", "mean")).reset_index()
    )
    return summary
