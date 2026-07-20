---
id: DOC-JAPA-CONTEXT
type: context
title: Japa Context
scope: product
product: japa
status: active
owner: priyansh
version: 1.0
updated_at: 2026-07-20
review_at: 2026-08-20
source_of_truth_for: [compact-product-context]
classification: internal
---

# Japa Context

## Definition

Japa is a local-first iOS app for meditative mantra repetition counted on a mala. It replaces a physical bead loop with an eyes-free digital counter. It is not a social, streak, or gamified habit app.

## Primary users

Practitioners who want a private, calm, distraction-free way to count repetitions without a physical mala.

## Core loop

Open into a live round → tap anywhere to count a bead → receive a distinct per-bead haptic → reach the target → receive a distinct completion haptic and optional tone → save the round to quiet history.

## Signature capabilities

- Whole-screen advance
- Distinct per-bead and completion haptics
- Selectable visual mala styles
- Custom mantras and seed content
- Interruption-safe resume
- Deletable non-gamified history
- Dynamic Type and VoiceOver support

## Principles

- Local-first and private
- No accounts or backend
- No third-party runtime SDKs
- Real persistence
- Calm, non-coercive design

## Current state

The v1 feature set is built and has been validated on device. The simulator suite includes 53 unit and 11 UI tests. Studio OS and App Factory enrollment work exists in the product-repository PR and should remain separate until its CI failure is resolved. Maestro flows have been generated and manually exercised, but the product PR is not yet merged.

## Immediate milestone

Merge the product enrollment safely, close the remaining content and VoiceOver sign-offs, and complete the first verified signed TestFlight upload.

## Current blockers

- Product enrollment PR CI currently fails in the test step
- Seed-mantra content sign-off remains open
- VoiceOver user validation remains open
- TestFlight upload remains unverified

## Read next

- `manifest.yaml`
- `status.yaml`
- Product repository: `pri8771/Japa`
- App Factory: `pri8771/iOS_app_factory_rules`
