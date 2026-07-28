"""Central logging configuration for the project."""

from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """Create a configured logger instance."""

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def ensure_log_dir(log_dir: str | Path | None = None) -> Path:
    """Create the log directory if it does not exist."""

    path = Path(log_dir or "logs")
    path.mkdir(parents=True, exist_ok=True)
    return path
