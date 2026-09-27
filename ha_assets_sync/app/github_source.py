from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

_REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_USER_AGENT = "ha-assets-sync/0.1"


class SourceError(RuntimeError):
    pass


def validate_repository(repository: str) -> str:
    repository = repository.strip()
    if not _REPOSITORY_RE.fullmatch(repository):
        raise SourceError("repository must be in owner/name form")
    return repository


def validate_branch(branch: str) -> str:
    branch = branch.strip()
    if not branch or branch.startswith("-") or any(ch.isspace() for ch in branch):
        raise SourceError("branch must be a non-empty Git ref without whitespace")
    return branch


def _request(url: str, *, timeout: int = 30) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": _USER_AGENT,
            "Accept": "application/vnd.github+json",
        },
    )


def resolve_revision(repository: str, branch: str, *, timeout: int = 30) -> str:
    repository = validate_repository(repository)
    branch = validate_branch(branch)
    encoded_branch = urllib.parse.quote(branch, safe="")
    url = f"https://api.github.com/repos/{repository}/commits/{encoded_branch}"

    try:
        with urllib.request.urlopen(_request(url, timeout=timeout), timeout=timeout) as response:
            payload = json.load(response)
    except Exception as exc:
        raise SourceError(f"failed to resolve GitHub revision: {exc}") from exc

    sha = payload.get("sha")
    if not isinstance(sha, str) or len(sha) != 40:
        raise SourceError("GitHub response did not contain a valid commit SHA")
    return sha


def download_archive(
    repository: str,
    revision: str,
    destination: Path,
    *,
    timeout: int = 60,
) -> None:
    repository = validate_repository(repository)
    if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        raise SourceError("revision must be a 40-character Git commit SHA")

    url = f"https://codeload.github.com/{repository}/tar.gz/{revision}"
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise SourceError(f"failed to download GitHub archive: {exc}") from exc
