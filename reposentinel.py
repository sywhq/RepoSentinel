#!/usr/bin/env python3
"""Compatibility entry point for running RepoSentinel from source."""

from reposentinel.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
