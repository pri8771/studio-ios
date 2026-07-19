---
id: DOC-CHAIRSIDE-CONTEXT
type: context
title: Chairside Context
scope: product
product: chairside
status: active
owner: priyansh
version: 1.0
updated_at: 2026-07-19
review_at: 2026-08-19
source_of_truth_for: [compact-product-context]
classification: internal
---

# Chairside Context

## Definition

Chairside is a local-first client-memory and session-continuity app for solo service professionals. It is not a booking, payment, or marketplace product.

## Primary users

Independent hairstylists, tattoo artists, estheticians, massage therapists, personal trainers, nail technicians, and private instructors.

## Core loop

Review client brief → conduct session → capture notes, photos, formulas, preferences, and care flags → generate aftercare → use the accumulated memory before the next visit.

## Signature capabilities

- Client profiles and session history
- Quick Capture with autosave and Needs Filing inbox
- Before/after/progress photo timelines
- Formulas, preferences, contraindications, and boundaries
- Pre-appointment “Last time we did…” client brief
- Branded aftercare export

## Principles

- Local-first and private
- SwiftUI and SwiftData
- Fast capture with real persistence
- Stable identifiers and versioned models for future sync
- Accessible, warm, professional design
- No fake functionality or decorative controls

## Current state

Product definition and architecture direction are established. A connected implementation repository has not been identified in the accessible GitHub inventory, so implementation verification is pending.

## Immediate milestone

Create or identify the product repository, bootstrap it with App Factory 0.4.0, and implement the core client/session/Quick Capture vertical slice with generated UI-test manifests.

## Current blockers

- Product repository not registered
- No build evidence available
- No automated UI contract implemented

## Read next

- `manifest.yaml`
- `status.yaml`
- `../../standards/testing/IOS_AUTOMATED_UI_TESTING.md`
- App Factory: `pri8771/iOS_app_factory_rules`
