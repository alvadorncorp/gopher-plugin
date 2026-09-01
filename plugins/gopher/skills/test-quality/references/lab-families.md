# Canonical Lab Families

Twelve families, and no others, are canonical for the `quality-lab` mode. Each
entry names the risk it falsifies, the oracle it needs, the seam it needs, its
cost, its Go tooling, and what a passing result does and does not prove. Standard
library first; a third-party tool appears only when the project has already
adopted it.

Select with the ladder in `references/quality-lab.md`. Cost is relative effort to
build and to run, not wall-clock alone: `low`, `medium`, `high`, `highest`.

| Family | Risk it falsifies | Cost |
|---|---|---|
| `deterministic-concurrency` | timing-dependent behavior is correct at every ordering the design allows | medium |
| `integration` | the components agree once really wired together | high |
| `contract` | both sides of an interface still agree | medium |
| `hermetic` | the result depends only on the code and its declared inputs | low |
| `flake` | this suite's failures and passes are real signal | low (wall-clock grows with `-count`) |
| `race-leak` | shared access is synchronized and goroutines end with their work | low |
| `golden` | serialized output is stable and intentional | low |
| `property` | an invariant holds across the input domain, not only the chosen examples | medium |
| `metamorphic` | the relation between two related inputs holds when no expected output exists | medium |
| `differential` | this implementation agrees with a trusted reference | medium |
| `model-state` | a stateful component matches its specification across operation sequences | high |
| `mutation` | the suite would actually fail if the code were wrong | highest |

## `deterministic-concurrency`

- **Oracle**: the ordering or admission invariant stated in the contract and
  asserted under controlled time, independent of what the code reports.
- **Seam**: a bubble in which every goroutine is known, plus time the test
  controls — an injected clock when the toolchain has no bubble.
- **Tooling**: `testing/synctest` (`synctest.Test` with `synctest.Wait`) on the
  Go versions that ship it; otherwise an injected clock interface with explicit
  barriers built from `sync` and channels.
- **Proves**: the invariant held on the schedules the bubble explored with fake
  time, deterministically and without sleeps.
- **Does not prove**: absence of data races, which is `race-leak`, or behavior
  under real timing on a loaded machine.

## `integration`

- **Oracle**: the real dependency's observable behavior, at a named version.
- **Seam**: a composition root that accepts real implementations, plus a gate
  that keeps the slow path out of the default run.
- **Tooling**: `testing` with build tags and `testing.Short`, `net/http/httptest`
  for HTTP boundaries, and the project's already-adopted container harness for
  real datastores.
- **Proves**: the wiring works for the paths exercised against that dependency
  version and configuration.
- **Does not prove**: branch-level behavior inside each component, or behavior
  against a different dependency version.

## `contract`

- **Oracle**: a shared contract external to both sides — a schema, an interface
  definition, or a reusable suite every implementation must pass.
- **Seam**: a named interface plus a table-driven suite that any implementation,
  real or fake, can be handed to.
- **Tooling**: `testing` subtests run over every implementation of the interface,
  `httptest` for the transport side, generated stubs for the schema side.
- **Proves**: provider and consumer both satisfy the recorded contract today.
- **Does not prove**: that the contract describes what the consumer actually
  needs, or that an unrecorded field is unused.

## `hermetic`

- **Oracle**: the same test under a controlled or denied ambient environment
  producing the same result.
- **Seam**: injected clock, filesystem, environment, and network access points.
- **Tooling**: `t.TempDir`, `t.Setenv`, `testing/fstest` for a synthetic
  filesystem, `httptest` for the network, `testing/iotest` for reader behavior
  including truncation and injected errors, and `-count=1` to defeat the cache.
- **Proves**: the test no longer depends on the ambient inputs it used to read.
- **Does not prove**: production behavior when the real clock, filesystem, or
  network differ from the substitutes.

## `flake`

- **Oracle**: the distribution of outcomes across repeated runs under varied
  ordering and parallelism — not any single run.
- **Seam**: the ability to re-run a package many times and to vary order and
  parallelism from the command line.
- **Tooling**: `go test -count=N`, `-shuffle=on` with the seed recorded,
  `-cpu=1,2,8`, `-race` combined, and `-run` to narrow the target.
- **Proves**: no failure was observed in N runs at the recorded seeds and
  orderings, which bounds the observed failure rate.
- **Does not prove**: determinism. A rare schedule can survive many green runs;
  report N and the seeds with the claim.

## `race-leak`

- **Oracle**: the race detector's happens-before analysis and a goroutine
  inventory taken outside the code's own assertions.
- **Seam**: tests that exercise the concurrent path with real parallelism, plus a
  point at which goroutines can be counted before and after.
- **Tooling**: `go test -race`; goroutine-leak detection through an adopted
  leak-check helper or through the bubble-exit check that `testing/synctest`
  performs when a bubble's goroutines outlive its root; `runtime/pprof`
  goroutine dumps for an inventory when no helper is adopted. On Go 1.27 and
  newer the `goroutineleak` profile names goroutines the collector proves cannot
  be unblocked, which is a stronger inventory than a count delta because it
  excludes goroutines that are merely still running.
- **Proves**: no race was detected on the schedules actually executed, and no
  goroutine was outstanding at the checked point.
- **Does not prove**: race freedom in general. The detector reports only what the
  executed schedules touched, and it needs the code path to actually run.

## `golden`

- **Oracle**: a reviewed, checked-in artifact produced independently of the
  current run.
- **Seam**: a deterministic serializer with stable ordering, plus an `-update`
  flag that only a reviewer uses.
- **Tooling**: `testing` with `testdata/`, an explicit `-update` flag, and a
  normalizer for volatile fields such as timestamps and IDs.
