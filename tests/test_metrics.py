import pandas as pd

from onboardiq.analytics.metrics import summarize_contributor_risk


def test_summarize_contributor_risk_assigns_risk_levels() -> None:
    df = pd.DataFrame(
        {
            "contributor": ["alice", "alice", "bob"],
            "onboarding_score": [0.2, 0.3, 0.8],
            "risk_score": [0.8, 0.7, 0.2],
        }
    )

    result = summarize_contributor_risk(df)

    assert list(result.columns) == [
        "contributor",
        "onboarding_score",
        "risk_score",
        "risk_level",
    ]
    assert result.loc[result["contributor"] == "alice", "risk_level"].iloc[0] == "high"
    assert result.loc[result["contributor"] == "bob", "risk_level"].iloc[0] == "low"
