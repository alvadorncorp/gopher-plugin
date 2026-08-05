# Pointer-Passing Rules

The garbage collector moves and reclaims Go memory, and it cannot see pointers
stored in C memory. The cgo pointer-passing rules exist so that both properties
stay safe across the boundary. State the rule that applies to every pointer that
crosses.

## The rules

1. Go code may pass a Go pointer to C, and the pointed-to memory stays valid for
   the duration of the call.
2. C code may use that pointer only until the call returns. Retaining a copy
   after the return is outside the rules.
3. Go memory passed to C must itself be free of Go pointers. The relevant memory
   is the whole object the pointer identifies: for a pointer to a struct field
   it is that field, and for a pointer to a slice element it is the entire
   backing array.
4. A Go function called from C follows the same restriction on what it returns
   and on what C keeps after that function returns.
5. C memory carries none of these restrictions. Go code may hold a C pointer
   indefinitely, and the collector neither moves nor reclaims that memory.

Rule 3 is the one that surprises. A `*C.char` obtained from `C.CString` is C
memory and crosses freely; a `[]byte` crosses because its backing array holds no
pointers; a `[]string`, a `map`, a `chan`, a `func`, an interface value, or a
struct with a pointer field does not cross as Go memory, because the object it
identifies contains Go pointers.

## Choosing the crossing shape

| Need | Shape | Version gate |
|---|---|---|
| C reads the bytes during the call only | Pass the Go pointer directly | Any |
| C keeps the data after the call | Copy into C memory and free it explicitly | Any |
| C keeps an identity and hands it back later | `runtime/cgo.Handle` | Go 1.17 |
| C needs the real Go address stored in C memory | `runtime.Pinner` | Go 1.21 |
| C owns the buffer already | Keep it in C memory | Any |

### `runtime/cgo.Handle`

A handle turns a Go value into an integer token, so no Go pointer crosses at
all. It is the default answer for callback context.

```go
h := cgo.NewHandle(state)        // token, not a pointer
defer h.Delete()                 // releases the entry
C.register(C.uintptr_t(h))       // C stores the token
```

The C side stores the token as `uintptr_t` and passes it back; the Go side
recovers the value with `h.Value()`. The handle stays valid until `Delete`, and
every `NewHandle` needs exactly one `Delete` or the referenced value leaks.

### `runtime.Pinner`

Pinning keeps a Go object at a fixed address and alive until it is released, so
its address may be stored in C memory or inside Go memory passed to C.

```go
var pinner runtime.Pinner
pinner.Pin(obj)
defer pinner.Unpin()
```

Pinning applies per object. An object that is pinned may itself contain Go
pointers, but each referenced object that C will dereference needs its own
`Pin`. Keep the pinned window as short as the C retention requires, because a
pinned object constrains the collector for as long as the pinner lives.

## Detection with `cgocheck`

The runtime enforces a cheap subset of the rules at each crossing, and a build
experiment enables the expensive full check. Both raise detection; neither is a
place to trade away safety.

| Setting | Scope | What it catches |
|---|---|---|
| `GODEBUG=cgocheck=1` (default) | Every cgo call | A Go pointer passed to C whose object contains Go pointers, and a Go pointer written into non-Go memory |
| `GOEXPERIMENT=cgocheck2` (build time, Go 1.21 and newer) | Every write of a pointer into memory | Go pointers stored into C memory anywhere, at a large runtime cost |

Before Go 1.21 the expensive mode was selected with `GODEBUG=cgocheck=2`; from
Go 1.21 it is a build experiment instead. Confirm the form against the project's
declared Go version before recommending a command.

| Detection message | Meaning | Remediation |
|---|---|---|
| `cgo argument has Go pointer to unpinned Go pointer` | Rule 3: the passed object contains a Go pointer that is neither pinned nor removed | Copy into C memory, use a handle, or pin the referenced object |
| `cgo argument has Go pointer to Go pointer` | The same violation, in the wording used before pinning existed | The same remediation |
| `cgo result has Go pointer` | Rule 4: an exported Go function returned a Go pointer to C | Return a handle or C memory instead |
| `cgo argument has Go pointer to unallocated memory` | The pointer does not identify a live Go object | Fix the pointer arithmetic or the conversion that produced it |
| `Go pointer stored into non-Go memory` | A Go pointer was written into C memory | Store a handle, or pin the object for the retention window |

Each detection names a real defect in ownership or lifetime. Lowering the check
level removes the report and leaves the defect, so the remediation is always the
ownership or lifetime change the message points at.
