# Tests Lens

Review whether tests prove changed behavior with independent expected values.
Cover success, absence, errors, boundaries, compatibility, and regression
scenarios. Identify tautological assertions, implementation-coupled tests,
missing essential coverage, nondeterminism, and inappropriate mocks.

Recommend race, fuzz, benchmark, or integration coverage only when the changed
risk justifies it. A missing essential test is `important`; optional confidence
or maintainability coverage is `minor`. Route fixes to the implementation owner.
