# RepoSentinel

RepoSentinel is a lightweight repository security self-check tool. It scans a source code directory for secrets, risky files, and dependency manifests, then generates JSON or HTML reports.

## Features

- Secret pattern detection: private keys, AWS keys, GitHub tokens, passwords, API keys, and database URLs.
- Risky file detection: `.env`, SSH private keys, credential JSON files, and similar files.
- Dependency manifest detection: `requirements.txt`, `package.json`, `pom.xml`, `go.mod`, `Cargo.toml`, and more.
- JSON and HTML report output.
- Custom regex rules through a JSON rule file.
- Extensible scanner structure for future checks.

## Quick Start

```bash
python reposentinel.py examples -o report.json
```

Generate an HTML report:

```bash
python reposentinel.py examples -f html -o report.html
```

Use custom rules:

```bash
python reposentinel.py ./your_repo --rules rules.json -o report.json
```

Fail CI when high-risk findings exist:

```bash
python reposentinel.py ./your_repo --fail-on high
```

## Project Structure

```text
reposentinel/
  cli.py                  command line interface
  engine.py               scan orchestration
  rules.py                rule loading
  scanners/               built-in and future scanners
  reporting/              report writers
examples/                 demo files
rules.json                example custom rules
reposentinel.py           source-tree entry point
```

## Custom Rules

```json
{
  "id": "demo-rule",
  "name": "Demo Rule",
  "severity": "medium",
  "pattern": "secret_[A-Za-z0-9]+",
  "description": "Detects a demo secret format."
}
```

Supported severities: `critical`, `high`, `medium`, `low`, `info`.

## Extension Ideas

- Dependency CVE matching.
- Dockerfile and Kubernetes security checks.
- Git history secret scanning.
- SARIF output for GitHub code scanning.
- Web UI for scan reports.

## License

MIT License
