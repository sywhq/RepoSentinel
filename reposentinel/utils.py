"""Small filesystem and text helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable


def iter_files(root: Path, excluded_dirs: set[str]) -> Iterable[Path]:
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file_name in files:
            yield Path(current_root) / file_name


def relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def is_probably_binary(path: Path, sample_size: int = 4096) -> bool:
    try:
        chunk = path.read_bytes()[:sample_size]
    except OSError:
        return True
    return b"\x00" in chunk


def read_text_if_safe(path: Path, max_file_size: int) -> str | None:
    try:
        if path.stat().st_size > max_file_size:
            return None
    except OSError:
        return None

    if is_probably_binary(path):
        return None

    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def mask_evidence(text: str, keep: int = 6) -> str:
    clean = text.strip()
    if len(clean) <= keep * 2:
        return clean
    return f"{clean[:keep]}...{clean[-keep:]}"
