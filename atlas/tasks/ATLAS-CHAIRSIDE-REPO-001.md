# Atlas Task: Create or Identify Chairside Repository

## Objective

Resolve the only blocking gap in the Chairside pilot: no accessible product repository currently exists.

## Instructions

1. Search the signed-in GitHub account for an existing Chairside repository or branch under another repository.
2. If a suitable repository exists, record its exact owner/name and default branch in `products/chairside/manifest.yaml` and `status.yaml` through a pull request.
3. If none exists, create a private repository named `chairside-ios` under `pri8771`.
4. Initialize it with a README and run the existing App Factory remote initializer in `existing` or `new` mode as appropriate.
5. Add a Studio OS reference identifying `PROD-CHAIRSIDE` and `products/chairside/manifest.yaml`.
6. Do not add payment information, enable paid services, or publish the repository.

## Stop only for human

- GitHub reauthentication, passkey, or MFA
- a naming collision that requires a business choice
- a request to make the repository public
- a paid-plan gate

## Completion evidence

- Repository URL
- Default branch
- App Factory validation result
- Pull request or commit link
