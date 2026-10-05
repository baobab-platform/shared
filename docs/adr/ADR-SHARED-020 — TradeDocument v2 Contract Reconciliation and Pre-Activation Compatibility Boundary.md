# ADR-SHARED-020 — TradeDocument v2 Contract Reconciliation and Pre-Activation Compatibility Boundary

**Status:** Accepted — Normative Shared Contract Reconciliation  
**Date:** 2026-10-05  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-020  
**Decision Type:** Shared Contract Evolution / TradeDocument / Versioning / Event Compatibility / Authority Boundary  
**Implements:** RTD-04 from ADR-SHARED-019  
**Platform Boundary Authority:** ADR-SHARED-019 — Regulatory Intelligence, Trade Documents and Evidence Cross-Engine Boundary  
**Trade Docs Authorities:** `baobab-platform/baobab-trade-docs` ADR-TDOC-0001 and ADR-TDOC-0002  
**Regulations Reconciliation:** `baobab-platform/baobab-regulations` ADR-REG-0026 and ADR-REG-0027 as amended by RTD-03  
**Pulse Reconciliation:** `baobab-platform/baobab-pulse` ADR-PULSE-012  
**Compatibility Constraint:** `baobab-platform/thamani` ADR-THA-0018 §83

---

## 1. Executive Decision

Shared SHALL introduce:

```text
contracts/trade-document/v2
```

as the canonical **pre-activation TradeDocument contract family** aligned with the dedicated Baobab Trade Docs bounded context.

Shared SHALL NOT silently mutate the existing:

```text
contracts/trade-document/v1
```

schema into the richer Trade Docs model.

The v1 package is preserved as a historical compatibility scaffold because an accepted Thamani ADR explicitly requires v2 or a new contract family rather than silent mutation.

The v2 package SHALL establish these foundational distinctions:

```text
TradeDocument
    != File

TradeDocument
    != DocumentVersion

DocumentVersion
    != ContentArtifact

Document Lifecycle
    != Verification State

Document Lifecycle
    != Temporal Validity

Verification
    != Regulatory Sufficiency

Document Number
    != Canonical TradeDocument ID

TradeDocument ID
    != Control Plane CanonicalEntity ID
```

The core authority model is:

| Concern | Authority |
|---|---|
| TradeDocument identity and lifecycle | Baobab Trade Docs |
| DocumentVersion | Baobab Trade Docs |
| ContentArtifact association and integrity metadata | Baobab Trade Docs |
| Document-to-document relationship | Baobab Trade Docs |
| Documentary verification projection | Baobab Trade Docs |
| Tenant/platform context | Control Plane |
| Canonical organisation identity | Control Plane |
| Regulatory document/permit/evidence requirement | Baobab Regulations |
| Regulatory requirement satisfaction | Baobab Regulations |
| External legal issuance / Customs authority | Competent external issuer/authority |
| Underlying commercial/transport/financial facts | Owning operational engine |
| Cross-domain intelligence | Baobab Pulse |

---

## 2. Why RTD-04 Exists

ADR-SHARED-019 established the platform boundary:

```text
Regulations
    determines regulatory meaning

Trade Docs
    owns documentary and Customs-workflow state

Pulse
    analyses authorised evidence
```

RTD-02 reconciled Pulse.

RTD-03 reconciled Regulations.

RTD-04 now makes the **Shared TradeDocument contract itself** conform to that architecture.

The current v1 contract predates the dedicated Trade Docs engine and therefore contains assumptions that no longer match the accepted architecture.

---

## 3. Existing v1 Defects

The v1 package currently contains the following problems.

| v1 behaviour | Problem | v2 correction |
|---|---|---|
| Says Control Plane mints `trade_document_id` | Violates TDOC domain ownership | Trade Docs mints opaque domain ID |
| One `status` includes DRAFT/ISSUED/VERIFIED/REJECTED/SUPERSEDED | Conflates lifecycle and verification/workflow | Separate lifecycle and verification axes |
| No DocumentVersion | Cannot preserve immutable semantic states | First-class immutable DocumentVersion |
| `storage_reference` on TradeDocument root | Treats document as one file | Storage moves to ContentArtifact |
| Closed document type enum | Cannot scale to real trade/regulatory corpus | Extensible governed type-code syntax |
| `related_shipment_id`, `related_procurement_request_id` | Foreign-key explosion | Typed subject associations |
| One issuing-party string | Weak issuer semantics | Structured issuer claim |
| No business identifier collection | Confuses document number and canonical identity | Separate business identifiers |
| No document relationship model | Cannot express supersession/amendment/provenance graph | First-class relationship |
| `verified` / `rejected` events as lifecycle events | Conflates verification and workflow outcome | Version verification-change event; lifecycle facts separate |

