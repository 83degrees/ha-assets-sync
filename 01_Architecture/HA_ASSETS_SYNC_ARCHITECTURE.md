# ha-assets-sync Architecture

## 1. Status and authority

This document is the proposed authoritative architecture for `ha-assets-sync`, established through ASTV-269 and intended to govern the runtime implementation tracked by ASTV-268 once accepted.

It describes the product boundary and target architecture. It must not be read as evidence that the runtime is already implemented or deployed.

## 2. Product responsibility

`ha-assets-sync` owns the Home Assistant-side materialisation of the public `83degrees/ha-assets` repository into the dedicated local static subtree:

```text
/config/www/ha-assets/
```

Home Assistant exposes that subtree to consumers as:

```text
/local/ha-assets/
```

The product does not own the asset content, MediaCat catalogue semantics, GitHub Pages delivery, or Google Cast behaviour.

## 3. Target flow

```text
83degrees/ha-assets
        |
        | public GitHub archive for selected branch/revision
        v
ha-assets-sync app
        |
        | download to isolated staging area
        v
archive validation
        |
        | safe extraction / tree validation
        v
staged candidate
        |
        | safe replacement
        v
/config/www/ha-assets/
        |
        v
/local/ha-assets/
```

## 4. Safety boundary

The live destination is fixed to `/config/www/ha-assets/`.

The runtime must not provide a general user-configurable destination capable of targeting `/config`, arbitrary `/config/www/` subtrees, secrets, or unrelated Home Assistant state.

Archive handling must reject unsafe members, including path traversal and absolute paths, and must prevent symlink-based escape from the staging boundary.

Downloaded content is treated as data only and is never executed.

## 5. Update semantics

The runtime downloads and validates a complete candidate before replacing the active tree.

Failure during acquisition, extraction, or validation leaves the currently active tree unchanged.

The implementation may retain one previous tree if required to make final replacement/restoration safe.

The successfully installed source revision should be recorded so unchanged revisions can be detected without replacing the active tree unnecessarily.

## 6. Scheduling and operation

The target runtime supports:

- sync on app start;
- configurable periodic refresh;
- clear success, no-change and failure logging;
- app restart as the initial manual sync trigger.

A richer Home Assistant control surface is not required for v1.

## 7. Dependencies and boundaries

GitHub supplies public HTTPS archive delivery.

Home Assistant supplies the app/container runtime and filesystem mapping.

`ha-assets` remains the authoritative asset-content repository.

MediaCat and other consumers may use the resulting local paths but do not control replication.

## 8. Durable decision

The selection of an archive-based purpose-built replicator over GitOps, rclone/cloud intermediary, Syncthing and per-file manifest/downloader approaches is material and is to be captured by the product DDR created under ASTV-268.
