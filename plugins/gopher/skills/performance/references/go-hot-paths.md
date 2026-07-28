# Tier 2: Go Copying and Storage Patterns

Apply these only after a measurement places the cost on the path in question.
Implementation owner is `gopher:developer`.

## Growing string concatenation to `strings.Builder`

- **Preconditions:** the value is built incrementally and read once at the end.
- **Cost:** removes the repeated copying of the accumulated prefix. `Grow` is a
  capacity hint that may remove further allocations; it is not the operation
  that removes the repeated copying.
- **Failure modes:** copying a non-zero `Builder` is a misuse; retaining the
  builder across requests retains its buffer.
- **Evidence:** `B/op` and `allocs/op` on the path, or the concatenation loop in
  an allocation profile.

Sources: <https://pkg.go.dev/strings#Builder>,
<https://go.dev/src/strings/builder.go>.

## Repeated middle deletion to stable in-place filtering

- **Preconditions:** the caller tolerates mutation of the backing array, or the
  slice is owned locally.
- **Cost:** one linear pass instead of a shift per removal.
- **Failure modes:** aliases of the same backing array observe the mutation; a
  manual filter that does not clear the pointer-containing tail retains
  unreachable objects.
- **Version guard:** `slices.DeleteFunc` requires Go 1.21 or newer; automatic
  tail clearing in the standard library begins in Go 1.22. Below 1.22, clear the
  tail explicitly.
- **Evidence:** the deletion count per pass and the measured cost of the current
  loop.

Sources: <https://pkg.go.dev/slices#Delete>,
<https://go.dev/blog/generic-slice-functions>.

## `slices.Contains` in a loop to a prebuilt membership index

- **Preconditions:** enough probes to repay building the index, comparable keys,
  an acceptable memory budget, and no dependence on the slice ordering.
- **Cost:** one build pass plus expected constant-time probes, instead of a
  linear search per probe.
- **Failure modes:** too few probes to repay the build; a key type that is not
  comparable; the lost ordering that a later step relied on.
- **Evidence:** the probe count and the set size from the representative
  workload. The crossover between a slice scan and a map is workload-specific
  and is measured per case; the standard library's internal insertion-sort
  cutoff is unrelated and is not a threshold for this decision.

## Capacity hints for slices and maps

- **Preconditions:** a trustworthy upper bound on the final size exists and does
  not come from untrusted input.
- **Cost:** removes growth reallocations and their copies. It does not change
  the amortized asymptotic class of `append`.
- **Failure modes:** overestimation retains memory; an attacker-controlled size
  amplifies memory use; map capacity is an approximate hint, not a reservation.
- **Evidence:** `allocs/op` before and after on the same input.

## Formatted composite keys to comparable struct keys

- **Preconditions:** every field of the key is comparable.
- **Cost:** removes the formatting work and the delimiter collision class.
- **Failure modes:** a pointer field compares identity rather than value; a
  dynamic interface value can be non-comparable and panics at runtime; `NaN` is
  not equal to itself; a very large key raises hashing and copying cost.
- **Evidence:** the formatting call in a CPU or allocation profile.

Source: <https://go.dev/ref/spec#Comparison_operators>.
