# Federation authority source governance

Accepted ADR-IAM-0026, ADR-IAM-0031 and ADR-IAM-0033 require governed IAM
trust/configuration approval and authoritative CP identity/provider evidence.
This additive vocabulary closes the permission and reference-namespace
prerequisite identified by IAM #66. It implements no grants or deployment.

`security.federation.view/propose/decide/revoke` are canonical administrative
permissions, separate from product capabilities and OAuth transport scopes.
A decision is CRITICAL, independent and non-delegable; Shared's existing
assurance, bounded/JIT grant and grant-issuance separation rules still apply.
Runtime source handlers must use the grants evaluator directly and fail closed,
without the legacy-role fallback of a migration/display policy.

`federation-authority:read` admits workloads to private source reads;
`federation-governance:manage` admits humans to private governance operations.
Neither grants authority. No ACTIVE workload entry or administrative profile is
changed. Deployment must explicitly approve caller-target association and
provision any required grants through existing governed workflows.

The canonical policy is `identity/v1/federation-authority-policy.yaml`.
It binds target purposes to registered `baobab_iam` or `baobab_cp` native
namespaces, engine ownership and exact native types. These are Control Plane
ExternalReferences under the canonical-mapping model, not identity/v1's
engine-person reference. Native target bytes must be immutable and non-secret;
CP registration or a manually imported reference never means approval.
CP retains platform registry, placement, bindings and identity relationships.
IAM retains trust revisions, native configuration, assurance policies and
approval decisions. Approving relationship evidence cannot create, merge or
link a person. No email or provider Organisation creates canonical scope.

Public wire APIs are not added. Existing private source serialization remains
private; endpoint deployment still requires authenticated composition, approved
backends, fresh reference verification, lifecycle checks, replay/revocation
fences and operational acceptance. This contract does not promote MP2-C to
production completion or permit MP7 reduction.
