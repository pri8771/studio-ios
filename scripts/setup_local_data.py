#!/usr/bin/env python3
"""Create private, git-ignored local Studio OS data stores.

The files are intentionally simple JSON so humans and agents can inspect and
edit them without a database or third-party service. Existing files are never
overwritten.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local"

FILES: dict[str, object] = {
    "crm/contacts.json": {
        "schemaVersion": 1,
        "contacts": [],
        "notes": "Private local CRM. Do not commit this file.",
    },
    "marketing/content.json": {
        "schemaVersion": 1,
        "items": [],
        "notes": "Local content calendar and draft queue.",
    },
    "approvals.json": {
        "schemaVersion": 1,
        "items": [],
        "notes": "Actions requiring human approval before execution.",
    },
    "inbox.json": {
        "schemaVersion": 1,
        "items": [],
        "notes": "Unsorted local decision and capture inbox.",
    },
    "calendar/events.json": {
        "schemaVersion": 1,
        "events": [],
        "notes": "Optional local operating dates; not a replacement for a personal calendar.",
    },
}


def main() -> int:
    created = 0
    for relative, payload in FILES.items():
        path = LOCAL / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            print(f"exists  {path.relative_to(ROOT)}")
            continue
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        created += 1
        print(f"created {path.relative_to(ROOT)}")
    print(f"Local data ready: {created} new file(s), {len(FILES) - created} existing file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
