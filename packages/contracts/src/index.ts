// Entry point for @baobab-platform/contracts-ts.
//
// Both re-exports below point at generated code that does not exist until
// `pnpm generate` has run (buf generate + graphql-codegen). This file is
// intentionally thin — it should never contain hand-written contract types.
//
// PLACEHOLDER STATE: only the health-check contract exists right now.
// Trade Intelligence / Property Intelligence / BIE exports will be added
// here as their respective .proto/.graphql sources are authored — see
// ADR-0001 for why they are absent from this initial scaffold.

// Canonical Mapping Model implementations (§23-24)
export * from './canonical-mapping-resolver';

// Context Resolution Flow (§17, §22)
export * from './context-resolver';

// Audit Trail and Approval Workflow (§48-49)
export * from './audit-trail';

export * from './generated/baobab_platform/shared/v1/health';
export * from './generated/graphql';