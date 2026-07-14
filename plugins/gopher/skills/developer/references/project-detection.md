# Go Project Detection

Inspect in this order and record evidence:

1. `go.mod`: module path, `go` directive, dependencies, replacements.
2. `toolchain` directive or `go.work`: selected toolchain and workspace modules.
3. CI, Makefile/Taskfile, scripts, and contributor docs: canonical commands.
4. Existing code/tests: package naming, errors, constructors, test libraries.
5. Adopted lint, generation, vulnerability, race, fuzz, and benchmark tooling.

Use the declared version even when a newer local toolchain exists. For a new
project with no declaration, verify the current stable Go release from the
official Go site before choosing it. Record version requirements beside advice
that depends on newer APIs.

Official sources: <https://go.dev/ref/mod>, <https://go.dev/doc/toolchain>.
Last verified: 2026-07-14.
