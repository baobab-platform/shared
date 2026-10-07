#!/usr/bin/env python3
"""Self-tests for RTD-10 conformance profile governance."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import rtd_conformance as rtd  # noqa: E402


def load(name: str) -> dict:
    return yaml.safe_load(
        (ROOT / "contracts/rtd-conformance/v1/examples" / name).read_text()
    )


def assert_valid(name: str) -> None:
    findings = rtd.schema_findings(load(name))
    assert not findings, f"{name}: {findings}"


for example in ("regulations.yaml", "trade-docs.yaml", "pulse.yaml"):
    assert_valid(example)

bad = copy.deepcopy(load("regulations.yaml"))
bad["repository"]["maturity"] = "ARCHITECTURE_ONLY"
assert rtd.schema_findings(bad), "Regulations role must require DOMAIN_RUNTIME"

bad = copy.deepcopy(load("trade-docs.yaml"))
bad["repository"]["id"] = "baobab-pulse"
assert rtd.schema_findings(bad), "Trade Docs role must bind baobab-trade-docs"

bad = copy.deepcopy(load("pulse.yaml"))
bad["evidence"]["test_paths"] = []
assert rtd.schema_findings(bad), "Pulse implemented consumer must provide test evidence"

assert "contracts/cross-engine-reference/v1/domain.schema.json" in rtd.ROLE_CONTRACTS["REGULATIONS_AUTHORITY"]
assert "contracts/trade-document/v2/domain.schema.json" in rtd.ROLE_CONTRACTS["TRADE_DOCUMENT_AUTHORITY"]
assert "contracts/regulatory-document-exchange/v1/events.schema.json" in rtd.ROLE_CONTRACTS["INTELLIGENCE_CONSUMER"]
assert "contracts/capability/v1/catalogue.yaml" in rtd.ROLE_CONTRACTS["INTELLIGENCE_CONSUMER"]
assert "contracts/intelligence/v1/capabilities.yaml" in rtd.ROLE_CONTRACTS["INTELLIGENCE_CONSUMER"]
assert "contracts/intelligence/v1/domain.schema.json" in rtd.ROLE_CONTRACTS["INTELLIGENCE_CONSUMER"]
assert "contracts/regulatory-decision/v1/domain.schema.json" in rtd.ROLE_CONTRACTS["REGULATIONS_AUTHORITY"]
assert "contracts/regulatory-decision/v1/regulations.openapi.yaml" in rtd.ROLE_CONTRACTS["REGULATIONS_AUTHORITY"]

canonical_regulations = {
    "regulations.evidence.assess",
    "regulations.requirement.resolve",
}
partial = {
    "providers": [
        {
            "provider_key": "baobab-regulations.core",
            "support": [
                {
                    "capability_key": "regulations.evidence.assess",
                    "implementation_status": "PARTIAL",
                    "implementation_evidence": [{"path": "scripts/rtd_conformance.py"}],
                }
            ],
        }
    ],
    "planned_capabilities": [],
}
assert not rtd.validate_regulations_provider_support(ROOT, partial, canonical_regulations)

implemented = copy.deepcopy(partial)
implemented["providers"][0]["support"][0]["implementation_status"] = "IMPLEMENTED"
assert any(
    "must remain PARTIAL during R-CAP-07" in finding
    for finding in rtd.validate_regulations_provider_support(
        ROOT, implemented, canonical_regulations
    )
)

missing_evidence = copy.deepcopy(partial)
missing_evidence["providers"][0]["support"][0]["implementation_evidence"] = []
assert any(
    "requires implementation evidence" in finding
    for finding in rtd.validate_regulations_provider_support(
        ROOT, missing_evidence, canonical_regulations
    )
)

noncanonical = copy.deepcopy(partial)
noncanonical["providers"][0]["support"][0]["capability_key"] = "regulations.fake.execute"
assert any(
    "not a canonical Shared capability" in finding
    for finding in rtd.validate_regulations_provider_support(
        ROOT, noncanonical, canonical_regulations
    )
)

duplicated = copy.deepcopy(partial)
duplicated["planned_capabilities"] = [
    {
        "capability_key": "regulations.evidence.assess",
        "proposal_status": "CONTRACTED",
    }
]
assert any(
    "both planned and provider support" in finding
    for finding in rtd.validate_regulations_provider_support(
        ROOT, duplicated, canonical_regulations
    )
)

canonical_intelligence = {
    "intelligence.evidence.search",
    "intelligence.research-mission.manage",
}
partial_pulse = {
    "providers": [
        {
            "provider_key": "baobab-pulse.core",
            "support": [
                {
                    "capability_key": "intelligence.evidence.search",
                    "implementation_status": "PARTIAL",
                    "implementation_evidence": [
                        {"path": "scripts/rtd_conformance.py"}
                    ],
                },
                {
                    "capability_key": "intelligence.research-mission.manage",
                    "implementation_status": "PARTIAL",
                    "implementation_evidence": [
                        {"path": "scripts/tests/test_rtd_conformance.py"}
                    ],
                },
            ],
        }
    ],
    "planned_capabilities": [],
}
assert not rtd.validate_pulse_provider_declaration(
    ROOT, partial_pulse, canonical_intelligence
)

implemented_pulse = copy.deepcopy(partial_pulse)
implemented_pulse["providers"][0]["support"][0]["implementation_status"] = "IMPLEMENTED"
assert any(
    "must remain PARTIAL during P-CAP-06" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, implemented_pulse, canonical_intelligence
    )
)

missing_pulse_evidence = copy.deepcopy(partial_pulse)
missing_pulse_evidence["providers"][0]["support"][0]["implementation_evidence"] = []
assert any(
    "requires implementation evidence" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, missing_pulse_evidence, canonical_intelligence
    )
)

uncensused_pulse = copy.deepcopy(partial_pulse)
uncensused_pulse["providers"][0]["support"][0]["capability_key"] = (
    "intelligence.fake.execute"
)
assert any(
    "cannot promote uncensused Intelligence capability" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT,
        uncensused_pulse,
        canonical_intelligence | {"intelligence.fake.execute"},
    )
)

incomplete_pulse = copy.deepcopy(partial_pulse)
incomplete_pulse["providers"][0]["support"] = incomplete_pulse["providers"][0][
    "support"
][:1]
assert any(
    "must cover exactly the two first-census capabilities" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, incomplete_pulse, canonical_intelligence
    )
)

duplicated_pulse = copy.deepcopy(partial_pulse)
duplicated_pulse["planned_capabilities"] = [
    {
        "capability_key": "intelligence.evidence.search",
        "proposal_status": "CONTRACTED",
    }
]
assert any(
    "both planned and provider support" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, duplicated_pulse, canonical_intelligence
    )
)

planned_pulse = {
    "planned_capabilities": [
        {
            "capability_key": "intelligence.evidence.search",
            "proposal_status": "CONTRACTED",
        },
        {
            "capability_key": "intelligence.research-mission.manage",
            "proposal_status": "CONTRACTED",
        },
    ]
}
assert not rtd.validate_pulse_provider_declaration(
    ROOT, planned_pulse, canonical_intelligence
)

noncanonical_pulse = copy.deepcopy(planned_pulse)
noncanonical_pulse["planned_capabilities"][0]["capability_key"] = "intelligence.fake.execute"
assert any(
    "not present in the Shared catalogue" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, noncanonical_pulse, canonical_intelligence
    )
)

print("RTD-10 conformance profile self-tests passed")
