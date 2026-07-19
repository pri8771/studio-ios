# Agent Operating Rules

## Objective
Reduce human operational work while preserving correctness, reversibility, and human control over consequential actions.

## Default roles
- ChatGPT: cross-system coordination, synthesis, CRM/communication preparation, monitoring, decision support
- Claude: product reasoning, long-form docs, research/marketing synthesis, positioning, deep discussions
- Codex: code, tests, websites, dashboards, APIs, GitHub Actions, integrations
- Cursor/IDE agents: interactive debugging, local refinement, human-guided changes

## Task contract
Material tasks require:
```yaml
id:
title:
objective:
scope:
product:
assigned_agent:
status:
acceptance_criteria: []
context:
  required: []
  optional: []
  prohibited: []
approval:
  required: false
verification: []
```

## Context loading
Load root rules, studio context, product context/status, task, required context, then optional files only when needed. Search indexes first. Avoid raw evidence and archives by default.

## External action levels
1. Read/prepare: autonomous
2. Internal reversible writes: allowed when assigned
3. Consequential actions: explicit human approval

Consequential includes sending, publishing, public deployment, release merges, deletion, spending, pricing, production access, public claims, legal changes, customer contact, or autonomous publishing.

## Pull requests as authorization
Agent prepares → PR opens → validation runs → human reviews → merge authorizes execution → result is logged.

PRs for execution must state affected systems, reversibility, required approval, and expected evidence.

## Verification
Use the strongest practical method: tests, build, schema checks, link checks, generated-output inspection, API response, before/after comparison, deployment health, or scheduling confirmation.

If unavailable, state exactly what remains unverified and the required check.

## Failure behavior
Preserve evidence, do not report success, avoid blind retries, classify the failure, attempt only bounded safe recovery, record unresolved failures, and escalate only when access or approval is required.

## Handoffs
Under 800 words unless necessary. Include objective, completed work, current state, files/records changed, decisions, assumptions, tests/results, unverified areas, known issues, exact next action, suggested next agent, and human input required.

## Multi-agent conversations
Define objective, deliverable, participants, turn order, schedule, max turns/duration, checkpoint, stop conditions, context, and output.

Each turn receives only objective, rolling summary, accepted decisions, open questions, recent relevant turns, and product context.

Every turn must add evidence, challenge an assumption, improve a proposal, identify risk, narrow options, convert discussion to action, or produce a decision-ready recommendation.

Pause after three no-progress turns, high repetition, deliverable completion, consequential decision, or limit reached.

## Token controls
Use compact YAML, stable IDs, summaries, deltas, bounded context, and short handoffs. Do not remove necessary evidence, acceptance criteria, or risks.

## Automation contract
Every automation defines trigger, input, systems, output, owner, approval, retry, idempotency, failure notification, disable procedure, rollback, and usage cap. Missing required configuration means disabled.

## Completion format
```yaml
result:
  status:
  summary:
  verified: []
  unverified: []
  changed: []
  created: []
  decisions_needed: []
  next_action:
```
