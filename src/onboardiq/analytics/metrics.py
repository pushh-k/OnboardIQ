"""Analytical metrics for contributor onboarding."""

from __future__ import annotations

import pandas as pd

from onboardiq.utils.logging import get_logger

logger = get_logger(__name__)


def calculate_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Calculate onboarding KPIs from a pull request dataset."""

    if df.empty:
        return {
            "total_contributors": 0.0,
            "total_pull_requests": 0.0,
            "avg_merge_time_hours": 0.0,
            "retention_rate": 0.0,
        }

    contributor_count = df["contributor"].nunique() if "contributor" in df.columns else 0
    pr_count = len(df)
    avg_merge = float(df["merge_time_hours"].mean()) if "merge_time_hours" in df.columns else 0.0
    retention = (
        float(df["repeat_contributor"].mean()) if "repeat_contributor" in df.columns else 0.0
    )
    logger.info("Calculated KPIs for %s contributors", contributor_count)
    return {
        "total_contributors": float(contributor_count),
        "total_pull_requests": float(pr_count),
        "avg_merge_time_hours": avg_merge,
        "retention_rate": retention,
    }
