# Incremental Architecture Migration

Use this sequence for an approved structural change:

1. Record current behavior, consumers, invariants, and dependency graph.
2. Add a compatibility seam at the consumer boundary.
3. Move one cohesive behavior with characterization tests.
4. Run old and new paths only when a bounded comparison is safe.
5. Switch consumers in small batches with rollback instructions.
6. Remove the old path after references and architecture checks reach zero.

Every step names affected contracts, rollback, verification, and completion
evidence. Keep migrations within one deployment until operational evidence
justifies a distributed boundary.
