"""Scanner for dependency manifest files."""

from __future__ import annotations

from reposentinel.config import DEPENDENCY_FILES
from reposentinel.models import Finding, ScanContext
from reposentinel.scanners.base import BaseScanner


class DependencyManifestScanner(BaseScanner):
    name = "dependency-manifests"

    def scan(self, context: ScanContext) -> list[Finding]:
        if context.file_name not in DEPENDENCY_FILES:
            return []
        return [
            Finding(
                type="dependency-manifest",
                severity="info",
                rule_id="dependency-manifest",
                title=f"Dependency manifest: {context.file_name}",
                path=context.relative_path,
                line=None,
                evidence=context.file_name,
                description=DEPENDENCY_FILES[context.file_name],
            )
        ]
