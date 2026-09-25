#!/usr/bin/env python3
"""Validate the ADR-SHARED-011 commercial contracts (ADR-BCP-018 gate ORG-11).

Covers the subscription classification additions to product/v1, the
subscriptions/v1 billing package, the payments/v1 package and the
capability/v1 engine registration schema, with real JSON Schema Draft
2020-12 validation and every cross-schema $ref resolved locally:

  1. schemas are valid, their $id matches their path, required $defs exist
     and every $ref resolves;
  2. the subscription-type vocabulary is ADR-BCP-005's, identical in
     product/v1 and admission/v1, with no INTERNAL_GROUP;
  3. billing-policy.yaml covers every type, INTERNAL is zero charge with
     metering, audit and controls on and payments never invoked, and only
     INTERNAL and TRIAL are zero-charge;
  4. every example validates and agrees with the policy table
     (projections, explanations, usage billability, payment currencies);
  5. negative fixtures prove the load-bearing rules reject bad data: no
     INTERNAL without eligibility evidence, no fake commercial readiness on
     a simulated provider, no unmarked sandbox results;
  6. engine capability registrations are valid, use registered domains and
     never permit a simulated provider in production;
  7. asyncapi.yaml registrations and event payload privacy;
  8. contracts.lock.yaml registers every file.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-commercial-contracts.py
"""

from __future__ import annotations

import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
BASE = "https://contracts.baobab-platform.com/"

# path under contracts/ -> $defs it must define (a subset for shared files).
REQUIRED_DEFS = {
    "product/v1/domain.schema.json": {"subscriptionType", "classificationSource", "subscriptionClassificationId",
                                      "monetaryCharge", "paymentExecution"},
    "product/v1/subscription.schema.json": {"productSubscription", "subscriptionClassification", "classificationReference",
                                            "classificationReferenceRule", "SubscriptionClassificationRecord",
                                            "billingPolicy", "ClassificationExplanation"},
    "product/v1/events.schema.json": {"subscriptionClassifiedEventData"},
    "subscriptions/v1/domain.schema.json": {"billingSubscriptionId", "usageRecordId", "billingState", "readinessStatus",
                                            "readinessReason", "billingProviderKind", "usageMetricKey"},
    "subscriptions/v1/billing.schema.json": {"classificationProvenance", "billingPolicy", "EnsureBillingProjectionRequest",
                                             "BillingProjection", "BillingProjectionCommand", "RecordUsageRequest", "UsageRecord"},
    "subscriptions/v1/events.schema.json": {"BillingSubscriptionCreated", "BillingSubscriptionSuspended",
                                            "BillingSubscriptionCancelled", "UsageRecorded"},
    "payments/v1/domain.schema.json": {"paymentIntentId", "paymentId", "refundId", "currencyCode", "paymentIntentStatus",
                                       "paymentStatus", "refundStatus", "captureMethod", "paymentProviderKind", "sourceEngine"},
    "payments/v1/payment.schema.json": {"Money", "PaymentContext", "ProviderResult", "CreatePaymentIntentRequest",
                                        "PaymentIntent", "ConfirmPaymentIntentRequest", "Payment", "CapturePaymentRequest",
                                        "CancelPaymentRequest", "CreateRefundRequest", "Refund"},
    "payments/v1/events.schema.json": {"PaymentCreated", "PaymentAuthorized", "PaymentCaptured", "PaymentFailed",
                                       "PaymentCancelled", "PaymentRefunded"},
    "capability/v1/registration.schema.json": {"EngineRegistration"},
}
EXACT_DEFS = {path for path in REQUIRED_DEFS if path.split("/")[0] in {"subscriptions", "payments"}} | {
    "capability/v1/registration.schema.json"}

SUBSCRIPTION_TYPES = ["COMMERCIAL", "INTERNAL", "TRIAL", "PARTNER", "MANUAL", "MIGRATION"]
ZERO_CHARGE_TYPES = {"INTERNAL", "TRIAL"}
INTERNAL_POLICY = {"monetary_charge": "ZERO", "billing_required": False, "usage_metering": True,
                   "entitlement_control": True, "audit": True, "readiness_control": True,
                   "isolation_control": True, "payment_execution": "NEVER"}

