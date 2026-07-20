#!/usr/bin/env python3
"""Studio OS command line interface.

Dependency-free control plane for creating, enrolling, validating, and reporting
on products. External mutations are explicit, dry-runnable, and rolled back where
safe. The CLI intentionally delegates App Factory enrollment to studio_enroll.py
so there is one canonical implementation of product registration.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OWNER = os.environ.get("STUDIO_GITHUB_OWNER", "pri8771")


class StudioError(RuntimeError):
    """Expected operational error with a user-actionable message."""


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise StudioError("Name must contain at least one letter or number.")
    return slug


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
    dry_run: bool = False,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command))
    if dry_run:
        return subprocess.CompletedProcess(command, 0, "", "")
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            check=True,
            capture_output=capture,
        )
    except FileNotFoundError as exc:
        raise StudioError(f"Required command is not installed: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise StudioError(
            f"Command failed ({exc.returncode}): {' '.join(command)}"
            + (f"\n{detail}" if detail else "")
        ) from exc


@dataclass
class Transaction:
    dry_run: bool = False
    rollback_actions: list[tuple[str, Callable[[], None]]] = field(default_factory=list)

    def defer(self, label: str, action: Callable[[], None]) -> None:
        if not self.dry_run:
            self.rollback_actions.append((label, action))

    def rollback(self) -> None:
        for label, action in reversed(self.rollback_actions):
            try:
                print(f"rollback: {label}")
                action()
            except Exception as exc:  # best effort; preserve original failure
                print(f"warning: rollback failed for {label}: {exc}", file=sys.stderr)


def ensure_clean_destination(path: Path, *, allow_existing: bool = False) -> None:
    if path.exists() and not allow_existing:
        raise StudioError(f"Destination already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str, *, dry_run: bool) -> None:
    print("write", path)
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def document_ai_files(name: str, slug: str) -> dict[str, str]:
    package = slug.replace("-", "_")
    return {
        "README.md": f"""# {name}\n\nConfigurable document intake, extraction, validation, review, and export.\n\n## Start\n\n```bash\ncp .env.example .env\ndocker compose up --build\n```\n\n- API: http://localhost:8000\n- API docs: http://localhost:8000/docs\n- Web: http://localhost:5173\n\n## Architecture\n\nReceived → preprocessing → OCR → classification → extraction → validation → review/approval → export.\n\nProvider interfaces prevent hard-coding an OCR vendor, LLM vendor, schema, intake source, or downstream system.\n""",
        ".gitignore": ".env\n__pycache__/\n*.pyc\n.pytest_cache/\nnode_modules/\ndist/\n.venv/\ndata/*\n!data/.gitkeep\n",
        ".env.example": "DATABASE_URL=postgresql://document_flow:document_flow@db:5432/document_flow\nSTORAGE_ROOT=/data\n",
        "docker-compose.yml": f"""services:\n  db:\n    image: postgres:16-alpine\n    environment:\n      POSTGRES_USER: document_flow\n      POSTGRES_PASSWORD: document_flow\n      POSTGRES_DB: document_flow\n    healthcheck:\n      test: [\"CMD-SHELL\", \"pg_isready -U document_flow\"]\n      interval: 5s\n      timeout: 5s\n      retries: 10\n    volumes: [postgres-data:/var/lib/postgresql/data]\n  api:\n    build: ./api\n    environment:\n      DATABASE_URL: postgresql://document_flow:document_flow@db:5432/document_flow\n      STORAGE_ROOT: /data\n    volumes: [./data:/data]\n    ports: [\"8000:8000\"]\n    depends_on:\n      db:\n        condition: service_healthy\n  web:\n    build: ./web\n    environment:\n      VITE_API_URL: http://localhost:8000\n    ports: [\"5173:5173\"]\n    depends_on: [api]\nvolumes:\n  postgres-data:\n""",
        "api/Dockerfile": "FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY app app\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n",
        "api/requirements.txt": "fastapi==0.115.6\nuvicorn[standard]==0.34.0\npydantic==2.10.5\npython-multipart==0.0.20\npsycopg[binary]==3.2.3\n",
        "api/app/__init__.py": "",
        "api/app/main.py": f'''from __future__ import annotations\n\nfrom enum import StrEnum\nfrom typing import Any, Protocol\nfrom uuid import UUID, uuid4\n\nfrom fastapi import FastAPI, File, HTTPException, UploadFile\nfrom pydantic import BaseModel, Field\n\napp = FastAPI(title={name!r}, version="0.1.0")\n\n\nclass DocumentStatus(StrEnum):\n    RECEIVED = "RECEIVED"\n    PREPROCESSING = "PREPROCESSING"\n    OCR = "OCR"\n    CLASSIFYING = "CLASSIFYING"\n    EXTRACTING = "EXTRACTING"\n    VALIDATING = "VALIDATING"\n    REVIEW_REQUIRED = "REVIEW_REQUIRED"\n    APPROVED = "APPROVED"\n    EXPORTING = "EXPORTING"\n    COMPLETED = "COMPLETED"\n    FAILED = "FAILED"\n\n\nclass ExtractionField(BaseModel):\n    name: str\n    value: Any = None\n    confidence: float = Field(ge=0, le=1)\n    source: str | None = None\n\n\nclass DocumentRecord(BaseModel):\n    id: UUID\n    filename: str\n    content_type: str\n    status: DocumentStatus\n    document_type: str | None = None\n    fields: list[ExtractionField] = []\n    errors: list[str] = []\n\n\nclass OCRProvider(Protocol):\n    async def extract_text(self, content: bytes, content_type: str) -> str: ...\n\n\nclass ExtractionProvider(Protocol):\n    async def extract(self, text: str, schema: dict[str, Any]) -> list[ExtractionField]: ...\n\n\nDOCUMENTS: dict[UUID, DocumentRecord] = {{}}\n\n\n@app.get("/health")\ndef health() -> dict[str, str]:\n    return {{"status": "ok"}}\n\n\n@app.post("/documents", response_model=DocumentRecord, status_code=201)\nasync def upload_document(file: UploadFile = File(...)) -> DocumentRecord:\n    allowed = {{"application/pdf", "image/png", "image/jpeg"}}\n    if file.content_type not in allowed:\n        raise HTTPException(415, f"Unsupported content type: {{file.content_type}}")\n    content = await file.read()\n    if not content:\n        raise HTTPException(400, "Empty file")\n    record = DocumentRecord(\n        id=uuid4(),\n        filename=file.filename or "upload",\n        content_type=file.content_type,\n        status=DocumentStatus.RECEIVED,\n    )\n    DOCUMENTS[record.id] = record\n    return record\n\n\n@app.get("/documents", response_model=list[DocumentRecord])\ndef list_documents() -> list[DocumentRecord]:\n    return list(DOCUMENTS.values())\n\n\n@app.get("/documents/{{document_id}}", response_model=DocumentRecord)\ndef get_document(document_id: UUID) -> DocumentRecord:\n    try:\n        return DOCUMENTS[document_id]\n    except KeyError as exc:\n        raise HTTPException(404, "Document not found") from exc\n''',
        "web/Dockerfile": "FROM node:22-alpine\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install\nCOPY . .\nCMD [\"npm\", \"run\", \"dev\", \"--\", \"--host\", \"0.0.0.0\"]\n",
        "web/package.json": json.dumps({"name": package + "_web", "private": True, "version": "0.1.0", "type": "module", "scripts": {"dev": "vite", "build": "tsc && vite build"}, "dependencies": {"@vitejs/plugin-react": "latest", "vite": "latest", "typescript": "latest", "react": "latest", "react-dom": "latest"}, "devDependencies": {"@types/react": "latest", "@types/react-dom": "latest"}}, indent=2) + "\n",
        "web/index.html": '<!doctype html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Document Flow</title></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>\n',
        "web/src/main.tsx": '''import React, { useEffect, useState } from "react";\nimport { createRoot } from "react-dom/client";\n\ntype DocumentRecord = { id: string; filename: string; content_type: string; status: string };\nconst API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";\n\nfunction App() {\n  const [documents, setDocuments] = useState<DocumentRecord[]>([]);\n  const [error, setError] = useState<string | null>(null);\n  const load = () => fetch(`${API}/documents`).then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); }).then(setDocuments).catch(e => setError(String(e)));\n  useEffect(load, []);\n  async function upload(file: File) {\n    const body = new FormData(); body.append("file", file);\n    const response = await fetch(`${API}/documents`, { method: "POST", body });\n    if (!response.ok) { setError(await response.text()); return; }\n    await load();\n  }\n  return <main style={{maxWidth: 960, margin: "40px auto", fontFamily: "system-ui"}}>\n    <h1>Document Flow</h1><p>Upload documents for extraction, validation, review, and export.</p>\n    <input type="file" accept="application/pdf,image/png,image/jpeg" onChange={e => e.target.files?.[0] && upload(e.target.files[0])} />\n    {error && <p role="alert">{error}</p>}\n    <table><thead><tr><th>File</th><th>Type</th><th>Status</th></tr></thead><tbody>{documents.map(d => <tr key={d.id}><td>{d.filename}</td><td>{d.content_type}</td><td>{d.status}</td></tr>)}</tbody></table>\n  </main>;\n}\ncreateRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);\n''',
        "web/tsconfig.json": json.dumps({"compilerOptions": {"target": "ES2022", "useDefineForClassFields": True, "lib": ["ES2022", "DOM", "DOM.Iterable"], "allowJs": False, "skipLibCheck": True, "esModuleInterop": True, "allowSyntheticDefaultImports": True, "strict": True, "forceConsistentCasingInFileNames": True, "module": "ESNext", "moduleResolution": "Bundler", "resolveJsonModule": True, "isolatedModules": True, "noEmit": True, "jsx": "react-jsx"}, "include": ["src"]}, indent=2) + "\n",
        ".github/workflows/ci.yml": "name: CI\non:\n  pull_request:\n  push:\n    branches: [main]\njobs:\n  validate:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with: {python-version: '3.12'}\n      - run: python -m compileall api/app\n      - uses: actions/setup-node@v4\n        with: {node-version: '22', cache: npm, cache-dependency-path: web/package-lock.json}\n      - run: npm install\n        working-directory: web\n      - run: npm run build\n        working-directory: web\n",
        "docs/README.md": f"# {name} documentation\n\nCanonical product documentation index.\n",
        "docs/ARCHITECTURE.md": "# Architecture\n\nProvider-based modular monolith for the MVP. Persisted workflow state is authoritative; every transition is explicit and auditable.\n",
        "docs/STATUS.md": "# Status\n\nStage: scaffolded\n\nNext: persistent repository, pipeline worker, schema configuration, review UI, and output connectors.\n",
        "data/.gitkeep": "",
    }


