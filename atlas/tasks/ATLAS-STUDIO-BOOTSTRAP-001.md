---
id: TASK-STUDIO-ATLAS-001
type: task
title: Configure GitHub repository safeguards
scope: studio
status: ready
owner: priyansh
version: 0.2
updated_at: 2026-07-20
review_at: 2026-07-27
source_of_truth_for:
  - atlas-github-bootstrap-task
classification: internal
---

# Configure GitHub Repository Safeguards and Actions

## Objective

Configure the browser-only GitHub settings for `pri8771/studio-ios` and resolve the current Actions infrastructure failure while minimizing human intervention.

## Authorized system

- GitHub repository settings for `pri8771/studio-ios`
- GitHub account Actions billing/usage page only as needed to diagnose runner assignment

## Current evidence

Multiple `Validate Studio OS` runs on pull requests create a failed job but execute zero steps and expose no job logs or artifacts. Treat this as a repository/account Actions-runner or billing/settings problem until proven otherwise—not as a code-test result.

## Steps Atlas should complete autonomously

1. Confirm `main` is the default branch and the repository remains private.
2. Confirm GitHub Actions are enabled for the repository and allowed actions include the official `actions/*` actions used by the workflow.
3. Inspect the failed `Validate Studio OS` runs and identify the exact GitHub UI message shown before job execution.
4. Check whether the account has exhausted included private-repository Actions minutes, has a zero spending limit that prevents runner assignment, has a billing hold, or has another runner-policy restriction.
5. Resolve any free/no-cost configuration issue that does not require payment or a consequential policy choice.
6. Re-run the latest `Validate Studio OS` workflow and confirm at least the checkout and Python setup steps begin.
7. Inspect repository visibility and record it; do not change visibility without human approval.
8. Open branch protection/rulesets for `main` and prepare:
   - Pull request required before merge
   - At least one approval where practical for a solo repository
   - Required status check: `validate`
   - Require branches to be up to date where available
   - Block force pushes
   - Block deletion
9. Only enable a required status check after the workflow can actually receive a runner; do not permanently lock `main` behind an impossible check.
10. Record screenshots or exact UI text as evidence.

## Human-only checkpoints

Stop only when GitHub requires:

- Reauthentication or MFA
- Payment, billing information, or a paid-plan upgrade
- Changing the repository from private to public
- An organization/account-level policy choice
- Confirmation of a setting whose consequence differs materially from this task

## Evidence required

- Repository visibility and default branch
- Actions enabled/allowed-actions status
- Exact pre-execution failure reason
- Included-minutes or billing/runner status without exposing private payment details
- Successful rerun URL or documented human-only blocker
- Ruleset summary

## Completion output

```yaml
result:
  status:
  repository: pri8771/studio-ios
  default_branch:
  visibility:
  actions_enabled:
  runner_failure_reason:
  validation_workflow:
  ruleset:
  completed: []
  unavailable: []
  human_required: []
  next_action:
```
