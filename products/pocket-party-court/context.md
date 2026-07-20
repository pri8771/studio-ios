---
id: DOC-PROD-POCKET-COURT-CONTEXT
type: product-context
title: Pocket Party Court Context
scope: product
product: PROD-POCKET-COURT
status: active
owner: priyansh
version: 0.1.0
updated_at: 2026-07-19
review_at: null
source_of_truth_for: [compact-product-context]
classification: internal
---

# Pocket Party Court Context

## Definition

Pocket Party Court is an offline iOS party game where a co-located group puts silly disputes on trial, votes locally on one shared phone, and produces a dramatic shareable verdict card.

## Primary Audience

Friend groups, roommates, couples, families, and party hosts seeking a short pass-the-phone activity with no account or internet setup.

## Core Loop

Choose deck → enter players and assign roles → reveal case → run argument timer → vote → reveal verdict → share verdict card.

## Current State

A real SwiftUI and SwiftData app plays one case end to end. Starter decks, setup, reveal, timer, voting, verdict rendering, sharing, and local history exist. Tests are present on disk but are not wired into the Xcode project, so CI does not currently execute them.

## Current Milestone

Close the launch-critical gaps and establish App Factory enrollment plus generated UI smoke coverage.

## Major Blockers

- Three-player games leave no jury and fall back to a single judge vote.
- Multi-case loop, scoring, and winner finale are not implemented.
- There is no restart-safe central game state machine.
- Test files are not wired into the Xcode project.
- App icon and privacy manifest are missing.
- Automated UI manifests, deterministic fixtures, and simulator evidence are not yet present.

## Constraints

- iOS 17+, iPhone and iPad.
- SwiftUI, SwiftData, Apple frameworks only.
- No backend, login, network dependency, ads, or tracking for v1.
- v1 ships without monetization.
- Do not treat planned StoreKit stubs as implemented monetization.

## Read Next

- Repository `LAUNCH_READINESS.md` for authoritative build-to scope.
- Repository root instructions and `.factory/repository-map.json` after enrollment.
- `products/pocket-party-court/status.yaml` for current operational status.
