# `--explain` flow

`--explain` is read-only. It never writes or edits the file. It reports the
effective configuration and how each value was resolved.

## Output contract

For every effective value, report:

- Name: the `table.key` path.
- Value: the effective value in use.
- Source: the precedence tier that supplied it — session instruction,
  `.gopher-plugin.toml`, adopted project configuration, or Gopher default.
- Default: the Gopher default from `templates/default.gopher-plugin.toml`.
- Effect: what the value changes in the consuming workflow.
- Accepted range or enum: from `references/schema.md`.
- Consumed by: the owning workflow (`gopher:complexity`,
  `gopher:test-quality`, `gopher:modernize`, `gopher:refactor`, `gopher:doctor`,
  `gopher:fuzz`, `gopher:architecture`, or the shared project scope).

## Presentation

- Group values by canonical table (`gopher`, `project`, `complexity`,
  `test-quality`, `modernize`, `refactor`, `tools`, `doctor`, `fuzz`,
  `architecture`).
- Mark any value that differs from its default, and name the source tier that
  overrode it.
- When the state is `INVALID` or `UNSUPPORTED_VERSION`, explain the effective
  values that still apply and state clearly which workflows are blocked.

## `MIGRATION_AVAILABLE`

When the state is `MIGRATION_AVAILABLE`, explain the effective values of the
older contract as usual and add:

- The `schema_version` found in the file and the version this skill supports.
- The values that would change under migration: the version bump itself, the
  tables and keys the current schema adds, and the default each one would take.
- The fact that every value the file already sets is preserved by migration.
- The fact that `--explain` writes nothing. Migration happens only inside
  `--bootstrap`, with a shown diff and explicit confirmation.
- Name the resolved tool for each `[tools]` entry, or report the limitation when
  an `auto` tool is unavailable.

Explanation never changes state and never triggers a write; direct any edit to
`--bootstrap`.
