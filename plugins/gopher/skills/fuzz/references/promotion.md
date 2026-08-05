# Promotion

Promotion converts a minimized, reproducible failure into a permanent
regression seed and hands the defect to the owner who will fix it.

## What qualifies

A case is promoted when all four hold.

1. It is minimized: every remaining element is load-bearing.
2. It reproduces `repro_runs` times through a plain `go test -run` replay.
3. It carries no secrets and no personal data.
4. It fails for a stated reason, tied to the target's invariant.

A case missing any of these stays evidence. Report it with what is missing and
the next step that would complete it, rather than committing it as a regression.

## Committing the seed

The engine already wrote the failing input to
`testdata/fuzz/<FuzzTarget>/<name>`. Promotion is the deliberate act of keeping
it, naming it, and documenting it.

- Rename the generated content-hash file to something a reviewer can read, such
  as `truncated-length-prefix` or `nested-depth-overflow`. The file name is free
  text and the format is unchanged.
- Keep the file in `testdata/fuzz/<FuzzTarget>/` so a plain `go test` replays it
  on every run, with no fuzzing engine and no budget.
- Promote a very small case as an `f.Add` call instead when it reads better in
  the target itself; both locations are part of the seed corpus.
- Commit the seed together with the invariant it violates, so the two travel as
  one change.

## Naming and provenance

Name the case after the defect it exposes, not after the input's bytes. Record
alongside it, in the commit message or in a comment next to the matching
`f.Add`:

| Field | Content |
|---|---|
| Target | The `FuzzXxx` function and its package |
| Invariant | The property the input violates |
| Discovery | Campaign date, budget, Go version, and parallelism |
| Reduction | Automatic, manual, or both |
| Reproduction | The exact `go test -run` command and `repro_runs` |
| Sanitization | Whether the input derives from a real sample, and what was replaced |

Provenance is what lets a future reader decide whether the seed is still
relevant after the format or the invariant changes.

## The before-and-after requirement

A promoted seed earns its place by demonstrating both halves.

1. On the current code, the replay fails. Capture that output.
2. After the fix lands under the receiving owner, the same replay passes with no
   change to the seed file.

A seed that passes before the fix is not a regression test for this defect; it
either lost its reducing power during minimization or targets a different path.
Return it to triage rather than committing it.

Keep the seed after the fix ships. Its cost is one replay per test run, and its
value is detecting the reintroduction of the same defect.

## The handoff record

The fix happens under the receiving owner. Hand over a record that is
self-contained, so the receiving owner starts from evidence rather than from a
description.

```yaml
handoff: gopher:developer
target: FuzzDecode (internal/wire)
invariant: decoding a frame never panics and never returns a length beyond the buffer
minimized_input: testdata/fuzz/FuzzDecode/truncated-length-prefix
reproduction: go test ./internal/wire -run='FuzzDecode/truncated-length-prefix' -count=3
observed: panic in decodeHeader at internal/wire/frame.go:88 (slice bounds out of range)
expected: a returned error naming the truncated frame
campaign: 300s budget, Go 1.25.1, -parallel=8, warm cache corpus
```

Choose the receiving owner by the nature of the defect: `gopher:developer` for
an ordinary correctness defect, `gopher:security` when the input crosses a trust
boundary or the failure is exploitable, `gopher:concurrency` for a race or a
deadlock, and `gopher:performance` when the input drives super-linear cost. Name
exactly one owner. When the classification is genuinely unclear, hand the
evidence to `gopher:diagnose` for attribution instead of guessing.
