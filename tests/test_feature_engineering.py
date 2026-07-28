import pandas as pd

from onboardiq.services.feature_engineering import engineer_contributor_features


def test_engineer_contributor_features_creates_expected_columns() -> None:
    df = pd.DataFrame(
        {
            "contributor": ["alice", "alice", "bob"],
            "pull_request_number": [1, 2, 3],
            "created_at": ["2024-01-01", "2024-01-10", "2024-01-20"],
            "merged_at": ["2024-01-02", "2024-01-11", "2024-01-21"],
            "review_count": [2, 1, 3],
            "comments_count": [1, 2, 1],
            "ci_status": ["success", "failure", "success"],
            "is_documentation_change": [False, True, False],
        }
    )

    result = engineer_contributor_features(df)

    assert "first_contribution" in result.columns
    assert "repeat_contributor" in result.columns
    assert "merge_time_hours" in result.columns
    assert "documentation_quality_score" in result.columns
    assert "ci_failure_rate" in result.columns
