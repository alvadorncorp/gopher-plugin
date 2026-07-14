# Optional and Fallible Value Patterns

Keep configuration options, optional values, and fallible results as three
separate problem families.

| ID | Meaning | Select when | Direct baseline / counter-signal | Liabilities |
|---|---|---|---|---|
| `pattern.optional-value` | Transport presence or absence. | Absence is a domain value and must compose or cross a boundary. | A language-native `(value, present)`/nullable result is already explicit. | Nested optionals and lost absence reason. |
| `pattern.result` | Transport success or failure. | Failure is expected, typed, and must be inspected or composed. | A language-native error return/exception contract is sufficient. | Wrapper ceremony and ignored error branches. |
| `pattern.generic-option` | Generic wrapper for optional presence. | Domain/interoperability evidence requires a first-class value. | Native presence result is clearer at ordinary lookups. | Ecosystem mismatch and conversion churn. |
| `pattern.generic-result` | Generic wrapper for success/failure. | A pipeline/interoperability contract genuinely needs a value container. | Native error conventions preserve tooling and call-site clarity. | Parallel error protocol and stack/cause loss. |

Validation must cover presence, absence, success, failure, serialization (when
applicable), and caller ergonomics. A language owner selects the native form.
