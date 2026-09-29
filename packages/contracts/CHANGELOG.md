# @baobab-platform/contracts-ts

## 0.1.0

### Minor Changes

- 43514d8: Remove `CanonicalMappingResolver` and its types (`ResolutionInput`, `Mapping`,
  `MappingScope`, `ResolutionResult`, `ResolutionFailure`). It resolved mappings
  against a context its caller supplied, which ADR-SHARED-014 forbids: mapping
  resolution is the Control Plane's `resolveMapping`, which redeems a stored
  context by `context_id`. `ResolutionContext` moves to `context-resolver`.

## 0.0.1

### Patch Changes

- f62a697: Fix the package build. The entry point imported the generated health contract
  from `generated/baobab-platform/...`, but buf writes it under
  `generated/baobab_platform/...` (the proto package is `baobab_platform.shared.v1`),
  so the build could not resolve it. Type declarations are now emitted with
  `tsc --emitDeclarationOnly`, as in `@baobab-platform/supplier-domain`, because
  tsup's bundled declaration build cannot run on TypeScript 7.
