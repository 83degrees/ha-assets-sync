import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = REPOSITORY_ROOT / "04_Source" / "ha_assets_sync"


class RepositoryLayoutTests(unittest.TestCase):
    def test_repository_metadata_remains_at_root(self):
        self.assertTrue((REPOSITORY_ROOT / "repository.yaml").is_file())

    def test_supervisor_recursive_discovery_finds_one_app(self):
        # Mirrors Supervisor StoreData._find_app_configs(), which recursively
        # searches a custom repository with path.glob("**/config.*").
        configs = [
            path
            for path in REPOSITORY_ROOT.glob("**/config.yaml")
            if not any(part.startswith(".") or part == "rootfs" for part in path.parts)
        ]
        self.assertEqual(configs, [APP_ROOT / "config.yaml"])

    def test_app_identity_and_version_are_preserved(self):
        config = (APP_ROOT / "config.yaml").read_text(encoding="utf-8")
        self.assertIn('slug: "ha_assets_sync"', config)
        self.assertIn('version: "0.1.0"', config)

    def test_complete_app_package_uses_canonical_location(self):
        for relative_path in (
            "config.yaml",
            "Dockerfile",
            "run.sh",
            "app/main.py",
        ):
            with self.subTest(relative_path=relative_path):
                self.assertTrue((APP_ROOT / relative_path).is_file())

        self.assertFalse((REPOSITORY_ROOT / "ha_assets_sync").exists())


if __name__ == "__main__":
    unittest.main()
