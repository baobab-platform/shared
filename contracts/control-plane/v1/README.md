# Control Plane v1 contracts — implementation and ownership

**Owner:** baobab-platform/shared · This directory is the canonical published
interface. The Control Plane API is a *consumer/implementer*, not a schema owner.

## Dataset-operation contract (CX-05)

- [`openapi.yaml`](openapi.yaml) describes concrete `/admin/datasets`
  routes: preview, propose, read immutable review receipt, independently
  approve, execute, and auditable CSV download.
- [`console-dataset.schema.json`](console-dataset.schema.json) defines the
  bounded, closed DTOs: `PreviewRequest`, `PreviewResponse`,
  `ProposalRequest`, `DecisionRequest`, `Receipt` and `ReviewReceipt`.
- [`../../administration/v1/permission-registry.yaml`](../../administration/v1/permission-registry.yaml)
  specifies exact, independently held organisation-scoped export, proposal
  and approval grants. Permissions cannot be inferred from group affiliation.

| Contract operation | CP responsibility | No-go |
| --- | --- | --- |
| Preview | Current authorised redacted rows and source version | Raw provider registration/evidence; caller-supplied principal |
| Propose | Immutable source/targets/purpose/recipient/TTL, durable idempotency | Export rights inferred from `organisation.view` |
| Read review receipt | Independently scoped checker sees full immutable proposal | Approval of an opaque digest |
| Approve | Different authorised human, current assurance and audit | Maker self-approval or stale rights |
| Execute | Source/revision revalidation, atomic commit | Partial bulk writes or replaying a completed mutation |
| Download | Redacted, bounded, freshly authorised audited CSV | Plaintext artifact storage, cross-organisation access |

The Shared interface is **not** evidence that the provider supports live
operations. CP must preserve the nonproduction feature gate until IAM sessions,
independent maker/checker, source verification, database migration, encryption,
retention, and protected live staging tests have passed.

## How to publish a contract change

1. Change Shared OpenAPI and JSON Schema together, with relevant
   administrative permissions and regression fixtures.
2. CI must validate shape and backwards compatibility; merge the approved
   Shared PR.
3. In each consumer, move its explicit Shared commit pin and embedded copy,
   regenerate typed clients, and validate client and handler drift.
4. Add a consumer route, persistence and negative-permission tests.
5. Update the consumer README, operation runbook and rationale comments.
6. Independently demonstrate authenticated staging acceptance before calling
   the capability production-ready.

A schema is not an implementation. A green consumer unit test is not
equivalent to deployed, issuer-authenticated E2E evidence.

## Documentation comments

Security-critical runtime code needs comments explaining _why_ a condition
must fail closed (ACR, scope, revocation, version, idempotency, key choice).
Exported Go symbols should have GoDoc; JS/TS public helper entry points should
have short JSDoc. Avoid narrating obvious assignments or using comments as a
substitute for tests.
