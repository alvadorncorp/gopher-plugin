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
  `gopher:test-quality`, `gopher:modernize`, `gopher:refactor`, or the shared
  project scope).

## Presentation

- Group values by canonical table (`gopher`, `project`, `complexity`,
  `test-quality`, `modernize`, `refactor`, `tools`).
- Mark any value that differs from its default, and name the source tier that
  overrode it.
- When the state is `INVALID` or `UNSUPPORTED_VERSION`, explain the effective
  values that still apply and state clearly which workflows are blocked.
- Name the resolved tool for each `[tools]` entry, or report the limitation when
  an `auto` tool is unavailable.

Explanation never changes state and never triggers a write; direct any edit to
`--bootstrap`.
