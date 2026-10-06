#!/usr/bin/env python3
"""Validate ADR-SHARED-025 / RTD-09 intelligence namespace reservation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
CAP = CONTRACTS / "capability" / "v1"
EVENTS = CONTRACTS / "events" / "v1"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


namespace_doc = yaml.safe_load((CAP / "namespace-registry.yaml").read_text())
catalogue_doc = yaml.safe_load((CAP / "catalogue.yaml").read_text())
domain = json.loads((CAP / "domain.schema.json").read_text())
context_doc = yaml.safe_load((EVENTS / "context-registry.yaml").read_text())
event_registry = yaml.safe_load((EVENTS / "event-registry.yaml").read_text())

namespaces = {item["key"]: item for item in namespace_doc.get("namespaces", [])}
if "intelligence" not in namespaces:
    fail("intelligence capability namespace must be registered")
if "pulse" in namespaces:
    fail("pulse must not be a canonical capability namespace")

capability_domains = set(domain.get("$defs", {}).get("capabilityDomain", {}).get("enum", []))
if "intelligence" not in capability_domains:
    fail("capabilityDomain enum must contain intelligence")
if "pulse" in capability_domains:
    fail("capabilityDomain enum must not contain pulse")

catalogued = [
    item.get("capability_key", "")
    for item in (catalogue_doc.get("capabilities") or [])
    if isinstance(item, dict)
]
intelligence_caps = [key for key in catalogued if key.startswith("intelligence.")]
if intelligence_caps:
    fail(f"RTD-09 must not catalogue intelligence capabilities yet: {sorted(intelligence_caps)}")
pulse_caps = [key for key in catalogued if key.startswith("pulse.")]
if pulse_caps:
    fail(f"pulse.* capability keys are forbidden: {sorted(pulse_caps)}")

contexts = {item["key"]: item for item in context_doc.get("contexts", [])}
intelligence = contexts.get("intelligence")
if not intelligence:
    fail("intelligence event context must be reserved")
else:
    if intelligence.get("status") != "RESERVED":
        fail("intelligence event context must remain RESERVED in RTD-09")
    if intelligence.get("stewards") != ["baobab-pulse"]:
        fail("intelligence event context steward must be exactly baobab-pulse")
    if intelligence.get("capability_domains") != ["intelligence"]:
        fail("intelligence event context must map to intelligence capability domain")
    if "ADR-SHARED-025" not in (intelligence.get("authority") or []):
        fail("intelligence event context must cite ADR-SHARED-025")

if "pulse" in contexts:
    fail("pulse must not be registered as an event context")

registered_types = [
    item.get("type", "")
    for item in (event_registry.get("events") or [])
    if isinstance(item, dict)
]
intelligence_events = [t for t in registered_types if t.startswith("com.baobab-platform.intelligence.")]
if intelligence_events:
    fail(f"RTD-09 must not activate intelligence events: {sorted(intelligence_events)}")
pulse_events = [t for t in registered_types if t.startswith("com.baobab-platform.pulse.")]
if pulse_events:
    fail(f"repository-named pulse event types must not be canonical: {sorted(pulse_events)}")

for required in (
    "com.baobab-platform.regulations.document-requirements.determined.v1",
    "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1",
    "com.baobab-platform.documents.regulatory-evidence.offered.v1",
    "com.baobab-platform.documents.document-version.verification-changed.v2",
    "com.baobab-platform.documents.document-version.validity-changed.v2",
):
    if required not in registered_types:
        fail(f"RTD-09 upstream source event is not active in Shared: {required}")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} RTD-09 intelligence namespace failure(s)", file=sys.stderr)
    sys.exit(1)

print("RTD-09 intelligence namespace reservation passed non-promotion, reserved-context and upstream-event invariants")
