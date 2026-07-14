# Profiling and Runtime Evidence

Select the profile that matches the claim:

- CPU profile for on-CPU hotspots.
- Heap/in-use profile for retained memory.
- Allocation profile for allocation volume.
- Mutex/block profiles for contention and blocking.
- Execution trace for scheduler, goroutine, network, and GC timing.
- Runtime metrics/GC traces for heap and collection behavior.

Capture a representative workload and profile duration. Attribute cost to a
call path before changing code, then repeat the same capture after the change.
Production profiling requires authorization and a bounded collection plan.

Source: <https://go.dev/doc/diagnostics>.
Last verified: 2026-07-14.
