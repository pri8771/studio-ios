---
id: DOC-DOCUMENT-FLOW-CONTEXT
type: context
title: Document Flow Context
scope: product
product: document-flow
status: active
owner: priyansh
version: 1.0
updated_at: 2026-07-20
review_at: 2026-08-20
source_of_truth_for: [compact-product-context]
classification: internal
---

# Document Flow Context

## Definition

Document Flow is a configurable platform that receives business documents, classifies them, extracts fields and repeating tables, validates the results, routes uncertain data for human review, and exports approved structured data or triggers downstream actions.

## Primary users

Operations, finance, customer-service, supply-chain, shared-services, and small-business teams that currently convert PDFs, scans, images, spreadsheets, or forms into system data manually.

## Core loop

Receive document → preprocess and OCR → classify document type → extract against a configurable schema → validate against rules and reference data → review uncertain results → approve or correct → export or trigger an integration.

## Non-negotiable boundaries

- Do not hardcode the product around purchase orders, SAP, ABBYY, email intake, or one provider.
- OCR, classification, extraction, validation, storage, and output must use replaceable interfaces.
- Uncertain results require explicit review policy.
- Failed processing must not appear successful.
- Document contents and prompts must not leak into ordinary logs.

## Initial proof document types

1. Purchase order
2. Invoice
3. Generic application form

Adding invoice or application-form support should primarily require configuration, validation rules, and fixtures—not changes to the core pipeline.

## MVP boundary

- Manual PDF/image upload
- Configurable scalar fields and one repeating table
- OCR and extraction provider boundaries
- Confidence and evidence
- Human correction and approval
- JSON, CSV, and webhook-oriented output contracts
- Processing history and explicit failure states

Deferred: authentication, billing, email ingestion, SAP, multi-tenant public SaaS, complex workflow builder, and mobile apps.

## Immediate milestone

Create the private `pri8771/document-flow` repository with the `document-ai` Studio CLI template, complete App Factory and Studio OS linkage, and verify the generated local foundation.

## Current blockers

- Repository has not been created.
- `studio new` has not yet been executed on an authenticated Mac.
- The generated template has not yet passed Docker and application verification.

## Read next

- `manifest.yaml`
- `status.yaml`
- `../../atlas/tasks/ATLAS-DOCUMENT-FLOW-CREATE-001.md`
