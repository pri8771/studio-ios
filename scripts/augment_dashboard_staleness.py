#!/usr/bin/env python3
"""Add freshness metadata and visible stale warnings to the generated dashboard."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dashboard/data.json"
INDEX = ROOT / "dashboard/index.html"
STALE_AFTER_DAYS = 14


def age_days(value: object) -> int | None:
    if not value:
        return None
    try:
        updated = date.fromisoformat(str(value)[:10])
    except ValueError:
        return None
    return (date.today() - updated).days


def main() -> int:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    products = payload.get("products", [])
    stale_count = 0
    unknown_count = 0
    for product in products:
        age = age_days(product.get("updated_at"))
        product["ageDays"] = age
        product["freshness"] = "unknown" if age is None else "stale" if age > STALE_AFTER_DAYS else "current"
        if product["freshness"] == "stale":
            stale_count += 1
        elif product["freshness"] == "unknown":
            unknown_count += 1
        product["freshnessWarning"] = (
            "No update date recorded" if age is None else
            f"Status is {age} days old" if age > STALE_AFTER_DAYS else
            ""
        )
    payload.setdefault("summary", {})["staleProducts"] = stale_count
    payload["summary"]["unknownFreshness"] = unknown_count
    payload["freshnessPolicy"] = {"staleAfterDays": STALE_AFTER_DAYS}
    payload["generatedAt"] = datetime.now(timezone.utc).isoformat()
    DATA.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    page = INDEX.read_text(encoding="utf-8")
    banner = (
        "<section class='panel freshness-banner'><strong>Data freshness</strong> "
        f"<span>{stale_count} stale · {unknown_count} unknown · stale after {STALE_AFTER_DAYS} days</span></section>"
    )
    page = page.replace("<h2>Products</h2>", banner + "<h2>Products</h2>", 1)
    page = page.replace("</style>", ".freshness-banner{display:flex;justify-content:space-between;gap:14px;margin:18px 0;background:#fff7ed;border-color:#fdba74}.freshness-banner span{color:#9a3412}</style>", 1)
    INDEX.write_text(page, encoding="utf-8")
    print(f"Added freshness metadata: {stale_count} stale, {unknown_count} unknown")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
