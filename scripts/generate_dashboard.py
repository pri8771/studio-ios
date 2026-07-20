#!/usr/bin/env python3
"""Generate a dependency-free local Studio OS command center."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean(value: str) -> str | None:
    value = value.strip().strip("'\"")
    return None if value in {"", "null", "[]"} else value


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*([^#\n]+)", text)
    return clean(match.group(1)) if match else None


def nested_scalar(text: str, section: str, key: str) -> str | None:
    match = re.search(
        rf"(?ms)^\s*{re.escape(section)}:\s*\n(?P<body>(?:\s{{2,}}.*\n?)*)",
        text,
    )
    if not match:
        return None
    return scalar(match.group("body"), key)


def list_count(text: str, section: str) -> int:
    match = re.search(
        rf"(?ms)^\s*{re.escape(section)}:\s*\n(?P<body>(?:\s{{2,}}.*\n?)*)",
        text,
    )
    return len(re.findall(r"(?m)^\s+-\s+", match.group("body"))) if match else 0


def parse_registry(path: Path, allowed_fields: tuple[str, ...]) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    fields = "|".join(map(re.escape, allowed_fields))
    for line in text.splitlines():
        start = re.match(r"\s*- id:\s*(\S+)", line)
        if start:
            if current:
                records.append(current)
            current = {"id": start.group(1)}
            continue
        field = re.match(rf"\s{{4}}({fields}):\s*(.*)", line)
        if field and current is not None:
            current[field.group(1)] = clean(field.group(2))
    if current:
        records.append(current)
    return records


def parse_products() -> list[dict[str, object]]:
    products = parse_registry(
        ROOT / "registry/products.yaml",
        ("slug", "name", "stage", "health", "priority", "repository", "owner", "updated_at", "context", "status_file"),
    )
    for product in products:
        status_path = product.get("status_file")
        if not status_path:
            product.update(
                verification="not imported",
                next_action="Create compact product records",
                current_milestone="Not imported",
                blocker_count=None,
            )
            continue
        path = ROOT / str(status_path)
        if not path.exists():
            product.update(
                verification="missing status file",
                next_action="Repair product registration",
                current_milestone="Registration error",
                blocker_count=None,
            )
            continue
        status = path.read_text(encoding="utf-8")
        product["current_milestone"] = nested_scalar(status, "current_milestone", "name") or scalar(status, "current_milestone") or "Unspecified"
        product["next_action"] = nested_scalar(status, "next_action", "task") or scalar(status, "next_action") or "Unspecified"
        build = nested_scalar(status, "verification", "build") or scalar(status, "build") or "unknown"
        ui = nested_scalar(status, "verification", "ui_tests") or nested_scalar(status, "verification", "ui_flows_maestro") or scalar(status, "ui_tests") or "unknown"
        factory = nested_scalar(status, "verification", "factory_registration") or scalar(status, "app_factory") or "unknown"
        product["verification"] = f"factory {factory}; build {build}; UI {ui}"
        product["blocker_count"] = list_count(status, "blockers")
    return products


def parse_services() -> list[dict[str, object]]:
    return parse_registry(
        ROOT / "registry/services.yaml",
        ("name", "purpose", "status", "owner", "free_tier_limit", "usage_warning", "replacement", "failure_behavior", "updated_at"),
    )


def parse_tasks() -> list[dict[str, object]]:
    tasks = parse_registry(ROOT / "atlas/tasks/index.yaml", ("title", "file", "status", "summary"))
    for task in tasks:
        task["path"] = f"atlas/tasks/{task.get('file')}" if task.get("file") else None
    return tasks


def badge(value: object) -> str:
    text = html.escape(str(value or "unknown"))
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return f'<span class="badge {slug}">{text}</span>'


def esc(value: object, fallback: str = "—") -> str:
    return html.escape(str(value if value not in {None, ""} else fallback))


def product_rows(products: list[dict[str, object]]) -> str:
    return "\n".join(
        "<tr>"
        f"<td><strong>{esc(p.get('name'))}</strong><br><small>{esc(p.get('repository'), 'No repository')}</small></td>"
        f"<td>{badge(p.get('stage'))}</td><td>{badge(p.get('health'))}</td><td>{badge(p.get('priority'))}</td>"
        f"<td>{esc(p.get('current_milestone'))}</td><td>{esc(p.get('blocker_count'))}</td>"
        f"<td>{esc(p.get('verification'))}</td><td>{esc(p.get('next_action'))}</td>"
        "</tr>"
        for p in products
    )


def service_cards(services: list[dict[str, object]]) -> str:
    return "".join(
        f"<article class='service'><div class='row'><strong>{esc(s.get('name'))}</strong>{badge(s.get('status'))}</div>"
        f"<p>{esc(s.get('purpose'))}</p><small><b>Free/local policy:</b> {esc(s.get('free_tier_limit'))}</small>"
        f"<small><b>Fallback:</b> {esc(s.get('replacement'))}</small></article>"
        for s in services
    )


def task_cards(tasks: list[dict[str, object]]) -> str:
    return "".join(
        f"<article class='task'><div class='row'><strong>{esc(t.get('title'))}</strong>{badge(t.get('status'))}</div>"
        f"<p>{esc(t.get('summary'))}</p><small>{esc(t.get('path'))}</small></article>"
        for t in tasks
    )


def main() -> int:
    products = parse_products()
    services = parse_services()
    tasks = parse_tasks()
    summary = {
        "registered": len(products),
        "red": sum(p.get("health") == "red" for p in products),
        "missingRepositories": sum(not p.get("repository") for p in products),
        "fullyImported": sum(bool(p.get("status_file")) for p in products),
        "activeServices": sum(s.get("status") in {"active", "foundation-ready"} for s in services),
        "openTasks": sum(t.get("status") not in {"completed", "cancelled"} for t in tasks),
    }
    dashboard = {
        "schemaVersion": 3,
        "summary": summary,
        "products": products,
        "services": services,
        "tasks": tasks,
        "generatedFrom": ["registry/products.yaml", "products/*/status.yaml", "registry/services.yaml", "atlas/tasks/index.yaml"],
    }
    out = ROOT / "dashboard"
    out.mkdir(parents=True, exist_ok=True)
    (out / "data.json").write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")

    metrics = [
        ("Registered products", summary["registered"]),
        ("Fully imported", summary["fullyImported"]),
        ("Red health", summary["red"]),
        ("Missing repositories", summary["missingRepositories"]),
        ("Active/local services", summary["activeServices"]),
        ("Open setup tasks", summary["openTasks"]),
    ]
    metric_cards = "".join(f"<article class='metric-card'><div class='metric'>{value}</div><div>{label}</div></article>" for label, value in metrics)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Studio OS</title><style>
:root{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,sans-serif;background:#f4f4f5;color:#18181b}}*{{box-sizing:border-box}}body{{margin:0}}main{{max-width:1500px;margin:auto;padding:34px}}h1{{font-size:2.4rem;letter-spacing:-.04em;margin:0}}h2{{margin-top:38px}}.sub{{color:#71717a}}.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:24px 0}}article,.panel{{background:white;border:1px solid #e4e4e7;border-radius:17px;padding:18px;box-shadow:0 7px 25px #18181b0a}}.metric{{font-size:2rem;font-weight:780}}.panel{{overflow:auto}}table{{width:100%;border-collapse:collapse;min-width:1250px}}th,td{{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #e4e4e7}}th{{font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:#71717a}}small{{display:block;color:#71717a;margin-top:7px;line-height:1.4}}.badge{{display:inline-block;padding:4px 8px;border-radius:999px;background:#e4e4e7;font-size:.72rem;white-space:nowrap}}.red,.blocked,.not-configured{{background:#fecaca}}.yellow,.building,.planned,.selected{{background:#fef3c7}}.active,.verified,.foundation-ready,.completed{{background:#dcfce7}}.p1{{font-weight:800}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(275px,1fr));gap:12px}}.row{{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}}.service p,.task p{{color:#52525b;line-height:1.45}}@media(max-width:700px){{main{{padding:22px 14px}}}}
</style></head><body><main><h1>Studio OS</h1><p class="sub">Local portfolio, services, blockers, verification, and setup queue</p>
<section class="summary">{metric_cards}</section>
<h2>Products</h2><section class="panel"><table><thead><tr><th>Product</th><th>Stage</th><th>Health</th><th>Priority</th><th>Milestone</th><th>Blockers</th><th>Verification</th><th>Next action</th></tr></thead><tbody>{product_rows(products)}</tbody></table></section>
<h2>Shared services</h2><section class="cards">{service_cards(services)}</section>
<h2>Atlas / human queue</h2><section class="cards">{task_cards(tasks)}</section>
</main></body></html>"""
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"Generated dashboard for {len(products)} products, {len(services)} services, and {len(tasks)} setup tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
