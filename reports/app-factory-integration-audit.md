# App Factory Integration Audit

## Result

The existing App Factory standard is already strongly aligned with Studio OS: both require canonical ownership, compact agent entry paths, machine-readable maps, current truth before history, explicit status, evidence, and no cross-product contamination.

## Preserve as canonical in App Factory

- one repository per product;
- `.factory/repository-map.json`, `project-context.json`, and `standard-lock.json`;
- product documentation and feature contracts;
- Apple-platform build, test, accessibility, layout, persistence, and release rules;
- reusable-library catalog and promotion workflow;
- product bootstrap and onboarding scripts;
- universal engineering definition of done.

## Canonical in Studio OS

- portfolio stages and priorities;
- product registry and graduation state;
- shared marketing, CRM, websites, domains, and service inventory;
- cross-system agent permissions and external-action approval;
- Atlas queue and human approval queue;
- cross-product dashboard and documentation health.

## Required compatibility work

1. Product standard locks must identify both Studio OS and App Factory.
2. Studio OS statuses map to App Factory implementation statuses rather than replacing them.
3. App Factory bootstrap should later add a Studio OS product reference.
4. Product import must read App Factory maps instead of scanning repositories.
5. UI testing should be added as an App Factory domain capability, with Studio OS tracking compliance only.

## Status differences

Studio OS uses operational task states such as `ready`, `in-progress`, and `completed`. App Factory uses implementation truth such as `implemented`, `partially_implemented`, and `verified`. These are different dimensions and must not be collapsed into one field.

## No rewrite needed

The correct approach is a compatibility layer and dual standard lock, not migration of App Factory content into Studio OS.
