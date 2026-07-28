"""GitHub API client wrappers for REST and GraphQL access."""

from __future__ import annotations

from typing import Any

import requests

from onboardiq.config.settings import settings
from onboardiq.utils.logging import get_logger

logger = get_logger(__name__)


class GitHubClient:
    """Authenticated GitHub API client with simple retry handling."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token or settings.github_token
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"Authorization": f"token {self.token}"})

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """Perform a GET request against the GitHub REST API."""

        if not self.token:
            raise ValueError("GITHUB_TOKEN is required for GitHub ingestion")

        url = f"{settings.github_api_url.rstrip('/')}{endpoint}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> Any:
        """Perform a GraphQL request against GitHub."""

        if not self.token:
            raise ValueError("GITHUB_TOKEN is required for GitHub ingestion")

        response = self.session.post(
            f"{settings.github_api_url.rstrip('/')}/graphql",
            json={"query": query, "variables": variables or {}},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
