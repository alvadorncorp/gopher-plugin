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

## Controls that moved in Go 1.27

A toolchain upgrade changes controls without a code change. Each entry below is
a question to re-ask, not a finding.

| Change | Family | What to re-ask |
|---|---|---|
| Seven GODEBUGs removed — `tlsrsakex`, `tls3des`, `tls10server`, `tlsunsafeekm`, `x509keypairleaf`, `asynctimerchan`, `gotypesalias` — and an old value now fails the build | Crypto, randomness, TLS | Which weakness was the pin holding open, and does removing it break a peer the project must still reach? |
| `SSL_CERT_FILE` and `SSL_CERT_DIR` are honored on macOS and Windows, and setting either **prevents the platform verification API from being used** unless `x509sslcertoverrideplatform=0` | Crypto, randomness, TLS | Can anything in the deployment environment set those variables, and would that silently replace the trust anchors and disable platform verification? |
| `crypto/mldsa` implements ML-DSA (FIPS 204); `crypto/x509` accepts `*mldsa.PublicKey` and `*mldsa.PrivateKey` | Crypto, randomness, TLS | Is a post-quantum signature actually required, and is the FIPS 140-3 module constraint acceptable — the package is unavailable under Go Cryptographic Module v1.0.0? |
| `MLKEM1024` joins the hybrid key exchanges; defaults already carry `X25519MLKEM768` (Go 1.24) and `SecP256r1MLKEM768` / `SecP384r1MLKEM1024` (Go 1.26) | Crypto, randomness, TLS | Does the project disable them with `tlsmlkem=0` or `tlssecpmlkem=0`, and is that still justified? |
| `crypto/tls` `Config.Rand` is deprecated: "this should be left nil in production" | Crypto, randomness, TLS | Is a custom `Rand` set outside tests, and can it move to `testing/cryptotest.SetGlobalRandom`? |
| `runtime/pprof` goroutine labels appear in tracebacks by default (`tracebacklabels`, default flipped to on) | Secrets, logs, and errors | Does any label carry a tenant, account, or request attribute that must not reach a panic log? |
| `http.Server.MaxHeaderValueCount` with `DefaultMaxHeaderValueCount = 500` | Resource exhaustion | Is the default appropriate for this service, and does a legitimate client send more values than it allows? |
| `encoding/json/v2` rejects invalid UTF-8 and duplicate object names by default, where v1 replaced and allowed them | Inputs, parsing, serialization | Does anything relax that with `jsontext.AllowInvalidUTF8` or the duplicate-name option, reopening a parser-confusion gap between the project and a peer parser? |

The duplicate-name and invalid-UTF-8 defaults are a real hardening, not a
formality: two parsers disagreeing about which duplicate wins, or one silently
substituting the replacement character, is how an authorization decision and the
data it authorized come apart.
