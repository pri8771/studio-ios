# Studio iOS

Central operating system for a multi-product, AI-operated software studio.

## What this repository controls

- Agent rules and approval boundaries
- Token-efficient documentation standards
- Product, service, agent, and automation registries
- Task, requirement, decision, risk, and conversation templates
- Multi-agent coordination state
- Repository validation and generated dashboard data

## Start here

1. Read [`AGENTS.md`](AGENTS.md).
2. Read [`context.md`](context.md).
3. Use the relevant registry or template.
4. Make changes to canonical records only.
5. Let GitHub Actions validate the repository.

## Current status

Foundation bootstrap is in progress. No product has been imported as the pilot yet.

## Human intervention policy

Browser-dependent setup should be assigned to Atlas using files under [`atlas/tasks/`](atlas/tasks/). Atlas should continue autonomously until authentication, MFA, payment, legal acceptance, or another true human-only checkpoint is reached.

## Key locations

- `standards/` — shared rules
- `registry/` — compact studio indexes
- `templates/` — canonical record templates
- `scripts/` — validation and generation tools
- `atlas/` — browser-task queue
- `products/` — product-specific context and records
- `generated/` — derived views; never edit manually
