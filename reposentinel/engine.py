"""Scan orchestration."""

from __future__ import annotations

from pathlib import Path

from reposentinel.config import DEFAULT_EXCLUDED_DIRS, DEFAULT_MAX_FILE_SIZE
from reposentinel.models import Finding, ScanContext
from reposentinel.rules import Rule
from reposentinel.scanners import DependencyManifestScanner, RiskyFileScanner, SecretPatternScanner
from reposentinel.scanners.base import BaseScanner
from reposentinel.utils import iter_files, read_text_if_safe, relative_path


def default_scanners(rules: list[Rule]) -> list[BaseScanner]:
    return [
        RiskyFileScanner(),
        DependencyManifestScanner(),
        SecretPatternScanner(rules),
    ]


class ScanEngine:
    def __init__(
        self,
        scanners: list[BaseScanner],
        max_file_size: int = DEFAULT_MAX_FILE_SIZE,
        excluded_dirs: set[str] | None = None,
    ) -> None:
        self.scanners = scanners
        self.max_file_size = max_file_size
        self.excluded_dirs = set(excluded_dirs or DEFAULT_EXCLUDED_DIRS)

    def scan(self, root: Path) -> list[Finding]:
        findings: list[Finding] = []
        for path in iter_files(root, self.excluded_dirs):
            context = self._build_context(path, root)
            for scanner in self.scanners:
                findings.extend(scanner.scan(context))
        return findings

    def _build_context(self, path: Path, root: Path) -> ScanContext:
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        return ScanContext(
            root_label=str(root.resolve()),
            relative_path=relative_path(path, root),
            file_name=path.name,
            size=size,
            text=read_text_if_safe(path, self.max_file_size),
        )
