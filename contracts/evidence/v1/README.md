# Evidence and verification contracts v1

**Authority:** ADR-BCP-023 (Organisation Evidence, Verification, Trust and Compliance Record Model), gate OEV-01.
**Runtime owner:** `baobab-platform/baobab-cp` owns the verification workflow and the evidence metadata (section 280). This package defines their shape only. Evidence binaries sit behind the approved storage boundary (section 281) and never appear in these contracts.

Evidence is not truth (section 6). This package keeps three things apart:

- **the evidence:** what material supports a claim, and where it came from;
- **the verification:** which checks were actually performed, and what they found;
- **the claim:** the proposition itself, and its current standing.

Assurance and compliance (sections 83-100) build on these, and are later gates.

## Files

- `domain.schema.json`: identifier grammars and closed vocabularies:
  - evidence types and statuses;
  - data classifications;
  - source classes;
  - claim types and statuses;
  - verification purposes, methods, outcomes and dimensions;
  - freshness states;
  - case and discrepancy statuses;
  - the `evidence:evr_…` canonical reference string.
- `evidence.schema.json`:
  - `EvidenceRecord`: what a piece of evidence is, what it concerns, its source and its protection. It points at an artifact, a source record or a credential, and never contains one.
  - `EvidenceReference`: its metadata-only view.
  - `EvidenceSource`: provenance, and the claim types and jurisdictions the source is authoritative for.
  - `EvidenceClaim`, and `EvidenceClaimSubmission`, which is what a caller may submit.
- `verification.schema.json`:
  - `VerificationCase`: the work done for one purpose.
  - `VerificationCheck`: one action actually performed.
  - `VerificationResult`: one claim's standing, established by the checks it cites.
  - `EvidenceDiscrepancy`: a material disagreement between sources.
- `source-registry.yaml`: the evidence sources the Control Plane recognises (today URSB, CIPC and applicant submissions), and exactly which claim types in which jurisdictions each is authoritative for. Evidence and checks may name only registered sources.
- Request schemas for the Control Plane's Verification routes (control-plane `openapi.yaml` 1.14.0, gate OEV-03). None accepts an identity, status or artifact the Control Plane derives:
  - `VerificationCaseCreateRequest` and `VerificationCaseTransitionRequest`;
  - `EvidenceRegistrationRequest`, for a source record or credential only (uploads are gate OEV-02);
  - `VerificationCheckRecordRequest` and `VerificationResultRecordRequest`;
  - `EvidenceDiscrepancyRecordRequest` and `EvidenceDiscrepancyTransitionRequest`;
  - and list responses.
- `lifecycle.yaml`: four state machines (evidence record, claim, verification case and discrepancy), with the actors allowed to perform each transition.
- `examples/organisation-admission-verification.json`: a Ugandan admission, following the evidence chain of section 178 end to end:
  - one claim verified against a registry lookup;
  - one claim conflicted and held as an open discrepancy;
  - one claim still self-asserted, with its evidence in quarantine.

## Rules the Control Plane enforces

- **Applicants never verify (sections 9, 169).** A claim submission has no status field and no verification field. An applicant's claim starts `SELF_ASSERTED`, and nobody checks or decides their own claim. No applicant transition in `lifecycle.yaml` makes anything available, verified, concluded or resolved.
- **Authority is per claim type and jurisdiction (sections 20-22).** A source verifies a claim only if its `trusted_for` names that claim type in the claim's jurisdiction. An `APPLICANT_SUPPLIED` source is trusted for nothing: it can corroborate, never verify.
- **Integrity is not truth (sections 35-36).** A check or result answers each verification dimension separately. VERIFIED needs both `CLAIM_MATCH` and `ISSUER_AUTHORITY` to pass.
- **No circular evidence (section 180).** A positive check cites independent evidence or a source record.
- **Standing comes from results.**
  - A claim is VERIFIED, NOT_VERIFIED or CONFLICTED only because its current `VerificationResult` says so.
  - A newer result supersedes an older one, and both remain (section 72).
  - NOT_VERIFIED means the evidence was insufficient, never that the claim is false (section 33).
- **Conflicts are recorded, not resolved silently (sections 74-76).** A CONFLICTED result names its discrepancy. Only a reviewer resolves one, with a reason.
- **Quarantine first (sections 238-239).** Uploaded content is reviewer-accessible only after scanning. A positive check never cites quarantined, restricted or destroyed evidence.
- **Metadata by default (section 270).** Lists return `EvidenceReference`s. Opening artifact content is a separate, authorised action (gate OEV-02).

## Relationship to existing contracts

- `organisation/v1` `evidenceReference` stays an opaque string, so existing references remain valid.
- A value in the `evidence:evr_…` form resolves to an `EvidenceRecord`.
- Events are not defined here. The events of section 230 are registered in the Shared event registry when the Control Plane first emits them. Like the existing organisation events, they carry identifiers and counts, never evidence (section 231).

## Versioning

Adding an enum value, a definition or an optional field is additive. Removing or renaming any of them, or narrowing a grammar, is breaking and needs a v2.
