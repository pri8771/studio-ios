# Atlas Task: Close Japa v1 launch gates

## Objective

Complete the browser-, Apple-account-, and human-validation steps that remain before Japa (`PROD-JAPA`) can ship its first TestFlight build.

## Repositories

- Product: `pri8771/Japa`
- Studio record: `pri8771/studio-ios/products/japa/`

## Preconditions

Do not proceed to TestFlight until the product enrollment PR is merged and its CI is green.

## Steps

1. Confirm the enrollment branch is merged and the main-branch simulator build and tests pass.
2. In the Japa repository Actions secrets, configure names only—never commit values:
   - `ASC_KEY_ID`
   - `ASC_ISSUER_ID`
   - `ASC_KEY_CONTENT`
   - `DEVELOPMENT_TEAM`
3. Trigger the TestFlight workflow and record the build/upload result under the product repository's quality evidence.
4. Obtain accountable human sign-off for the seed-mantra content review.
5. Run the primary flow on a physical device with VoiceOver and record evidence.
6. Confirm the App Store marketing icon is opaque RGB on the final merged branch.

## Completion evidence

- Main-branch CI URL
- TestFlight build number or upload confirmation
- Signed content-review commit
- VoiceOver evidence file
- Final icon verification result

## Stop only for Priyansh

- Apple ID, passkey, MFA, or reauthentication
- Apple signing/team approval
- Legal or spiritual-content acceptance requiring Priyansh personally
- Payment or paid-plan gate
- A public/private repository decision

## Do not

- Do not expose secret values.
- Do not change signing architecture without an approved decision record.
- Do not rewrite the app or rename established accessibility identifiers during launch setup.
