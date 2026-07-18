# Complexity metrics

Measure the configured package scope and report each metric the selected
analyzer supports. Report only values the selected analyzer produces.

## Metrics

- Cyclomatic complexity: independent paths through a function. Compare against
  `complexity.cyclomatic_max`.
- Cognitive complexity: how hard a function is to follow (nesting, breaks in
  linear flow). Compare against `complexity.cognitive_max`, where supported.
- Function size: lines per function, against `complexity.function_lines_max`.
- File size: lines per file, against `complexity.file_lines_max`.
- Maintainability: a composite signal, against `complexity.maintainability_min`.

## Threshold violation versus baseline regression

- A threshold violation is a value past a configured maximum or minimum in the
  measured scope.
- A baseline regression is a value that worsened versus the prior measurement of
  the same scope, even when still inside the threshold.
- Report the two independently. A legacy project may hold many pre-existing
  violations; the gate for a change is that the measured scope maintains or
  improves its baseline, not that every value already meets target.

## Like-for-like comparison

Use the same analyzer, configuration, command, and tool version for the before
and after measurement. Record all four. A comparison across different tools or
configurations is not evidence and must be reported as such.
