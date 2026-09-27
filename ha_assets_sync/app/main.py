from __future__ import annotations

import json
import logging
import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from archive import ArchiveError, extract_archive
from constants import (
    DEFAULT_BRANCH,
    DEFAULT_REPOSITORY,
    DEFAULT_SYNC_INTERVAL,
    EXPECTED_ROOT_ENTRY,
    LIVE_DIR,
    MAX_SYNC_INTERVAL,
    MIN_SYNC_INTERVAL,
    OPTIONS_FILE,
    PREVIOUS_DIR,
    STAGING_DIR,
    STATE_FILE,
)
from github_source import SourceError, resolve_revision, download_archive
from install import (
    InstallError,
    InstallPaths,
    activate_staging,
    load_state,
    prepare_staging,
    save_state,
    validate_candidate,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
LOGGER = logging.getLogger("ha-assets-sync")


@dataclass(frozen=True)
class Options:
    repository: str
    branch: str
    sync_interval: int


def load_options(path: Path = OPTIONS_FILE) -> Options:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        payload = {}

    interval = int(payload.get("sync_interval", DEFAULT_SYNC_INTERVAL))
    if not MIN_SYNC_INTERVAL <= interval <= MAX_SYNC_INTERVAL:
        raise ValueError(
            f"sync_interval must be between {MIN_SYNC_INTERVAL} and {MAX_SYNC_INTERVAL} seconds"
        )

    return Options(
        repository=str(payload.get("repository", DEFAULT_REPOSITORY)),
        branch=str(payload.get("branch", DEFAULT_BRANCH)),
        sync_interval=interval,
    )


def sync_once(options: Options) -> bool:
    revision = resolve_revision(options.repository, options.branch)
    installed = load_state(STATE_FILE)

    if installed == revision and LIVE_DIR.is_dir():
        LOGGER.info("Already current at revision %s", revision)
        return False

    paths = InstallPaths(
        live=LIVE_DIR,
        staging=STAGING_DIR,
        previous=PREVIOUS_DIR,
    )

    with tempfile.TemporaryDirectory(prefix="ha-assets-sync-", dir="/data") as work:
        workdir = Path(work)
        archive = workdir / "source.tar.gz"
        extracted = workdir / "extracted"

        LOGGER.info("Downloading %s at %s", options.repository, revision)
        download_archive(options.repository, revision, archive)
        candidate = extract_archive(archive, extracted)
        validate_candidate(candidate, EXPECTED_ROOT_ENTRY)

        prepare_staging(candidate, paths)
        activate_staging(paths)
        save_state(STATE_FILE, revision)

    LOGGER.info("Installed revision %s", revision)
    return True


def main() -> int:
    options = load_options()
    LOGGER.info(
        "Starting HA Assets Sync: repository=%s branch=%s interval=%ss",
        options.repository,
        options.branch,
        options.sync_interval,
    )

    while True:
        try:
            sync_once(options)
        except (ArchiveError, InstallError, SourceError, OSError, ValueError) as exc:
            LOGGER.error("Sync failed: %s", exc)
        except Exception:
            LOGGER.exception("Unexpected sync failure")

        time.sleep(options.sync_interval)


if __name__ == "__main__":
    raise SystemExit(main())
