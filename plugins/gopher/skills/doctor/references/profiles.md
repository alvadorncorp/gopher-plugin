# Readiness Profiles

A profile is the rule set a run considers. `doctor.profile` selects it, with
`standard` as the effective default. Profiles are nested: `standard` contains
every `quick` rule, and `strict` contains every `standard` rule.

| Rule id | Cost | quick | standard | strict |
|---|---|---|---|---|
| `action.scope-declared` | metadata | yes | yes | yes |
| `config.contract-valid` | parse | yes | yes | yes |
| `module.go-mod-present` | metadata | yes | yes | yes |
| `test.baseline-known` | metadata | yes | yes | yes |
| `toolchain.version-declared` | metadata | yes | yes | yes |
| `generated.output-current` | subprocess | | yes | yes |
| `module.go-sum-consistent` | subprocess | | yes | yes |
| `module.replace-policy` | parse | | yes | yes |
| `toolchain.resolvable` | subprocess | | | yes |
| `workspace.membership-consistent` | parse | | | yes |

## `quick`

Five rules, all `metadata` or `parse`, all answerable from files the project
already contains. This is the profile automatic mode runs, and it is the profile
to choose when a readiness answer is needed inside a few hundred milliseconds.

`quick` runs no subprocess rule for three reasons:

- **Bounded cost.** A file read has a cost the deadline can predict. A
  subprocess inherits the cost of a module download, a generator, or a toolchain
  resolution, and none of those fit inside a hook budget.
- **Environment independence.** A subprocess rule depends on a command being
  installed and permitted. Automatic mode has to return the same answer in a
  restricted sandbox as on a developer machine, and metadata rules do.
- **Read-only certainty.** File reads observe the project. A generator or a
  module command can populate a cache or write a lock file, and automatic mode
  keeps the project untouched.

## `standard`

Eight rules: the `quick` set plus the three that answer whether the current
module is internally consistent and its generated output is current. This is the
default for a manual `check` before an action that edits code.

The three additions all reach outside a single file read:
`module.go-sum-consistent` verifies the module graph, `generated.output-current`
compares committed artifacts against their generator, and
`module.replace-policy` reads every `replace` directive against the effective
`architecture.replace_mode`.

## `strict`

All ten rules: the `standard` set plus the two whose scope reaches beyond the
current module. `workspace.membership-consistent` compares `go.work` against
every discovered module root, and `toolchain.resolvable` checks the environment
against the declared toolchain. Choose `strict` before a release, a module
topology change, or a toolchain migration.

A `strict` run costs more wall time than `deadline_ms` usually allows. Raise
`deadline_ms` together with the profile, otherwise the run truncates and reports
the remaining rules as skipped, which yields `LIMITED`.

## How `required_rules` composes

`doctor.required_rules` adds rules to the selection. It never removes a rule the
profile already includes, so a `strict` run stays a `strict` run whatever the
list contains.

The composition has three effects:

1. **Selection.** A rule id in `required_rules` is considered even when the
   active profile excludes it. A `quick` run with
   `required_rules = ["module.go-sum-consistent"]` considers that rule, and its
   subprocess cost is charged against the same deadline.
2. **Readiness.** A run reports `READY` only when every required rule ran and
   passed. A required rule that produced a finding keeps the run at `WARN` or
   `BLOCKED` according to the blocking policy.
3. **Completeness.** A required rule that was skipped — deadline, missing
   capability, or missing authorization — makes the run `LIMITED` and appears in
   `checks_skipped` with its reason. A required rule is never reported as
   passed on the strength of not having run.

An id in `required_rules` that matches no rule in `references/rules.md` is
reported as an unknown required rule in `checks_skipped`, and the run continues
with the profile's own rules.
