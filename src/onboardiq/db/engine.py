"""Database engine helpers for SQLAlchemy."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from onboardiq.config.settings import settings


def get_engine() -> Engine:
    """Create a SQLAlchemy engine from the configured database URL."""

    if not settings.database_url:
        raise ValueError("DATABASE_URL is not configured")
    return create_engine(settings.database_url)
