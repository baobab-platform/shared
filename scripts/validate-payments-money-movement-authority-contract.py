#!/usr/bin/env python3
"""P0-04B Payments money-movement authority contract conformance (ADR-SHARED-035).

Checks the payments/v2 schema, catalogue, examples, fingerprint vectors,
negative fixtures and the workload-only, non-authorising scope. Synthetic
examples prove the contract shape only; they are not evidence of a running
resolver, a certified provider or any money movement.
"""
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
BASE = "https://contracts.baobab-platform.com/"
V2 = CONTRACTS / "payments/v2"
SCOPE = "payments-money-movement-authority:resolve"
FIELDS = sorted(["amount_minor", "currency", "destination_reference", "market", "merchant_profile_reference",
                 "operating_organisation_id", "operation_class", "operation_reference", "parent_reference",
                 "payment_reference", "tenant_id"])
# Provider vocabulary stays out of the contract (ADR-PAY-0001: HyperSwitch is an adapter, not the model).
VENDOR = ("hyperswitch", "connector", "stripe", "api_key", "pan", "card_number", "cvv")


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


def canonical(operation_class: str, operation_reference: str, instruction: dict) -> bytes:
    document = {**instruction, "operation_class": operation_class, "operation_reference": operation_reference}
    assert sorted(document) == FIELDS, sorted(document)
    return json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def fingerprint(operation_class: str, operation_reference: str, instruction: dict) -> str:
    return hashlib.sha256(canonical(operation_class, operation_reference, instruction)).hexdigest()


