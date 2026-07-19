# Studio OS Agent Rules

## Mission
This repository is the canonical operating system for the studio and all products. Optimize for correctness, minimal context, traceability, reversibility, and human control of consequential actions.

## Instruction priority
1. Current explicit human instruction
2. Approved decision record
3. This file
4. Nearest nested `AGENTS.md`
5. Task specification
6. Other current documentation
7. Agent inference

Stop and request human review only when a material conflict cannot be resolved by this order.

## Retrieval protocol
1. Read `/context.md`.
2. Identify the affected product or studio area.
3. Read that area's `context.md` and `status.yaml` when present.
4. Read the task record and only its declared context.
5. Use indexes before detailed files.
6. Prefer summaries over raw evidence.
7. Ignore `archive/`, `superseded/`, generated files, and unrelated products unless explicitly required.
8. Do not scan the entire repository without a documented reason.

## Canonical data
Store each fact once. Reference stable IDs instead of copying content.

Canonical homes:
- Product definition: product manifest/core record
- Current state: `status.yaml`
- Requirements: requirement records
- Decisions: decision records
- Work: task records/GitHub Issues
- Metrics: KPI records
- Customer data: CRM
- Secrets: approved secret store
- Code history: Git

Generated views may repeat canonical data but must never be edited manually.

## Stable IDs
Use `TYPE-PRODUCT-SHORT-NNN`, for example `REQ-CHAIR-CAPTURE-014`.

Prefixes: `PROD`, `FEAT`, `REQ`, `TASK`, `DEC`, `ASM`, `RISK`, `BUG`, `TEST`, `KPI`, `EXP`, `CAMP`, `REL`, `AUTO`, `CONV`, `VENDOR`.

Never rename an existing ID.

## Approved statuses
General: `draft`, `in-review`, `approved`, `active`, `blocked`, `needs-update`, `deprecated`, `archived`.

Tasks: `backlog`, `ready`, `in-progress`, `blocked`, `in-review`, `completed`, `cancelled`.

Requirements: `proposed`, `approved`, `implementing`, `implemented`, `verified`, `deferred`, `rejected`.

## Evidence
Do not present assumptions as facts. Confidence values: `verified`, `strong`, `moderate`, `weak`, `unvalidated`, `unknown`.

## Change rules
- Make the smallest coherent change.
- Do not rewrite unrelated files.
- Update the canonical record first.
- Record material decisions.
- Add verification evidence.
- Regenerate derived views.
- Report only the delta.

## Human approval required
Agents may prepare but must not execute without explicit human approval:
- Public publishing or sending messages
- Customer, lead, partner, or press contact
- Pricing or monetization changes
- Spending money or starting paid trials requiring payment details
- Production deployment, release, deletion, or credential changes
- Legal, privacy, security, portfolio-priority, or product-archive changes
- Permission escalation or fully autonomous external actions

## Safe autonomous work
Agents may read authorized content, draft internal documents, create tasks/branches/PRs, run tests, update non-sensitive structured records, refresh indexes, and generate internal reports.

## Quality
Never claim completion without evidence. Evidence may include tests, builds, screenshots, API responses, schema validation, preview URLs, requirement mapping, or human approval.

Prohibited: fake functionality, placeholder production data, hidden errors, success before confirmation, secrets in source, approval bypass, duplicate canonical data, unrelated sensitive reads, service-limit evasion, or silent scope changes.

## Token efficiency
- Read indexes and summaries first.
- Load only relevant standards.
- Use IDs and compact YAML.
- Keep status/context files current.
- Compress conversations to rolling summaries plus recent turns.
- Archive operational noise.
- Split oversized files.

## Completion response
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
