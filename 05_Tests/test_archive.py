import io
import tarfile
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1]
        / "04_Source"
        / "ha_assets_sync"
        / "app"
    ),
)

from archive import ArchiveError, extract_archive


class ArchiveTests(unittest.TestCase):
    def _archive(self, members):
        temp = tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False)
        temp.close()
        path = Path(temp.name)
        with tarfile.open(path, "w:gz") as archive:
            for name, data, kind in members:
                info = tarfile.TarInfo(name)
                if kind == "dir":
                    info.type = tarfile.DIRTYPE
                    archive.addfile(info)
                elif kind == "symlink":
                    info.type = tarfile.SYMTYPE
                    info.linkname = "../../escape"
                    archive.addfile(info)
                else:
                    payload = data.encode()
                    info.size = len(payload)
                    archive.addfile(info, io.BytesIO(payload))
        return path

    def test_extracts_single_root_and_strips_repository_directory(self):
        archive = self._archive([
            ("ha-assets-sha/", "", "dir"),
            ("ha-assets-sha/media-assets/", "", "dir"),
            ("ha-assets-sha/media-assets/test.txt", "ok", "file"),
        ])
        with tempfile.TemporaryDirectory() as temp:
            result = extract_archive(archive, Path(temp) / "extract")
            self.assertEqual((result / "media-assets" / "test.txt").read_text(), "ok")

    def test_rejects_path_traversal(self):
        archive = self._archive([
            ("ha-assets-sha/", "", "dir"),
            ("ha-assets-sha/../escape.txt", "bad", "file"),
        ])
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ArchiveError):
                extract_archive(archive, Path(temp) / "extract")

    def test_rejects_symlink(self):
        archive = self._archive([
            ("ha-assets-sha/", "", "dir"),
            ("ha-assets-sha/link", "", "symlink"),
        ])
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ArchiveError):
                extract_archive(archive, Path(temp) / "extract")


if __name__ == "__main__":
    unittest.main()
