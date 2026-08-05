---
name: cgo
description: Designs, implements, and audits Go/C boundaries across ABI and representation, memory ownership and lifetime, the cgo pointer-passing rules, callbacks, thread affinity, blocking calls, linking, build tags, sanitizers, and build matrices. Use to wrap a C library or bind to a native library from Go, and for cgo integration design, pointer-rule audits, `//export` callbacks, `LockOSThread` affinity, and `CGO_ENABLED` or cross-compilation matrices. Route an unattributed crash or hang to `gopher:diagnose` and goroutine mechanics to `gopher:concurrency`.
---

# Go CGO Boundaries

## Context and ownership

Own the Go/C frontier and the risks that exist because the frontier exists:
ABI and representation, memory ownership and lifetime, the cgo pointer-passing
rules, callbacks, thread affinity, blocking C calls, the linker, build tags,
sanitizers, and build matrices. Primary owner: `gopher:cgo`.

This skill takes attributed boundary work. Keep the split with attribution
concrete: a segfault nobody has attributed yet is `gopher:diagnose`; auditing
whether a pointer that crosses the boundary satisfies the pointer-passing rules
is `gopher:cgo`, and this skill takes the boundary question once the evidence
names it.

| Question | Owner |
|---|---|
| A crash or hang with no causal attribution | `gopher:diagnose` |
| Goroutine and synchronization mechanics | `gopher:concurrency` |
| Implementation unrelated to the boundary | `gopher:developer` |
| Security of the integration | `gopher:security` |
| Representation, ownership, pointer rules, callbacks, linking, build matrix | `gopher:cgo` |

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `design` | A Go/C boundary is being defined or reshaped | The boundary, data shapes, ownership contracts, and pointer rules are written down and reviewable |
| `implement` | An authorized integration is being written | The authorized boundary code exists, its ownership pairing is explicit, and the project's adopted checks run clean |
| `audit` | An existing boundary needs its guarantees reviewed | Every crossing value has a stated rule, owner, and lifetime, and each open risk is recorded with its evidence |
| `build-matrix` | Targets, toolchains, or linking change | Each `GOOS`/`GOARCH`, `CGO_ENABLED`, compiler, and link mode is either verified or reported as an unavailable requirement |

Terminal states: `COMPLETE` when the mode's stop condition holds with no open
risk; `RISKS_FOUND` when the work finished and at least one boundary risk stays
open; `BLOCKED` when a required toolchain, header, library, or authorization is
unavailable and the exact requirement is reported.

## Workflow

1. Define the boundary and the data representations: every function that
   crosses, every type on each side, and the C-to-Go mapping from
   `references/abi-representation.md`.
2. Assign memory ownership and lifetime on each side using
   `references/ownership-lifetime.md`, so every allocation names its allocator,
   its releaser, and the moment of release.
3. Declare the rule and the runtime guarantee for every pointer that crosses,
   following `references/pointer-rules.md`, including pinning and handle
   choices gated by the project's declared Go version.
4. Classify callbacks, thread affinity, locked OS threads, and blocking calls
   with `references/callbacks-threads.md`, and state the OS-thread cost of each
   blocking crossing.
5. Enumerate build tags, compilers, linkers, `pkg-config`, static and dynamic
   linking, and cross-compilation from `references/build-matrix.md`.
6. Verify with the tools the project has already adopted
   (`references/verification.md`), and record for each result what it proves and
   what it leaves untested.

## Output format

```yaml
selected_skill: gopher:cgo
primary_owner: gopher:cgo
mode: design | implement | audit | build-matrix
status: COMPLETE | RISKS_FOUND | BLOCKED
boundary_summary:
pointer_rules:
thread_affinity:
build_matrix:
verification:
risks:
limitations:
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
```

## Authorization boundaries

- Resolve a pointer-rule detection by changing the ownership or the lifetime so
  the crossing satisfies the rule. Keep `GODEBUG=cgocheck` at its default level,
  which is cheap enough to leave on everywhere including production, and run
  `GOEXPERIMENT=cgocheck2` as a dedicated verification build. Lowering either to
  clear a detection is never the remediation: it removes the report and leaves
  the defect, and the resulting corruption is unrecoverable once the collector
  moves or reclaims the object.
- An unattributed crash keeps its owner: `gopher:diagnose`. Report the symptom
  and hand it back rather than treating a stack trace as a boundary finding.
- Use the toolchains and tools the project's contract declares, and report an
  unavailable cross-compiler, sanitizer, header, or library as a limitation
  together with the exact requirement.
- Use the compilers, linkers, sanitizers, and test commands the project already
  declares. Adding a dependency, a system package, or a new link mode is an
  approval-gated change.
- Hand a local reversible edit outside the boundary to `gopher:developer`, and
  keep the integration's threat model with `gopher:security`.

## Quality checklist

- Every crossing value has a stated C type, Go type, size, and alignment.
- Every allocation names its allocator, its releaser, and the release moment.
- Every pointer crossing states its rule, and pinning or handle use names the
  Go version that provides it.
- Callbacks name their registration path, their exported Go entry point, and the
  thread they run on.
- Blocking C calls state their OS-thread cost and any locked-thread requirement.
- The build matrix lists each target with its compiler, flags, link mode, and
  verification status.
- Each verification result records what it proves and what it leaves untested.
- Unavailable toolchains appear as limitations with their exact requirement.

## References

- `references/abi-representation.md` — C-to-Go type mapping, layout, strings, slices, and the cases cgo cannot express.
- `references/ownership-lifetime.md` — allocation and release pairing, lifetimes beyond the call, and the ownership table.
- `references/pointer-rules.md` — the cgo pointer-passing rules, `runtime.Pinner`, `cgo.Handle`, and `cgocheck` detections.
- `references/callbacks-threads.md` — `//export` callbacks, thread affinity, blocking calls, stacks, and signals.
- `references/build-matrix.md` — `CGO_ENABLED`, target matrix, `#cgo` directives, `pkg-config`, linking, and cross-compilation.
- `references/verification.md` — adopted tools, what each one proves, and what it leaves untested.
- `references/sources.md` — version-sensitive official references and review cadence.
