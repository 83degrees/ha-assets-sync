from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path


class InstallError(RuntimeError):
    pass


@dataclass(frozen=True)
class InstallPaths:
    live: Path
    staging: Path
    previous: Path


def _remove(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.exists():
        shutil.rmtree(path)


def validate_candidate(candidate: Path, expected_root_entry: str) -> None:
    if not candidate.is_dir():
        raise InstallError("candidate tree is not a directory")
    expected = candidate / expected_root_entry
    if not expected.is_dir():
        raise InstallError(f"candidate is missing required '{expected_root_entry}/' directory")


def prepare_staging(candidate: Path, paths: InstallPaths) -> None:
    _remove(paths.staging)
    paths.staging.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(candidate, paths.staging, symlinks=False)


def activate_staging(paths: InstallPaths) -> None:
    _remove(paths.previous)

    had_live = paths.live.exists() or paths.live.is_symlink()
    if had_live:
        paths.live.rename(paths.previous)

    try:
        paths.staging.rename(paths.live)
    except Exception as exc:
        if had_live and paths.previous.exists() and not paths.live.exists():
            paths.previous.rename(paths.live)
        raise InstallError(f"failed to activate staged tree: {exc}") from exc

    _remove(paths.previous)


def save_state(path: Path, revision: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps({"installed_revision": revision}) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_state(path: Path) -> str | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError):
        return None

    revision = payload.get("installed_revision")
    return revision if isinstance(revision, str) else None
