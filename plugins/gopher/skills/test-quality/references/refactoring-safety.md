# Refactoring safety nets

A refactor must be protected by tests that pin the behavior it preserves. When
that protection is missing, add it first — under an explicit, approved phase.

## Characterization tests

- A characterization test records the current observable behavior of code that
  is about to be refactored, so an accidental change is caught.
- Add characterization tests only when the user has approved a safety-net phase
  before production edits. They are test-only and change no production behavior.
- Base each expected value on an independent computation or a documented
  contract, not on the code's own current output copied verbatim.

## Sequencing

1. Establish or restore a passing baseline.
2. If the behavior under refactor is unprotected, add characterization tests and
   confirm they pass against current behavior.
3. Only then does the refactor proceed, owned by `gopher:developer` or
   `gopher:refactor`; re-run the safety net after each change.

## Boundary

This skill adds and strengthens tests. It does not perform the production
refactor and does not alter behavior to satisfy a test. A production defect
surfaced while building the safety net is handed to `gopher:developer`.
