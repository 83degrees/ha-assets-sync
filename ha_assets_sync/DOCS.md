# HA Assets Sync

## Install on a Home Assistant instance

The custom app repository must be publicly readable because Home Assistant Supervisor clones custom repositories anonymously.

1. Open **Settings → Apps → Install app**.
2. Open the app-store menu and choose **Repositories**.
3. Add:
   ```text
   https://github.com/83degrees/ha-assets-sync
   ```
4. Return to the app store and open **HA Assets Sync** from **83degrees Home Assistant Apps**.
5. Install the app.
6. Keep the default configuration unless a different public source repository, branch/ref, or refresh interval is required.
7. Start the app.
8. Check the app log for either:
   - `Installed revision <sha>` on a new/changed source revision; or
   - `Already current at revision <sha>` when no update is required.

The app is configured to start automatically with Home Assistant. Restarting the app is the v1 manual "sync now" mechanism.

## Configuration

```yaml
repository: 83degrees/ha-assets
branch: main
sync_interval: 3600
```

- `repository`: public GitHub repository in `owner/name` form.
- `branch`: branch or Git ref to follow.
- `sync_interval`: refresh interval in seconds, minimum 300 and maximum 86400.

The destination is intentionally not configurable.

## Local serving

A source asset such as:

```text
media-assets/radio/images/128x128/classic-fm.png
```

is materialised at:

```text
/config/www/ha-assets/media-assets/radio/images/128x128/classic-fm.png
```

and served by Home Assistant as:

```text
/local/ha-assets/media-assets/radio/images/128x128/classic-fm.png
```

For a LAN check, append the `/local/ha-assets/...` path to that Home Assistant instance's normal local frontend origin.

## Refresh and update behaviour

On startup and every configured refresh interval, the app resolves the configured branch/ref to an exact Git commit.

If that revision is already installed and the live mirror exists, the app takes the no-change path and leaves the current tree in place.

If the source revision has changed, the app downloads and validates the complete new archive before replacing the active mirror. Whole-tree replacement means source deletions are also reflected locally.

## Failure behaviour

A failed download, archive validation, extraction or candidate validation leaves the currently active local tree unchanged.

During activation, the existing live tree is renamed to the fixed rollback path before the staged tree is renamed into place. If activation fails, the previous tree is restored.

Failures are logged by the app and do not make the downloaded repository content executable.
