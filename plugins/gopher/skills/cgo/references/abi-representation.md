# ABI and Representation

The `C` pseudo-package is a compile-time view of the preamble, not a runtime
package. Every crossing type needs an explicit mapping, an explicit size, and an
explicit conversion. Write the mapping down before writing the call.

## Scalar mapping

| C type | cgo type | Notes |
|---|---|---|
| `char` | `C.char` | Signedness is platform-defined; `C.schar` and `C.uchar` are explicit |
| `short`, `unsigned short` | `C.short`, `C.ushort` | |
| `int`, `unsigned int` | `C.int`, `C.uint` | Typically 32-bit; Go `int` is typically 64-bit |
| `long`, `unsigned long` | `C.long`, `C.ulong` | 32-bit on Windows and on 32-bit targets, 64-bit on most 64-bit Unix targets |
| `long long` | `C.longlong`, `C.ulonglong` | |
| `float`, `double` | `C.float`, `C.double` | |
| `size_t`, `ssize_t` | `C.size_t`, `C.ssize_t` | Width follows the target |
| `ptrdiff_t`, `intptr_t`, `uintptr_t` | `C.ptrdiff_t`, `C.intptr_t`, `C.uintptr_t` | |
| `void *` | `unsafe.Pointer` | Carries no ownership information |
| `T *` | `*C.T` | The pointee keeps C ownership semantics |

Treat `C.int` and Go `int` as different types with different widths. Convert at
the boundary with an explicit range check when the Go value can exceed the C
width, and convert back the same way on return.

## Structs, alignment, and padding

A C `struct foo` is `C.struct_foo`; `union bar` is `C.union_bar`; `enum baz` is
`C.enum_baz`. A field whose C name collides with a Go keyword gains a leading
underscore. cgo reproduces the C layout, so padding and alignment come from the
target ABI rather than from Go's own struct rules.

Verify layout assumptions rather than assuming them:

```go
fmt.Println(unsafe.Sizeof(s), unsafe.Alignof(s), unsafe.Offsetof(s.field))
```

Record size, alignment, and each offset in the boundary document when the C
side and the Go side both construct the struct. A field reordering on either
side changes the ABI silently, so keep one side authoritative and derive the
other from the header.

## Strings and byte slices

| Direction | Call | Allocates in | Released by |
|---|---|---|---|
| Go string to C string | `C.CString(s)` | C heap | `C.free(unsafe.Pointer(p))` |
| Go bytes to C buffer | `C.CBytes(b)` | C heap | `C.free(unsafe.Pointer(p))` |
| C string to Go string | `C.GoString(p)` | Go heap (copy) | Garbage collector |
| C string with length | `C.GoStringN(p, n)` | Go heap (copy) | Garbage collector |
| C buffer to Go bytes | `C.GoBytes(p, n)` | Go heap (copy) | Garbage collector |

`C.CString` appends the terminating NUL and rejects nothing, so a Go string
containing an interior NUL crosses as a truncated C string. Validate before
converting when the payload is untrusted. The `C.Go*` conversions copy, so the
resulting Go value stays valid after the C buffer is released.

In this toolchain `C.malloc` never returns nil: an allocation failure aborts the
process instead. Treat a size computed from untrusted input as a validation
requirement rather than an allocation that can fail gracefully.

## Arrays and slices

A C array inside a struct becomes a Go array of the same length, which copies
by value on assignment. A pointer plus a length becomes a Go slice only through
an explicit construction:

```go
s := unsafe.Slice((*C.uchar)(p), n) // Go 1.17 and newer
```

The resulting slice aliases C memory. It stays valid exactly as long as that
allocation does, and it is not managed by the garbage collector. When the value
must outlive the C allocation, copy it with `C.GoBytes` instead.

## Cases cgo cannot express

| Case | Effect | Boundary response |
|---|---|---|
| Bitfields | The field is absent from the Go struct | Add accessor functions in C |
| Unions | Exposed as a byte array of the union size | Decode in C, or reinterpret behind a documented invariant |
| Incomplete (opaque) types | Usable only as `*C.struct_foo`, never as a value | Keep the handle opaque and allocate through the library |
| Variadic functions | Not callable directly | Wrap with a fixed-arity C function |
| Function-like macros | Not visible as functions | Wrap with a static C function in the preamble |
| C++ symbols | Outside the cgo mapping | Expose an `extern "C"` wrapper layer |
| Static inline functions | Availability varies by toolchain | Provide a non-inline wrapper for stability |

Every wrapper added for these cases becomes part of the boundary and inherits
the same ownership, lifetime, and pointer obligations as a native call.
