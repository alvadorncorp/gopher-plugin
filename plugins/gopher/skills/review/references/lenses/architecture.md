# Architecture Lens

Review dependency direction, package/module/internal boundaries, public and
internal surface, interface seams, migration safety, ADR constraints, and
speculative abstractions. Compare the diff to existing ownership and approved
decisions; identify concrete cycles, forbidden edges, compatibility breaks, or
unnecessary boundary growth.

Folder preference without a demonstrated risk is not a finding. Route structural
fixes to `gopher:architecture` and conceptual application-boundary questions to
`gopher:application-architecture`. Hand public-API or module-topology
modernization findings to `gopher:modernize`, which routes contract-changing
work back to `gopher:architecture`.
