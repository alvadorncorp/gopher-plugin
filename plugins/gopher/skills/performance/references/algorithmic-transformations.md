# Tier 1: Access Pattern and Asymptotic Cost

Change the access pattern before removing copying, and remove copying before
reaching for the runtime. Every entry states expected cost, not a guarantee.
Implementation owner for each entry is `gopher:developer` unless the change
crosses a package boundary or a public contract, which belongs to
`gopher:architecture`.

## Nested loops to hash grouping

- **Preconditions:** keys are comparable, the grouping preserves the original
  semantics, and duplicate and ordering rules are defined.
- **Cost:** expected `O(n + m + output)` time with `O(n)` extra memory. Go does
  not specify map lookup complexity, so this is an expectation, not a language
  guarantee.
- **Failure modes:** unstable output ordering, silent duplicate collapse,
  memory growth on high-cardinality keys, rehashing without a capacity hint.
- **Evidence:** the quadratic scan visible in a CPU profile plus benchmark
  growth across input sizes.

Sources: <https://go.dev/blog/maps>, <https://go.dev/ref/spec#Map_types>.

## N+1 I/O to a set-based batch

- **Preconditions:** the per-item query is the same shape for every item, and
  ordering, per-parent limits, snapshot semantics, and error semantics are
  preserved.
- **Cost:** fewer round trips. Total work still includes the identifier list,
  the returned rows, remote execution, grouping, and the output.
- **Failure modes:** driver or database parameter limits on large sets,
  changed `NULL` and empty-set behavior, lost per-parent ordering or limits,
  a partial failure that previously affected one item now affecting the batch.
- **Evidence:** the request count and payload size at the boundary, plus a CPU
  profile that excludes local computation as the dominant cost.

Chunk large sets or change the query shape rather than growing one parameter
list without bound.

Sources:
<https://docs.sqlc.dev/en/stable/howto/select.html#passing-a-slice-as-a-parameter-to-a-query>,
<https://www.postgresql.org/docs/current/functions-comparisons.html#FUNCTIONS-COMPARISONS-ANY-SOME>,
<https://pkg.go.dev/github.com/jackc/pgx/v5#Batch>.

## Repeated range aggregation to prefix sums

- **Preconditions:** ordering is stable, the aggregate is invertible, and reads
  dominate writes.
- **Cost:** `O(n)` build and `O(n)` memory, then `O(1)` per additive range
  query. An update is `O(n)`.
- **Failure modes:** integer overflow, floating-point error accumulation, a
  stale table after a mutation.
- **Alternatives:** a running total for a single pass; a Fenwick or segment tree
  when updates are frequent.
- **Evidence:** the query-to-update ratio in the workload plus the measured cost
  of the current repeated scan.

## Full sort to a bounded top-k heap

- **Preconditions:** only the top `k` items are needed and the comparator is a
  strict weak ordering with defined tie behavior.
- **Cost:** `O(n log k)` time and `O(k)` memory; sorted output adds
  `O(k log k)`.
- **Failure modes:** undefined tie order surfacing as flaky output, a `k` close
  to `n` where a plain sort is simpler and no slower.
- **Evidence:** the sort dominating a CPU profile plus the observed `k` and `n`.

Source: <https://go.dev/src/container/heap/heap.go>.

## Linear scan to binary search

- **Preconditions:** the slice is sorted under exactly the comparator the search
  uses, and it stays sorted across updates.
- **Cost:** `O(log n)` per lookup, plus the `O(n log n)` sort and the cost of
  keeping the order on every update.
- **Failure modes:** a comparator that disagrees with the sort order returns a
  wrong answer silently; a single lookup rarely repays the sort.
- **Version guard:** `slices.BinarySearchFunc` requires Go 1.21 or newer.
- **Evidence:** the lookup count per sort, measured over the representative
  workload.

Source: <https://go.dev/src/slices/sort.go>.

## Nested membership to sort plus two pointers

- **Preconditions:** both inputs can be sorted or already are, and duplicate and
  interval endpoint semantics are defined.
- **Cost:** linear after sorting for intersection or merge. Emitting every
  overlapping pair can still be quadratic in the output.
- **Failure modes:** in-place sorting mutates a caller's slice; duplicates
  change the pair count; half-open and closed intervals give different answers.
- **Evidence:** the input sizes, the expected output size, and whether the
  inputs arrive sorted.

## Sparse set to a dense bitset

- **Preconditions:** identifiers are dense, stable integers with a known upper
  bound.
- **Cost:** membership is one indexed mask operation; set-wide operations cost
  `O(U/64)` where `U` is the identifier universe.
- **Failure modes:** sparse identifiers waste memory proportional to the
  universe; a string-to-identifier map keeps the hashing cost it was meant to
  remove; persisted identifiers need versioning; concurrent mutation needs
  synchronization, which is a `gopher:concurrency` question.
- **Evidence:** identifier density and the measured cost of the current
  representation. Do not claim an order-of-magnitude gain without a measurement.
