# Local-First Studio OS

This milestone intentionally runs without Cloudflare, Attio, Notion, Postiz, Brevo, Pipedream, Google Workspace, or a hosted database.

## Prerequisites

- macOS
- Git
- Python 3.10 or newer
- A local clone of `pri8771/studio-ios`

Docker is not required to view the Studio OS dashboard. Xcode is not required unless running iOS product builds or tests.

## First-time setup

```bash
mkdir -p ~/Developer
cd ~/Developer
git clone https://github.com/pri8771/studio-ios.git
cd studio-ios
```

For an existing clone:

```bash
cd ~/Developer/studio-ios
git pull --ff-only
```

Optionally create the agreed local folder structure:

```bash
python3 scripts/setup_local_workspace.py --apply \
  --product "Document Flow" \
  --product "Jyot" \
  --product "Pocket Party Court" \
  --product "Japa"
```

This command only creates missing directories. It does not move, delete, or overwrite existing files.

## View the dashboard locally

```bash
cd ~/Developer/studio-ios
bash scripts/studio-local
```

The command:

1. validates Studio OS records;
2. checks standard drift;
3. regenerates the private dashboard;
4. regenerates the sanitized shared-website preview;
5. assembles both into `generated/local-portal/`;
6. starts a local web server;
7. opens the portal in the default browser.

Default address:

```text
http://127.0.0.1:8787/
```

Stop it with `Ctrl+C`.

Useful options:

```bash
# Use another port
bash scripts/studio-local --port 9000

# Build files without starting a server
bash scripts/studio-local --build-only

# Do not open the browser automatically
bash scripts/studio-local --no-open

# Temporarily render despite a known validation problem
# Use only for diagnosis; do not treat the output as authoritative.
bash scripts/studio-local --skip-validation
```

## Local outputs

```text
generated/local-portal/
├── index.html
├── dashboard/
└── website/
```

These are generated views. Do not edit them manually.

Canonical sources remain:

- `registry/products.yaml`
- `products/*/status.yaml`
- `registry/services.yaml`
- `atlas/tasks/index.yaml`
- `website/products.yaml`

## Create Document Flow locally first

A local-only scaffold can be created without a GitHub repository:

```bash
cd ~/Developer/studio-ios
scripts/studio new \
  --name "Document Flow" \
  --slug document-flow \
  --template document-ai \
  --private \
  --no-remote
```

Expected local path:

```text
~/Developer/document-flow
```

The local scaffold can then be reviewed and tested before any remote repository is created.

## Validate manually

```bash
python3 scripts/validate_repo.py
python3 scripts/check_standard_drift.py
python3 scripts/generate_dashboard.py
python3 scripts/generate_public_site.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Current local-first boundaries

Available locally now:

- product registry and status records;
- Studio OS validation;
- standards drift checks;
- app enrollment and project creation CLI;
- portfolio dashboard;
- shared website preview;
- Atlas/human task queue;
- local folder bootstrap.

Deferred until later:

- cloud dashboard deployment;
- Google Workspace or email routing;
- hosted CRM;
- social publishing;
- marketing email;
- hosted automation bridges;
- unattended model/API execution.

These deferred services are tracked in `registry/services.yaml`; their absence does not block the local Studio OS milestone.