EVENT_TYPES = {
    "subscriptions/v1": {
        "com.baobab-platform.subscriptions.billing-subscription.created.v1": "BillingSubscriptionCreated",
        "com.baobab-platform.subscriptions.billing-subscription.suspended.v1": "BillingSubscriptionSuspended",
        "com.baobab-platform.subscriptions.billing-subscription.cancelled.v1": "BillingSubscriptionCancelled",
        "com.baobab-platform.subscriptions.usage.recorded.v1": "UsageRecorded",
    },
    "payments/v1": {
        "com.baobab-platform.payments.payment.created.v1": "PaymentCreated",
        "com.baobab-platform.payments.payment.authorized.v1": "PaymentAuthorized",
        "com.baobab-platform.payments.payment.captured.v1": "PaymentCaptured",
        "com.baobab-platform.payments.payment.failed.v1": "PaymentFailed",
        "com.baobab-platform.payments.payment.cancelled.v1": "PaymentCancelled",
        "com.baobab-platform.payments.payment.refunded.v1": "PaymentRefunded",
    },
}
# Event payloads carry identifiers and state only.
FORBIDDEN_EVENT_FIELDS = {"reason", "description", "payment_method_reference", "classification_reference",
                          "internal_eligibility", "classified_by", "legal_name", "card_number", "metadata"}

LOCK = {
    "product": ["domain.schema.json", "product.schema.json", "subscription.schema.json", "events.schema.json",
                "billing-policy.yaml"],
    "subscriptions": ["domain.schema.json", "billing.schema.json", "events.schema.json", "capabilities.json"],
    "payments": ["domain.schema.json", "payment.schema.json", "events.schema.json", "capabilities.json"],
}
RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


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


registry = Registry()
for path in sorted(CONTRACTS.rglob("*.json")):
    try:
        document = json.loads(path.read_text())
    except json.JSONDecodeError:
        continue
    if isinstance(document, dict) and isinstance(document.get("$id"), str):
        registry = registry.with_resource(document["$id"], Resource.from_contents(document))


def errors_for(ref: str, instance: object) -> list[str]:
    validator = Draft202012Validator({"$ref": BASE + ref}, registry=registry, format_checker=FORMATS)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in validator.iter_errors(instance)]


def walk_refs(node: object):
    if isinstance(node, dict):
        if isinstance(node.get("$ref"), str):
            yield node["$ref"]
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)


def load(rel: str):
    path = CONTRACTS / rel
    return yaml.safe_load(path.read_text()) if path.suffix == ".yaml" else json.loads(path.read_text())


# 1. Packaging.
schemas = {}
for rel, required in REQUIRED_DEFS.items():
    path = CONTRACTS / rel
    if not path.is_file():
        fail(f"contracts/{rel} is missing")
        continue
    schema = json.loads(path.read_text())
    schemas[rel] = schema
    if schema.get("$id") != BASE + rel:
        fail(f"contracts/{rel}: $id {schema.get('$id')!r} does not match its path")
    for error in Draft202012Validator(Draft202012Validator.META_SCHEMA).iter_errors(schema):
        fail(f"contracts/{rel}: invalid Draft 2020-12 schema: {error.message}")
    defined = set(schema.get("$defs", {}))
    if not required <= defined:
        fail(f"contracts/{rel}: missing $defs {sorted(required - defined)}")
    if rel in EXACT_DEFS and defined != required:
        fail(f"contracts/{rel}: $defs {sorted(defined ^ required)} differ from its responsibilities")
    resolver = registry.resolver(base_uri=BASE + rel)
    for ref in walk_refs(schema):
        try:
            resolver.lookup(ref)
        except Exception:  # noqa: BLE001
            fail(f"contracts/{rel}: $ref {ref!r} does not resolve")
if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

# 2. Vocabulary.
product_types = schemas["product/v1/domain.schema.json"]["$defs"]["subscriptionType"]["enum"]
admission_types = load("admission/v1/decision.schema.json")["$defs"]["subscriptionType"]["enum"]
if product_types != SUBSCRIPTION_TYPES or admission_types != SUBSCRIPTION_TYPES:
    fail(f"subscriptionType must be exactly {SUBSCRIPTION_TYPES} in product/v1 and admission/v1 "
         f"(product {product_types}, admission {admission_types})")

