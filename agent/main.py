"""Hosted check: read the Trase secret and return repository metadata."""

import json
import os

import httpx

from trase_os_sdk.secrets import create_secret_store_from_environment

SECRET_NAME = "github-repository-read"
OWNER = "rei-int"
REPO = "temperature-tool-doc-check"


def run() -> str:
    """Read github-repository-read on the worker and return repo metadata."""
    # Always the secret store, so a machine GITHUB_TOKEN cannot satisfy this check.
    token = create_secret_store_from_environment().get(SECRET_NAME).decode("utf-8").strip()
    if not token:
        raise ValueError("GitHub credential is empty")
    response = httpx.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "trase-docs-example",
        },
        timeout=15.0,
        follow_redirects=False,
    )
    response.raise_for_status()
    data = response.json()
    result = {
        "repository": data["full_name"],
        "private": data["private"],
        "archived": data["archived"],
        "last_push": data.get("pushed_at"),
        "url": data["html_url"],
        "credential_source": "secret-store",
        "github_token_env_set": "GITHUB_TOKEN" in os.environ,
        "internal_token_env_set": "TRASE_INTERNAL_TOKEN" in os.environ,
    }
    encoded = json.dumps(result)
    if token in encoded:
        raise RuntimeError("token leaked into the result")
    return encoded
