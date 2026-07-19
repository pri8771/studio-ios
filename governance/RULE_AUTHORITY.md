# Rule Authority and Inheritance

## Authority order

1. Current explicit human instruction
2. Approved Studio OS governance and decisions
3. Registered domain standard, such as iOS App Factory
4. Product repository rules
5. Task instructions
6. Agent inference

Lower layers may add stricter rules but may not weaken security, approval, evidence, privacy, or quality requirements from higher layers.

## Repository ownership

- `pri8771/studio-ios`: portfolio, operations, shared services, agent governance, approvals, marketing, CRM references, dashboards, and domain-standard registration.
- `pri8771/iOS_app_factory_rules`: iOS/macOS product engineering, repository bootstrap, documentation, quality, reuse, testing, build, and release standards.
- Product repositories: product code, product requirements, current architecture, tests, releases, evidence, and product-specific decisions.

## Conflict handling

When rules conflict, an agent must:

1. identify both rules;
2. apply the higher-authority rule;
3. avoid silently rewriting either source;
4. record a proposed compatibility change when the conflict is durable;
5. request human review only when the conflict changes scope, risk, cost, legal posture, or external behavior.

## Versioning

Every product repository must pin both Studio OS and domain-standard versions. A newer central version creates an upgrade proposal; it does not silently change product behavior.

## Duplication rule

Studio OS may summarize domain-standard requirements but must link to the canonical domain document. Product repositories may contain compact adapters and locks, not copied central rulebooks.
