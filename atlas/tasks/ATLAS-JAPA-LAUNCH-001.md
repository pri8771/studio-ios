# Atlas Task: Close Japa v1 launch gates (secrets, sign-offs, Maestro run)

## Objective

Complete the human-only and Mac/tooling-only steps that remain before Japa
(`PROD-JAPA`) can ship a first TestFlight build. All code, docs, App Factory
registration, and automated tests are already done and green; these are the
steps an autonomous agent cannot safely perform.

## Exact repository

`pri8771/Japa` (product repo). Studio OS record: `products/japa/`.

## Steps

1. **App Store Connect secrets (JAPA-9).** In `pri8771/Japa` repository settings
   → Secrets and variables → Actions, add the four secrets the TestFlight
   workflow requires: `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_CONTENT` (base64 of
   the AuthKey_XXXX.p8), `DEVELOPMENT_TEAM`. Do not commit any of these to source.
2. **First signed TestFlight run (JAPA-9).** Trigger `release-testflight.yml`
   (push a `vX.Y.Z` tag or run it manually) and confirm the build reaches
   TestFlight. Record the result under `pri8771/Japa` `quality/evidence/` and flip
   the end-to-end row in `docs/DEPLOYMENT.md` to `verified`.
3. **Seed-mantra content sign-off (JAPA-6).** Have the accountable human review
   and sign `docs/CONTENT_REVIEW.md` for the seed mantras (spiritual-content
   accuracy). App Store submission is blocked until this is signed.
4. **VoiceOver validation (JAPA-8).** Run the primary flow on a physical device
   with VoiceOver and record evidence. Dynamic Type is already implemented and
   smoke-tested; this is the assistive-tech user validation only.
5. **Maestro simulator run (UI testing).** DONE 2026-07-19 — 4/4 flows passed on
   Maestro 2.6.1 against an iPhone 17 Pro simulator (evidence:
   `pri8771/Japa` `quality/evidence/2026-07-19-maestro-ui-flows.md`; executable
   copies in `quality/ui/runnable/`). Remaining upstream improvement: have the
   App Factory generator emit `launchApp: arguments:` and teach the app to read
   the `UI_*` flags from launch arguments (Maestro-settable) plus a test-mode
   intro skip, so the raw generated flows run without the hand-added intro step.
6. **Fix the App Store marketing icon.** The 1024×1024 app icon has an alpha
   channel; flatten to opaque RGB before submission (App Store Connect rejects
   marketing icons with transparency).

## Completion evidence

- Links to the configured secrets (names only, never values)
- TestFlight build number / upload confirmation
- Signed `CONTENT_REVIEW.md` commit
- VoiceOver evidence file under `quality/evidence/`
- Maestro run log / result
- Commit flattening the app icon

## Stop only for human

- Apple ID / App Store Connect authentication, passkey, or MFA
- Apple identity, signing, or team approval
- Any payment or paid-plan gate
- Legal or content acceptance that requires Priyansh personally
- A decision to make any repository public

## What not to change

- Do not modify `project.yml` signing settings (signing is injected at archive
  time by design — DEC-005).
- Do not rewrite app source or the App Factory documents.
- Do not rename existing accessibility identifiers (the XCUITest suite depends on
  them; the convention-alignment follow-up is tracked separately).