# 3. Billing policy.
policy = load("product/v1/billing-policy.yaml")
policies = policy.get("policies", {})
if sorted(policies) != sorted(SUBSCRIPTION_TYPES):
    fail(f"billing-policy.yaml must define exactly {SUBSCRIPTION_TYPES}, got {list(policies)}")
for kind, entry in policies.items():
    for error in errors_for("product/v1/subscription.schema.json#/$defs/billingPolicy", entry):
        fail(f"billing-policy.yaml {kind}: {error}")
    if entry.get("monetary_charge") == "ZERO" and kind not in ZERO_CHARGE_TYPES:
        fail(f"billing-policy.yaml {kind}: only {sorted(ZERO_CHARGE_TYPES)} may be zero-charge")
if policies.get("INTERNAL") != INTERNAL_POLICY:
    fail(f"billing-policy.yaml INTERNAL must be exactly {INTERNAL_POLICY} (ADR-BCP-017 section 11)")


def billing_view(kind: str) -> dict:
    entry = policies.get(kind, {})
    return {key: entry.get(key) for key in ("monetary_charge", "billing_required", "usage_metering", "payment_execution")}


# 4. Examples.
EXAMPLES = {
    "product/v1/examples/subscription-classification.json": {
        "product_subscriptions": "product/v1/subscription.schema.json#/$defs/productSubscription",
        "classification_records": "product/v1/subscription.schema.json#/$defs/SubscriptionClassificationRecord",
        "explanations": "product/v1/subscription.schema.json#/$defs/ClassificationExplanation",
    },
    "subscriptions/v1/examples/billing-projections.json": {
        "ensure_requests": "subscriptions/v1/billing.schema.json#/$defs/EnsureBillingProjectionRequest",
        "projections": "subscriptions/v1/billing.schema.json#/$defs/BillingProjection",
        "usage_requests": "subscriptions/v1/billing.schema.json#/$defs/RecordUsageRequest",
        "usage_records": "subscriptions/v1/billing.schema.json#/$defs/UsageRecord",
        "commands": "subscriptions/v1/billing.schema.json#/$defs/BillingProjectionCommand",
    },
    "payments/v1/examples/payments.json": {
        "intent_requests": "payments/v1/payment.schema.json#/$defs/CreatePaymentIntentRequest",
        "intents": "payments/v1/payment.schema.json#/$defs/PaymentIntent",
        "confirm_requests": "payments/v1/payment.schema.json#/$defs/ConfirmPaymentIntentRequest",
        "payments": "payments/v1/payment.schema.json#/$defs/Payment",
        "capture_requests": "payments/v1/payment.schema.json#/$defs/CapturePaymentRequest",
        "refund_requests": "payments/v1/payment.schema.json#/$defs/CreateRefundRequest",
        "refunds": "payments/v1/payment.schema.json#/$defs/Refund",
    },
}
examples = {}
for rel, keys in EXAMPLES.items():
    doc = load(rel)
    examples[rel] = doc
    unknown = set(doc) - set(keys) - {"_comment"}
    if unknown:
        fail(f"contracts/{rel}: unknown keys {sorted(unknown)}")
    for key, ref in keys.items():
        if not doc.get(key):
            fail(f"contracts/{rel}: {key} has no examples")
        for index, record in enumerate(doc.get(key, [])):
            for error in errors_for(ref, record):
                fail(f"contracts/{rel}: {key}[{index}] {error}")

classification = examples["product/v1/examples/subscription-classification.json"]
records = {r["classification_id"]: r for r in classification["classification_records"]}
for sub in classification["product_subscriptions"]:
    current = sub.get("classification")
    record = records.get(current["classification_id"]) if current else None
    if record is None or any(record[k] != current[k] for k in current) or record["subscription_id"] != sub["subscription_id"]:
        fail(f"product example: {sub['subscription_id']} classification does not match a record")
for explanation in classification["explanations"]:
    kind = explanation["current"]["subscription_type"]
    if explanation["billing_policy"] != policies.get(kind):
        fail(f"product example: explanation of {explanation['subscription_id']} does not apply the {kind} billing policy")
    if explanation["history"][0] != explanation["current"]:
        fail(f"product example: explanation of {explanation['subscription_id']}: history[0] must be the current record")

