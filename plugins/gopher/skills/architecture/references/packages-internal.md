# Go Packages and internal Boundaries

- Group code by cohesive responsibility and change, not type category.
- Keep package names short and meaningful at call sites.
- Use `internal/` when an ownership boundary must be enforced across consumers.
- Keep dependency direction explicit; detect import cycles before proposing an interface.
- Move behavior with the data/invariants it owns rather than creating utility packages.
- Keep package APIs small; unexport implementation detail until a real consumer exists.

Evidence includes import graph, change history, callers, owned invariants, and
team/module responsibility. A new folder without a dependency rule is not an
architecture boundary.
