#!/usr/bin/env python3
"""Census invariants for ADR-SHARED-027."""

from __future__ import annotations

from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "contracts/capability/v1/catalogue.yaml"
DEFINITIONS = ROOT / "contracts/regulations/v1/capabilities.yaml"

catalogue = yaml.safe_load(CATALOGUE.read_text())
definitions = yaml.safe_load(DEFINITIONS.read_text())

catalogued = {
    item["capability_key"]: item
    for item in catalogue.get("capabilities", [])
    if isinstance(item, dict) and str(item.get("capability_key", "")).startswith("regulations.")
}
assert set(catalogued) == {
    "regulations.evidence.assess",
    "regulations.requirement.resolve",
}

defined = {
    item["capability_key"]: item
    for item in definitions.get("capabilities", [])
    if isinstance(item, dict)
}
assert set(defined) == set(catalogued)

for key, item in defined.items():
    assert item["owner"] == "baobab-regulations"
    assert item["domain"] == "regulations"
    assert item["lifecycle"] == "DRAFT"
    assert item["maturity"] == "EXPERIMENTAL"
    assert item["data_classification"] == "TENANT_CONFIDENTIAL"
    assert item["metadata"]["provider_implementation"] == "governed-by-engine-declaration"
    assert "implementation_status" not in item["metadata"]
    assert catalogued[key]["source"] == "../../regulations/v1/capabilities.yaml"

assert (
    defined["regulations.requirement.resolve"]["contracts"][0]["request_schema"]
    == "../../regulatory-document-exchange/v1/domain.schema.json#/$defs/requirementResolveRequest"
)
assert (
    defined["regulations.requirement.resolve"]["contracts"][0]["response_schema"]
    == "../../regulatory-document-exchange/v1/domain.schema.json#/$defs/requirementResolveResponse"
)
assert (
    defined["regulations.evidence.assess"]["contracts"][0]["request_schema"]
    == "../../regulatory-document-exchange/v1/domain.schema.json#/$defs/documentEvidenceAssessmentRequest"
)
assert (
    defined["regulations.evidence.assess"]["contracts"][0]["response_schema"]
    == "../../regulatory-document-exchange/v1/domain.schema.json#/$defs/documentEvidenceAssessmentResult"
)

# The first census deliberately does not canonicalize the broader proposals.
for forbidden in (
    "regulations.context.resolve",
    "regulations.decision.evaluate",
    "regulations.change.subscribe",
    "regulations.pack.compose",
):
    assert forbidden not in catalogued

# RTD-10 must now pin the capability vocabulary it uses for Regulations.
sys.path.insert(0, str(ROOT / "scripts"))
import rtd_conformance as rtd  # noqa: E402

assert "contracts/capability/v1/catalogue.yaml" in rtd.ROLE_CONTRACTS["REGULATIONS_AUTHORITY"]
assert "contracts/regulations/v1/capabilities.yaml" in rtd.ROLE_CONTRACTS["REGULATIONS_AUTHORITY"]

print("ADR-SHARED-027 Regulations capability census invariants passed")
