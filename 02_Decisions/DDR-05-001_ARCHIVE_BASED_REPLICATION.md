# DDR-05-001 — Archive-based Home Assistant asset replication

## Status

Proposed

## Decision

Implement `ha-assets-sync` as a purpose-built Home Assistant app that resolves a configured public GitHub branch to an exact commit, downloads that revision as a public GitHub archive, validates and stages the complete tree, and safely replaces a fixed local Home Assistant asset mirror.

The app owns only three fixed writable paths in the Home Assistant configuration mount:

- `/config/www/ha-assets/` — active mirror;
- `/config/www/.ha-assets-sync-staging/` — same-filesystem activation staging;
- `/config/www/.ha-assets-sync-previous/` — temporary rollback location.

The destination paths are not user-configurable.

## Context

The shared `83degrees/ha-assets` repository already provides predictable public HTTPS delivery through GitHub Pages. Home Assistant instances also require a local mirror so consumers can use `/local/ha-assets/...`.

Existing approaches investigated included the official Git pull app, generic GitOps tools, Syncthing, rclone/cloud intermediaries, and per-file Downloader/manifest materialisation.

The solution needs exact-tree replication, deletion semantics, safe failure behaviour, multiple-instance reuse, and a hard safety boundary around Home Assistant configuration.

A same-filesystem directory swap requires sibling staging/rollback paths; restricting all writes to the live directory alone would prevent a safe rename-based replacement.

## Alternatives considered

### Official Home Assistant Git pull app

Rejected because it is designed around the broader Home Assistant configuration tree and does not provide the narrow destination safety model required here.

### Generic Git/GitOps tooling

Rejected because it introduces a Git working tree and broader operational surface for a problem that only requires one-way materialisation.

### Syncthing

Rejected because GitHub is not a Syncthing peer and another synchronisation host would be required.

### rclone / cloud intermediary

Rejected because direct whole-tree replication from GitHub Pages is not clean and a Box/Dropbox/OneDrive intermediary would add authentication and another authority/dependency.

### Per-file Downloader / manifest

Rejected for v1 because tree enumeration, deletion semantics and manifest maintenance would add complexity compared with downloading an exact repository archive.

## Rationale

A public branch archive:

- requires no Git client;
- requires no credentials for the public source;
- represents the complete repository revision;
- naturally supports exact-mirror deletion semantics;
- can be validated before activation;
- keeps the Home Assistant runtime small and purpose-built;
- allows the installed source revision to be recorded exactly.

A separate Home Assistant app provides a stronger failure and dependency boundary than running this file-management logic inside Home Assistant Core.

## Consequences / trade-offs

- The app depends on GitHub API/archive availability.
- Unauthenticated GitHub API rate limits apply.
- The app has a writable `homeassistant_config` mapping, so the implementation must enforce the fixed path boundary itself.
- Safe activation requires two fixed sibling paths under `/config/www`, expanding the owned write boundary beyond the live directory while still preventing arbitrary destinations.
- Archive symlinks, hardlinks, devices and FIFOs are rejected rather than reproduced.
- The first implementation is specific to GitHub public repositories rather than a generic sync engine.

## Source Linear issue

`ASTV-268`

## Supersedes

Not applicable
