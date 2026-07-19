---
id: TASK-STUDIO-ATLAS-001
type: task
title: Configure GitHub repository safeguards
scope: studio
status: ready
owner: priyansh
version: 0.1
updated_at: 2026-07-19
review_at: 2026-07-26
source_of_truth_for:
  - atlas-github-bootstrap-task
classification: internal
---

# Configure GitHub Repository Safeguards

## Objective
Configure the browser-only GitHub settings for `pri8771/studio-ios` while minimizing human intervention.

## Authorized system
- GitHub repository settings for `pri8771/studio-ios`

## Steps Atlas should complete autonomously
1. Open the repository and confirm `main` is the default branch.
2. Confirm GitHub Actions are enabled.
3. Confirm the `Validate Studio OS` workflow appears under Actions.
4. Inspect repository visibility and record whether it is public or private; do not change visibility without human approval.
5. Open branch protection/rulesets for `main`.
6. Prepare a ruleset with:
   - Pull request required before merge
   - At least one approval
   - Required status check: `validate`
   - Require branches to be up to date where available
   - Block force pushes
   - Block deletion
7. If GitHub permits saving these settings without an unavailable paid feature or ownership decision, save them.
8. Confirm the ruleset is active and record evidence.

## Human-only checkpoints
Stop only when GitHub requires:
- Reauthentication or MFA
- A paid plan upgrade
- An organization-level policy choice
- Confirmation of a setting whose consequence differs materially from this task

## Evidence required
- Repository visibility
- Default branch
- Actions enabled status
- Workflow visibility/result
- Ruleset summary
- Any unavailable settings and why

## Completion output
```yaml
result:
  status:
  repository: pri8771/studio-ios
  default_branch:
  visibility:
  actions_enabled:
  validation_workflow:
  ruleset:
  completed: []
  unavailable: []
  human_required: []
  next_action:
```
