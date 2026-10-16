#!/usr/bin/env python3
"""P0-04B Trade-0 order-authority contract conformance (ADR-SHARED-039).

Checks the trade/v2 catalogue, order-authority request and decision, the
CP-owned Seller Operating Binding shapes, examples, negative fixtures and the
workload-only, non-authorising scopes. Synthetic examples prove the contract
shape only; they are not evidence of a running resolver or of commerce support.
"""
from __future__ import annotations

import copy
import json
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
BASE = "https://contracts.baobab-platform.com/"
V2 = CONTRACTS / "trade/v2"
RESOLVE = "trade-order-authority:resolve"
ATTEST = "trade-seller-binding:attest"
DISCOVER = "trade-seller-binding:resolve"
HUMAN = [f"seller-operating-binding:{a}" for a in ("propose", "approve", "activate", "suspend", "revoke")]
# Native Medusa identifiers never cross this boundary.
NATIVE = ("cart_id", "order_id", "sales_channel", "region_id", "medusa", "store_id", "draft_order_id")


def registry() -> Registry:
    resources = []
    for path in CONTRACTS.rglob("*.schema.json"):
        document = json.loads(path.read_text())
        uri = document.get("$id") or BASE + path.relative_to(CONTRACTS).as_posix()
        resources.append((uri, Resource.from_contents(document)))
    return Registry().with_resources(resources)


def validator(schema: dict, name: str, reg: Registry) -> Draft202012Validator:
    return Draft202012Validator(
        {"$ref": f"{schema['$id']}#/$defs/{name}"}, registry=reg, format_checker=FormatChecker())


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def load(name: str) -> dict:
    return json.loads((V2 / "examples" / name).read_text())


