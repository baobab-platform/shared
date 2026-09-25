#!/usr/bin/env python3
"""Validate the ADR-BCP-017 admission/v1 contracts.

Real JSON Schema Draft 2020-12 validation with every cross-schema $ref
resolved against the contracts in this repository:

  1. each schema is a valid Draft 2020-12 schema, its $id matches its file
     name, it defines exactly the $defs it is responsible for, and every
     $ref resolves;
  2. every example record validates against its $def, and the examples are
     coherent (applications and their decisions agree, an approved market
     scope lies within the requested markets, INTERNAL carries evidence);
  3. lifecycle.yaml is a sound state machine over applicationStatus, and
     applicants can never decide;
  4. negative fixtures prove the load-bearing rules reject bad data,
     above all that applicants cannot write server-authoritative fields;
  5. asyncapi.yaml registers exactly the section 40 events, composed with
     the canonical envelope, and payloads carry no names, text, evidence
     or principals;
  6. contracts.lock.yaml registers exactly these files, and the
     authorization scope registry defines the admission scopes for humans
     only, with review and decision privileged and distinct.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-admission-contracts.py
"""

from __future__ import annotations

import copy
import json
import re
import sys
from collections import deque
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PKG = CONTRACTS / "admission" / "v1"
BASE_URI = "https://contracts.baobab-platform.com/admission/v1/"

RESPONSIBILITIES = {
    "application.schema.json": {
        "clientApplicationId", "applicationReference", "applicationStatus", "applicationChannel", "principalId",
        "countryCode", "applicantIdentifier", "applicantAddress", "authorisedRepresentative", "declaredLegalEntity",
        "ApplicantOrganisationProfile", "BusinessRequirements", "requestedMarket", "applicationEvidenceType",
        "ApplicationEvidence", "InformationRequest", "DecisionSummary", "ClientApplication", "ClientApplicationDraft",
        "InformationRequestCommand", "ApplicantResponseCommand", "ClosureCommand",
    },
    "decision.schema.json": {
        "admissionDecisionId", "admissionDecisionValue", "subscriptionType", "isolationStrategy",
        "InternalEligibilityEvidence", "AdmissionDecisionRequest", "AdmissionDecision",
    },
    "events.schema.json": {
        "ClientApplicationCreated", "ClientApplicationSubmitted", "ClientApplicationInformationRequested",
        "ClientApplicationWithdrawn", "ClientApplicationApproved", "ClientApplicationRejected",
    },
}
LOCKED_FILES = [*RESPONSIBILITIES, "lifecycle.yaml"]

EVENT_TYPES = {
    "com.baobab-platform.control-plane.client-application.created.v1": "ClientApplicationCreated",
    "com.baobab-platform.control-plane.client-application.submitted.v1": "ClientApplicationSubmitted",
    "com.baobab-platform.control-plane.client-application.information-requested.v1": "ClientApplicationInformationRequested",
    "com.baobab-platform.control-plane.client-application.withdrawn.v1": "ClientApplicationWithdrawn",
    "com.baobab-platform.control-plane.client-application.approved.v1": "ClientApplicationApproved",
    "com.baobab-platform.control-plane.client-application.rejected.v1": "ClientApplicationRejected",
}
ENVELOPE_REF = "../../events/v1/envelope.schema.json"
FORBIDDEN_EVENT_FIELDS = {
    "legal_name", "trading_names", "organisation_profile", "registration_identifiers", "authorised_representative",
    "reason", "message", "response", "evidence", "evidence_references", "evidence_reference", "applicant_principal_id",
    "decided_by", "assigned_reviewer", "internal_eligibility", "conditions", "requested_markets",
}
# ADR-BCP-005's vocabulary, and the parallel type section 10 forbids.
SUBSCRIPTION_TYPES = {"COMMERCIAL", "INTERNAL", "TRIAL", "PARTNER", "MANUAL", "MIGRATION"}
ACTORS = {"APPLICANT", "REVIEWER", "DECIDER", "PLATFORM"}
# Fields only the server may set; ClientApplicationDraft must never accept them.
SERVER_AUTHORITATIVE = {
    "status", "application_channel", "client_application_id", "reference", "applicant_principal_id",
    "assigned_reviewer", "decision", "approved_subscription_type", "subscription_type", "tenant_id",
    "organisation_id", "submitted_at", "closed_at", "created_at", "updated_at", "information_requests",
}
RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


