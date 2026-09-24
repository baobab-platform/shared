# Baobab buyer-organisation contracts v1

This package defines Gate ZB-04's cross-engine contract for a B2B organisation applying
to trade with a Baobab tenant such as ZuriBeans.

It does **not** model an organisation applying to become a Baobab platform tenant.
That separate admission lifecycle is governed by `baobab-cp` ADR-BCP-017.

## Authority boundaries

| Concern | Authority |
| --- | --- |
| Buyer application and commercial approval | Baobab Trade |
| Registration and verification of a `BUYER_ORGANISATION` canonical entity; tenant/context attestation | Baobab Control Plane (ADR-BCP-016, with Organisation authority settled by ADR-BCP-018) |
| Human authentication and principal lifecycle | Baobab IAM |
| Buyer membership, roles and purchasing authority | Baobab Trade |
| Customer/Business Partner projection, credit and accounting consequences | Baobab ERP |
| Buyer-facing presentation | ZuriBeans digital estate |
| Cross-engine schemas and events | Baobab Shared Contracts |

A login does not confer organisation membership. Membership does not approve an
organisation. Approval does not grant unrestricted purchasing authority. An approved
buyer cannot trade until canonical linkage, required commercial controls and active
membership are all present.

## Contract surfaces

- `domain.schema.json` defines buyer applications, approved organisations,
  memberships, delivery/billing sites and the cross-engine commercial profile.
- `events.schema.json` defines submission, decision, organisation, membership and
  commercial-profile event data.
- `asyncapi.yaml` publishes those payloads through the canonical event envelope.

## Lifecycle

```text
DRAFT
  -> SUBMITTED
  -> INFORMATION_REQUIRED | UNDER_REVIEW
  -> APPROVED | REJECTED
```

Approval creates the Trade-owned buyer relationship. Canonical linkage remains nullable until a
Control Plane `BUYER_ORGANISATION` entity is registered and verified. ADR-BCP-018 (section 194)
settles the Organisation authority ADR-BCP-016 left open: the Control Plane is the runtime
authority, and existing `BUYER_ORGANISATION` IDs remain reusable as canonical Organisation IDs.
Rejection,
withdrawal and suspension preserve audit history.

## Guardrails

- Browser input never selects `tenant_id`, canonical IDs, credit decisions or privileged roles.
- Keycloak organisation IDs and Medusa/ERP native IDs are external references, not
  canonical business identity.
- Trade may project ERP credit/payment-term facts but may not become their accounting
  authority.
- Site, tax, contract and price references remain scoped to the buyer organisation and
  owning tenant.
- Cross-tenant or cross-buyer access must fail closed.
- Events contain references and business state, never credentials or document binaries.

## Compatibility

The v1 resource preserves all existing required fields and event payloads while adding
the application and membership vocabulary required by ZB-04. Consumers must reject
unknown enum values safely and pin this package through their contracts lock.


### Invitation identity transition

An `INVITED` membership reserves organisation-scoped role authority for an intended email
recipient but is not yet a Trade customer or canonical Principal relationship. Therefore
`customer_id` and `principal_id` are present as `null` until the one-time invitation is
accepted. Every non-`INVITED` membership requires both identifiers. Implementations must not
manufacture placeholder identities to satisfy the contract.
