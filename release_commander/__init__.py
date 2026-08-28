"""Release Commander — agentic release-readiness workflow (GO / NO-GO)."""

from .pipeline import (
    PERSONAS,
    apply_fixes,
    generate_artifacts,
    run_checks,
    verdict,
)
from .report import render_report

__version__ = "0.1.0"

__all__ = [
    "PERSONAS",
    "apply_fixes",
    "generate_artifacts",
    "render_report",
    "run_checks",
    "verdict",
    "__version__",
]