def main() -> None:
    authority = json.loads((V2 / "order-authority.schema.json").read_text())
    binding_schema = json.loads((V2 / "seller-operating-binding.schema.json").read_text())
    for schema, name in ((authority, "order-authority"), (binding_schema, "seller-operating-binding")):
        Draft202012Validator.check_schema(schema)
        assert schema["$id"] == BASE + f"trade/v2/{name}.schema.json"
        for key in walk_keys(schema):
            assert not any(n in key.lower() for n in NATIVE), f"native field {key!r} in trade/v2 {name}"
    reg = registry()
    request = validator(authority, "OrderAuthorityRequest", reg)
    decision = validator(authority, "OrderAuthorityDecision", reg)

    # --- the closed catalogue ---------------------------------------------------------------
    catalogue = yaml.safe_load((V2 / "order-operations.yaml").read_text())
    assert catalogue["version"] == 1
    ops = catalogue["operations"]
    classes = [o["operation_class"] for o in ops]
    assert len(classes) == len(set(classes)), "duplicate operation class"
    assert classes == authority["$defs"]["operationClass"]["enum"], "catalogue and schema enum differ"
    roles = json.loads((CONTRACTS / "organisation/v2/legal-actor-mandate.schema.json").read_text())[
        "$defs"]["legalActorRole"]["enum"]
    for o in ops:
        assert set(o) == {"operation_class", "legal_actor_role", "activity", "capability_key", "increment",
                          "activatable"}, o
        assert o["operation_class"].startswith("trade.") and o["operation_class"].count(".") == 2, o
        assert o["legal_actor_role"] == "SELLER_OF_RECORD" and o["legal_actor_role"] in roles, o
        assert o["activity"].isupper() and 3 <= len(o["activity"]) <= 160, o
        assert o["capability_key"] is None, "commerce capability keys are not registered yet"
        assert o["increment"] in {"TRADE_A", "TRADE_B", "TRADE_C"}, o
        # No blanket commerce permission.
        assert not o["operation_class"].endswith((".manage", ".any", ".all", ".admin")), o
    activities = [o["activity"] for o in ops]
    assert len(activities) == len(set(activities)), "each class needs its own activity scope"
    # Only Trade-A is activatable in catalogue version 1 (ADR-SHARED-039 §2).
    assert {o["operation_class"] for o in ops if o["activatable"]} == {
        "trade.order.commit", "trade.order.create", "trade.draft-order.finalize"}
    assert all(o["increment"] == "TRADE_A" for o in ops if o["activatable"])
    # A Trade decision is never money-movement or ERP posting authority.
    money = yaml.safe_load((CONTRACTS / "payments/v2/money-movement-operations.yaml").read_text())["operations"]
    erp = yaml.safe_load((CONTRACTS / "erp/v2/posting-operations.yaml").read_text())["operations"]
    assert not set(activities) & ({m["activity"] for m in money} | {e["activity"] for e in erp}), \
        "a Trade activity reuses a Payments or ERP activity"

    # --- request: the caller selects no authority ---------------------------------------------
    good = load("order-authority-request.json")
    request.validate(good)
    for forged in ["tenant_id", "operating_organisation_id", "legal_entity_id", "responsible_legal_entity_id",
                   "mandate_id", "role", "legal_actor_role", "activity", "market", "capability", "evaluated_at",
                   "binding_status", "cart_id", "order_id", "sales_channel_id"]:
        assert not request.is_valid({**good, forged: "forged"}), forged
    for required in authority["$defs"]["OrderAuthorityRequest"]["required"]:
        bad = copy.deepcopy(good)
        del bad[required]
        assert not request.is_valid(bad), required
    for bad_value in [{"operation_class": "trade.order.manage"}, {"operation_class": "erp.gl-journal.post"},
                      {"engine_instance_id": "trade-1"}, {"context_id": "not-a-uuid"},
                      {"operation_reference": "has space"}, {"operation_reference": "x" * 257},
                      {"native_configuration_digest": "ABC"},
                      {"seller_operating_binding_reference": {"binding_id": good["seller_operating_binding_reference"]["binding_id"],
                                                              "binding_version": 0}},
                      {"seller_operating_binding_reference": {**good["seller_operating_binding_reference"], "cart": "c1"}}]:
        assert not request.is_valid({**good, **bad_value}), bad_value

    # --- decision ----------------------------------------------------------------------------
    authorized = load("order-authority-decision-authorized.json")
    not_activated = load("order-authority-decision-not-activated.json")
    decision.validate(authorized)
    decision.validate(not_activated)
    for required in ["tenant_id", "operating_organisation_id", "market", "legal_actor_role", "activity",
                     "mandate_id", "responsible_legal_entity_id", "evidence_references", "mandate_effective_from",
                     "expires_at", "decision_id"]:
        bad = copy.deepcopy(authorized)
        del bad[required]
        assert not decision.is_valid(bad), required
    for leaked in ["mandate_id", "responsible_legal_entity_id", "evidence_references", "expires_at",
                   "mandate_effective_from"]:
        assert not decision.is_valid({**not_activated, leaked: authorized[leaked]}), leaked
    assert not decision.is_valid({**authorized, "provider_permissions_granted": True})
    assert not decision.is_valid({**authorized, "outcome": "PROVIDER_RESTRICTED"})
    issued = datetime.fromisoformat(authorized["evaluated_at"].replace("Z", "+00:00"))
    expires = datetime.fromisoformat(authorized["expires_at"].replace("Z", "+00:00"))
    assert issued < expires <= issued + timedelta(seconds=30), "examples must keep the 30 s lease"
    assert "evaluated_at + 30 seconds" in authority["$defs"]["OrderAuthorityDecision"]["description"]
    # Role and activity are bound per class; a reserved class only ever answers OPERATION_NOT_ACTIVATED.
    for o in ops:
        good_decision = {**authorized, "operation_class": o["operation_class"], "legal_actor_role": o["legal_actor_role"],
                         "activity": o["activity"]}
        assert decision.is_valid(good_decision) == o["activatable"], o["operation_class"]
        for other in ops:
            if other["activity"] != o["activity"]:
                assert not decision.is_valid({**good_decision, "activity": other["activity"]}), (o, other)
        for role in roles:
            if role != o["legal_actor_role"]:
                assert not decision.is_valid({**good_decision, "legal_actor_role": role}), (o, role)
        request.validate({**good, "operation_class": o["operation_class"]})
        if not o["activatable"]:
            decision.validate({**not_activated, "operation_class": o["operation_class"]})
            assert not decision.is_valid({**not_activated, "operation_class": o["operation_class"],
                                          "outcome": "NO_APPLICABLE_MANDATE"}), o
    assert decision.is_valid({**not_activated, "operation_class": "trade.order.commit", "outcome": "BINDING_NOT_ACTIVE"})
    # Only a reserved class may answer OPERATION_NOT_ACTIVATED: an enabled one never claims to be unavailable.
    for o in ops:
        assert decision.is_valid({**not_activated, "operation_class": o["operation_class"]}) == (not o["activatable"]), o
    # The decision is bound to the operation currency, which CP checks against the binding's scope.
    assert authorized["currency"] == good["currency"]
    for bad_currency in ["ugx", "UG", "USDT", 1]:
        assert not request.is_valid({**good, "currency": bad_currency}), bad_currency
        assert not decision.is_valid({**authorized, "currency": bad_currency}), bad_currency
    assert "currency_scope" in authority["$defs"]["currency"]["description"]
    # The decision echoes the binding version and digest exactly.
    assert authorized["seller_operating_binding_reference"] == good["seller_operating_binding_reference"]
    assert authorized["native_configuration_digest"] == good["native_configuration_digest"]

    # --- the CP-owned Seller Operating Binding -----------------------------------------------------
    record = validator(binding_schema, "SellerOperatingBinding", reg)
    attestation = validator(binding_schema, "NativeConfigurationAttestationRequest", reg)
    command = validator(binding_schema, "BindingTransitionCommand", reg)
    event = validator(binding_schema, "SellerOperatingBindingChanged", reg)
    active = load("seller-operating-binding-active.json")
    record.validate(active)
    assert len({active["proposed_by"], active["approved_by"], active["activated_by"]}) == 3, "maker/checker/operator"
    # The binding is never cart-scoped and has no cart field to carry.
    assert "cart_id" not in binding_schema["$defs"]["SellerOperatingBinding"]["properties"]
    for status, missing in [("ACTIVE", "activated_by"), ("ACTIVE", "approved_by"), ("APPROVED", "approval_id"),
                            ("SUSPENDED", "activation_id")]:
        bad = copy.deepcopy(active)
        bad["status"] = status
        del bad[missing]
        assert not record.is_valid(bad), (status, missing)
    pending = {k: v for k, v in active.items() if k not in
               {"approved_by", "approval_id", "activated_by", "activation_id"}}
    record.validate({**pending, "status": "PENDING_APPROVAL"})
    assert not record.is_valid({**active, "status": "ENABLED"})
    attestation.validate(load("native-configuration-attestation-request.json"))
    for forged in ["tenant_id", "operating_organisation_id", "market", "status", "responsible_legal_entity_id"]:
        assert not attestation.is_valid({**load("native-configuration-attestation-request.json"), forged: "x"}), forged
    activate = load("binding-transition-activate.json")
    command.validate(activate)
    command.validate({**activate, "expected_status": "SUSPENDED"})  # reinstatement is a fresh activation
    assert not command.is_valid({**activate, "expected_status": "PENDING_APPROVAL"}), "activation needs approval first"
    assert not command.is_valid({**activate, "transition": "APPROVE", "expected_status": "SUSPENDED"})
    assert not command.is_valid({**activate, "transition": "SUSPEND", "expected_status": "APPROVED"})
    assert not command.is_valid({**activate, "transition": "REVOKE", "expected_status": "REVOKED"}), "terminal"
    assert not command.is_valid({**activate, "transition": "ENABLE"})
    event.validate({"event_version": 1, "transition_id": "6a7b8c9d-0e1f-4a2b-8c3d-5e6f7a8b9c0d",
                    "binding_reference": {"binding_id": active["binding_id"], "binding_version": active["binding_version"]},
                    "status": "ACTIVE", "tenant_id": active["tenant_id"],
                    "operating_organisation_id": active["operating_organisation_id"],
                    "trade_engine_instance_id": active["trade_engine_instance_id"],
                    "native_configuration_digest": active["native_configuration_digest"],
                    "occurred_at": "2026-10-16T05:00:00Z"})

    # --- binding discovery (Trade-A TA-01, ADR-SHARED-039 §5) ------------------------------
    discover = validator(binding_schema, "BindingResolveRequest", reg)
    resolution = validator(binding_schema, "BindingResolution", reg)
    ask = load("binding-resolve-request.json")
    discover.validate(ask)
    for forged in ["tenant_id", "operating_organisation_id", "market", "responsible_legal_entity_id", "binding_id",
                   "binding_reference", "status", "cart_id", "order_id", "sales_channel_id", "region_id",
                   "currency_scope", "effective_at"]:
        assert not discover.is_valid({**ask, forged: "forged"}), forged
    for required in binding_schema["$defs"]["BindingResolveRequest"]["required"]:
        bad = copy.deepcopy(ask)
        del bad[required]
        assert not discover.is_valid(bad), required
    for bad_value in [{"currency": "ugx"}, {"native_configuration_digest": "ABC"}, {"engine_instance_id": "trade"},
                      {"native_configuration_reference": "/leading"}, {"context_id": "nope"}]:
        assert not discover.is_valid({**ask, **bad_value}), bad_value
    resolved = load("binding-resolution-resolved.json")
    resolution.validate(resolved)
    assert {k: resolved[k] for k in ask} == ask, "a resolution echoes the request exactly"

    # Consumers correlate EVERY echoed field with the originating request; a
    # schema-valid answer to another (delayed, replayed or concurrent) request
    # is a failed resolution, never a binding and never a denial.
    def consumer_accepts(sent: dict, answer: dict) -> bool:
        return resolution.is_valid(answer) and all(answer.get(k) == v for k, v in sent.items())
    assert "MUST correlate every echoed field" in binding_schema["$defs"]["BindingResolution"]["description"]
    assert consumer_accepts(ask, resolved)
    other = {"context_id": "0b1c2d3e-4f5a-4b6c-8d7e-9f0a1b2c3d4e", "engine_instance_id": "ei_tradestaging02",
             "native_configuration_reference": "trade:seller-config/other/v1",
             "native_configuration_digest": "2" * 64, "currency": "USD"}
    for field, value in other.items():
        swapped = {**resolved, field: value}
        assert resolution.is_valid(swapped), field  # schema-valid, so only correlation catches it
        assert not consumer_accepts(ask, swapped), f"uncorrelated {field} accepted"
    outcomes = binding_schema["$defs"]["bindingResolutionOutcome"]["enum"]
    assert outcomes[0] == "RESOLVED" and len(outcomes) == len(set(outcomes))
    denied = {k: v for k, v in resolved.items() if k not in {"binding_reference", "status", "effective_from"}}
    for outcome in outcomes[1:]:
        resolution.validate({**denied, "outcome": outcome})
        for leaked in ["binding_reference", "status", "effective_from"]:
            assert not resolution.is_valid({**denied, "outcome": outcome, leaked: resolved[leaked]}), (outcome, leaked)
    for missing in ["binding_reference", "status", "effective_from"]:
        bad = copy.deepcopy(resolved)
        del bad[missing]
        assert not resolution.is_valid(bad), missing
    assert not resolution.is_valid({**resolved, "status": "SUSPENDED"}), "only an ACTIVE binding resolves"
    assert not resolution.is_valid({**resolved, "provider_permissions_granted": True})
    assert not resolution.is_valid({**resolved, "decision_id": resolved["resolution_id"]}), "discovery is not a decision"

    def reference_resolve(context: dict, req: dict, bindings: list[dict], at: datetime) -> tuple[str, dict | None]:
        def when(v):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        candidates = [x for x in bindings
                      if x["tenant_id"] == context["tenant_id"]
                      and x["operating_organisation_id"] == context["operating_organisation_id"]
                      and x["market"] == context["market"]
                      and x["trade_engine_instance_id"] == req["engine_instance_id"]
                      and x["native_configuration_reference"] == req["native_configuration_reference"]
                      and req["currency"] in x["currency_scope"]]
        if not candidates:
            return "NO_APPLICABLE_BINDING", None
        live = [x for x in candidates if x["status"] == "ACTIVE" and when(x["effective_from"]) <= at
                and ("effective_to" not in x or at < when(x["effective_to"]))]
        if not live:
            return "BINDING_NOT_ACTIVE", None
        exact = [x for x in live if x["native_configuration_digest"] == req["native_configuration_digest"]]
        if not exact:
            return "NATIVE_CONFIGURATION_MISMATCH", None
        if len(exact) > 1:
            return "AMBIGUOUS_BINDING", None
        return "RESOLVED", {"binding_id": exact[0]["binding_id"], "binding_version": exact[0]["binding_version"]}

    golden = load("binding-resolution-vectors.json")
    at = datetime.fromisoformat(golden["evaluated_at"].replace("Z", "+00:00"))
    statuses = set(binding_schema["$defs"]["bindingStatus"]["enum"])
    for x in golden["registry"]:
        assert x["status"] in statuses, x
    ids = [v["vector_id"] for v in golden["vectors"]]
    assert len(ids) == len(set(ids)), "duplicate vector id"
    seen = set()
    for v in golden["vectors"]:
        discover.validate({"context_id": ask["context_id"], **v["request"]})
        outcome, ref = reference_resolve(v["context"], v["request"], golden["registry"], at)
        assert outcome == v["expected_outcome"], (v["vector_id"], outcome)
        assert ref == v.get("expected_binding_reference"), (v["vector_id"], ref)
        resolution.validate({**denied, **v["request"], "outcome": outcome,
                             **({"binding_reference": ref, "status": "ACTIVE",
                                 "effective_from": "2026-10-16T00:00:00Z"} if ref else {})})
        seen.add(outcome)
    assert seen == set(outcomes) - {"ENGINE_INSTANCE_NOT_BOUND", "CONTEXT_NOT_USABLE"}, \
        "every registry-derived outcome needs a golden vector"

    # --- scopes and workload ---------------------------------------------------------------------
    scopes = {s["name"]: s for s in yaml.safe_load((CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]}
    for name in (RESOLVE, ATTEST, DISCOVER):
        s = scopes[name]
        assert s["audience"] == ["baobab-control-plane"] and s["allowed_actors"] == ["workload"], name
        assert s["grants_authority"] is False, name
    for name in HUMAN:
        s = scopes[name]
        assert s["allowed_actors"] == ["human"] and s.get("privileged") is True and s["grants_authority"] is False, name
    workloads = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())["workloads"]
    for name in (RESOLVE, ATTEST, DISCOVER):
        holders = {w for w, d in workloads.items() if name in d.get("allowed_scopes", [])}
        assert holders == {"baobab-trade-legal-actor-assessor-staging"}, (name, holders)
        assert all(workloads[w]["status"] == "PROVISIONED" and workloads[w]["environment"] == "staging" for w in holders)
    for name in HUMAN:
        assert not any(name in d.get("allowed_scopes", []) for d in workloads.values()), f"{name} assigned to a workload"

    lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())
    entry = next(c for c in lock["contracts"] if c["domain"] == "trade" and c["version"] == "v2")
    assert set(entry["schemas"]) == {"order-authority.schema.json", "order-operations.yaml",
                                     "seller-operating-binding.schema.json"}
    print("Trade order-authority contract, catalogue, seller-operating binding, examples and scopes passed")


if __name__ == "__main__":
    main()
