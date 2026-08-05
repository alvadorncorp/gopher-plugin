# Go Architecture Migration

This reference carries the `migration` mode of `gopher:architecture`. A migration
is a sequence of slices. A slice is the smallest structural change that can be
released, verified, and reverted on its own. The plan is the ordered list of
slices; the migration is complete when the last slice's verification passes and
the compatibility window closes.

## The slice record

Every slice declares five things before it starts, plus its approval status:

```text
slice: <n> <name>
entry_condition: <the verified state that must hold before this slice begins>
change: <the single structural edit, behavior held constant>
verification: <the exact commands and the result that counts as a pass>
compatibility: <what every existing consumer may keep doing while this slice is live>
rollback: <the exact revert action and the verified state it restores>
approval: granted | pending
```

A slice with an unwritten field is a plan, not a slice. Write all five, then
execute.

## The canonical sequence

1. Capture imports, public consumers, behavior, errors, and tests. This is the
   baseline every later verification compares against.
2. Add a consumer seam or a compatibility entry point, additive only.
3. Move one cohesive responsibility behind the seam without changing behavior.
4. Migrate call sites in bounded batches, one batch per slice.
5. Run package, module, architecture, and compatibility checks after each slice.
6. Remove the old path only after references reach zero, as its own slice with
   its own approval.

Steps 3 and 4 usually expand into several slices. Steps 2 and 6 stay separate:
the additive slice opens the migration window and the removal slice closes it.

## Entry-condition discipline

A slice begins only after the previous slice's verification has run and passed on
the integration branch. The entry condition names that passing state explicitly —
a green command, a merged commit, a published tag, a consumer count at zero — so
that starting is a check rather than a judgment.

- Write the entry condition as something observable now: `go test ./... passes on
  main at <commit>`, `rg '<old import path>' returns zero matches`, `module
  example.com/x/component v0.2.0 is published`.
- A slice whose entry condition is unmet stays queued. Queued work is visible,
  and the sequence keeps its meaning.
- When a verification fails, the response is to roll that slice back or to fix it
  forward within the same slice. Later slices stay queued either way, so a single
  failure has one owner and one blast radius.
- Slices that touch disjoint packages and share no entry condition may run in
  parallel. State that independence explicitly; the default assumption is
  sequential.

## Compatibility across a public contract

During a multi-slice migration the public contract stays continuously usable, so
consumers migrate on their own schedule instead of in lockstep with the plan.

- **Add before removing.** Publish the new entry point first, keep the old one
  exported and working, and let the old one delegate to the new one so a single
  implementation backs both.
- **Hold the whole contract stable**, not only signatures: exported names,
  behavior, error identity and sentinel values, zero-value semantics, option
  ordering and defaults, and serialization shape.
- **Mark the old path** with a `// Deprecated:` comment that names the
  replacement, and document the migration in the same release that adds the new
  path.
- **Cross a module path change through coexistence.** A `v2+` path is a different
  import path, so both majors can build in one program; publish the new path and
  keep the old module releasing forwarding versions for the window's duration.
- **Bound the window.** Name its end condition (usually "references reach zero"),
  its owner, and the release that closes it. An unbounded window turns the seam
  into permanent duplicate ownership.
- **Gate each slice** with the checks in `references/architecture-tests.md`, so
  the compatibility promise is machine-checked and not asserted.

Verify compatibility with the commands the project already runs — `go build
./...`, `go test ./...`, an adopted API-compatibility check, `go list -m all`
across modules — plus at least one build of a real downstream consumer where one
is available.

## What makes a rollback real

A rollback is real when it can be executed right now, by someone who is not the
author, and lands in a state that has already passed verification:

- **It is a named executable action**, not an intention: revert commit `<sha>`,
  retag `<version>`, flip `<flag>` to its previous value. The action is written
  before the slice runs.
- **It reverts one slice.** Reverting slice N leaves slices 1 through N-1 intact
  and needs nothing from slices after N.
- **It lands on a verified state.** The state it restores is the previous slice's
  passing verification, so the recovery target is already known-good.
- **Its data consequences are bounded.** Data or state written under the new path
  during the slice stays readable by the old path, or the slice sits behind a
  flag whose previous value restores the old path completely.
- **It has been exercised.** The revert ran at least once — in CI, a branch, or a
  staging environment — so the first execution happens before the incident rather
  than during it.
- **It has an owner and an expiry.** Once the removal slice publishes, recovery
  becomes a forward fix; that is exactly why the removal slice is last, separately
  approved, and taken only after references reach zero.

A rollback that would require unpublishing a released version is aspirational: a
published module version is permanent. Recovery there is a new release plus a
`retract`, which belongs in the slice record from the start.

Every slice records its approval status. Keep old and new APIs together only for
the documented migration window, and let the removal slice close it.
