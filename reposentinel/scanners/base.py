"""Base scanner interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from reposentinel.models import Finding, ScanContext


class BaseScanner(ABC):
    name = "base"

    @abstractmethod
    def scan(self, context: ScanContext) -> list[Finding]:
        """Return findings for one file."""
