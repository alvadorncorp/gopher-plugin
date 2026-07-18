---
name: modernize
description: Modernizes Go language, APIs, modules, dependencies, and toolchain against the declared version, previewing changes before applying them. Use to upgrade Go syntax or APIs, adopt idioms, or review dependency and toolchain policy. Route public-API, module-topology, and cross-package contract changes to `gopher:architecture`.
---

# Go Modernize

## Context and ownership

Own declared-version-aware modernization of Go language and APIs, modules,
dependencies, and toolchain, always previewing before applying. Primary owner:
`gopher:modernize`. Read the effective target and policy from `gopher:config`.

Route a public-API change, a module-topology change, or a cross-package contract
migration to `gopher:architecture`. This skill modernizes within the declared
contract; it does not redraw package boundaries or public interfaces.

## State machine

```text
DETECT DECLARED VERSION -> RESOLVE TARGET -> COMPATIBILITY BASELINE -> ANALYZE -> PREVIEW -> APPLY INCREMENTS -> VERIFY
```

## Workflow

1. Detect the declared Go and toolchain versions, module and workspace
   structure, and adopted commands (`references/project-contract.md`).
2. Resolve the target from `modernize.target_go`; keep `declared` non-upgrading.
3. Establish a compatibility baseline: a passing build and test run under the
   current versions.
4. Analyze for language, API, module, and toolchain modernizations using
   `references/language-apis.md` and `references/modules-toolchain.md`.
5. Preview every change first. With `apply_fixes = false`, stop at the preview.
6. Apply increments only when authorized, one reviewable step at a time
   (`references/migration.md`), then verify against the baseline.
7. Report applied changes, previews, exact tool and target versions,
   limitations, and handoffs.

## Safeguards

- `target_go = "declared"` keeps the declared Go version; recommend or apply only
  changes compatible with it, and leave any version upgrade to a separate,
  explicitly approved decision.
- `apply_fixes = false` returns a preview only; application requires an explicit
  opt-in.
- Dependency updates follow `modernize.dependency_updates` and require an
  explicit level — `none`, `patch`, or `minor` — before any bump, and preview
  every change.
- Record the exact tool and target versions with every change.
- Require manual review for merge conflicts, generated or machine-authored
  comments, and any change that touches a contract.

## Output format

```yaml
selected_skill: gopher:modernize
primary_owner: gopher:modernize
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
config_status: ABSENT | VALID | INVALID | UNSUPPORTED_VERSION
baseline_status: passing | failing | not-run
authorization_gate: none | preview-only | approval-required | blocked
handoff: gopher:architecture | gopher:developer | null
```

## Authorization boundaries

- A public-API change, module-topology change, or cross-package contract
  migration requires `gopher:architecture` and its approval gate.
- Apply fixes only under an explicit opt-in; otherwise preview and stop.
- Keep changes inside the declared version; a version upgrade is a separate,
  explicitly approved decision.
- Use only adopted or already-available tools; report a missing tool as an
  explicit limitation.

## References

- `references/project-contract.md` — declared versions, structure, and policy semantics.
- `references/language-apis.md` — language and API modernization with the `modernize` pass.
- `references/modules-toolchain.md` — module, workspace, and dependency modernization.
- `references/migration.md` — incremental application, preview-first, versioned records.
- `references/tooling.md` — `auto` discovery and the `modernize` analysis pass.
- `references/sources.md` — version-sensitive official references and review cadence.