FORMATS = FormatChecker()


@FORMATS.checks("date-time")
def _is_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if not RFC3339.match(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def build_registry() -> Registry:
    registry = Registry()
    for path in sorted(CONTRACTS.rglob("*.json")):
        try:
            document = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if isinstance(document, dict) and isinstance(document.get("$id"), str):
            registry = registry.with_resource(document["$id"], Resource.from_contents(document))
    return registry


REGISTRY = build_registry()
SCHEMAS: dict[str, dict] = {}


def errors_for(schema_file: str, definition: str, instance: object) -> list[str]:
    validator = Draft202012Validator({"$ref": f"{BASE_URI}{schema_file}#/$defs/{definition}"},
                                     registry=REGISTRY, format_checker=FORMATS)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
            for e in validator.iter_errors(instance)]


def walk_refs(node: object):
    if isinstance(node, dict):
        if isinstance(node.get("$ref"), str):
            yield node["$ref"]
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)


# 1. Packaging, meta-schema validity and $ref resolution.
for name, responsibilities in RESPONSIBILITIES.items():
    path = PKG / name
    if not path.is_file():
        fail(f"{rel(path)} is missing")
        continue
    schema = json.loads(path.read_text())
    SCHEMAS[name] = schema
    if schema.get("$id") != BASE_URI + name:
        fail(f"{rel(path)}: $id {schema.get('$id')!r} does not match {BASE_URI + name}")
    for error in Draft202012Validator(Draft202012Validator.META_SCHEMA).iter_errors(schema):
        fail(f"{rel(path)}: not a valid Draft 2020-12 schema: {error.message}")
    defined = set(schema.get("$defs", {}))
    if defined != responsibilities:
        fail(f"{rel(path)}: $defs {sorted(defined ^ responsibilities)} differ from its responsibilities")
    resolver = REGISTRY.resolver(base_uri=BASE_URI + name)
    for ref in walk_refs(schema):
        try:
            resolver.lookup(ref)
        except Exception:  # noqa: BLE001
            fail(f"{rel(path)}: $ref {ref!r} does not resolve")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

application = SCHEMAS["application.schema.json"]["$defs"]
decision_defs = SCHEMAS["decision.schema.json"]["$defs"]
STATUSES = set(application["applicationStatus"]["enum"])
if set(decision_defs["subscriptionType"]["enum"]) != SUBSCRIPTION_TYPES:
    fail("subscriptionType must be exactly the ADR-BCP-005 vocabulary (no INTERNAL_GROUP)")
if set(application["ClientApplicationDraft"]["properties"]) & SERVER_AUTHORITATIVE:
    fail(f"ClientApplicationDraft accepts server-authoritative fields: "
         f"{sorted(set(application['ClientApplicationDraft']['properties']) & SERVER_AUTHORITATIVE)}")
for definition in ("applicantIdentifier", "applicantAddress"):
    if "verified" in application[definition]["properties"]:
        fail(f"{definition} must not carry 'verified': applicants never assert verification")

