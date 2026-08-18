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
- Testing and documentation scaffolding

## Quick Start

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

> Copy `.env.example` to `.env` before running the app locally and keep secrets out of version control.

## Project Structure

- `src/onboardiq/` application package
- `tests/` unit and integration tests
- `sql/` SQL scripts
- `reports/` generated reports
- `exports/` exports
- `docs/` architecture and user docs



## requirements

pandas>=2.2.0
numpy>=1.26.0
sqlalchemy>=2.0.30
psycopg2-binary>=2.9.9
plotly>=5.18.0
streamlit>=1.35.0
requests>=2.32.0
python-dotenv>=1.0.1
pytest>=8.3.0
black>=24.4.0
ruff>=0.5.0
mypy>=1.10.0
openai>=1.50.0

