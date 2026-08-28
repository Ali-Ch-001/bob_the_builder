"""Release Commander — report rendering."""

from .pipeline import PERSONAS, verdict


def render_report(repo_name, release_ref, results, now, applied=None, slug=None):
    n_pass, n_warn, n_fail, go = verdict(results)
    badge = "GO" if go else "NO-GO"
    lines = []
    lines.append("# Release Readiness Report\n")
    lines.append(f"**Project:** {repo_name} · **Release ref:** {release_ref}")
    lines.append(f"**Generated:** {now} · **Orchestrated by:** IBM Bob (Agent mode)\n")
    lines.append("---\n")
    lines.append(f"## Verdict: **{badge}**\n")
    if go:
        lines.append("> All release gates passed. Remaining WARN items are non-blocking advisories.\n")
    else:
        lines.append("> Blocking issues found. See FAIL items below.\n")
    lines.append("## Summary\n")
    lines.append("| | Count |")
    lines.append("|---|---|")
    lines.append(f"| PASS | {n_pass} |")
    lines.append(f"| WARN | {n_warn} |")
    lines.append(f"| FAIL | {n_fail} |\n")
    lines.append(f"{n_pass}/18 PASS · {n_warn} WARN · {n_fail} FAIL\n")

    by_domain = {}
    it = iter(results)
    for name, _ in PERSONAS:
        by_domain[name] = [next(it) for _ in range(3)]
    for name, _ in PERSONAS:
        lines.append(f"## {name}\n")
        for r in by_domain[name]:
            lines.append(f"### {r['item']} — {r['status']}")
            lines.append(f"**Finding:** {r['finding']}")
            lines.append(f"**Fix applied:** {r['fix']}\n")

    lines.append("## Issues fixed by Release Commander\n")
    if applied:
        for a in applied:
            lines.append(f"- [x] {a}")
    else:
        fixed = [r for r in results if r["fix"] not in ("none",)]
        if fixed:
            for r in fixed:
                lines.append(f"- [ ] {r['item']} — {r['fix']}")
        else:
            lines.append("- [ ] (none — all fixes pending)")

    open_items = [r for r in results if r["status"] in ("FAIL", "WARN")]
    lines.append("\n## Open items requiring human decision\n")
    if open_items:
        for r in open_items:
            lines.append(f"- [ ] {r['item']} ({r['status']}) — {r['finding'].splitlines()[0]}")
    else:
        lines.append("- [ ] (none)")

    lines.append("\n## Auto-generated release artifacts\n")
    lines.append(f"- **Bumped version:** `{release_ref}`")
    lines.append("- **Changelog entry:** `CHANGELOG.md`")
    if slug:
        lines.append(f"- **Release notes:** `release-notes-{slug}.md`")
        lines.append(f"- **Rollback runbook:** `rollback-runbook-{slug}.md`")
    else:
        lines.append("- **Release notes:** generated")
        lines.append("- **Rollback runbook:** generated")
    lines.append("")
    return "\n".join(lines)