# 2. Examples.
examples = {}
for path in sorted((PKG / "examples").glob("*.json")):
    examples[path.name] = document = json.loads(path.read_text())
    for key, (schema_file, definition) in {
        "client_applications": ("application.schema.json", "ClientApplication"),
        "admission_decisions": ("decision.schema.json", "AdmissionDecision"),
        "client_application_drafts": ("application.schema.json", "ClientApplicationDraft"),
        "admission_decision_requests": ("decision.schema.json", "AdmissionDecisionRequest"),
    }.items():
        for index, record in enumerate(document.get(key, [])):
            for error in errors_for(schema_file, definition, record):
                fail(f"{rel(path)}: {key}[{index}] {error}")
    unknown = set(document) - {"_comment", "client_applications", "admission_decisions",
                               "client_application_drafts", "admission_decision_requests"}
    if unknown:
        fail(f"{rel(path)}: unknown example keys {sorted(unknown)}")

    decisions = {d["admission_decision_id"]: d for d in document.get("admission_decisions", [])}
    for app in document.get("client_applications", []):
        summary = app.get("decision")
        if not summary:
            continue
        full = decisions.get(summary["admission_decision_id"])
        if full is None:
            fail(f"{rel(path)}: {app['client_application_id']} names decision {summary['admission_decision_id']} with no record")
            continue
        for field in ("decision", "decided_at", "reason"):
            if full[field] != summary[field]:
                fail(f"{rel(path)}: {app['client_application_id']} decision {field} disagrees with its record")
        if full["client_application_id"] != app["client_application_id"]:
            fail(f"{rel(path)}: decision {full['admission_decision_id']} belongs to another application")
        requested = {m["country_code"] for m in app["requested_markets"]}
        if not set(full.get("approved_market_scope", [])) <= requested:
            fail(f"{rel(path)}: {full['admission_decision_id']} approves markets the application did not request")
        if full["decided_by"] == app["applicant_principal_id"]:
            fail(f"{rel(path)}: {full['admission_decision_id']} is decided by its own applicant")
        eligibility = full.get("internal_eligibility")
        if eligibility and eligibility["evaluated_at"] != full["decided_at"]:
            fail(f"{rel(path)}: {full['admission_decision_id']} eligibility must be evaluated when deciding")
if "client-application-lifecycle.json" not in examples:
    fail("examples/client-application-lifecycle.json is missing")

# 3. Lifecycle.
lifecycle = yaml.safe_load((PKG / "lifecycle.yaml").read_text())
transitions = lifecycle.get("transitions", [])
terminal = set(lifecycle.get("terminal", []))
states = {t["from"] for t in transitions} | {t["to"] for t in transitions} | {lifecycle.get("initial")}
if states != STATUSES:
    fail(f"lifecycle.yaml states {sorted(states ^ STATUSES)} differ from applicationStatus")
if lifecycle.get("initial") != "DRAFT":
    fail("lifecycle.yaml: the initial state must be DRAFT")
if not terminal <= STATUSES or {"APPROVED", "REJECTED", "WITHDRAWN", "EXPIRED", "CANCELLED"} != terminal:
    fail("lifecycle.yaml: terminal states must be APPROVED, REJECTED, WITHDRAWN, EXPIRED and CANCELLED")
seen = set()
for t in transitions:
    key = (t["command"], t["from"])
    if key in seen:
        fail(f"lifecycle.yaml: {t['command']} from {t['from']} is ambiguous")
    seen.add(key)
    if t["from"] in terminal:
        fail(f"lifecycle.yaml: terminal state {t['from']} has an outgoing transition")
    if t.get("actor") not in ACTORS:
        fail(f"lifecycle.yaml: unknown actor {t.get('actor')!r}")
    if t["to"] in {"APPROVED", "REJECTED"} and (t["actor"] != "DECIDER" or t["from"] != "UNDER_REVIEW"):
        fail(f"lifecycle.yaml: {t['to']} must be reached only by a DECIDER from UNDER_REVIEW")
    if t["actor"] == "DECIDER" and t["to"] not in {"APPROVED", "REJECTED"}:
        fail(f"lifecycle.yaml: a DECIDER only decides ({t['command']})")
