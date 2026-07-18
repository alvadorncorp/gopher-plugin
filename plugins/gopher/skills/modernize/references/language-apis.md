# Language and API modernization

Modernize Go source toward idioms and APIs available in the declared version,
one reviewable increment at a time.

## Scope

- Language idioms supported by the declared Go version (for example range-over
  constructs, generics where they simplify, standard-library helpers that
  replace hand-rolled code).
- Standard-library API adoption that is available at the declared version and
  preserves behavior.
- Deprecated-API replacement, when the replacement exists at the declared
  version.

## The `modernize` analysis pass

- The official `modernize` analysis pass proposes many of these rewrites. Use it
  only when it is compatible with the declared Go version.
- Its bulk apply mode changes many files at once, so preview its diagnostics,
  apply the suggested fixes incrementally, and validate after each increment.
- Record the exact tool version; a different version can propose different
  rewrites.

## Boundaries

- A change to a public API, an exported signature, or a cross-package contract
  is handed to `gopher:architecture`.
- Keep every rewrite behavior-preserving; a modernization that changes observable
  behavior is a code change for `gopher:developer`, not a modernization.
