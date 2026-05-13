"""JSON report support."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from reposentinel import __version__
from reposentinel.models import Finding


def severity_counts(findings: list[Finding]) -> dict[str, int]:
    order = ["critical", "high", "medium", "low", "info"]
    counts = {severity: 0 for severity in order}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    return counts


def build_report(root: Path, findings: list[Finding]) -> dict:
    return {
        "tool": "RepoSentinel",
        "version": __version__,
        "target": str(root.resolve()),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(findings),
            "by_severity": severity_counts(findings),
        },
        "findings": [finding.to_dict() for finding in findings],
    }


def write_json_report(report: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
