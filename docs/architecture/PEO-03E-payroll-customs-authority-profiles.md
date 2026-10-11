# PEO-03E — South African employer and customs evidence profiles

**Status:** source *reservation only*, no live verification transport certified.
**Architecture:** ADR-BCP-023, ADR-BCP-026, ADR-SHARED-019/021/022/028.
**Implementing engine:** baobab-cp for Organisation evidence and verification
case; baobab-regulations for legal requirements and decisions; Trade Docs for
document ownership; ERP/Trade/TMS for operational enforcement; Pulse for
non-authorising analysis.

## 1. Do not mistake registration for compliance

| Claim category | Authoritative source candidate | Distinct from |
|---|---|---|
| PAYE employer registration | SARS | EMP201 submission, payment, tax compliance |
| UIF contribution registration | SARS or UIF office (as applicable) | UIF contributions paid and worker eligibility |
| SDL employer registration | SARS | statutory SDL liability, calculation and payment |
| Customs importer/exporter registration | SARS Customs | a shipment release, import permit or clearance |
| Customs operator authorisation | competent customs authority | incorporation, tax number or self-declared importer |
| HS tariff classification | jurisdiction's competent customs/Regulations rule set | organisation identity or customs trader registration |

**None** is inferred from incorporation with CIPC, a self-entered number,
an uploaded certificate, a valid TCS PIN, or payroll/invoice records. No
registration source is entitled to certify filing, employer remittance or
tax-payment status unless the approved authority provides that *separate*
claim and verifiable method.

SARS explains that UIF registration may occur via SARS or the UIF office.
Accordingly both source roles are reserved, while the actual source must be
identified by the verification method and operator authority. See
https://www.sars.gov.za/types-of-tax/pay-as-you-earn/registering/

## 2. Non-activating source reservation

Shared evidence/v1 claimType now distinguishes PAYE, UIF, SDL and customs
trader/authorisation claims. The source registry has five new separate
* SUSPENDED * sources. Neither Baobab nor any consumer can claim that
its existence denotes a real subscription, API, approved evidence policy or
an active verification. The existing evidence-source contract forbids
unregistered and suspended sources from supporting VERIFIED.

A future activation must demonstrate a lawful acquisition method,
appropriate applicant consent/representative mandate, independent verifier,
approved origin, source-record reference, response digest, freshness, source
certification, revoke/expire path, case+subject+purpose binding and
idempotent immutable observation acceptance; credentials and SARS taxpayer
PINs are **never** returned as evidence fields.

The source registry is a **claim-type trust allowlist**, not an approval
of an Organisation or a regulatory status.

## 3. Relationship to legal-time customs and HS classification

**A company's customs trader registration is an Organisation claim. HS
classification is a commodity-specific legal determination.** The latter
cannot be represented as a generic Organisation evidence claim or reused
unchanged across countries, tariff editions, goods or dates.

The lawful trade sequence is:

```text
Trade product/consignment (product description, attributes, origin, market)
    -> candidate HS code (Pulse may suggest with references)
    -> Regulations evaluates applicable national tariff/HS edition,
       interpretative rules, notes, rulings and legal/knowledge time
    -> a RegulatoryDecision states outcome, uncertainty and rule references
    -> Trade Docs attaches the decision reference to the correct
       declaration/document version
    -> Trade / TMS applies the transaction policy at point of use
    -> an actual sovereign customs release remains external authority
```

Existing Shared RTD-06 evidence exchange (ADR-SHARED-022) and the
`regulations.decision.evaluate` contract (ADR-SHARED-028) are the intended
authority paths. Do **not** register `HS_CLASSIFICATION` as an
Organisation EvidenceClaim or allow Pulse to generate an authoritative
RegulatoryDecision. WCO HS data, classification opinions and national tariff
schedules must be edition/time pinned, and a ruling's applicability to
specific product facts must be reviewed.

South Africa's SARS tariff determinations:
https://www.sars.gov.za/latest-news/customs-and-excise-tariff-classification/
WCO HS official interpretation:
https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/tools-to-assist-with-the-classification-in-the-hs.aspx

## 4. Engine responsibilities and data minimisation

- **Control Plane** owns the Organisation claim, authorised source observation,
  verification-case evidence chain, admission and legal-actor binding. It does
  not calculate payroll or assign HS codes.
- **Regulations** owns requirement applicability, temporal legal interpretation
  and decisions; it consumes references, never copies all personal data.
- **ERP** owns payroll/GL and can request current employer statutory readiness
  before legally consequential activities. ERP accounting facts do not
  establish an external statutory registration.
- **Trade Docs** owns document/version/status and issuer communications;
  documentary verification does not equal a customs permission or Regulations
  sufficiency assessment.
- **Pulse** can detect changed official material, suggest candidates and
  surface disputed classifications in a labelled decision-support output.
  It must never emit a claim standing or government authorisation.

Each consumer must receive its own minimum necessary scoped decision with
canonical subject, jurisdiction, source reference, observation version,
policy, freshness and revocation correlation. Tenant access and POPIA
boundaries continue to apply.

## 5. No-AWS acceptance gates

- Shared contract tests prevent PAYE/UIF/SDL/customs source conflation.
- Source reservation defaults SUSPENDED and does not change CIPC authority.
- CP uses an explicitly authorised source and durable verified observation
  before a positive OEV-03 result; synthetic fixtures cannot become production
  evidence (PEO-03C/D).
- ERP, Trade, Trade Docs and Regulations PEP integrations are future gates,
  and must fail closed when required evidence is absent/stale.
- No live provider / PSP / customs / SARS verification certification is claimed.
