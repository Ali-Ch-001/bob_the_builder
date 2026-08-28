"""Tests for Release Commander's reference orchestrator.

These tests prove the core claim of the project: the pipeline detects every
seeded release defect (NO-GO) and, after Bob-style auto-fixes, flips the verdict
to GO.

Run with:
    python -m pytest release-commander/tests/ -v

Requires pytest + fastapi + httpx + pydantic (see sample-app/requirements-dev.txt)
so that the Test Marshal subagent can actually execute the test suite.
"""

import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]  # bob_the_builder
RC_DIR = ROOT / "release-commander"
sys.path.insert(0, str(RC_DIR))

import release_commander as rc  # noqa: E402


def run_personas(repo: Path):
    results = []
    for _name, fn in rc.PERSONAS:
        results.extend(fn(repo))
    return results


@pytest.fixture()
def sample_copy(tmp_path):
    dest = tmp_path / "sample-app"
    shutil.copytree(ROOT / "sample-app", dest)
    return dest


# The nine checklist items that must FAIL on the unready sample app.
SEEDED_FAIL_ITEMS = {"S2", "T1", "V1", "V2", "D1", "M1", "M2", "E1", "E2"}


def test_detects_all_seeded_defects(sample_copy):
    results = run_personas(sample_copy)
    fails = {r["item"] for r in results if r["status"] == "FAIL"}
    missing = SEEDED_FAIL_ITEMS - fails
    assert not missing, f"undetected seeded defects: {missing}"
    n_pass, n_warn, n_fail, go = rc.verdict(results)
    assert n_fail >= len(SEEDED_FAIL_ITEMS)
    assert go is False


def test_fix_flips_verdict_to_go(sample_copy):
    before = run_personas(sample_copy)
    applied = rc.apply_fixes(sample_copy, before)
    assert len(applied) >= 8
    after = run_personas(sample_copy)
    still_failing = [r["item"] for r in after if r["status"] == "FAIL"]
    assert not still_failing, f"unresolved after fix: {still_failing}"
    n_pass, n_warn, n_fail, go = rc.verdict(after)
    assert n_fail == 0
    assert go is True


def test_report_verdict_reflects_state(sample_copy):
    before = run_personas(sample_copy)
    md = rc.render_report(sample_copy.name, "1.3.0", before,
                          "2026-08-29T00:00:00Z", slug=sample_copy.name)
    assert "**NO-GO**" in md

    rc.apply_fixes(sample_copy, before)
    after = run_personas(sample_copy)
    md2 = rc.render_report(sample_copy.name, "1.3.0", after,
                           "2026-08-29T00:00:00Z",
                           applied=["fix"], slug=sample_copy.name)
    assert "**GO**" in md2


def test_artifacts_generated_when_go(sample_copy):
    before = run_personas(sample_copy)
    rc.apply_fixes(sample_copy, before)
    notes, runbook = rc.generate_artifacts(sample_copy, "1.3.0",
                                           sample_copy.name, RC_DIR / "reports")
    assert notes.exists() and runbook.exists()
    assert "Rollback Runbook" in runbook.read_text()
