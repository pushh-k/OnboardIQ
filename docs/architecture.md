# Architecture

OnboardIQ follows a layered architecture:

- Configuration: environment and settings management
- Data layer: ingestion, validation, cleaning, and persistence
- Analytics layer: KPIs, retention, and feature engineering
- Visualization layer: Plotly chart generation
- Dashboard layer: Streamlit UI
- AI layer: recommendations for insights and remediation

The dashboard consumes prepared datasets and never contains business logic.
