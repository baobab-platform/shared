# ADR-SHARED-028 — Canonical Regulatory Decision Evaluation Contract

**Status:** Accepted — R-CAP-08 Contract Authority  
**Decision ID:** ADR-SHARED-028  
**Domain:** regulations  
**Semantic Owner:** baobab-regulations  
**Contract Authority:** baobab-platform/shared  
**Date:** 2026-10-06  
**Implements:** R-CAP-08  
**Depends On:** ADR-SHARED-017, ADR-SHARED-021, ADR-SHARED-022, ADR-SHARED-024, ADR-SHARED-027

---

## 1. Decision

Shared SHALL catalogue:

```text
regulations.decision.evaluate
```

as the canonical provider-neutral capability for deterministic regulatory
decision evaluation.

Contract major 1 SHALL be defined by:

```text
contracts/regulatory-decision/v1/domain.schema.json
contracts/regulatory-decision/v1/regulations.openapi.yaml
```

The contract SHALL describe Regulations domain semantics and SHALL NOT expose a
specific policy runtime, compiler or deployment technology.

---

## 2. Why this capability is separate

The existing canonical capabilities answer narrower documentary questions:

```text
regulations.requirement.resolve
regulations.evidence.assess
```

They do not express the broader decision problem:

```text
Given:
  a regulatory question,
  trusted platform context,
  pinned regulated subjects,
  regulated activities,
  bounded facts,
  pinned evidence,
  pinned rule-set identity,
  legal time,
  knowledge time,
  evaluation/assurance profile

What deterministic RegulatoryDecision does Regulations reach?
```

That broader question is now stable enough to contract before R-CAP-09
implements a production evaluator.

---

## 3. Authority boundary

```text
Control Plane
    caller-bound PlatformContext
    capability/grant/binding/runtime resolution authority

Regulations
    rule-set authority
    legal-time / knowledge-time semantics
    deterministic evaluation
    assessment
    RegulatoryDecision
    reason structure
    enforcement class
    replay identity

Other domain engines
    canonical subjects
    evidence/fact objects they own

Operational domain PEP
    shipment/order/payment/business-state enforcement
```

A decision response does not grant Regulations authority to mutate another
engine's operational aggregate.

---

## 4. Provider neutrality

The contract SHALL NOT contain:

```text
OPA
Rego
bundle URL
package/query path
compiler build
sidecar identity
Kubernetes pod
AWS resource
vendor evaluator ID
```

Those are implementation or execution provenance.

The semantic chain is:

```text
canonical rule set
    ↓
provider implementation
    ↓
deterministic evaluation
    ↓
canonical RegulatoryDecision
```

Replacing the evaluator must not rename the capability or change the canonical
decision semantics.

---

## 5. Regulatory question is explicit

Every request SHALL declare a regulatory question.

The initial vocabulary is:

```text
MAY_TRANSACTION_PROCEED
WHAT_OBLIGATIONS_APPLY
WHAT_REQUIREMENTS_REMAIN
WHAT_DOCUMENTS_ARE_REQUIRED
IS_REQUIREMENT_SATISFIED
IS_ACTION_PROHIBITED
IS_EXPLICIT_PERMISSION_AVAILABLE
WHAT_DUTY_OR_AMOUNT_APPLIES
WHAT_REGULATORY_GAPS_EXIST
WHAT_CHANGED
WHAT_WOULD_APPLY_AT_FUTURE_TIME
```

This prevents a generic "is this compliant?" endpoint from obscuring the
decision being requested.

---

## 6. Explicit temporal semantics

Every request SHALL carry:

```text
legal_time
knowledge_time
```

They are different dimensions.

`legal_time` identifies the time at which law/regulatory effect is evaluated.

`knowledge_time` identifies the verified regulatory knowledge perspective
authorised for the evaluation.

The provider MUST NOT silently substitute wall-clock now for either field.

---

## 7. Rule-set identity

Every request SHALL carry a pinned Regulations-owned:

```text
REGULATORY_RULE_SET
```

reference.

Every response SHALL repeat the pinned rule-set reference and provide its
SHA-256 semantic fingerprint.

A current/mutable rule-set reference is not sufficient for a consequential
decision.

---

## 8. Facts

Facts SHALL be bounded typed assertions.

A fact contains:

```text
fact_code
value
observed_at
optional unit/currency
optional pinned source reference
```

