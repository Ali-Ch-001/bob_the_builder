# How We Used IBM Bob to Build This Project

Release Commander is not just "built with Bob" — Bob *is* the runtime. The
solution itself is an IBM Bob workflow, and we used every capability the
hackathon asked us to demonstrate.

## Agent mode (orchestrator)

The top-level Bob agent runs in **Agent mode** as the Release Commander
orchestrator. Its task is defined in `release-commander/orchestrator.md`. It is
prompted to act as a *conductor, not a doer*: it plans the release, delegates all
six readiness domains, and is the single point of accountability for the GO /
NO-GO decision. It never inlines the six workstreams — it delegates them.

## Parallel tasks

The six readiness domains are independent, so the orchestrator runs them
**simultaneously** rather than sequentially. This is the core efficiency win: a
release check that would take a human a full day of serial effort is compressed
to the wall-clock time of the single slowest subagent.

## Subagents

We defined six named subagents, each with a focused role file under
`release-commander/subagents/`:

1. `security-sentinel.md` — S1/S2/S3 (CVEs, secrets, licenses)
2. `test-marshal.md` — T1/T2/T3 (tests, flakiness, coverage)
3. `version-changelog-clerk.md` — V1/V2/V3 (semver, changelog, tags)
4. `docs-curator.md` — D1/D2/D3 (docs freshness)
5. `migration-auditor.md` — M1/M2/M3 (migration order/reversibility)
6. `env-drift-checker.md` — E1/E2/E3 (config drift, secrets)

Each subagent owns exactly three checklist items, reports evidence with file +
line references, applies safe fixes, and explicitly stays in its lane.

## Document understanding

The **Docs Curator** and **Migration Auditor** subagents use Bob's document
understanding to read and cross-reference READMEs, changelogs, and SQL migration
files against the actual code — catching stale commands, phantom endpoints, and
non-reversible migrations that a keyword search would miss.

## Synthesis & reporting

Bob merges the six subagent reports into a single Release Readiness Report using
`release-commander/report-template.md`, applies the verdict rule (GO iff 0 FAIL
and ≤ 2 WARN), and auto-generates four release artifacts.

## Reference implementation

We also ship `release-commander/release_commander.py`, a stdlib-only Python
orchestrator that emulates the same 18 checks so the proof-of-concept runs even
without a live Bob session. In the live run, each check is replaced by a real Bob
subagent — the checklist, verdict logic, and report format are identical.

## Bobcoins budget

We designed once (cheap), then spent coins on the six parallel subagent runs —
never on re-running serial steps. Each team member owned a distinct subagent
track to divide the 40-coins-per-person allocation efficiently.
