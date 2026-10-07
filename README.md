# ha-assets-sync

Governed product repository for the Home Assistant asset replication component.

The Home Assistant App package is maintained at:

```text
04_Implementation/haos/source/apps/ha_assets_sync/
```

The root `repository.yaml` is the Home Assistant custom-repository manifest. Home Assistant Supervisor discovers the App's nested `config.yaml` recursively, so no duplicate root-level App package is required. Supervisor's authoritative store loader performs this discovery with `path.glob("**/config.*")` in [`supervisor/store/data.py`](https://github.com/home-assistant/supervisor/blob/main/supervisor/store/data.py).

Repository bootstrap is tracked by ASTV-269. The initial governed App repository
layout is tracked by ASTV-294, and migration to the current target-first
deployment architecture is tracked by ASTV-319.