---

## 4. Why v2 Instead of Editing v1

This is not merely a stylistic version bump.

Accepted Thamani ADR-THA-0018 §83 states that:

```text
contracts/trade-document/v1
```

must not be silently mutated into the richer TDOC model and requires:

```text
v2
or
a new canonical contract family
```

through Shared governance.

That constraint is correct.

Even though v1 events remain PROPOSED and there is no authorised producer, documentation and design artefacts already reference the package.

Therefore:

> **Pre-activation does not mean we should destroy compatibility evidence. It means we can introduce the correct contract before runtime activation without carrying legacy runtime obligations into the new design.**

---

## 5. v1 Compatibility Policy

The v1 schema/event shapes SHALL remain preserved.

Its README SHALL mark it:

```text
superseded before activation
```

for new implementations.

The following v1 events remain PROPOSED:

```text
com.baobab-platform.documents.trade-document.issued.v1
com.baobab-platform.documents.trade-document.verified.v1
com.baobab-platform.documents.trade-document.rejected.v1
```

They are not activated by RTD-04.

They are not the event surface new producers should implement.

---

## 6. v2 Contract Scope

RTD-04 defines only the foundational contract family covered by TDOC-0001 and TDOC-0002:

```text
TradeDocument
DocumentVersion
ContentArtifact
DocumentIdentifier
IssuerClaim
SubjectAssociation
DocumentRelationship
document lifecycle
verification projection
temporal validity projection
provenance summary
minimal cross-engine document events
```

It deliberately does not attempt to complete the entire future Trade Docs engine.

---

## 7. TradeDocument Identity

The canonical v2 TradeDocument identifier SHALL be minted by the Trade Docs provider.

Conceptually:

```text
Trade Docs
    ↓
tdoc_<opaque-id>
```

The identifier SHALL:

- be opaque;
- be tenant-safe;
- avoid encoding document type;
- avoid encoding jurisdiction;
- avoid encoding issuer;
- avoid encoding provider implementation;
- remain durable.

Hard invariant:

```text
TradeDocument domain ID
    !=
Control Plane CanonicalEntity ID
```

Control Plane may separately register or map a TradeDocument where platform architecture requires it.

---

## 8. No Synchronous CP ID-Minting Dependency

Creating a TradeDocument SHALL NOT normally require a synchronous round trip to Control Plane merely to mint the domain identifier.

This preserves local transactional availability.

Control Plane remains authoritative for:

- tenant context;
- canonical organisations;
- capability resolution;
- engine/provider topology;
- canonical mappings where applicable.

---

## 9. Document Number Is Not Canonical Identity

A TradeDocument may have many identifiers.

Example:

```text
Canonical ID:
tdoc_01...

Issuer document number:
UG-PHYTO-2026-004188

Customs reference:
MRN-...

Carrier reference:
B/L-...
```

Those business/external identifiers SHALL not replace the TradeDocument domain identity.

---

## 10. Document Type Becomes Extensible

v1 uses a closed enum.

That is insufficient for:

- permits;
- licences;
- SPS certificates;
- Customs messages;
- warehouse documents;
- transport variants;
- letters of credit;
- regulatory filings;
- specialised authority documents;
- future standards.

v2 SHALL therefore use:

```text
document_type = governed code
```

with a stable syntax rather than a permanently closed enum.

A future DocumentTypeRegistry may govern the accepted code set.

---

## 11. Type Registry Is Not a Rule Engine

The future document-type registry may describe structural/document policy.

It SHALL NOT determine jurisdiction-specific regulatory requirements.

This remains prohibited:

```text
if document_type == PHYTOSANITARY_CERTIFICATE:
    requirement_satisfied = true
```

Regulations owns legal applicability and sufficiency.

---

## 12. Document Families

v2 introduces high-level families such as:

