# ADR-SHARED-026 — Cross-Repository Regulations, Trade Docs and Pulse Conformance Architecture

**Status:** Accepted — Normative Cross-Repository Conformance Architecture  
**Date:** 2026-10-06  
**Repository:** baobab-platform/shared  
**Decision ID:** ADR-SHARED-026  
**Decision Type:** Cross-Repository Contract / Authority / Maturity Conformance  
**Implements:** RTD-10 from ADR-SHARED-019  
**Depends On:** ADR-SHARED-019, ADR-SHARED-020, ADR-SHARED-021, ADR-SHARED-022, ADR-SHARED-023, ADR-SHARED-024, ADR-SHARED-025  
**Participants:** baobab-regulations, baobab-trade-docs, baobab-pulse
**Refined By:** ADR-SHARED-027 §14 for post-census Regulations capability handling

---

## 1. Decision

RTD-10 establishes a machine-enforced cross-repository conformance system for
the Regulations ↔ Trade Docs ↔ Pulse programme.

Shared owns:

1. the canonical conformance profile schema;
2. the role policies;
3. the reusable validator;
4. the reusable CI workflow;
5. the meaning of a passing result.

Each participating repository owns:

1. its local .baobab/rtd-conformance.yaml;
2. an immutable Shared commit pin;
3. evidence paths for the maturity it actually has;
4. keeping its implementation inside its assigned bounded context.

The fundamental rule is:

> **A repository may declare evidence, but it may not declare the rules by which that evidence is judged.**

---

## 2. Why RTD-10 Exists

RTD-01 through RTD-09 created correct architecture and contracts across four
repositories. Without RTD-10, all repositories can remain individually green
while the platform relationship becomes collectively wrong.

~~~text
Shared says Regulations owns RegulatoryDecision
        │
        ├── Trade Docs could later implement legal-rule logic
        ├── Pulse could later copy RegulatoryDecision as its own aggregate
        └── Regulations could later create a shadow DocumentVersion
~~~

RTD-10 turns the relationship itself into testable policy.

---

## 3. Conformance Topology

~~~text
                         SHARED
                contract / policy authority
                         │
              ADR-SHARED-026 + schema
                         │
               rtd_conformance.py
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
  baobab-regulations  baobab-trade-docs  baobab-pulse
 REGULATIONS_AUTHORITY TRADE_DOCUMENT_   INTELLIGENCE_
                         AUTHORITY         CONSUMER
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 RTD-10 conformance
~~~

A consumer pins an immutable Shared commit, so the policy that judged a commit
is replayable.

---

## 4. Role and Maturity Matrix

| Role | Repository | Required RTD-10 v1 maturity |
|---|---|---|
| REGULATIONS_AUTHORITY | baobab-regulations | DOMAIN_RUNTIME |
| TRADE_DOCUMENT_AUTHORITY | baobab-trade-docs | ARCHITECTURE_ONLY |
| INTELLIGENCE_CONSUMER | baobab-pulse | IMPLEMENTED_CONSUMER |

Maturity is part of the assertion. A repository SHALL NOT raise its declared
maturity merely to look more complete.

---

## 5. What a PASS Means

A PASS means that, at the checked repository revision:

- required Shared contracts are pinned;
- repository evidence exists;
- the repository remains inside the accepted authority boundary;
- its declared maturity matches observable repository state;
- role-specific RTD invariants pass.

A PASS does not mean:

~~~text
deployed
production-ready
operationally healthy
certified
capability ACTIVE
tenant entitled
provider bound
SLA proven
security accreditation complete
~~~

RTD-10 is architecture/conformance evidence, not production certification.

---

## 6. Canonical Profile

Every participant SHALL carry:

~~~text
.baobab/rtd-conformance.yaml
~~~

The canonical schema is:

~~~text
contracts/rtd-conformance/v1/profile.schema.json
~~~

The profile contains only programme identity, repository identity, role,
maturity, immutable Shared pin, required contract paths and evidence paths.

It deliberately contains no skip, ignore, exception, custom-policy or
authority-override field. A consumer cannot weaken the platform boundary
through its own manifest.

---

## 7. Immutable Shared Pin

The profile SHALL pin a full 40-character Shared commit.

~~~text
consumer revision
      │
      └── rtd-conformance.yaml
               │
               └── Shared commit SHA
~~~

The validator SHALL execute from that exact Shared revision.

~~~text
repository revision
    +
Shared policy revision
    =
replayable conformance verdict
~~~

---

## 8. Required Contract Families

The Shared validator owns the minimum contract set for each role.

### Regulations

At minimum:

~~~text
control-plane/v1/domain.schema.json
cross-engine-reference/v1/domain.schema.json
events/v1/envelope.schema.json
regulatory-document-exchange/v1/domain.schema.json
regulatory-document-exchange/v1/events.schema.json
~~~

### Trade Docs

At minimum:

~~~text
control-plane/v1/domain.schema.json
cross-engine-reference/v1/domain.schema.json
events/v1/envelope.schema.json
trade-document/v2/domain.schema.json
trade-document/v2/events.schema.json
regulatory-document-exchange/v1/domain.schema.json
regulatory-document-exchange/v1/events.schema.json
~~~

### Pulse

At minimum:

~~~text
control-plane/v1/domain.schema.json
cross-engine-reference/v1/domain.schema.json
events/v1/envelope.schema.json
regulatory-document-exchange/v1/domain.schema.json
regulatory-document-exchange/v1/events.schema.json
trade-document/v2/domain.schema.json
trade-document/v2/events.schema.json
~~~

A consumer may declare more contracts but SHALL NOT omit the role minimum.

---

## 9. Regulations Authority Conformance

baobab-regulations SHALL prove that it remains the regulatory meaning
authority.

RTD-10 requires that:

- RegulatoryDecision remains a Regulations domain object;
- Regulations does not define canonical TradeDocument, DocumentVersion,
  ContentArtifact, DocumentDossier, CustomsCase, CustomsDeclaration or
  AuthorityResponse aggregates;
- Regulations does not define Pulse-owned Insight, Opportunity, Forecast,
  Recommendation or EvidenceSet aggregates;
- Regulations does not directly import Pulse or Trade Docs runtime packages;
- ADR-REG-0026 and ADR-REG-0027 retain the RTD-03 ownership correction;
- repository-local pre-Shared evaluation event schemas remain explicitly v0;
- those local v0 schemas do not claim canonical com.baobab-platform producer authority;
- regulations capability declarations remain proposed until the separate
  capability census and canonical catalogue process promotes them.

~~~text
Regulations owns regulatory meaning
        !=
Regulations owns documentary workflow
~~~

---

## 10. Trade Docs Authority Conformance

Trade Docs currently declares ARCHITECTURE_ONLY.

RTD-10 SHALL therefore prove the absence of a falsely claimed runtime.

A PASS requires:

- accepted Trade Docs boundary ADRs;
- README disclosure that runtime implementation has not started;
- no src runtime tree;
- no real capability-provider declaration;
- no locally forked Shared trade-document or regulatory-document-exchange contracts;
- explicit separation of verification and regulatory sufficiency;
- explicit recognition that Regulations owns requirement/satisfaction authority;
- explicit recognition that Shared producer activation is not evidence that a
  runtime/outbox/broker publisher already exists.

~~~text
Shared producer authority
        !=
deployed Trade Docs publisher
~~~

When runtime implementation begins, ARCHITECTURE_ONLY SHALL fail by design
until the conformance policy and repository maturity are deliberately evolved.

---

## 11. Pulse Intelligence Consumer Conformance

Pulse SHALL prove that it remains an asynchronous intelligence consumer.

RTD-10 requires:

- contracts.lock.yaml pinned to the same Shared revision as the RTD profile;
- required RTD-05/06/07/08 contract families in that lock;
- byte-identical vendored fixtures for the consumed Shared contracts;
- no foreign Regulations or Trade Docs canonical aggregates in Pulse domain code;
- the RTD-09 upstream projector;
- all five approved upstream event families;
- logical producer binding to baobab-regulations and baobab-trade-docs;
- no HTTP, direct database, Haystack, Qdrant or direct sibling-engine runtime
  dependency in the ingestion projector;
- UpstreamFactProjection remains a read/value projection rather than a
  foreign canonical aggregate;
- event deduplication remains based on canonical CloudEvents source + id;
- future Pulse-owned event naming uses intelligence rather than pulse;
- no premature intelligence capability-provider claim before the capability census.

~~~text
Pulse consumes authority
        !=
Pulse absorbs authority
~~~

---

## 12. Authority Invariants Preserved

RTD-10 mechanically protects the programme's central distinctions:

~~~text
DocumentRequirement
        !=
TradeDocument

TradeDocument
        !=
DocumentVersion

DocumentVersion VERIFIED
        !=
Requirement SATISFIED

Evidence OFFERED
        !=
Evidence ACCEPTED

Pulse projection
        !=
foreign canonical aggregate

event producer authority
        !=
runtime deployment evidence
~~~

---

## 13. Cross-Engine References

ADR-SHARED-021 remains authoritative.