def generate_template(name: str, slug: str, template: str, target: Path, dry_run: bool) -> None:
    if template != "document-ai":
        raise StudioError(f"Unknown project template: {template}")
    for relative, content in document_ai_files(name, slug).items():
        write_text(target / relative, content, dry_run=dry_run)


def git_init(target: Path, *, dry_run: bool) -> None:
    run(["git", "init", "-b", "main"], cwd=target, dry_run=dry_run)
    run(["git", "add", "."], cwd=target, dry_run=dry_run)
    run(["git", "commit", "-m", "chore: initialize product from Studio OS"], cwd=target, dry_run=dry_run)


def create_remote(repo: str, target: Path, *, private: bool, dry_run: bool) -> None:
    visibility = "--private" if private else "--public"
    run(["gh", "repo", "create", repo, visibility, "--source", str(target), "--remote", "origin", "--push"], cwd=target, dry_run=dry_run)


def command_new(args: argparse.Namespace) -> dict[str, object]:
    slug = args.slug or slugify(args.name)
    repo = args.repo or f"{args.owner}/{slug}"
    target = Path(args.target or Path.home() / "Developer" / slug).expanduser().resolve()
    ensure_clean_destination(target)
    tx = Transaction(args.dry_run)
    try:
        print(f"Creating {args.name} at {target}")
        if not args.dry_run:
            target.mkdir(parents=True)
        tx.defer("remove generated local checkout", lambda: shutil.rmtree(target, ignore_errors=True))
        generate_template(args.name, slug, args.template, target, args.dry_run)
        git_init(target, dry_run=args.dry_run)
        if not args.no_remote:
            create_remote(repo, target, private=args.private, dry_run=args.dry_run)
        enroll = [sys.executable, str(ROOT / "scripts/studio_enroll.py"), "--target", str(target), "--repo", repo, "--name", args.name, "--slug", slug, "--mode", "new"]
        if args.skip_factory_bootstrap:
            enroll.append("--skip-factory-bootstrap")
        run(enroll, cwd=ROOT, dry_run=args.dry_run)
        return {"status": "completed" if not args.dry_run else "dry-run", "product": args.name, "slug": slug, "repository": repo, "target": str(target), "template": args.template}
    except Exception:
        tx.rollback()
        raise


