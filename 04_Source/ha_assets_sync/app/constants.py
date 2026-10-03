from pathlib import Path

HA_CONFIG_ROOT = Path("/homeassistant")
WWW_ROOT = HA_CONFIG_ROOT / "www"

LIVE_DIR = WWW_ROOT / "ha-assets"
STAGING_DIR = WWW_ROOT / ".ha-assets-sync-staging"
PREVIOUS_DIR = WWW_ROOT / ".ha-assets-sync-previous"

STATE_FILE = Path("/data/state.json")
OPTIONS_FILE = Path("/data/options.json")

EXPECTED_ROOT_ENTRY = "media-assets"

DEFAULT_REPOSITORY = "83degrees/ha-assets"
DEFAULT_BRANCH = "main"
DEFAULT_SYNC_INTERVAL = 3600
MIN_SYNC_INTERVAL = 300
MAX_SYNC_INTERVAL = 86400
