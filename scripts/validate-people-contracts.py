#!/usr/bin/env python3
"""Offline verification of Accepted ADR-SHARED-045, not provider qualification.

Run: python scripts/validate-people-contracts.py
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PACKAGE = CONTRACTS / "people/v1"
CAPABILITIES = (
    "payroll.evidence.attest",
    "payroll.run.read",
    "workforce.employment.manage",
    "workforce.employment.read",
)
EVENTS = (
    "com.baobab-platform.payroll.evidence.receipt-verified.v1",
    "com.baobab-platform.workforce.employment.proposal-recorded.v1",
)


def schema_registry() -> Registry:
    registry = Registry()
    seen = set()
    for path in sorted(CONTRACTS.rglob("*.schema.json")):
        document = json.loads(path.read_text())
        uri = document.get("$id")
        if not isinstance(uri, str):
            continue
        if uri in seen:
            raise ValueError(f"duplicate schema URI {uri}")
        seen.add(uri)
        registry = registry.with_resource(uri, Resource.from_contents(document))
    return registry


def references(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref":
                yield value
            else:
                yield from references(value)
    elif isinstance(node, list):
        for child in node:
            yield from references(child)


def validate_schema(name: str, sample: dict, registry=None) -> None:
    if not name.endswith(".schema.json") or "/" in name or ".." in name:
        raise ValueError("only local People schema paths are valid")
    document = json.loads((PACKAGE / name).read_text())
    validator = Draft202012Validator(
        document, registry=registry or schema_registry(), format_checker=FormatChecker()
    )
    validator.validate(sample)


def validate_package() -> int:
    expected = {
        "domain.schema.json",
        "provider-selection.schema.json",
        "employment-read-request.schema.json",
        "employment-read-response.schema.json",
        "employment-manage-request.schema.json",
        "employment-manage-response.schema.json",
        "payroll-run-read-request.schema.json",
        "payroll-run-read-response.schema.json",
        "payroll-evidence-attest-request.schema.json",
        "payroll-evidence-attest-response.schema.json",
        "events.schema.json",
    }
    actual = {p.name for p in PACKAGE.glob("*.schema.json")}
    if actual != expected:
        raise ValueError(f"People schema inventory differs: {actual ^ expected}")
    resources = schema_registry()
    for filename in sorted(expected):
        document = json.loads((PACKAGE / filename).read_text())
        uri = f"https://contracts.baobab-platform.com/people/v1/{filename}"
        if document.get("$id") != uri:
            raise ValueError(f"incorrect immutable ID in {filename}")
        Draft202012Validator.check_schema(document)
        resolver = resources.resolver(base_uri=uri)
        for r in references(document):
            resolver.lookup(r)

    doc = yaml.safe_load((PACKAGE / "capabilities.yaml").read_text())
    caps = doc["capabilities"]
    keys = [entry["capability_key"] for entry in caps]
    if keys != list(CAPABILITIES) or len(set(keys)) != len(keys):
        raise ValueError("People capability list is not precisely governed")
    for entry in caps:
        if (entry["owner"], entry["domain"], entry["lifecycle"],
            entry["maturity"], entry["data_classification"]) != (
            "baobab-erp", entry["capability_key"].split(".")[0], "DRAFT",
            "EXPERIMENTAL", "RESTRICTED"
        ):
            raise ValueError("People provider readiness is falsely represented")
        contract = entry["contracts"]
        if len(contract) != 1 or contract[0]["major"] != 1:
            raise ValueError("People contract major mismatch")
        for field in ("request_schema", "response_schema"):
            if contract[0][field] not in expected:
                raise ValueError("Unknown People request or response schema")
        if contract[0]["error_schema"] != "../../errors/v1/problem-details.schema.json":
            raise ValueError("Generic restricted error contract required")

    catalogue = yaml.safe_load((CONTRACTS / "capability/v1/catalogue.yaml").read_text())["capabilities"]
    selected = [x for x in catalogue if x["capability_key"].split(".")[0] in ("payroll", "workforce")]
    if [x["capability_key"] for x in selected] != list(CAPABILITIES):
        raise ValueError("People catalogue must include only accepted subset")
    if any(x["owner"] != "baobab-erp" or x["source"] != "../../people/v1/capabilities.yaml"
           for x in selected):
        raise ValueError("Provider-neutral capability source drift")

    allowed = yaml.safe_load((CONTRACTS / "capability/v1/namespace-registry.yaml").read_text())
    names = {x["key"] for x in allowed["domains"]}
    if not {"payroll", "workforce"}.issubset(names):
        raise ValueError("People domain not registered")

    lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())["contracts"]
    matches = [x for x in lock if x["domain"] == "people" and x["version"] == "v1"]
    desired = expected | {"asyncapi.yaml", "capabilities.yaml"}
    if len(matches) != 1 or len(matches[0]["schemas"]) != len(desired) or set(matches[0]["schemas"]) != desired:
        raise ValueError("People lock must include every published wire schema")

    contexts = yaml.safe_load((CONTRACTS / "events/v1/context-registry.yaml").read_text())["contexts"]
    for key in ("payroll", "workforce"):
        matches = [x for x in contexts if x["key"] == key]
        if len(matches) != 1 or matches[0]["status"] != "ACTIVE" or matches[0]["capability_domains"] != [key]:
            raise ValueError("People event context registration drift")

    events = yaml.safe_load((CONTRACTS / "events/v1/event-registry.yaml").read_text())["events"]
    matches = [x for x in events if x["type"] in EVENTS]
    if len(matches) != 2 or tuple(sorted(x["type"] for x in matches)) != EVENTS:
        raise ValueError("People event registry mismatch")
    for event in matches:
        if event["asyncapi"] != "contracts/people/v1/asyncapi.yaml" or event["lifecycle"] != "PROPOSED" or "producer" in event:
            raise ValueError("People producer may not be assigned by contract acceptance")

    manifest = json.loads((PACKAGE / "examples/manifest.json").read_text())
    seen = set()
    for row in manifest:
        path = PACKAGE / "examples" / row["file"]
        if row["file"] != Path(row["file"]).name or path in seen or row["schema"] not in expected:
            raise ValueError("Invalid or duplicate People example")
        seen.add(path)
        validate_schema(row["schema"], json.loads(path.read_text()), resources)
    available = {p for p in (PACKAGE / "examples").glob("*.json") if p.name != "manifest.json"}
    if available != seen:
        raise ValueError("Unvalidated People examples")
    return len(seen)


if __name__ == "__main__":
    print(f"People v1 contract conformance PASS: {validate_package()} synthetic examples; no live provider activation")
