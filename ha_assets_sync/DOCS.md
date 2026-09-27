# HA Assets Sync

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

## Failure behaviour

A failed download, archive validation, extraction or candidate validation leaves the currently active local tree unchanged.

During activation, the existing live tree is renamed to the fixed rollback path before the staged tree is renamed into place. If activation fails, the previous tree is restored.
