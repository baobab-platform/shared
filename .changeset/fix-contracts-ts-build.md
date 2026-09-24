---
"@baobab-platform/contracts-ts": patch
---

Fix the package build. The entry point imported the generated health contract
from `generated/baobab-platform/...`, but buf writes it under
`generated/baobab_platform/...` (the proto package is `baobab_platform.shared.v1`),
so the build could not resolve it. Type declarations are now emitted with
`tsc --emitDeclarationOnly`, as in `@baobab-platform/supplier-domain`, because
tsup's bundled declaration build cannot run on TypeScript 7.
