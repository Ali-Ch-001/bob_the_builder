# Release Commander

An agentic release-readiness workflow built on **IBM Bob 2.0**. Bob acts as a
release orchestrator, spawns six specialist subagents in parallel, and produces a
single **GO / NO-GO** release report with auto-generated artifacts.

Built for the **IBM TechXchange 2026 Pre-conference Dev Day Hackathon**.

## The problem

Cutting a release is a 1–2 day manual checklist (tests, security, versions,
changelog, docs, migrations, config) — and a skipped item becomes a production
incident.

## The solution

Point Bob at a repo and a version. Bob (Agent mode) delegates six readiness
domains to parallel subagents, each owning three checks (18 total), fixes what it
can, and synthesizes a Release Readiness Report with a GO / NO-GO verdict.

| Subagent | Owns |
|---|---|
| Security Sentinel | S1 CVEs · S2 secrets · S3 licenses |
| Test Marshal | T1 tests · T2 flakiness · T3 coverage |
| Version & Changelog Clerk | V1 semver · V2 changelog · V3 tags |
| Docs Curator | D1 quickstart · D2 endpoints · D3 links |
| Migration Auditor | M1 order · M2 reversibility · M3 pending |
| Env Drift Checker | E1 key drift · E2 secrets · E3 flags |

## Layout

```
SPEC.md                     # single source of truth
sample-app/                 # the repo Release Commander operates on (seeded defects)
release-commander/
  orchestrator.md           # Bob Agent-mode orchestrator prompt
  subagents/                # six persona role files
  checklist/                # 18-item release checklist
  report-template.md        # GO / NO-GO report template
  release_commander.py      # runnable reference orchestrator
  reports/                  # generated reports (JSON + Markdown)
docs/                       # problem/solution, Bob usage, demo storyboard
```

## Run the reference pipeline

```bash
# Diagnose a release (emits a GO / NO-GO report)
python3 release-commander/release_commander.py --repo sample-app

# Auto-apply safe fixes and re-evaluate (flips NO-GO → GO, generates artifacts)
python3 release-commander/release_commander.py --repo sample-app --fix
```

Emits `release-commander/reports/release-readiness-{repo}.{md,json}` and, on GO,
`release-notes-{repo}.md` + `rollback-runbook-{repo}.md`.

## Test it

```bash
python -m pytest release-commander/tests/ -v
```

Requires `pytest`, `fastapi`, `httpx`, `pydantic`
(`pip install -r sample-app/requirements-dev.txt`). The tests prove the core
claim: the pipeline detects every seeded defect (NO-GO), then auto-fixes flip
the verdict to GO.

## How Bob is used

See [`docs/BOB_USAGE.md`](docs/BOB_USAGE.md) — Agent mode (orchestrator),
parallel tasks, six subagents, document understanding, and synthesis.
