# Baobab product and subscription contracts v1

This package defines the canonical, implementation-neutral vocabulary for
Product, ProductVersion, ProductSubscription and EntitlementProjection
(Technical Specification SS31 "Product Composition and Subscription", SS88
"Programme Gate P1 — Shared Contract Foundation", SS91 "Programme Gate P4 —
Product and Composition Engine"). It answers:

- **What can be subscribed to?** -> `product.schema.json` (`Product`,
  `ProductVersion`).
- **What has a tenant subscribed to?** -> `subscription.schema.json`
  (`ProductSubscription`).
- **Has that subscription actually produced entitlements yet?** ->
  `subscription.schema.json` (`EntitlementProjection`).

## What this package is not

Like `contracts/capability/v1`, this is a contract-authority package: JSON
Schema, AsyncAPI and this README only. It does **not**:

- run as a service, hold tenant state, or perform composition expansion --
  that is `baobab-platform/baobab-cp`'s runtime responsibility;
- decide which capabilities a composition contains -- see
  `contracts/capability/v1/composition.schema.json`'s `CapabilityComposition`,
  which `ProductVersion.composition_key` references;
- issue or revoke `CapabilityGrant` records directly -- `EntitlementProjection`
  is the read-model record of that expansion, not the grant itself
  (`contracts/capability/v1/grant.schema.json` is authoritative for grants).

## Relationship to `contracts/capability/v1`

The chain this package and `capability/v1` together describe is:

```text
ProductSubscription
      |
      v
ProductVersion --composition_key--> CapabilityComposition
      |                                      |
      |                                      v
      +--subscription_profiles[]--> (additional CapabilityComposition members)
                                             |
                                             v
                                     CapabilityGrant (source=PRODUCT_SUBSCRIPTION,
                                                       source_reference=subscription_id)
                                             |
                                             v
                                     EntitlementProjection (this package's own
                                                             record that the
                                                             expansion happened)
```

A `Product` is identified by the existing
`contracts/control-plane/v1/domain.schema.json#/$defs/productId` grammar --
no new product identifier grammar is introduced here. `ProductVersion`,
`ProductSubscription` and `EntitlementProjection` mint their own opaque IDs
(`prodver_`, `sub_`, `entproj_`) via `domain.schema.json` in this package,
following the same pattern as `capability/v1/domain.schema.json`'s `cap_`/
`comp_`/`grant_` IDs.

## Contract surfaces

- `domain.schema.json` -- identifier grammar and closed enumerations for this
  package (`productVersionId`, `subscriptionId`, `entitlementProjectionId`,
  `productLifecycle`, `subscriptionStatus`, `subscriptionSource`,
  `entitlementProjectionStatus`).
- `product.schema.json` -- `Product` and `ProductVersion`.
- `subscription.schema.json` -- `ProductSubscription` and
  `EntitlementProjection`.
- `events.schema.json` / `asyncapi.yaml` -- lifecycle events, using the
  `com.baobab-platform.<context>.<...>.v<N>` convention (ADR-SHARED-008).

All asynchronous messages use `contracts/events/v1/envelope.schema.json`.

## Subscription classification (ADR-SHARED-011, ADR-BCP-018 gate ORG-11)

A ProductSubscription's commercial classification, and why it holds, is Control Plane data defined here.

- **`subscriptionType`** is the ADR-BCP-005 vocabulary: COMMERCIAL, INTERNAL, TRIAL, PARTNER, MANUAL and MIGRATION. It is identical to `admission/v1`, and there is no INTERNAL_GROUP.
- **`productSubscription.classification`** holds the current type, its source (`ADMISSION_DECISION`, `RECLASSIFICATION`, `MIGRATION` or `MANUAL_GOVERNANCE`), its reference (the `admission_decision_id` for an admission) and when it was made.
- **`SubscriptionClassificationRecord`** is each immutable classification. An INTERNAL record always carries the server-evaluated `InternalEligibilityEvidence`: the qualifying platform relationships. Reclassification appends a record to the same subscription; it never replaces the tenant, organisation or subscription identity.
- **`ClassificationExplanation`** answers "why is this subscription INTERNAL?" from Control Plane records. It gives the current record, the history, eligibility re-evaluated now (drift is visible) and the billing policy.
- **`billing-policy.yaml`** says what each type means for billing. INTERNAL is zero monetary charge and no billing, but it stays metered, entitled, audited, readiness- and isolation-controlled, and payments are never invoked.
- **`com.baobab-platform.product.subscription.classified.v1`** is published on every (re)classification.

Classification never changes CapabilityGrant semantics. INTERNAL still grants through ProductSubscription → ProductVersion → CapabilityComposition → CapabilityGrant.
