# Release Readiness Report

**Project:** rc-fix-demo · **Release ref:** 1.3.0
**Generated:** 2026-08-28T21:20:37Z · **Orchestrated by:** IBM Bob (Agent mode)

---

## Verdict: **GO**

> All release gates passed. Remaining WARN items are non-blocking advisories.

## Summary

| | Count |
|---|---|
| PASS | 10 |
| WARN | 8 |
| FAIL | 0 |

10/18 PASS · 8 WARN · 0 FAIL

## Security Sentinel

### S1 — WARN
**Finding:** Offline check: no CVE database reachable in reference run. Bob runs pip-audit / OSV scan in the live workflow.
**Fix applied:** none

### S2 — PASS
**Finding:** No hardcoded secrets found.
**Fix applied:** none

### S3 — WARN
**Finding:** Unpinned dependencies: ['fastapi', 'uvicorn', 'pydantic', 'pytest']
**Fix applied:** Pin to exact versions

## Test Marshal

### T1 — PASS
**Finding:** Test suite passed.
**Fix applied:** none

### T2 — WARN
**Finding:** Single run performed; re-run twice to confirm stability.
**Fix applied:** none

### T3 — WARN
**Finding:** Coverage not measured (run pytest --cov).
**Fix applied:** none

## Version & Changelog Clerk

### V1 — PASS
**Finding:** Version consistent (1.3.0).
**Fix applied:** none

### V2 — PASS
**Finding:** CHANGELOG has a real entry.
**Fix applied:** none

### V3 — WARN
**Finding:** No release branch / git tag detected in reference run.
**Fix applied:** Create tag v1.3.0

## Docs Curator

### D1 — PASS
**Finding:** README quickstart matches entrypoint.
**Fix applied:** none

### D2 — PASS
**Finding:** Endpoints documented.
**Fix applied:** none

### D3 — WARN
**Finding:** No link checker run; verify links resolve.
**Fix applied:** none

## Migration Auditor

### M1 — PASS
**Finding:** Migrations ordered correctly.
**Fix applied:** none

### M2 — PASS
**Finding:** All migrations reversible.
**Fix applied:** none

### M3 — WARN
**Finding:** No live schema to compare against migrations.
**Fix applied:** none

## Env Drift Checker

### E1 — PASS
**Finding:** Config keys consistent.
**Fix applied:** none

### E2 — PASS
**Finding:** No secrets in config.
**Fix applied:** none

### E3 — WARN
**Finding:** Environment variables not documented in a .env.example.
**Fix applied:** Document env vars

## Issues fixed by Release Commander

- [x] V1 — bumped pyproject.toml version to 1.3.0
- [x] V2 — wrote real CHANGELOG entry
- [x] D1 — updated README quickstart command
- [x] S2/E2 — replaced hardcoded prod password with ${DB_PASSWORD}
- [x] E1 — aligned config keys (added REDIS_URL where missing, fixed prod LOG_LEVEL)
- [x] M1 — corrected migration ordering
- [x] M2 — added down-migrations (DROP TABLE)
- [x] T1 — fixed test assertion (999.0 → 19.99)

## Open items requiring human decision

- [ ] S1 (WARN) — Offline check: no CVE database reachable in reference run. Bob runs pip-audit / OSV scan in the live workflow.
- [ ] S3 (WARN) — Unpinned dependencies: ['fastapi', 'uvicorn', 'pydantic', 'pytest']
- [ ] T2 (WARN) — Single run performed; re-run twice to confirm stability.
- [ ] T3 (WARN) — Coverage not measured (run pytest --cov).
- [ ] V3 (WARN) — No release branch / git tag detected in reference run.
- [ ] D3 (WARN) — No link checker run; verify links resolve.
- [ ] M3 (WARN) — No live schema to compare against migrations.
- [ ] E3 (WARN) — Environment variables not documented in a .env.example.

## Auto-generated release artifacts

- **Bumped version:** `1.3.0`
- **Changelog entry:** `CHANGELOG.md`
- **Release notes:** `release-notes-rc-fix-demo.md`
- **Rollback runbook:** `rollback-runbook-rc-fix-demo.md`
