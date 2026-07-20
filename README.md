# Studio iOS

Central operating system for a multi-product, AI-operated software studio.

## What this repository controls

- Agent rules and approval boundaries
- Token-efficient documentation standards
- Product, service, agent, and automation registries
- Task, requirement, decision, risk, and conversation templates
- Multi-agent coordination state
- Repository validation and generated dashboard data
- Integration with `pri8771/iOS_app_factory_rules`

## Start here

1. Read [`AGENTS.md`](AGENTS.md).
2. Read [`context.md`](context.md).
3. Use the relevant registry or template.
4. Make changes to canonical records only.
5. Let GitHub Actions validate the repository.

## Current status

The governance and validation foundation is active. Chairside is registered as the definition-level pilot, Pocket Party Court is the first repository-backed engineering pilot, and the remaining portfolio is registered at an initial inventory level.

Current implementation priorities:

1. Prove one-command enrollment on real product repositories.
2. Generate Studio OS records automatically from App Factory registration.
3. Generate manifest-driven Maestro UI smoke flows.
4. Run iOS build and UI verification on a macOS runner.
5. Feed repository, validation, and test health into the dashboard.

## Enroll an app

From this repository:

```bash
python scripts/studio_enroll.py \
  --target /path/to/product-repository \
  --repo pri8771/product-repository \
  --name "Product Name" \
  --mode existing \
  --platforms ios
```

The command bootstraps App Factory registration when needed, inspects the product, creates or updates Studio OS product records, adds UI-test manifests when missing, and regenerates the dashboard. It does not claim Xcode verification unless a macOS build actually runs.

## Local-first portal

Run `bash scripts/studio-local` for a private loopback-only portal. It creates local private stores, validates records, and generates both the private dashboard and a sanitized website preview. See [`docs/LOCAL_FIRST.md`](docs/LOCAL_FIRST.md) for operating and verification details.

## Human intervention policy

Browser-dependent setup should be assigned to Atlas using files under [`atlas/tasks/`](atlas/tasks/). Atlas should continue autonomously until authentication, MFA, payment, legal acceptance, Apple signing approval, or another true human-only checkpoint is reached.

## Key locations

- `standards/` — shared rules
- `registry/` — compact studio indexes
- `templates/` — canonical record templates
- `scripts/` — enrollment, validation, drift detection, and generation tools
- `atlas/` — browser and Mac task queue
- `products/` — product-specific context and records
- `dashboard/` — generated portfolio view
- `generated/` — other derived views; never edit manually
