#!/usr/bin/env python3
"""Enroll a local product repository into App Factory and Studio OS.

Dependency-free by design. Run from the Studio OS checkout. This script changes
only the target product checkout and this Studio OS checkout; it never pushes.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTORY_REMOTE_INIT = "https://raw.githubusercontent.com/pri8771/iOS_app_factory_rules/main/scripts/remote-init.sh"


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, text=True, check=check)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def product_id(slug: str) -> str:
    return "PROD-" + re.sub(r"[^A-Z0-9]+", "-", slug.upper()).strip("-")


def yaml_quote(value: str) -> str:
    return json.dumps(value)


def ensure_factory(target: Path, name: str, mode: str, platforms: str, skip: bool) -> None:
    if (target / ".factory/project-context.json").exists():
        print("App Factory registration already present.")
        return
    if skip:
        print("App Factory bootstrap skipped by request.")
        return
    shell = (
        f"curl -fsSL {FACTORY_REMOTE_INIT} | bash -s -- "
        f"--target {json.dumps(str(target))} --mode {mode} "
        f"--name {json.dumps(name)} --platforms {json.dumps(platforms)}"
    )
    run(["bash", "-lc", shell], cwd=target)


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("created", path.relative_to(path.parents[len(path.parts) - 2]) if len(path.parts) > 2 else path)


def ensure_ui_manifests(target: Path, slug: str) -> None:
    prefix = slug.replace("-", "")
    write_if_missing(target / "quality/ui/screens.yaml", f"""schemaVersion: 1
product: {slug}
screens:
  - id: SCREEN-HOME
    name: Home
    rootIdentifier: {prefix}.home.root.container
    fixtures: [empty, content, long-text]
    requiredElements: []
    navigation:
      exits: []
""")
    write_if_missing(target / "quality/ui/journeys.yaml", f"""schemaVersion: 1
product: {slug}
journeys:
  - id: JOURNEY-LAUNCH
    name: Launch app
    fixture: empty
    launchArguments:
      - UI_TEST_MODE=1
      - UI_FIXTURE=empty
      - UI_RESET_STATE=1
      - UI_DISABLE_ANIMATIONS=1
    steps:
      - launchApp: true
      - assertVisible: {prefix}.home.root.container
    destructive: false
    externalAction: false
""")
    write_if_missing(target / "quality/ui/safe-actions.yaml", """schemaVersion: 1
safeActions: []
prohibitedClasses:
  - purchase
  - account-deletion
  - external-communication
  - production-data-deletion
  - permission-change
""")


def detect(target: Path) -> dict[str, object]:
    project_files = [p.name for p in target.iterdir() if p.suffix in {".xcodeproj", ".xcworkspace"}]
    return {
        "factoryRegistered": (target / ".factory/project-context.json").exists(),
        "standardLock": (target / ".factory/standard-lock.json").exists(),
        "repositoryMap": (target / ".factory/repository-map.json").exists(),
        "uiScreens": (target / "quality/ui/screens.yaml").exists(),
        "uiJourneys": (target / "quality/ui/journeys.yaml").exists(),
        "projectFiles": project_files,
        "hasTests": any("test" in p.name.lower() for p in target.rglob("*") if p.is_dir()),
    }


def upsert_registry(slug: str, name: str, repo: str, pid: str, today: str) -> None:
    path = ROOT / "registry/products.yaml"
    text = path.read_text(encoding="utf-8")
    if re.search(rf"(?m)^\s+- id:\s*{re.escape(pid)}\s*$", text):
        text = re.sub(
            rf"(?ms)(\s+- id:\s*{re.escape(pid)}\s*\n.*?)(?=\n\s+- id:|\nnotes:|\Z)",
            lambda m: re.sub(r"(?m)^\s{4}repository:.*$", f"    repository: {repo}", m.group(1)),
            text,
        )
        if f"context: products/{slug}/context.md" not in text:
            text = text.replace(f"    name: {name}\n", f"    name: {name}\n    context: products/{slug}/context.md\n    status_file: products/{slug}/status.yaml\n", 1)
    else:
        block = f"""  - id: {pid}
    slug: {slug}
    name: {name}
    stage: building
    health: yellow
    priority: p3
    context: products/{slug}/context.md
    status_file: products/{slug}/status.yaml
    repository: {repo}
    owner: priyansh
    updated_at: {today}

