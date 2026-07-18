# Tool discovery

`[tools].modernize` governs analyzer selection. `auto` discovers an adopted or
already-available tool and never installs one.

## Discovery order

1. An explicit command in `[tools].modernize` (used verbatim).
2. The official `modernize` analysis pass, when it is available in the project's
   toolchain and compatible with the declared Go version.
3. An adopted project modernization command already declared.
4. Otherwise, report an explicit limitation — do not install a tool.

## Using the `modernize` pass

- Run it in preview mode first and read its diagnostics.
- Apply its fixes incrementally, not in one bulk pass, and verify after each
  increment.
- Pin and record the tool version so the preview is reproducible.

## Degradation

- `off` disables the dimension; report it as not run.
- An unavailable `auto` tool is a limitation. Analysis still reports the
  modernizations it can identify by inspection and marks the rest as unverified.
