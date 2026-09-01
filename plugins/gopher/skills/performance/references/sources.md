# Version-sensitive sources

These references change with Go releases and tool versions. Confirm each against
the toolchain the target project actually declares before relying on a detail
here.

## Measurement and diagnostics

- Go diagnostics overview: <https://go.dev/doc/diagnostics>
- `testing` benchmarks: <https://pkg.go.dev/testing#B>
- `benchstat`: <https://pkg.go.dev/golang.org/x/perf/cmd/benchstat>
- `runtime/pprof`: <https://pkg.go.dev/runtime/pprof>
- `net/http/pprof`: <https://pkg.go.dev/net/http/pprof>
- `runtime/trace`: <https://pkg.go.dev/runtime/trace>
- `go tool trace`: <https://go.dev/cmd/trace/>
- `goroutineleak` profile: <https://pkg.go.dev/runtime/pprof#Profile>
- Execution traces: <https://go.dev/blog/execution-traces-2024>

## Runtime, GC, and compiler

- GC guide, optimization: <https://go.dev/doc/gc-guide#Optimization_guide>
- GC guide, memory limit: <https://go.dev/doc/gc-guide#Memory_limit>
- GC guide, cost model: <https://go.dev/doc/gc-guide#Understanding_costs>
- Profile-guided optimization: <https://go.dev/doc/pgo>
- Compiler diagnostics: <https://go.dev/src/cmd/compile/README>
- Green Tea GC: <https://go.dev/blog/greenteagc>
- Go 1.26 runtime notes: <https://go.dev/doc/go1.26#runtime>
- Go 1.27 release notes: <https://go.dev/doc/go1.27>

## Language and standard library

- `unsafe`: <https://pkg.go.dev/unsafe>
- `slices`: <https://pkg.go.dev/slices>
- `strings.Builder`: <https://pkg.go.dev/strings#Builder>
- `sync.Pool`: <https://pkg.go.dev/sync#Pool>
- Maps: <https://go.dev/blog/maps>
- Comparison operators: <https://go.dev/ref/spec#Comparison_operators>
- Map types: <https://go.dev/ref/spec#Map_types>
- `container/heap`: <https://go.dev/src/container/heap/heap.go>
- `slices` sort source: <https://go.dev/src/slices/sort.go>
- `slices.Delete`: <https://pkg.go.dev/slices#Delete>
- Generic slice functions: <https://go.dev/blog/generic-slice-functions>
- `strings.Builder` source: <https://go.dev/src/strings/builder.go>

## Data access

- sqlc slice parameters: <https://docs.sqlc.dev/en/stable/howto/select.html#passing-a-slice-as-a-parameter-to-a-query>
- PostgreSQL ANY/SOME: <https://www.postgresql.org/docs/current/functions-comparisons.html#FUNCTIONS-COMPARISONS-ANY-SOME>
- pgx Batch: <https://pkg.go.dev/github.com/jackc/pgx/v5#Batch>

## Review cadence

- Re-read the guard table in `references/version-sensitive.md` after every
  stable Go release; a runtime change can invalidate a recommendation that was
  correct one release earlier.
- Record the Go version, toolchain, flags, and machine state with every
  measurement so a later reviewer can reproduce it.
- When a source reports that a knob was deprecated, renamed, or removed, confirm
  it against the toolchain in hand before updating the guard — an unknown
  `GOEXPERIMENT` name errors, an accepted one echoes back, and `go help` and
  `go tool <cmd> -h` report the flags that release actually registers. A removal
  a release note forecasts is not a removal (`adr:gopher:011`). Restate the
  baseline once the guard changes.

Last verified: 2026-08-31 against a local go1.27.0 toolchain.
