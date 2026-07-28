# Product Requirements Document (PRD) — OnboardIQ

Version: 0.1
Last updated: 2026-07-24

## 1. Overview

- Project name: OnboardIQ
- Purpose: Provide analytics, automation, and recommendations to improve new-hire onboarding and employee retention insights by integrating with GitHub and other data sources.
- Scope: Data ingestion, processing pipelines, analytics metrics, AI-driven recommendations, dashboards and reports, CLI utilities, and operational runbook.

## 2. Objectives & Success Metrics

- Objective 1: Ingest GitHub repository and organizational data reliably.
  - Success metric: 99% scheduled ingestion success rate over 30 days.
- Objective 2: Produce core analytics (retention, activity, funnel) and dashboards.
  - Success metric: Dashboards update within 15 minutes of pipeline completion.
- Objective 3: Offer automated recommendations using the AI recommender module.
  - Success metric: 20% uplift in recommended actions acceptance (tracked in pilot).
- Objective 4: Securely manage secrets and production configuration.
  - Success metric: No production secrets stored in repo and secrets rotated every 90 days.

## 3. Stakeholders

- Product owner: [TEAM 01 members]
- Engineering lead: [Name]
- Data engineer: [Name]
- Data scientist: [Name]
- DevOps / SRE: [Name]
- End users: People Ops, Engineering managers, Onboarding teams

## 4. Users & Personas

- People Ops Analyst: Uses dashboards and scheduled reports to identify retention risks.
- Engineering Manager: Uses recommendations to improve onboarding practices.
- Data Scientist: Extends models in `src/onboardiq/ai/recommender.py`.
- SRE: Monitors pipelines and uptime; uses runbook for incident response.

## 5. Requirements

### 5.1 Functional Requirements

- FR-1: Data Ingestion
  - The system must ingest GitHub events, repo metadata, and user profiles on a configurable schedule.
  - Support backfill and incremental runs.
- FR-2: Data Processing
  - Implement cleaning and feature engineering pipelines in `src/onboardiq/services/cleaning.py` and `src/onboardiq/services/feature_engineering.py`.
  - Persist processed artifacts to `processed_data/` and `exports/`.
- FR-3: Analytics
  - Provide retention and activity metrics in `src/onboardiq/analytics/metrics.py` and `retention.py`.
- FR-4: Recommender
  - Provide `recommend()` API returning prioritized recommendations for onboarding improvements.
- FR-5: Dashboards and Reports
  - Expose Streamlit or Dash app at `src/onboardiq/dashboard/app.py` for interactive visualization.
- FR-6: CLI
  - Provide `src/onboardiq/cli/main.py` commands for running ingestion, pipelines, and reports.

### 5.2 Non-Functional Requirements

- NFR-1: Security
  - Do not commit secrets to the repository; support `.env`, `.env.prd`, and environment variables.
- NFR-2: Reliability
  - Pipelines must be idempotent and support retries.
- NFR-3: Observability
  - Emit metrics, logs, and traces for ingestion and pipeline runs.
- NFR-4: Performance
  - Typical pipeline run for a medium-sized org (<100 repos) should complete within 30 minutes.

## 6. Architecture

- Components:
  - Data ingestion workers (`src/onboardiq/data/ingestion.py`, `github_client.py`)
  - Processing pipelines (`src/onboardiq/services`)
  - Analytics modules (`src/onboardiq/analytics`)
  - Recommender (`src/onboardiq/ai/recommender.py`)
  - Dashboard (`src/onboardiq/dashboard/app.py`)
  - CLI (`src/onboardiq/cli/main.py`)
- Storage: local `processed_data/`, `exports/` for artifacts. Production deployments should use managed databases and object storage.

## 7. Data Model & Schemas

- Primary entities:
  - Repository: id, name, org, created_at, language
  - User: id, username, email (hashed in exports), join_date
  - Event: id, repo_id, user_id, type, timestamp, payload
  - Metric: key, value, timestamp, dimensions
- Keep canonical SQL schema in `src/onboardiq/db/schema.sql` and maintain migrations in the repo if applicable.

## 8. Security & Compliance

- Secrets: Use deployment secrets managers (Vault, AWS Secrets Manager, Azure Key Vault). Local dev uses `.env` files (added to `.gitignore`).
- PII: Exported datasets must have hashed or redacted personal data fields.
- Access control: Dashboards and API endpoints should integrate with SSO/OAuth in production.

## 9. Deployment & Runbook

### 9.1 Environments
- `dev`: local developer machines; `.env` used.
- `stg`: staging environment mirroring production.
- `prd`: production; secrets injected via secret manager or `.env.prd` in CI (avoid storing in repo).

### 9.2 Deployment Steps (basic)
1. Build application image (optional) or prepare Python environment.
2. Ensure environment variables present (see `.env.prd` template).
3. Run DB migrations if needed.
4. Start ingestion and pipeline jobs (cron, Airflow, or CI scheduled workflows).
5. Start dashboard service.

### 9.3 Runbook — Common Incidents
- Ingestion failure:
  - Check logs in the ingestion worker. Restart job. If API rate limit, wait and increase backoff.
- Database connectivity:
  - Verify `DATABASE_URL`. Check network and auth.
- Secrets missing:
  - Confirm secret manager or `.env.prd` has required keys.

## 10. Monitoring & Alerts
- Track pipeline success/failure counts, latency, and error rates.
- Alert on repeated ingestion failures, high error rates, or storage full conditions.

## 11. Acceptance Criteria
- End-to-end ingestion → processing → dashboard pipeline runs successfully on staging with test data.
- All configs are environment-driven; no secrets in repo.
- Documentation completed: this PRD, architecture, data dictionary, and runbook.

## 12. Open Questions
- Which secret management service will production use?
- Will we use a scheduler (Airflow/Cron/Kubernetes CronJob) or serverless triggers?
- Who is responsible for rotating production secrets?

## 13. Appendix
- Related docs: [docs/architecture.md](architecture.md), [docs/data_dictionary.md](data_dictionary.md), [sql/views.sql](sql/views.sql)
- Key files:
  - `src/onboardiq/config/settings.py`
  - `src/onboardiq/data/ingestion.py`
  - `src/onboardiq/services/feature_engineering.py`
  - `src/onboardiq/ai/recommender.py`