"""
        text = text.replace("notes:\n", block + "notes:\n")
    path.write_text(text, encoding="utf-8")


def write_studio_records(slug: str, name: str, repo: str, pid: str, report: dict[str, object]) -> None:
    today = date.today().isoformat()
    base = ROOT / "products" / slug
    base.mkdir(parents=True, exist_ok=True)
    (base / "manifest.yaml").write_text(f"""id: {pid}
type: product
title: {yaml_quote(name)}
summary: {yaml_quote('Repository-backed product enrolled through the Studio OS enrollment command.')}
status: active
owner: priyansh
updated_at: {today}
slug: {slug}
repository: {repo}
platforms: [ios]
factory_standard: 0.4.0
studio_standard: 0.1.0
""", encoding="utf-8")
    if not (base / "context.md").exists():
        (base / "context.md").write_text(f"""---
id: DOC-{pid}-CONTEXT
type: product-context
title: {name} Context
scope: product
product: {pid}
status: active
owner: priyansh
version: 0.1.0
updated_at: {today}
review_at: null
source_of_truth_for: [compact-product-context]
classification: internal
---

# {name} Context

## Definition

Repository-backed product enrolled in Studio OS. Product definition remains to be confirmed from canonical product documentation.

## Current State

- Repository: `{repo}`
- App Factory registered: `{str(report['factoryRegistered']).lower()}`
- Xcode project/workspace found: `{bool(report['projectFiles'])}`
- Automated UI manifests present: `{str(report['uiScreens'] and report['uiJourneys']).lower()}`

## Constraints

- Do not claim build or UI verification until it runs on macOS.
- Product-specific code and requirements remain authoritative in the product repository.

## Read Next

- Product repository root agent instructions
- `.factory/repository-map.json`
- Product repository `docs/README.md`
""", encoding="utf-8")
    (base / "status.yaml").write_text(f"""id: STATUS-{pid}
type: product-status
title: {yaml_quote(name + ' current status')}
summary: {yaml_quote('Enrolled; macOS build and generated UI execution remain unverified.')}
status: active
owner: priyansh
updated_at: {today}
product: {pid}
stage: building
health: yellow
priority: p3
repository: {repo}
current_milestone: Complete enrollment verification
active_work: []
blockers:
  - macOS build and simulator verification not yet recorded
decisions_needed: []
next_action: Run App Factory validation and generated UI smoke flows on macOS
verification:
  repository: verified
  app_factory: {str(report['factoryRegistered']).lower()}
  build: unverified
  ui_tests: unverified
""", encoding="utf-8")
    (base / "standard-lock.json").write_text(json.dumps({
        "schemaVersion": 1,
        "productId": pid,
        "standards": [
            {"id": "STD-STUDIO-OS", "version": "0.1.0"},
            {"id": "STD-IOS-APP-FACTORY", "version": "0.4.0"},
        ],
        "lastChecked": today,
    }, indent=2) + "\n", encoding="utf-8")
    upsert_registry(slug, name, repo, pid, today)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--product-id")
    parser.add_argument("--mode", choices=["new", "existing"], default="existing")
    parser.add_argument("--platforms", default="ios")
    parser.add_argument("--skip-factory-bootstrap", action="store_true")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if not (target / ".git").exists():
        raise SystemExit(f"Target is not a git checkout: {target}")
    slug = args.slug or slugify(args.name)
    pid = args.product_id or product_id(slug)

    ensure_factory(target, args.name, args.mode, args.platforms, args.skip_factory_bootstrap)
    ensure_ui_manifests(target, slug)
    report = detect(target)
    write_studio_records(slug, args.name, args.repo, pid, report)

    run([sys.executable, "scripts/validate_repo.py"], ROOT)
    run([sys.executable, "scripts/check_standard_drift.py"], ROOT)
    run([sys.executable, "scripts/generate_dashboard.py"], ROOT)

    output = {
        "status": "partial" if not report["projectFiles"] else "completed-with-mac-verification-pending",
        "productId": pid,
        "product": args.name,
        "repository": args.repo,
        "target": str(target),
        "appFactory": report,
        "studioRecord": f"products/{slug}/manifest.yaml",
        "humanActions": ["Run Xcode build and generated UI flows on macOS"],
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