```text
TRADE
TRANSPORT
CUSTOMS
REGULATORY
PROCUREMENT
FINANCIAL
INSURANCE
QUALITY
WAREHOUSE
PAYMENT
CONTRACT
IDENTITY_SUPPORTING
OTHER
```

Family is organisational/semantic metadata.

It does not determine legal authority.

---

## 13. TradeDocument and DocumentVersion

The durable root answers:

> **Which document is this?**

The version answers:

> **Which immutable semantic state of that document is this?**

Therefore:

```text
TradeDocument TD-1
    │
    ├── DocumentVersion V1
    ├── DocumentVersion V2
    └── DocumentVersion V3
```

is valid where document policy treats revisions as versions of one legal/business document.

---

## 14. Correction May Require a New Document

Some legal/document policies require:

```text
TradeDocument A
    │
    │ REPLACED_BY
    ▼
TradeDocument B
```

rather than version 2 of A.

Shared SHALL not force one universal correction model.

---

## 15. DocumentVersion Is Immutable Once Committed

Once a version is materially:

- issued;
- submitted;
- signed;
- accepted by an authority;
- otherwise committed under its document policy,

its semantic state SHALL not be silently rewritten.

Correction occurs through:

- a new DocumentVersion; or
- a new TradeDocument with an explicit relationship.

---

## 16. DocumentVersion Is Not a File

A DocumentVersion may have multiple representations:

```text
DocumentVersion
    ├── canonical JSON
    ├── XML
    ├── human-readable PDF
    ├── source scan
    └── signed envelope
```

Those representations are ContentArtifacts.

---

## 17. ContentArtifact Owns Storage Location

The v1 root-level:

```text
TradeDocument.storage_reference
```

is removed from v2.

Instead:

```text
ContentArtifact.storage_reference
```

owns the artifact location.

This allows:

```text
Version 1 JSON -> object A
Version 1 PDF  -> object B
Version 2 JSON -> object C
```

without pretending the TradeDocument itself is one file.

---

## 18. Content Integrity Is Explicit

Material ContentArtifacts SHOULD carry:

```text
digest_algorithm
digest_value
```

plus an explicitly identified storage representation.

But:

```text
hash matches
    !=
issuer authenticated
```

and:

```text
issuer authenticated
    !=
regulatory requirement satisfied
```

---

## 19. Source Original and Derived Content

v2 artifact roles support distinctions such as:

```text
SOURCE_ORIGINAL
DERIVED_EXTRACTION
CANONICAL_STRUCTURED_CONTENT
HUMAN_RENDERING
AUTHORITY_NATIVE_MESSAGE
SIGNED_ENVELOPE
SCANNED_COPY
```

If structured content is extracted from a PDF, the derived representation SHALL not silently replace the source original.

---

## 20. Lifecycle State Is Narrow

v2 TradeDocument lifecycle includes intrinsic states such as:

```text
DRAFT
ISSUED
SUPERSEDED
VOIDED
WITHDRAWN
ARCHIVED
```

The following SHALL NOT be lifecycle values:

```text
VERIFIED
REJECTED
```

because they express other semantic axes.

---

## 21. Verification State Is Separate

v2 models documentary verification separately:

```text
UNVERIFIED
PENDING
VERIFIED
FAILED
DISPUTED
UNKNOWN
```

Verification is a documentary trust/evidence projection.

It does not automatically establish:

- authenticity;
- legal validity;
- issuer authority;
- regulatory sufficiency.

---

## 22. Temporal Validity Is Separate

A document/version may independently be:

```text
NOT_YET_EFFECTIVE
CURRENTLY_VALID
EXPIRED
REVOKED
UNKNOWN
```

An expired certificate is still a TradeDocument.

Expiry does not mean deletion.

Revocation does not mean content mutation.

---

## 23. Medium Classification

v2 supports the distinction:

```text
NATIVE_DIGITAL
DIGITISED_PAPER
PAPER_REFERENCE
HYBRID
```

This prevents:

```text
scan of paper document
    =
native electronic record
```

from becoming an accidental assumption.

---

## 24. Issuer Claim Is Structured

Every TradeDocument SHALL have a determinable issuer claim.

v2 represents:

```text
party reference
issuer role
source identity
authority context
```

without asserting that the claim has been verified.

Hard invariant:

```text
issuer claim
    !=
issuer verification
```

---

## 25. Do Not Create Duplicate Organisation Masters

