---
name: config
description: Bootstraps, validates, migrates, edits, and explains the `.gopher-plugin.toml` project contract that drives Gopher's quality workflows. Use to create project configuration, run `--bootstrap` or `--explain`, or inspect thresholds, tool policy, refactoring safeguards, doctor profiles, fuzz budgets, and module policy. Route code, complexity, test, modernization, and refactor work to their canonical owners.
---

# Go Project Config

## Context and ownership

Own the `.gopher-plugin.toml` project contract: bootstrap, interactive editing,
explanation, validation, defaults, and schema evolution. Primary owner:
`gopher:config`. The contract selects scope, metrics, and targets for every
Gopher quality workflow; it never performs the analysis or mutation itself.

Route routine implementation to `gopher:developer`, complexity measurement to
`gopher:complexity`, test-suite quality to `gopher:test-quality`, version and
API modernization to `gopher:modernize`, and multi-dimension refactoring to
`gopher:refactor`. Route readiness checks to `gopher:doctor`, fuzz campaigns to
`gopher:fuzz`, and module or workspace topology to `gopher:architecture`. This
skill reads and writes configuration only.

The `[agents]` table declares the project's policy for the packaged `developer`,
`architect`, and `reviewer` agents. This skill validates and explains that table
and never applies it, because each agent's binding is read by the host when it
loads the agent.

The `[developer]` table declares the `gopher:developer` workflow policy through
`idiom_policy` and `test_workflow`. This skill validates, bootstraps, migrates,
and explains those values; `gopher:developer` consumes them when it performs
work. A version `1`, `2`, or `3` file with no `[developer]` table remains
usable: these values resolve to their schema defaults until a confirmed
`--bootstrap` migration persists them.

## Modes

- No mode: detect the project root, locate the file, report its path and
  configuration state, and direct the user to `--bootstrap` or `--explain`.
  Never write in this mode.
- `--bootstrap`, file absent: first ask whether to accept all defaults or
  customize. Accept-all writes the complete canonical file; customize asks only
  the relevant interactive questions. Show the exact preview and require
  confirmation before writing. See `references/bootstrap.md`.
- `--bootstrap`, file present: load and validate, edit interactively, preserve
  unchanged content, show the exact diff, and require confirmation. Never
  overwrite merely because the file exists.
- `--explain`: stay read-only. Explain every effective value — its source,
  default, effect, accepted range or enum, and consuming workflows. See
  `references/explain.md`.

## State machine

```text
DETECT_ROOT -> LOCATE -> PARSE -> VALIDATE -> BOOTSTRAP | EXPLAIN | INFORM
```

## Configuration states and precedence

- `ABSENT`: no file present; analysis is allowed and `--bootstrap` can create one.
- `VALID`: every rule passes at the current schema version; the effective
  configuration can drive workflows.
- `MIGRATION_AVAILABLE`: a past supported schema; every rule passes, so analysis
  and explanation proceed on that contract's effective values, and only
  `--bootstrap` may migrate it.
- `INVALID`: at least one validation rule fails; explanation and diagnosis are
  allowed, and non-config mutations block.
- `UNSUPPORTED_VERSION`: a future schema; read-only guidance only, never rewrite.
  Recovery belongs to the user: update Gopher to a release that supports the
  schema, or edit the file directly to a supported version.

Effective-value precedence, highest first:

1. Explicit instruction for the current session.
2. `.gopher-plugin.toml`.
3. Adopted project configuration and commands.
4. Gopher defaults (`templates/default.gopher-plugin.toml`).

This precedence selects scope, metrics, and targets. It never relaxes an
authorization or safety boundary.

## Workflow

1. Detect the project root and locate `.gopher-plugin.toml`.
2. Parse and validate against `references/schema.md` and
   `references/validation.md`, then classify the configuration state.
3. No mode: report the path, state, and effective values, then direct the user
   to `--bootstrap` or `--explain` without writing.
4. `--bootstrap`: run the absent or present flow from `references/bootstrap.md`,
   always previewing and confirming before any write.
5. `--explain`: produce the read-only, value-by-value explanation from
   `references/explain.md`.
6. Resolve every effective value by precedence, report which tier supplied it,
   and carry `config_mode` and `config_status` in the output.

## Output format

```yaml
selected_skill: gopher:config
primary_owner: gopher:config
status: COMPLETE | BLOCKED
config_mode: none | bootstrap | explain
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
authorization_gate: none | confirmation-required | blocked
effective_values: # one entry per value: table.key, value, source tier (session | file | adopted | default)
handoff: gopher:<skill> | null
```

`effective_values` carries every resolved value in every mode. Under `--explain`,
expand each entry with the full per-value contract in `references/explain.md`.

## Authorization boundaries

- `INVALID` blocks non-config mutations until the file is corrected; explanation
  and diagnosis remain allowed.
- `UNSUPPORTED_VERSION` is read-only; never auto-rewrite a future schema.
- `MIGRATION_AVAILABLE` is migrated only inside `--bootstrap`, with the exact
  diff shown and explicit confirmation, preserving every value already set.
  Nothing is ever migrated automatically, and no other mode rewrites the file.
- An unavailable optional tool is a limitation, not an invalid configuration,
  unless its configured mode requires it.
- Every write — create, edit, or migrate — requires a shown preview or diff and
  explicit user confirmation.

## Quality checklist

- Name the source tier for every effective value reported.
- Write only after a shown preview or diff and explicit user confirmation.
- Migrate a `MIGRATION_AVAILABLE` file only inside `--bootstrap`.
- Keep `--explain` and no-mode runs read-only.
- Report an unavailable optional tool as a limitation, with its configured mode.
- Name a real `gopher:<skill>` in `handoff`, or leave it `null`.

## References

- `references/schema.md` — every canonical table and key, with type, range or
  enum, default, and consuming workflow.
- `references/bootstrap.md` — the `--bootstrap` absent and present flows.
- `references/explain.md` — the `--explain` read-only output contract.
- `references/validation.md` — validation rules and the five configuration states.
- `templates/default.gopher-plugin.toml` — the canonical default written on bootstrap.
