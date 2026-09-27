# HA Assets Sync

Home Assistant app that safely materialises the public `83degrees/ha-assets` repository into local static storage.

## Runtime behaviour

- Resolves the configured public GitHub branch to an exact commit SHA.
- Downloads that revision as a GitHub tar archive.
- Validates archive paths and rejects links/devices/unsafe members.
- Extracts into private app staging under `/data`.
- Validates that the expected `media-assets/` tree exists.
- Copies the candidate into a fixed same-filesystem staging directory.
- Swaps the staged tree into `/config/www/ha-assets/` using fixed rollback paths.
- Records the installed revision in app-private persistent state.
- Skips replacement when the exact revision is already installed.

The writable Home Assistant paths are deliberately fixed:

- `/config/www/ha-assets/`
- `/config/www/.ha-assets-sync-staging/`
- `/config/www/.ha-assets-sync-previous/`

No arbitrary destination is configurable.
