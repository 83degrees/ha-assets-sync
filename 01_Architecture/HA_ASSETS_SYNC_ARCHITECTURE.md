# ha-assets-sync Architecture

## 1. Status and authority

This document is the authoritative implemented architecture for `ha-assets-sync`, established through ASTV-269 and implemented/validated through ASTV-268.

It describes the current product boundary and runtime architecture.

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

## 3. Implemented flow

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

The active mirror is fixed to `/config/www/ha-assets/`.

Safe same-filesystem activation also requires two fixed sibling paths:

- `/config/www/.ha-assets-sync-staging/` — transient activation staging;
- `/config/www/.ha-assets-sync-previous/` — transient rollback location.

These three paths form the complete product-owned write boundary. None is user-configurable.

Inside the app container, Home Assistant maps the host configuration directory to `/homeassistant`, so the implementation uses the corresponding container paths under `/homeassistant/www/`.

The runtime does not provide a general user-configurable destination capable of targeting `/config`, arbitrary `/config/www/` subtrees, secrets, or unrelated Home Assistant state.

Archive handling rejects unsafe members, including path traversal, absolute paths, symlinks, hardlinks, devices and FIFOs.

Downloaded content is treated as data only and is never executed.

## 5. Update semantics

The runtime resolves the configured branch to an exact Git commit, downloads and validates that complete candidate, and records the successfully installed revision in app-private persistent state.

Failure during acquisition, extraction, candidate validation, or staging leaves the currently active tree unchanged.

Activation is performed with same-filesystem renames: the current live tree is moved to the fixed previous path, the validated staged tree is moved into the live path, and the previous tree is removed only after activation succeeds. If activation fails after moving the live tree, the previous tree is restored.

The successfully installed source revision is recorded so unchanged revisions are detected without replacing the active tree unnecessarily.

## 6. Scheduling and operation

The runtime supports:

- sync on app start;
- configurable periodic refresh;
- exact-revision comparison so unchanged revisions do not replace the live tree;
- clear success, no-change and failure logging;
- app restart as the initial manual sync trigger.

A richer Home Assistant control surface is not required for v1.

## 7. Dependencies and boundaries

GitHub supplies public HTTPS archive delivery.

Home Assistant supplies the app/container runtime and filesystem mapping.

`ha-assets` remains the authoritative asset-content repository.

MediaCat and other consumers may use the resulting local paths but do not control replication.

## 8. Durable decision

The archive-based purpose-built replication decision is recorded in accepted `DDR-05-001 — Archive-based Home Assistant asset replication`.
