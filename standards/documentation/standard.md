# Documentation Standard

## Objective
Give humans and agents the smallest accurate context needed to decide, implement, verify, and revisit work.

## File roles
Every file must be one of:
1. `index` — locates records
2. `context` — compact working summary
3. `record` — canonical operational item
4. `standard` — reusable rule
5. `evidence` — detailed support
6. `generated` — derived human view
7. `archive` — inactive history

## Progressive disclosure
1. Registry/index
2. Studio or product context
3. Topic records
4. Raw evidence

Agents default to the lowest sufficient layer.

## Canonical-source rule
Maintain information once. Views and reports reference or generate from canonical records.

Canonical homes:
- Product definition: manifest/core record
- Current product truth: `status.yaml`
- Requirements: requirement records
- Decisions: decision records
- Tasks: task records/GitHub Issues
- Metrics: KPI records
- Customer relationships: CRM
- Secrets: secret manager
- History: Git

## Formats
- YAML: compact operational records
- Markdown: reasoning, synthesis, standards, handoffs, postmortems
- JSON: application/schema/generated interchange only
- CSV: tabular imports/exports only

## Required record fields
```yaml
id:
type:
title:
summary:
status:
owner:
updated_at:
```
Add only relevant optional fields: `product`, `priority`, `confidence`, `evidence`, `tags`, `links`, `dependencies`, `verification`, `review_at`.

## Narrative metadata
```yaml
---
id:
type:
title:
scope:
product:
status:
owner:
version:
updated_at:
review_at:
source_of_truth_for: []
classification: internal
---
```
Classifications: `public`, `internal`, `confidential`, `restricted`.

## Size targets
- Studio/product context: 1,500 words
- Topic summary: 1,200
- Feature spec/handoff: 800
- Weekly report: 600
- Decision: 400
- Requirement: 200
- Risk: 150

When oversized: remove duplication, replace copies with references, move evidence, split topics, update indexes.

## Product context
Every active product maintains `context.md` containing only definition, audience, problem, core loop, principles, stage, milestone, constraints, blockers, recent approved decisions, and links.

## Product status
Every active product maintains:
```yaml
product:
stage:
health:
priority:
current_milestone:
active_work: []
blockers: []
decisions_needed: []
next_action:
updated_at:
```
Current truth only; history remains in Git and records.

## Indexes
Directories with multiple records use `index.yaml` entries containing only `id`, `title`, `file`, `status`, and `summary`.

## Requirements
Must state stable ID, observable behavior, priority, status, source, acceptance criteria, verification, and dependencies. Requirements must be testable.

## Decisions
Must state context, decision, alternatives, rationale, consequences, revisit condition, and status.

## Assumptions
Must state confidence, evidence, validation method, threshold, deadline, result, and resulting decision.

## Risks
Must state probability, impact, severity, trigger, mitigation, owner, and status.

## Traceability
Support: Evidence → Requirement → Design → Component → Task → PR → Test → Release → KPI.

## Generated files
Must include `generated: true`, `generated_at`, `sources`, and `generator`. Never edit generated files manually.

## Freshness
Authoritative records require owner, update date, review date, and status. Mark `needs-update` when stale, contradicted, invalidated, or materially diverged from implementation.

## Approval test
A document is ready when scope is clear, canonical ownership is known, claims are evidenced or labeled, terminology is stable, open questions have owners, requirements are testable, references resolve, classification is set, review timing exists, and duplication is minimized.
