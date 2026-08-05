# Seeds and corpora

Seeds decide where the campaign starts. A campaign seeded with realistic inputs
reaches interesting code paths in seconds; a campaign seeded with an empty
string spends its budget rediscovering the grammar.

## Where seeds come from

| Source | Why it earns a place | Handling |
|---|---|---|
| Real production-shaped inputs | They exercise the paths the code actually serves. | Sanitize before committing |
| Previously fixed failures | They keep a closed defect closed. | Commit as regression seeds |
| Specification examples | They cover the format's declared corners. | Cite the specification section |
| Existing table-test cases | They already encode the team's understanding. | Reuse verbatim |
| Boundary values | Empty, single element, maximum length, invalid UTF-8, and the largest accepted numeric value. | Add explicitly |

Aim for a small, diverse seed set. Twenty structurally different seeds explore
more than two hundred near-duplicates, and every seed is replayed on every run,
so the set is also a fixed cost on each campaign.

## The two corpora

Go fuzzing keeps two distinct corpora, and they behave differently.

| Corpus | Location | Lifetime | Version control |
|---|---|---|---|
| Seed corpus | `f.Add` calls plus `testdata/fuzz/<FuzzTarget>/` | Permanent | Checked in |
| Cache corpus | `fuzz` subdirectory of `go env GOCACHE` | Machine-local, grows during campaigns | Left out of version control |

The seed corpus runs during a plain `go test`, which is what makes a promoted
failing input act as a regression test. The cache corpus holds inputs the engine
found interesting during a campaign; it accelerates later runs on the same
machine and is cleared with `go clean -fuzzcache`. Treat a result that depends
on the cache corpus as machine-local, and reproduce it from the seed corpus
before reporting it.

When a campaign finds a failing input, the engine writes that single input into
`testdata/fuzz/<FuzzTarget>/` next to the test file, using a content-derived
file name. That file is a candidate for promotion, not yet a promoted
regression; `references/promotion.md` covers the difference.

## Corpus file format

Each file holds one input for one target. The first line is the format version,
and each following line is one argument of the `f.Fuzz` function, in order, as a
type-qualified Go literal.

```text
go test fuzz v1
string("key=value")
int(17)
```

The argument lines match the fuzz target's signature exactly, in count, order,
and type. `[]byte` values are written as `[]byte("...")` with escapes, so a
binary seed stays a plain reviewable text file.

Files are added by hand as well as by the engine. A hand-written seed uses the
same format and the same directory, and the file name is free text, so a
descriptive name such as `truncated-length-prefix` reads better in a diff than a
content hash.

## Sanitizing a real-world input

A seed lives in the repository for as long as the target does, so it carries
only data the repository may hold.

1. Identify the fields that carry meaning for the invariant. A parser cares
   about structure, delimiters, lengths, and encodings, seldom about the values.
2. Replace credentials, tokens, keys, signatures, and session identifiers with
   structurally equivalent stand-ins of the same length and character class.
3. Replace names, addresses, contact details, account identifiers, and free-text
   fields with synthetic values of the same shape.
4. Re-run the target on the sanitized seed and confirm it still reaches the code
   path that motivated it. A sanitized seed that no longer reaches that path has
   lost its value and is replaced with a synthetic seed built for the path.
5. Record the provenance in the seed file name or in a short comment next to the
   matching `f.Add`, so a later reader knows what the seed represents.

An input that resists sanitization stays out of the repository. Keep it as a
local reproduction, describe the structure it exercises, and construct a
synthetic seed with the same structure for the checked-in corpus.
