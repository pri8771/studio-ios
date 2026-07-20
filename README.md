# Studio iOS

Central operating system for a multi-product, AI-operated software studio.

## Local quick start

```bash
cd ~/Developer/studio-ios
git pull --ff-only
bash scripts/studio-local
```

The command validates the repository, regenerates the private portfolio dashboard and sanitized shared-site preview, starts a local server, and opens:

```text
http://127.0.0.1:8787/
```

No cloud account, Docker service, CRM, Google Workspace, or deployment is required to use the local dashboard.

Full local instructions: [`docs/LOCAL_FIRST.md`](docs/LOCAL_FIRST.md).

## What this repository controls

- Agent rules and approval boundaries
- Token-efficient documentation standards
- Product, service, agent, and automation registries
- Task, requirement, decision, risk, and conversation templates
- Multi-agent coordination state
- Repository validation and generated dashboard data
- Integration with `pri8771/iOS_app_factory_rules`
- Local shared-website preview and local workspace setup

## Start here

1. Read [`AGENTS.md`](AGENTS.md).
2. Read [`context.md`](context.md).
3. Use the relevant registry or template.
4. Make changes to canonical records only.
5. Run `bash scripts/studio-local` to validate and inspect the result.

## Current status

The local control-plane foundation is active. Chairside is registered as the definition-level pilot, Pocket Party Court is the first repository-backed engineering pilot, Japa is registered with verified simulator testing and remaining launch gates, and Document Flow is registered for local one-command creation.

Current local implementation priorities:

1. Create and inspect Document Flow locally with `scripts/studio new ... --no-remote`.
2. Fully import remaining repository-backed products.
3. Complete manifest-driven iOS UI test execution and evidence capture.
4. Improve portfolio status freshness and local reporting.
5. Keep cloud services deferred until the local workflow is proven.

## Create a new local project

```bash
scripts/studio new \
  --name "Document Flow" \
  --slug document-flow \
  --template document-ai \
  --private \
  --no-remote
```

This creates `~/Developer/document-flow`, applies the template, initializes Git, runs App Factory enrollment, and registers the product in Studio OS without creating a GitHub repository.

## Enroll an existing app

```bash
scripts/studio enroll \
  --target /path/to/product-repository \
  --repo pri8771/product-repository \
  --name "Product Name"
```

The command bootstraps App Factory registration when needed, inspects the product, creates or updates Studio OS product records, adds UI-test manifests when missing, and regenerates the dashboard. It does not claim Xcode verification unless a macOS build actually runs.

## Optional local folder setup

```bash
python3 scripts/setup_local_workspace.py --apply \
  --product "Document Flow" \
  --product "Jyot" \
  --product "Pocket Party Court" \
  --product "Japa"
```

The script only creates missing directories. It never moves, deletes, or overwrites existing files.

## Human intervention policy

Browser-dependent setup should be assigned to Atlas using files under [`atlas/tasks/`](atlas/tasks/). Atlas should continue autonomously until authentication, MFA, payment, legal acceptance, Apple signing approval, or another true human-only checkpoint is reached.

For the current local-first milestone, browser and cloud tasks are deferred and do not block the dashboard.

## Key locations

- `standards/` — shared rules
- `registry/` — compact studio indexes
- `templates/` — canonical record templates
- `scripts/` — creation, enrollment, validation, drift detection, and local generation tools
- `atlas/` — deferred browser and Mac task queue
- `products/` — product-specific context and records
- `dashboard/` — generated private portfolio view
- `website/` — sanitized public-site configuration
- `generated/local-portal/` — assembled local portal; never edit manually