reachable, queue = {"DRAFT"}, deque(["DRAFT"])
while queue:
    state = queue.popleft()
    for t in transitions:
        if t["from"] == state and t["to"] not in reachable:
            reachable.add(t["to"])
            queue.append(t["to"])
if reachable != STATUSES:
    fail(f"lifecycle.yaml: unreachable states {sorted(STATUSES - reachable)}")
for state in STATUSES - terminal:
    if not any(t["from"] == state and t["command"] == "withdraw" for t in transitions) and state != "DRAFT":
        fail(f"lifecycle.yaml: the applicant cannot withdraw from {state}")
editable = set(lifecycle.get("editable_by_applicant", []))
if editable != {"DRAFT", "INFORMATION_REQUIRED"}:
    fail("lifecycle.yaml: the applicant may edit only DRAFT and INFORMATION_REQUIRED applications")

# 4. Negative fixtures: each mutation MUST be rejected.
lifecycle_doc = examples.get("client-application-lifecycle.json", {})
apps = {a["client_application_id"]: a for a in lifecycle_doc.get("client_applications", [])}
decisions = {d["admission_decision_id"]: d for d in lifecycle_doc.get("admission_decisions", [])}
NEGATIVE: list[tuple[str, str, str, dict]] = []


def negative(label: str, schema_file: str, definition: str, record: dict) -> None:
    NEGATIVE.append((label, schema_file, definition, record))


