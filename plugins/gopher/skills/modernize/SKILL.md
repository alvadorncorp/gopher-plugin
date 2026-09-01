---
name: modernize
description: Modernizes Go language, APIs, modules, dependencies, and toolchain against the declared version, previewing changes before applying them. Use to upgrade Go syntax or APIs, adopt idioms, or review dependency and toolchain policy. Module lifecycle, sequenced migration, and public-API or cross-package contract change belong to `gopher:architecture`.
---

# Go Modernize

## Context and ownership

Own declared-version-aware modernization of Go language and APIs, modules,
dependencies, and toolchain, always previewing before applying. Primary owner:
`gopher:modernize`. This skill keeps metadata, dependencies, and toolchain
maintenance: the declared Go and toolchain versions, the dependency version
policy, and idiomatic language and API modernization inside the current
contract. Read the effective target and policy from `gopher:config`.

Module lifecycle belongs to `gopher:architecture` and its `module-lifecycle`
mode: creating, splitting, merging, or retiring a module, `go.work` membership,
`replace` directives, and release grouping. Sequencing a structural,
module-topology, or public-contract change into slices — each with an entry
condition, a compatibility guarantee, and a rollback — belongs to
`gopher:architecture` and its `migration` mode. Public-API and cross-package
contract change belongs to `gopher:architecture` as well.

This skill sequences its own in-contract work as verified increments: the change
stays inside the declared version and the current public contract, so the
compatibility baseline, not a slice protocol, is the guard.

Concretely: bumping a dependency to a patch release is `gopher:modernize`;
splitting a package into a second module with its own version line is
`gopher:architecture`. Applying a `modernize` pass in verified increments inside
the current contract is `gopher:modernize`; sequencing a package-boundary change
into slices with per-slice rollback is `gopher:architecture`.

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
4. Analyze for language, API, module, and toolchain modernizations, using
   `go fix` for language and API modernization when the active toolchain is Go
   1.26 or newer (`references/language-apis.md`,
   `references/modules-toolchain.md`).
5. Preview every change first — `go fix -diff ./...` for language and API
   modernization. With `apply_fixes = false`, stop at the preview.
6. Apply increments only when authorized, using the bulk-then-triage loop for
   `go fix` (`references/migration.md`), then verify against the baseline.
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
- An active toolchain below Go 1.26 makes the `go fix` modernizer unavailable;
  report it as a limitation rather than substituting the legacy `go fix` tool.
- Analyzer names are a versioned surface: derive the roster from
  `go tool fix help` on the active toolchain, never from release notes or
  package documentation, and revalidate any pinned analyzer name on a toolchain
  upgrade — a withdrawn name fails the invocation.
- Removed `GODEBUG` settings pinned in `go.mod` or `//go:debug` block a
  toolchain upgrade from Go 1.27 onward; audit them before recommending the
  bump (`references/modules-toolchain.md`).
- A partial apply (some fixes applied, some remain) is
  `COMPLETE_WITH_LIMITATIONS`, never a silent `COMPLETE`; name the residue.

## Output format

```yaml
selected_skill: gopher:modernize
primary_owner: gopher:modernize
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
baseline_status: passing | failing | not-run
authorization_gate: none | preview-only | approval-required | blocked
handoff: gopher:<skill> | null
```

## Authorization boundaries

- Module lifecycle, sequenced migration, and public-API or cross-package
  contract change belong to `gopher:architecture` and its approval gate.
- A project contract at an older but supported schema version reports
  `MIGRATION_AVAILABLE`; migrating it belongs to `gopher:config --bootstrap`.
- `ABSENT`, `VALID`, and `MIGRATION_AVAILABLE` proceed on the effective values.
  `INVALID` and `UNSUPPORTED_VERSION` permit analysis and preview and block
  application; report `authorization_gate: blocked` and hand correction to
  `gopher:config`.
- A failing or unavailable baseline permits analysis and preview and blocks
  application; report `baseline_status` with `authorization_gate: blocked` and
  name the failing command.
- Apply fixes only under an explicit opt-in; otherwise preview and stop.
- Keep changes inside the declared version; a version upgrade is a separate,
  explicitly approved decision.
- Use only adopted or already-available tools; report a missing tool as an
  explicit limitation.

## References

- `references/project-contract.md` — declared versions, structure, and policy semantics.
- `references/language-apis.md` — language and API modernization with `go fix`.
- `references/modules-toolchain.md` — module, workspace, and dependency modernization.
- `references/migration.md` — incremental application, preview-first, versioned records.
- `references/tooling.md` — `auto` discovery and `go fix` commands.
- `references/sources.md` — version-sensitive official references and review cadence.
