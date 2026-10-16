#!/usr/bin/env python3
"""P0-04B ERP posting-authority contract conformance (ADR-SHARED-034).

Checks the erp/v2 schema, catalogue, examples, negative fixtures and the
workload-only, non-authorising scope. Synthetic examples prove the contract
shape only; they are not evidence of a running resolver or of posting support.
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
V2 = CONTRACTS / "erp/v2"
SCOPE = "erp-posting-authority:resolve"
VENDOR = ("ad_client", "ad_org", "c_", "m_", "gl_", "fact_acct", "record_id")


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


def main() -> None:
    schema = json.loads((V2 / "posting-authority.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    assert schema["$id"] == BASE + "erp/v2/posting-authority.schema.json"
    # Native placement stays ERP-owned: no vendor identifier is a contract field.
    for key in walk_keys(schema):
        assert not key.lower().startswith(VENDOR), f"vendor field {key!r} in erp/v2"
    reg = registry()
    request = validator(schema, "PostingAuthorityRequest", reg)
    decision = validator(schema, "PostingAuthorityDecision", reg)

    examples = V2 / "examples"
    good_request = json.loads((examples / "posting-authority-request.json").read_text())
    authorized = json.loads((examples / "posting-authority-decision-authorized.json").read_text())
    denied = json.loads((examples / "posting-authority-decision-denied.json").read_text())
    request.validate(good_request)
    decision.validate(authorized)
    decision.validate(denied)

    # The caller can never select authority, identity or time.
    for forged in ["tenant_id", "operating_organisation_id", "legal_entity_id", "responsible_legal_entity_id",
                   "mandate_id", "role", "legal_actor_role", "activity", "market", "capability",
                   "effective_at", "evaluated_at", "ad_client_id", "ad_org_id"]:
        assert not request.is_valid({**good_request, forged: "forged"}), forged
    for required in ["context_id", "engine_instance_id", "operation_class",
                     "native_placement_reference", "operation_reference"]:
        bad = copy.deepcopy(good_request)
        del bad[required]
        assert not request.is_valid(bad), required
    for bad_value in [{"operation_class": "erp.anything.post"}, {"engine_instance_id": "erp-1"},
                      {"context_id": "not-a-uuid"}, {"operation_reference": "has space"},
                      {"operation_reference": "x" * 257},
                      {"native_placement_reference": {"placement_id": good_request["native_placement_reference"]["placement_id"], "placement_version": 0}},
                      {"native_placement_reference": {**good_request["native_placement_reference"], "ad_org_id": 11}}]:
        assert not request.is_valid({**good_request, **bad_value}), bad_value

    # AUTHORIZED carries the full actor; every other outcome carries none of it.
    for required in ["tenant_id", "operating_organisation_id", "market", "legal_actor_role", "activity",
                     "mandate_id", "responsible_legal_entity_id", "evidence_references",
                     "mandate_effective_from", "expires_at", "decision_id"]:
        bad = copy.deepcopy(authorized)
        del bad[required]
        assert not decision.is_valid(bad), required
    for leaked in ["mandate_id", "responsible_legal_entity_id", "evidence_references", "expires_at",
                   "supersedes_mandate_id", "mandate_effective_from"]:
        assert not decision.is_valid({**denied, leaked: authorized[leaked]}), leaked
    # Evidence is projected whole: a mandate's evidence list has no cap, so
    # neither does the decision that cites it.
    decision.validate({**authorized, "evidence_references": [f"synthetic:evidence/{i}" for i in range(25)]})
    assert schema["$defs"]["PostingAuthorityDecision"]["properties"]["evidence_references"].get("maxItems") is None
    assert not decision.is_valid({**authorized, "evidence_references": []})
    assert not decision.is_valid({**authorized, "evidence_references": ["dup", "dup"]})
    assert not decision.is_valid({**authorized, "provider_permissions_granted": True})
    assert not decision.is_valid({**authorized, "outcome": "PROVIDER_RESTRICTED"})
    issued = datetime.fromisoformat(authorized["evaluated_at"].replace("Z", "+00:00"))
    expires = datetime.fromisoformat(authorized["expires_at"].replace("Z", "+00:00"))
    assert issued < expires <= issued + timedelta(seconds=30), "examples must keep the 30 s lease"

    # The catalogue is closed, one role and activity per class, matching the schema enum.
    catalogue = yaml.safe_load((V2 / "posting-operations.yaml").read_text())
    roles = json.loads((CONTRACTS / "organisation/v2/legal-actor-mandate.schema.json").read_text())[
        "$defs"]["legalActorRole"]["enum"]
    classes = [entry["operation_class"] for entry in catalogue["operations"]]
    assert len(classes) == len(set(classes)), "duplicate operation class"
    assert classes == schema["$defs"]["operationClass"]["enum"], "catalogue and schema enum differ"
    for entry in catalogue["operations"]:
        assert set(entry) == {"operation_class", "legal_actor_role", "activity", "capability_key"}, entry
        assert entry["legal_actor_role"] in roles, entry
        assert 3 <= len(entry["activity"]) <= 160 and entry["activity"].isupper(), entry
        assert entry["capability_key"] is None, "finance capability keys await ADR-SHARED-033"
    # Role and activity are bound to the operation class by the schema itself,
    # mirroring the catalogue entry for entry.
    bindings = [rule for rule in schema["$defs"]["PostingAuthorityDecision"]["allOf"]
                if "operation_class" in rule.get("if", {}).get("properties", {})]
    assert {(b["if"]["properties"]["operation_class"]["const"],
             b["then"]["properties"]["legal_actor_role"]["const"],
             b["then"]["properties"]["activity"]["const"]) for b in bindings} == {
        (e["operation_class"], e["legal_actor_role"], e["activity"]) for e in catalogue["operations"]}
    for entry in catalogue["operations"]:
        good = {**authorized, "operation_class": entry["operation_class"],
                "legal_actor_role": entry["legal_actor_role"], "activity": entry["activity"]}
        decision.validate(good)
        for other in catalogue["operations"]:
            if other["legal_actor_role"] != entry["legal_actor_role"]:
                assert not decision.is_valid({**good, "legal_actor_role": other["legal_actor_role"]}), (entry, other)
            if other["activity"] != entry["activity"]:
                assert not decision.is_valid({**good, "activity": other["activity"]}), (entry, other)
    assert not decision.is_valid({**denied, "legal_actor_role": "ACCOUNTING_ENTITY"}), "denied role/class mismatch"
    assert "evaluated_at + 30 seconds" in schema["$defs"]["PostingAuthorityDecision"]["description"]

    # Catalogue version 2 (ADR-SHARED-037): version 1 classes are unchanged and
    # first, in order; the revision only appends purchase-side recording classes.
    assert catalogue["version"] == 2, "catalogue revision must be versioned"
    v1 = [("erp.gl-journal.post", "ACCOUNTING_ENTITY", "GENERAL_LEDGER_POSTING"),
          ("erp.customer-invoice.issue", "INVOICE_ISSUER", "CUSTOMER_INVOICE_ISSUANCE"),
          ("erp.payment.record", "ACCOUNTING_ENTITY", "PAYMENT_RECORDING"),
          ("erp.allocation.record", "ACCOUNTING_ENTITY", "PAYMENT_ALLOCATION"),
          ("erp.shipment.complete", "CONTRACTING_PARTY", "GOODS_DELIVERY"),
          ("erp.sales-order.complete", "CONTRACTING_PARTY", "SALES_ORDER_COMMITMENT")]
    as_tuples = [(e["operation_class"], e["legal_actor_role"], e["activity"]) for e in catalogue["operations"]]
    assert as_tuples[:len(v1)] == v1, "version 1 classes must stay unchanged and first"
    assert as_tuples[len(v1):] == [
        ("erp.purchase-order.complete", "CONTRACTING_PARTY", "PURCHASE_ORDER_COMMITMENT"),
        ("erp.material-receipt.complete", "CONTRACTING_PARTY", "GOODS_RECEIPT"),
        ("erp.vendor-invoice.record", "ACCOUNTING_ENTITY", "VENDOR_INVOICE_RECORDING"),
        ("erp.vendor-payment.record", "ACCOUNTING_ENTITY", "VENDOR_PAYMENT_RECORDING"),
        ("erp.payables-allocation.record", "ACCOUNTING_ENTITY", "PAYABLES_ALLOCATION")], "ADR-SHARED-037 table"
    activities = [e["activity"] for e in catalogue["operations"]]
    assert len(activities) == len(set(activities)), "each class needs its own activity scope"
    # Recording is never money movement: no ERP activity or class name may
    # coincide with, or read as, a payments/v2 movement (ADR-SHARED-035 §1).
    money = yaml.safe_load((CONTRACTS / "payments/v2/money-movement-operations.yaml").read_text())["operations"]
    assert not set(activities) & {m["activity"] for m in money}, "ERP activity reuses a money-movement activity"
    for entry in catalogue["operations"]:
        assert not entry["operation_class"].endswith((".disburse", ".execute", ".payout")), entry
    assert all(entry["legal_actor_role"] != "INVOICE_ISSUER" for entry in catalogue["operations"]
               if entry["operation_class"].startswith(("erp.vendor-", "erp.purchase-", "erp.material-",
                                                       "erp.payables-"))), "a buyer never issues"
    vendor_payment = json.loads((examples / "posting-authority-decision-vendor-payment-authorized.json").read_text())
    decision.validate(vendor_payment)
    assert not decision.is_valid({**vendor_payment, "activity": "PAYMENT_RECORDING"}), "receipt scope != disbursement"

    # Golden vectors: complete over the catalogue and agreeing with the schema.
    vectors = json.loads((examples / "catalogue-vectors.json").read_text())
    assert vectors["catalogue_version"] == catalogue["version"]
    assert vectors["base_example"] == "posting-authority-decision-authorized.json"
    expected = set()
    # Every legal-actor role, not only the ones ERP uses: a consumer that accepts
    # e.g. PAYMENT_BENEFICIARY for an ERP class must fail a vector.
    all_roles = roles
    for entry in catalogue["operations"]:
        expected.add((entry["operation_class"], entry["legal_actor_role"], entry["activity"], "VALID"))
        expected |= {(entry["operation_class"], role, entry["activity"], "INVALID")
                     for role in all_roles if role != entry["legal_actor_role"]}
        expected |= {(entry["operation_class"], entry["legal_actor_role"], act, "INVALID")
                     for act in activities if act != entry["activity"]}
    got = [(v["operation_class"], v["legal_actor_role"], v["activity"], v["expected"]) for v in vectors["vectors"]]
    assert len(got) == len(set(got)) and set(got) == expected, "golden vectors incomplete or stale"
    assert len({v["vector_id"] for v in vectors["vectors"]}) == len(got), "duplicate vector_id"
    for v in vectors["vectors"]:
        candidate = {**authorized, "operation_class": v["operation_class"],
                     "legal_actor_role": v["legal_actor_role"], "activity": v["activity"]}
        assert decision.is_valid(candidate) == (v["expected"] == "VALID"), v["vector_id"]
        request.validate({**good_request, "operation_class": v["operation_class"]})
    assert authorized["activity"] == next(
        e["activity"] for e in catalogue["operations"] if e["operation_class"] == authorized["operation_class"])

    # ERP-B (ADR-SHARED-038): vendor-payment recording needs independently
    # verified execution evidence. The catalogue stays frozen at version 2.
    evidence_schema = json.loads((V2 / "payment-execution-evidence.schema.json").read_text())
    Draft202012Validator.check_schema(evidence_schema)
    assert evidence_schema["$id"] == BASE + "erp/v2/payment-execution-evidence.schema.json"
    for key in walk_keys(evidence_schema):
        assert not key.lower().startswith(VENDOR), f"vendor field {key!r} in erp/v2 evidence"
    evidence = validator(evidence_schema, "PaymentExecutionEvidence", reg)
    good_evidence = json.loads((examples / "payment-execution-evidence-synthetic.json").read_text())
    evidence.validate(good_evidence)
    # The only admissible authority is synthetic: a real one needs a revision.
    assert evidence_schema["$defs"]["executionAuthority"]["enum"] == ["SYNTHETIC_ENGINE_LOCAL"]
    for required in evidence_schema["$defs"]["PaymentExecutionEvidence"]["required"]:
        bad = copy.deepcopy(good_evidence)
        del bad[required]
        assert not evidence.is_valid(bad), required
    for bad_value in [{"execution_authority": "PAYMENTS_PAYOUT"}, {"execution_authority": "BANK_STATEMENT"},
                      {"amount": "0"}, {"amount": "0.00"}, {"amount": "-5"}, {"amount": "1e3"},
                      {"amount": 1250}, {"currency": "zar"}, {"responsible_legal_entity_id": "le-1"},
                      {"payee_reference": "has space"}, {"obligation_reference": ""},
                      {"evidence_references": []}, {"evidence_references": ["dup", "dup"]},
                      {"native_placement_reference": {**good_evidence["native_placement_reference"], "ad_org_id": 11}}]:
        assert not evidence.is_valid({**good_evidence, **bad_value}), bad_value
    # Evidence is a fact, never an instruction or a grant.
    for forged in ["disbursement_instruction", "destination", "bank_account", "provider_permissions_granted",
                   "operation_class", "mandate_id", "decision_id", "c_payment_id", "ad_client_id"]:
        assert not evidence.is_valid({**good_evidence, forged: "forged"}), forged
    assert catalogue["version"] == 2, "ERP-B freezes the catalogue at version 2"

    # Workload-only, non-authorising scope, granted to no ACTIVE workload.
    scopes = yaml.safe_load((CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]
    scope = next(s for s in scopes if s["name"] == SCOPE)
    assert scope["audience"] == ["baobab-control-plane"] and scope["allowed_actors"] == ["workload"]
    assert scope["grants_authority"] is False
    workloads = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())
    holders = {name: w for name, w in workloads["workloads"].items() if SCOPE in w.get("allowed_scopes", [])}
    assert set(holders) == {"baobab-erp-legal-actor-assessor-staging"}, holders
    assert all(w["status"] == "PROVISIONED" and w["environment"] == "staging" for w in holders.values())

    lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())
    entry = next(c for c in lock["contracts"] if c["domain"] == "erp" and c["version"] == "v2")
    assert set(entry["schemas"]) == {"payment-execution-evidence.schema.json", "posting-authority.schema.json",
                                     "posting-operations.yaml"}
    print("ERP posting-authority contract, catalogue, examples and scope passed")


if __name__ == "__main__":
    main()
