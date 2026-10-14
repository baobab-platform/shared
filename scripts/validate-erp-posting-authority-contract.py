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
    assert authorized["activity"] == next(
        e["activity"] for e in catalogue["operations"] if e["operation_class"] == authorized["operation_class"])

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
    assert set(entry["schemas"]) == {"posting-authority.schema.json", "posting-operations.yaml"}
    print("ERP posting-authority contract, catalogue, examples and scope passed")


if __name__ == "__main__":
    main()
