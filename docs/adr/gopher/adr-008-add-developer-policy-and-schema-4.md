---
type: adr
id: adr:gopher:008
context: gopher
title: Add developer policy and migrate the project contract to schema 4
status: Accepted
tags: [go, plugins, developer, config, tdd, schema, migration]
deciders: [Alvadorncorp]
date: 2026-08-08
---
# ADR-008: Add developer policy and migrate the project contract to schema 4

## Context and Problem

Routine development has no project-level idiom or test-sequencing policy. The
repository also duplicated release numbers in structural tests; official
packaging validators are the authoritative version-consistency gate.

## Decision Drivers

- Safe test-first behavior by default.
- Declared-Go-version compatibility and bounded local edits.
- Opt-in, value-preserving configuration migration.
- One shared workflow across all harnesses.

## Considered Options

### Native `[developer]` policy (chosen)

Add a bounded, native `[developer]` table to the project contract. This keeps
the workflow self-contained and deterministic, while making idiom and test
sequencing policy explicit and reproducible.

### Compose external TDD and modernize workflows

Compose `gopher:developer` with external TDD and `gopher:modernize` workflows.
This reuses existing workflows, but adds plugin availability, handoff, context,
and harness dependence to the default local-development contract.

### Hard-code behavior without configuration

Always use modern idioms and TDD. This minimizes schema surface, but gives
legacy projects no controlled override and fails to express project-level
policy.

## Decision

Adopt schema version 4 with `[developer].idiom_policy = latest-compatible |
project-aligned | explicit-only` and `[developer].test_workflow = adaptive-tdd |
strict-tdd | test-after`. Defaults are `latest-compatible` and `adaptive-tdd`.
Resolve each value independently by session, file, adopted project policy, then
default. Versions 1–3 remain `MIGRATION_AVAILABLE`; only confirmed
`gopher:config --bootstrap` persists missing defaults.

Keep workflow ownership in `gopher:developer`, specialist boundaries unchanged,
and packaged agents thin. `latest-compatible` remains capped by the declared Go
version; `project-aligned` prioritizes nearby conventions; and `explicit-only`
adopts newer idioms only when requested. No policy invokes `go fix`, performs
package-wide modernization, or consumes `modernize.target_go`.

Remove copied release-number assertions and rely on official packaging
validators. Synchronize versioned catalogs to the existing `0.5.1` manifests
and repair the YAML-ambiguous codegen description without changing its meaning.

## Consequences

Positive consequences are a safe default, reproducible project policy, and
cross-harness parity through one shared developer workflow. The negative
consequences are that rollback from schema 4 requires restoring the prior
project-contract revision, and the developer result envelope becomes larger to
carry configuration, policy-source, baseline, and test evidence. Neutral
constraints are that modernization remains bounded and specialist-owned, and
migration remains opt-in with no automatic configuration write.

## Validation

The mandatory repository commands are:

- `python3 tests/validate_repo.py`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 tests/run_forward_tests.py --validate-only`

When installed, the packaging validators are:

- `python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/gopher`
- `claude plugin validate . --strict`
- `grok plugin validate plugins/gopher`

Every executed command must exit zero. Unavailable optional host CLIs are
reported as limitations and are never installed implicitly.
