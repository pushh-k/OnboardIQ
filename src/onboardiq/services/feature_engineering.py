"""Feature engineering for contributor onboarding analytics."""

from __future__ import annotations

import pandas as pd

from onboardiq.utils.logging import get_logger

logger = get_logger(__name__)


def engineer_contributor_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create reusable contributor features from pull request events."""

    features = df.copy()
    if "created_at" in features.columns:
        features["created_at"] = pd.to_datetime(features["created_at"], errors="coerce")
    if "merged_at" in features.columns:
        features["merged_at"] = pd.to_datetime(features["merged_at"], errors="coerce")

    if "contributor" in features.columns:
        features["first_contribution"] = features.groupby("contributor")["created_at"].transform(
            "min"
        )
        features["repeat_contributor"] = (
            features.groupby("contributor")["pull_request_number"].transform("count") > 1
        )

    if "merged_at" in features.columns and "created_at" in features.columns:
        features["merge_time_hours"] = (
            features["merged_at"] - features["created_at"]
        ).dt.total_seconds() / 3600.0

    if "review_count" in features.columns:
        features["documentation_quality_score"] = features["review_count"].astype(float) / (
            features["review_count"].astype(float) + 1.0
        )
    else:
        features["documentation_quality_score"] = 0.0

    if "ci_status" in features.columns:
        features["ci_failure_rate"] = (
            features["ci_status"]
            .eq("failure")
            .astype(float)
            .groupby(features.get("contributor", pd.Series([""] * len(features))))
            .transform("mean")
        )
    else:
        features["ci_failure_rate"] = 0.0

    features["onboarding_score"] = (
        features["documentation_quality_score"] * 0.4 + features["ci_failure_rate"] * 0.6
    )
    features["risk_score"] = 1.0 - features["onboarding_score"]

    logger.info("Engineered contributor features for %s rows", len(features))
    return features