- **Proves**: the output is byte-identical to the reviewed artifact.
- **Does not prove**: that the artifact is correct. An artifact regenerated
  without review makes the code its own oracle, which the selection ladder
  rejects.
- **Toolchain sensitivity**: a golden artifact can encode toolchain behavior
  rather than project behavior. Go 1.27 changed the encoded output of
  `compress/flate` and the error strings of `encoding/json` v1, so a compressed
  golden file or an asserted JSON error message can go red on a toolchain bump
  with no code change. Diagnose a golden failure that appears alongside a
  toolchain upgrade against the upgrade first; regenerating without that check
  is how a real regression gets absorbed into the artifact.

## `property`

- **Oracle**: the invariant itself, stated independently of the implementation —
  a round trip, idempotence, an ordering, or a conservation law.
- **Seam**: a function pure enough to call repeatedly, plus a value generator for
  its domain.
- **Tooling**: `testing/quick` for simple domains, or the project's adopted
  property library, always with the seed and the run count recorded.
- **Proves**: no counterexample among the generated values at that seed and
  count.
- **Does not prove**: the invariant universally. Coverage of the byte-level input
  domain is a fuzz campaign and belongs to `gopher:fuzz`.

## `metamorphic`

- **Oracle**: the metamorphic relation between two related runs — permuting the
  input leaves the sorted output unchanged; scaling every price by k scales the
  total by k.
- **Seam**: the ability to construct the transformed input and to compare two
  executions.
- **Tooling**: plain `testing` with paired executions, and a generator when the
  relation is checked across many pairs.
- **Proves**: the relation held on the pairs tested, which is reachable even when
  no expected output can be computed.
- **Does not prove**: absolute correctness. Both runs can be wrong in the same
  way and still satisfy the relation.

## `differential`

- **Oracle**: a trusted reference implementation — the previous code, a
  specification implementation, or an independent library.
- **Seam**: both implementations callable behind one signature over the same
  inputs.
- **Tooling**: `testing` tables or a generator driving both implementations, with
  a recorded corpus of inputs and any divergence printed in full.
- **Proves**: the two implementations agreed on every input compared, which makes
  it the strongest cheap net during a rewrite or an optimization.
- **Does not prove**: that either is correct. Implementations sharing an origin
  share their bugs.

## `model-state`

- **Oracle**: a small, obviously correct model of the specification written
  independently — a map for a cache, a slice for a queue.
- **Seam**: an operation interface both the real component and the model accept,
  plus a sequence generator and a way to shrink a failing sequence.
- **Tooling**: `testing` plus a generator, the seed recorded, and `-race` when
  the sequences run concurrently.
- **Proves**: no divergence between component and model over the generated
  operation sequences.
- **Does not prove**: that the model is the real specification, and it costs a
  second implementation to maintain.

## `mutation`

The risk is that the suite would pass even if the code were wrong; the oracle is
the injected fault, external to both the code and the assertions; the seam is a
compilable package plus a pinned mutation tool. Cost is the highest of the
twelve.

Result classes, the normalized score, tool discovery, and the advisory versus
required policy live in `references/mutation.md`. That file is the single source
for this family; nothing here restates it.

## Version gating

Resolve every candidate against the Go version declared in the project's
`go.mod`, never against the current stable release or the version installed on
the machine. A technique whose guard the project does not meet is rejected with
the guard stated, not offered with a caveat.

| Capability | Available from | Below the guard |
|---|---|---|
| `t.TempDir` | Go 1.15 | build and clean the temporary directory manually |
| `testing/fstest` | Go 1.16 | use a real temporary directory as the filesystem substitute |
| `t.Setenv` | Go 1.17 | save, set, and restore the variable by hand, and keep the test serial |
| `go test -shuffle` | Go 1.17 | ordering variation needs an external harness |
| `testing/synctest` behind `GOEXPERIMENT=synctest`, with `synctest.Run` | Go 1.24 | no bubble; `deterministic-concurrency` runs on an injected clock |
| `testing/synctest` as a stable API, with `synctest.Test` and `synctest.Wait` | Go 1.25 | on Go 1.24 the experiment gate and the older entry point apply; earlier, neither exists |
| `synctest.Sleep`, which advances the synthetic clock and waits in one call | Go 1.27 | pair `time.Sleep` with an explicit `synctest.Wait` |
| `httptest.NewTestServer(t, handler)`, an in-memory server with automatic cleanup | Go 1.27 | `httptest.NewServer` with an explicit `defer Close`, over a real loopback socket |
| `goroutineleak` profile for the `race-leak` inventory | Go 1.27 | an adopted leak-check helper, the `synctest` bubble-exit check, or a goroutine-count delta |

`go test -race` needs a supported platform and a working cgo or race-enabled
toolchain; when the target platform does not support it, that is a stated
limitation on the `race-leak` family rather than a silent skip.

The guard is enforced by the toolchain, not only by review. `stdversion` is part
of the high-confidence vet subset `go test` runs before building the test
binary, so a standard-library symbol newer than the declared version fails the
run rather than reaching it:

```text
./s.go:5:46: strings.CutLast requires go1.27 or later (module is go1.25)
FAIL	example.com/stdver [build failed]
```

A technique proposed above the project's guard therefore costs a red suite, not
a caveat.

Sources: <https://pkg.go.dev/testing>, <https://pkg.go.dev/testing/synctest>,
<https://pkg.go.dev/testing/quick>, <https://pkg.go.dev/testing/iotest>,
<https://pkg.go.dev/testing/fstest>, <https://pkg.go.dev/net/http/httptest>,
<https://go.dev/doc/articles/race_detector>,
<https://go.dev/doc/go1.27>.
Last verified: 2026-08-31 against a local go1.27.0 toolchain.
