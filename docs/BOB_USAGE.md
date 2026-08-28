# How We Used IBM Bob to Build This Project

Release Commander is not just "built with Bob" — Bob *is* the runtime. The
solution itself is an IBM Bob workflow, and we used every capability the
hackathon asked us to demonstrate.

## Agent mode (orchestrator)

The top-level Bob agent runs in **Agent mode** as the Release Commander
orchestrator. Its task is defined in [`bob/orchestrator.md`](../bob/orchestrator.md).
It is prompted to act as a *conductor, not a doer*: it plans the release,
delegates all six readiness domains, and is the single point of accountability
for the GO / NO-GO decision. It never inlines the six workstreams — it spawns
and delegates them.

## Parallel tasks (subagents)

The six readiness domains are independent, so the orchestrator runs them
**simultaneously** rather than sequentially. This is the core efficiency win: a
release check that would take a human a full day of serial effort is compressed
to the wall-clock time of the single slowest subagent.

## Six named subagents

Each subagent has a focused role file under [`bob/subagents/`](../bob/subagents/):

| Role file | Checklist items | Domain |
|---|---|---|
| `security-sentinel.md` | S1 / S2 / S3 | CVEs, secrets, licenses |
| `test-marshal.md` | T1 / T2 / T3 | tests, flakiness, coverage |
| `version-changelog-clerk.md` | V1 / V2 / V3 | semver, changelog, tags |
| `docs-curator.md` | D1 / D2 / D3 | docs freshness, accuracy |
| `migration-auditor.md` | M1 / M2 / M3 | migration order, reversibility |
| `env-drift-checker.md` | E1 / E2 / E3 | config drift, secrets |

Each subagent owns exactly three checklist items, reports evidence with file +
line references, applies safe fixes, and explicitly stays in its lane.

## Document understanding

The **Docs Curator** and **Migration Auditor** subagents use Bob's document
understanding to read and cross-reference READMEs, changelogs, and SQL migration
files against the actual code — catching stale commands, phantom endpoints, and
non-reversible migrations that a keyword search would miss.

## Synthesis & reporting

Bob merges the six subagent reports into a single Release Readiness Report using
[`bob/report-template.md`](../bob/report-template.md), applies the verdict rule
(GO iff 0 FAIL), and auto-generates four release artifacts (bumped version,
changelog entry, release notes, rollback runbook).

## Shell skill

The workflow ships as an installable CLI:

```bash
pip install .            # installs the `release-commander` command
# or, no install:
bin/release-commander --repo /path/to/your/repo
```

This means Release Commander works as a reusable **shell skill** — run it
against any repo, any team, any cadence, and drop it into CI (exit 0 = GO,
exit 1 = NO-GO).

## Reference implementation

The `release_commander` Python package is a stdlib-only orchestrator that
emulates the same 18 checks so the proof-of-concept runs without a live Bob
session. In the live run, each check is replaced by a real Bob subagent — the
checklist, verdict logic, and report format are identical.

## Verified results

```bash
python -m pytest tests/ -v
```

```
test_detects_seeded_defects      PASSED   # every defect caught → NO-GO
test_fix_flips_verdict_to_go     PASSED   # auto-fixes flip to GO
```

## Bobcoins budget

We designed once (cheap), then spent coins on the six parallel subagent runs —
never on re-running serial steps. Each team member owned a distinct subagent
track to divide the 40-coins-per-person allocation efficiently.
