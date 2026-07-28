"""CLI entrypoint for running the onboarding pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from onboardiq.analytics.metrics import calculate_kpis
from onboardiq.services.cleaning import clean_dataset
from onboardiq.services.feature_engineering import engineer_contributor_features
from onboardiq.utils.logging import get_logger
from onboardiq.utils.validation import validate_dataset

logger = get_logger(__name__)


def run_pipeline(input_path: str, output_path: str) -> None:
    """Execute the data pipeline on a CSV file."""

    logger.info("Starting pipeline for %s", input_path)
    df = pd.read_csv(input_path)
    report = validate_dataset(df, required_columns=["id", "contributor", "created_at"])
    logger.info("Validation report: %s", report)
    cleaned = clean_dataset(df)
    features = engineer_contributor_features(cleaned)
    metrics = calculate_kpis(features)
    logger.info("KPIs: %s", metrics)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OnboardIQ pipeline")
    parser.add_argument("input_path", help="Path to the input CSV file")
    parser.add_argument("output_path", help="Path to the output CSV file")
    args = parser.parse_args()
    run_pipeline(args.input_path, args.output_path)