References preserve owner identity and historical pinning semantics.

~~~text
reference another engine
        !=
own another engine's object
~~~

RTD-10 therefore treats owner-preserving references as an architectural
requirement, especially for Pulse's analytical projections of Regulations and
Trade Docs facts.

---

## 14. No Direct Cross-Engine Database Access

The architectural rule remains:

> No RTD engine may read or mutate another RTD engine's database directly.

RTD-10 v1 detects obvious source/import coupling. Future production-hardening
work may add deployment, network, credential and database-policy evidence.

The inability of a static check to see every possible deployment mistake does
not weaken the architectural rule.

---

## 15. Event Authority

Shared remains the event authority.

~~~text
regulations.*
    canonical producer = baobab-regulations

documents.*
    canonical producer = baobab-trade-docs

intelligence context
    RESERVED
    no Pulse-produced event activated by RTD-10
~~~

A consumer repository SHALL NOT contradict that registry.

---

## 16. Capability Authority

RTD-10 does not perform the planned capability census.

Current state remains:

~~~text
regulations namespace
    registered

intelligence namespace
    registered

specific regulations.* capability keys
    not promoted by RTD-10

specific intelligence.* capability keys
    not promoted by RTD-10
~~~

A conformance PASS does not create a capability, provider, binding, grant or
entitlement.

---

## 17. Evidence Paths

Profiles list reviewable evidence paths, for example:

| Repository | Typical ADR evidence | Typical executable evidence |
|---|---|---|
| Regulations | ADR-REG-0026/0027 | RegulatoryDecision source + architecture tests |
| Trade Docs | ADR-TDOC-0001/0002 | none while ARCHITECTURE_ONLY |
| Pulse | ADR-PULSE-013 | upstream projector + RTD-09 architecture/contract tests |

Evidence paths provide traceability. They do not define the policy.

---

## 18. Reusable Workflow

Shared publishes:

~~~text
.github/workflows/rtd-cross-repository-conformance.yml
~~~

Each participant calls it by immutable Shared SHA.

~~~text
checkout caller
      │
read RTD profile
      │
checkout exact Shared pin
      │
install validator runtime
      │
execute Shared-owned role policy
      │
PASS / FAIL
~~~

The validator is not copied into engines.

---

## 19. Why Execution Is Distributed

A single central job cloning every sibling repository would require broad
cross-repository credentials and make one repository's ordinary CI depend on
the availability and permission model of all others.

RTD-10 therefore centralizes policy and distributes execution.

Benefits:

- least-privilege access;
- failure appears in the repository that drifted;
- independent PR review;
- immutable policy pinning;
- no organization-wide read token required for every run.

---

## 20. Foundation Relationship

Foundation and RTD-10 are complementary.

~~~text
Foundation
    repository engineering conformance

RTD-10
    cross-engine domain-authority conformance
~~~

A repository may pass Foundation and fail RTD-10. That is expected.

---

## 21. Maturity Transition

When Trade Docs implementation begins:

~~~text
ARCHITECTURE_ONLY
        │
        │ src/runtime appears
        ▼
RTD-10 FAIL
        │
        ▼
governed maturity transition
        │
        ├── contracts.lock.yaml
        ├── runtime source
        ├── runtime tests
        ├── outbox/event evidence
        └── evolved Shared conformance policy
~~~

The failure is a useful architectural signal and SHALL NOT be suppressed with
a local ignore flag.

---

## 22. Relation to RTD-01 Through RTD-09

| Step | What RTD-10 protects |
|---|---|
| RTD-01 | Shared authority boundary remains governing |
| RTD-02 | Pulse does not reclaim regulatory/document authority |
| RTD-03 | Regulations retains the requirement/document split |
| RTD-04 | Trade Docs targets Shared v2 rather than legacy v1 |
| RTD-05 | cross-engine owner identity remains explicit |
| RTD-06 | requirement/evidence choreography remains separated |
| RTD-07 | documents producer authority is not mistaken for runtime deployment |
| RTD-08 | Regulations producer authority and local-v0 quarantine remain distinct |
| RTD-09 | Pulse remains asynchronous and non-enforcing |
| RTD-10 | these constraints become repository-local CI obligations |

---

## 23. Failure Semantics

Examples of hard failures:

~~~text
Pulse adds RegulatoryDecision aggregate
    → FAIL

Regulations imports baobab_trade_docs runtime
    → FAIL

Trade Docs gains src/ while still ARCHITECTURE_ONLY
    → FAIL

Pulse contract lock pin differs from RTD profile pin
    → FAIL

