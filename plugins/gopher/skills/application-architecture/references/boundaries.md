# Internal Boundary Discovery

Build a boundary evidence map before proposing structure:

| Evidence | Question |
|---|---|
| Capability and vocabulary | Which decisions and terms change together? |
| Change history | Which files/modules repeatedly change in the same work item? |
| Data and invariants | Who owns each invariant and transaction boundary? |
| Dependencies | Which direction is stable, and where are cycles? |
| Runtime needs | Which interactions need isolation, latency, or failure handling? |
| Team ownership | Who can evolve the boundary independently? |

A boundary is justified when it contains cohesive policy and reduces observed
change coupling. Folder symmetry or hypothetical reuse alone is insufficient.
Record inputs, outputs, owned invariants, allowed dependencies, and prohibited
knowledge for every proposed boundary.
