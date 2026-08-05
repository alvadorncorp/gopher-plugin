---
name: complexity
description: Measures, ranks, and reduces Go cyclomatic and cognitive complexity, function/file size, and maintainability hotspots against configured thresholds. Use to measure complexity, find hotspots, plan reductions, or set complexity CI policy. Route local edits to `gopher:developer` and boundary or contract changes to `gopher:architecture`. Asymptotic and algorithmic cost belongs to `gopher:performance` even when the user calls it complexity.
---

# Go Complexity

## Context and ownership

Own Go complexity measurement, hotspot ranking, reduction guidance, and
complexity CI policy. Primary owner: `gopher:complexity`. Read the effective
scope and thresholds from `gopher:config` and measure the configured package
scope with a pinned analyzer and configuration.

Cyclomatic complexity, cognitive complexity, function and file size, and
maintainability thresholds stay here. Asymptotic time and space cost belongs to
`gopher:performance`. The two are different measurements and stay separate.

Hand a local, reversible reduction to `gopher:developer`. Route a boundary,
public-contract, or module-topology change to `gopher:architecture`. This skill
measures and recommends; it does not own cross-package restructuring.

## State machine

```text
LOAD CONFIG -> PASSING TEST BASELINE -> MEASURE -> RANK HOTSPOTS -> PROPOSE OR APPLY AUTHORIZED CHANGES -> RE-MEASURE
```

## Workflow

1. Load the effective configuration and resolve the package scope and thresholds
   from `gopher:config`; see `references/tooling.md` for analyzer discovery.
2. Establish a passing test baseline. A failing baseline permits measurement but
   blocks any code change until it is restored.
3. Measure the configured scope with a pinned analyzer and configuration using
   `references/metrics.md`. Record the exact command, tool name, and version.
4. Rank hotspots and report the concentration of complexity using
   `references/hotspots.md`.
5. Propose reductions from `references/refactoring.md`; apply only authorized,
   local, reversible changes and hand off anything cross-package.
6. Re-measure with the same command and tool version, then report before/after
   values, skipped work, limitations, and handoffs.

## Metrics

- Cyclomatic and cognitive complexity where the analyzer supports them, function
  and file size, and maintainability signals.
- A threshold violation (a value past a configured maximum or minimum) is
  distinct from a baseline regression (a value that worsened versus the prior
  measurement). Report the two separately.
- A legacy project below a target passes the change gate when the measured scope
  maintains or improves its baseline; report the remaining threshold violations
  separately.
- Compare only like-for-like: the same analyzer, configuration, command, and
  tool version before and after. See `references/metrics.md`.

## Output format

```yaml
selected_skill: gopher:complexity
primary_owner: gopher:complexity
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
baseline_status: passing | failing | not-run
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
```

## Authorization boundaries

- A failing test baseline permits analysis but blocks code refactoring until the
  baseline is restored.
- Local, reversible reductions may be handed to `gopher:developer`.
- Boundary, public-contract, module, or ADR-affecting changes retain
  `gopher:architecture` and its approval gate.
- An unavailable analyzer is an explicit limitation, not a silent skip, unless
  `complexity.mode` is configured as `required`, which blocks the dimension.
- Use only an adopted or already-available analyzer; report a missing tool as an
  explicit limitation.
- Route a configuration contract that blocks work or invites migration to
  `gopher:config`, which owns every configuration state and the only migration
  path.

## References

- `references/metrics.md` — metric definitions and violation-versus-regression rules.
- `references/hotspots.md` — hotspot ranking and complexity concentration.
- `references/refactoring.md` — idiomatic Go reduction techniques and handoffs.
- `references/tooling.md` — `auto` analyzer discovery and pinning for comparison.
- `references/trends-ci.md` — trend tracking and complexity CI policy.
- `references/sources.md` — version-sensitive official references and review cadence.