Facts are input assertions.

They SHALL NOT encode legal conclusions such as:

```text
COMPLIANT = true
ALLOW = true
RULE_APPLIES = true
```

unless such a value is itself a canonical externally owned fact under a
separately governed contract.

---

## 9. Evidence and subjects

Subject and evidence references SHALL preserve:

```text
owner engine
object type
object identity/version
scope
tenant when tenant-scoped
historical pinning
```

using ADR-SHARED-021.

A reference never transfers authority over the referenced object.

---

## 10. Tenant authority

The request SHALL NOT contain `tenant_id`.

The trusted tenant is derived from:

```text
authenticated caller
    +
caller-bound PlatformContext validation
```

Every nested tenant-scoped reference must agree with that trusted tenant.

Well-formed request JSON is not authorisation.

---

## 11. Assessment purpose and profile

The request SHALL declare an assessment purpose and evaluation profile.

Initial purposes:

```text
TRANSACTION_DECISION
COMPLIANCE_REVIEW
LEGAL_REVIEW
AUDIT
HISTORICAL_REPLAY
FUTURE_SIMULATION
```

Initial profiles:

```text
ADVISORY
STANDARD
HIGH_ASSURANCE
HISTORICAL_REPLAY
FUTURE_SIMULATION
SHADOW
```

A provider may impose stricter governance on combinations of purpose, profile,
time and enforcement ceiling.

---

## 12. Assurance and enforcement ceiling

The request SHALL carry:

```text
requested_assurance
requested_enforcement_class_ceiling
```

The initial enforcement classes remain:

```text
E0 informational
E1 advisory
E2 review gate
E3 conditional deterministic
E4 high assurance
```

The ceiling limits the consequence class the caller is asking Regulations to
produce. It does not force Regulations to produce that class.

---

## 13. Decision outcome

The canonical outcome vocabulary is:

```text
SATISFIED
SATISFIED_WITH_REQUIREMENTS
UNSATISFIED
PROHIBITED
INDETERMINATE
NOT_APPLICABLE
```

These are regulatory conclusions.

---

## 14. Technical failure is not outcome

The following are implementation/runtime failures:

```text
EVALUATOR_UNDEFINED
EVALUATOR_PROTOCOL_ERROR
EVALUATOR_RUNTIME_ERROR
EVALUATOR_NOT_READY
RULE_SET_UNAVAILABLE
AUTHORITY_UNAVAILABLE
```

They SHALL be returned as RFC 9457 ProblemDetails.

Therefore:

```text
INDETERMINATE
    !=
evaluator failed
```

and:

```text
HTTP 200
    !=
valid evaluator result
```

unless the canonical response schema validates.

---

## 15. Decision reasons

A RegulatoryDecision SHALL expose structured reasons.

A reason includes:

```text
stable reason code
human-readable message
legal-basis references
rule-version references
evidence references
```

The message is explanatory projection.

The code and references carry durable machine/audit semantics.

---

## 16. Legal basis and evidence

Responses SHALL preserve both:

```text
legal_basis_references[]
evidence_references[]
```

at decision level.

Individual reasons MAY narrow those sets.

This enables the decision to be traced toward:

```text
law/rule
    +
facts/evidence
```

without embedding foreign domain payloads in the decision.

---

## 17. Recommended disposition

A response SHALL explicitly carry either:

```text
recommended_disposition
```

or:

```text
null
```

A recommendation is non-enforcing.

```text
RegulatoryDecision
    !=
operational transition
```

A domain PEP decides whether and how its own aggregate changes.

---

## 18. Idempotency and replay are distinct

The HTTP command uses:

```text
Idempotency-Key
```

The semantic request uses:

```text
replay_key
```

They answer different questions.

```text
Idempotency-Key
    "Have I already executed this command occurrence?"

replay_key
    "Which deterministic semantic input set is this decision/replay about?"
```

Implementations MUST NOT collapse them into one field merely because both may
be used for deduplication.

---

## 19. Replay identity

The response SHALL include:

```text
replay_key
input_fingerprint
rule_set_fingerprint
```

The input fingerprint is the provider-neutral canonical semantic input
fingerprint for the decision.

It MUST NOT be a hash of transient transport metadata such as bearer tokens,
HTTP connection details or deployment identity.

---

## 20. Provenance

Canonical provenance SHALL include only provider-neutral reproducibility facts:

