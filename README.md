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

Point `release-commander` at any repo and a version. It delegates six readiness
domains to parallel checks (or live Bob subagents), fixes what it can, and
synthesizes a Release Readiness Report with a GO / NO-GO verdict.

| Subagent | Owns |
|---|---|
| Security Sentinel | S1 CVEs · S2 secrets · S3 licenses |
| Test Marshal | T1 tests · T2 flakiness · T3 coverage |
| Version & Changelog Clerk | V1 semver · V2 changelog · V3 tags |
| Docs Curator | D1 quickstart · D2 endpoints · D3 links |
| Migration Auditor | M1 order · M2 reversibility · M3 pending |
| Env Drift Checker | E1 key drift · E2 secrets · E3 flags |

## Proven results (sample-app)

| Stage | Result |
|---|---|
| Diagnose unready release | **NO-GO** · 1/18 PASS · 8 WARN · 9 FAIL — all 8 seeded defects caught |
| Auto-fix + re-evaluate | **GO** · 10/18 PASS · 0 FAIL · 8 fixes applied |
| Artifacts generated | `release-notes-*.md`, `rollback-runbook-*.md` |

4/4 tests pass:
```
test_detects_all_seeded_defects      PASSED   # proves it catches every defect
test_fix_flips_verdict_to_go         PASSED   # proves NO-GO → GO
test_report_verdict_reflects_state   PASSED   # report matches state
test_artifacts_generated_when_go     PASSED   # artifacts real
```

## Install as a shell command

```bash
chmod +x install.sh && ./install.sh
```

This installs a `release-commander` command into `/usr/local/bin` (or `~/bin`
if not writable without sudo) and installs Python dependencies.

Then point it at any repo:

```bash
# Diagnose a release — emits GO / NO-GO report
release-commander --repo /path/to/your/repo

# Auto-apply safe fixes and re-evaluate (flips NO-GO → GO, generates artifacts)
release-commander --repo /path/to/your/repo --fix

# Specify a release version
release-commander --repo /path/to/your/repo --release-ref 2.0.0 --fix
```

Or run without installing:

```bash
python3 release-commander/release_commander.py --repo /path/to/your/repo
python3 release-commander/release_commander.py --repo /path/to/your/repo --fix
```

## Reproduce the demo

```bash
# 0. Install dependencies
pip install -r sample-app/requirements-dev.txt

# 1. Prove the pipeline works (4/4 tests)
python -m pytest release-commander/tests/ -v

# 2. Run against the seeded sample app — expect NO-GO
release-commander --repo sample-app

# 3. Auto-fix and re-evaluate — expect GO + artifacts
release-commander --repo sample-app --fix
```

## Layout

```
install.sh                  # one-command install (creates shell command)
SPEC.md                     # single source of truth
sample-app/                 # FastAPI demo app with 8 seeded defects (test fixture)
release-commander/
  release_commander.py      # executable orchestrator (shebang; run directly)
  orchestrator.md           # Bob Agent-mode orchestrator prompt
  subagents/                # six persona role files
  checklist/                # 18-item release checklist
  report-template.md        # GO / NO-GO report template
  reports/                  # generated reports (JSON + Markdown)
  tests/                    # test suite (4 tests)
docs/                       # problem/solution, Bob usage, demo storyboard
```

> **`sample-app/`** is the test fixture that `release-commander/tests/` runs against.
> It ships with 8 intentional defects so the demo proves real detection, not mocked results.
> It is not meant to be deleted — the test suite copies it to a temp directory each run.

## How Bob is used

See [`docs/BOB_USAGE.md`](docs/BOB_USAGE.md) — Agent mode (orchestrator),
parallel tasks, six subagents, document understanding, and synthesis.
