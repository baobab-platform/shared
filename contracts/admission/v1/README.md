# Organisation Admission: ClientApplication and AdmissionDecision Contracts

**Governing ADR:** ADR-BCP-017 — Organisation Admission, Subscription Classification and Tenant Onboarding Lifecycle Model (`baobab-platform/baobab-cp`)
**Related:** ADR-BCP-018 (organisation admission, internal eligibility), ADR-BCP-019 (onboarding experience), ADR-BCP-020 (reviewer, approver and self-approval), ADR-BCP-023 (evidence)

**Contract authority:** `baobab-platform/shared`
**Runtime authority:** `baobab-platform/baobab-cp`

## Purpose

Baobab admits an organisation before it provisions a tenant (ADR-BCP-017 §1). These contracts cover the first half of that journey, from an applicant's ClientApplication to the AdmissionDecision that ends it. The approved decision's `admission_decision_id` then keys organisation admission (`organisation/v1/admission.schema.json`) and, later, tenant onboarding.

Registration, application, admission, subscription, entitlement, provisioning and authorization are distinct concerns (§1, §4). Nothing in these contracts creates a tenant, a membership, a subscription or a capability.

## Files

Every JSON file is a definition library. Validate a resource against its fragment URI (for example `application.schema.json#/$defs/ClientApplication`), not the document root.

| File | Contents |
|------|----------|
| `application.schema.json` | `ClientApplication` and its parts (`ApplicantOrganisationProfile`, `BusinessRequirements`, `ApplicationEvidence`, `InformationRequest`, `DecisionSummary`), plus the commands: `ClientApplicationDraft` (applicant create and edit), `ApplicantResponseCommand`, `InformationRequestCommand`, `ClosureCommand` |
| `decision.schema.json` | `AdmissionDecisionRequest` (what a decider submits), `AdmissionDecision` (the immutable record), `InternalEligibilityEvidence` and the ADR-BCP-005 `subscriptionType` vocabulary |
| `lifecycle.yaml` | Every permitted status transition, the command that performs it and the actor allowed to issue it |
| `events.schema.json` | Data payloads of the §40 lifecycle events |
| `asyncapi.yaml` | Registers those events and composes each with the canonical envelope (`contracts/events/v1`) |
| `examples/` | A Nabhold Group affiliate approved INTERNAL, an external applicant approved COMMERCIAL after an information request, and an incomplete draft; `examples/events/` holds example envelopes |

`scripts/validate-admission-contracts.py` validates the schemas, examples, lifecycle, negative fixtures, events and lock entry.

## Rules the contracts enforce

- **Applicant data is evidence, not canonical state (§7, §24).** `ClientApplicationDraft` is the only shape an applicant writes. It cannot carry any of these fields:
  - status or channel;
  - a decision or subscription classification;
  - tenant or organisation identifiers;
  - timestamps.

  Applicant identifiers and addresses have no `verified` field, so an applicant cannot assert verification at all.
- **Documents by reference only (§42, ADR-BCP-023).** Evidence is an opaque `evidence_reference` into the document store. A binary is rejected.
- **Data minimisation (§43).** Every text field has a length limit. The authorised representative carries a name, a role and an optional email only.
- **Business language (§18).** Requirements are yes/no business questions and free-text notes. They never name providers or engines.
- **Markets are declared, not decided (§20).** An applicant requests countries. Review maps them to Markets, and an approval's `approved_market_scope` must lie within them. Markets never choose a deployment region.
- **Explicit lifecycle (§8).** `lifecycle.yaml` lists the only permitted transitions:
  - an application cannot jump from DRAFT to a decision;
  - only a DECIDER reaches APPROVED or REJECTED, and only from UNDER_REVIEW;
  - the applicant can edit only DRAFT and INFORMATION_REQUIRED applications, and can withdraw from any open state;
  - terminal states are final.
- **A complete application to submit.** Once past DRAFT, an application has:
  - its legal name, jurisdiction, at least one registration identifier and an authorised representative;
  - at least one requested market;
  - `submitted_at`.
- **An explicit decision (§21).**
  - APPROVED requires a subscription type, a market scope and at least one evidence reference.
  - REJECTED can carry none of the approval fields.
  - The decider's identity comes from authentication, never from the request body.
  - The decider is never the applicant (ADR-BCP-020 §39).
- **Server-authoritative classification (§10-13).** The subscription vocabulary is ADR-BCP-005's: COMMERCIAL, INTERNAL, TRIAL, PARTNER, MANUAL and MIGRATION. There is no INTERNAL_GROUP. For INTERNAL, the decider names the canonical Organisation, and the Control Plane evaluates eligibility itself from governed platform and corporate relationships. The decision records `InternalEligibilityEvidence`: the verified PLATFORM_OWNER or PLATFORM_GROUP_AFFILIATE relationships in force when the decision was made. Nobody can submit that evidence, and a non-INTERNAL decision cannot carry it. INTERNAL means a zero monetary charge, never zero governance (§11).
- **Approval is not activation (§22).** An AdmissionDecision is immutable. Approval permits governed onboarding. A failed onboarding does not rewrite the decision (§44), and a later subscription change is a reclassification (§48).

## Authorization

The scopes are registered in `contracts/authorization/v1/scope-registry.yaml`:

| Scope | Holder | Permits |
|-------|--------|---------|
| `application:read` | applicant | Reading their own applications |
| `application:write` | applicant | Creating, editing, submitting, answering and withdrawing their own applications |
| `admission:review` (privileged) | platform reviewer | Inspecting applications, starting validation and review, requesting information, cancelling |
| `admission:decide` (privileged) | platform approver | Approving or rejecting an application under review. The approver is never the application's applicant. |

A scope is necessary but not sufficient. An applicant reaches only applications they own. The review and decision scopes also require platform-administrator authority in the Control Plane. The reviewer role does not include the decision (ADR-BCP-020 §34).

## Resource identifiers

| Resource | Grammar |
|----------|---------|
| ClientApplication | `capp_[a-z0-9]+` |
| AdmissionDecision | `adm_[a-z0-9]+`: a subset of `organisation/v1` `admissionDecisionId`, so it keys organisation admission directly |
| Application reference | `APP-<year>-<sequence>`: for correspondence only, never for authorization |

## Events (§40)

| Event type | When |
|------------|------|
| `com.baobab-platform.control-plane.client-application.created.v1` | An application was opened |
| `com.baobab-platform.control-plane.client-application.submitted.v1` | A DRAFT was submitted |
| `com.baobab-platform.control-plane.client-application.information-requested.v1` | A reviewer asked the applicant for more information |
| `com.baobab-platform.control-plane.client-application.withdrawn.v1` | The applicant withdrew the application |
| `com.baobab-platform.control-plane.client-application.approved.v1` | The application was approved; the payload carries the approved subscription type |
| `com.baobab-platform.control-plane.client-application.rejected.v1` | The application was rejected |

Payloads carry identifiers and state only. They never carry names, identifiers, contacts, evidence, request or decision text, or principal identifiers. The Control Plane publishes them from its transactional outbox in the same transaction as the change, and a replay that changes nothing publishes nothing. Validation, review, cancellation and expiry are audited but not published. Tenant onboarding, provisioning and activation events belong to provisioning.