if {"capp_01k9kilima", "capp_01k9duma"} <= set(apps) and {"adm_01k9zuribeans", "adm_01k9kilima"} <= set(decisions):
    kilima, duma = apps["capp_01k9kilima"], apps["capp_01k9duma"]
    internal, commercial = decisions["adm_01k9zuribeans"], decisions["adm_01k9kilima"]
    draft = {"organisation_profile": {"legal_name": "Duma Logistics"}}

    for field, value in {"status": "APPROVED", "application_channel": "INTERNAL_GROUP", "approved_subscription_type": "INTERNAL",
                         "tenant_id": "tn_01k9duma", "organisation_id": "ce_zuribeans", "decision": {"decision": "APPROVED"}}.items():
        negative(f"applicant draft sets server-authoritative {field}", "application.schema.json", "ClientApplicationDraft",
                 {**draft, field: value})
    verified = copy.deepcopy(draft)
    verified["organisation_profile"]["registration_identifiers"] = [{"type": "COMPANY_REGISTRATION", "value": "X1", "verified": True}]
    negative("applicant asserts a verified identifier", "application.schema.json", "ClientApplicationDraft", verified)
    address = copy.deepcopy(draft)
    address["organisation_profile"]["registered_address"] = {"lines": ["1 Road"], "country_code": "TZ", "verified": True}
    negative("applicant asserts a verified address", "application.schema.json", "ClientApplicationDraft", address)
    binary = copy.deepcopy(draft)
    binary["evidence"] = [{"evidence_type": "OTHER", "evidence_reference": "evd_x", "content_base64": "AAAA"}]
    negative("evidence carries a binary", "application.schema.json", "ClientApplicationDraft", binary)
    negative("website is not https", "application.schema.json", "ClientApplicationDraft",
             {"organisation_profile": {"website": "http://duma.example"}})

    incomplete = copy.deepcopy(kilima)
    del incomplete["organisation_profile"]["registration_identifiers"]
    negative("submitted without registration identifiers", "application.schema.json", "ClientApplication", incomplete)
    no_markets = copy.deepcopy(kilima)
    no_markets["requested_markets"] = []
    negative("submitted without a market", "application.schema.json", "ClientApplication", no_markets)
    undecided = copy.deepcopy(kilima)
    del undecided["decision"]
    negative("APPROVED without a decision", "application.schema.json", "ClientApplication", undecided)
    mismatched = copy.deepcopy(kilima)
    mismatched["decision"]["decision"] = "REJECTED"
    negative("APPROVED application with a REJECTED decision", "application.schema.json", "ClientApplication", mismatched)
    decided_draft = copy.deepcopy(duma)
    decided_draft["decision"] = copy.deepcopy(kilima["decision"])
    negative("DRAFT with a decision", "application.schema.json", "ClientApplication", decided_draft)
    unsubmitted = {**copy.deepcopy(kilima), "status": "UNDER_REVIEW"}
    del unsubmitted["decision"], unsubmitted["submitted_at"]
    negative("under review without submitted_at", "application.schema.json", "ClientApplication", unsubmitted)
    parallel = {**copy.deepcopy(commercial), "approved_subscription_type": "INTERNAL_GROUP"}
    negative("parallel INTERNAL_GROUP subscription type", "decision.schema.json", "AdmissionDecision", parallel)

    request = {"decision": "APPROVED", "reason": "ok", "approved_subscription_type": "COMMERCIAL",
               "approved_market_scope": ["UG"], "evidence_references": ["evd_x"]}
    negative("approval without a subscription type", "decision.schema.json", "AdmissionDecisionRequest",
             {k: v for k, v in request.items() if k != "approved_subscription_type"})
    negative("approval without evidence", "decision.schema.json", "AdmissionDecisionRequest", {**request, "evidence_references": []})
    negative("approval without a market scope", "decision.schema.json", "AdmissionDecisionRequest",
             {k: v for k, v in request.items() if k != "approved_market_scope"})
    negative("INTERNAL without an organisation to evaluate", "decision.schema.json", "AdmissionDecisionRequest",
             {**request, "approved_subscription_type": "INTERNAL"})
    negative("COMMERCIAL naming an internal-eligibility organisation", "decision.schema.json", "AdmissionDecisionRequest",
             {**request, "internal_eligibility_organisation_id": "ce_zuribeans"})
    negative("rejection carrying a classification", "decision.schema.json", "AdmissionDecisionRequest",
             {"decision": "REJECTED", "reason": "no", "approved_subscription_type": "COMMERCIAL"})
    negative("request names its own decider", "decision.schema.json", "AdmissionDecisionRequest", {**request, "decided_by": "prn_x"})
    negative("request supplies eligibility evidence", "decision.schema.json", "AdmissionDecisionRequest",
             {**request, "internal_eligibility": internal["internal_eligibility"]})

    no_evidence = copy.deepcopy(internal)
    del no_evidence["internal_eligibility"]
    negative("INTERNAL decision without eligibility evidence", "decision.schema.json", "AdmissionDecision", no_evidence)
    no_basis = copy.deepcopy(internal)
    no_basis["internal_eligibility"]["basis_relationship_ids"] = []
    negative("eligibility without a governing relationship", "decision.schema.json", "AdmissionDecision", no_basis)
    corporate_basis = copy.deepcopy(internal)
    corporate_basis["internal_eligibility"]["basis_relationship_ids"] = ["crel_01k8nabzuri"]
    negative("eligibility resting on a corporate relationship id", "decision.schema.json", "AdmissionDecision", corporate_basis)
    ineligible = copy.deepcopy(internal)
    ineligible["internal_eligibility"]["eligibility_status"] = "INELIGIBLE"
    negative("INTERNAL with ineligible evidence", "decision.schema.json", "AdmissionDecision", ineligible)
    commercial_evidence = {**copy.deepcopy(commercial), "internal_eligibility": internal["internal_eligibility"]}
    negative("COMMERCIAL decision carrying eligibility evidence", "decision.schema.json", "AdmissionDecision", commercial_evidence)
    anonymous = copy.deepcopy(commercial)
    del anonymous["decided_by"]
    negative("decision without a decider", "decision.schema.json", "AdmissionDecision", anonymous)
    foreign = {**copy.deepcopy(commercial), "admission_decision_id": "decision-1"}
    negative("decision id outside the adm_ form", "decision.schema.json", "AdmissionDecision", foreign)
