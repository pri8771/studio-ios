#!/usr/bin/env python3
"""Preview or safely initialize a local Studio OS workspace."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

DIRECTORIES = ["00_Inbox", "01_Studio_Operations", "02_Products", "03_Marketing", "04_Sales_CRM", "05_Finance_Legal", "06_Research", "07_Assets", "08_Exports", "09_Private", "99_Archive"]
PRIVATE_FILES = {".local/crm/contacts.json": {"schemaVersion": 1, "contacts": []}, ".local/marketing/content.json": {"schemaVersion": 1, "content": []}, ".local/calendar/events.json": {"schemaVersion": 1, "events": []}, ".local/approvals.json": {"schemaVersion": 1, "approvals": []}, ".local/inbox.json": {"schemaVersion": 1, "items": []}}
README = "# Private local stores\n\nPrivate, local substitutes for CRM, marketing, calendar, approval, and inbox services. Ignored by Git. Do not store secrets or production customer data here.\n"

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, default=Path.cwd()); parser.add_argument("--product", action="append", default=[]); parser.add_argument("--apply", action="store_true"); args = parser.parse_args()
    root = args.root.expanduser().resolve()
    planned = [root / name for name in DIRECTORIES] + [root / "02_Products" / product.replace(" ", "_") for product in args.product] + [root / path for path in PRIVATE_FILES] + [root / ".local/README.md"]
    created, preserved = [], []
    for path in planned:
        if path.exists(): preserved.append(str(path)); continue
        if not args.apply: created.append(str(path)); continue
        if path.suffix == ".json": path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(PRIVATE_FILES[str(path.relative_to(root))], indent=2) + "\n", encoding="utf-8")
        elif path.name == "README.md": path.parent.mkdir(parents=True, exist_ok=True); path.write_text(README, encoding="utf-8")
        else: path.mkdir(parents=True, exist_ok=False)
        created.append(str(path))
    print(json.dumps({"mode": "apply" if args.apply else "preview", "root": str(root), "created": created, "preserved": preserved}, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
