# Complexity Lens

Review cyclomatic complexity, cognitive complexity, function and file size, and
maintainability signals in the changed code. Compare against the thresholds the
project declares in `.gopher-plugin.toml`, and separate a threshold violation
from a regression against the prior measurement.

This lens does not cover asymptotic time or space complexity, which belongs to
the `performance` lens. A subjective preference for shorter functions without a
threshold or a measured regression is not a finding.

Route measurement, hotspot ranking, and reduction plans to `gopher:complexity`,
the local reversible reduction to `gopher:developer`, and any boundary or
public-contract change to `gopher:architecture`. An unavailable analyzer is an
explicit limitation, not a silent skip.
