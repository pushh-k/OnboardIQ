"""Ingestion orchestration for GitHub datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from onboardiq.data.github_client import GitHubClient
from onboardiq.utils.logging import get_logger

logger = get_logger(__name__)


class GitHubIngestionService:
    """Fetch and persist GitHub repository data."""

    def __init__(self, client: GitHubClient | None = None) -> None:
        self.client = client or GitHubClient()

    def ingest_repository(
        self, owner: str, repo: str, output_dir: str | Path | None = None
    ) -> dict[str, Any]:
        """Ingest a repository and save raw JSON payloads."""

        output_path = Path(output_dir or "raw_data")
        output_path.mkdir(parents=True, exist_ok=True)

        repository = self.client.get(f"/repos/{owner}/{repo}")
        pulls = self.client.get(
            f"/repos/{owner}/{repo}/pulls", params={"state": "all", "per_page": 100}
        )
        issues = self.client.get(
            f"/repos/{owner}/{repo}/issues", params={"state": "all", "per_page": 100}
        )

        for name, payload in {
            "repository.json": repository,
            "pulls.json": pulls,
            "issues.json": issues,
        }.items():
            path = output_path / name
            with path.open("w", encoding="utf-8") as file_handle:
                json.dump(payload, file_handle, indent=2)

        logger.info("Saved raw payloads for %s/%s", owner, repo)
        return {"repository": repository, "pulls": pulls, "issues": issues}
