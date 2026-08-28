# Release Readiness Report

**Project:** sample-app · **Release ref:** 1.3.0
**Generated:** 2026-08-28T21:24:56Z · **Orchestrated by:** IBM Bob (Agent mode)

---

## Verdict: **NO-GO**

> Blocking issues found. See FAIL items below.

## Summary

| | Count |
|---|---|
| PASS | 1 |
| WARN | 8 |
| FAIL | 9 |

1/18 PASS · 8 WARN · 9 FAIL

## Security Sentinel

### S1 — WARN
**Finding:** Offline check: no CVE database reachable in reference run. Bob runs pip-audit / OSV scan in the live workflow.
**Fix applied:** none

### S2 — FAIL
**Finding:** Hardcoded credentials detected:
  config/prod.env:3 — DATABASE_URL=postgres://***:***@prod-db:5432/orders
**Fix applied:** Replace with env placeholder ${DB_PASSWORD}

### S3 — WARN
**Finding:** Unpinned dependencies: ['fastapi', 'uvicorn', 'pydantic', 'pytest']
**Fix applied:** Pin to exact versions

## Test Marshal

### T1 — FAIL
**Finding:** Test suite failed:
assert response.status_code == 200
>       assert response.json()["total"] == 999.0
E       assert 19.99 == 999.0
tests/test_app.py:36: AssertionError
FAILED tests/test_app.py::test_create_order_total - assert 19.99 == 999.0
1 failed, 3 passed in 0.40s
**Fix applied:** Fix failing test(s)

### T2 — WARN
**Finding:** Single run performed; re-run twice to confirm stability.
**Fix applied:** none

### T3 — WARN
**Finding:** Coverage not measured (run pytest --cov).
**Fix applied:** none

## Version & Changelog Clerk

### V1 — FAIL
**Finding:** Version mismatch: pyproject=1.2.0 vs CHANGELOG=1.3.0
**Fix applied:** Bump pyproject.toml to 1.3.0

### V2 — FAIL
**Finding:** CHANGELOG entry for 1.3.0 is a placeholder (no real notes).
**Fix applied:** Write real change notes for 1.3.0

### V3 — WARN
**Finding:** No release branch / git tag detected in reference run.
**Fix applied:** Create tag v1.3.0

## Docs Curator

### D1 — FAIL
**Finding:** README quickstart uses outdated `uvicorn main:app`; real entrypoint is `uvicorn app.main:app`.
**Fix applied:** Update README quickstart command

### D2 — PASS
**Finding:** Endpoints documented.
**Fix applied:** none

### D3 — WARN
**Finding:** No link checker run; verify links resolve.
**Fix applied:** none

## Migration Auditor

### M1 — FAIL
**Finding:** Migrations out of order: 0002_add_users.sql depends on 0003
**Fix applied:** Reorder migrations to sequential order

### M2 — FAIL
**Finding:** Missing down-migrations: 0001_create_orders.sql (no DROP TABLE orders); 0002_add_users.sql (no DROP TABLE users)
**Fix applied:** Add reversible down-migration

### M3 — WARN
**Finding:** No live schema to compare against migrations.
**Fix applied:** none

## Env Drift Checker

### E1 — FAIL
**Finding:** Key drift: REDIS_URL only in ['prod.env']; Suspicious prod values: LOG_LEVEL=debug
**Fix applied:** Align config keys/values across environments

### E2 — FAIL
**Finding:** Secrets in config: prod.env: DATABASE_URL=postgres://***:***@prod-db:5432/orders
**Fix applied:** Move to secret manager / env placeholder

### E3 — WARN
**Finding:** Environment variables not documented in a .env.example.
**Fix applied:** Document env vars

## Issues fixed by Release Commander

- [ ] S2 — Replace with env placeholder ${DB_PASSWORD}
- [ ] S3 — Pin to exact versions
- [ ] T1 — Fix failing test(s)
- [ ] V1 — Bump pyproject.toml to 1.3.0
- [ ] V2 — Write real change notes for 1.3.0
- [ ] V3 — Create tag v1.3.0
- [ ] D1 — Update README quickstart command
- [ ] M1 — Reorder migrations to sequential order
- [ ] M2 — Add reversible down-migration
- [ ] E1 — Align config keys/values across environments
- [ ] E2 — Move to secret manager / env placeholder
- [ ] E3 — Document env vars

## Open items requiring human decision

- [ ] S1 (WARN) — Offline check: no CVE database reachable in reference run. Bob runs pip-audit / OSV scan in the live workflow.
- [ ] S2 (FAIL) — Hardcoded credentials detected:
- [ ] S3 (WARN) — Unpinned dependencies: ['fastapi', 'uvicorn', 'pydantic', 'pytest']
- [ ] T1 (FAIL) — Test suite failed:
- [ ] T2 (WARN) — Single run performed; re-run twice to confirm stability.
- [ ] T3 (WARN) — Coverage not measured (run pytest --cov).
- [ ] V1 (FAIL) — Version mismatch: pyproject=1.2.0 vs CHANGELOG=1.3.0
- [ ] V2 (FAIL) — CHANGELOG entry for 1.3.0 is a placeholder (no real notes).
- [ ] V3 (WARN) — No release branch / git tag detected in reference run.
- [ ] D1 (FAIL) — README quickstart uses outdated `uvicorn main:app`; real entrypoint is `uvicorn app.main:app`.
- [ ] D3 (WARN) — No link checker run; verify links resolve.
- [ ] M1 (FAIL) — Migrations out of order: 0002_add_users.sql depends on 0003
- [ ] M2 (FAIL) — Missing down-migrations: 0001_create_orders.sql (no DROP TABLE orders); 0002_add_users.sql (no DROP TABLE users)
- [ ] M3 (WARN) — No live schema to compare against migrations.
- [ ] E1 (FAIL) — Key drift: REDIS_URL only in ['prod.env']; Suspicious prod values: LOG_LEVEL=debug
- [ ] E2 (FAIL) — Secrets in config: prod.env: DATABASE_URL=postgres://***:***@prod-db:5432/orders
- [ ] E3 (WARN) — Environment variables not documented in a .env.example.

## Auto-generated release artifacts

- **Bumped version:** `1.3.0`
- **Changelog entry:** `CHANGELOG.md`
- **Release notes:** `release-notes-sample-app.md`
- **Rollback runbook:** `rollback-runbook-sample-app.md`
