from __future__ import annotations

import shutil
import tarfile
from pathlib import Path, PurePosixPath


class ArchiveError(RuntimeError):
    pass


def _validated_relative_path(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        raise ArchiveError(f"unsafe archive path: {name}")
    if not path.parts:
        raise ArchiveError("archive contains an empty path")
    return path


def extract_archive(archive_path: Path, extraction_root: Path) -> Path:
    if extraction_root.exists():
        shutil.rmtree(extraction_root)
    extraction_root.mkdir(parents=True)

    top_levels: set[str] = set()

    try:
        with tarfile.open(archive_path, mode="r:gz") as archive:
            for member in archive.getmembers():
                path = _validated_relative_path(member.name)
                top_levels.add(path.parts[0])

                if member.issym() or member.islnk() or member.isdev() or member.isfifo():
                    raise ArchiveError(f"unsupported archive member type: {member.name}")
                if not (member.isdir() or member.isreg()):
                    raise ArchiveError(f"unsupported archive member: {member.name}")

            if len(top_levels) != 1:
                raise ArchiveError("archive must contain exactly one top-level directory")

            top_level = next(iter(top_levels))

            for member in archive.getmembers():
                path = _validated_relative_path(member.name)
                relative_parts = path.parts[1:]
                if not relative_parts:
                    continue

                destination = extraction_root.joinpath(*relative_parts)
                resolved_parent = destination.parent.resolve()
                if extraction_root.resolve() not in (resolved_parent, *resolved_parent.parents):
                    raise ArchiveError(f"archive path escapes extraction root: {member.name}")

                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                    continue

                destination.parent.mkdir(parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    raise ArchiveError(f"unable to read archive member: {member.name}")
                with source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output)

    except (tarfile.TarError, OSError) as exc:
        raise ArchiveError(f"failed to extract archive: {exc}") from exc

    return extraction_root