billing = examples["subscriptions/v1/examples/billing-projections.json"]
projections = {p["billing_subscription_id"]: p for p in billing["projections"]}
for projection in billing["projections"]:
    if projection["billing_policy"] != billing_view(projection["subscription_type"]):
        fail(f"subscriptions example: {projection['billing_subscription_id']} does not apply the "
             f"{projection['subscription_type']} billing policy")
for usage in billing["usage_records"]:
    projection = projections.get(usage["billing_subscription_id"])
    if projection is None or projection["tenant_id"] != usage["tenant_id"] \
            or projection["product_subscription_id"] != usage["product_subscription_id"]:
        fail(f"subscriptions example: {usage['usage_record_id']} is not scoped to its projection's tenant and subscription")
    elif usage["billable"] != (projection["billing_policy"]["monetary_charge"] == "PRICED"):
        fail(f"subscriptions example: {usage['usage_record_id']} billable must follow the projection's charge")

payments = examples["payments/v1/examples/payments.json"]
for key in ("intent_requests", "intents"):
    for record in payments[key]:
        if record["amount"]["currency"] != record["context"]["currency"]:
            fail(f"payments example: {key} amount currency must equal the context currency")
for payment in payments["payments"]:
    if payment["refunded_amount_minor"] > payment["captured_amount_minor"] or \
            payment["captured_amount_minor"] > payment["amount"]["amount_minor"]:
        fail(f"payments example: {payment['payment_id']} refunds exceed captures or captures exceed the amount")

# 5. Negative fixtures.
NEGATIVE: list[tuple[str, str, dict]] = []


def negative(label: str, ref: str, record: dict) -> None:
    NEGATIVE.append((label, ref, record))


SUBS = "product/v1/subscription.schema.json#/$defs/"
internal = copy.deepcopy(records["subcls_01k9zuriinternal"])
reclass = copy.deepcopy(records["subcls_01k9zuricommercial"])
no_evidence = copy.deepcopy(internal); del no_evidence["internal_eligibility"]
negative("INTERNAL record without eligibility evidence", SUBS + "SubscriptionClassificationRecord", no_evidence)
negative("COMMERCIAL record carrying eligibility evidence", SUBS + "SubscriptionClassificationRecord",
         {**copy.deepcopy(reclass), "internal_eligibility": internal["internal_eligibility"]})
negative("ADMISSION_DECISION referencing something other than an admission decision", SUBS + "SubscriptionClassificationRecord",
         {**copy.deepcopy(internal), "classification_reference": "chg_01k9other"})
no_previous = copy.deepcopy(reclass); del no_previous["previous_subscription_type"]
negative("reclassification without the previous type", SUBS + "SubscriptionClassificationRecord", no_previous)
negative("parallel INTERNAL_GROUP type", SUBS + "SubscriptionClassificationRecord", {**copy.deepcopy(reclass), "subscription_type": "INTERNAL_GROUP"})
negative("eligibility evidence resting on nothing", SUBS + "SubscriptionClassificationRecord",
         {**copy.deepcopy(internal), "internal_eligibility": {**internal["internal_eligibility"], "basis_relationship_ids": []}})
negative("classified by nobody", SUBS + "SubscriptionClassificationRecord", {k: v for k, v in internal.items() if k != "classified_by"})
explanation = copy.deepcopy(classification["explanations"][0]); del explanation["current_eligibility"]
negative("INTERNAL explanation without current eligibility", SUBS + "ClassificationExplanation", explanation)
negative("zero-charge policy that bills", SUBS + "billingPolicy", {**INTERNAL_POLICY, "billing_required": True})
negative("zero-charge policy that invokes payments", SUBS + "billingPolicy", {**INTERNAL_POLICY, "payment_execution": "REQUIRED"})
negative("unmetered policy", SUBS + "billingPolicy", {**INTERNAL_POLICY, "usage_metering": False})
negative("priced policy that does not bill", SUBS + "billingPolicy", {**policies["COMMERCIAL"], "billing_required": False})

BILL = "subscriptions/v1/billing.schema.json#/$defs/"
internal_projection = copy.deepcopy(billing["projections"][0])
commercial_projection = copy.deepcopy(billing["projections"][1])
negative("INTERNAL projection that bills", BILL + "BillingProjection",
         {**internal_projection, "billing_policy": {**internal_projection["billing_policy"], "billing_required": True}})
