# Security Data Flow and Reachability

Trace each candidate path in this order:

```text
external/internal source
  -> parse/decode
  -> validation/normalization
  -> authentication/authorization
  -> transformation/storage
  -> filesystem/network/subprocess/crypto/log sink
```

Record file and symbol evidence at each hop, trust transitions, controls,
alternate paths, build tags, and whether the path is reachable in the deployed
configuration. A dependency advisory is a hypothesis until the vulnerable
symbol and an applicable call path are established. A missing control is a
finding only when the security invariant requires it.
