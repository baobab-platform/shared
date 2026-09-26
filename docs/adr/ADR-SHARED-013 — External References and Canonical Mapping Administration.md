# ADR-SHARED-013 — External References and Canonical Mapping Administration

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-26 |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-SHARED-012; Baobab Canonical Mapping Model §§8-9, 23, 26-27 and 46-49; baobab-cp ADR-BCP-018 (ORG-10), ADR-BCP-022 |
| **Applies to** | `baobab-cp` and every administrator or workload that records, relates or resolves native identities |

## Context

The Control Plane stored a local "external reference" that differed from Shared's `externalReference` in four ways:
- it embedded the canonical entity it belonged to;
- it used its own field names;
- it carried free metadata;
- it served a reverse lookup under the resource's own name.

Shared's Mapping operations described a model that could not be administered safely:
- **Server-owned fields were client input.** Creation and change took the whole `mapping` record as the request, including `mapping_id`, `revision` and `created_by`.
- **The actor was self-asserted.** Activation and retirement named their own actor in the body (`approved_by`, `retired_by`).
- **A DRAFT mapping was stranded.** Nothing moved a mapping from DRAFT to VALIDATED.
- **Administrators could not read a mapping.** Reading one was workload-only.
- **The read model contradicted Mapping Model §9.2.** Its `oneOf` let a canonical-to-canonical mapping omit its canonical entity.

## Decision

1. **An ExternalReference records only that a native object exists.** It never names a canonical entity; a Mapping relates the two, within one tenant.
   - `createExternalReference` takes `externalReferenceCreateRequest`. Its (`system_namespace`, `engine_id`) pair must be registered in `external-systems.yaml` (ADR-SHARED-012), and a namespace is never guessed.
   - The Control Plane sets the identifier (`ref_…`), sets `status` to `unverified` until reconciliation verifies it, and sets `source_authority` to `manual-import` for an administrative registration. It sets the timestamps too.
   - A native identity is recorded once: `EXTERNAL_REFERENCE_EXISTS` (409). `listExternalReferences` finds it by that identity, and `getExternalReference` reads it by id.
2. **A Mapping is proposed, then governed.**
   - `createMapping` takes `mappingCreateRequest`. It carries no identifier, status, revision or actor, and exactly one target.
   - A mapping starts DRAFT. `updateMapping` changes only a DRAFT mapping, and never what it relates, its tenant or its type.
   - `validateMapping` moves DRAFT to VALIDATED. `activateMapping` moves VALIDATED to ACTIVE, and the approver must not be the creator (`MAPPING_SELF_APPROVAL`, four-eyes, §48). `retireMapping` takes a reason.
   - Every command requires the revision in `If-Match`: 428 when missing, 412 when stale.
   - The actor is always the verified caller.
   - Cross-tenant mappings are refused (§47).
3. **Resolution names what it resolves.**
   - `resolveExternalReference` (`POST /resolution/external-references`) resolves a native object to its canonical entity through ACTIVE EXTERNAL_TO_CANONICAL or BIDIRECTIONAL mappings in effect.
   - No match is `MAPPING_NOT_FOUND` (404). Equally authoritative matches are `MAPPING_AMBIGUOUS` (409), which resolve to nothing.
   - An IAM organisation is resolved by `resolveIamOrganisation` (ADR-BCP-018 ORG-10), never through a generic mapping.
4. **Reads.** Administrators read through `canonical:read`, alongside the workload `mapping:read` and `mapping:resolve`. Writes use `mapping:write`, and activation `mapping:approve`.
5. **The `mapping` read model follows §9.2.** `canonical_entity_id` is always set, with exactly one of `external_reference_id` and `target_canonical_entity_id`.

## Consequences

- The Control Plane replaces its local external reference and its `GET /v1/external-references` lookup. It never emits the old field names or both shapes at once.
- The Control Plane migrates existing canonical-to-canonical mappings into this model. It records the semantics its resolver already applied, marked `metadata.source: legacy-canonical-mapping`, and lists them in a migration report.
- Existing references whose system the registry cannot establish are reported, not back-filled.
- The runtime resolver reads the same Mapping store the administrative API governs.
