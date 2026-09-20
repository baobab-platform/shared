# Baobab buyer-organisation contracts v1

This package defines Gate ZB-04's cross-engine contract for a B2B organisation applying
to trade with a Baobab tenant such as ZuriBeans.

It does **not** model an organisation applying to become a Baobab platform tenant.
That separate admission lifecycle is governed by `baobab-cp` ADR-BCP-017.

## Authority boundaries

| Concern | Authority |
| --- | --- |
| Buyer application and commercial approval | Baobab Trade |
| Canonical `BUYER_ORGANISATION` identity and tenant/context attestation | Baobab Control Plane |
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

Approval may create an engine-owned buyer organisation only after the Control Plane
has minted or verified the canonical `BUYER_ORGANISATION` identity. Rejection,
withdrawal and suspension preserve audit history.

## Guardrails

- Browser input never selects `tenant_id`, canonical IDs, credit decisions or roles.
- Keycloak organisation IDs and Medusa/ERP native IDs are external references, not
  canonical business identity.
- Trade may project ERP credit/payment-term facts but may not become their accounting
  authority.
- Site, tax, contract and price references remain scoped to the buyer organisation and
  owning tenant.
- Cross-tenant or cross-buyer access must fail closed.
- Events contain references and business state, never credentials or document binaries.

## Compatibility

The v1 resource keeps the existing buyer-organisation lifecycle values while adding
the application and membership vocabulary required by ZB-04. Consumers must reject
unknown enum values safely and pin this package through their contracts lock.
