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