def main() -> None:
    schema = json.loads((V2 / "money-movement-authority.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    assert schema["$id"] == BASE + "payments/v2/money-movement-authority.schema.json"
    for key in walk_keys(schema):
        assert not key.lower().startswith(VENDOR), f"provider field {key!r} in payments/v2"
    reg = registry()
    request = validator(schema, "MoneyMovementAuthorityRequest", reg)
    decision = validator(schema, "MoneyMovementAuthorityDecision", reg)

    examples = V2 / "examples"
    good_request = json.loads((examples / "money-movement-authority-request.json").read_text())
    authorized = json.loads((examples / "money-movement-authority-decision-authorized.json").read_text())
    denied = json.loads((examples / "money-movement-authority-decision-denied.json").read_text())
    payout = json.loads((examples / "money-movement-authority-decision-payout-not-activated.json").read_text())
    request.validate(good_request)
    for document in (authorized, denied, payout):
        decision.validate(document)

    # The fingerprint is reproducible from the canonical encoding, and every vector is exact.
    vectors = json.loads((examples / "fingerprint-vectors.json").read_text())["vectors"]
    assert len(vectors) >= 6
    assert {v["operation_class"] for v in vectors} == set(schema["$defs"]["operationClass"]["enum"])
    for vector in vectors:
        raw = canonical(vector["operation_class"], vector["operation_reference"], vector["instruction"])
        assert raw.decode("utf-8") == vector["canonical"], vector["operation_reference"]
        assert hashlib.sha256(raw).hexdigest() == vector["instruction_fingerprint"], vector["operation_reference"]
        request.validate({**good_request, "operation_class": vector["operation_class"],
                          "operation_reference": vector["operation_reference"], "instruction": vector["instruction"],
                          "instruction_fingerprint": vector["instruction_fingerprint"], "attempt": 1})
    assert good_request["instruction_fingerprint"] == fingerprint(
        good_request["operation_class"], good_request["operation_reference"], good_request["instruction"])
    # Every financial field moves the fingerprint: a decision for one instruction never covers another.
    base = vectors[1]
    for field, changed in [("amount_minor", 149999), ("currency", "KES"), ("merchant_profile_reference", "mprof_other"),
                           ("parent_reference", "pay_other"), ("payment_reference", "pay_other"),
                           ("tenant_id", "tn_other01"), ("market", "KE"), ("destination_reference", "bnf_other"),
                           ("operating_organisation_id", "3d9f5a7b-2c4e-4f6a-9b8d-0e1f2a3b4c5d")]:
        assert fingerprint(base["operation_class"], base["operation_reference"], {**base["instruction"], field: changed}) \
            != base["instruction_fingerprint"], field
    assert fingerprint("payments.refund.execute", base["operation_reference"], base["instruction"]) != base["instruction_fingerprint"]
    assert fingerprint(base["operation_class"], base["operation_reference"] + "x", base["instruction"]) != base["instruction_fingerprint"]

    # The caller can never select authority, identity or time.
    for forged in ["mandate_id", "legal_actor_role", "role", "activity", "capability", "capability_key",
                   "responsible_legal_entity_id", "legal_entity_id", "effective_at", "evaluated_at",
                   "provider_permissions_granted", "approved"]:
        assert not request.is_valid({**good_request, forged: "forged"}), forged
        assert not request.is_valid({**good_request, "instruction": {**good_request["instruction"], forged: "forged"}}), forged
    for required in ["context_id", "engine_instance_id", "operation_class", "operation_reference", "attempt",
                     "instruction", "instruction_fingerprint"]:
        bad = copy.deepcopy(good_request)
        del bad[required]
        assert not request.is_valid(bad), required
    for required in good_request["instruction"]:
        bad = copy.deepcopy(good_request)
        del bad["instruction"][required]
        assert not request.is_valid(bad), required
    for bad_value in [{"operation_class": "payments.anything.execute"}, {"engine_instance_id": "pay-1"},
                      {"context_id": "not-a-uuid"}, {"operation_reference": "has space"},
                      {"operation_reference": "x" * 257}, {"attempt": 0}, {"attempt": 1001},
                      {"instruction_fingerprint": "A" * 64}, {"instruction_fingerprint": "0" * 63}]:
        assert not request.is_valid({**good_request, **bad_value}), bad_value
    for bad_instruction in [{"amount_minor": 0}, {"amount_minor": -1}, {"amount_minor": 1.5}, {"amount_minor": "150000"},
                            {"currency": "ugx"}, {"market": "UGA"}, {"parent_reference": None},
                            {"destination_reference": "bnf_synthetic01"}]:
        bad = {**good_request, "instruction": {**good_request["instruction"], **bad_instruction}}
        assert not request.is_valid(bad), bad_instruction
    # Per-class instruction shape: refunds go back to the original method only; payouts need a destination.
    refund = next(v for v in vectors if v["operation_class"] == "payments.refund.execute")
    refund_request = {**good_request, "operation_class": refund["operation_class"],
                      "operation_reference": refund["operation_reference"], "instruction": refund["instruction"],
                      "instruction_fingerprint": refund["instruction_fingerprint"]}
    request.validate(refund_request)
    for bad_instruction in [{"destination_reference": "bnf_synthetic01"}, {"destination_reference": None},
                            {"parent_reference": None}]:
        assert not request.is_valid({**refund_request, "instruction": {**refund["instruction"], **bad_instruction}})
    authorize = next(v for v in vectors if v["operation_class"] == "payments.authorization.create")
    assert not request.is_valid({**good_request, "operation_class": authorize["operation_class"],
                                 "instruction": {**authorize["instruction"], "parent_reference": "pay_x"}})
    payout_vector = next(v for v in vectors if v["operation_class"] == "payments.payout.execute")
    assert not request.is_valid({**good_request, "operation_class": payout_vector["operation_class"],
                                 "instruction": {**payout_vector["instruction"], "destination_reference": None}})

    # AUTHORIZED carries the full actor; every other outcome carries none of it.
    for required in ["tenant_id", "operating_organisation_id", "market", "legal_actor_role", "activity",
                     "mandate_id", "responsible_legal_entity_id", "evidence_references",
                     "mandate_effective_from", "expires_at", "decision_id", "attempt", "instruction_fingerprint"]:
        bad = copy.deepcopy(authorized)
        del bad[required]
        assert not decision.is_valid(bad), required
    for leaked in ["mandate_id", "responsible_legal_entity_id", "evidence_references", "expires_at",
                   "mandate_effective_from", "mandate_effective_to"]:
        assert not decision.is_valid({**denied, leaked: authorized[leaked]}), leaked
    assert not decision.is_valid({**authorized, "provider_permissions_granted": True})
    assert not decision.is_valid({**authorized, "outcome": "PROVIDER_RESTRICTED"})
    assert not decision.is_valid({**authorized, "evidence_references": []})
    assert not decision.is_valid({**authorized, "instruction_fingerprint": "0" * 63})
    issued = datetime.fromisoformat(authorized["evaluated_at"].replace("Z", "+00:00"))
    expires = datetime.fromisoformat(authorized["expires_at"].replace("Z", "+00:00"))
    assert issued < expires <= issued + timedelta(seconds=30), "examples must keep the 30 s lease"
    for key in ["context_id", "engine_instance_id", "operation_class", "operation_reference", "attempt",
                "instruction_fingerprint"]:
        assert authorized[key] == good_request[key] == denied[key], key

    # The catalogue is closed; activatable classes bind one role, activity and capability.
    catalogue = yaml.safe_load((V2 / "money-movement-operations.yaml").read_text())
    roles = json.loads((CONTRACTS / "organisation/v2/legal-actor-mandate.schema.json").read_text())[
        "$defs"]["legalActorRole"]["enum"]
    capabilities = {c["capability_key"] for c in yaml.safe_load(
        (CONTRACTS / "capability/v1/catalogue.yaml").read_text())["capabilities"]}
    operations = catalogue["operations"]
    classes = [entry["operation_class"] for entry in operations]
    assert len(classes) == len(set(classes)), "duplicate operation class"
    assert classes == schema["$defs"]["operationClass"]["enum"], "catalogue and schema enum differ"
    for entry in operations:
        assert set(entry) == {"operation_class", "legal_actor_role", "activity", "capability_key",
                              "provider_operation", "activatable"}, entry
        assert entry["operation_class"].startswith("payments."), entry
        assert 3 <= len(entry["activity"]) <= 160 and entry["activity"].isupper(), entry
        assert entry["activity"] != "PAYMENT_RECORDING", "accounting authority is never money-movement authority"
        if entry["activatable"]:
            assert entry["legal_actor_role"] in roles, entry
            assert entry["capability_key"] in capabilities, entry
        else:
            assert entry["legal_actor_role"] is None and entry["capability_key"] is None, entry
    assert [e["provider_operation"] for e in operations] == ["AUTHORIZE", "CAPTURE", "REFUND", "VOID", "PAYOUT"]
    # Collection authority never implies disbursement authority.
    payout_entry = next(e for e in operations if e["provider_operation"] == "PAYOUT")
    assert payout_entry["activatable"] is False and payout_entry["activity"] == "BENEFICIARY_DISBURSEMENT"
    collection = {e["activity"] for e in operations if e["activatable"]}
    assert "BENEFICIARY_DISBURSEMENT" not in collection

    for entry in operations:
        if not entry["activatable"]:
            continue
        good = {**authorized, "operation_class": entry["operation_class"], "legal_actor_role": entry["legal_actor_role"],
                "activity": entry["activity"], "capability_key": entry["capability_key"]}
        decision.validate(good)
        for other in operations:
            if other["activity"] != entry["activity"]:
                assert not decision.is_valid({**good, "activity": other["activity"]}), (entry, other)
            if other["capability_key"] and other["capability_key"] != entry["capability_key"]:
                assert not decision.is_valid({**good, "capability_key": other["capability_key"]}), (entry, other)
        for role in roles:
            if role != entry["legal_actor_role"]:
                assert not decision.is_valid({**good, "legal_actor_role": role}), (entry, role)
    # A payout can never be AUTHORIZED, carry a role or a capability, and only it is NOT_ACTIVATED.
    payout_authorized = {**authorized, "operation_class": "payments.payout.execute", "activity": "BENEFICIARY_DISBURSEMENT"}
    payout_authorized.pop("legal_actor_role")
    payout_authorized.pop("capability_key")
    assert not decision.is_valid(payout_authorized), "AUTHORIZED payout"
    assert not decision.is_valid({**payout, "outcome": "NO_APPLICABLE_MANDATE"}), "payout outcome"
    assert not decision.is_valid({**payout, "legal_actor_role": "PAYMENT_BENEFICIARY"}), "payout role"
    assert not decision.is_valid({**denied, "outcome": "OPERATION_NOT_ACTIVATED"}), "NOT_ACTIVATED on collection"
    assert "evaluated_at + 30 seconds" in schema["$defs"]["MoneyMovementAuthorityDecision"]["description"]

    # Workload-only, non-authorising scope, granted to no ACTIVE workload.
    scopes = yaml.safe_load((CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]
    scope = next(s for s in scopes if s["name"] == SCOPE)
    assert scope["audience"] == ["baobab-control-plane"] and scope["allowed_actors"] == ["workload"]
    assert scope["grants_authority"] is False
    workloads = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())
    holders = {name: w for name, w in workloads["workloads"].items() if SCOPE in w.get("allowed_scopes", [])}
    assert set(holders) == {"baobab-payments-legal-actor-assessor-staging"}, holders
    assert all(w["status"] == "PROVISIONED" and w["environment"] == "staging" for w in holders.values())

    lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())
    entry = next(c for c in lock["contracts"] if c["domain"] == "payments" and c["version"] == "v2")
    assert set(entry["schemas"]) == {"money-movement-authority.schema.json", "money-movement-operations.yaml"}
    print("Payments money-movement authority contract, catalogue, fingerprint vectors, examples and scope passed")


if __name__ == "__main__":
    main()
