#!/usr/bin/env python3
"""Generate a dependency-free static portfolio dashboard from registry/products.yaml."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
        field = re.match(r"\s{4}(slug|name|stage|health|priority|repository|owner|updated_at):\s*(.*)", line)
        if field and current is not None:
            value = field.group(2).strip()
            current[field.group(1)] = None if value in {"null", ""} else value
    if current:
        products.append(current)
    return products


def main() -> int:
    products = parse_products()
    dashboard = {
        "schemaVersion": 1,
        "productCount": len(products),
        "products": products,
        "generatedFrom": "registry/products.yaml",
    }
    out = ROOT / "dashboard"
    out.mkdir(parents=True, exist_ok=True)
    (out / "data.json").write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")

    rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(str(p.get('name', '')))}</td>"
        f"<td>{html.escape(str(p.get('stage', '')))}</td>"
        f"<td>{html.escape(str(p.get('health', '')))}</td>"
        f"<td>{html.escape(str(p.get('priority', '')))}</td>"
        f"<td>{html.escape(str(p.get('repository') or 'Not registered'))}</td>"
        "</tr>"
        for p in products
    )
    page = f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Studio OS</title><style>
body{{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#f5f5f7;color:#1d1d1f}}main{{max-width:1100px;margin:auto;padding:32px}}h1{{margin-bottom:4px}}.card{{background:white;border-radius:16px;padding:20px;box-shadow:0 1px 4px #0002;overflow:auto}}table{{width:100%;border-collapse:collapse}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #ddd}}th{{font-size:.8rem;text-transform:uppercase;color:#666}}.count{{font-size:2rem;font-weight:700}}
</style></head><body><main><h1>Studio OS</h1><p>Generated portfolio view</p><section class=\"card\"><div class=\"count\">{len(products)}</div><p>registered products</p><table><thead><tr><th>Product</th><th>Stage</th><th>Health</th><th>Priority</th><th>Repository</th></tr></thead><tbody>{rows}</tbody></table></section></main></body></html>"""
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"Generated dashboard for {len(products)} products")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
