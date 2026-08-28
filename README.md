# Release Commander

An agentic release-readiness workflow built on **IBM Bob 2.0**. Point it at any
repository and it runs 18 release-gate checks across six parallel subagent
domains, auto-fixes what it can, and produces a **GO / NO-GO Release Readiness
Report** plus generated release notes and a rollback runbook.

> Built for the IBM TechXchange 2026 Pre-conference Dev Day Hackathon.

---

## Install

Requires Python 3.10+.

```bash
# Option A — pip install (recommended)
pip install .
release-commander --help

# Option B — run straight from the repo, no install
bin/release-commander --help

# Option C — one-line installer (editable install)
bash install.sh
```

## Use

```bash
# Diagnose a release (checks the current directory by default)
release-commander --repo /path/to/your/repo

# Auto-apply safe fixes, re-evaluate, emit artifacts on GO
release-commander --repo /path/to/your/repo --fix

# Pin the release version and output directory
release-commander --repo . --release-ref 2.1.0 --outdir ./reports --fix
```

A run writes to the output directory (default `./release-commander-reports/`):

- `release-readiness-<repo>.md` / `.json` — the full report
- `release-notes-<repo>.md`
- `rollback-runbook-<repo>.md`

Exit code is `0` on **GO** and `1` on **NO-GO**, so it drops straight into CI.

## What it checks (18 gates · 6 domains)

| Subagent | Items | Domain |
|---|---|---|
| Security Sentinel | S1 · S2 · S3 | CVEs · secrets · licenses |
| Test Marshal | T1 · T2 · T3 | tests · flakiness · coverage |
| Version & Changelog Clerk | V1 · V2 · V3 | semver · changelog · tags |
| Docs Curator | D1 · D2 · D3 | quickstart · endpoints · links |
| Migration Auditor | M1 · M2 · M3 | order · reversibility · pending |
| Env Drift Checker | E1 · E2 · E3 | key drift · secrets · flags |

Verdict rule: **GO** iff 0 `FAIL` (WARN items are non-blocking advisories).

## The IBM Bob skill

The `bob/` directory contains the actual IBM Bob skill — the prompts you feed to
Bob to run the workflow with real agents instead of the reference checks:

- `bob/orchestrator.md` — Agent-mode orchestrator system prompt
- `bob/subagents/` — six subagent role files
- `bob/checklist/release-checklist.md` — the 18-item checklist
- `bob/report-template.md` — the GO/NO-GO report template

The Python package is the *reference implementation* of that workflow: it runs
the same 18 checks as static analysis so the proof-of-concept works without a
live Bob session.

## Test it

```bash
python -m pytest tests/ -v
```

## Repository layout

```
bin/release-commander        # shell entry point (no install required)
install.sh                   # editable install (pip install -e .)
pyproject.toml               # pip package + `release-commander` console script
release_commander/           # Python package (pipeline, report, CLI)
bob/                         # IBM Bob skill prompts (orchestrator + subagents)
tests/                       # self-contained pipeline tests
docs/                        # hackathon deliverables (problem/solution, Bob usage, demo)
```

## Docs

- `docs/PROBLEM_STATEMENT.md` — problem, solution, impact numbers
- `docs/BOB_USAGE.md` — every IBM Bob capability used and why
- `docs/DEMO_STORYBOARD.md` — 3-minute demo script
