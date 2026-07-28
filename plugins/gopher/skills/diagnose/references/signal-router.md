# Evidence-based Signal Router

| Dominant supported signal | Primary owner |
|---|---|
| Local API, types, errors, modules, tooling, tests, or reversible implementation | `gopher:developer` |
| Cross-package dependency, package boundary, interface seam, module/workspace, or public contract | `gopher:architecture` |
| Goroutine lifetime, channel, synchronization, context, race, deadlock, goroutine leak, or backpressure | `gopher:concurrency` |
| Algorithmic or asymptotic cost, allocation, GC, memory growth, cache behavior, parsing, I/O amplification, benchmark, profile, latency, or throughput | `gopher:performance` |
| Explicit pattern forces and selection/rejection | `gopher:design-patterns` |
| Language-agnostic internal application boundary or dependency direction | `gopher:application-architecture` |
| Threat, trust boundary, exploit path, vulnerable dependency/symbol, or security control | `gopher:security` |
| Diff/PR review intent rather than diagnosis | `gopher:review` |
| Project configuration bootstrap, validation, or explanation | `gopher:config` |
| Cyclomatic/cognitive complexity, hotspots, or complexity thresholds | `gopher:complexity` |
| Coverage, mutation score, or whether tests detect behavioral faults | `gopher:test-quality` |
| Go version, API, module, dependency, or toolchain modernization | `gopher:modernize` |
| Repository-wide or multidimensional remediation across two or more dimensions | `gopher:refactor` |

Mixed symptoms still receive one owner: choose the domain whose risk and
evidence explain the observed failure. Put secondary constraints in `handoff`
without assigning multiple primary owners.
