"""Scanner for regular-expression based secret rules."""

from __future__ import annotations

from reposentinel.models import Finding, ScanContext
from reposentinel.rules import Rule
from reposentinel.scanners.base import BaseScanner
from reposentinel.utils import mask_evidence


class SecretPatternScanner(BaseScanner):
    name = "secret-patterns"

    def __init__(self, rules: list[Rule]) -> None:
        self.rules = rules

    def scan(self, context: ScanContext) -> list[Finding]:
        if context.text is None:
            return []

        findings: list[Finding] = []
        for line_number, line in enumerate(context.text.splitlines(), start=1):
            for rule in self.rules:
                for match in rule.regex.finditer(line):
                    findings.append(
                        Finding(
                            type="secret",
                            severity=rule.severity,
                            rule_id=rule.id,
                            title=rule.name,
                            path=context.relative_path,
                            line=line_number,
                            evidence=mask_evidence(match.group(0)),
                            description=rule.description,
                        )
                    )
        return findings
