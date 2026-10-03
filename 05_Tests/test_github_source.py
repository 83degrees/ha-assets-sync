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

from github_source import SourceError, validate_branch, validate_repository


class GitHubSourceTests(unittest.TestCase):
    def test_valid_repository(self):
        self.assertEqual(validate_repository("83degrees/ha-assets"), "83degrees/ha-assets")

    def test_invalid_repository_rejected(self):
        for value in ("ha-assets", "../repo", "owner/repo/extra", ""):
            with self.subTest(value=value):
                with self.assertRaises(SourceError):
                    validate_repository(value)

    def test_invalid_branch_rejected(self):
        for value in ("", "bad branch", "-danger"):
            with self.subTest(value=value):
                with self.assertRaises(SourceError):
                    validate_branch(value)


if __name__ == "__main__":
    unittest.main()
