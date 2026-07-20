#!/usr/bin/env python3
"""Generate a deliberately sanitized static portfolio preview."""
from __future__ import annotations
import html, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def products():
    result, current = [], {}
    for line in (ROOT / "registry/products.yaml").read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*- id:\s*(\S+)", line)
        if match:
            if current: result.append((current.get("name", "Unnamed product"), current.get("stage", "planned")))
            current = {"id": match.group(1)}
        match = re.match(r"\s{4}(name|stage):\s*(.+)", line)
        if match and current: current[match.group(1)] = match.group(2).strip().strip("'\"")
    if current: result.append((current.get("name", "Unnamed product"), current.get("stage", "planned")))
    return result
def main() -> int:
    items = products(); cards = "".join(f"<li><strong>{html.escape(n)}</strong><span>{html.escape(s)}</span></li>" for n,s in items); out = ROOT / "generated/public-site"; out.mkdir(parents=True, exist_ok=True)
    out.joinpath("index.html").write_text(f"<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Studio preview</title><style>body{{font-family:system-ui;margin:0;background:#101827;color:#f8fafc}}main{{max-width:900px;margin:auto;padding:5rem 1.5rem}}h1{{font-size:clamp(2.5rem,8vw,5rem);margin:0}}p{{color:#cbd5e1;max-width:60ch}}ul{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1rem;padding:0;list-style:none}}li{{background:#1e293b;padding:1.25rem;border-radius:1rem}}span{{display:block;color:#93c5fd;margin-top:.5rem}}small{{color:#94a3b8}}</style><main><small>Local shared website preview</small><h1>Studio</h1><p>A small portfolio of software products. This local preview publishes no private operating records, local stores, contact data, task details, or credentials.</p><ul>{cards}</ul></main></html>", encoding="utf-8")
    print(f"Generated sanitized website preview for {len(items)} products"); return 0
if __name__ == "__main__": raise SystemExit(main())
