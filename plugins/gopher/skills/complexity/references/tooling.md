# Analyzer discovery and pinning

The `[tools].complexity` value governs analyzer selection. `auto` discovers a
compatible project-adopted or already-available analyzer. It never installs one.

## Discovery order

1. An explicit command in `[tools].complexity` (used verbatim).
2. A project-adopted standalone complexity analyzer already declared or vendored.
3. Configured GolangCI-Lint complexity linters, when the project runs it.
4. Otherwise, report an explicit limitation — do not install a tool.

## Pinning for comparison

- Record the selected analyzer, its version, and its exact configuration.
- Reuse that pinned analyzer, version, and configuration for the after
  measurement so before/after values are like-for-like.
- If the analyzer or configuration must change mid-task, restate the baseline
  under the new pin before comparing; never compare across pins.

## Degradation

- `off` disables the dimension; report it as not measured.
- An unavailable `auto` analyzer is a limitation, not a silent skip. When
  `complexity.mode` is `required`, the missing analyzer blocks the dimension;
  otherwise analysis continues and reports the gap.
