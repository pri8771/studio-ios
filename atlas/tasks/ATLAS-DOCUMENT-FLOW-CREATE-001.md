# Atlas Task: Create and verify Document Flow

## Objective

Use the merged Studio CLI to create the private `pri8771/document-flow` repository, apply the `document-ai` template, enroll it in the App Factory and Studio OS, and return concrete verification evidence.

## Source repository

`pri8771/studio-ios`

## Preconditions

On a Mac with:

- Python 3.12+
- git
- authenticated GitHub CLI (`gh auth status`)
- curl and bash
- Docker Desktop for verification

## Commands

```bash
git clone https://github.com/pri8771/studio-ios.git
cd studio-ios

scripts/studio --dry-run new \
  --name "Document Flow" \
  --slug document-flow \
  --template document-ai \
  --private

scripts/studio new \
  --name "Document Flow" \
  --slug document-flow \
  --template document-ai \
  --private
```

If `~/Developer/document-flow` or `pri8771/document-flow` already exists, stop and inspect it. Do not delete or overwrite it.

## Required verification

From the created product repository:

```bash
docker compose config
docker compose build
```

Run all generated backend/frontend checks documented by the template. Record each as passed, failed, blocked, or not run. Do not claim extraction works; the first template establishes provider boundaries and upload/list/detail behavior only.

## Completion evidence

- Repository URL and default branch
- Product bootstrap commit
- App Factory registration version
- Studio OS registration commit or PR
- `docker compose config` result
- Docker build result
- Backend test result
- Frontend build/test result
- Exact remaining implementation blockers

## Stop only for Priyansh

- GitHub MFA, passkey, or reauthentication
- Repository naming/visibility conflict
- Docker administrator permission
- Paid-plan or billing gate
- A request to expose the repository publicly

## Do not

- Do not add real customer documents.
- Do not add OCR/LLM credentials.
- Do not connect SAP or production systems.
- Do not weaken private visibility.
- Do not report the scaffold as production-ready.
