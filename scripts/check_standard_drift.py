#!/usr/bin/env python3
"""Check product standard locks against the Studio OS standards registry."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def standards_registry() -> dict[str, str]:
    text = (ROOT / "registry/standards.yaml").read_text(encoding="utf-8")
    result: dict[str, str] = {}
    current_id: str | None = None
    for line in text.splitlines():
        m = re.match(r"\s*- id:\s*(\S+)", line)
        if m:
            current_id = m.group(1)
            continue
        m = re.match(r"\s+version:\s*(\S+)", line)
        if m and current_id:
            result[current_id] = m.group(1)
            current_id = None
    return result


def main() -> int:
    expected = standards_registry()
    findings: list[dict[str, object]] = []
    for lock_path in ROOT.glob("products/*/standard-lock.json"):
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        for standard in lock.get("standards", []):
            standard_id = standard.get("id")
            actual = standard.get("version")
            wanted = expected.get(standard_id)
            if wanted and actual != wanted:
                findings.append({"product": lock.get("productId"), "standard": standard_id, "actual": actual, "expected": wanted})
    report = {"schemaVersion": 1, "findings": findings, "status": "drift" if findings else "current"}
    output = ROOT / "generated/standard-drift.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
