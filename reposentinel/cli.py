"""Command line interface."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from reposentinel.config import DEFAULT_EXCLUDED_DIRS, DEFAULT_MAX_FILE_SIZE
from reposentinel.engine import ScanEngine, default_scanners
from reposentinel.models import Finding
from reposentinel.reporting import build_report, write_html_report, write_json_report
from reposentinel.rules import load_rules


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="reposentinel",
        description="Scan a repository for secrets, risky files, and dependency manifests.",
    )
    parser.add_argument("target", help="Path to the repository or directory to scan.")
    parser.add_argument("-o", "--output", default="reposentinel-report.json", help="Report output path.")
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "html"],
        default="json",
        help="Report format.",
    )
    parser.add_argument("--rules", help="Optional JSON rule file.")
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=DEFAULT_MAX_FILE_SIZE,
        help="Maximum text file size to scan, in bytes.",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Directory name to exclude. Can be used multiple times.",
    )
    parser.add_argument(
        "--fail-on",
        choices=["critical", "high", "medium", "low", "info", "never"],
        default="never",
        help="Return exit code 2 when findings at this severity or higher exist.",
    )
    return parser.parse_args(argv)


def should_fail(findings: list[Finding], threshold: str) -> bool:
    if threshold == "never":
        return False
    weights = {"critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1}
    target = weights[threshold]
    return any(weights.get(item.severity, 0) >= target for item in findings)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target = Path(args.target).resolve()
    output = Path(args.output)

    if not target.exists() or not target.is_dir():
        print(f"Target directory does not exist: {target}", file=sys.stderr)
        return 1

    try:
        rules = load_rules(Path(args.rules) if args.rules else None)
    except (OSError, ValueError, re.error, json.JSONDecodeError) as exc:
        print(f"Failed to load rules: {exc}", file=sys.stderr)
        return 1

    excluded_dirs = set(DEFAULT_EXCLUDED_DIRS)
    excluded_dirs.update(args.exclude_dir)

    engine = ScanEngine(
        scanners=default_scanners(rules),
        max_file_size=args.max_file_size,
        excluded_dirs=excluded_dirs,
    )
    findings = engine.scan(target)
    report = build_report(target, findings)

    if args.format == "json":
        write_json_report(report, output)
    else:
        write_html_report(report, output)

    counts = report["summary"]["by_severity"]
    print(
        "Scan finished: "
        f"{report['summary']['total']} findings "
        f"(critical={counts.get('critical', 0)}, "
        f"high={counts.get('high', 0)}, "
        f"medium={counts.get('medium', 0)}, "
        f"low={counts.get('low', 0)}, "
        f"info={counts.get('info', 0)})."
    )
    print(f"Report written to: {output}")

    return 2 if should_fail(findings, args.fail_on) else 0
