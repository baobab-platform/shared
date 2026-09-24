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
