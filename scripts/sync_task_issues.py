#!/usr/bin/env python3
"""Sync structured Studio OS GitHub Issues into dashboard/task-issues.json.

Uses the GitHub REST API when GITHUB_TOKEN is available. Without a token, writes
an empty but valid snapshot so local dashboard generation remains deterministic.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "pri8771/studio-ios")
TOKEN = os.environ.get("GITHUB_TOKEN")


def field(body: str, label: str) -> str | None:
    pattern = rf"(?ms)^### {re.escape(label)}\s*\n\s*(.+?)(?=\n### |\Z)"
    match = re.search(pattern, body or "")
    if not match:
        return None
    value = match.group(1).strip()
    return None if value in {"", "_No response_"} else value


def labels(issue: dict[str, Any]) -> list[str]:
    return [item.get("name", "") for item in issue.get("labels", []) if item.get("name")]


def normalized_status(issue: dict[str, Any]) -> str:
    names = labels(issue)
    for candidate in ("queued", "running", "blocked", "approval-needed", "in-review", "verified", "completed", "cancelled"):
        if f"status:{candidate}" in names:
            return candidate
    return "completed" if issue.get("state") == "closed" else "queued"


def fetch_issues() -> list[dict[str, Any]]:
    if not TOKEN:
        return []
    url = f"https://api.github.com/repos/{REPOSITORY}/issues?state=all&labels=studio-task&per_page=100"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "studio-os-dashboard",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def transform(issue: dict[str, Any]) -> dict[str, Any]:
    body = issue.get("body") or ""
    status = normalized_status(issue)
    return {
        "number": issue["number"],
        "title": re.sub(r"^\[TASK\]\s*", "", issue.get("title", "")),
        "url": issue.get("html_url"),
        "state": issue.get("state"),
        "status": status,
        "product": field(body, "Product") or "Unspecified",
        "owner": field(body, "Execution owner") or "Unassigned",
        "priority": field(body, "Priority") or "P3",
        "objective": field(body, "Objective"),
        "acceptanceCriteria": field(body, "Acceptance criteria"),
        "approvalGate": field(body, "Human approval required before") or "No additional approval",
        "dueDate": field(body, "Due date"),
        "updatedAt": issue.get("updated_at"),
        "approvalNeeded": status == "approval-needed",
        "labels": labels(issue),
    }


def main() -> int:
    issues = [item for item in fetch_issues() if "pull_request" not in item]
    tasks = [transform(item) for item in issues]
    tasks.sort(key=lambda item: (item["status"] in {"completed", "cancelled"}, item["priority"], item.get("dueDate") or "9999-12-31"))
    snapshot = {
        "schemaVersion": 1,
        "repository": REPOSITORY,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "tokenAvailable": bool(TOKEN),
        "tasks": tasks,
        "summary": {
            "total": len(tasks),
            "open": sum(task["status"] not in {"completed", "cancelled"} for task in tasks),
            "running": sum(task["status"] == "running" for task in tasks),
            "blocked": sum(task["status"] == "blocked" for task in tasks),
            "approvalNeeded": sum(task["approvalNeeded"] for task in tasks),
        },
    }
    output = ROOT / "dashboard" / "task-issues.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {len(tasks)} Studio task issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