```text
contract major
input fingerprint
pinned rule-set reference
rule-set fingerprint
evaluation profile
```

Implementation-specific provenance MAY additionally retain:

```text
compiler revision
compiled artefact hash
OPA bundle revision
OPA decision_id
runtime build
OpenTelemetry identifiers
```

outside the canonical decision contract.

---

## 21. Side effects

The capability is a Regulations PDP operation.

It MAY persist:

```text
RegulatoryAssessment
RegulatoryDecision
decision replay material
canonical Regulations event intent
audit provenance
```

It SHALL NOT directly mutate:

```text
shipment
order
payment
TradeDocument
ERP transaction
inventory
other domain-owned operational state
```

---

## 22. HTTP surface

Contract major 1 uses:

```text
POST /decisions/evaluate
operationId: evaluateRegulatoryDecision
```

Headers:

```text
Authorization: Bearer <workload token>
Idempotency-Key
X-Correlation-ID?
traceparent?
```

No tenant header is authoritative.

---

## 23. Success semantics

A successful command may return:

```text
201 new decision
200 idempotent replay / existing committed decision
```

Both responses use the same canonical decision response schema.

---

## 24. Error semantics

Canonical technical classes include:

| HTTP | Meaning |
|---|---|
| 400 | malformed/semantically invalid deterministic request |
| 401 | workload authentication failed |
| 403 | caller/context/reference/capability authority denied |
| 404 | exact pinned authority cannot resolve requested object/context |
| 409 | pinned version/fingerprint/replay/idempotency conflict |
| 503 | required authority/rule-set/evaluator unavailable or not ready |

A provider MAY use more specific stable ProblemDetails `code` values while
preserving these classes.

---

## 25. Capability governance

Shared SHALL catalogue:

```text
regulations.decision.evaluate
```

with:

```text
owner:     baobab-regulations
lifecycle: DRAFT
maturity:  EXPERIMENTAL
contract major: 1
```

Contracting the capability does not assert that any provider implements it.

---

## 26. R-CAP sequencing

```text
R-CAP-08
contract semantics
      ↓
R-CAP-09
production evaluator implementation
      ↓
R-CAP-10
provider support promotion with full evidence
```

R-CAP-09 SHALL conform to this contract.

It SHALL NOT rewrite this contract merely to fit the chosen evaluator.

---

## 27. Rejected alternatives

### 27.1 Expose OPA directly

Rejected.

```text
POST /v1/data/<rego-package>
```

is an evaluator API, not a Baobab regulatory decision contract.

### 27.2 Boolean allow/deny

Rejected.

Regulatory semantics include:

```text
requirements
prohibition
indeterminacy
non-applicability
assurance
reason/legal basis
```

that cannot be faithfully represented by one Boolean.

### 27.3 Implicit current time

Rejected.

It destroys historical/legal reproducibility.

### 27.4 Mutable current rule set

Rejected for consequential evaluation.

### 27.5 Arbitrary JSON facts

Rejected for the canonical v1 boundary.

Facts require bounded codes, scalar values and observation time.

### 27.6 Treat evaluator failure as INDETERMINATE

Rejected.

It hides infrastructure failure as legal uncertainty.

### 27.7 Let Regulations enforce operational state

Rejected.

Regulations remains PDP; domain owners remain PEPs.

---

## 28. R-CAP-08 exit criteria

R-CAP-08 is complete when Shared proves:

1. `regulations.decision.evaluate` is catalogued;
2. request schema resolves;
3. response schema resolves;
4. ProblemDetails error schema resolves;
5. request example validates;
6. response example validates;
7. request has no `tenant_id`;
8. rule-set reference is pinned and Regulations-owned;
9. legal time and knowledge time are explicit;
10. outcome excludes technical failure values;
11. replay identity is explicit;
12. OpenAPI exposes the canonical operation;
13. capability remains DRAFT/EXPERIMENTAL;
14. no provider implementation/activation is inferred.

---

## 29. Final decision

> **Shared defines `regulations.decision.evaluate` as a provider-neutral,
> deterministic regulatory decision capability whose semantics are pinned by
> explicit question, context, rule-set, legal time, knowledge time, facts,
> evidence, assurance and replay identity. The contract owns regulatory meaning;
> R-CAP-09 may choose an evaluator, but the evaluator does not get to define the
> contract.**
