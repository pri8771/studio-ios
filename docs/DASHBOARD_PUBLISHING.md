# Dashboard publishing

Studio OS generates a read-only dashboard from canonical repository records.

## Automatic generation

`publish-dashboard.yml` runs when portfolio records, product statuses, Atlas tasks, or dashboard code changes. It also runs daily and can be triggered manually. Every successful run uploads the complete `dashboard/` directory as a 30-day artifact.

## Private Cloudflare Pages deployment

Deployment activates only after configuration:

Repository secrets:
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

Repository variable:
- `CLOUDFLARE_PAGES_PROJECT`

Cloudflare Access must protect the Pages hostname before it is considered private.

## Human verification gate

After the first deployment, test from another device or private browser session:
1. the URL resolves;
2. unauthenticated visitors are denied;
3. the approved identity can sign in;
4. the dashboard shows a generated timestamp and freshness warning.

Never place secrets, credentials, or customer data in dashboard records.
