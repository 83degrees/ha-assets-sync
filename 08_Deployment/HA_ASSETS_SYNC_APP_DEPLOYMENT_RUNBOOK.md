# HA Assets Sync App deployment runbook

## Scope and authority

This runbook covers installation, update, validation and rollback of the
`ha_assets_sync` Home Assistant App through the governed custom App repository.
It implements the Home Assistant App Deployment Standard but does not itself
authorise deployment, Beta entry, stable promotion or rollback.

The deployable unit is:

| Field | Value |
| --- | --- |
| Type | `haos_app` |
| Authoritative source | `04_Implementation/haos/source/apps/ha_assets_sync/**` |
| Mechanism | `app_repository` |
| App slug | `ha_assets_sync` |
| Beta repository source | `https://github.com/83degrees/ha-assets-sync#beta` |
| Stable repository source | `https://github.com/83degrees/ha-assets-sync` |

The repository is intentionally public, so this product does not use a
temporary-public deployment window.

## Preflight

Before an install or update, record the governing Linear issue and confirm:

- the target Home Assistant instance and release channel are authorised;
- the selected repository source and branch resolve to the intended Git
  candidate;
- root `repository.yaml` and the recursively discovered App `config.yaml` are
  valid;
- App slug `ha_assets_sync` and its version identify the intended candidate;
- the App package, build inputs and dependencies are publicly obtainable;
- current App configuration and App-private `/data` state have a usable backup
  or preservation route;
- the prior working Git candidate, repository source and App version are known;
  and
- the active `/config/www/ha-assets/` tree is not removed as part of the update.

## Install or update

1. In **Settings → Apps → Install app → Repositories**, add or refresh the
   authorised Beta or stable repository source shown above.
2. Verify that Home Assistant selected the expected source, branch and App
   version.
3. Install or update **HA Assets Sync** without removing its repository source,
   App configuration or App-private data.
4. Start the App and inspect its log.
5. Record the target instance, repository source, selected branch, App version,
   Git candidate, operation result and observation time against the Linear issue.

## Validation

For the exact deployed candidate, confirm:

- the App starts successfully;
- the log reports `Installed revision <sha>` for a changed source or
  `Already current at revision <sha>` for an unchanged source;
- `/config/www/ha-assets/` remains the active fixed destination;
- a representative asset is served through `/local/ha-assets/...`;
- a repeated no-change run leaves the active tree in place; and
- App configuration and App-private state remain available.

Record the result and sufficient running-version or deployed-content evidence
to bind the running App to the intended Git candidate.

## Failure and rollback

If repository refresh, build, install, update, start-up or candidate verification
fails, do not claim success or promote the candidate. Preserve diagnostics
without secrets and prefer repair or rollback that keeps the existing Supervisor
repository/App identity and App-private data.

With explicit rollback authority, restore the recorded prior working repository
source, Git candidate and App version. Reverify the installed version, running
state, App configuration, App-private data and active asset tree. Removing and
re-adding the repository or reinstalling the App is not a default rollback
because it may detach the App identity or discard private data.