else:
    fail("client-application-lifecycle.json lacks the records the negative fixtures mutate")

for label, schema_file, definition, record in NEGATIVE:
    if not errors_for(schema_file, definition, record):
        fail(f"negative fixture accepted: {label}")

# 5. Events.
asyncapi = yaml.safe_load((PKG / "asyncapi.yaml").read_text())
messages = (asyncapi.get("components") or {}).get("messages") or {}
registered = {}
for key, message in messages.items():
    layers = (message.get("payload") or {}).get("allOf") or []
    if not any(isinstance(layer, dict) and layer.get("$ref") == ENVELOPE_REF for layer in layers):
        fail(f"asyncapi.yaml {key}: payload is not composed with the canonical envelope")
    refs = [layer.get("properties", {}).get("data", {}).get("$ref") for layer in layers if isinstance(layer, dict)]
    refs = [r for r in refs if r]
    if len(refs) != 1 or not refs[0].startswith("./events.schema.json#/$defs/"):
        fail(f"asyncapi.yaml {key}: data must reference exactly one events.schema.json $def")
        continue
    registered[message.get("name")] = refs[0].rsplit("/", 1)[-1]
if registered != EVENT_TYPES:
    fail(f"asyncapi.yaml registers {sorted(set(registered.items()) ^ set(EVENT_TYPES.items()))} differently from section 40")
for definition, schema in SCHEMAS["events.schema.json"]["$defs"].items():
    leaked = set(schema.get("properties", {})) & FORBIDDEN_EVENT_FIELDS
    if leaked:
        fail(f"events.schema.json {definition} publishes {sorted(leaked)}")
    if schema.get("additionalProperties") is not False:
        fail(f"events.schema.json {definition} must be closed")
event_examples = sorted((PKG / "examples" / "events").glob("*.json"))
if not event_examples:
    fail("no example event envelopes")
for path in event_examples:
    envelope = json.loads(path.read_text())
    definition = EVENT_TYPES.get(envelope.get("type"))
    if definition is None:
        fail(f"{rel(path)}: type {envelope.get('type')!r} is not an admission event")
        continue
    composed = {"allOf": [{"$ref": "https://contracts.baobab-platform.com/events/v1/envelope.schema.json"},
                          {"type": "object", "properties": {"data": {"$ref": f"{BASE_URI}events.schema.json#/$defs/{definition}"}}}]}
    for error in Draft202012Validator(composed, registry=REGISTRY, format_checker=FORMATS).iter_errors(envelope):
        fail(f"{rel(path)}: {error.message}")

# 6. Lock registration.
lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())
entries = [c for c in lock.get("contracts", []) if c.get("domain") == "admission" and c.get("version") == "v1"]
if len(entries) != 1:
    fail("contracts.lock.yaml must register domain admission v1 exactly once")
elif entries[0].get("schemas") != LOCKED_FILES:
    fail(f"contracts.lock.yaml admission v1 schemas must be {LOCKED_FILES}")

scopes = {entry["name"]: entry for entry in
          yaml.safe_load((CONTRACTS / "authorization" / "v1" / "scope-registry.yaml").read_text())["scopes"]}
for name, privileged in {"application:read": False, "application:write": False,
                         "admission:review": True, "admission:decide": True}.items():
    entry = scopes.get(name)
    if entry is None:
        fail(f"scope-registry.yaml does not define {name}")
    elif entry.get("allowed_actors") != ["human"] or bool(entry.get("privileged")) != privileged \
            or entry.get("audience") != ["baobab-control-plane"]:
        fail(f"scope-registry.yaml {name}: must be a {'privileged ' if privileged else ''}human-only Control Plane scope")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} admission contract failure(s)", file=sys.stderr)
    sys.exit(1)
print(f"admission contracts passed ({len(NEGATIVE)} negative fixtures, {len(transitions)} lifecycle transitions, "
      f"{len(event_examples)} example events)")
