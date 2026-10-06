# Regulatory decision contracts v1

R-CAP-08 defines the canonical provider-neutral contract for:

```text
regulations.decision.evaluate
```

It specifies **what a Regulations provider must evaluate and return**. It does
not specify which policy engine, compiler, bundle format or runtime executes the
rules.

## Authority

```text
Control Plane
  caller-bound PlatformContext / capability authority

Regulations
  rule-set authority
  legal/knowledge-time semantics
  deterministic regulatory assessment
  RegulatoryDecision
  reasons / legal basis / enforcement class
  replay/provenance semantics

Owning domain engines
  regulated subjects
  facts/evidence objects referenced by pinned cross-engine references

Domain PEPs
  operational business-state enforcement
```

## Request

The request declares:

- opaque caller-bound `context_id`;
- regulatory question and assessment purpose;
- pinned regulated-subject references;
- regulated activities;
- bounded typed facts;
- pinned evidence references;
- pinned Regulations rule-set reference;
- explicit legal time and knowledge time;
- evaluation profile;
- requested assurance;
- enforcement-class ceiling;
- replay key.

The request carries **no tenant_id**. The resource server obtains trusted tenant
authority from caller-bound Control Plane context validation.

## Two identities: idempotency vs replay

```text
Idempotency-Key
    = this command occurrence

replay_key
    = this deterministic semantic input identity
```

The HTTP idempotency key prevents duplicate command creation.

The replay key participates in decision reproducibility and historical replay.
They are intentionally not interchangeable.

## Temporal model

`legal_time` asks:

> What law/regulatory state applies at this time?

`knowledge_time` asks:

> What verified regulatory knowledge was available/authorised at this time?

The provider must not silently replace either with wall-clock "now".

Profiles/purposes govern whether the requested times represent a current
assessment, historical replay or future simulation.

## Outcomes are not technical statuses

Valid regulatory outcomes are:

```text
SATISFIED
SATISFIED_WITH_REQUIREMENTS
UNSATISFIED
PROHIBITED
INDETERMINATE
NOT_APPLICABLE
```

Technical failures are **not** outcomes.

For example:

```text
EVALUATOR_UNDEFINED
EVALUATOR_PROTOCOL_ERROR
EVALUATOR_RUNTIME_ERROR
EVALUATOR_NOT_READY
```

must return RFC 9457 `application/problem+json` (normally 503), never:

```text
FALSE
UNSATISFIED
INDETERMINATE
```

This preserves the difference between "the regulatory state is indeterminate"
and "the evaluation infrastructure failed".

## Rule-set pinning

Consequential evaluation requires a pinned:

```text
owner_engine_id = baobab-regulations
object_type     = REGULATORY_RULE_SET
reference_mode  = IDENTITY_PINNED | VERSION_PINNED
```

plus the response `rule_set_fingerprint`.

Provider/runtime implementation may compile that rule set into Rego or another
deterministic executable representation, but those implementation artefacts do
not become the Shared domain contract.

## Facts and evidence

Facts are bounded typed assertions with an observation time.

Evidence is referenced by pinned cross-engine identity. Referencing another
engine's evidence does not transfer authority over the underlying object to
Regulations.

## Response

The response contains:

- pinned Regulations decision and assessment references;
- regulatory outcome;
- enforcement class;
- structured reason codes/messages;
- legal-basis references;
- evidence references;
- optional non-enforcing recommended disposition;
- pinned rule-set reference + fingerprint;
- evaluated/legal/knowledge times;
- provider-neutral provenance;
- replay identity.

## Enforcement boundary

`recommended_disposition` is advisory to the operational Policy Enforcement
Point.

```text
RegulatoryDecision
      !=
shipment/order state transition
```

Regulations remains a PDP. Trade, Logistics, ERP or another domain owner remains
the PEP for its operational state.

## Provider neutrality

The canonical contract deliberately contains no:

- OPA URL;
- Rego package/query;
- OPA decision_id;
- OPA bundle revision;
- compiler version;
- sidecar topology;
- AWS/Kubernetes deployment identifier.

Those may be retained in implementation/audit provenance underneath the
canonical decision without becoming capability semantics.

## R-CAP sequence

```text
R-CAP-08
Shared contract
      ↓
R-CAP-09
production evaluator implementation
      ↓
R-CAP-10
provider promotion only with complete evidence
```