Where an issuer is a known Baobab organisation or authority, Trade Docs should reference that canonical identity.

Trade Docs SHALL not create independent master organisations such as:

```text
"URA in Trade Docs"
"SARS in Trade Docs"
"Maersk in Trade Docs"
```

that compete with Control Plane identity.

---

## 26. Subject Associations Replace Foreign-Key Explosion

v1 contains one-off fields such as:

```text
related_shipment_id
related_procurement_request_id
```

That model does not scale.

v2 introduces typed subject associations:

```text
subject_context
subject_type
subject_reference
role
effective period
```

Examples may associate a document with:

- shipment;
- consignment;
- order;
- invoice;
- payment;
- organisation;
- product;
- Customs case;
- regulatory assessment.

---

## 27. RTD-05 Is Not Pre-Empted

The v2 subject association intentionally does **not** define the platform-wide cross-engine canonical object-reference model.

That model belongs to RTD-05.

Therefore:

```text
v2 subject_reference
    !=
final CrossEngineObjectReference contract
```

Future APIs/events needing portable canonical cross-engine identity SHALL adopt RTD-05.

---

## 28. Document Relationships Are First-Class

v2 supports document-to-document relationships such as:

```text
SUPERSEDES
AMENDS
CORRECTS
REPLACES
CANCELS
SUPPORTS
EVIDENCES
REFERENCES
DERIVED_FROM
GENERATED_FROM
SUBMITTED_WITH
RESPONDS_TO
DUPLICATES
```

Direction SHALL be explicit.

---

## 29. Requirement Fulfilment Is Deliberately Excluded from v2 Document Relationships

TDOC-0002 discusses:

```text
FULFILS_REQUIREMENT
```

as a broader relationship concept.

RTD-04 deliberately does not encode that inside the document-to-document relationship enum because:

```text
DocumentRequirement
    -> Regulations

TradeDocument
    -> Trade Docs
```

Their portable relationship needs RTD-05 cross-engine references and RTD-06 Regulations ↔ Trade Docs contract choreography.

This prevents RTD-04 from inventing an incompatible requirement reference.

---

## 30. Provenance Summary

v2 carries a bounded provenance summary sufficient to state whether a version was:

```text
EXTERNAL_INGESTED
BAOBAB_GENERATED
MIGRATED
DERIVED
```

and to retain source/supplier/system context.

This is not the complete future provenance/evidence architecture.

It is a minimum cross-engine contract surface.

---

## 31. TradeDocument Is Not Evidence

Hard invariant:

```text
TradeDocument
    !=
Evidence
```

A TradeDocument or exact DocumentVersion may be referenced as evidence.

Evidence purpose, sufficiency and decision context remain separate.

---

## 32. Regulations Boundary

v2 does not contain:

- DocumentRequirement;
- PermitRequirement;
- RegulatoryEvidenceAssessment;
- RequirementSatisfaction;
- RegulatoryDecision.

Those belong to Regulations.

The future relationship is:

```text
Regulations requirement
        ↓
Trade Docs document/version
        ↓
Regulations satisfaction assessment
```

through RTD-05/RTD-06 contracts.

---

## 33. External Authority Boundary

Trade Docs storing or generating a document does not make Trade Docs the legal issuer.

Examples:

```text
Certificate of origin
    -> competent issuer

Customs release
    -> Customs authority

Bill of lading issuance
    -> issuing carrier

Commercial invoice business authority
    -> issuing commercial/legal entity
```

Trade Docs governs the documentary representation and workflow.

---

## 34. v2 Event Model

RTD-04 proposes v2 facts for:

```text
content artifact registered
document relationship created
document version created
document version issued
document version verification changed
TradeDocument created
TradeDocument issued
TradeDocument superseded
TradeDocument voided
```

These events are deliberately minimal.

They carry identifiers and bounded facts, not complete foreign aggregates.

---

## 35. Verification Events Are Version-Oriented

The old v1:

```text
trade-document.verified
trade-document.rejected
```

surface is not copied into v2.

Verification is represented as:

```text
document-version.verification-changed
```

because verification applies to a concrete semantic version/artifact context.

External authority rejection belongs to later Customs/submission workflow contracts, not generic document lifecycle.

---

## 36. Events Remain PROPOSED

RTD-04 SHALL NOT activate the v2 events.

