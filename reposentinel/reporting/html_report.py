"""HTML report support."""

from __future__ import annotations

import html
from pathlib import Path


def write_html_report(report: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in report["findings"]:
        location = item["path"]
        if item["line"]:
            location = f"{location}:{item['line']}"
        rows.append(
            "<tr>"
            f"<td>{html.escape(item['severity'])}</td>"
            f"<td>{html.escape(item['type'])}</td>"
            f"<td>{html.escape(item['title'])}</td>"
            f"<td>{html.escape(location)}</td>"
            f"<td><code>{html.escape(item['evidence'])}</code></td>"
            f"<td>{html.escape(item['description'])}</td>"
            "</tr>"
        )

    counts = report["summary"]["by_severity"]
    body = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>RepoSentinel Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
    h1 {{ margin-bottom: 4px; }}
    .summary {{ display: flex; gap: 12px; margin: 20px 0; flex-wrap: wrap; }}
    .badge {{ border: 1px solid #ddd; border-radius: 6px; padding: 8px 10px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #f4f6f8; }}
    code {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h1>RepoSentinel Report</h1>
  <p>Target: <code>{html.escape(report["target"])}</code></p>
  <p>Generated at: {html.escape(report["generated_at"])}</p>
  <div class="summary">
    <div class="badge">Total: {report["summary"]["total"]}</div>
    <div class="badge">Critical: {counts.get("critical", 0)}</div>
    <div class="badge">High: {counts.get("high", 0)}</div>
    <div class="badge">Medium: {counts.get("medium", 0)}</div>
    <div class="badge">Low: {counts.get("low", 0)}</div>
    <div class="badge">Info: {counts.get("info", 0)}</div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Severity</th>
        <th>Type</th>
        <th>Title</th>
        <th>Location</th>
        <th>Evidence</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows) if rows else '<tr><td colspan="6">No findings.</td></tr>'}
    </tbody>
  </table>
</body>
</html>
"""
    output.write_text(body, encoding="utf-8")
