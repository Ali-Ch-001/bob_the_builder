# Demo Storyboard (3:00 video · 90s live demo)

## 0:00–0:30 — Hook & problem (30s)

- "Every release is a 1–2 day manual checklist. And every skipped item is a
  future production incident."
- Flash three failure cards on screen: *stale doc*, *missed migration*,
  *hardcoded secret*.
- One sentence: "We built Release Commander — IBM Bob as an autonomous release
  orchestrator. One command. GO or NO-GO. Done."

## 0:30–0:50 — Architecture (20s)

- Show the orchestrator → six subagent diagram:
  Security Sentinel · Test Marshal · Version & Changelog Clerk ·
  Docs Curator · Migration Auditor · Env Drift Checker.
- Key point: they run **in parallel** — not sequentially.
- "18 checks across 6 domains. Bob coordinates. You decide."

## 0:50–2:20 — Live demo (90s)

### Step 1 — Install (0:50–1:00, 10s)

Show the one command that gets everything:

```bash
pip install .        # or:  bin/release-commander --help  (no install)
```

"Installs in seconds. Now it's a command on your PATH."

### Step 2 — Diagnose: NO-GO (1:00–1:30, 30s)

```bash
release-commander --repo ./demo-repo
```

Show the terminal output:

```
Verdict: NO-GO  |  1/18 PASS · 8 WARN · 9 FAIL
```

Call out five seeded defects Bob caught:
- **S2** — hardcoded `DATABASE_URL` password in `prod.env`
- **T1** — test asserts `total == 999.0`, actual is `19.99`
- **V1** — `pyproject.toml` says `1.2.0`, CHANGELOG says `1.3.0`
- **M1** — migration `0002` depends on `0003` (out of order)
- **D1** — README quickstart uses `uvicorn main:app` (wrong entrypoint)

### Step 3 — Auto-fix: GO (1:30–1:55, 25s)

```bash
release-commander --repo ./demo-repo --fix
```

Show:

```
Verdict: GO  |  10/18 PASS · 0 FAIL
Fixes applied: 8
```

"8 fixes applied. Zero blocking issues."

### Step 4 — Artifacts (1:55–2:20, 25s)

Open the output directory `release-commander-reports/`:
- `release-readiness-<repo>.md` — the full report
- `release-notes-<repo>.md` — auto-generated release notes
- `rollback-runbook-<repo>.md` — undo runbook for every migration and config change

"Release artifacts written. Normally hand-written. Now done."

## 2:20–2:40 — Impact (20s)

Before / after slide:

| | Before | After |
|---|---|---|
| Release prep | ~2 days | ~25 min |
| Checklist coverage | ~14/18 | 18/18 |
| Incidents | recurring | ~0 |

"Works on any repo, any team, any release cadence."

## 2:40–3:00 — Close (20s)

- "Release Commander: Bob doesn't just write code — Bob ships it safely."
- Show: `release-commander --repo <your-repo> --fix`
- Title card + team + `#watsonxHackathon` + GitHub link:
  `github.com/Ali-Ch-001/bob_the_builder`
