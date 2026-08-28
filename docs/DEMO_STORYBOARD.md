# Demo Storyboard (3:00 video · 90s live demo)

## 0:00–0:30 — Hook & problem (30s)

- "Every release is a 1–2 day manual checklist. And every skipped item is a
  future production incident."
- Flash three failure cards on screen: *stale doc*, *missed migration*,
  *hardcoded secret*.
- One sentence: "We built Release Commander — IBM Bob as an autonomous release
  orchestrator."

## 0:30–0:50 — Architecture (20s)

- Show the orchestrator + six subagent diagram (Security Sentinel, Test Marshal,
  Version & Changelog Clerk, Docs Curator, Migration Auditor, Env Drift Checker).
- Emphasize: **parallel**, not sequential.

## 0:50–2:20 — Live demo (90s)

1. **0:50** Point Bob at `sample-app` + release ref `1.3.0`. Kick off Agent mode.
2. **0:55–1:20** Screen-share the six subagents spinning up **in parallel**, each
   with its own task and status. Call out the parallel lanes visually.
3. **1:20–1:40** Watch Bob catch seeded defects live: version mismatch (V1),
   hardcoded secret (S2/E2), out-of-order migration (M1), stale README (D1),
   failing test (T1).
4. **1:40–1:55** Bob applies fixes and re-runs; show the converging statuses.
5. **1:55–2:20** Bob synthesizes the **Release Readiness Report**: verdict badge,
   `X/18 PASS · Y WARN · Z FAIL`, fixed vs. open items, and the four
   auto-generated artifacts (bumped version, changelog entry, release notes,
   rollback runbook).

## 2:20–2:40 — Impact (20s)

- Before/after slide: **2 days → ~25 min**, **18/18 coverage**, **~0 release
  incidents**.
- One line: "Works on any repo, any team, any release cadence."

## 2:40–3:00 — Close (20s)

- "Release Commander: Bob doesn't just write code — Bob ships it safely."
- Title card + team + hashtags #watsonxHackathon.
