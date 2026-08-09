---
name: codegen
description: "Inventories Go generators, records provenance, reproduces generation in a temporary location, and classifies checked-in output as fresh, stale, or nondeterministic before verifying the artifacts. Use for `go generate`, a file carrying a `DO NOT EDIT` header, or mocks, protobuf, sqlc, and stringer output: to check whether generated Go code is current and reproducible, to regenerate on request, or to adopt an ad hoc generator. Route generator implementation to `gopher:developer` and generated-contract changes to `gopher:architecture`."
---

# Go Code Generation

## Context and ownership

Own the lifecycle and trustworthiness of generated Go code: which generators a
project declares, what provenance each artifact carries, whether the checked-in
output still reproduces from its inputs, and whether the artifacts verify.
Primary owner: `gopher:codegen`. Read the analysis scope from `gopher:config`
(`[project].module_roots`, `[project].package_patterns`) and carry its contract
state as `config_status`. Declared commands and generator pins come from the
project surfaces in `references/inventory.md`: `//go:generate` directives,
Makefile targets, registry configs, the `tool` directive in `go.mod`, and
`tools.go`.

Keep the split sharp: writing the generator's own Go code is `gopher:developer`;
deciding whether the checked-in output still matches its inputs is
`gopher:codegen`. A change to a generated contract — an exported API, a wire
schema, a persisted shape — belongs to `gopher:architecture`, and `gopher:doctor`
reports a stale artifact as a readiness finding and hands the work here.

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `check` | Default. Confirm that the checked-in output is current and reproducible. Read-only against the working tree. | A terminal state is recorded with its comparison evidence and handoffs. |
| `generate` | Regeneration is requested and this mode is explicitly selected. | Declared commands have run, the artifacts verify, and the resulting diff is reported. |
| `adopt` | An ad hoc or undeclared generator enters the project contract. | The pin, command, header, and owner are approved and recorded, or the adoption plan is reported with the gate still closed. |

## State machine

```text
INVENTORY -> PROVENANCE -> REPRODUCE -> COMPARE -> CLASSIFY -> VERIFY -> REPORT
```

Terminal states:

- `FRESH`: two runs from identical inputs agree with each other and with the
  checked-in output, and the verified artifacts pass their gates.
- `STALE`: the runs agree with each other, at least one input hash moved, and the
  reproduced output differs from the checked-in output. Generation is
  deterministic and the inputs moved, so regeneration produces one known,
  reviewable result. An intentional local change — the runs agree, every input
  hash is unchanged, and the artifact still differs — is reported as `STALE`
  too, with the unchanged input hashes and the hand-edit finding recorded in
  `comparison_evidence`.
- `NONDETERMINISTIC`: two runs from identical inputs disagree. The generator is
  unstable, so staleness stays undecidable until determinism is restored.
- `BLOCKED`: a missing pin, declared command, input, or authorization keeps
  reproduction from establishing any state above.

## Workflow

1. Inventory generation: `go:generate` directives, build tags, the `tool`
   directive, `tools.go`, Makefiles, and registries (`references/inventory.md`).
2. Record provenance per artifact: generator identity, pinned version, exact
   command, input hashes, toolchain, header (`references/provenance.md`).
3. Reproduce generation in a temporary location, at least twice from identical
   inputs, with the environment controlled (`references/reproduction.md`).
4. Compare hashes and diffs, byte level first and semantic equality second.
5. Classify the result as fresh, stale, or nondeterministic output, or an
   intentional local change (`references/staleness.md`).
6. Verify that the artifacts compile, the project's own test command passes, and
   the public surface is what it claims (`references/verification.md`).
7. Report the state, the evidence, the verified artifacts, and the handoffs.

## Output format

```yaml
selected_skill: gopher:codegen
primary_owner: gopher:codegen
mode: check | generate | adopt
status: FRESH | STALE | NONDETERMINISTIC | BLOCKED
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
generators:
provenance:
comparison_evidence:
verified_artifacts:
authorization_gate: none | approval-required | blocked
handoffs:  # one entry per finding: {finding, owner: gopher:<skill>, evidence}
```

## Authorization boundaries

- `authorization_gate` is `none` in `check` and in an explicitly selected
  `generate`, `approval-required` in `adopt`, and `blocked` when a required
  authorization is withheld.
- Remediate a generated file at its input or its generator, then regenerate and
  re-verify; when the generated contract itself must change — an exported API, a
  wire schema, a persisted shape — that decision is `gopher:architecture`.
  Hand-editing the artifact is never the remediation: the edit disappears at the
  next regeneration and the artifact keeps claiming a provenance it no longer has.
- Run only the generator the project already pins, resolved through the `tool`
  directive, a `//go:build tools` import, or an explicit `go run <module>@<version>`.
  An unavailable or unpinned generator is `BLOCKED` and is reported as a
  limitation with the exact pin line the project would add; obtaining or
  installing it stays with the project's own dependency workflow, and adopting it
  runs behind the approval gate in `references/adopt.md`.
- Declared commands are the only commands that run, and a command writes into
  the working tree only in `generate`, explicitly selected. `check` reproduces
  into a temporary location and leaves the working tree untouched.
- Adoption edits project files, so it carries an approval gate; a declined
  adoption is reported as a plan (`references/adopt.md`).
- Route a generator defect to `gopher:developer` and a public-surface movement
  to `gopher:architecture`, each with its evidence.

## Quality checklist

- Base every verdict on at least two reproduction runs from identical inputs.
- Record provenance as observed: module, version, command, input hashes, toolchain.
- Keep `STALE` and `NONDETERMINISTIC` distinct; decide staleness after determinism holds.
- Treat an intentional local change as a finding remediated in the input or the generator.
- Confirm the code generation header matches its required form on every artifact.
- Report the exact commands, their exit status, and every limitation.

## References

- `references/inventory.md` — discovering declared generation and its surfaces.
- `references/provenance.md` — generator identity, pins, input hashes, and the header.
- `references/reproduction.md` — temporary reproduction, environment control, and comparison.
- `references/staleness.md` — the classification decision table and required evidence.
- `references/verification.md` — compilation, project tests, and public surface checks.
- `references/adopt.md` — bringing an ad hoc generator into the project contract.
