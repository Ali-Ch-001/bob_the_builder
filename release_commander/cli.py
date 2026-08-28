"""Release Commander — command-line interface."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from .pipeline import apply_fixes, generate_artifacts, run_checks, verdict
from .report import render_report

DEFAULT_OUTDIR = "release-commander-reports"


def _detect_release_ref(repo: Path) -> str:
    cl = repo / "CHANGELOG.md"
    if cl.exists():
        m = re.search(r"^##\s+\[?([0-9]+\.[0-9]+\.[0-9]+)", cl.read_text(errors="ignore"), re.M)
        if m:
            return m.group(1)
    return "HEAD"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="release-commander",
        description="Agentic release-readiness check (GO / NO-GO) built on IBM Bob 2.0.",
    )
    ap.add_argument("--repo", default=".",
                    help="Path to the repository to check (default: current directory)")
    ap.add_argument("--release-ref", default=None,
                    help="Release version/branch (default: auto-detect from CHANGELOG)")
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR,
                    help=f"Output directory for reports/artifacts (default: ./{DEFAULT_OUTDIR})")
    ap.add_argument("--fix", action="store_true",
                    help="Auto-apply safe fixes for deterministic FAIL findings, then re-evaluate")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"error: repository not found: {repo}", file=sys.stderr)
        return 2

    release_ref = args.release_ref or _detect_release_ref(repo)
    slug = repo.name or "repo"

    results = run_checks(repo)

    applied = []
    if args.fix:
        applied = apply_fixes(repo, results)
        results = run_checks(repo)

    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_pass, n_warn, n_fail, go = verdict(results)

    report_md = outdir / f"release-readiness-{slug}.md"
    report_md.write_text(render_report(repo.name, release_ref, results, now,
                                       applied=applied, slug=slug))
    report_json = outdir / f"release-readiness-{slug}.json"
    report_json.write_text(json.dumps({
        "repo": repo.name,
        "release_ref": release_ref,
        "generated": now,
        "verdict": "GO" if go else "NO-GO",
        "summary": {"pass": n_pass, "warn": n_warn, "fail": n_fail},
        "fixes_applied": applied,
        "items": results,
    }, indent=2))

    if go:
        generate_artifacts(repo, release_ref, slug, outdir)

    print(f"Verdict: {'GO' if go else 'NO-GO'}  |  "
          f"{n_pass}/18 PASS · {n_warn} WARN · {n_fail} FAIL")
    if applied:
        print(f"Fixes applied: {len(applied)}")
    print(f"Report: {report_md}")
    print(f"JSON:   {report_json}")
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
