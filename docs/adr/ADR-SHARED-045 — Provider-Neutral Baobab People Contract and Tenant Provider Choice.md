# ADR-SHARED-045 — Provider-Neutral Baobab People Contract and Tenant Provider Choice

**Status: Accepted — Normative Shared Contract Architecture, 8 November 2026.**
**Decision authority:** Baobab Platform product owner. **Contract steward:** Shared. **People semantic steward:** baobab-erp.
**Related:** Accepted ADR-SHARED-007/012/013/014/016/017/018/021/041, ADR-ERP-023 Addendum B, Shared PR #434.
**Acceptance scope:** contract semantics and governed namespace only. Provider qualification, runtime support, employee records, statutory rates, CP binding, payments and deployment remain separately gated.

## Decision

1. **Permanent tenant provider autonomy.** A legal employer may indefinitely retain its existing HRIS, payroll bureau, workforce, attendance, leave, payslip, benefits, statutory and document vendors, use Baobab People where qualified, or combine them function by function. Native People is **never** a mandatory dependency, source replacement or migration prerequisite for another Baobab capability. Market entry and legal verification remain independently checked at operation time.
2. **Canonical vocabulary, independent implementation.** Register `workforce` and `payroll` as governed capability domains. Publish `contracts/people/v1`, with exactly `workforce.employment.read`, `workforce.employment.manage`, `payroll.run.read` and `payroll.evidence.attest`. Each is DRAFT/EXPERIMENTAL. A catalogue entry defines meaning only, and it is illegal to infer an implemented provider, active binding, certification, statutory eligibility or grant from it. Later attendance/leave/filing/payslip/payrun-posting operations require separate accepted contracts; the other labels in `proposals/people-contracts/` are not automatically admitted.
3. **CP-owned selected authority.** Control Plane is the authority for tenant, legal employer, registered provider, capability entitlement/binding, jurisdiction, effective window and binding revision. IAM independently authenticates current Principal and purpose, with maker/checker and step-up as required. The `provider-selection` readback is **issued by CP**, never accepted as caller assertions or from an untrusted provider webhook. A legal employer may operate in several jurisdictions; Market, employment jurisdiction and tax residence are not interchangeable.
4. **One authoritative result at a time.** The employer must designate **one and only one** source of employment versions per scoped function and **one** authoritative payroll result for each employer/run/version. A shadow/parallel calculator is observational and cannot approve, post, file, pay or silently become the source of record. Historical runs retain original selected provider, rule digest, provenance, correction version and effective-date lineage across provider changes.
5. **Least information and lawful custody.** The first accepted shapes carry only opaque references, provider-selection evidence, qualified result receipts and metadata; no employee names, salary, deductions, tax IDs, benefits, payslips or bank information. Employer-specific personal record access, restricted documents, lawful basis, POPIA controls, retention, residency and cross-border transfer require separate evidence. Fail closed without leaking even protected-record existence to unauthorised principals.
6. **No native finance or payment coercion.** An external payroll service can remain independent of Baobab's iDempiere ledger and Baobab Payments. Explicit native journal handoff remains subject to ERP's posting veto, correct legal actor, cost centre, balanced entries, policy and period; independent bank release/settlement remains with authorised Payments/Treasury. Verifying a payroll receipt cannot bypass either boundary or certify statutory calculations.
7. **Adapter qualification and portability.** Real adapters may support API/event, encrypted source files or attested manual data where permitted. Each needs versioned capability/jurisdiction support, authenticated source provenance, idempotency, revoked/stale credential refusal, vendor-private ExternalReferences, incident recovery, reconciliation, lawful export and employer-approved effective-dated cutover. No silent failover, concurrent authoritative writes, duplicate pay consequences, vendor lock-in or related-tenant inheritance.
8. **Events remain producer-unassigned.** Versioned `workforce.employment.proposal-recorded.v1` and `payroll.evidence.receipt-verified.v1` are published as PROPOSED canonical shapes under separate workforce/payroll contexts. Shared acceptance assigns **no event producer**, evidence completeness, broker semantics or permission to trigger consequential consumers.

## Ownership matrix

| Area | Authority |
| --- | --- |
| Schemas, canonical capability keys and event semantics | Shared |
| Tenant, legal employer, jurisdiction-scoped provider choice, binding, grant, revision | CP |
| Principal identity and authentication assurance | IAM |
| Employment and payroll source of truth | Selected qualified native or external provider, per function and effective time |
| Adapter mapping and private vendor IDs | Registered adapter, under CP and legal-employer scope |
| Individual lawful employee records and retained evidence | Chosen custodian and tenant privacy policy |
| Aggregate accounting and native posting veto (if requested) | ERP |
| Bank disbursement and release (if requested) | Separate authorised treasury/payment provider |
| Jurisdiction-specific statutory verification | Independent experts, rule-pack attestation and approved Regulations evidence |

## Gate and negative acceptance

Schema validation confirms *shape*, never jurisdictional correctness or runtime permission. Before an implementation becomes supported and activated: verify current IAM/CP authority and legal employer; trusted provider identity; adapter credentials; fixed employer/market/jurisdiction/time window; effective-date cutover; replay and race fencing; signed receipts; historical export; restricted lawful purpose and retention; independently accepted ZA or UG rule vectors. BYOP-01…12 scenarios in ERP's provider-neutrality design are required.

Mandatory negatives include forged user-supplied tenant, employer or provider identity; expired/revoked binding; unrelated employer or jurisdiction; stale selection revision; unverified or conflicting payroll receipt; replay, lost commit, duplicate webhook, wrong retention policy, missing mandate, source outage and unapproved alternate provider fallback. A denied operation must not deny unrelated tenant services or expose PII.

## Consequences

**Accepted canonical semantics** make BYOP and portability durable. **Not accepted as runtime implementation:** ERP #126 experimental metadata, unqualified CDSoftware, any external payroll vendor, CP bindings, protected operational processing, live statutory filing or money movement. Future implementation PRs must add their own provider support evidence, pin Shared, pass owner-native conformance and obtain separate controlled activation.
