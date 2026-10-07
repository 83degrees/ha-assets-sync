# PROJECT_PROFILE: ha-assets-sync

## Profile conformance

This profile contains the required product-profile subjects for the implemented `ha-assets-sync` product.

## Document status

- Governance state: current

## Product identity

- Product name: ha-assets-sync
- Repository: `83degrees/ha-assets-sync`
- Repository visibility: public
- DDR origin code: `05`

## Linear work routing

- Default Linear team: `ASTV`

## Purpose

`ha-assets-sync` provides a safe, repeatable Home Assistant-side mechanism for materialising the public `83degrees/ha-assets` repository into local static storage for serving under `/local/ha-assets/`.

## Scope

### In scope

- Acquiring the public `ha-assets` repository archive.
- Safe archive staging and validation.
- One-way materialisation into `/config/www/ha-assets/`.
- Safe replacement/rollback behaviour.
- Installed-revision tracking.
- Scheduled/startup synchronisation.
- Sync logging and failure reporting.
- Deployment/update mechanics for the Home Assistant app.

### Out of scope

- Authoring or ownership of the public asset content itself.
- MediaCat catalogue schema or artwork-resolution behaviour.
- GitHub Pages/public HTTPS hosting.
- Google Cast behaviour.
- General Home Assistant configuration GitOps.
- Synchronisation of arbitrary Home Assistant directories.

## Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes |
| --- | --- | --- | --- |
| Public static asset content | consumed | `ha-assets` | `83degrees/ha-assets` remains authoritative for asset content. |
| Home Assistant replication/materialisation mechanism | owned | `ha-assets-sync` | Owns archive acquisition, staging, validation, safe replacement, scheduling and logging. |
| Local replication write boundary | owned operational boundary | `ha-assets-sync` | Writes are hard-bound to `/config/www/ha-assets/`, `/config/www/.ha-assets-sync-staging/`, and `/config/www/.ha-assets-sync-previous/`. |
| MediaCat artwork metadata/resolution | external | MediaCat | MediaCat may consume local/public asset routes but does not own replication. |
| GitHub archive delivery | external | GitHub | Public HTTPS source for the selected repository revision. |
| Home Assistant runtime / Supervisor app platform | external | Home Assistant | Hosts the app and exposes the configured writable filesystem mapping. |

## Approved architecture location

- Approved architecture location: `01_Architecture/HA_ASSETS_SYNC_ARCHITECTURE.md`
- Architecture state: implemented/current
- Material DDRs: `DDR-05-001` (Accepted)

## Contracts provided

None currently.

## Contracts consumed

None currently.

## Product dependencies

| Dependency | Type | Owner | Governed interface/evidence | Required state | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| `83degrees/ha-assets` | data/repository | ha-assets | Public repository/archive | Selected branch archive available | Sync fails without modifying the active local tree. |
| GitHub HTTPS archive delivery | external service | GitHub | Public archive endpoint | Archive and selected revision retrievable | Sync fails and current local tree remains active. |
| Home Assistant app platform | platform | Home Assistant | Supervisor app/add-on runtime and filesystem mapping | App can run and access its hard-bound local destination | Failure remains within the app; Home Assistant Core continues operating. |

## Implementation namespace / naming identity

- Implementation namespace / naming identity: `ha-assets-sync`

| Identity | Classification | Owner | Permitted use | Evidence |
| --- | --- | --- | --- | --- |
| `ha-assets-sync` | owned | ha-assets-sync | Product/repository/app identity | This profile and architecture |
| `ha-assets` | external | ha-assets | Consumed repository/content identity only | `83degrees/ha-assets` |
| `/config/www/ha-assets/` and fixed sync siblings | owned operational boundary | ha-assets-sync | Hard-bound materialisation/staging/rollback paths | Architecture / DDR-05-001 |
| `/local/ha-assets/` | external serving projection | Home Assistant | Read-only consumer URL projection of the destination | Home Assistant static-file behaviour |

## Repository and App package layout

- Root `repository.yaml` is the required Home Assistant custom-repository manifest.
- The single authoritative App package is
  `04_Implementation/haos/source/apps/ha_assets_sync/**`.
- Home Assistant Supervisor recursively discovers
  `04_Implementation/haos/source/apps/ha_assets_sync/config.yaml` from the
  repository root.
- No duplicate deployable App package is maintained at repository root.
- App identity remains `ha_assets_sync`; versioning remains owned by the canonical nested `config.yaml`.
- There is no separate machine-consumed App repository packaging or release
  tooling. If introduced through governed work, it belongs under
  `04_Implementation/haos/packaging/apps/**`.
- Operator-facing deployment and recovery guidance is maintained at
  `08_Deployment/HA_ASSETS_SYNC_APP_DEPLOYMENT_RUNBOOK.md`.

## Deployable units

| Deployable unit | Type | Authoritative source | Target | Mechanism | Detailed authority |
| --- | --- | --- | --- | --- | --- |
| HA Assets Sync App | `haos_app` | `04_Implementation/haos/source/apps/ha_assets_sync/**` | Home Assistant OS App runtime on the selected managed instance | `app_repository` | `00_Governance/01_Central/01_Standards/HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md` |

No HACS integration, operator-managed HAOS configuration unit, HAOS managed-data
unit, static-asset publication unit, or Raspberry Pi OS package is deployed from
this repository. Root `repository.yaml` is the sole platform-required placement
exception; it is metadata, not a second deployable source tree.

## Production and evidence route

- Production route: `haos_app` deployment through the Home Assistant
  `app_repository` mechanism from the governed public custom repository to
  managed HA instances, initially `ha-starburst`, with `ha-shorefoot` as an
  additional intended target. Beta uses the branch-qualified
  `https://github.com/83degrees/ha-assets-sync#beta` route; stable uses
  `https://github.com/83degrees/ha-assets-sync` at the accepted stable state.
- Evidence route: governed repository state plus deployment/runtime evidence from the applicable Home Assistant instance.
- Secrets and mutable-state boundary: no GitHub credential is required for the
  public source; App configuration and mutable installed-revision/runtime state
  remain outside governed source and must be preserved across update or rollback.
- Validation evidence route: repository tests plus deployment/runtime evidence recorded against the governing Linear issue.
- Current deployment evidence: `ha-starburst` is running the app; first materialisation, local `/local/ha-assets/...` serving and repeated no-change checks have been observed under ASTV-268.
- Known limitation pending ASTV-268 closure: real-world propagation of a subsequent source-repository revision remains to be demonstrated.

## Current and target state summary

| Area | State | Statement | Authority/evidence |
| --- | --- | --- | --- |
| Product repository | current implemented | Public repository exists at `83degrees/ha-assets-sync`. | GitHub |
| Repository layout | current implemented | Root `repository.yaml` identifies the custom repository and the single authoritative App package resides at `04_Implementation/haos/source/apps/ha_assets_sync/**`, discoverable recursively by Supervisor. | ASTV-319 / repository layout tests |
| Replication runtime | current implemented | Purpose-built Home Assistant archive-based replication app is implemented and running on `ha-starburst`. | ASTV-268 runtime evidence |
| Local destination | current implemented | Destination is hard-bound to `/config/www/ha-assets/` with fixed sibling staging/rollback paths. | Architecture / implementation |
| Local serving | current implemented | Home Assistant serves replicated assets under `/local/ha-assets/...`; verified on `ha-starburst`. | ASTV-268 runtime evidence |
| Public asset authority | current implemented | `83degrees/ha-assets` remains authoritative for public static content. | ASTV-266 |
