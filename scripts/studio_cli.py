#!/usr/bin/env python3
"""Small local-only Studio CLI; no network or remote repository operations."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
def slugify(value: str) -> str: return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8")
def document_ai(target: Path, name: str, slug: str) -> None:
    files = {
      "README.md": f"# {name}\n\nLocal Document AI foundation. Providers are intentionally unavailable; it does not perform OCR, extraction, or persistence.\n",
      "backend/requirements.txt": "fastapi>=0.110\nuvicorn>=0.27\n",
      "backend/app/main.py": "from fastapi import FastAPI, HTTPException\napp = FastAPI(title='Document Flow')\ndocuments = {}\n@app.get('/documents')\ndef list_documents(): return list(documents.values())\n@app.get('/documents/{document_id}')\ndef detail(document_id: str):\n    if document_id not in documents: raise HTTPException(404, 'Document not found')\n    return documents[document_id]\n@app.post('/documents')\ndef upload(): raise HTTPException(501, 'Local storage boundary is not implemented')\n",
      "backend/app/providers.py": "from enum import Enum\nclass ProcessingState(str, Enum):\n    uploaded='uploaded'; ocr_pending='ocr_pending'; classified='classified'; extracted='extracted'; validation_failed='validation_failed'; unavailable='unavailable'\nclass UnavailableProvider:\n    def run(self, *args, **kwargs): raise NotImplementedError('Provider is explicitly unavailable in the local foundation')\nOCRProvider = ClassificationProvider = ExtractionProvider = OutputConnector = LocalStorage = UnavailableProvider\n",
      "frontend/package.json": json.dumps({"scripts":{"build":"vite build","test":"echo 'No frontend tests implemented'"},"dependencies":{"@vitejs/plugin-react":"latest","vite":"latest","react":"latest","react-dom":"latest","typescript":"latest"}}, indent=2) + "\n",
      "frontend/index.html": "<div id=\"root\"></div><script type=\"module\" src=\"/src.tsx\"></script>\n",
      "frontend/src.tsx": "import React from 'react'; import {createRoot} from 'react-dom/client'; createRoot(document.getElementById('root')!).render(<main><h1>Document Flow</h1><p>Local processing providers are not implemented.</p></main>);\n",
      "docker-compose.yml": "services:\n  postgres:\n    image: postgres:16-alpine\n    environment:\n      POSTGRES_DB: document_flow\n      POSTGRES_USER: document_flow\n      POSTGRES_PASSWORD: local_only\n    ports: ['127.0.0.1:5432:5432']\n",
      "docs/ARCHITECTURE.md": "# Architecture\n\nFastAPI exposes document list/detail and upload boundary endpoints. Processing state is explicit. OCR, classification, extraction, validation, output, and local storage are boundaries with unavailable implementations. PostgreSQL is declared for future local persistence; no persistence claim is made.\n",
      "tests/test_placeholders.py": "import unittest\nclass BoundariesTest(unittest.TestCase):\n    def test_placeholder(self): self.assertTrue(True)\n",
      ".factory/project-context.json": json.dumps({"name":name,"slug":slug,"mode":"new","platforms":["web","api"],"localOnly":True}, indent=2) + "\n"}
    for relative, content in files.items(): write(target / relative, content)
def main() -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True); new = sub.add_parser("new")
    new.add_argument("--name",required=True); new.add_argument("--slug",required=True); new.add_argument("--template",required=True); new.add_argument("--target",type=Path,required=True); new.add_argument("--private",action="store_true"); new.add_argument("--no-remote",action="store_true"); args = parser.parse_args()
    target = args.target.expanduser().resolve()
    if args.template != "document-ai": raise SystemExit("Only the local document-ai template is available")
    if slugify(args.name) != args.slug: raise SystemExit("Name and slug do not match")
    if target.exists() and any(target.iterdir()): raise SystemExit(f"Refusing to overwrite non-empty target: {target}")
    target.mkdir(parents=True, exist_ok=True); document_ai(target,args.name,args.slug); print(f"Created local {args.name} foundation at {target}"); return 0
if __name__ == "__main__": raise SystemExit(main())
