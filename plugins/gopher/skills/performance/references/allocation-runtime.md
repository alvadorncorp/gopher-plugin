# Tier 3: Allocation, Runtime, and Advanced Techniques

Reach this tier only when tier 1 and tier 2 are exhausted and the remaining cost
is attributed by a profile.

Implementation owner for each entry is `gopher:developer` unless the change
crosses a package boundary or a public contract, which belongs to
`gopher:architecture`. Every advanced-tier entry additionally carries the
explicit approval gate stated in `SKILL.md` under Authorization boundaries.

## Allocation evidence before compiler diagnostics

Locate the cost with an allocation profile first, then ask the compiler why.

```bash
go build -gcflags=-m=3 ./pkg 2>&1 | grep 'escapes to heap'
```

Escape analysis output explains a compiler decision. It does not prove the
escape is needless, and the result depends on the toolchain version, build tags,
and the surrounding code. Treat every line as a hypothesis to benchmark.

Reject allocation count as a universal latency predictor. Track `allocs/op` and
`B/op` next to the user-visible metric: GC cost also depends on allocation bytes
and rate, live heap size, roots, pointer density, graph shape, and scan work.

Sources: <https://go.dev/doc/gc-guide#Optimization_guide>,
<https://go.dev/src/cmd/compile/README>,
<https://go.dev/doc/gc-guide#Understanding_costs>.

## What the toolchain already does for small allocations

From Go 1.27 the compiler emits size-specialized allocation routines. Small
allocations — under 80 bytes — cost up to 30% less, allocation-heavy programs
move about 1%, and binaries grow by roughly 60 KB. The gain arrives without a
code change, so on a Go 1.27 project it is already in the baseline: an
allocation-shaving change is measured against the new numbers, not credited with
them.

`GOEXPERIMENT=nosizespecializedmalloc` restores the previous path. It exists to
bisect a suspected regression and is expected to be removed in Go 1.28, so it is
never a setting to ship (`references/version-sensitive.md`).

## Large value copies in range loops

- **Preconditions:** the element type is large and the loop body does not need
  its own copy.
- **Cost:** indexing avoids the per-iteration copy.
- **Failure modes:** `&s[i]` changes mutation and aliasing semantics and can
  itself cause an escape; the copy may already be free after inlining.
- **Evidence:** benchmark the exact loop. This is a hypothesis, never an
  automatic pointer rewrite.

## `sync.Pool`

- **Preconditions:** temporary, reusable, independently owned objects on a
  measured allocation hot path.
- **Cost:** reduces allocation volume for short-lived buffers.
- **Failure modes:** an entry can disappear at any time; values need an explicit
  reset; oversized buffers need a retention policy; a pool provides no
  correctness, ownership, resource lifecycle, or bounded caching guarantee, and
  a pooled buffer handed to `unsafe` string conversion is a use-after-free.
- **Evidence:** an allocation profile that names the object plus a before and
  after benchmark. A pool proposed without that evidence is rejected.

Source: <https://pkg.go.dev/sync#Pool>.

## Struct field ordering

- **Preconditions:** the struct is allocated in large quantities and padding is
  verifiable.
- **Cost:** less padding is verifiable with `unsafe.Sizeof`, `unsafe.Alignof`,
  and `unsafe.Offsetof`. Cache-locality and struct-of-arrays gains are
  hypotheses to benchmark.
- **Failure modes:** reordering can break cgo and `unsafe` layout assumptions,
  reflection or serialization field order, and positional composite literals.
- **Evidence:** the measured size before and after plus a realistic benchmark.

## Advanced tier: `unsafe`, `GOMEMLIMIT`, and PGO

Each entry here needs an explicit risk statement, authorization, a rollout plan,
a rollback plan, and a named owner for ongoing maintenance. Recommend one only
when the measured cost justifies the liability.

### Zero-copy conversion with `unsafe`

- **Version guard:** `unsafe.Slice` requires Go 1.17; `unsafe.String`,
  `unsafe.StringData`, and `unsafe.SliceData` require Go 1.20.
- **Preconditions:** the bytes behind a string stay immutable for the whole
  lifetime of that string, and the empty and nil cases are handled.
- **Cost:** removes one copy of the byte payload per conversion; it changes no
  asymptotic term.
- **Failure modes:** a pooled or reused buffer makes the conversion unsound;
  `unsafe` bypasses type safety and the Go compatibility promise.
- **Authorization:** explicit approval, plus a comment at the call site naming
  the invariant that keeps it sound.
- **Evidence:** an allocation profile naming the conversion plus a before and
  after benchmark on the same workload. A conversion proposed without that
  evidence is returned as a measurement plan.

Source: <https://pkg.go.dev/unsafe>.

### `GOMEMLIMIT`

- **Version guard:** Go 1.19 or newer.
- **Semantics:** a soft limit over runtime-managed memory. It is not a process
  RSS ceiling, it excludes cgo allocations, mappings, and OS-held memory, and
  the runtime may exceed it to avoid GC thrashing.
- **Preconditions:** a controlled resource reservation, 5 to 10 percent
  headroom, a canary, and a rollback path.
- **Cost:** trades GC CPU share for a bounded heap; the magnitude is
  workload-dependent and is never assumed.
- **Failure modes:** a limit below the live-heap working set drives sustained
  GC; the runtime caps GC CPU utilization at 50 percent and then exceeds the
  soft limit rather than thrashing without bound, so the observable failure is
  a large GC CPU share and degraded throughput, not a hard stop. cgo-heavy or
  mapping-heavy processes still exceed RSS expectations because the limit does
  not cover that memory.
- **Evidence:** RSS, GC CPU share, throughput, and tail latency before and
  after.

Source: <https://go.dev/doc/gc-guide#Memory_limit>.

### Profile-guided optimization

- **Version guard:** preview in Go 1.20; generally available in Go 1.21, which
  auto-detects `default.pgo` in the main package directory.
- **Preconditions:** a representative CPU profile, a named owner for refreshing
  it, reproducible builds, and a separate decision per binary and workload.
- **Cost:** trades profile collection and refresh maintenance for a
  workload-dependent gain; state an expected improvement, never a fixed range.
- **Failure modes:** a stale or unrepresentative profile silently misdirects
  inlining and devirtualization decisions.
- **Evidence:** before and after measurement on the same workload with the same
  toolchain.

Source: <https://go.dev/doc/pgo>.
