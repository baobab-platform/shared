# PEO-01 / PEO-02R — Applicable requirement and documentary review contracts

This package implements the contract vocabulary of ADR-BCP-026 §§6–7 and
does not replace the RTD-06/RTD-08 Regulations documentary requirement
contracts or any statutory, provider or sovereign decision authority.

## Authority boundaries

- **Control Plane** owns the governed enterprise admission record, the
  deferral tied to one *original* provisional admission approval, due
  review work and consumer-specific capability restriction orchestration.
- **Regulations** owns source-backed statutory applicability and legal
  sufficiency. CP consumes *pinned* Regulations decisions, not editable
  applicant text or a guessed universal requirement.
- **Evidence service / provider** owns verified evidence and provider
  eligibility assertions for its audience. A reference alone does not
  convert an applicant claim into approved evidence.
- **Consumer PEP** owns its actual operation authorisation (ERP invoice,
  Trade seller, Payments merchant, Trade Docs issuance, etc.). A CP
  review record cannot grant a permit or waive third-party conditions.

## Contract definitions

`RequirementApplicabilityAssessment`: one expiring, policy-versioned,
organisation-bound applicable/non-applicable/unresolved assessment for a
named requirement, authority class and trusted business context. For
`APPROVED_EVIDENCE`, an exact reference is mandatory, but the consumer
must independently validate provenance and temporal freshness.

`DocumentaryReviewCheckpoint`: an **immutable due-work record**, not a
positive evidence or compliance result. Milestone months are the exact
6th, 12th, 18th, or 24th UTC-calendar-month anniversary of the original
provisional approval. A reapplication, rename or tenant registration
cannot reset the origin.

`DocumentaryReviewAssessment`: a proposed resolution record that names
the distinct human reviewer and versioned applicability assessments.
The consumer must check that all requirements and their policy references
match the original deferral and that the reviewer is independently
authorised. Merely accepting a JSON value must never mark any evidence
as verified, clear an obligation or reactivate an expired grace.

## Integration stages

1. The CP PostgreSQL PEO-02R migration/worker provides the immutable
   due-work queue. It is not an entitlement/event service.
2. Subsequent governed CP API and explicit staff approval workflows may
   consume this schema only after independent policy and security review.
3. Versioned, evidence-backed remediation and capability-specific
   restrictions are separate decisions, with auditable outbox publication
   after their own producer contracts are approved.
4. The first production admission remains blocked pending real IAM tokens,
   staging acceptance, provider-enforcement and operator sign-off.

**This schema alone does not commission any actual review outcome.**

## PEO-02T — current, negative-only documentary PEP veto

The canonical `documentary-restriction.schema.json` defines the private
authenticated CP runtime `POST /internal/documentary/v1/restrictions/assess`
boundary. `DocumentaryRestrictionAssessmentRequest` carries only a trusted
workload-owned runtime `context_id` and the exact market, capability and
irreversible operation reference. It cannot nominate a tenant, legal actor,
parent company, provider or mandate.

CP independently redeems the Context and checks the ACTIVE tenant's PRIMARY
Organisation before reading its current documentary restriction ledger.
`DocumentaryRestrictionAssessmentResponse` echoes the exact scope, bounds
the decision lifetime to **at most two seconds**, has `blocked:boolean`
and MUST contain `authority_granted:false`. A missing/expired/unknown
decision or service outage requires a deny, not an optimistic default.
Responses (including denied authorization) require `Cache-Control: no-store`.

**No negative hold** (`blocked:false`) is not proof of incorporation, a
signed acting mandate, Regulations legal applicability, compliance, provider
certification or permission to transact. Every Trade, ERP, Payments and
Trade Docs PEP must separately verify its own complete operation-specific
authority, and recheck an active hold at the point of irreversible execution.

**JSON Schema alone cannot compare response timestamps or match a response
to its originating request.** The normative executable pair/lease predicate
lives in `scripts/documentary_restriction_binding.py`, and
`scripts/tests/test_peo02t_documentary_restriction_contract.py` is executed
in Shared's required CI. Consumers **MUST** implement and test equivalent
runtime checks; simply validating the response JSON object does not satisfy
this contract. Reject nonpositive or >2-second leases, expired/stale decisions
and every mismatched echoed Context, operation, market or capability.

CP owns this negative-scoped fact; Trade/ERP/Payments/Trade Docs never
create or directly remove holds. Independent verified remediation approval
is required before any release. Existing CP PEO-02S documentary review
decisions can impose negative holds but do **not** grant positive readiness.
A canonical Shared schema does not activate or certify any provider.
