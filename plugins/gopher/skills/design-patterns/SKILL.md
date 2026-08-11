---
name: design-patterns
description: Diagnoses forces and selects, combines, rejects, or names no-pattern from a language-agnostic code/module catalog (pattern.*). Use when choosing or comparing Factory vs constructor/NewT, Strategy vs function, Builder vs config, Decorator/chain, Optional/Result vs native returns, Singleton/locator/registry suspicion, clone vs copy, snapshot/undo, interning/canonicalization, or expression/AST eval—including "should I use X", "X vs Y", or "is this pattern needed". Prefer no-pattern when direct code satisfies the forces. Hand Go implementation of a chosen shape to gopher:developer, package/public-contract work to gopher:architecture, app modular boundaries to gopher:application-architecture, goroutine/pipeline mechanics to gopher:concurrency, and measured pooling to gopher:performance. Stay here when peers hand off open pattern forces without a pattern.* ID; leave when the request is implement a named local Go API already decided.
---

# Design Patterns

## Context and ownership

Own code- and module-level pattern diagnosis. Start from the problem and forces
before naming a pattern. Keep the catalog language-agnostic and use stable
`pattern.*` identifiers so language owners can adapt or veto a selection.

Primary owner: `gopher:design-patterns`.

Receive reverse handoffs from `gopher:developer` and `gopher:architecture` when
pattern forces are open and no `pattern.*` ID is supplied. Route internal
application boundaries to `gopher:application-architecture`, Go implementation
to `gopher:developer`, Go package/public-contract decisions to
`gopher:architecture`, concurrency mechanics to `gopher:concurrency`, and
performance mechanics to `gopher:performance`.

## Progressive reference loading

Load only what the request requires:

| Situation | Load |
|---|---|
| Family unclear, anti-pattern named, or diagnostic/boundary disposition unknown | `references/diagnostics.md` first |
| Object or configuration creation | `references/construction.md` |
| Seams, wrappers, composition, dispatch | `references/composition.md` |
| Commands, events, coordination | `references/behavior.md` |
| Iteration, state, traversal, snapshot, intern, eval | `references/state-traversal.md` |
| Optional or fallible value protocols | `references/values-errors.md` |

Use dispositions from `references/diagnostics.md`:

- **full** — compare candidates on card signals and counter-signals; select only
  when forces fit.
- **diagnostic** — apply that card's evidence rules before selection; otherwise
  return `no-pattern` or the baseline with the missing evidence named.
- **boundary** — may select the concept `pattern.*` ID; set `handoff.owner` to
  the named peer and leave mechanics to that owner (`gopher:concurrency` for
  cancellation/pipeline, `gopher:performance` for pooling).

Keep unloaded family references out of context.

## Workflow

1. Capture the problem, evidence, desired outcome, and current design.
2. State forces and constraints. Classify each supporting claim as `observed`,
   `inferred`, or `unknown`. When an unknown blocks the next step, stop and
   name the exact evidence or owner decision required.
3. Describe the direct baseline without a pattern or refactor.
4. Classify the problem family and load only the matching reference row above;
   open `diagnostics.md` when the family or disposition is unclear.
5. Compare at most three candidates using signals, counter-signals, mechanics,
   liabilities, useful combinations, and validation questions from the loaded
   cards.
6. Decide `selected`, `rejected`, `combined`, or `no-pattern`. A named request
   still receives the baseline and counter-signals. Prefer `no-pattern` when the
   baseline satisfies the forces.
7. Choose output depth (compact vs full), define validation proportional to
   decision risk, and hand language or boundary mechanics to exactly one owner.

## Output format

Always emit every key in the schema below. Choose depth by decision class:

| Class | When | Depth |
|---|---|---|
| Local reversible | Baseline or selection stays inside one language-owner package envelope with no public-contract, persistence, security-boundary, or ADR effect | Compact: one-line values allowed under `candidates_and_liabilities` and `rejected_alternatives` when they only restate the baseline or a single counter-signal |
| Structural | Public-contract, multi-package, persistence, security-boundary, ADR, diagnostic selection, boundary selection, multi-candidate structural choice, or any approval-gated change | Full: multi-line evidence under every field, including liabilities and rejected alternatives |

```yaml
problem_and_evidence:
forces_and_constraints:
baseline_without_pattern_or_refactor:
candidates_and_liabilities:
decision: selected | rejected | combined | no-pattern
rejected_alternatives:
validation:
primary_owner: gopher:design-patterns
handoff:
  owner: gopher:<skill>
  pattern: pattern.<id> | none
  language_mapping: go.<id> | pending
  evidence:
  liabilities:
```

Set `handoff.pattern` to the chosen `pattern.*` ID or `none`. Set
`language_mapping` to a known `go.<id>` when the receiving Go owner already has
a mapping; otherwise `pending`. For boundary dispositions, `handoff.owner` is
the peer named on the card and `language_mapping` stays `pending` unless that
peer supplies a mapping.

## Authorization and stopping rules

Analysis and design output are read-only. Implementation starts only after a
language owner accepts the handoff. Structural, public-contract, persistence,
security-boundary, or ADR-affecting changes require evidence, alternatives, and
explicit approval before editing.

Stop without selecting a pattern when:

- an `unknown` claim blocks distinguishing the leading candidates;
- a diagnostic card's evidence rules are unmet;
- the direct baseline satisfies the forces (`no-pattern`).

When evidence cannot distinguish the leading candidates, return the direct
baseline plus the missing evidence.

### Proportional validation

| Decision class | Cheapest sufficient validation |
|---|---|
| `no-pattern` or local reversible selection | Name one observable check that would falsify the decision (focused test, compile, or caller review) |
| Structural or diagnostic selection | Card validation questions plus the receiving owner's acceptance criteria; mark approval-gated edits |
| Boundary selection | Confirm forces match the boundary card; receiving owner owns mechanic verification |

## Quality checklist

- Start from forces and include the direct baseline.
- Use only IDs listed in `references/diagnostics.md`.
- Give every candidate at least one liability and counter-signal.
- Keep language mechanics in the receiving owner.
- Prefer `no-pattern` when direct code satisfies the forces.
- Make validation observable and proportionate to the decision risk.
- Classify evidence as observed, inferred, or unknown; stop when unknowns block
  the next step.

## References

- `references/construction.md` — object/configuration creation decisions.
- `references/composition.md` — seams, wrappers, composition, and dispatch.
- `references/behavior.md` — commands, events, and coordination.
- `references/state-traversal.md` — iteration, state, traversal, snapshot, intern, and eval.
- `references/values-errors.md` — optional and fallible value protocols.
- `references/diagnostics.md` — canonical index, dispositions, and card schema.
