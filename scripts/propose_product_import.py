#!/usr/bin/env python3
"""Create a compact Studio OS import proposal from an accessible GitHub repository.

Requires the GitHub CLI to be installed and authenticated. The script is read-only.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

CANDIDATE_FILES = [
    "README.md",
    "AGENTS.md",
    "LLM_START_HERE.md",
    ".factory/project-context.json",
    ".factory/standard-lock.json",
    ".factory/repository-map.json",
    "docs/STATUS.md",
    "STATUS.md",
    "LAUNCH_READINESS.md",
]


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], check=True, text=True, capture_output=True)
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", help="owner/name")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    metadata = json.loads(gh("repo", "view", args.repository, "--json", "nameWithOwner,defaultBranchRef,isPrivate,isArchived,url"))
    found: dict[str, str] = {}
    for path in CANDIDATE_FILES:
        try:
            content = gh("api", f"repos/{args.repository}/contents/{path}", "-H", "Accept: application/vnd.github.raw+json")
        except subprocess.CalledProcessError:
            continue
        found[path] = content[:4000]

    proposal = {
        "schemaVersion": 1,
        "slug": args.slug,
        "name": args.name,
        "repository": metadata,
        "discoveredFiles": sorted(found),
        "factoryRegistered": ".factory/project-context.json" in found,
        "standardLockPresent": ".factory/standard-lock.json" in found,
        "statusSource": next((p for p in ["docs/STATUS.md", "STATUS.md", "LAUNCH_READINESS.md", "README.md"] if p in found), None),
        "requiresHumanReview": ["stage", "priority", "portfolio status", "product identity conflicts"],
        "notes": "This is a proposal. It does not modify the product repository.",
    }
    output = Path(args.output or f"generated/imports/{args.slug}.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
