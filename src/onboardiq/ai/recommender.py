"""AI-style recommendation generation."""

from __future__ import annotations

from typing import Any

import pandas as pd


class RecommendationEngine:
    """Generate simple recommendations based on analytics output."""

    def generate_recommendations(self, df: pd.DataFrame) -> list[dict[str, Any]]:
        """Return recommendation objects for a dataset."""

        if df.empty:
            return []

        suggestions: list[dict[str, Any]] = []
        if "risk_score" in df.columns:
            high_risk = df[df["risk_score"] > 0.6]
            if not high_risk.empty:
                suggestions.append(
                    {
                        "title": "Reduce onboarding friction",
                        "detail": "Prioritize contributors with elevated risk scores for mentoring and documentation support.",
                    }
                )
        if "merge_time_hours" in df.columns:
            suggestions.append(
                {
                    "title": "Accelerate review cycles",
                    "detail": "Shorten response times for pull requests with long merge windows.",
                }
            )
        return suggestions
