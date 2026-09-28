import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ha_assets_sync" / "app"))

from install import (
    InstallError,
    InstallPaths,
    activate_staging,
    load_state,
    prepare_staging,
    save_state,
    validate_candidate,
)


class InstallTests(unittest.TestCase):
    def test_candidate_requires_media_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp) / "candidate"
            candidate.mkdir()
            with self.assertRaises(InstallError):
                validate_candidate(candidate, "media-assets")

            (candidate / "media-assets").mkdir()
            validate_candidate(candidate, "media-assets")

    def test_activation_replaces_tree_and_reflects_deletions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            live = root / "ha-assets"
            staging = root / ".staging"
            previous = root / ".previous"
            candidate = root / "candidate"

            (live / "media-assets").mkdir(parents=True)
            (live / "media-assets" / "old.txt").write_text("old")

            (candidate / "media-assets").mkdir(parents=True)
            (candidate / "media-assets" / "new.txt").write_text("new")

            paths = InstallPaths(live=live, staging=staging, previous=previous)
            prepare_staging(candidate, paths)
            activate_staging(paths)

            self.assertFalse((live / "media-assets" / "old.txt").exists())
            self.assertEqual((live / "media-assets" / "new.txt").read_text(), "new")
            self.assertFalse(previous.exists())

    def test_activation_failure_restores_previous_live_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            live = root / "ha-assets"
            staging = root / ".staging"
            previous = root / ".previous"
            candidate = root / "candidate"

            (live / "media-assets").mkdir(parents=True)
            (live / "media-assets" / "old.txt").write_text("old")

            (candidate / "media-assets").mkdir(parents=True)
            (candidate / "media-assets" / "new.txt").write_text("new")

            paths = InstallPaths(live=live, staging=staging, previous=previous)
            prepare_staging(candidate, paths)

            original_rename = Path.rename

            def controlled_rename(path, target):
                if path == staging:
                    raise OSError("simulated activation failure")
                return original_rename(path, target)

            with patch.object(Path, "rename", new=controlled_rename):
                with self.assertRaises(InstallError):
                    activate_staging(paths)

            self.assertTrue((live / "media-assets" / "old.txt").exists())
            self.assertFalse((live / "media-assets" / "new.txt").exists())
            self.assertFalse(previous.exists())

    def test_state_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "state.json"
            revision = "a" * 40
            save_state(state, revision)
            self.assertEqual(load_state(state), revision)
            self.assertEqual(json.loads(state.read_text())["installed_revision"], revision)


if __name__ == "__main__":
    unittest.main()
