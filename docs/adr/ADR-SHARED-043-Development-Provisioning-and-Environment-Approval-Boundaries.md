# ADR-SHARED-043 — Development provisioning and environment approval boundaries

**Status: Accepted**  
**Date: 23 October 2026**  
**Decision owner:** platform owner direction, 23 October 2026.  
**Applies to:** every Baobab engine, infrastructure tool and digital estate.

## Context and precedence

Requiring independently appointed human administrators, official company
verification and externally witnessed custody before disposable synthetic
integration created a bootstrap cycle. It prevented testing the very controls
that would later qualify a protected deployment.

This decision supersedes the **development execution/acceptance restrictions**
in the INT-03C ruling, Shared #354 CMS bootstrap decision, Infrastructure #49
runbook and dependent estate plans. It supplements EA v2.3; it does not change
canonical domain ownership, real legal facts or protected operation contracts.
Historical receipts remain immutable and retain their original classification.

## 1. Standing development authorisation

Local development, disposable CI and isolated shared-development environments
may automatically provision synthetic enterprises, test identities, engine
instances and estate content. No per-run independent human approval, personal
appointment, official incorporation verification or external witness is needed.
An identified technical owner and normal reviewed source/CI remain required.
The authorisation covers Nabhold, ZuriBeans, Thamani, Equator and an unrelated
external-client negative/control case; it is not limited to a single estate.

The canonical reusable profile contract is `contracts/development/v1`.
Legal-entity/Organisation/Tenant boundaries remain independent. Nabhold is a
non-trading holding company; ZuriBeans is B2B trade; Thamani is B2B logistics.
Group affiliation grants no implicit access. External clients need no estate.

## 2. Supported bootstrap rather than a production bypass

- CP owns an explicit development bootstrap command and generated canonical
  identifiers. It may seed **synthetic initial state** in an isolated marked
  development database before normal authentication/admission can operate.
  Infrastructure must not patch protected CP storage or fabricate results.
- Synthetic records must carry run/profile provenance and a bounded lease.
  Their names and records must identify them as synthetic. They are not real
  company registrations, legal verification, provider certification or mandates.
- One developer/CI job may control distinct synthetic maker/checker identities
  and automate both workflow steps. Normal APIs must still reject the *same
  Principal* acting as its own checker. Protected environments require actual
  independent authorised people; synthetic separation is not human separation.
- IAM issues actual credentials through its provider. Test secrets are random,
  private and bounded. Tokens, tenant context and resource-server enforcement
  are exercised normally. A locally fabricated bearer is not issuer evidence.
- Development bootstrap is default-off, restricted to explicitly marked
  development databases and unavailable through production HTTP routes/images.
  Missing/unknown environment, staging or production must fail closed. No
  production identity, shared production secret or product registry row is
  activated by selecting a development profile.
- Development provider fixtures may declare isolated synthetic routing support;
  actual provider availability and operation success must be observed. A seeded
  binding, a UI prototype or an Accepted ADR cannot make an absent engine pass.

## 3. Repeatable provisioning and testing

Infrastructure composes exact-source engine adapters and estate profiles with
prepare/up/test/down commands, private run state and recoverable teardown.
Profiles reuse shared engines where supported; no cluster per subsidiary is
required. IAM identity, CP context/grants/bindings, engine storage and estate
content must retain each enterprise boundary.

Each implemented integration must test positive own-tenant access, sibling and
external-client denial, missing grant, wrong audience, expiry/revocation,
maker/checker denial, dependency failure/recovery and cleanup where relevant.
The seven INT-03C and fourteen NAB-03 case meanings are unchanged. Unsupported
providers/cases report BLOCKED/NOT_IMPLEMENTED, never PASS or an invented N/A.

Successful actual runtime assertions may report PASS immediately with evidence
class `REAL_COMPONENT_SYNTHETIC_DATA`, run/source/image pins and retained
sanitized logs/hashes. Source-only or mocked tests retain their own weaker
classification. Development PASS requires neither human certification nor
external WORM storage; CI artifacts or private local receipts are sufficient.
Reports must keep protected staging, external certification and production
acceptance false. Hashes and separate checking processes prove their stated
technical properties; they do not establish independent human acceptance.

Bounded lifetime, scoped credentials, private networking, resource ownership,
durable create-before-mutate recovery state and cleanup on failure remain
mandatory. A reusable development lease is at most 24 hours; per-run token
lifetimes remain short. No independent signing ceremony is required to renew
an isolated development environment, but renewed resources need current state
and fresh credentials. No automatic renewal into protected environments.

## 4. CMS development activation

The former development registry hold on `baobab-int03-cms-consumer` and
`baobab-int03-cms-validator` is lifted within this isolated profile. Their
exact #354 audience/scope/owner ceilings remain unchanged. Separately named
per-estate development callers may use the same content contract and must
have separate credentials, canonical Principals and tenant-scoped contexts.
Normal production workloads including `nabhold-backend` retain their existing
lifecycle; development bootstrap cannot promote them.

## 5. Where independent approvals apply

Preparing/provisioning **protected staging** requires actual authorised people,
independent security/operations review, verified administrative separation,
approved host/network/secret access, current legal/provider evidence where
applicable, durable evidence custody and recovery/teardown acceptance.
Production additionally requires capability/tenant/market/legal-actor-specific
business, operational, legal and provider go/no-go. Developer approval of source
or a passing disposable run supplies none of those approvals.

Changesets, execution fences, financial controls, tenant isolation and statutory
requirements remain enforced in their domains. This decision removes the
development *human approval gate*, not the mechanisms being tested.

## Implementation and rollback

Shared publishes the closed development profiles and allowed development
identities; CP implements guarded bootstrap; IAM owns provider issuance;
Infrastructure owns lifecycle/testing; engines/estates own their adapters.
Consumers pin the merged Shared revision. Protected behavior must have negative
regression coverage. Rollback disables development bootstrap and tears down
owned disposable resources; no protected identity/state may depend on them.
