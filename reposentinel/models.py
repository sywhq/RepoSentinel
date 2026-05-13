"""Shared data models."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Finding:
    type: str
    severity: str
    rule_id: str
    title: str
    path: str
    line: int | None
    evidence: str
    description: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScanContext:
    root_label: str
    relative_path: str
    file_name: str
    size: int
    text: str | None
