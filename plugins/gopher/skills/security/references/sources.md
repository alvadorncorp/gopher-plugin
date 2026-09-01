# Official Security Sources

| Topic | Source | Last verified |
|---|---|---|
| Go vulnerability management | <https://go.dev/security/vuln/> | 2026-07-14 |
| `govulncheck` | <https://go.dev/doc/tutorial/govulncheck> | 2026-07-14 |
| Fuzzing | <https://go.dev/doc/fuzz/> | 2026-07-14 |
| Race detector | <https://go.dev/doc/articles/race_detector> | 2026-07-14 |
| TLS configuration | <https://pkg.go.dev/crypto/tls> | 2026-07-14 |
| Cryptographic randomness | <https://pkg.go.dev/crypto/rand> | 2026-07-14 |
| Filesystem paths | <https://pkg.go.dev/path/filepath> | 2026-07-14 |
| HTTP client/server | <https://pkg.go.dev/net/http> | 2026-07-14 |
| `GODEBUG` history and removals | <https://go.dev/doc/godebug> | 2026-08-31 |
| Post-quantum signatures (ML-DSA) | <https://pkg.go.dev/crypto/mldsa> | 2026-08-31 |
| FIPS 140-3 module status | <https://go.dev/doc/security/fips140> | 2026-08-31 |
| JSON v2 defaults and options | <https://pkg.go.dev/encoding/json/v2> | 2026-08-31 |
| Go 1.27 release notes | <https://go.dev/doc/go1.27> | 2026-08-31 |

Confirm every version-sensitive detail against the Go toolchain the target
project declares; these pages track the current release. Re-verify after every
stable Go release and at least quarterly; `references/go-risk-catalog.md`
carries the controls that moved in the release it names. Add third-party
sources only when the project adopts the related tool.
