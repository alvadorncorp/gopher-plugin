# `.gopher-plugin.toml` schema

Every value lives inside a canonical table. Root-level loose keys and dotted
keys (for example `complexity.cyclomatic_max = 15` at the root) are not
canonical and fail validation. The seven canonical tables are `gopher`,
`project`, `complexity`, `test-quality`, `modernize`, `refactor`, and `tools`.

Defaults are configurable targets, not universal claims about Go code. A legacy
project below a target does not automatically fail when the measured scope
maintains or improves its baseline.

## `[gopher]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `schema_version` | integer | `1` | `1` | validation, every workflow |

`schema_version` pins the contract. A newer value than this skill supports is
`UNSUPPORTED_VERSION` and is treated read-only.

## `[project]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `module_roots` | list of string | module directories, relative to root | `[]` (auto-detect) | every workflow's scope |
| `package_patterns` | list of string | `go` package patterns | `["./..."]` | every workflow's scope |

## `[complexity]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `mode` | string | `advisory` \| `required` | `advisory` | `gopher:complexity` |
| `cyclomatic_max` | integer | `> 0` | `15` | `gopher:complexity` |
| `cognitive_max` | integer | `> 0` | `20` | `gopher:complexity` |
| `maintainability_min` | integer | `0`–`100` | `20` | `gopher:complexity` |
| `function_lines_max` | integer | `> 0` | `60` | `gopher:complexity` |
| `file_lines_max` | integer | `> 0` | `500` | `gopher:complexity` |

## `[test-quality]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `coverage_target` | integer | `0`–`100` | `80` | `gopher:test-quality` |
| `coverage_regression_max` | integer | `>= 0` (percentage points) | `0` | `gopher:test-quality` |
| `mutation_mode` | string | `advisory` \| `required` | `advisory` | `gopher:test-quality` |
| `mutation_target` | integer | `0`–`100` | `75` | `gopher:test-quality` |

## `[modernize]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `target_go` | string | `declared` \| an explicit Go version | `declared` | `gopher:modernize` |
| `apply_fixes` | boolean | `true` \| `false` | `false` | `gopher:modernize` |
| `dependency_updates` | string | `none` \| `patch` \| `minor` | `none` | `gopher:modernize` |

`target_go = "declared"` keeps the project's declared Go version and prevents an
implicit upgrade; modernization may still recommend or apply changes compatible
with that version. `apply_fixes = false` makes modernization preview-only until
a run explicitly enables application. `dependency_updates` never defaults to an
unattended `latest`.

## `[refactor]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `require_passing_baseline` | boolean | `true` \| `false` | `true` | `gopher:refactor` |
| `require_behavior_tests` | boolean | `true` \| `false` | `true` | `gopher:refactor` |

## `[tools]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `complexity` | string | `auto` \| `off` \| an explicit command | `auto` | `gopher:complexity` |
| `mutation` | string | `auto` \| `off` \| an explicit command | `auto` | `gopher:test-quality` |
| `modernize` | string | `auto` \| `off` \| an explicit command | `auto` | `gopher:modernize` |

`auto` means discover and use a compatible project-adopted or already-available
tool. It never means install one; an unavailable optional tool becomes an
explicit limitation unless its mode is `required`.

## Effective-value precedence

The authoritative four-tier precedence and the rule that it never relaxes an
authorization or safety boundary live in the `## Configuration states` section
of `SKILL.md`. Resolve every effective value there, then apply the per-table
ranges, enums, and defaults above.
