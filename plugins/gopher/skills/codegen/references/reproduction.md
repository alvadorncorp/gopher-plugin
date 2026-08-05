# Reproducing Generation

Reproduction answers one question: run the declared command again from the same
inputs, and does the same output come back? The answer is trustworthy only when
the working tree stays untouched and the environment is controlled.

## Reproduce into a temporary location

Copy the tracked tree into a scratch directory, run the declared command there,
and read the result out. The working tree keeps its content and its timestamps.

```bash
tmp="$(mktemp -d)"
git archive --format=tar HEAD | tar -x -C "$tmp"
( cd "$tmp" && go generate ./... )
git diff --no-index -- ./internal/pill/pill_string.go "$tmp/internal/pill/pill_string.go"
```

Two properties matter. The copy comes from tracked content, so untracked noise
stays out of the comparison. The command runs inside the copy, so any file the
generator writes lands in the scratch directory.

When the project's declared command is a Makefile target or a registry
invocation, run that target inside the copy rather than reconstructing the
command by hand. The declared command is part of the contract being tested.

## At least two runs

Determinism is a property of repetition, so a single run proves nothing. Run the
same declared command from identical inputs into two distinct scratch
directories and compare all three artifacts:

| Comparison | Meaning |
|---|---|
| run A versus run B | whether the generator is deterministic |
| run A versus checked-in | whether the checked-in output is current |

Record this as `repro_runs: 2` in the evidence, alongside the two hashes. A
project may configure a higher count for a generator with known instability;
raise the count, never lower it below two.

## Controlling the environment

A diff means something only when everything outside the inputs is held fixed.

| Source of drift | Symptom in the diff | Control |
|---|---|---|
| Absolute paths | The scratch path appears in the output | Run at the same relative depth, or normalize the path before comparing |
| Timestamps and dates | A header line changes on every run | Ask the generator for a time-free output; record time-in-output as a generator defect |
| Map iteration order | Declarations or fields reorder between runs | The generator sorts its keys; report reordering to `gopher:developer` |
| Concurrency inside the generator | Output order varies under load | Same as above; the fix belongs to the generator |
| Generator version drift | Whole-file reformatting or new fields | Pin the generator and re-run |
| Toolchain version | An embedded version string moves | Pin `go` and `toolchain` in `go.mod`; record `go version` |
| Environment variables | Output varies by machine | Fix `GOOS`, `GOARCH`, `CGO_ENABLED`, `TZ`, and `LANG` explicitly for both runs |
| Remote inputs | Output varies with an upstream fetch | Vendor the input and hash it, so the input set is complete |

Set the controlled variables identically for both runs and record the exact set
used. An uncontrolled variable turns a real difference and an environmental
artifact into the same diff.

## Comparing the result

Compare at two levels, in this order:

1. **Byte level.** Hash each artifact and diff the bytes. Byte identity is the
   default verdict and the only one that needs no interpretation.

   ```bash
   git hash-object "$tmp/internal/pill/pill_string.go" internal/pill/pill_string.go
   diff -u internal/pill/pill_string.go "$tmp/internal/pill/pill_string.go"
   ```

2. **Semantic level.** When the bytes differ, establish what kind of difference
   it is. Normalize formatting with `gofmt` on both sides, then compare again; a
   difference that survives formatting is a content difference, and one that
   disappears is a formatting difference worth reporting separately.

   ```bash
   gofmt -d internal/pill/pill_string.go
   ```

Semantic equality is a documented downgrade from byte equality, never a silent
substitution. State which level produced the verdict, and keep the byte-level
hashes in the evidence either way.

## Handing the result forward

Two agreeing runs hand a decidable comparison to `references/staleness.md`. Two
disagreeing runs stop there: the generator is unstable, the state is
`NONDETERMINISTIC`, and the finding routes to `gopher:developer` with the two
differing outputs as evidence.
