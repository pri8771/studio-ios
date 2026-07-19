---
id: DOC-JAPA-CONTEXT
type: context
title: Japa Context
scope: product
product: japa
status: active
owner: priyansh
version: 1.0
updated_at: 2026-07-19
review_at: 2026-08-19
source_of_truth_for: [compact-product-context]
classification: internal
---

# Japa Context

## Definition

Japa is a local-first iOS app for japa — the meditative repetition of a mantra
counted on a mala (108 beads). It replaces a physical bead loop with an
eyes-free digital counter. It is not a social, streak, or gamified habit app.

## Primary users

Practitioners of mantra meditation who want a private, calm, distraction-free
way to count repetitions without a physical mala.

## Core loop

Open the app straight into a live round → tap anywhere to count a bead (distinct
per-bead haptic) → reach the target and feel a distinct completion haptic and
optional tone → the round is saved to a quiet, non-gamified history.

## Signature capabilities

- Whole-screen advance; the practice surface is the home screen
- Distinct per-bead vs. completion haptics for eyes-free use
- 21 selectable visual mala styles
- Custom mantras alongside a seed set
- Interruption-safe resume of an in-progress round
- Honest, deletable history (no streaks, no chains, no nudges)
- Dynamic Type and VoiceOver support

## Principles

- Local-first and private: no network, no accounts, no third-party SDKs
- SwiftUI, XcodeGen-generated project
- Real persistence, no fake data or decorative controls
- Calm, non-coercive design (deliberately not gamified)

## Current state

v1 feature set is built and on-device validated (2026-07-18, iPhone 16 Pro Max).
App Factory registration is complete at standard 0.4.0. The automated suite is
green on simulator (53 unit + 11 UI). App Factory automated-UI-testing manifests
(`quality/ui/`) and the deterministic `UI_TEST_MODE` contract were added during
Studio OS enrollment (2026-07-19). Lifecycle state is `verified`: automated and
single-device validation done, human launch gates still open.

## Immediate milestone

Close the v1 launch gates: seed-mantra content sign-off (JAPA-6), VoiceOver user
validation (JAPA-8), and App Store Connect secrets plus a first verified signed
TestFlight upload (JAPA-9).

## Current blockers

- Seed-mantra content review unsigned (JAPA-6)
- VoiceOver user validation on device pending (JAPA-8)
- TestFlight end-to-end upload unverified; needs four App Store Connect secrets
  and one successful run (JAPA-9)

## Read next

- `manifest.yaml`
- `status.yaml`
- `../../standards/testing/IOS_AUTOMATED_UI_TESTING.md`
- Product repo canonical status: `pri8771/Japa` `docs/STATUS.md`
- App Factory: `pri8771/iOS_app_factory_rules`
