# @baobab-platform/supplier-domain

## 0.2.1

### Patch Changes

- e2acbed: Raise the minimum Zod version to 4.6.6 to address GHSA-mrhx-c7xc-m3w5
  (oversized collection validation can exhaust memory). Refresh the workspace
  lockfile using the existing pnpm 11.24.0 toolchain.

## 0.2.0

### Minor Changes

- 8fe3dfc: Add the initial `@baobab-platform/supplier-domain` package: a generic lifecycle
  state-machine mechanism plus Zod shapes for a supplier organisation, its
  contacts, capabilities, certifications, and status-change audit trail.
  Generalized from baobab-platform/zuribeans' proven supplier-registration vertical
  slice (ADR-0006) so other digital estates (starting with baobab-platform/thamani)
  can adopt the same mechanism instead of duplicating it from scratch.
