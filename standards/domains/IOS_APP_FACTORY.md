# iOS App Factory Domain Standard

## Registration

- ID: `STD-IOS-APP-FACTORY`
- Canonical repository: `pri8771/iOS_app_factory_rules`
- Current observed version: `0.4.0`
- Scope: iOS, iPadOS, macOS, and related product engineering
- Studio owner: Priyansh

## Canonical responsibilities

The App Factory owns product-repository structure, agent entrypoints, Swift and Apple-platform engineering standards, quality rules, feature contracts, reusable-library discovery, build/test expectations, onboarding, and release verification.

Studio OS owns portfolio selection, priorities, shared business operations, agent permissions, external actions, dashboards, and registration of products and standards.

## Required product connection

Every registered Apple-platform product must identify:

- Studio OS product ID and manifest path;
- App Factory version and commit lock;
- product repository and default branch;
- project type (`new` or `existing`);
- compact repository map and agent entrypoint;
- build and test commands;
- current verification state.

## Read path

Agents entering a product repository follow the App Factory path:

`AGENTS.md → .factory/repository-map.json → .factory/project-context.json → .factory/standard-lock.json → docs/README.md → task-relevant records`

They load Studio OS only for portfolio, operational, approval, or cross-product questions.
