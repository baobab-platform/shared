# EA-04 — Federated workload activation boundary

**Date:** 2026-09-30  
**Scope:** `baobab-cp-workload` and `baobab-subscriptions-workload`  
**Authority:** Shared workload registry  
**Related:** ADR-0007 workload identity; IAM migration PR #42; baobab-cp provider-neutral evidence PR #225

## 1. Purpose

The workload registry contains two identities whose credential profile is
`federated_workload_token` rather than `client_credentials`:

```text
baobab-cp-workload
        |
        | billing:manage / billing:read
        v
baobab-subscriptions

baobab-subscriptions-workload
        |
        | payment:execute / payment:refund / payment:read
        v
baobab-payments
```

Both deliberately remain `PROVISIONED`.

This document defines when Shared may promote either workload to `ACTIVE`.

## 2. Authority split

```text
Shared
  owns workload identity meaning
  ├─ logical client id
  ├─ credential type
  ├─ allowed audiences
  ├─ allowed scopes
  └─ canonical lifecycle
        |
        v
baobab-iam
  owns provider mechanics
  ├─ projected-token trust
  ├─ OAuth/OIDC exchange
  ├─ provider client configuration
  └─ credential/token lifecycle
        |
        v
resource engine
  verifies the issued access token
        |
        v
Shared lifecycle may become ACTIVE
```

Neither IAM provider configuration nor a successful token-endpoint call alone
may promote the canonical lifecycle.

## 3. Activation evidence

A `federated_workload_token` workload MAY move from `PROVISIONED` to
`ACTIVE` only when all of the following are evidenced:

1. the runtime obtains a short-lived projected assertion without a stored OAuth
   client secret;
2. the identity provider explicitly trusts the assertion issuer and the exact
   workload subject;
3. the assertion is exchanged for a short-lived access token;
4. the access token is signed by the expected identity-provider issuer;
5. the actual resource server accepts the intended API audience;
6. the token resolves to the registered workload identity;
7. the token is classified as `actor_type=workload`;
8. its scopes are a subset of the registry entry's `allowed_scopes`;
9. a real protected request succeeds;
10. suspension/revocation can make subsequent token acquisition or use fail.

## 4. CP -> Subscriptions

Current Shared expectation:

```text
client_id: baobab-cp-workload
credential_type: federated_workload_token
audience: baobab-subscriptions
scopes:
  - billing:manage
  - billing:read
```

The Control Plane already consumes an externally projected token through its
billing workload-token file boundary. The remaining activation proof is an
identity-provider exchange whose resulting access token passes
`baobab-subscriptions`' real workload verifier.

Until that evidence exists, status remains `PROVISIONED`.

## 5. Subscriptions -> Payments

Current Shared expectation:

```text
client_id: baobab-subscriptions-workload
credential_type: federated_workload_token
audience: baobab-payments
scopes:
  - payment:execute
  - payment:refund
  - payment:read
```

`baobab-payments` has a workload-token verifier for this identity, but the
Subscriptions repository must also contain and exercise the outbound payment
execution path before this leg can be certified end to end.

Until then status remains `PROVISIONED`.

## 6. Fail-closed invariants

The activation programme SHALL NOT:

- replace `federated_workload_token` with a static client secret;
- add `actor-type-workload` as a new authorization scope merely because
  legacy Keycloak configuration used a client-scope mapper of that name;
- rename the canonical `context:resolve` scope for provider convenience;
- add Tenant, LegalEntity, Market or Capability business authority to the
  identity provider;
- mark a workload ACTIVE from provider-side configuration evidence alone.

## 7. Lifecycle rule

```text
REGISTERED IN SHARED
        |
        v
PROVISIONED
        |
        | provider + consumer live proof
        v
ACTIVE
        |
        +--> SUSPENDED
        +--> REVOKED
        +--> RETIRED
```

Shared is the canonical record of that transition.
