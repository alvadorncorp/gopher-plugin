# Correctness Lens

Review behavior, invariants, errors, edge cases, affected call sites, public
contracts, compatibility, and over-building. Trace changed inputs through
branches and outputs. Confirm error/absence/partial-result semantics and check
callers affected by signature or behavior changes.

Report only concrete failure scenarios with file:line evidence. Route local
fixes to `gopher:developer` and package/public-contract fixes to
`gopher:architecture`. Keep test-quality, security, architecture style, and
performance claims in their selected lenses unless they directly cause the
correctness failure.
