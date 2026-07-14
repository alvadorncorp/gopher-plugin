# Go Security Risk Catalog

Inspect only families relevant to the mapped data flow:

| Family | Evidence questions |
|---|---|
| Inputs, parsing, serialization | Are limits, ambiguity, validation order, and unknown fields appropriate? |
| Authentication and authorization | Is identity bound to every protected action and object? |
| Secrets, logs, and errors | Can credentials, tokens, personal data, or internals cross a sink? |
| Crypto, randomness, TLS | Are algorithms, entropy, nonce/key lifecycle, verification, and transport settings appropriate? |
| Filesystem and archives | Can input control paths, links, permissions, traversal, or overwrite? |
| Subprocesses | Can input affect executable, arguments, environment, or shell interpretation? |
| HTTP and outbound requests | Can input affect hosts, redirects, schemes, headers, or response size (SSRF)? |
| Resource exhaustion | Are body, allocation, concurrency, recursion, and time limits bounded? |
| `unsafe`, cgo, reflection | Are memory/type/build assumptions proven and visible to analysis? |
| Concurrency | Can a race violate authorization, identity, nonce, or secret invariants? |
| Dependencies | Is an advisory reachable through the vulnerable symbol/configuration? |

Treat checklists as coverage prompts, not findings. Every result still needs a
specific path, precondition, control analysis, and impact.
