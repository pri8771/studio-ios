# Shared Studio Website

This directory defines the public, generated studio website.

## Safety model

The private Studio OS product registry is never published directly. A product appears on the public site only when `website/products.yaml` contains an approved entry with:

```yaml
published: true
```

New products default to hidden. Generated files live under `generated/public-site/` and must not contain internal status, blockers, customer data, repositories, credentials, or private strategy.

## Generate locally

```bash
python scripts/generate_public_site.py
```

Open:

```text
generated/public-site/index.html
```

## Deployment

The generated directory can be deployed to Cloudflare Pages, GitHub Pages, or another static host after the studio name/domain and public product entries are approved. The private dashboard is a separate artifact and must remain behind authentication.

## Product spin-off rule

Products begin at `/apps/<slug>/`. A dedicated product domain should redirect to that page until traffic, SEO, brand, legal, team, or operational needs justify a separate site.
