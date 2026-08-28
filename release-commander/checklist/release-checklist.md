# Release Readiness Checklist — 18 items

Release Commander evaluates these 18 items across six domains, run by six
parallel subagents.

## Security Sentinel
- [ ] **S1** — Dependencies scanned; no known critical/high CVEs
- [ ] **S2** — No secrets or credentials committed to the repo
- [ ] **S3** — Dependency versions are pinned and licenses are compatible

## Test Marshal
- [ ] **T1** — Full test suite passes on the release branch
- [ ] **T2** — No flaky tests (suite is repeat-run stable)
- [ ] **T3** — Coverage meets threshold (≥ 80%)

## Version & Changelog Clerk
- [ ] **V1** — Version bumped correctly (semver) and consistent across all manifests
- [ ] **V2** — CHANGELOG has an entry for this release
- [ ] **V3** — Release branch / git tag naming is correct

## Docs Curator
- [ ] **D1** — README quickstart matches the current setup
- [ ] **D2** — API/endpoint documentation is up to date
- [ ] **D3** — Docs reference the correct version and have no dead links

## Migration Auditor
- [ ] **M1** — Migrations are ordered and reversible
- [ ] **M2** — Migrations are tested (up and down)
- [ ] **M3** — No pending/unapplied migrations vs. the declared schema

## Env Drift Checker
- [ ] **E1** — Config keys are consistent across dev/staging/prod
- [ ] **E2** — No hardcoded secrets or env-specific values leaked
- [ ] **E3** — Feature flags / environment variables are documented

## Verdict

- **GO** — 0 `FAIL` and ≤ 2 `WARN`
- **NO-GO** — any `FAIL`, or > 2 `WARN`
