"""Streamlit dashboard for OnboardIQ with starter UX improvements.

Features added:
- Sidebar data source selection (upload or sample file)
- Simple filters and download button
- "How it works" explainer inside the app
"""

from __future__ import annotations

import io
from pathlib import Path
import pandas as pd
import streamlit as st

from onboardiq.analytics.metrics import calculate_kpis
from onboardiq.analytics.retention import analyze_retention
from onboardiq.services.cleaning import clean_dataset
from onboardiq.services.feature_engineering import engineer_contributor_features
from onboardiq.utils.logging import get_logger
from onboardiq.visualization.plotting import create_retention_chart, create_risk_chart

logger = get_logger(__name__)

st.set_page_config(page_title="OnboardIQ", layout="wide")


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SAMPLE_CSV = PROJECT_ROOT / "processed_data" / "sample_contributors.csv"


@st.cache_data(show_spinner=False)
def load_dataset_from_file(path_or_buffer) -> pd.DataFrame:
    """Load and prepare a CSV file or file-like object into feature-ready DataFrame."""

    df = pd.read_csv(path_or_buffer)
    cleaned = clean_dataset(df)
    features = engineer_contributor_features(cleaned)
    return features


def show_kpis(df: pd.DataFrame) -> None:
    metrics = calculate_kpis(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Contributors", int(metrics.get("total_contributors", 0)))
    col2.metric("Pull Requests", int(metrics.get("total_pull_requests", 0)))
    col3.metric("Avg Merge Time (hrs)", round(metrics.get("avg_merge_time_hours", 0.0), 2))
    col4.metric("Retention Rate", round(metrics.get("retention_rate", 0.0), 2))


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


st.title("OnboardIQ")
st.write("GitHub contributor onboarding analytics")

with st.sidebar:
    st.header("Data")
    data_source = st.selectbox("Select data source", ["Upload CSV", "Use sample data (if available)"])
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload contributor data (CSV)", type=["csv"])
    else:
        uploaded_file = None

    st.markdown("---")
    st.header("Filters")
    show_only_risk = st.checkbox("Show only at-risk contributors", value=False)
    max_rows = st.slider("Max rows to display", min_value=10, max_value=1000, value=50)
    st.markdown("---")
    st.header("Help")
    st.write("Use the controls above to load data, filter, and download results.")

df = None
if data_source == "Use sample data (if available)" and SAMPLE_CSV.exists():
    try:
        df = load_dataset_from_file(SAMPLE_CSV)
    except Exception as exc:  # pragma: no cover - UI error handling
        st.error(f"Error loading sample data: {exc}")

if data_source == "Upload CSV" and uploaded_file is not None:
    try:
        df = load_dataset_from_file(uploaded_file)
    except Exception as exc:  # pragma: no cover - UI error handling
        st.error(f"Error loading uploaded file: {exc}")

if df is None:
    st.info("Upload a CSV file or place a sample at processed_data/sample_contributors.csv to try the dashboard.")
else:
    # Optional simple risk filter
    if show_only_risk and "risk_score" in df.columns:
        df_view = df[df["risk_score"] > 0.5]
    else:
        df_view = df

    show_kpis(df_view)

    retention = analyze_retention(df_view)
    st.plotly_chart(create_retention_chart(retention), use_container_width=True)
    st.plotly_chart(create_risk_chart(df_view), use_container_width=True)

    st.subheader("Data preview")
    st.dataframe(df_view.head(max_rows))

    csv_bytes = df_to_csv_bytes(df_view)
    st.download_button("Download CSV of current view", data=csv_bytes, file_name="onboardiq_export.csv", mime="text/csv")

    with st.expander("How this dashboard works (beginner-friendly)"):
        st.markdown(
            """
            - Upload a CSV of contributor events or use the sample file.
            - The app cleans data, derives contributor features, computes KPIs and retention.
            - Charts show retention curves and contributor risk; use filters to narrow results.
            - Use the download button to export the processed view for further analysis.
            """
        )