The `documents` event context may record the accepted target authority, but the event registry entries remain:

```text
lifecycle: PROPOSED
```

with no producer.

Producer activation is a separate governance step.

---

## 37. No Commands Hidden as Events

The following are commands:

```text
CreateTradeDocument
CreateDocumentVersion
IssueDocument
SupersedeDocument
AttachContentArtifact
VerifyDocument
```

They SHALL NOT be represented as fact events merely by using imperative event names.

Events record committed facts.

---

## 38. Scope Deferred Beyond RTD-04

The following are explicitly deferred:

- CrossEngineObjectReference — RTD-05;
- Regulations ↔ Trade Docs requirements/evidence APIs/events — RTD-06;
- document-event producer activation;
- DocumentDossier;
- CustomsCase;
- CustomsDeclaration workflow;
- submission lifecycle;
- Customs authority response contract;
- authority adapters;
- document generation APIs;
- detailed signature/trust model;
- transferable-record control;
- endorsement chain;
- retention/deletion;
- complete DocumentTypeRegistry.

These require later TDOC ADRs or RTD increments.

---

## 39. Why Dossier and CustomsCase Are Not in v2 Yet

TDOC-0001 identifies those as part of the future engine mission.

TDOC-0002 defines the document/version/content/relationship foundation.

RTD-04 aligns Shared with the **accepted domain model that is already sufficiently specified**.

It does not guess the contract shapes of future TDOC-0003/0004/0005 decisions.

---

## 40. Example — Phytosanitary Certificate

```text
TradeDocument
  id = tdoc_...
  type = PHYTOSANITARY_CERTIFICATE
  family = REGULATORY
  issuer claim = Uganda NPPO
  lifecycle = ISSUED
  current version = V1

DocumentVersion V1
  verification = VERIFIED
  temporal validity = CURRENTLY_VALID
  medium = NATIVE_DIGITAL

ContentArtifacts
  source PDF
  canonical JSON
```

Regulations may later evaluate whether that exact version satisfies a specific SPS requirement.

v2 does not claim that VERIFIED means SATISFIED.

---

## 41. Example — Corrected Commercial Invoice

Where policy permits a new version:

```text
TradeDocument TD-10
  ├── V1 issued
  └── V2 issued, supersedes V1
```

V1 remains historically available.

Where policy requires a new legal instrument:

```text
TradeDocument TD-10
    │ REPLACED_BY
    ▼
TradeDocument TD-11
```

Shared supports both models.

---

## 42. Example — Source Scan and Derived Extraction

```text
external PDF
   ↓
SOURCE_ORIGINAL ContentArtifact
   ↓
extraction process
   ↓
DERIVED_EXTRACTION ContentArtifact
```

The derived value does not silently become the issuer's authoritative assertion.

---

## 43. Validation Requirements

Shared CI SHALL validate at minimum that:

1. v2 schemas use JSON Schema 2020-12.
2. immutable contract URIs are correct.
3. TradeDocument ID no longer claims CP minting.
4. document type is not a closed enum.
5. lifecycle excludes VERIFIED/REJECTED.
6. verification is a separate axis.
7. root TradeDocument has no `storage_reference`.
8. ContentArtifact owns storage and digest.
9. DocumentVersion exists and is first-class.
10. v1 contract shape remains preserved.
11. v2 event surface matches this ADR.
12. v2 does not pre-empt requirement fulfilment.
13. example resources validate.
14. event examples validate through the platform event registry.

---

## 44. Contract Invariants