negative("INTERNAL projection that invokes payments", BILL + "BillingProjection",
         {**internal_projection, "billing_policy": {**internal_projection["billing_policy"], "payment_execution": "REQUIRED"}})
negative("commercial projection ACTIVE on a simulated provider", BILL + "BillingProjection", {**commercial_projection, "billing_state": "ACTIVE"})
negative("commercial projection READY on a simulated provider", BILL + "BillingProjection",
         {**commercial_projection, "readiness": {"status": "READY", "reasons": []}})
negative("READY with blockers", BILL + "BillingProjection",
         {**internal_projection, "readiness": {"status": "READY", "reasons": ["PAYMENT_PROVIDER_NOT_CONFIGURED"]}})
negative("BLOCKED without a reason", BILL + "BillingProjection", {**commercial_projection, "readiness": {"status": "BLOCKED", "reasons": []}})
negative("temporary provider claiming to be real", BILL + "BillingProjection",
         {**internal_projection, "provider": {"kind": "TEMPORARY", "simulated": False}})
negative("suspended projection that still reports ready", BILL + "BillingProjection", {**internal_projection, "billing_state": "SUSPENDED"})
negative("ensure request carrying eligibility evidence", BILL + "EnsureBillingProjectionRequest",
         {**billing["ensure_requests"][0], "internal_eligibility": internal["internal_eligibility"]})
negative("ensure request without classification", BILL + "EnsureBillingProjectionRequest",
         {k: v for k, v in billing["ensure_requests"][0].items() if k != "classification"})
negative("negative usage", BILL + "RecordUsageRequest", {**billing["usage_requests"][0], "quantity": -1})

PAY = "payments/v1/payment.schema.json#/$defs/"
intent = copy.deepcopy(payments["intents"][0])
negative("sandbox result not marked simulated", PAY + "PaymentIntent", {**intent, "provider": {"kind": "SANDBOX", "simulated": False}})
negative("real provider marked simulated", PAY + "PaymentIntent", {**intent, "provider": {"kind": "HYPERSWITCH", "simulated": True}})
negative("card data in an intent request", PAY + "CreatePaymentIntentRequest", {**payments["intent_requests"][0], "card_number": "4111111111111111"})
negative("card data in a confirmation", PAY + "ConfirmPaymentIntentRequest", {**payments["confirm_requests"][0], "card_number": "4111111111111111"})
negative("zero amount", PAY + "CreatePaymentIntentRequest",
         {**payments["intent_requests"][0], "amount": {"currency": "UGX", "amount_minor": 0}})
negative("lowercase currency", PAY + "CreatePaymentIntentRequest",
         {**payments["intent_requests"][0], "amount": {"currency": "ugx", "amount_minor": 1}})
negative("context without a tenant", PAY + "CreatePaymentIntentRequest",
         {**payments["intent_requests"][0], "context": {k: v for k, v in payments["intent_requests"][0]["context"].items() if k != "tenant_id"}})
negative("payment event without simulated", "payments/v1/events.schema.json#/$defs/PaymentCaptured",
         {k: v for k, v in load("payments/v1/examples/events/payment-captured.json")["data"].items() if k != "simulated"})

REG = "capability/v1/registration.schema.json#/$defs/EngineRegistration"
subscription_registration = load("subscriptions/v1/capabilities.json")
negative("simulated provider permitted in production", REG,
         {**subscription_registration, "provider": {**subscription_registration["provider"], "production_permitted": True}})
negative("capability in an unregistered domain", REG,
         {**subscription_registration, "capabilities": [{**subscription_registration["capabilities"][0], "domain": "subscription"}]})

for label, ref, record in NEGATIVE:
    if not errors_for(ref, record):
        fail(f"negative fixture accepted: {label}")

