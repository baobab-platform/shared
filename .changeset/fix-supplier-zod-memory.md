---
"@baobab-platform/supplier-domain": patch
---

Raise the minimum Zod version to 4.6.6 to address GHSA-mrhx-c7xc-m3w5
(oversized collection validation can exhaust memory). Refresh the workspace
lockfile using the existing pnpm 11.24.0 toolchain.
