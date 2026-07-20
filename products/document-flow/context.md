---
id: DOC-PROD-DOCUMENT-FLOW-CONTEXT
type: product-context
title: Document Flow Context
summary: Local document-processing foundation.
status: active
owner: priyansh
updated_at: 2026-07-20
---

# Document Flow

## Definition

Document Flow is a local foundation for receiving documents and moving them through an explicit processing-state model.

## Local implementation

- Repository: `/Users/pchordia/Documents/studio-ios/02_Products/Document_Flow/repository`
- App Factory registration: implemented locally as `.factory/project-context.json`.
- Studio linkage: `PROD-DOCUMENT-FLOW` registry and status records.
- Backend and frontend: locally verified with FastAPI, Vite, and automated API tests.
- Persistence: SQLite is locally verified for the local milestone; PostgreSQL Compose remains declared but unavailable on this Mac.
- Processing: deterministic text-fixture classification, extraction, and validation are locally verified. English PNG/JPEG OCR is locally verified with Tesseract; PDF OCR remains explicitly unavailable.

## Deferred external integration

OCR, classification, extraction, output connectors, and any external deployment are explicitly unavailable or deferred. Provider selection can require human approval.
