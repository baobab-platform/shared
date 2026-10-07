#!/usr/bin/env python3
"""Census invariants for ADR-SHARED-029."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "contracts/capability/v1/catalogue.yaml"
DEFINITIONS = ROOT / "contracts/intelligence/v1/capabilities.yaml"
DOMAIN = ROOT / "contracts/intelligence/v1/domain.schema.json"

catalogue = yaml.safe_load(CATALOGUE.read_text())
definitions = yaml.safe_load(DEFINITIONS.read_text())
domain = json.loads(DOMAIN.read_text())

catalogued = {
    item["capability_key"]: item
    for item in catalogue.get("capabilities", [])
    if isinstance(item, dict) and str(item.get("capability_key", "")).startswith("intelligence.")
}
assert set(catalogued) == {
    "intelligence.evidence.search",
    "intelligence.research-mission.manage",
}

defined = {
    item["capability_key"]: item
    for item in definitions.get("capabilities", [])
    if isinstance(item, dict)
}
assert set(defined) == set(catalogued)

for key, item in defined.items():
    assert item["owner"] == "baobab-pulse"
    assert item["domain"] == "intelligence"
    assert item["lifecycle"] == "DRAFT"
    assert item["maturity"] == "EXPERIMENTAL"
    assert item["data_classification"] == "TENANT_CONFIDENTIAL"
    assert item["metadata"]["authority"] == "ADR-SHARED-031"
    assert item["metadata"]["provider_implementation"] == "p-cap-07-readiness-governed"
    assert catalogued[key]["source"] == "../../intelligence/v1/capabilities.yaml"

defs = domain["$defs"]

evidence_request = defs["evidenceSearchRequest"]
research_create = defs["researchMissionCreateRequest"]
forbidden_authority = {
    "tenant_id",
    "requester_clearance",
    "principal_id",
    "capability_grant_id",
}
assert forbidden_authority.isdisjoint(evidence_request["properties"])
assert forbidden_authority.isdisjoint(research_create["properties"])

encoded = json.dumps(domain, sort_keys=True).lower()
for forbidden_vendor in (
    "qdrant_point_id",
    "embedding_vector",
    "haystack_pipeline",
    "model_provider",
):
    assert forbidden_vendor not in encoded

candidate = defs["evidenceCandidate"]
assert set(candidate["required"]) == {
    "canonical_object_id",
    "evidence_set_id",
    "score",
    "is_stale",
}
assert "confidence" not in candidate["properties"]
assert "quality" not in candidate["properties"]

mission_status = set(defs["researchMissionStatus"]["enum"])
assert mission_status == {
    "PROPOSED",
    "SCOPED",
    "SOURCE_PLANNED",
    "ACQUIRING",
    "ANALYSING",
    "REVIEW",
    "PUBLISHED",
    "SUSPENDED",
    "CANCELLED",
    "INSUFFICIENT_EVIDENCE",
    "SUPERSEDED",
}

manage = defs["researchMissionManageRequest"]
refs = {item["$ref"] for item in manage["oneOf"]}
assert refs == {
    "#/$defs/researchMissionCreateRequest",
    "#/$defs/researchMissionGetRequest",
}

assert (
    defined["intelligence.evidence.search"]["contracts"][0]["request_schema"]
    == "domain.schema.json#/$defs/evidenceSearchRequest"
)
assert (
    defined["intelligence.evidence.search"]["contracts"][0]["response_schema"]
    == "domain.schema.json#/$defs/evidenceSearchResponse"
)
assert (
    defined["intelligence.research-mission.manage"]["contracts"][0]["request_schema"]
    == "domain.schema.json#/$defs/researchMissionManageRequest"
)
assert (
    defined["intelligence.research-mission.manage"]["contracts"][0]["response_schema"]
    == "domain.schema.json#/$defs/researchMissionResponse"
)

# The first census deliberately rejects speculative capability proliferation.
for forbidden in (
    "intelligence.signal.detect",
    "intelligence.risk.assess",
    "intelligence.opportunity.detect",
    "intelligence.forecast.generate",
    "intelligence.recommendation.generate",
    "intelligence.regulatory.query",
):
    assert forbidden not in catalogued

print("ADR-SHARED-029 Pulse intelligence capability census invariants passed")
