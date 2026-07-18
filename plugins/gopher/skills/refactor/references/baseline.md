# Immutable baseline and recovery

The baseline is the fixed reference every dimension measures against and every
mutating phase returns to. Capture it once, before any change.

## Capture

Record before the first mutation:

```yaml
source_commit:
working_tree_diff:
config_path_state_hash:
effective_values:
selected_packages_modules:
selected_dimensions:
baseline_build:
baseline_tests:
metric_baselines:
```

Use a concrete source commit. A passing build and test run is the baseline gate;
a failing baseline permits analysis but blocks mutation until it is restored.

## Per-phase evidence

Each mutating phase records its own starting diff, exact commands, tool names and
versions, and results. A phase begins only from a passing state.

## Recovery at phase boundaries

- Recovery happens at phase boundaries, not mid-phase.
- A failed phase stops all subsequent mutations, preserves unrelated user work,
  and reports the last passing boundary.
- Re-measurement after a phase uses the same method and tool versions as the
  baseline, so before/after values are comparable.
