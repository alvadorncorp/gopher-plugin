# Triage

Triage turns a raw failure into a case a reviewer can act on: a smallest input
that still fails, a command that replays it, and a classification that says
whether the input or the environment caused it.

## Automatic minimization

When a campaign finds a failing input, the engine immediately tries to shrink
it, bounded by `-fuzzminimizetime`. It repeatedly proposes a smaller or simpler
input and keeps the ones that still fail, then writes the smallest surviving
input to `testdata/fuzz/<FuzzTarget>/`.

Its limits are worth knowing before trusting the result.

- The budget bounds it. A short `-fuzzminimizetime` returns a partially reduced
  input, which is a starting point rather than a finished one.
- It preserves failure, not cause. An input that fails for a second, unrelated
  reason can survive minimization and hide the first.
- A non-deterministic target confuses it, because a candidate that fails
  intermittently looks like a candidate that passed.
- It shrinks the value, never the invariant. An over-broad assertion produces a
  small input that fails for an uninteresting reason.

## Manual reduction

Continue by hand when the automatic result is still large or still noisy.

1. Copy the written `testdata` file and work on the copy, keeping the original.
2. Remove one structural element at a time — a field, a repetition, a nesting
   level — and re-run after each removal.
3. Replace surviving bytes with neutral values (`0x00`, `a`, `0`) to separate
   the structure that matters from the content that happens to be there.
4. Narrow the assertion. When the target checks several properties, split them
   until exactly one property fails.
5. Stop when every remaining element is load-bearing: removing any one of them
   makes the failure disappear.

Record each reduction step. The sequence itself often names the defect before
the final input does.

## Replaying the written failure

The failure file lives in the seed corpus, so a plain test run replays it with
no fuzzing engine involved.

```sh
go test ./internal/wire -run='FuzzDecode/a1b2c3d4e5f6'
```

The sub-test name is the failure file's name inside
`testdata/fuzz/FuzzDecode/`. Running the whole target replays every seed file at
once:

```sh
go test ./internal/wire -run=FuzzDecode
```

This replay is the reproduction that matters. It uses no cache corpus, no
mutation, and no budget, so it is what a reviewer and CI will both execute.

## Reproducing `repro_runs` times

Run the replay `repro_runs` times (default `3`) before classifying it.

```sh
go test ./internal/wire -run='FuzzDecode/a1b2c3d4e5f6' -count=3
```

Use `-count`, which forces re-execution, rather than repeating the command,
which the test cache may satisfy without running anything. Add `-race` when the
target touches shared state; a data race reported here is a concurrency defect
and routes to `gopher:concurrency`.

Every run failing is a `CRASH`. Every run passing, or an intermittent mix, moves
to the table below.

## Real crash or flaky environment

| Observation | Reading | Status |
|---|---|---|
| Fails on every replay, on a clean checkout, on another machine | Input-driven defect | `CRASH` |
| Fails only with `-race`, and the report names a data race | Concurrency defect, still real | `CRASH`, handoff to `gopher:concurrency` |
| Fails only past a test timeout, and the input is large | The input drives super-linear cost | `CRASH`, handoff to `gopher:performance` |
| Fails only under load or with many parallel workers | Resource exhaustion in the harness | `FLAKY`, re-run with `-parallel=1` |
| Fails only after other tests in the same package | Shared global state or ordering dependence | `FLAKY` until the target is isolated |
| Fails only on one machine, one operating system, or one Go version | Environment-specific behavior | `LIMITED` until reproduced elsewhere |
| Failed once during the campaign and never on replay | Transient environment effect | `FLAKY` |
| Fails only when the file system, network, or clock is touched | The target reaches outside its input | `FLAKY` until the seam is introduced |

A `FLAKY` result is a finding about the harness rather than about the input.
Report what varied between the failing and the passing runs, and name the
isolation step that would make the target deterministic.

A `CRASH` proceeds to `references/promotion.md`. The production fix itself
belongs to the receiving owner, not to this skill.