required Shared contract omitted from profile
    → FAIL

Trade Docs copies canonical Shared TradeDocument schemas locally
    → FAIL
~~~

A failure is treated as architecture drift until corrected or deliberately
superseded by a new Shared decision.

---

## 24. No Local Exception Mechanism

RTD-10 v1 defines no repository-local override or suppression.

If a legitimate architecture change invalidates a rule:

1. update the governing Shared ADR/contract;
2. update the Shared validator;
3. review the platform-wide consequence;
4. then update consumers.

This keeps one authority for the relationship.

---

## 25. Security

The reusable workflow needs read-only repository contents.

It does not require cloud credentials, deployment credentials, database
credentials or production secrets.

A SHARED_READ_TOKEN may be supplied where the caller's GitHub token cannot
read Shared.

---

## 26. Versioning

The profile begins at:

~~~text
schema = baobab-rtd-conformance
version = 1.0
programme = RTD-10
~~~

Consumers additionally pin the exact Shared commit so conformance verdicts are
replayable even when compatible policy evolves.

---

## 27. RTD-10 v1 Invariants

~~~text
INV-RTD10-001 Shared owns the cross-repository conformance rules.
INV-RTD10-002 Consumers declare evidence but cannot weaken Shared policy.
INV-RTD10-003 Every participant pins an immutable Shared commit.
INV-RTD10-004 Validation runs from exactly that Shared commit.
INV-RTD10-005 Only Regulations may canonically define RegulatoryDecision in the RTD group.
INV-RTD10-006 Regulations does not own TradeDocument/DocumentVersion/customs-workflow canonicals.
INV-RTD10-007 Trade Docs does not own regulatory requirement/satisfaction authority.
INV-RTD10-008 ARCHITECTURE_ONLY Trade Docs cannot silently acquire a runtime src tree.
INV-RTD10-009 Shared event producer authority is not runtime publication evidence.
INV-RTD10-010 Pulse does not define Regulations or Trade Docs canonical aggregates.
INV-RTD10-011 Pulse consumes the approved upstream facts asynchronously.
INV-RTD10-012 Pulse projector has no synchronous upstream/database/provider dependency.
INV-RTD10-013 Pulse fixtures equal contracts at the pinned Shared revision.
INV-RTD10-014 Pulse preserves canonical CloudEvents source + id occurrence identity.
INV-RTD10-015 Future Pulse event names use intelligence, not pulse.
INV-RTD10-016 RTD-10 promotes no regulations.* or intelligence.* capability.
INV-RTD10-017 Cross-engine references preserve owner authority.
INV-RTD10-018 Document verification is not regulatory satisfaction.
INV-RTD10-019 Evidence offered is not evidence accepted.
INV-RTD10-020 RTD repositories do not use sibling runtime imports as persistence shortcuts.
INV-RTD10-021 Repository maturity is itself a conformance assertion.
INV-RTD10-022 A PASS is not production certification.
INV-RTD10-023 No consumer-local ignore/override mechanism exists.
INV-RTD10-024 Maturity transitions require deliberate Shared policy evolution.
~~~

---

## 28. Rejected Alternatives

### A. One central CI job cloning all repositories

Rejected as the sole mechanism because it creates broad credential and
availability coupling.

### B. Copy the conformance script into each engine

Rejected because policy would fork.

### C. Let each repository define its own invariants

Rejected because a consumer could remove the rule it violates.

### D. Treat Trade Docs as implemented because Shared events are ACTIVE

Rejected because canonical producer authority and deployed publisher evidence
are separate facts.

### E. Use RTD-10 to promote capabilities

Rejected. Capability census and catalogue governance remain separate.

### F. Equate conformance with production readiness

Rejected. RTD-10 is one layer of architectural evidence.

---

## 29. Completion Sequence

RTD-10 is complete only when:

~~~text
Shared
  ADR-SHARED-026
  profile schema
  validator
  reusable workflow
  self-tests
        │
        ▼
Shared merged
        │
        ├── Regulations profile + workflow PASS
        ├── Trade Docs profile + workflow PASS
        └── Pulse profile + workflow PASS
~~~

Consumer profiles SHALL pin the resulting Shared merge commit, never the
feature branch.

---

## 30. Final Decision

~~~text
Regulations determines regulatory meaning.

Trade Docs owns documentary truth and workflow.

Pulse derives intelligence from authorised facts.

Shared defines how those boundaries are tested.

Each repository proves its own side against the same immutable policy.
~~~

> **RTD-10 makes the relationship between the engines executable architecture: a repository may evolve independently, but it may not silently cross the authority boundary.**
