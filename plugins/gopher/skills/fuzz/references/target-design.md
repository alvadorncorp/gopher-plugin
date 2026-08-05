# Target design

A fuzz target is a hypothesis about a function plus a check that can fail. The
design work is choosing the function, writing the invariant, and finding an
oracle that is independent of the code being exercised.

## Choosing the function under test

The natural candidates take untrusted or highly variable input and carry a
non-trivial decision tree.

| Candidate | Why it pays off | Typical invariant |
|---|---|---|
| Parser (`Parse`, `Unmarshal`, `Scan`) | Grammar edge cases multiply faster than hand-written cases. | Structural, no panic, bounded output |
| Decoder or wire-format reader | Length prefixes, offsets, and padding produce arithmetic edges. | No panic, bounded allocation |
| Encoder plus decoder pair | The pair already contains its own oracle. | Round-trip |
| State machine or protocol driver | Input order matters, and the reachable state space is large. | Metamorphic, structural |
| Normalizer, sanitizer, or escaper | Idempotence and containment are easy to state and easy to break. | Metamorphic, differential |
| Replacement for a trusted implementation | A reference implementation is available for comparison. | Differential |

A pure function of its input, deterministic, and fast enough to execute tens of
thousands of times per second gives the campaign the most exploration per
second of budget. Functions that reach the network, the clock, or global state
belong behind a seam first; route that seam work to `gopher:developer`.

## Writing a falsifiable invariant

A usable invariant states a property that a concrete input can violate, in
terms the test can evaluate.

- Falsifiable: "decoding an encoded value returns the original value".
- Not falsifiable: "the parser behaves correctly".

Write the invariant before the campaign starts. An invariant written after a
crash tends to describe the crash rather than the property, and it stops
detecting the next defect in the same family.

## The independent-oracle requirement

The oracle is whatever decides pass or fail for a generated input. It stays
independent of the function under test.

- A second implementation of the same algorithm, written from the same
  assumptions, reproduces the same mistakes and agrees with the defect.
- A trusted external implementation, an inverse operation, a stricter
  post-condition, or a relation between two calls are all independent.
- Standard-library behavior, a specification, or a previous released version are
  usable trusted references when the project already depends on them.

When no independent oracle exists, the honest target checks structural
properties only: absence of a panic, bounded output size, bounded allocation, or
termination. That is still a real target, and reporting it as structural keeps
the conclusion accurate.

## The four durable invariant families

| Family | Statement | Failure means |
|---|---|---|
| Round-trip | `decode(encode(x))` equals `x`, or `parse(format(v))` equals `v` | The pair disagrees about the format |
| Differential | The function and a trusted implementation agree on every input | One of the two is wrong on that input |
| Metamorphic | A transformation of the input changes the output in a stated way, including idempotence, order independence, and monotonicity | The stated relation is broken |
| Structural | No panic, no unbounded allocation, no infinite loop, output within declared bounds | The function fails on shapes it accepts |

Round-trip is the most productive family for encoders and decoders.
Differential is the strongest when a trusted reference exists. Metamorphic
covers functions with no inverse and no reference. Structural is the fallback
that still catches the largest class of reachable crashes.

## The `testing.F` shape

A fuzz target lives in a `_test.go` file, is named `FuzzXxx`, takes exactly one
`*testing.F`, and calls `f.Fuzz` exactly once.

```go
func FuzzRoundTrip(f *testing.F) {
    f.Add("key=value")          // seed from a real, sanitized input
    f.Add("")                   // seed from a previously fixed failure
    f.Fuzz(func(t *testing.T, in string) {
        v, err := Parse(in)
        if err != nil {
            t.Skip()            // reject the input instead of asserting on it
        }
        again, err := Parse(Format(v))
        if err != nil {
            t.Fatalf("re-parse of formatted value failed: %v", err)
        }
        if !reflect.DeepEqual(v, again) {
            t.Fatalf("round-trip mismatch: %#v != %#v", v, again)
        }
    })
}
```

The arguments of the `f.Fuzz` function after `*testing.T` define the target's
signature; every `f.Add` call supplies values of exactly those types in the same
order.

## Supported seed types

The fuzzing engine mutates these types only: `[]byte`, `string`, `bool`,
`byte`, `rune`, `int`, `int8`, `int16`, `int32`, `int64`, `uint`, `uint8`,
`uint16`, `uint32`, `uint64`, `float32`, and `float64`.

A richer input is built inside the target from these primitives: derive a
struct, a slice length, or an enum choice from a `[]byte` or from an `int`
reduced into range. Keep that derivation deterministic, so a recorded failing
input replays to the same value.
