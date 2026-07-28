"""Reusable cleaning pipelines for onboarding datasets."""

from __future__ import annotations

import pandas as pd

from onboardiq.utils.logging import get_logger

logger = get_logger(__name__)


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize and clean a contributor dataset."""

    cleaned = df.copy()
    cleaned = (
        cleaned.drop_duplicates(subset=["id"], keep="first") if "id" in cleaned.columns else cleaned
    )
    for column in cleaned.columns:
        if cleaned[column].dtype == "object":
            cleaned[column] = cleaned[column].astype(str).str.strip()
            cleaned[column] = cleaned[column].replace({"nan": "", "None": ""})
    if "created_at" in cleaned.columns:
        cleaned["created_at"] = pd.to_datetime(cleaned["created_at"], errors="coerce")
    if "merged_at" in cleaned.columns:
        cleaned["merged_at"] = pd.to_datetime(cleaned["merged_at"], errors="coerce")
    for column in cleaned.columns:
        if cleaned[column].dtype == "object":
            cleaned[column] = cleaned[column].fillna("")
    logger.info("Dataset cleaned successfully")
    return cleaned
