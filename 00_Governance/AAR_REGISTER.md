# AAR Register — ha-assets-sync

## 2026-10-03 — Root-level Home Assistant App package obscured the governed source boundary

- Source issue/task: ASTV-292; product remediation ASTV-294
- Observation: The App package was initially stored at repository root even though the canonical governed implementation location is `04_Source/**`. The placement was chosen under the mistaken assumption that Home Assistant Supervisor required a root-level App directory.
- Practical impact: Runtime source sat outside the standard implementation boundary, the central path-based Beta routing check could not identify it as runtime-affecting, and the repository appeared to require a duplicate or exceptional deployment layout.
- Recommendation: Keep only the Home Assistant repository manifest at root, maintain the single authoritative App package under `04_Source/<app>/**`, and guard Supervisor-compatible recursive discovery and package uniqueness with repository tests.
- Status: Promoted
- Central follow-up reference: ASTV-292
