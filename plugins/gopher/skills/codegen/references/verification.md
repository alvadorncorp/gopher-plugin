# Verifying Generated Artifacts

A reproducible artifact is not yet a trustworthy one. Verification confirms that
the output compiles, that the project's own gates pass with it, and that the
public surface is what the artifact claims to provide.

## The verification ladder

| Level | Question | Command |
|---|---|---|
| Compilation | Does the artifact build in its package? | `go build ./internal/pill/...` |
| Toolchain checks | Does the artifact pass the project's static gates? | `go vet ./internal/pill/...` and the adopted lint command |
| Project tests | Does the project's own test command pass? | the declared command, for example `make test` or `go test ./...` |
| Public surface | Is the exported API the one the artifact claims? | `go doc -all ./internal/pill` before and after |

Climb the ladder in order and stop at the first failing rung, because a
compilation failure makes every result above it meaningless.

## Build tags

A generated artifact guarded by a build constraint compiles only when the tag is
set. Read the `//go:build` line on the artifact and pass the same tags to every
verification command:

```bash
grep -n '^//go:build' internal/pill/pill_string.go
go build -tags=integration ./internal/pill/...
```

An artifact that compiles only under a tag the project never sets in its gates
is a limitation worth reporting: nothing in the pipeline currently proves it
builds.

## Use the project's own test command

Read the declared test command from `gopher:config`, the Makefile, or the CI
workflow, and run that command. An invented substitute can pass where the real
gate fails, which turns verification into a false assurance. When the declared
command is unavailable, report that as a limitation and record the narrower
command actually used.

Scope the run proportionally: the packages holding the artifacts and their
direct dependents first, the full suite when the artifact sits on a widely
imported contract.

## Public surface comparison

Generated APIs are contracts, so a regeneration that adds, removes, or changes
an exported symbol is a contract movement, not a refresh.

```bash
go doc -all ./internal/pill > /tmp/surface-before.txt
go doc -all ./internal/pill > /tmp/surface-after.txt
diff -u /tmp/surface-before.txt /tmp/surface-after.txt
```

When the project has adopted and pinned an API diff tool, prefer it and record
the pin; when it has not, `go doc -all` on both sides is the portable evidence.

Classify what the diff shows:

| Surface change | Meaning | Route |
|---|---|---|
| No exported change | A refresh of unexported or internal detail | stays with `gopher:codegen` |
| Added exported symbol | The contract grew | `gopher:architecture` |
| Removed or renamed exported symbol | The contract broke compatibility | `gopher:architecture` |
| Changed exported signature or type | The contract moved | `gopher:architecture` |

## Boundaries

- A public-surface change on a generated artifact belongs to
  `gopher:architecture`, which owns the contract decision. Report the diff, the
  driving input change, and the compatibility impact, and hand it over.
- A compilation failure inside the generator's own Go code belongs to
  `gopher:developer`, together with the failing output as evidence.
- A failing project test caused by a regenerated artifact is reported with the
  test name, the failure, and the classification that produced the artifact, so
  the receiving owner starts from evidence rather than from a symptom.

## Recording verified artifacts

Fill `verified_artifacts` with one entry per artifact: its path, its hash, the
levels of the ladder that passed, the tags used, and the exact commands with
their exit status. An artifact that reached only the compilation rung is
recorded as verified to that level, not as verified.
