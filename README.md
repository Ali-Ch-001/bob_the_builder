# Release Commander

> **IBM Bob 2.0 · Agent mode · Agentic release-readiness workflow**
>
> Built for the IBM TechXchange 2026 Pre-conference Dev Day Hackathon.

Cutting a release is a 1–2 day manual checklist. A skipped item becomes a production
incident. **Release Commander** turns that into a single command.

Bob acts as a release orchestrator, spawns **six specialist subagents in parallel**
across 18 release-gate checks, auto-fixes what it can, and produces a **GO / NO-GO
Release Readiness Report** with generated artifacts.

---

## One-click install

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Ali-Ch-001/bob_the_builder/main/install.sh)
```

That's it. No cloning required. The script installs Python dependencies and puts a
`release-commander` command on your `$PATH`.

> **Requires:** Python 3.11+, pip, curl

Then point it at any repo:

```bash
release-commander --repo /path/to/your/repo
release-commander --repo /path/to/your/repo --fix
```

---

## What it checks (18 gates · 6 domains)

| Subagent | Items | Domain |
|---|---|---|
| Security Sentinel | S1 · S2 · S3 | CVEs · secrets · licenses |
| Test Marshal | T1 · T2 · T3 | tests · flakiness · coverage |
| Version & Changelog Clerk | V1 · V2 · V3 | semver · changelog · tags |
| Docs Curator | D1 · D2 · D3 | quickstart · endpoints · links |
| Migration Auditor | M1 · M2 · M3 | order · reversibility · pending |
| Env Drift Checker | E1 · E2 · E3 | key drift · secrets · flags |

---

## Proven results

Against the bundled `sample-app` (8 intentional seeded defects):

| Stage | Verdict | Score | Detail |
|---|---|---|---|
| Before | **NO-GO** | 1/18 PASS · 8 WARN · 9 FAIL | all 8 defects caught |
| After `--fix` | **GO** | 10/18 PASS · 0 FAIL | 8 fixes applied |
| Artifacts | ✓ | `release-notes-*.md` · `rollback-runbook-*.md` | auto-generated |

Test suite — **4/4 pass:**

```
test_detects_all_seeded_defects      PASSED   # proves every defect is caught
test_fix_flips_verdict_to_go         PASSED   # proves NO-GO → GO
test_report_verdict_reflects_state   PASSED   # report matches actual state
test_artifacts_generated_when_go     PASSED   # artifacts written to disk
```

---

## Usage

```bash
# Diagnose a release — emits a GO / NO-GO report
release-commander --repo /path/to/your/repo

# Auto-apply safe fixes, re-evaluate, emit artifacts (release notes + rollback runbook)
release-commander --repo /path/to/your/repo --fix

# Specify a release version (default: 1.3.0)
release-commander --repo /path/to/your/repo --release-ref 2.0.0 --fix

# Help
release-commander --help
```

### Run without installing (clone first)

```bash
git clone https://github.com/Ali-Ch-001/bob_the_builder.git
cd bob_the_builder
pip install -r sample-app/requirements-dev.txt
python3 release-commander/release_commander.py --repo sample-app
python3 release-commander/release_commander.py --repo sample-app --fix
```

### Reproduce the full demo

```bash
# 1. Install deps
pip install -r sample-app/requirements-dev.txt

# 2. Run the test suite (proves the pipeline)
python -m pytest release-commander/tests/ -v

# 3. NO-GO run against seeded sample app
release-commander --repo sample-app

# 4. GO run with auto-fix + artifacts
release-commander --repo sample-app --fix
```

---

## Repository layout

```
install.sh                      # one-click installer (curl | bash)
SPEC.md                         # single source of truth
sample-app/                     # FastAPI demo repo — 8 seeded release defects (test fixture)
release-commander/
  release_commander.py          # executable orchestrator  (python3 / direct ./…)
  orchestrator.md               # Bob Agent-mode system prompt
  subagents/                    # six persona role files
  checklist/release-checklist.md
  report-template.md
  reports/                      # generated GO / NO-GO reports (MD + JSON)
  tests/                        # 4-test suite
docs/
  PROBLEM_STATEMENT.md
  BOB_USAGE.md
  DEMO_STORYBOARD.md
```

> **`sample-app/`** ships with 8 intentional defects so the demo proves real
> detection — not mocked results. The test suite copies it to a temp directory on
> every run; it is not modified in place during tests.

---

## How Bob is used

See [`docs/BOB_USAGE.md`](docs/BOB_USAGE.md) — Agent mode orchestrator, parallel
`spawn_subagent` calls, document understanding, synthesis, and auto-fix.

## Docs

- [`docs/PROBLEM_STATEMENT.md`](docs/PROBLEM_STATEMENT.md) — problem, solution, impact numbers
- [`docs/BOB_USAGE.md`](docs/BOB_USAGE.md) — every Bob capability used and why
- [`docs/DEMO_STORYBOARD.md`](docs/DEMO_STORYBOARD.md) — 3-minute demo script
- [`release-commander/reports/release-readiness-sample-app.md`](release-commander/reports/release-readiness-sample-app.md) — canonical NO-GO report (the "before" state)