```text
INV-TDOC-SHARED-001
Trade Docs, not Control Plane, mints TradeDocument domain IDs.

INV-TDOC-SHARED-002
TradeDocument ID is distinct from business/external document numbers.

INV-TDOC-SHARED-003
TradeDocument is distinct from DocumentVersion.

INV-TDOC-SHARED-004
DocumentVersion is distinct from ContentArtifact.

INV-TDOC-SHARED-005
storage_reference exists on ContentArtifact, not TradeDocument.

INV-TDOC-SHARED-006
Document lifecycle is distinct from verification state.

INV-TDOC-SHARED-007
Document lifecycle is distinct from temporal validity.

INV-TDOC-SHARED-008
Verification does not imply regulatory sufficiency.

INV-TDOC-SHARED-009
document_type remains extensible through governed codes.

INV-TDOC-SHARED-010
Typed subject associations replace one-off related_* foreign keys in v2.

INV-TDOC-SHARED-011
Issuer claim is distinct from issuer verification.

INV-TDOC-SHARED-012
Issued/committed DocumentVersions are immutable historical states.

INV-TDOC-SHARED-013
Document relationships are explicit and directional.

INV-TDOC-SHARED-014
Requirement fulfilment is not encoded as a Trade Docs-local relationship in RTD-04.

INV-TDOC-SHARED-015
v1 is preserved rather than silently rewritten.

INV-TDOC-SHARED-016
v2 event types remain PROPOSED until producer activation.

INV-TDOC-SHARED-017
External sovereign/legal authority is not transferred to Trade Docs.

INV-TDOC-SHARED-018
No direct database coupling is implied by the Shared contract.

INV-TDOC-SHARED-019
Cross-engine portable object reference semantics remain reserved for RTD-05.

INV-TDOC-SHARED-020
Regulatory requirement and satisfaction semantics remain owned by Regulations.
```

---

## 45. Migration Model

The contract evolution is:

```text
v1 pre-Trade-Docs scaffold
        │
        │ preserved for compatibility evidence
        ▼
v2 TDOC-aligned foundation
        │
        ├── RTD-05 canonical cross-engine references
        ├── RTD-06 Regulations ↔ Trade Docs choreography
        ├── later TDOC workflow contracts
        └── producer activation
```

New implementation SHALL target v2.

No runtime v1 producer migration is required because no v1 producer was authorised.

---

## 46. Event-Versioning Rule

Because v2 changes payload semantics materially, its event types use:

```text
.v2
```

even where the business fact name resembles an old proposed v1 type.

This keeps event payload major version aligned with contract semantics.

---

## 47. Consumer Guidance

New consumers SHALL NOT depend on:

```text
tradeDocumentStatus
related_shipment_id
related_procurement_request_id
TradeDocument.storage_reference
trade-document.verified.v1
trade-document.rejected.v1
```

as the target architecture.

They SHALL use v2 and the later RTD-05/06 contracts where applicable.

---

## 48. Consequences

### Positive

- Corrects the original ownership mistake without erasing compatibility history.
- Makes immutable document versioning first-class before implementation.
- Prevents files from becoming document identity.
- Prevents verification from becoming lifecycle/compliance.
- Gives Trade Docs a scalable type and subject-association model.
- Enables multiple content representations with independent integrity.
- Aligns Shared, Trade Docs, Regulations, Pulse and Thamani architecture.
- Leaves later cross-engine and Customs workflow design space clean.

### Costs

- Two contract versions coexist before activation.
- Consumers must explicitly choose v2.
- v1 remains visible as historical scaffolding.
- Later RTD-05/06 work is still required before full Regulations integration.
- Dossier/Customs workflow contracts remain intentionally incomplete.

These costs are preferable to embedding known-wrong semantics into the first production Trade Docs implementation.

---

## 49. Rejected Alternatives

### A. Mutate v1 in place

Rejected.

It violates accepted Thamani architecture and removes a useful compatibility boundary.

### B. Keep v1 and implement around its defects

Rejected.

That would force Trade Docs to inherit CP ID minting, overloaded status, file-centric storage and missing version semantics.

### C. Put full CustomsCase and declaration workflow into v2 now

Rejected.

Those shapes are not yet sufficiently governed by the relevant later Trade Docs ADRs.

### D. Put DocumentRequirement into v2

Rejected.

That transfers Regulations semantics into Trade Docs and pre-empts RTD-05/06.

### E. Make document type a permanent enum

Rejected.

The real trade-document universe is too large and evolves independently from the base schema.

### F. Use one universal status

Rejected.

Lifecycle, verification, validity and authority submission are different state machines.

### G. Treat a document as a URI/file

Rejected.

A document is a semantic legal/business object with versions and multiple representations.

---

## 50. Final Decision

The canonical Shared contract evolution is:

```text
trade-document/v1
  preserved pre-activation scaffold

trade-document/v2
  canonical TDOC-aligned document foundation
```

The defining rule is:

> **Trade Docs owns durable document identity, immutable versions, documentary lifecycle, content-artifact association and document relationships. Shared v2 exposes those semantics without stealing regulatory meaning, platform identity, external legal authority or future cross-engine reference design.**
