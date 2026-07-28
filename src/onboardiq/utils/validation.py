"""Validation helpers for incoming dataset files."""

from __future__ import annotations

from typing import Any

import pandas as pd

from onboardiq.utils.logging import get_logger

logger = get_logger(__name__)


def validate_dataset(
    df: pd.DataFrame,
    required_columns: list[str] | None = None,
) -> dict[str, Any]:
    """Validate a dataset and return a structured report."""

    required_columns = required_columns or []
    report: dict[str, Any] = {
        "required_columns_missing": [],
        "duplicate_ids": 0,
        "missing_values": {},
        "invalid_dates": 0,
        "row_count": len(df),
        "column_count": len(df.columns),
        "is_valid": True,
    }

    missing_columns = [col for col in required_columns if col not in df.columns]
    report["required_columns_missing"] = missing_columns
    if missing_columns:
        report["is_valid"] = False

    if "id" in df.columns:
        report["duplicate_ids"] = int(df["id"].duplicated().sum())

    missing_values = {column: int(count) for column, count in df.isna().sum().items() if count > 0}
    report["missing_values"] = missing_values
    if missing_values:
        report["is_valid"] = False

    if "created_at" in df.columns:
        parsed = pd.to_datetime(df["created_at"], errors="coerce")
        report["invalid_dates"] = int(parsed.isna().sum())
        if report["invalid_dates"] > 0:
            report["is_valid"] = False

    logger.info("Validation completed with %s rows", report["row_count"])
    return report
