#!/usr/bin/env python3
"""Generate an opt-in static studio website without exposing private registry data."""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "website/config.yaml"
PRODUCTS = ROOT / "website/products.yaml"
OUTPUT = ROOT / "generated/public-site"


def scalar(text: str, key: str, default: str = "") -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.*)$", text)
    if not match:
        return default
    value = match.group(1).strip().strip("'\"")
    return "" if value in {"null", "~"} else value


def parse_products(text: str) -> list[dict[str, str | bool]]:
    products: list[dict[str, str | bool]] = []
    current: dict[str, str | bool] | None = None
    for line in text.splitlines():
        start = re.match(r"\s*- product_id:\s*(\S+)", line)
        if start:
            if current:
                products.append(current)
            current = {"product_id": start.group(1)}
            continue
        field = re.match(
            r"\s{4}(slug|name|published|tagline|description|status_label|app_url|waitlist_url|support_url|privacy_url|updated_at):\s*(.*)",
            line,
        )
        if field and current is not None:
            key, raw = field.groups()
            value = raw.strip().strip("'\"")
            if key == "published":
                current[key] = value.lower() == "true"
            else:
                current[key] = "" if value in {"null", "~"} else value
    if current:
        products.append(current)
    return products


def page_shell(title: str, body: str, site_name: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,sans-serif;color:#18181b;background:#fafafa}}*{{box-sizing:border-box}}body{{margin:0}}header,main,footer{{max-width:1080px;margin:auto;padding:24px}}header{{display:flex;justify-content:space-between;align-items:center}}a{{color:inherit}}.hero{{padding:72px 0 40px}}h1{{font-size:clamp(2.5rem,8vw,5.5rem);line-height:.98;letter-spacing:-.05em;margin:0 0 20px}}.lead{{font-size:1.25rem;max-width:700px;color:#52525b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}.card{{background:white;border:1px solid #e4e4e7;border-radius:20px;padding:24px}}.eyebrow{{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:#71717a}}footer{{color:#71717a;font-size:.9rem;padding-top:64px}}
</style></head><body><header><strong>{html.escape(site_name)}</strong><nav><a href="/">Products</a></nav></header><main>{body}</main><footer>© {html.escape(site_name)}. Product information is published only after explicit approval.</footer></body></html>"""


def main() -> int:
    config_text = CONFIG.read_text(encoding="utf-8")
    site_name = scalar(config_text, "name", "Studio")
    tagline = scalar(config_text, "tagline", "Focused software products.")
    published = [p for p in parse_products(PRODUCTS.read_text(encoding="utf-8")) if p.get("published") is True]

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)

    cards: list[str] = []
    for product in published:
        slug = str(product.get("slug", ""))
        name = str(product.get("name", slug))
        status = str(product.get("status_label", ""))
        tagline_text = str(product.get("tagline", ""))
        description = str(product.get("description", ""))
        cards.append(
            f'<article class="card"><div class="eyebrow">{html.escape(status)}</div>'
            f'<h2><a href="/apps/{html.escape(slug)}/">{html.escape(name)}</a></h2>'
            f'<p>{html.escape(tagline_text)}</p></article>'
        )
        product_body = (
            f'<section class="hero"><div class="eyebrow">{html.escape(status)}</div>'
            f'<h1>{html.escape(name)}</h1><p class="lead">{html.escape(tagline_text)}</p></section>'
            f'<section class="card"><p>{html.escape(description)}</p></section>'
        )
        product_dir = OUTPUT / "apps" / slug
        product_dir.mkdir(parents=True)
        (product_dir / "index.html").write_text(page_shell(name, product_body, site_name), encoding="utf-8")

    empty = '<section class="card"><p>No products are publicly listed yet.</p></section>'
    home_body = (
        f'<section class="hero"><div class="eyebrow">Independent software studio</div>'
        f'<h1>{html.escape(site_name)}</h1><p class="lead">{html.escape(tagline)}</p></section>'
        f'<section class="grid">{"".join(cards) if cards else empty}</section>'
    )
    (OUTPUT / "index.html").write_text(page_shell(site_name, home_body, site_name), encoding="utf-8")

    for route, title, text in (
        ("support", "Support", "Product-specific support details will appear here after approval."),
        ("privacy", "Privacy", "Product privacy notices are published separately and linked from each product page."),
    ):
        directory = OUTPUT / route
        directory.mkdir()
        body = f'<section class="hero"><h1>{html.escape(title)}</h1><p class="lead">{html.escape(text)}</p></section>'
        (directory / "index.html").write_text(page_shell(title, body, site_name), encoding="utf-8")

    print(f"Generated public site with {len(published)} approved products at {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
