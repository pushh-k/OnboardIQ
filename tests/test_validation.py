import pandas as pd

from onboardiq.utils.validation import validate_dataset


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
