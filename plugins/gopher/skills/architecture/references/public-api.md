# Go Public API Contracts

Treat these as compatibility surface:

- exported package/type/function/method/field names and signatures;
- interface method sets and satisfaction;
- behavior, error identity, sentinel/typed errors, and zero-value semantics;
- option constructors, ordering, defaults, validation, and nil behavior;
- serialization and generated-code contracts;
- module paths and supported Go versions.

Before change, enumerate consumers and affected call sites. Prefer additive
entry points and deprecation/migration windows. A variadic options parameter,
interface method, or moved package path can be breaking even when code compiles locally.

Public-API or module-topology modernization arrives from `gopher:modernize`;
contract-changing modernization is owned and gated here by `gopher:architecture`.

Source: <https://go.dev/blog/module-compatibility>.
Last verified: 2026-07-14.
