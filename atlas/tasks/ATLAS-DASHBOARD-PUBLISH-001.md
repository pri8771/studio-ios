# Atlas Task: Publish and verify the private Studio OS dashboard

## Objective

Complete the browser/account steps that cannot be performed safely from repository code.

## Steps

1. In Cloudflare Pages, create or select a project for the `dashboard/` directory.
2. In `pri8771/studio-ios`, configure repository secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` and variable `CLOUDFLARE_PAGES_PROJECT`.
3. Trigger `Publish Studio Dashboard`.
4. Configure Cloudflare Access so only Priyansh's approved identity can reach the Pages hostname.
5. Verify from another device or private browser session that anonymous access is denied and approved login works.
6. Record the protected URL and verification date in this task without recording credentials or tokens.

## Stop only for human

- Cloudflare login, MFA, passkey, or reauthentication
- creating or approving an API token
- approving the identity/access policy
- any paid-plan prompt

## Completion evidence

- protected Pages hostname
- successful workflow run
- anonymous denial confirmed
- approved-device access confirmed
