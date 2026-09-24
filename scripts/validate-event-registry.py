#!/usr/bin/env python3
"""Validate the platform-wide event registry (ADR-SHARED-008).

Every event type in the Baobab platform is registered in exactly one
contracts/<package>/v<N>/asyncapi.yaml under the single
com.baobab-platform.* namespace. This gate checks, across all packages:

  1. every message name matches the canonical envelope's type pattern and
     is registered exactly once platform-wide;
  2. every message is composed with the canonical envelope and its data
     $ref resolves to a schema in this repository;
  3. every example envelope under contracts/**/examples validates against
     the envelope plus the data schema registered for its type, and no
     example uses an unregistered type;
  4. no contract file mentions a legacy com.nabhold.* event type.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-event-registry.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
BASE_URI = "https://contracts.baobab-platform.com/"
ENVELOPE_ID = BASE_URI + "events/v1/envelope.schema.json"
ENVELOPE_REFS = {"../../events/v1/envelope.schema.json", "./event-envelope.schema.json"}
# Fixtures that exist to prove the envelope rejects legacy shapes.
EXCLUDED_EXAMPLE_DIRS = {CONTRACTS / "events" / "v1" / "compatibility"}
LEGACY_TYPE = re.compile(r"com\.nabhold\.[a-z0-9]")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


registry = Registry()
# Packages do not all mint $id from one host, so data $refs are resolved
# through the file they name on disk and that file's own $id.
id_by_path: dict[Path, str] = {}
for path in sorted(CONTRACTS.rglob("*.json")):
    try:
        document = json.loads(path.read_text())
    except json.JSONDecodeError:
        continue
    if isinstance(document, dict) and isinstance(document.get("$id"), str):
        registry = registry.with_resource(document["$id"], Resource.from_contents(document))
        id_by_path[path.resolve()] = document["$id"]

envelope_schema = json.loads((CONTRACTS / "events" / "v1" / "envelope.schema.json").read_text())
type_pattern = re.compile(envelope_schema["properties"]["type"]["pattern"])

# type -> (asyncapi path, absolute data schema URI)
registered: dict[str, tuple[Path, str]] = {}
for asyncapi_path in sorted(CONTRACTS.rglob("asyncapi.yaml")):
    document = yaml.safe_load(asyncapi_path.read_text()) or {}
    for key, message in ((document.get("components") or {}).get("messages") or {}).items():
        name = message.get("name", "")
        where = f"{rel(asyncapi_path)} message {key}"
        if not type_pattern.match(name):
            fail(f"{where}: {name!r} is not a canonical com.baobab-platform event type")
            continue
        if name in registered:
            fail(f"{where}: {name} is already registered in {rel(registered[name][0])}")
            continue
        layers = ((message.get("payload") or {}).get("allOf")) or []
        if not any(isinstance(layer, dict) and layer.get("$ref") in ENVELOPE_REFS for layer in layers):
            fail(f"{where}: payload is not composed with the canonical envelope")
        data_refs = [layer.get("properties", {}).get("data", {}).get("$ref")
                     for layer in layers if isinstance(layer, dict)]
        data_refs = [ref for ref in data_refs if ref]
        if len(data_refs) != 1:
            fail(f"{where}: expected exactly one data $ref, found {data_refs}")
            continue
        ref_path, _, fragment = data_refs[0].partition("#")
        schema_id = id_by_path.get((asyncapi_path.parent / ref_path).resolve())
        if schema_id is None:
            fail(f"{where}: data $ref {data_refs[0]!r} names no schema file with an $id")
            continue
        data_uri = schema_id + ("#" + fragment if fragment else "")
        try:
            registry.resolver().lookup(data_uri)
        except Exception:  # noqa: BLE001
            fail(f"{where}: data $ref {data_refs[0]!r} does not resolve ({data_uri})")
            continue
        registered[name] = (asyncapi_path, data_uri)


def envelope_errors(envelope: dict, data_uri: str) -> list[str]:
    composed = {"allOf": [{"$ref": ENVELOPE_ID},
                          {"type": "object", "properties": {"data": {"$ref": data_uri}}}]}
    validator = Draft202012Validator(composed, registry=registry)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
            for e in validator.iter_errors(envelope)]


examples = 0
for path in sorted(CONTRACTS.rglob("examples/**/*.json")):
    if any(excluded in path.parents for excluded in EXCLUDED_EXAMPLE_DIRS):
        continue
    document = json.loads(path.read_text())
    if not (isinstance(document, dict) and "specversion" in document and "type" in document):
        continue
    examples += 1
    entry = registered.get(document["type"])
    if entry is None:
        fail(f"{rel(path)}: example event type {document['type']!r} is not registered in any asyncapi.yaml")
        continue
    for error in envelope_errors(document, entry[1]):
        fail(f"{rel(path)}: {error}")

for path in sorted(CONTRACTS.rglob("*")):
    if path.is_file() and path.suffix in {".json", ".yaml", ".yml", ".md"} \
            and not any(excluded in path.parents for excluded in EXCLUDED_EXAMPLE_DIRS):
        if LEGACY_TYPE.search(path.read_text(errors="ignore")):
            fail(f"{rel(path)}: mentions a legacy com.nabhold.* event type; use com.baobab-platform.*")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} event registry failure(s)", file=sys.stderr)
    sys.exit(1)
print(f"event registry passed ({len(registered)} event types, {examples} example envelopes)")
