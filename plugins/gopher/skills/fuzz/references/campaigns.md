# Running a campaign

A campaign is a bounded experiment: one target, one budget, one recorded
command line. Everything in this file exists to keep it bounded and repeatable.

## The command

```sh
go test ./internal/wire \
  -run=FuzzDecode \
  -fuzz=FuzzDecode \
  -fuzztime=60s \
  -fuzzminimizetime=30s
```

| Flag | Meaning | Notes |
|---|---|---|
| `-fuzz=<Regexp>` | Selects the target to fuzz | Matches exactly one target per invocation |
| `-fuzztime=<duration>` | Total campaign budget | Accepts a duration such as `60s`, or an execution count such as `100000x` |
| `-fuzzminimizetime=<duration>` | Budget for minimizing a discovered failure | Also accepts an `Nx` count |
| `-run=<Regexp>` | Restricts the unit tests that run first | Keeps the pre-campaign phase short |
| `-parallel=<n>` | Concurrent workers during fuzzing | Defaults to `GOMAXPROCS` |
| `-v` | Verbose progress | Useful when interpreting a slow campaign |

Without `-fuzztime`, the campaign runs until it fails or is interrupted. Always
pass the budget resolved from `[fuzz]`, and record the full command line with
the result.

## One target per invocation

`-fuzz` fuzzes a single target, even when its pattern would match several. The
engine devotes the whole budget and the whole corpus to one target, which is
what makes coverage-guided exploration effective. Fuzzing several targets means
several invocations, each with its own budget.

A run that also matches unit tests executes those tests first, in the usual way,
and then starts fuzzing the selected target. Seeds from `f.Add` and from
`testdata` run during that first phase too, so a broken seed surfaces before any
budget is spent.

## Local and CI budget shapes

| Shape | Budget key | Typical value | Purpose |
|---|---|---|---|
| Interactive | `local_budget_seconds` | `60` | Fast feedback while designing a target or checking a fix |
| Unattended | `ci_budget_seconds` | `300` | Regular scheduled exploration with a larger corpus |

In CI, run the seed corpus on every commit through the ordinary `go test` path,
and run the coverage-guided campaign on a schedule rather than on every commit.
A scheduled job holds the cache corpus across runs, which compounds exploration;
a per-commit job starts cold every time and mostly re-derives the same inputs.
State the budget in the report, since the budget is what a `PASS` means.

## Parallelism

Workers execute in separate processes and share the corpus. Raising `-parallel`
raises executions per second when the target is CPU-bound and independent, and
it raises contention when the target touches a shared file, port, or global.

- A target that keeps per-input state inside its own call is safe to parallelize.
- A target that touches a process-wide or machine-wide resource is either made
  independent first or run with `-parallel=1`.
- Report the parallelism used, because it changes both throughput and the
  reproducibility of a timing-sensitive failure.

## Reading the progress output

```text
fuzz: elapsed: 3s, gathering baseline coverage: 42/128 completed
fuzz: elapsed: 6s, gathering baseline coverage: 128/128 completed, now fuzzing with 8 workers
fuzz: elapsed: 9s, execs: 71204 (23735/sec), new interesting: 6 (total: 134)
```

| Signal | Reading |
|---|---|
| Long baseline phase | The seed corpus is large or the target is slow per input |
| Low executions per second | The target does heavy work, allocates heavily, or performs I/O |
| `new interesting` climbing | The engine is still discovering new coverage; more budget is likely to pay |
| `new interesting` flat near zero | Exploration has plateaued; a new seed, a new invariant, or a narrower target helps more than more time |
| Failure reported | The engine writes the input to `testdata/fuzz/<FuzzTarget>/` and moves to minimization |

## What exhausting the budget means

A campaign that spends its whole budget without a failure is a bounded negative
result. It says that this target, with this corpus, on this machine, for this
budget, found no input that violates the invariant. It does not say the function
is correct, and it does not generalize to a different invariant or a different
target.

Report `PASS` together with the budget, the parallelism, the Go version, and
whether the cache corpus was warm. Those four facts are what makes the negative
result comparable to the next one.
