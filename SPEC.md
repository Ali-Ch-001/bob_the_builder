# Release Commander — Project Specification (Single Source of Truth)

This document is the contract every artifact in this repository must follow.
If something is ambiguous, this file wins.

## 1. What we are building

**Release Commander** is an agentic release-readiness workflow built on IBM Bob 2.0.

- A single **orchestrator** (Bob in **Agent mode**) owns the release.
- The orchestrator spawns **six parallel subagents**, each responsible for one readiness domain.
- Each subagent performs checks, fixes what it can, and reports findings.
- The orchestrator **synthesizes** the six reports into a single **Release Readiness Report**
  with a **go / no-go** verdict and auto-generated release artifacts.

The repository also contains a **runnable reference implementation** (`release_commander.py`)
that emulates the six subagents as static checks, so the proof-of-concept works even
without an active Bob session. The Bob-driven version replaces each check with a real
subagent invocation.

## 2. The six subagent personas

| Persona | File | Domain | Owns checklist items |
|---|---|---|---|
| Security Sentinel | `release-commander/subagents/security-sentinel.md` | vulnerabilities, secrets, licenses | S1, S2, S3 |
| Test Marshal | `release-commander/subagents/test-marshal.md` | tests, flakiness, coverage | T1, T2, T3 |
| Version & Changelog Clerk | `release-commander/subagents/version-changelog-clerk.md` | semver, changelog, tags | V1, V2, V3 |
| Docs Curator | `release-commander/subagents/docs-curator.md` | docs freshness, accuracy | D1, D2, D3 |
| Migration Auditor | `release-commander/subagents/migration-auditor.md` | DB migrations order/reversibility | M1, M2, M3 |
| Env Drift Checker | `release-commander/subagents/env-drift-checker.md` | config drift, secrets, flags | E1, E2, E3 |

## 3. The 18-point release checklist

**Security Sentinel**
- S1 — Dependencies scanned; no known critical/high CVEs
- S2 — No secrets or credentials committed to the repo
- S3 — Dependency versions are pinned and licenses are compatible

**Test Marshal**
- T1 — Full test suite passes on the release branch
- T2 — No flaky tests (suite is repeat-run stable)
- T3 — Coverage meets threshold (>= 80%)

**Version & Changelog Clerk**
- V1 — Version bumped correctly (semver) and consistent across all manifests
- V2 — CHANGELOG has an entry for this release
- V3 — Release branch / git tag naming is correct

**Docs Curator**
- D1 — README quickstart matches the current setup
- D2 — API/endpoint documentation is up to date
- D3 — Docs reference the correct version and have no dead links

**Migration Auditor**
- M1 — Migrations are ordered and reversible
- M2 — Migrations are tested (up and down)
- M3 — No pending/unapplied migrations vs. the declared schema

**Env Drift Checker**
- E1 — Config keys are consistent across dev/staging/prod
- E2 — No hardcoded secrets or env-specific values leaked
- E3 — Feature flags / environment variables are documented

Each item has one of three statuses in the report: `PASS`, `WARN`, or `FAIL`.
A release is **GO** only if zero items are `FAIL`; `WARN` items are non-blocking
advisories that a human may choose to act on.

## 4. Repository layout

```
bob_the_builder/
├── README.md
├── SPEC.md
├── sample-app/                       # the "real" project Release Commander operates on
│   ├── pyproject.toml
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── src/app/__init__.py
│   ├── src/app/main.py
│   ├── src/app/models.py
│   ├── tests/test_app.py
│   ├── migrations/0001_create_orders.sql
│   ├── migrations/0003_add_customer_index.sql
│   ├── migrations/0002_add_users.sql
│   └── config/dev.env, staging.env, prod.env
├── release-commander/
│   ├── orchestrator.md
│   ├── subagents/ (six persona files)
│   ├── checklist/release-checklist.md
│   ├── report-template.md
│   └── release_commander.py          # runnable reference orchestrator
├── docs/
│   ├── PROBLEM_STATEMENT.md
│   ├── BOB_USAGE.md
│   └── DEMO_STORYBOARD.md
└── .gitignore
```

## 5. The sample app

A minimal **FastAPI "Acme Orders"** service (Python 3.11+, `pytest`).

Endpoints: `GET /health`, `GET /orders`, `POST /orders`.

## 6. Seeded defects (the demo payload)

The sample app ships in a deliberately "unready" state so the demo shows
Release Commander catching real problems. These defects are INTENTIONAL:

1. **V1 version mismatch** — `pyproject.toml` says `1.2.0`; `CHANGELOG.md` top entry says `1.3.0`.
2. **V2 missing changelog** — the `1.3.0` changelog entry is a placeholder with no real content.
3. **S2/E2 hardcoded secret** — `config/prod.env` contains a hardcoded `DATABASE_URL` password.
4. **E1 config drift** — `prod.env` has `LOG_LEVEL=debug` and a `REDIS_URL` key missing from `staging.env`.
5. **M1 migration ordering** — migration files are numbered `0001`, `0003`, `0002` (out of order).
6. **D1 stale docs** — README quickstart references an outdated command (`uvicorn main:app`) that no longer matches the real entrypoint.
7. **T1 failing test** — one test is written against the wrong expected value and fails.
8. **M2 untested migration** — the down-migration for `0002_add_users.sql` is missing (no `DROP TABLE`).

These map 1:1 to checklist items so the report is crisp: 8 seeded findings across
5 of 6 domains, exactly the "manual checklist missed this" narrative.

## 7. The report

Generated at `release-commander/reports/release-readiness-<ref>.md`.

Structure (matches `report-template.md`):
- Header: project, release ref, timestamp, verdict badge (`GO` / `NO-GO`)
- Summary line: `X/18 PASS, Y WARN, Z FAIL`
- Per-domain sections with each item's status + finding + fix applied
- "Issues fixed by Release Commander" list
- "Open items requiring human decision" list
- Auto-generated artifacts: bumped version, changelog entry, release notes, rollback runbook

## 8. Verdict rules

- `GO` when 0 FAIL (WARN items are non-blocking advisories).
- `NO-GO` otherwise. The report must always explain what a human must do to flip to GO.

## 9. Non-negotiables

- Python 3.11+, no non-stdlib dependencies except `fastapi`, `uvicorn`, `pydantic`, `pytest`.
- All findings reference file + line/checklist item.
- No secrets are ever written to a real config; the seeded "secret" is an obvious fake.
- Keep the whole thing runnable with: `python release_commander.py --repo ../sample-app`.
