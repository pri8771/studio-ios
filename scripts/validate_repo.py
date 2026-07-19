#!/usr/bin/env python3
"""Lightweight Studio OS validation with no third-party dependencies."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID_GENERAL = {"draft", "in-review", "approved", "active", "blocked", "needs-update", "deprecated", "archived", "selected", "building"}
VALID_TASK = {"backlog", "ready", "in-progress", "blocked", "in-review", "completed", "cancelled"}
VALID_REQUIREMENT = {"proposed", "approved", "implementing", "implemented", "verified", "deferred", "rejected"}
ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^#\n]+)", text)
    return match.group(1).strip().strip("'\"") if match else None


def validate_yaml_like(path: Path, text: str, errors: list[str]) -> None:
    record_id = scalar(text, "id")
    record_type = scalar(text, "type")
    status = scalar(text, "status")
    owner = scalar(text, "owner")
    updated = scalar(text, "updated_at")

    if record_id and not ID_RE.match(record_id):
        errors.append(f"{path}: invalid stable id '{record_id}'")
    if record_type and "registry" not in path.parts:
        for field, value in (("id", record_id), ("title", scalar(text, "title")), ("summary", scalar(text, "summary")), ("status", status), ("owner", owner), ("updated_at", updated)):
            if not value:
                errors.append(f"{path}: missing required field '{field}'")
    if status and record_type:
        valid = VALID_TASK if record_type == "task" else VALID_REQUIREMENT if record_type == "requirement" else VALID_GENERAL
        if status not in valid:
            errors.append(f"{path}: invalid status '{status}' for type '{record_type}'")
    if record_type == "requirement" and "acceptance_criteria:" not in text:
        errors.append(f"{path}: requirement missing acceptance_criteria")
    if record_type == "task" and status == "completed" and "verification:" not in text:
        errors.append(f"{path}: completed task missing verification")


def validate_json(path: Path, text: str, errors: list[str]) -> None:
    try:
        json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON ({exc})")


def main() -> int:
    errors: list[str] = []
    seen_ids: dict[str, Path] = {}
    checked = 0

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "generated" in path.parts:
            continue
        if path.suffix not in {".md", ".yaml", ".yml", ".json", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        checked += 1

        secret = SECRET_RE.search(text)
        if secret:
            errors.append(f"{path}: possible committed secret near '{secret.group(1)}'")

        if path.suffix in {".yaml", ".yml"}:
            validate_yaml_like(path, text, errors)
            record_id = scalar(text, "id")
            if record_id and "registry" not in path.parts:
                if record_id in seen_ids:
                    errors.append(f"{path}: duplicate canonical id '{record_id}' also in {seen_ids[record_id]}")
                else:
                    seen_ids[record_id] = path
        elif path.suffix == ".json":
            validate_json(path, text, errors)

        if path.name == "context.md":
            words = len(re.findall(r"\b\w+\b", text))
            if words > 1500:
                errors.append(f"{path}: context exceeds 1500-word target ({words})")

    print(f"Checked {checked} files and {len(seen_ids)} canonical stable IDs.")
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Studio OS validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
