---
id: STUDIO-CONTEXT-001
type: context
title: Studio Working Context
scope: studio
status: active
owner: priyansh
version: 0.1
updated_at: 2026-07-19
review_at: 2026-07-26
source_of_truth_for:
  - studio-current-context
classification: internal
---

# Studio Working Context

## Definition
A centralized, AI-operated studio for creating, launching, and managing multiple software products without duplicating business infrastructure for every app.

## Operating model
- One studio, many products.
- Shared operations, PM, documentation, CRM, marketing, support, and dashboard by default.
- Product-specific separation only for security, legal needs, customer consent, production credentials, analytics properties, or proven traction.
- External services are replaceable execution endpoints; GitHub preserves durable operating truth.

## Current implementation goal
Build the minimum enforceable Studio OS foundation:
1. Agent and documentation rules
2. Compact registries and schemas
3. Validation automation
4. Multi-agent conversation framework
5. Generated dashboard data
6. External integrations only after the core records are stable

## Human operating preference
Priyansh should intervene only at explicit human-only checkpoints. Atlas may handle browser and account-configuration tasks where possible and escalate only when authentication, consent, payment, legal acceptance, or another human-only action is required.

## Current constraints
- Free-first; no paid dependency required for the base system.
- Minimize agent token usage through progressive disclosure.
- Human approval for consequential external actions.
- Avoid separate infrastructure per product until justified.
- Do not store secrets or customer data in this repository.

## Portfolio limits
- Maximum active product builds: 2
- Maximum products in launch preparation: 2
- Maximum active autonomous conversations: 5
- Maximum unreviewed turns per conversation: 8

## Immediate next milestone
Complete repository bootstrap and validate one pilot product before importing the full portfolio.

## Entry points
- Agent rules: `/AGENTS.md`
- Documentation standard: `/standards/documentation/standard.md`
- Agent execution policy: `/standards/agents/operating-rules.md`
- Product registry: `/registry/products.yaml`
- Automation registry: `/registry/automations.yaml`
- Atlas queue: `/atlas/tasks/`