# 6. Engine registrations.
domains = {entry["key"] for entry in load("capability/v1/namespace-registry.yaml")["domains"]}
for package in ("subscriptions/v1", "payments/v1"):
    registration = load(f"{package}/capabilities.json")
    for error in errors_for(REG, registration):
        fail(f"contracts/{package}/capabilities.json: {error}")
    keys = {c["capability_key"] for c in registration["capabilities"]}
    for capability in registration["capabilities"]:
        prefix = capability["capability_key"].split(".")[0]
        if prefix != capability["domain"] or prefix not in domains:
            fail(f"{package}: {capability['capability_key']} must sit in its registered domain")
        if capability["owner"] != registration["repository"]:
            fail(f"{package}: {capability['capability_key']} is owned by another repository")
        for contract in capability["contracts"]:
            for key in ("request_schema", "response_schema"):
                target, _, fragment = contract[key].partition("#")
                try:
                    registry.resolver(base_uri=BASE + package + "/capabilities.json").lookup(contract[key])
                except Exception:  # noqa: BLE001
                    fail(f"{package}: {capability['capability_key']} {key} {contract[key]!r} does not resolve")
        if registration["provider"]["simulated"] and capability["maturity"] != "EXPERIMENTAL":
            fail(f"{package}: capabilities served only by a simulated provider must be EXPERIMENTAL")
    if {s["capability_key"] for s in registration["support"]} != keys:
        fail(f"{package}: provider support must cover exactly the registered capabilities")
    if registration["provider"]["ownership"] != registration["repository"]:
        fail(f"{package}: provider ownership must be {registration['repository']}")
if "billing" not in domains:
    fail("namespace-registry.yaml must register the billing domain (ADR-SHARED-011)")

# 7. Events.
for package, expected in EVENT_TYPES.items():
    asyncapi = load(f"{package}/asyncapi.yaml")
    registered = {}
    for key, message in (asyncapi.get("components") or {}).get("messages", {}).items():
        refs = [layer.get("properties", {}).get("data", {}).get("$ref") for layer in message["payload"]["allOf"] if isinstance(layer, dict)]
        refs = [r for r in refs if r]
        registered[message["name"]] = refs[0].rsplit("/", 1)[-1] if refs else None
    if registered != expected:
        fail(f"{package}/asyncapi.yaml registers {registered}, expected {expected}")
    for definition, schema in load(f"{package}/events.schema.json")["$defs"].items():
        leaked = set(schema["properties"]) & FORBIDDEN_EVENT_FIELDS
        if leaked:
            fail(f"{package} {definition} publishes {sorted(leaked)}")
        if package == "payments/v1" and "simulated" not in schema.get("required", []):
            fail(f"payments {definition} must require simulated")
product_events = load("product/v1/asyncapi.yaml")["components"]["messages"]
if product_events.get("SubscriptionClassified", {}).get("name") != "com.baobab-platform.product.subscription.classified.v1":
    fail("product/v1/asyncapi.yaml must register com.baobab-platform.product.subscription.classified.v1")
if set(load("product/v1/events.schema.json")["$defs"]["subscriptionClassifiedEventData"]["properties"]) & FORBIDDEN_EVENT_FIELDS:
    fail("subscription.classified publishes forbidden fields")

# 8. Engine workload scopes: each engine's scopes are workload-only and
# issued for that engine's audience alone (ADR-SHARED-011 section 5).
ENGINE_SCOPES = {
    "billing:manage": "baobab-subscriptions", "billing:read": "baobab-subscriptions", "usage:record": "baobab-subscriptions",
    "payment:execute": "baobab-payments", "payment:refund": "baobab-payments", "payment:read": "baobab-payments",
}
scopes = {entry["name"]: entry for entry in load("authorization/v1/scope-registry.yaml")["scopes"]}
for name, audience in ENGINE_SCOPES.items():
    entry = scopes.get(name)
    if entry is None:
        fail(f"scope-registry.yaml must register {name}")
    elif entry.get("audience") != [audience] or entry.get("allowed_actors") != ["workload"]:
        fail(f"scope {name} must be workload-only with audience [{audience}]")

# 9. Lock.
lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())
by_domain = {entry["domain"]: entry for entry in lock["contracts"] if entry.get("version") == "v1"}
for domain, files in LOCK.items():
    if by_domain.get(domain, {}).get("schemas") != files:
        fail(f"contracts.lock.yaml {domain} v1 must list {files}")
if "registration.schema.json" not in by_domain.get("capability", {}).get("schemas", []):
    fail("contracts.lock.yaml capability v1 must list registration.schema.json")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} commercial contract failure(s)", file=sys.stderr)
    sys.exit(1)
print(f"commercial contracts passed ({len(NEGATIVE)} negative fixtures, {len(policies)} billing policies)")
