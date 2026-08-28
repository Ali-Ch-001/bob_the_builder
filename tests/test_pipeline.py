"""Tests for Release Commander's pipeline (self-contained, no external fixture).

These prove the core claim of the project on a synthetic unready repository: the
pipeline detects every seeded defect (NO-GO), then `apply_fixes` resolves the
deterministic ones and flips the verdict to GO.

Run with:
    python -m pytest tests/ -v
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from release_commander import apply_fixes, run_checks, verdict  # noqa: E402


def _make_unready_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "acme"
    (repo / "config").mkdir(parents=True)
    (repo / "migrations").mkdir(parents=True)
    (repo / "tests").mkdir(parents=True)

    (repo / "pyproject.toml").write_text(
        '[project]\nname = "acme"\nversion = "1.0.0"\ndependencies = ["fastapi"]\n')
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [1.1.0] - 2026-08-29\nUnreleased — pending.\n\n"
        "## [1.0.0]\nInitial release.\n")
    (repo / "README.md").write_text("# Acme\n\nRun with `python -m app`.\n")
    (repo / "config" / "dev.env").write_text(
        "APP_ENV=dev\nLOG_LEVEL=info\nDATABASE_URL=sqlite:///dev.db\n")
    (repo / "config" / "staging.env").write_text(
        "APP_ENV=staging\nLOG_LEVEL=info\n"
        "DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@staging:5432/acme\n")
    (repo / "config" / "prod.env").write_text(
        "APP_ENV=prod\nLOG_LEVEL=debug\n"
        "DATABASE_URL=postgres://acme:HardPass123!@prod:5432/acme\n"
        "REDIS_URL=redis://prod-cache:6379\n")
    (repo / "migrations" / "0001_create_users.sql").write_text(
        "CREATE TABLE users (id INT);\n")
    (repo / "migrations" / "0002_add_index.sql").write_text(
        "-- depends_on: 0003\nCREATE INDEX idx_users ON users(id);\n")
    (repo / "migrations" / "0003_create_orders.sql").write_text(
        "CREATE TABLE orders (id INT);\n")
    (repo / "tests" / "test_smoke.py").write_text(
        "def test_ok():\n    assert 1 == 1\n")
    return repo


SEEDED_FAIL_ITEMS = {"S2", "V1", "V2", "E1", "E2", "M1", "M2"}


def test_detects_seeded_defects(tmp_path):
    repo = _make_unready_repo(tmp_path)
    before = run_checks(repo)
    fails = {r["item"] for r in before if r["status"] == "FAIL"}
    missing = SEEDED_FAIL_ITEMS - fails
    assert not missing, f"undetected seeded defects: {missing}"
    n_pass, n_warn, n_fail, go = verdict(before)
    assert n_fail >= len(SEEDED_FAIL_ITEMS)
    assert go is False


def test_fix_flips_verdict_to_go(tmp_path):
    repo = _make_unready_repo(tmp_path)
    before = run_checks(repo)
    applied = apply_fixes(repo, before)
    assert len(applied) >= 6
    after = run_checks(repo)
    still_failing = [r["item"] for r in after if r["status"] == "FAIL"]
    assert not still_failing, f"unresolved after fix: {still_failing}"
    n_pass, n_warn, n_fail, go = verdict(after)
    assert n_fail == 0
    assert go is True
