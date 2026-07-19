# Reusable iOS UI Testing Standard

## Goal

Provide broad UI regression coverage without hand-authoring a new XCTest class for every screen or feature.

## Strategy

Use three layers:

1. **Generated contract checks** — validate accessibility identifiers, labels, reachable actions, screen manifests, and launch states.
2. **Generated Maestro flows** — create smoke, navigation, empty-state, persistence, dark-mode, and large-text flows from compact screen and journey manifests.
3. **Targeted XCUITest** — hand-author only critical, complex, security-sensitive, purchase, migration, and failure-recovery workflows.

This does not remove the need for all test design. It moves recurring test design into reusable manifests and generators.

## Required app contract

Each product must provide:

- deterministic launch arguments for test state;
- stable accessibility identifiers for interactive and important status elements;
- a screen manifest;
- a journey manifest for primary workflows;
- resettable local test data;
- fixtures for empty, one-record, many-record, long-text, error, and permission states;
- a scheme or test plan suitable for CI;
- simulator build and install commands.

## Accessibility identifier convention

`<product>.<screen>.<element>.<role>`

Examples:

- `chairside.clients.add.button`
- `chairside.quickCapture.notes.field`
- `chairside.quickCapture.saved.status`

Identifiers are API contracts. Do not derive tests from visible copy when a stable identifier is practical.

## Generated suites

### Smoke

- launch app;
- verify root screen;
- verify primary navigation destinations;
- verify no blocking system alert or crash;
- capture screenshots on failure.

### Screen contract

For every registered screen:

- required elements are visible in the specified fixture state;
- required controls are enabled or intentionally disabled;
- declared navigation targets can be entered and exited;
- loading, empty, content, and error states are reachable when declared.

### Accessibility and layout matrix

Run primary flows with:

- smallest supported phone;
- standard phone;
- largest accessibility text configured by the runner;
- dark appearance;
- reduced motion where applicable;
- representative iPad size when supported.

### Persistence

For records marked persistent:

- create or edit;
- terminate app;
- relaunch;
- assert data remains;
- delete;
- relaunch;
- assert deletion semantics.

### Exploratory crawler

A bounded crawler may inspect the accessibility tree and tap safe registered actions. It must:

- avoid destructive, purchase, external-send, permission, and account actions unless explicitly allowed;
- limit depth and repeated states;
- record screenshots and accessibility hierarchy;
- report crashes, unreachable exits, clipped required controls, and duplicate navigation states;
- never claim functional correctness solely from crawling.

## Manifest-driven generation

Screen manifests define selectors and states. Journey manifests define business intent and expected checkpoints. A generator converts them into Maestro YAML and CI matrices.

Agents should update a manifest when adding a screen or changing a primary flow. They should not write repetitive runner code.

## Tooling

- **Maestro CLI:** default black-box generated flow runner; open source, supports SwiftUI and iOS simulators.
- **XCUITest:** Apple-native targeted workflows and integration with Xcode test plans.
- **Accessibility audit:** use XCTest accessibility auditing where supported, plus manifest checks.
- **Snapshot/image comparison:** optional and limited to stable components; avoid pixel-perfect full-screen tests as the main signal.

## Completion rule

A feature is not verified merely because the generated smoke suite passes. Generated suites establish broad interface health. Feature contracts, unit/integration tests, and targeted critical-path tests establish behavior.
