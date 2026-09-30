#!/usr/bin/env python3
"""Event context and event-type registry validation (ADR-SHARED-018 SS3.5).

Checks contracts/events/v1/context-registry.yaml and event-registry.yaml
against their schemas, the capability namespace registry and every
contracts/*/v*/asyncapi.yaml:

  1. both registries match their JSON Schemas;
  2. context keys and event types are unique and sorted;
  3. context keys follow the naming hygiene rules (no vendor, engine,
     tenant, Digital Estate or platform token), except a DEPRECATED
     context kept for compatibility;
  4. every related capability domain is registered in
     contracts/capability/v1/namespace-registry.yaml;
  5. the event registry and the AsyncAPI messages correspond one to one,
     and each entry names the AsyncAPI document that defines it;
  6. every type's context is registered; RESERVED contexts carry no types;
     a DEPRECATED context carries exactly its frozen_types;
  7. a type that is not PROPOSED has a producer, and the producer is a
     steward of the type's context;
  8. the segments after the context follow the hygiene rules, unless an
     already-published type carries a naming_exception;
  9. every legacy type in `supersedes` is superseded only once;
 10. a legacy com.nabhold.* type appears in event-registry.yaml only as a
     `supersedes` value (validate-event-registry.py exempts this file from
     its legacy-type ban on that basis).

The envelope pattern stays the syntax gate. Payload resolution and example
validation stay in scripts/validate-event-registry.py.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/event_contexts.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
EVENTS = CONTRACTS / "events" / "v1"
TYPE_PREFIX = "com.baobab-platform."
LEGACY_TYPE = re.compile(r"com\.nabhold\.[a-z0-9]+(?:[.-][a-z0-9]+)*(?:\.v[1-9][0-9]*)?")

# Tokens a context or type segment may not contain (ADR-SHARED-018 SS3.4):
# vendor and product names, Digital Estates and tenants, engine roles and the
# platform itself. Country and region names are reviewed by hand.
FORBIDDEN_TOKENS = frozenset({
    "baobab", "nabhold", "zuribeans", "thamani", "equator",
    "medusa", "medusajs", "idempiere", "payload", "haystack", "keycloak", "ory",
    "killbill", "stripe", "erp", "cms", "iam",
})


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def schema_errors(schema_path: Path, document: object, label: str) -> list[str]:
    validator = Draft202012Validator(json.loads(schema_path.read_text()))
    return [
        f"{label}: {'/'.join(str(p) for p in error.absolute_path) or '(root)'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda e: list(map(str, e.absolute_path)))
    ]


def forbidden_tokens(text: str) -> set[str]:
    return {token for token in text.replace(".", "-").split("-") if token in FORBIDDEN_TOKENS}


def asyncapi_messages(contracts: Path) -> dict[str, str]:
    """Map each AsyncAPI message name to the document that defines it."""
    found: dict[str, str] = {}
    for path in sorted(contracts.rglob("asyncapi.yaml")):
        document = load_yaml(path) or {}
        for message in ((document.get("components") or {}).get("messages") or {}).values():
            name = (message or {}).get("name")
            if isinstance(name, str):
                found.setdefault(name, str(path.relative_to(contracts.parent)))
    return found


def validate(contexts_doc: dict, events_doc: dict, capability_domains: set[str],
             messages: dict[str, str], events_text: str = "") -> list[str]:
    failures: list[str] = []
    failures += schema_errors(EVENTS / "context-registry.schema.json", contexts_doc, "context-registry.yaml")
    failures += schema_errors(EVENTS / "event-registry.schema.json", events_doc, "event-registry.yaml")
    if failures:
        return failures

    contexts = contexts_doc["contexts"]
    keys = [context["key"] for context in contexts]
    if len(set(keys)) != len(keys):
        failures.append("context-registry.yaml: duplicate context keys")
    if keys != sorted(keys):
        failures.append("context-registry.yaml: contexts are not sorted by key")
    by_key = {context["key"]: context for context in contexts}
    for context in contexts:
        key = context["key"]
        tokens = forbidden_tokens(key)
        if tokens and context["status"] != "DEPRECATED":
            failures.append(f"context {key}: names {sorted(tokens)}; contexts name business contexts only")
        for domain in context.get("capability_domains", []):
            if domain not in capability_domains:
                failures.append(f"context {key}: capability domain {domain} is not registered")

    events = events_doc["events"]
    types = [event["type"] for event in events]
    if len(set(types)) != len(types):
        failures.append("event-registry.yaml: duplicate event types")
    if types != sorted(types):
        failures.append("event-registry.yaml: events are not sorted by type")
    for missing in sorted(set(messages) - set(types)):
        failures.append(f"{messages[missing]}: {missing} is not in event-registry.yaml")
    for extra in sorted(set(types) - set(messages)):
        failures.append(f"event-registry.yaml: {extra} is defined by no AsyncAPI document")

    used_by_context: dict[str, set[str]] = {}
    superseded: dict[str, str] = {}
    for event in events:
        event_type = event["type"]
        if event_type in messages and messages[event_type] != event["asyncapi"]:
            failures.append(f"{event_type}: defined in {messages[event_type]}, not {event['asyncapi']}")
        segments = event_type[len(TYPE_PREFIX):].split(".")
        key = segments[0]
        used_by_context.setdefault(key, set()).add(event_type)
        context = by_key.get(key)
        if context is None:
            failures.append(f"{event_type}: context {key} is not registered")
        elif context["status"] == "RESERVED":
            failures.append(f"{event_type}: context {key} is RESERVED and carries no event types")
        if len(segments) < 3:
            failures.append(f"{event_type}: needs at least <context>.<fact>.v<major>")
        tokens = forbidden_tokens(".".join(segments[1:-1]))
        if tokens and "naming_exception" not in event:
            failures.append(f"{event_type}: names {sorted(tokens)} without a naming_exception")
        producer = event.get("producer")
        if event["lifecycle"] == "PROPOSED" and producer:
            failures.append(f"{event_type}: a PROPOSED type has no producer yet; make it ACTIVE with its producer")
        if producer and context is not None and producer not in context["stewards"]:
            failures.append(f"{event_type}: producer {producer} is not a steward of context {key}")
        for legacy in event.get("supersedes", []):
            if legacy in superseded:
                failures.append(f"{legacy}: superseded by both {superseded[legacy]} and {event_type}")
            superseded[legacy] = event_type

    mentioned = LEGACY_TYPE.findall(events_text)
    if len(mentioned) != sum(len(event.get("supersedes", [])) for event in events) \
            or not set(mentioned) <= set(superseded):
        failures.append("event-registry.yaml: a legacy com.nabhold.* type appears outside a `supersedes` list")

    for context in contexts:
        if context["status"] == "DEPRECATED":
            used = used_by_context.get(context["key"], set())
            frozen = set(context["frozen_types"])
            for extra in sorted(used - frozen):
                failures.append(f"{extra}: context {context['key']} is DEPRECATED and accepts no new types")
            for gone in sorted(frozen - used):
                failures.append(f"context {context['key']}: frozen type {gone} is not registered")
    return failures


def main() -> int:
    namespace = load_yaml(CONTRACTS / "capability" / "v1" / "namespace-registry.yaml")
    failures = validate(
        load_yaml(EVENTS / "context-registry.yaml"),
        load_yaml(EVENTS / "event-registry.yaml"),
        {domain["key"] for domain in namespace["domains"]},
        asyncapi_messages(CONTRACTS),
        (EVENTS / "event-registry.yaml").read_text(),
    )
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    if failures:
        print(f"{len(failures)} event context failure(s)", file=sys.stderr)
        return 1
    events = load_yaml(EVENTS / "event-registry.yaml")["events"]
    active = sum(1 for event in events if event["lifecycle"] != "PROPOSED")
    print(f"event context and type registries passed ({len(events)} types, {active} with a registered producer)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
