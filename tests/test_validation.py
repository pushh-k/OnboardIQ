import pandas as pd

from onboardiq.utils.validation import summarize_validation_report, validate_dataset


def test_validate_dataset_detects_missing_and_duplicate_ids() -> None:
    df = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "repo": ["repo-a", "repo-a", "repo-b"],
            "created_at": ["2024-01-01", "2024-01-01", "bad-date"],
            "score": [1.0, None, 3.0],
        }
    )

    report = validate_dataset(df, required_columns=["id", "repo", "created_at", "score"])

    assert report["duplicate_ids"] == 1
    assert report["missing_values"]["score"] == 1
    assert report["invalid_dates"] == 1
    assert report["is_valid"] is False


def test_summarize_validation_report_formats_failure_message() -> None:
    report = {
        "required_columns_missing": ["created_at"],
        "duplicate_ids": 2,
        "missing_values": {"score": 1},
        "invalid_dates": 1,
        "row_count": 3,
        "column_count": 4,
        "is_valid": False,
    }

    summary = summarize_validation_report(report)

    assert summary == (
        "Dataset validation failed: missing columns: created_at; 2 duplicate ids; "
        "missing values: score=1; 1 invalid date"
    )
