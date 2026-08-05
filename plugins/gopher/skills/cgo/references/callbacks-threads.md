# Callbacks, Threads, and Blocking Calls

A call into C leaves the Go scheduler's control. A callback from C re-enters it.
Both directions have thread and stack consequences that belong in the boundary
document.

## Exporting a Go function

`//export` makes a Go function callable from C. The directive sits immediately
above the function, with no blank line, and the generated declaration appears in
`_cgo_export.h`.

```go
//export onEvent
func onEvent(ctx C.uintptr_t, code C.int) {
	state := cgo.Handle(ctx).Value().(*Session)
	state.handle(int(code))
}
```

A file that uses `//export` may declare things in its preamble but may not
define them, because the preamble is copied into two generated compilation
units. Keep C function bodies and variable definitions in a separate `.c` file
in the same package.

## Callback registration pattern

1. The Go side creates the context value and wraps it: `h := cgo.NewHandle(s)`.
2. The Go side registers a C trampoline plus the token: the trampoline is a
   plain C function whose body calls the exported Go function.
3. C invokes the trampoline, which calls back into Go with the token.
4. The Go side recovers the value with `cgo.Handle(tok).Value()`.
5. Deregistration happens before `h.Delete()`, so no in-flight callback can
   observe a deleted handle.

Passing a Go function value or a Go pointer as the C callback context is outside
the pointer rules. The token indirection is what makes the pattern legal, and it
also gives deregistration a single, checkable release point.

A callback that runs on a C-created thread enters Go on a thread the runtime has
not seen before. The runtime adopts that thread for the duration of the call,
which costs a thread-state setup on each entry; a hot callback benefits from a
thread that stays adopted rather than one created per event.

## Thread affinity and locked OS threads

| Situation | Requirement |
|---|---|
| The C library keeps state in thread-local storage | The goroutine holds `runtime.LockOSThread` for the whole session |
| The C library requires the process main thread, as many UI toolkits do | `runtime.LockOSThread` in an `init` of the main package, and the affected work runs on `main` |
| The C library requires the same thread for create, use, and destroy | One goroutine owns the whole lifecycle, locked for its duration |
| The C library is thread-agnostic and reentrant | No lock; document the assumption so it is rechecked on upgrade |

`runtime.LockOSThread` binds the calling goroutine to its OS thread until a
matching `runtime.UnlockOSThread`. A goroutine that exits while still locked
takes the thread with it, which is the intended behavior for a dedicated worker
and a thread leak for a short-lived one. Pair the lock and unlock in the same
function, and keep the locked goroutine free of unrelated work, because nothing
else can run on that thread meanwhile.

Goroutine and synchronization mechanics beyond this affinity question belong to
`gopher:concurrency`.

## Stacks

Go executes C code on a system stack rather than on the goroutine's growable
stack. Two consequences follow:

- Deep or large-frame C code can exhaust the system stack, and the failure looks
  like a crash inside C rather than a Go stack-growth message.
- A callback into Go runs on a goroutine stack again, so Go code invoked from C
  keeps normal growth behavior.

Record the stack expectations of any C library that recurses, uses large
automatic buffers, or documents a minimum stack size.

## Blocking C calls and the scheduler

A goroutine inside a C call holds an OS thread for the whole call. The runtime
detects a call that stays in C, retakes the processor, and lets other goroutines
run on another thread. The consequences to state in the boundary document:

- Concurrent blocking crossings create concurrent OS threads, roughly one per
  in-flight call, rather than multiplexing onto `GOMAXPROCS` threads.
- Thread count is bounded. The default maximum is 10000 threads, adjustable with
  `runtime/debug.SetMaxThreads`, and exceeding it terminates the process.
- Threads created for blocking calls are not returned aggressively, so a burst
  leaves a raised steady-state thread count.
- A blocking call that ignores context cancellation makes the surrounding Go
  timeout advisory only. Prefer a C API with its own cancel or timeout, and
  bound concurrency at the boundary when none exists.

Bound the number of concurrent blocking crossings explicitly when the C API has
no internal limit, and state that bound alongside the call in the boundary
document.

## Signals

The Go runtime installs handlers for the signals it needs, including the
profiling and preemption signals. A C library that installs its own handlers
interacts with that:

- A library that saves and chains the previous handler cooperates correctly.
- A library that replaces a runtime handler without chaining can break
  preemption, profiling, or crash reporting.
- Handlers the runtime installs use an alternate signal stack; a C library that
  installs handlers on threads it created should preserve that arrangement.
- A C thread that has not entered Go yet may receive signals with no Go handler
  installed, so crash behavior differs between adopted and unadopted threads.

When profiles must include C frames, `runtime.SetCgoTraceback` supplies the
unwinder the runtime uses for C stacks. Treat its absence as a known limitation
of any profile taken across the boundary.
