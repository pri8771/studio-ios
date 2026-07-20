#!/usr/bin/env python3
"""Generate a dependency-free static portfolio dashboard from Studio OS records."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*([^#\n]+)", text)
    if not match:
        return None
    value = match.group(1).strip().strip("'\"")
    return None if value in {"null", ""} else value


def parse_products() -> list[dict[str, object]]:
    text = (ROOT / "registry/products.yaml").read_text(encoding="utf-8")
    products: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in text.splitlines():
        start = re.match(r"\s*- id:\s*(\S+)", line)
        if start:
            if current:
                products.append(current)
            current = {"id": start.group(1)}
            continue
        field = re.match(r"\s{4}(slug|name|stage|health|priority|repository|owner|updated_at|context|status_file):\s*(.*)", line)
        if field and current is not None:
            value = field.group(2).strip()
            current[field.group(1)] = None if value in {"null", ""} else value
    if current:
        products.append(current)

    for product in products:
        status_path = product.get("status_file")
        if not status_path:
            product["verification"] = "not imported"
            product["next_action"] = "Create compact product records"
            product["blocker_count"] = None
            continue
        path = ROOT / str(status_path)
        if not path.exists():
            product["verification"] = "missing status file"
            product["next_action"] = "Repair product registration"
            product["blocker_count"] = None
            continue
        status = path.read_text(encoding="utf-8")
        product["current_milestone"] = scalar(status, "current_milestone")
        product["next_action"] = scalar(status, "next_action")
        build = scalar(status, "build") or "unknown"
        ui = scalar(status, "ui_tests") or "unknown"
        factory = scalar(status, "app_factory") or "unknown"
        product["verification"] = f"factory {factory}; build {build}; UI {ui}"
        blocker_section = re.search(r"(?ms)^blockers:\s*\n(.*?)(?=^[A-Za-z_]+:|\Z)", status)
        product["blocker_count"] = len(re.findall(r"(?m)^\s+-\s+", blocker_section.group(1))) if blocker_section else 0
    return products


def badge(value: object) -> str:
    text = html.escape(str(value or "unknown"))
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return f'<span class="badge {slug}">{text}</span>'


def main() -> int:
    products = parse_products()
    summary = {
        "registered": len(products),
        "red": sum(p.get("health") == "red" for p in products),
        "missingRepositories": sum(not p.get("repository") for p in products),
        "fullyImported": sum(bool(p.get("status_file")) for p in products),
    }
    dashboard = {
        "schemaVersion": 2,
        "summary": summary,
        "products": products,
        "generatedFrom": ["registry/products.yaml", "products/*/status.yaml"],
    }
    out = ROOT / "dashboard"
    out.mkdir(parents=True, exist_ok=True)
    (out / "data.json").write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")

    rows = "\n".join(
        "<tr>"
        f"<td><strong>{html.escape(str(p.get('name', '')))}</strong><br><small>{html.escape(str(p.get('repository') or 'No repository'))}</small></td>"
        f"<td>{badge(p.get('stage'))}</td>"
        f"<td>{badge(p.get('health'))}</td>"
        f"<td>{badge(p.get('priority'))}</td>"
        f"<td>{html.escape(str(p.get('blocker_count') if p.get('blocker_count') is not None else '—'))}</td>"
        f"<td>{html.escape(str(p.get('verification', '')))}</td>"
        f"<td>{html.escape(str(p.get('next_action') or 'Import product details'))}</td>"
        "</tr>"
        for p in products
    )
    cards = "".join(
        f'<article><div class="metric">{value}</div><div>{label}</div></article>'
        for label, value in [
            ("Registered products", summary["registered"]),
            ("Fully imported", summary["fullyImported"]),
            ("Red health", summary["red"]),
            ("Missing repositories", summary["missingRepositories"]),
        ]
    )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Studio OS</title><style>
:root{{color-scheme:light dark}}body{{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#f5f5f7;color:#1d1d1f}}main{{max-width:1400px;margin:auto;padding:32px}}h1{{margin-bottom:4px}}.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:24px 0}}article,.card{{background:white;border-radius:16px;padding:20px;box-shadow:0 1px 4px #0002}}.metric{{font-size:2rem;font-weight:750}}.card{{overflow:auto}}table{{width:100%;border-collapse:collapse;min-width:1050px}}th,td{{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #ddd}}th{{font-size:.75rem;text-transform:uppercase;color:#666}}small{{color:#666}}.badge{{display:inline-block;padding:4px 8px;border-radius:999px;background:#e8e8ed;font-size:.78rem}}.red,.blocked{{background:#ffd7d7}}.yellow,.building{{background:#fff0bd}}.p1{{font-weight:700}}@media(prefers-color-scheme:dark){{body{{background:#111;color:#eee}}article,.card{{background:#1c1c1e}}th,td{{border-color:#38383a}}small,th{{color:#aaa}}.badge{{background:#333}}}}
</style></head><body><main><h1>Studio OS</h1><p>Generated portfolio, blocker, and verification view</p><section class="summary">{cards}</section><section class="card"><table><thead><tr><th>Product</th><th>Stage</th><th>Health</th><th>Priority</th><th>Blockers</th><th>Verification</th><th>Next action</th></tr></thead><tbody>{rows}</tbody></table></section></main></body></html>"""
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"Generated dashboard for {len(products)} products")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
