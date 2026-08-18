# OnboardIQ

OnboardIQ is an enterprise-grade analytics platform for understanding GitHub contributor onboarding, retention, review friction, and maintainer bottlenecks.

## Features

- GitHub data ingestion and validation
- Data cleaning and feature engineering
- KPI and retention analytics
- Plotly visualizations
- Streamlit dashboard
- SQL schema for PostgreSQL
- CLI pipeline runner
- Testing documentation scaffolding



 Quick Start

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`
4. Launch the dashboard: `streamlit run src/onboardiq/dashboard/app.py`
5. Run the CLI pipeline: `python -m onboardiq.cli.main <input.csv> <output.csv>`

## Configuration

Set environment variables:

- `GITHUB_TOKEN`
- `OPENAI_API_KEY`
- `DATABASE_URL`

## Structure of project

- `src/onboardiq/` application package
- `tests/` unit and integration tests
- `sql/` SQL scripts
- `reports/` generated reports
- `exports/` exports
- `docs/` architecture and user docs





