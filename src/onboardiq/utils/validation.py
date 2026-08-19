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
    # Keep the report shape stable so callers can inspect every validation result.
    report: dict[str, Any] = {
        "required_columns_missing": [],
        "duplicate_ids": 0,
        "missing_values": {},
        "invalid_dates": 0,
        "row_count": len(df),
        "column_count": len(df.columns),
        "is_valid": True,
    }

    # Required columns are checked before row-level data quality checks.
    missing_columns = [col for col in required_columns if col not in df.columns]
    report["required_columns_missing"] = missing_columns
    if missing_columns:
        report["is_valid"] = False

    if "id" in df.columns:
        report["duplicate_ids"] = int(df["id"].duplicated().sum())

    # Record missing values by column so consumers can identify data gaps.
    missing_values = {column: int(count) for column, count in df.isna().sum().items() if count > 0}
    report["missing_values"] = missing_values
    if missing_values:
        report["is_valid"] = False

    if "created_at" in df.columns:
        # Invalid timestamps are coerced to NaT and counted as validation failures.
        parsed = pd.to_datetime(df["created_at"], errors="coerce")
        report["invalid_dates"] = int(parsed.isna().sum())
        if report["invalid_dates"] > 0:
            report["is_valid"] = False

    logger.info("Validation completed with %s rows", report["row_count"])
    return report


def summarize_validation_report(report: dict[str, Any]) -> str:
    """Convert a validation report into a short human-readable summary."""

    if report.get("is_valid", False):
        return (
            f"Dataset validation passed: {report.get('row_count', 0)} rows, "
            f"{report.get('column_count', 0)} columns."
        )

    issues: list[str] = []
    missing_columns = report.get("required_columns_missing", [])
    if missing_columns:
        issues.append(f"missing columns: {', '.join(missing_columns)}")

    duplicate_ids = int(report.get("duplicate_ids", 0))
    if duplicate_ids:
        issues.append(f"{duplicate_ids} duplicate id{'s' if duplicate_ids != 1 else ''}")

    missing_values = report.get("missing_values", {})
    if missing_values:
        details = ", ".join(f"{column}={count}" for column, count in missing_values.items())
        issues.append(f"missing values: {details}")

    invalid_dates = int(report.get("invalid_dates", 0))
    if invalid_dates:
        issues.append(f"{invalid_dates} invalid date{'s' if invalid_dates != 1 else ''}")

    return "Dataset validation failed: " + "; ".join(issues)
