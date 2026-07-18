---
name: config
description: Bootstraps, validates, edits, and explains the `.gopher-plugin.toml` project contract that drives Gopher's quality workflows. Use to create project configuration, run `--bootstrap` or `--explain`, or inspect thresholds, tool policy, and refactoring safeguards. Route code, complexity, test, modernization, and refactor work to their canonical owners.
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
`gopher:refactor`. This skill reads and writes configuration only.

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

## Configuration states

- `ABSENT`: no file present; analysis is allowed and `--bootstrap` can create one.
- `VALID`: the effective configuration can drive workflows.
- `INVALID`: explanation and diagnosis are allowed; non-config mutations block.
- `UNSUPPORTED_VERSION`: a future schema; read-only guidance only, never rewrite.

Effective-value precedence, highest first:

1. Explicit instruction for the current session.
2. `.gopher-plugin.toml`.
3. Adopted project configuration and commands.
4. Gopher defaults (`templates/default.gopher-plugin.toml`).

This precedence selects scope, metrics, and targets. It never relaxes an
authorization or safety boundary.

## Output format

```yaml
selected_skill: gopher:config
primary_owner: gopher:config
status: COMPLETE | BLOCKED
config_mode: none | bootstrap | explain
config_status: ABSENT | VALID | INVALID | UNSUPPORTED_VERSION
authorization_gate: none | confirmation-required | blocked
handoff: gopher:<skill> | null
```

## Authorization boundaries

- `INVALID` blocks non-config mutations until the file is corrected; explanation
  and diagnosis remain allowed.
- `UNSUPPORTED_VERSION` is read-only; never auto-rewrite a future schema.
- Migrate an older supported schema only inside `--bootstrap`, with a preview
  and explicit confirmation.
- An unavailable optional tool is a limitation, not an invalid configuration,
  unless its configured mode requires it.
- Every write — create, edit, or migrate — requires a shown preview or diff and
  explicit user confirmation.

## References

- `references/schema.md` — every canonical table and key, with type, range or
  enum, default, and consuming workflow.
- `references/bootstrap.md` — the `--bootstrap` absent and present flows.
- `references/explain.md` — the `--explain` read-only output contract.
- `references/validation.md` — validation rules and the four configuration states.
- `templates/default.gopher-plugin.toml` — the canonical default written on bootstrap.