def command_enroll(args: argparse.Namespace) -> dict[str, object]:
    target = Path(args.target).expanduser().resolve()
    slug = args.slug or slugify(args.name)
    cmd = [sys.executable, str(ROOT / "scripts/studio_enroll.py"), "--target", str(target), "--repo", args.repo, "--name", args.name, "--slug", slug, "--mode", "existing"]
    if args.skip_factory_bootstrap:
        cmd.append("--skip-factory-bootstrap")
    run(cmd, cwd=ROOT, dry_run=args.dry_run)
    return {"status": "completed" if not args.dry_run else "dry-run", "product": args.name, "repository": args.repo, "target": str(target)}


def command_validate(args: argparse.Namespace) -> dict[str, object]:
    checks = ["validate_repo.py", "check_standard_drift.py"]
    for check in checks:
        run([sys.executable, str(ROOT / "scripts" / check)], cwd=ROOT, dry_run=args.dry_run)
    return {"status": "passed" if not args.dry_run else "dry-run", "checks": checks}


def command_dashboard(args: argparse.Namespace) -> dict[str, object]:
    run([sys.executable, str(ROOT / "scripts/generate_dashboard.py")], cwd=ROOT, dry_run=args.dry_run)
    index = ROOT / "dashboard/index.html"
    data = ROOT / "dashboard/data.json"
    if not args.dry_run and (not index.exists() or not data.exists()):
        raise StudioError("Dashboard generator completed but expected outputs are missing.")
    return {"status": "generated" if not args.dry_run else "dry-run", "index": str(index), "data": str(data)}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="studio", description="Studio OS product factory")
    root.add_argument("--json", action="store_true", help="Print final result as JSON")
    root.add_argument("--dry-run", action="store_true", help="Describe actions without mutating anything")
    sub = root.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="Create, bootstrap, and register a new product")
    new.add_argument("--name", required=True)
    new.add_argument("--slug")
    new.add_argument("--template", default="document-ai", choices=["document-ai"])
    new.add_argument("--owner", default=DEFAULT_OWNER)
    new.add_argument("--repo", help="owner/repository; defaults to owner/slug")
    new.add_argument("--target", help="local destination; defaults to ~/Developer/<slug>")
    visibility = new.add_mutually_exclusive_group()
    visibility.add_argument("--private", action="store_true", default=True)
    visibility.add_argument("--public", action="store_false", dest="private")
    new.add_argument("--no-remote", action="store_true", help="Do not create or push a GitHub repository")
    new.add_argument("--skip-factory-bootstrap", action="store_true")
    new.set_defaults(handler=command_new)

    enroll = sub.add_parser("enroll", help="Enroll an existing product checkout")
    enroll.add_argument("--target", required=True)
    enroll.add_argument("--repo", required=True)
    enroll.add_argument("--name", required=True)
    enroll.add_argument("--slug")
    enroll.add_argument("--skip-factory-bootstrap", action="store_true")
    enroll.set_defaults(handler=command_enroll)

    validate = sub.add_parser("validate", help="Validate Studio OS and standard locks")
    validate.set_defaults(handler=command_validate)

    dashboard = sub.add_parser("dashboard", help="Generate dashboard data and static UI")
    dashboard.set_defaults(handler=command_dashboard)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = args.handler(args)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Studio operation complete:", json.dumps(result, indent=2))
        return 0
    except StudioError as exc:
        print(f"studio: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("studio: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
