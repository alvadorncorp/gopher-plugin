# Classifying the Comparison

Classification turns two reproduction runs and the checked-in artifact into one
verdict. Determinism is decided first, because staleness is meaningful only for
a generator that produces the same output twice.

## Decision table

| Run A versus run B | Reproduced versus checked-in | Inputs since last recorded generation | Verdict | Required evidence |
|---|---|---|---|---|
| identical | identical | any | `FRESH` | both run hashes, the checked-in hash, the command, the pin |
| identical | differ | at least one input hash moved | `STALE` | the two run hashes, the diff, the moved input hashes |
| identical | differ | every input hash unchanged | intentional local change (a finding) | the diff, the unchanged input hashes, the recorded provenance |
| identical | differ | provenance absent | `STALE` reported with the hand-edit hypothesis open | the diff plus the explicit statement that provenance is missing |
| differ | undecidable | any | `NONDETERMINISTIC` | the two differing run outputs and the varying region |
| unavailable | unavailable | any | `BLOCKED` | the missing pin, command, input, or authorization |

Read the table left to right. The first column decides whether the second column
can be interpreted at all. The third column separates a moved input from a moved
artifact, which is exactly the difference between `STALE` and a hand edit.

## `STALE` versus `NONDETERMINISTIC`

`STALE` says the pipeline works and the world moved: regeneration produces one
known, deterministic result that differs from what is checked in. The
remediation is a `generate` run, explicitly selected, followed by verification.

`NONDETERMINISTIC` says the pipeline itself is unstable: two runs from identical
inputs disagree, so there is no single expected output to compare against.
Staleness stays undecided until determinism is restored. Report the varying
region, name the likely source from the drift table in
`references/reproduction.md`, and hand the generator defect to
`gopher:developer`. A regeneration performed while the generator is unstable
only replaces one arbitrary output with another.

## The intentional local change

Sometimes the reproduction is deterministic, the inputs have not moved, and the
checked-in artifact still differs. Someone edited the generated file.

This is a finding, never an accepted state. The artifact now claims a provenance
it no longer has, and the next regeneration silently discards the edit. The
remediation is to move the change into the place that survives regeneration:

| Where the change belongs | When | Owner |
|---|---|---|
| The input | The change expresses data the generator already reads: a schema field, a type, a template value | `gopher:developer` |
| The generator | The change expresses behavior the generator should always emit | `gopher:developer` |
| The generated contract | The change alters an exported API, a wire schema, or a persisted shape | `gopher:architecture` |

After the change moves, regenerate and confirm the artifact reaches `FRESH`.
Re-editing the artifact by hand restores the same finding on the next check.

## `BLOCKED`

Reach `BLOCKED` when reproduction cannot start or cannot finish:

- The generator is unavailable, and installing it is outside this skill.
- The generator is unpinned, so no version can be attributed to the output.
- The declared command is missing, so there is nothing authoritative to run.
- An input is unreachable, for example a remote schema behind a network call.
- Running the declared command needs an authorization that is not granted.

A `BLOCKED` report states which of these applies, for which artifact, and the
exact remediation, such as the pin line the project would add. `BLOCKED` is a
complete answer with a missing precondition, not a failed attempt.

## Reporting the verdict

Every verdict carries its evidence in the output bundle: the two run hashes, the
checked-in hash, the diff or its absence, the input hashes with their comparison
against the recorded provenance, and the exact commands with their exit status.
A verdict without those fields is an opinion, so report the missing field as a
limitation instead of inferring the verdict.
