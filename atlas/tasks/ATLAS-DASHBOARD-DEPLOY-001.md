# Atlas Task: Deploy Private Studio OS Dashboard

## Objective

Deploy the generated `dashboard/` directory from `pri8771/studio-ios` as a private, authenticated dashboard accessible remotely.

## Preferred implementation

Cloudflare Pages protected by Cloudflare Access. Do not make the private Studio OS repository or internal dashboard data public.

## Steps

1. Create or select a Cloudflare account on the free plan.
2. Connect `pri8771/studio-ios` as a Pages project with access limited to the required repository.
3. Configure the build command:
   `python scripts/generate_dashboard.py`
4. Configure the output directory:
   `dashboard`
5. Deploy the project.
6. Configure Cloudflare Access so only Priyansh's approved identity can open it.
7. Verify unauthenticated access is denied.
8. Record the deployment URL and authentication method.

## Safety

- Do not expose the repository publicly.
- Do not add customer data, secrets, tokens, or private email content.
- Do not purchase a domain or paid plan.
- Do not modify DNS for an existing production domain without approval.

## Human-only stop conditions

- Cloudflare or GitHub reauthentication/MFA
- Selecting among existing Cloudflare organizations when ownership is ambiguous
- A request to change production DNS
- Any paid-plan requirement

## Completion evidence

- Private dashboard URL
- Successful authenticated access
- Screenshot or description of the portfolio table
- Confirmation that unauthenticated access is blocked
