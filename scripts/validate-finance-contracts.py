#!/usr/bin/env python3
"""Offline Finance F1 wire conformance, not an accounting/authority engine.

Validate actual Draft 2020-12 schemas, locally resolved cross-package refs,
synthetic examples, DRAFT catalogue definitions and the published lock index.
Never fetch a schema from a URL or contact CP, IAM, ERP or a provider. Native
posting, exact-decimal balancing, period policy and approval/COMMIT evidence
belong to ERP and are explicitly outside this validator's assurance claim.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PACKAGE = CONTRACTS / "finance/v1"
CAPABILITIES = {"finance.ledger.read", "finance.journal.manage", "finance.statement.read"}


def registry() -> Registry:
    """Only committed local resources can resolve an immutable contract URI.

    Registry's default retrieval raises NoSuchResource. There is deliberately
    no requests/urlopen fallback: a typo or hostile URI must fail offline.
    Register both the published ID and local file URI for existing packages.
    """
    resources = []
    seen = set()
    for path in sorted(CONTRACTS.rglob("*.schema.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        uri = document.get("$id")
        if not uri:
            continue
        if uri in seen:
            raise ValueError("duplicate published schema ID")
        seen.add(uri)
        resource = Resource.from_contents(document, default_specification=DRAFT202012)
        resources.extend(((uri, resource), (path.resolve().as_uri(), resource)))
    return Registry().with_resources(resources)


def refs(value: object) -> Iterator[str]:
    """Inspect all branches, including branches not reached by an example."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref":
                yield child
            else:
                yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def validator(name: str, resources: Registry | None = None) -> Draft202012Validator:
    path = (PACKAGE / name).resolve()
    if not path.is_relative_to(CONTRACTS) or not path.name.endswith(".schema.json"):
        raise ValueError("schema must be a local published contract")
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    formats = FormatChecker()
    required_formats = {"date", "date-time", "uuid", "uri"}
    if not required_formats.issubset(formats.checkers):
        raise RuntimeError("install the pinned Foundation format-validator dependencies")
    return Draft202012Validator(schema, registry=resources or registry(), format_checker=formats)


def validate_package() -> int:
    resources = registry()
    schemas = sorted(PACKAGE.glob("*.schema.json"))
    if len(schemas) != 7:
        raise ValueError("Finance F1 must publish common vocabulary and six wire schemas")
    for path in schemas:
        document = json.loads(path.read_text())
        expected = "https://contracts.baobab-platform.com/finance/v1/" + path.name
        if document.get("$id") != expected:
            raise ValueError("Finance F1 schema ID does not match its published path")
        Draft202012Validator.check_schema(document)
        resolver = resources.resolver(base_uri=expected)
        for reference in refs(document):
            resolver.lookup(reference)

    definitions = yaml.safe_load((PACKAGE / "capabilities.yaml").read_text())["capabilities"]
    if {entry["capability_key"] for entry in definitions} != CAPABILITIES or len(definitions) != 3:
        raise ValueError("Finance F1 capability census drift")
    for entry in definitions:
        if (entry["lifecycle"], entry["maturity"], entry["owner"], entry["data_classification"]) != (
            "DRAFT", "EXPERIMENTAL", "baobab-erp", "RESTRICTED"
        ):
            raise ValueError("Finance F1 vocabulary must not claim provider readiness")
    lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())["contracts"]
    entries = [item for item in lock if item["domain"] == "finance" and item["version"] == "v1"]
    if len(entries) != 1 or set(entries[0]["schemas"]) != {p.name for p in schemas} | {"capabilities.yaml"}:
        raise ValueError("Finance F1 lock index must list every published schema exactly once")
    if len(entries[0]["schemas"]) != 8:
        raise ValueError("Finance F1 lock index contains duplicates")

    count = 0
    manifest = json.loads((PACKAGE / "examples/manifest.json").read_text())
    listed = set()
    for example in manifest:
        path = (PACKAGE / "examples" / example["file"]).resolve()
        if path.parent != (PACKAGE / "examples").resolve() or path in listed:
            raise ValueError("example manifest contains an unsafe or duplicate path")
        listed.add(path)
        validator(example["schema"], resources).validate(json.loads(path.read_text()))
        count += 1
    if listed != {p.resolve() for p in (PACKAGE / "examples").glob("*.json") if p.name != "manifest.json"}:
        raise ValueError("every committed Finance F1 example must be validated")
    return count


if __name__ == "__main__":
    print(f"Finance F1 DRAFT wire contracts passed ({validate_package()} synthetic examples); no provider qualification")
