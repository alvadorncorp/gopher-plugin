# Ownership and Lifetime

Two allocators meet at the boundary. The garbage collector owns Go memory and
releases it when it becomes unreachable. The C allocator owns C memory and
releases it only when some code calls the matching release function. Every
value that crosses names one owner on each side and one release moment.

## Allocation and release pairing

| Allocated by | Released by | Release moment |
|---|---|---|
| `C.CString`, `C.CBytes`, `C.malloc` | `C.free` | The call site that allocated it, usually a `defer` |
| A library constructor such as `foo_new` | The library's own `foo_free` | The documented teardown call |
| A library accessor returning an internal pointer | The library, on its own schedule | Never freed by the caller; copy before the owner mutates |
| Go `make`, `new`, literals | Garbage collector | When the value becomes unreachable |
| `C.GoString`, `C.GoBytes` results | Garbage collector | Copies, independent of the C buffer |

Pair the allocation and the release in the same function whenever the lifetime
permits:

```go
cs := C.CString(s)
defer C.free(unsafe.Pointer(cs))
```

A library that documents its own release function keeps that function. Calling
`C.free` on memory a library allocated through a different allocator is a heap
corruption, not a portable shortcut.

## Lifetime longer than the call

When C keeps a value after the call returns, choose one of these shapes and
record which one the boundary uses.

| Shape | Mechanism | Cost | Fits when |
|---|---|---|---|
| Copy into C memory | `C.CBytes`, `C.CString`, or `C.malloc` plus `memcpy` | One copy, one explicit free | The payload is data, not identity |
| Pass identity through a handle | `runtime/cgo.Handle` (Go 1.17 and newer) | A map entry until `Delete` | C stores a token and calls back with it |
| Pin the Go object | `runtime.Pinner` (Go 1.21 and newer) | Pinned memory until `Unpin` | C needs the actual Go address for a bounded window |
| Keep ownership in C | The library allocates and frees | The library's own rules | The library already owns the buffer |

Record the release path with the shape. A handle that is never deleted is a
leak of the Go value it names; a pinner that is never unpinned holds the object
and its pinning state for the life of the pinner.

## Ownership table for the boundary

Fill one row per value that crosses. This table is the deliverable of the
`design` and `audit` modes.

| Value | Direction | Allocated by | Released by | Valid until | Crossing rule |
|---|---|---|---|---|---|
| | Go to C / C to Go | | | | Call-scoped / copied / handle / pinned |

A row with an empty releaser is a leak. A row whose validity window is shorter
than its use is a use-after-free. Both are findings, and both are resolved by
changing the ownership or the lifetime rather than by relaxing a check.

## Finalizers and cleanups

`runtime.SetFinalizer` attaches a function that may run after an object becomes
unreachable. It is a backstop, never a release plan, for these reasons:

- Execution is not guaranteed. A program that exits, or an object still live at
  exit, leaves the finalizer unrun.
- Timing is unpredictable. The release happens at some later collection, so a
  scarce resource such as a file descriptor or a lock stays held meanwhile.
- Reachability is subtle. A pointer held in C memory is invisible to the
  collector, and a self-reference or a cycle involving the finalized object
  prevents the finalizer from running at all.
- The finalizer goroutine is shared. A finalizer that blocks stalls every other
  pending finalizer.
- Resurrection is possible. A finalizer that stores the object somewhere
  reachable revives it, and the finalizer does not run again unless it is set
  again.

Prefer an explicit `Close` or `Release` method with a `defer` at the owning call
site, and make double release safe. Projects on Go 1.24 or newer can use
`runtime.AddCleanup`, which attaches to a pointer without the self-reference
hazard and allows more than one cleanup per object; the guarantees about timing
and about running at all stay the same.

Keep `runtime.KeepAlive` in mind for the opposite hazard: a Go object whose last
Go-visible use ends before the C call finishes can be collected while C still
reads through a field pointer. `runtime.KeepAlive(obj)` after the call states
the required liveness explicitly.
