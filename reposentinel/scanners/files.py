"""Scanner for risky committed file names."""

from __future__ import annotations

from reposentinel.config import RISKY_FILE_NAMES
from reposentinel.models import Finding, ScanContext
from reposentinel.scanners.base import BaseScanner


class RiskyFileScanner(BaseScanner):
    name = "risky-files"

    def scan(self, context: ScanContext) -> list[Finding]:
        if context.file_name not in RISKY_FILE_NAMES:
            return []
        return [
            Finding(
                type="risky-file",
                severity="high",
                rule_id="risky-file",
                title=f"Risky file: {context.file_name}",
                path=context.relative_path,
                line=None,
                evidence=context.file_name,
                description=RISKY_FILE_NAMES[context.file_name],
            )
        ]
