"""Plotly chart helpers for the dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def create_retention_chart(df: pd.DataFrame) -> object:
    """Create a retention funnel chart."""

    if df.empty:
        return px.bar(title="No retention data")

    fig = px.bar(df, x="cohort", y="retention_rate", title="Retention by Cohort")
    fig.update_layout(template="plotly_white")
    return fig


def create_risk_chart(df: pd.DataFrame) -> object:
    """Create a risk distribution chart."""

    if df.empty:
        return px.bar(title="No risk data")

    fig = px.histogram(df, x="risk_score", nbins=10, title="Risk Distribution")
    fig.update_layout(template="plotly_white")
    return fig
