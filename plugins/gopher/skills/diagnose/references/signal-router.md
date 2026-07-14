# Evidence-based Signal Router

| Dominant supported signal | Primary owner |
|---|---|
| Local API, types, errors, modules, tooling, tests, or reversible implementation | `gopher:developer` |
| Cross-package dependency, package boundary, interface seam, module/workspace, or public contract | `gopher:architecture` |
| Goroutine lifetime, channel, synchronization, context, race, leak, memory, throughput, benchmark, or profile | `gopher:concurrency-performance` |
| Explicit pattern forces and selection/rejection | `gopher:design-patterns` |
| Language-agnostic internal application boundary or dependency direction | `gopher:application-architecture` |
| Threat, trust boundary, exploit path, vulnerable dependency/symbol, or security control | `gopher:security` |
| Diff/PR review intent rather than diagnosis | `gopher:review` |

Mixed symptoms still receive one owner: choose the domain whose risk and
evidence explain the observed failure. Put secondary constraints in `handoff`
without assigning multiple primary owners.
