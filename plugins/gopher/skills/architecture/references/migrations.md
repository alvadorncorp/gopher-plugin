# Go Architecture Migration

1. Capture imports, public consumers, behavior, errors, and tests.
2. Add a consumer seam or compatibility entry point.
3. Move one cohesive responsibility without changing behavior.
4. Migrate call sites in bounded batches.
5. Run package, module, architecture, and compatibility checks.
6. Remove the old path only after references reach zero.

Every step names rollback and approval status. Keep old and new APIs together
only for a documented migration window; avoid permanent duplicate ownership.
