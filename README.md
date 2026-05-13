# RepoSentinel

RepoSentinel is a lightweight repository security self-check tool. It scans a source code directory for common secret patterns, risky files, and dependency manifest files, then generates JSON or HTML reports.

The project is intentionally small, but it is organized like a real Python package so new scanners can be added later.

## Features

- Detects common secret patterns such as private keys, AWS keys, GitHub tokens, hard-coded passwords, API keys, and database URLs.
- Flags risky files such as `.env`, SSH private key files, and credential JSON files.
- Detects dependency manifests such as `requirements.txt`, `package.json`, `pom.xml`, `go.mod`, and `Cargo.toml`.
- Supports JSON and HTML report output.
- Supports custom JSON rule files.
- Supports CI usage with `--fail-on`.
- Provides a scanner interface for future extensions.

## Project Structure

```text
RepoSentinel/
├── reposentinel.py                 # source-tree entry point
├── pyproject.toml                  # package metadata and console script
├── rules.json                      # example custom rule file
├── reposentinel/
│   ├── cli.py                      # command line interface
│   ├── config.py                   # default file and directory configuration
│   ├── engine.py                   # scan orchestration
│   ├── models.py                   # shared data models
│   ├── rules.py                    # rule loading and compilation
│   ├── utils.py                    # filesystem and text helpers
│   ├── scanners/
│   │   ├── base.py                 # scanner extension interface
│   │   ├── secrets.py              # regex secret scanner
│   │   ├── files.py                # risky file scanner
│   │   └── dependencies.py         # dependency manifest scanner
│   └── reporting/
│       ├── json_report.py          # JSON report writer
│       └── html_report.py          # HTML report writer
└── examples/
    ├── vulnerable_sample.txt       # demo vulnerable content
    ├── .env                        # demo risky file
    └── requirements.txt            # demo dependency manifest
```

## Quick Start

Run from the source tree:

```bash
python reposentinel.py examples -o report.json
```

Or run as a module:

```bash
python -m reposentinel examples -o report.json
```

Generate an HTML report:

```bash
python reposentinel.py examples -f html -o report.html
```

Use a custom rule file:

```bash
python reposentinel.py ./your_repo --rules rules.json -o report.json
```

Fail CI when high-risk findings exist:

```bash
python reposentinel.py ./your_repo --fail-on high
```

## Custom Rules

Rules are JSON objects with the following fields:

```json
{
  "id": "demo-rule",
  "name": "Demo Rule",
  "severity": "medium",
  "pattern": "secret_[A-Za-z0-9]+",
  "description": "Detects a demo secret format."
}
```

Supported severities are `critical`, `high`, `medium`, `low`, and `info`.

## Adding a New Scanner

Create a new file in `reposentinel/scanners/`, inherit from `BaseScanner`, and return a list of `Finding` objects.

Example:

```python
from reposentinel.models import Finding, ScanContext
from reposentinel.scanners.base import BaseScanner


class TodoScanner(BaseScanner):
    name = "todo-comments"

    def scan(self, context: ScanContext) -> list[Finding]:
        if context.text is None or "TODO" not in context.text:
            return []
        return [
            Finding(
                type="code-quality",
                severity="low",
                rule_id="todo-comment",
                title="TODO comment found",
                path=context.relative_path,
                line=None,
                evidence="TODO",
                description="A TODO marker was found in source code.",
            )
        ]
```

Then register it in `reposentinel/engine.py` inside `default_scanners()`.

## Possible Future Extensions

- CVE matching for dependency versions.
- Dockerfile and Kubernetes security checks.
- Git history secret scanning.
- Baseline files for ignoring known findings.
- SARIF report output for GitHub code scanning.
- Web UI for browsing scan reports.

## Project Name for Registration Table

| Name | Platform | URL |
| --- | --- | --- |
| RepoSentinel: Lightweight Repository Security Self-Check Tool | GitHub/Gitee | https://github.com/your-name/RepoSentinel |

Chinese description:

RepoSentinel 是一个轻量级开源仓库安全自检工具，支持对代码仓库中的敏感信息、危险配置文件和依赖清单进行扫描，并生成结构化风险报告，帮助开发者在开源发布前发现潜在安全隐患。

## License

MIT License
