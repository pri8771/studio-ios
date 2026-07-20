#!/usr/bin/env python3
"""Generate a dependency-free local Studio OS command-center dashboard."""
from __future__ import annotations
import html, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def unquote(value: str) -> str: return value.strip().strip("'\"")
def records(path: Path) -> list[dict[str, str]]:
    items, current = [], None
    if not path.exists(): return items
    for line in path.read_text(encoding="utf-8").splitlines():
        start = re.match(r"\s*- id:\s*(\S+)", line)
        if start:
            if current: items.append(current)
            current = {"id": start.group(1)}; continue
        field = re.match(r"\s{4}([a-z_]+):\s*(.*)", line)
        if field and current is not None: current[field.group(1)] = unquote(field.group(2))
    if current: items.append(current)
    return items
def scalar(text: str, key: str) -> str | None:
    hit = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n#]+)$", text); return unquote(hit.group(1)) if hit else None
def nested(text: str, parent: str, key: str) -> str | None:
    block = re.search(rf"(?ms)^{parent}:\s*\n(.*?)(?=^[A-Za-z_]+:|\Z)", text)
    if not block: return None
    hit = re.search(rf"(?m)^\s+{re.escape(key)}:\s*(.+)$", block.group(1)); return unquote(hit.group(1)) if hit else None
def product_view() -> list[dict[str, str]]:
    result = records(ROOT / "registry/products.yaml")
    for product in result:
        status_path = product.get("status_file"); status = (ROOT / status_path).read_text(encoding="utf-8") if status_path and (ROOT / status_path).exists() else ""
        blockers = re.search(r"(?ms)^blockers:\s*\n(.*?)(?=^[A-Za-z_]+:|\Z)", status)
        product.update({"current_milestone": scalar(status,"current_milestone") or nested(status,"current_milestone","name") or "Not recorded", "next_action": scalar(status,"next_action") or nested(status,"next_action","task") or "Record next action", "verification": "; ".join(f"{label} {nested(status,'verification',key) or 'unknown'}" for label,key in [("repo","repository"),("factory","app_factory"),("build","build"),("tests","ui_tests")]), "blocker_count": str(len(re.findall(r"(?m)^\s+-\s+", blockers.group(1))) if blockers else 0)})
    return result
def task_view() -> list[dict[str, str]]:
    result = records(ROOT / "atlas/tasks/index.yaml")
    for task in result:
        file = ROOT / "atlas/tasks" / task.get("file", "")
        text = file.read_text(encoding="utf-8") if file.exists() else ""
        task["related"] = scalar(text,"product") or scalar(text,"service") or "Studio"; task["human_only"] = "yes" if "Human-only checkpoints" in text else "no"
    return result
def esc(value: object) -> str: return html.escape(str(value or "—"))
def table(headers, rows, fields) -> str:
    body = "".join("<tr>" + "".join(f"<td>{esc(row.get(field))}</td>" for field in fields) + "</tr>" for row in rows) or f"<tr><td colspan={len(fields)}>No records.</td></tr>"
    return "<div class=table><table><thead><tr>" + "".join(f"<th>{esc(h)}</th>" for h in headers) + f"</tr></thead><tbody>{body}</tbody></table></div>"
def main() -> int:
    products, services, tasks = product_view(), records(ROOT / "registry/services.yaml"), task_view()
    data = {"schemaVersion":3,"localOnly":True,"products":products,"services":services,"tasks":tasks,"generatedFrom":["registry/products.yaml","registry/services.yaml","atlas/tasks/index.yaml","products/*/status.yaml"]}; out = ROOT / "dashboard"; out.mkdir(exist_ok=True); (out / "data.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    page = f"""<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Studio OS — Local</title><style>:root{{color-scheme:light dark}}body{{margin:0;font:15px system-ui,sans-serif;background:#f5f7fb;color:#14213d}}main{{max-width:1500px;margin:auto;padding:2rem}}.notice{{background:#dbeafe;border-left:4px solid #2563eb;padding:1rem;border-radius:.5rem}}section{{margin-top:2rem;background:Canvas;padding:1.25rem;border-radius:1rem;box-shadow:0 1px 4px #0002}}h1{{margin-bottom:.3rem}}.table{{overflow:auto}}table{{width:100%;border-collapse:collapse;min-width:900px}}th,td{{text-align:left;vertical-align:top;padding:.75rem;border-bottom:1px solid #d6dae3}}th{{font-size:.75rem;text-transform:uppercase;color:#64748b}}@media(max-width:600px){{main{{padding:1rem}}}}@media(prefers-color-scheme:dark){{body{{background:#111827;color:#e5e7eb}}th,td{{border-color:#374151}}.notice{{background:#172554}}}}</style><main><h1>Studio OS</h1><p>Private local command center</p><div class=notice><strong>Local-only status.</strong> This dashboard runs locally; cloud deployment is not configured. CRM, marketing, calendar, and approvals use private local stores. The shared website preview contains no private operating information.</div><section><h2>Portfolio</h2>{table(['Product','ID','Repository','Stage','Health','Priority','Milestone','Blockers','Verification','Next action'],products,['name','id','repository','stage','health','priority','current_milestone','blocker_count','verification','next_action'])}</section><section><h2>Shared services</h2>{table(['Service','Status','Purpose','Data held','Local policy','Failure behavior','Export / replacement'],services,['name','status','purpose','data_held','free_tier_limit','failure_behavior','export_path'])}</section><section><h2>Work queue</h2>{table(['Task','Status','Summary','Related','Human-only'],tasks,['title','status','summary','related','human_only'])}</section></main></html>"""
    (out / "index.html").write_text(page,encoding="utf-8"); print(f"Generated dashboard for {len(products)} products, {len(services)} services, and {len(tasks)} tasks"); return 0
if __name__ == "__main__": raise SystemExit(main())
