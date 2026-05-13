"""Rule loading and compilation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Pattern


DEFAULT_RULES = [
    {
        "id": "private-key",
        "name": "Private key block",
        "severity": "critical",
        "pattern": r"-----BEGIN (RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----",
        "description": "A private key appears to be committed.",
    },
    {
        "id": "aws-access-key",
        "name": "AWS access key",
        "severity": "high",
        "pattern": r"\bAKIA[0-9A-Z]{16}\b",
        "description": "Possible AWS access key ID.",
    },
    {
        "id": "github-token",
        "name": "GitHub token",
        "severity": "high",
        "pattern": r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b",
        "description": "Possible GitHub personal access token.",
    },
    {
        "id": "password-field",
        "name": "Hard-coded password field",
        "severity": "medium",
        "pattern": r"(?i)\b(password|passwd|pwd)\b\s*[:=]\s*[\"']?[^\"'\s]{6,}",
        "description": "A password-like value is hard-coded.",
    },
    {
        "id": "secret-field",
        "name": "Hard-coded secret field",
        "severity": "medium",
        "pattern": r"(?i)\b(secret|token|api[_-]?key|access[_-]?key)\b\s*[:=]\s*[\"']?[^\"'\s]{8,}",
        "description": "A secret-like value is hard-coded.",
    },
    {
        "id": "database-url",
        "name": "Database connection URL",
        "severity": "medium",
        "pattern": r"(?i)\b(mysql|postgres|postgresql|mongodb|redis)://[^\s\"']+",
        "description": "A database connection string may contain credentials.",
    },
]


@dataclass
class Rule:
    id: str
    name: str
    severity: str
    pattern: str
    description: str
    regex: Pattern[str]


def load_rule_data(path: Path | None) -> list[dict]:
    if path is None:
        return DEFAULT_RULES
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("Rules file must be a JSON array.")
    return data


def compile_rules(rule_data: list[dict]) -> list[Rule]:
    compiled: list[Rule] = []
    for raw in rule_data:
        missing = {"id", "name", "severity", "pattern"} - set(raw)
        if missing:
            raise ValueError(f"Rule is missing fields: {', '.join(sorted(missing))}")
        compiled.append(
            Rule(
                id=raw["id"],
                name=raw["name"],
                severity=raw["severity"],
                pattern=raw["pattern"],
                description=raw.get("description", ""),
                regex=re.compile(raw["pattern"]),
            )
        )
    return compiled


def load_rules(path: Path | None) -> list[Rule]:
    return compile_rules(load_rule_data(path))
