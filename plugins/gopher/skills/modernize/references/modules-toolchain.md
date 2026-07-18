# Modules, toolchain, and dependencies

Modernize module metadata, workspace layout, and dependencies conservatively,
staying inside the declared version and adopted commands.

## Modules and workspace

- Align `go.mod` directives with the declared version without raising it under
  `target_go = "declared"`.
- Respect an existing `go.work`; propose workspace changes as previews and hand
  a module-topology change to `gopher:architecture`.

## Toolchain

- Keep the declared `toolchain` directive authoritative. Recommend, but do not
  silently change, a toolchain version.
- Use the project's adopted build and generate commands; do not substitute a
  different toolchain invocation.

## Dependencies

- Follow `modernize.dependency_updates`: `none` proposes no version bump,
  `patch` allows patch-level updates, `minor` allows up to minor updates.
- A dependency update never resolves to an unattended latest version and always
  previews the resulting `go.mod` and `go.sum` diff.
- Verify the build and tests against the compatibility baseline after any
  accepted update, and record the exact before/after versions.
