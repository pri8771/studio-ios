# Local-first Studio OS

This milestone runs entirely on the Mac. It creates only private local files, binds the portal to `127.0.0.1`, and requires no cloud deployment, CRM, calendar, marketing, approval, or paid-service account.

The Studio OS checkout is the workspace root. Here it is `/Users/pchordia/Documents/studio-ios`.

## Run the portal

```bash
bash scripts/studio-local
```

The command validates records, checks standard drift, initializes `.local/`, creates safe workspace directories, generates the private dashboard and sanitized website preview, then starts the portal. Routes are `/`, `/dashboard/`, and `/website/`. Use `Ctrl-C` to stop it.

## Private stores

`scripts/setup_local_workspace.py --apply` creates `.local/README.md`, CRM contacts, marketing content, calendar events, approvals, and inbox JSON files only when absent. They are ignored by Git and intentionally empty templates, not production data.

## Document Flow

```bash
scripts/studio new --name "Document Flow" --slug document-flow --template document-ai --private --no-remote --target "$PWD/02_Products/Document_Flow/repository"
```

The generated project defines explicit unavailable provider boundaries. It does not claim OCR, extraction, persistence, or end-to-end document processing works until independently implemented and tested.

## Verification meanings

- `implemented`: code or records exist.
- `locally verified`: a named local command passed.
- `unverified`: not demonstrated locally.
- `deferred external integration`: intentionally outside this milestone.
- `human-only`: requires authentication, payment, legal acceptance, or approval.
