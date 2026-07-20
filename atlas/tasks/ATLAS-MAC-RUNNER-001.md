# Atlas Task: Configure Studio macOS Runner

## Objective

Configure Priyansh's Mac as a restricted self-hosted GitHub Actions runner capable of building enrolled iOS apps and running generated Maestro smoke flows.

## Repositories

- `pri8771/studio-ios`
- `pri8771/pocket-party-court-ios`

## Required outcome

A runner with labels `self-hosted`, `macOS`, and `studio-ios` is online and the `iOS UI Smoke` workflow in Pocket Party Court can be dispatched.

## Steps

1. Open repository settings for `pri8771/pocket-party-court-ios`.
2. Navigate to Actions → Runners and add a new self-hosted macOS runner.
3. Follow GitHub's generated commands in a dedicated local directory.
4. Add custom label `studio-ios` during configuration or in runner settings.
5. Configure the runner as a dedicated, non-admin local user where practical.
6. Confirm Xcode is installed and the license has been accepted.
7. Confirm an `iPhone 16 Pro` simulator runtime exists; if not, install a currently available iOS simulator and update the workflow destination consistently.
8. Start the runner and verify it appears online.
9. Dispatch `.github/workflows/ui-smoke.yml`.
10. Record the workflow URL and result in the Atlas task issue.

## Safety

- Do not expose the runner to public repositories other than specifically approved studio repositories.
- Do not add signing certificates, App Store credentials, production secrets, or broad personal filesystem access.
- Do not change repository visibility.
- Do not enable paid services.
- Stop the runner when not actively needed until hardening is complete.

## Human-only stop conditions

Involve Priyansh only for:

- macOS administrator authentication
- GitHub reauthentication or MFA
- Xcode license acceptance requiring his confirmation
- installation requiring Apple ID authentication
- a decision to grant broader repository access
- a paid-plan or billing gate

## Completion evidence

- Runner appears online with label `studio-ios`
- Workflow run URL
- Build result
- Generated Maestro result or exact failure
- Any simulator destination adjustment made
