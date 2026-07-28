"""Configuration helpers for OnboardIQ."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Determine project root early so we can load environment-specific .env files
project_root = Path(__file__).resolve().parents[2]

# If an environment name is provided (ENV or ONBOARDIQ_ENV), try loading
# an environment-specific file first (e.g. .env.prd). Then fall back to
# the default .env at the project root.
_env_name = os.getenv("ENV") or os.getenv("ONBOARDIQ_ENV")
if _env_name:
    dotenv_path = project_root / f".env.{_env_name.lower()}"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)

# Finally load the default .env (if present) to provide defaults
load_dotenv(dotenv_path=project_root / ".env")


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    project_root: Path = project_root
    data_dir: Path = project_root / "data"
    raw_data_dir: Path = project_root / "raw_data"
    processed_data_dir: Path = project_root / "processed_data"
    reports_dir: Path = project_root / "reports"
    exports_dir: Path = project_root / "exports"
    github_token: str | None = os.getenv("GITHUB_TOKEN")
    github_api_url: str = os.getenv("GITHUB_API_URL", "https://api.github.com")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    database_url: str | None = os.getenv("DATABASE_URL")


settings = Settings()
