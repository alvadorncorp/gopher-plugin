# Interfaces and Seams

Use a consumer-owned interface when at least one condition holds:

- two active behaviors must vary behind one consumer;
- a process/network/storage boundary needs substitution;
- an incremental migration needs a compatibility seam;
- a test cannot exercise the consumer safely through a concrete dependency.

Define the smallest behavior the consumer needs. Accept interfaces and return
concrete types. Keep provider-owned broad interfaces and speculative mock seams
as counter-signals. Record lifecycle, concurrency, error, and compatibility
semantics in addition to method signatures.

Official source: <https://go.dev/wiki/CodeReviewComments#interfaces>.
Last verified: 2026-07-14.
