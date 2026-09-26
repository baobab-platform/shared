---
"@baobab-platform/contracts-ts": minor
---

Remove `CanonicalMappingResolver` and its types (`ResolutionInput`, `Mapping`,
`MappingScope`, `ResolutionResult`, `ResolutionFailure`). It resolved mappings
against a context its caller supplied, which ADR-SHARED-014 forbids: mapping
resolution is the Control Plane's `resolveMapping`, which redeems a stored
context by `context_id`. `ResolutionContext` moves to `context-resolver`.
