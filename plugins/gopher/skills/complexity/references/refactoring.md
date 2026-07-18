# Complexity reduction techniques

Reduce complexity with idiomatic Go, preserving behavior. Every applied change
needs a passing baseline, focused tests, and a re-measurement.

## Idiomatic techniques

- Extract a cohesive helper to lower cyclomatic and cognitive complexity.
- Replace deep nesting with early returns and guard clauses.
- Turn a long conditional chain into a table or a small dispatch map.
- Split an oversized function along its natural seams; split an oversized file
  by responsibility.
- Reduce state carried through a function; prefer explicit parameters and useful
  zero values over hidden flags.

## Handoff boundaries

- A local, reversible reduction inside a package is handed to `gopher:developer`
  with the target unit, the intended shape, and the metric to improve.
- A change to a public contract, package boundary, or module topology is handed
  to `gopher:architecture`; complexity does not perform cross-package
  restructuring.
- Do not trade a complexity number for worse behavior, weaker error handling, or
  a broken abstraction. A reduction that harms clarity is not an improvement.
