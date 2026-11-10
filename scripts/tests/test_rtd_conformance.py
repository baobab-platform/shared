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
assert "contracts/authorization/v1/scope-registry.yaml" in rtd.ROLE_CONTRACTS["INTELLIGENCE_CONSUMER"]
assert "contracts/identity/v1/workload-registry.yaml" in rtd.ROLE_CONTRACTS["INTELLIGENCE_CONSUMER"]
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
implemented_pulse = {
    "providers": [
        {
            "provider_key": "baobab-pulse.core",
            "simulated": False,
            "production_permitted": True,
            "invocation": {
                "service_reference": "service://baobab-pulse/api",
                "protocol": "http",
            },
            "support": [
                {
                    "capability_key": "intelligence.evidence.search",
                    "implementation_status": "IMPLEMENTED",
                    "implementation_evidence": [
                        {"type": "source", "path": "scripts/rtd_conformance.py"},
                        {
                            "type": "contract-test",
                            "path": "scripts/tests/test_rtd_conformance.py",
                        },
                        {
                            "type": "integration-test",
                            "path": "scripts/tests/test_rtd_conformance.py",
                        },
                    ],
                },
                {
                    "capability_key": "intelligence.research-mission.manage",
                    "implementation_status": "IMPLEMENTED",
                    "implementation_evidence": [
                        {"type": "source", "path": "scripts/rtd_conformance.py"},
                        {
                            "type": "contract-test",
                            "path": "scripts/tests/test_rtd_conformance.py",
                        },
                        {
                            "type": "integration-test",
                            "path": "scripts/tests/test_rtd_conformance.py",
                        },
                    ],
                },
            ],
        }
    ],
    "planned_capabilities": [],
}
assert not rtd.validate_pulse_provider_declaration(
    ROOT, implemented_pulse, canonical_intelligence
)

partial_pulse = copy.deepcopy(implemented_pulse)
partial_pulse["providers"][0]["support"][0]["implementation_status"] = "PARTIAL"
assert any(
    "must be IMPLEMENTED for P-CAP-07" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, partial_pulse, canonical_intelligence
    )
)

missing_pulse_evidence = copy.deepcopy(implemented_pulse)
missing_pulse_evidence["providers"][0]["support"][0]["implementation_evidence"] = []
assert any(
    "requires implementation evidence" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, missing_pulse_evidence, canonical_intelligence
    )
)

weak_pulse_evidence = copy.deepcopy(implemented_pulse)
weak_pulse_evidence["providers"][0]["support"][0]["implementation_evidence"] = [
    {"type": "source", "path": "scripts/rtd_conformance.py"}
]
assert any(
    "readiness evidence is missing" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, weak_pulse_evidence, canonical_intelligence
    )
)

uncensused_pulse = copy.deepcopy(implemented_pulse)
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

incomplete_pulse = copy.deepcopy(implemented_pulse)
incomplete_pulse["providers"][0]["support"] = incomplete_pulse["providers"][0][
    "support"
][:1]
assert any(
    "must cover exactly the two first-census capabilities" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, incomplete_pulse, canonical_intelligence
    )
)

nonproduction_pulse = copy.deepcopy(implemented_pulse)
nonproduction_pulse["providers"][0]["production_permitted"] = False
assert any(
    "must be production_permitted" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, nonproduction_pulse, canonical_intelligence
    )
)

missing_invocation = copy.deepcopy(implemented_pulse)
missing_invocation["providers"][0].pop("invocation")
assert any(
    "requires logical invocation metadata" in finding
    for finding in rtd.validate_pulse_provider_declaration(
        ROOT, missing_invocation, canonical_intelligence
    )
)

duplicated_pulse = copy.deepcopy(implemented_pulse)
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


# ADR-SHARED-017/026: a candidate-only file must not be read as a provider.
# Exercise the actual Shared catalogue/schema validator and RTD-10 denial gate.
import tempfile

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / ".baobab").mkdir()
    candidate_file = root / ".baobab/capability-provider.yaml"
    candidate = {
        "schema": {"name": "baobab-capability-provider-declaration", "version": "1.0"},
        "engine": {"engine_id": "baobab-trade-docs"},
        "planned_capabilities": [{
            "proposed_key": "documents.trade-document.manage",
            "proposal_status": "CANDIDATE",
            "provenance": {"authority": {
                "repository": "baobab-platform/baobab-trade-docs",
                "decision": "ADR-TDOC-0002",
            }},
        }],
    }
    assert not rtd.validate_trade_docs_candidate_declaration(root, ROOT)
    candidate_file.write_text(yaml.safe_dump(candidate, sort_keys=False))
    assert not rtd.validate_trade_docs_candidate_declaration(root, ROOT), (
        "CANDIDATE intent is not provider support"
    )

    with_provider = copy.deepcopy(candidate)
    with_provider["providers"] = [{
        "provider_key": "baobab-trade-docs.fake",
        "provider_type": "BAOBAB_ENGINE",
        "simulated": False,
        "production_permitted": False,
        "support": [{
            "capability_key": "documents.trade-document.manage",
            "contract_versions": [1],
            "implementation_status": "PARTIAL",
        }],
    }]
    candidate_file.write_text(yaml.safe_dump(with_provider, sort_keys=False))
    assert any(
        "must not claim a real capability provider" in failure
        for failure in rtd.validate_trade_docs_candidate_declaration(root, ROOT)
    ), "Architecture-only must deny even PARTIAL provider support"

    empty = copy.deepcopy(candidate)
    empty["planned_capabilities"] = []
    candidate_file.write_text(yaml.safe_dump(empty, sort_keys=False))
    assert any(
        "nonempty planned_capabilities" in failure
        for failure in rtd.validate_trade_docs_candidate_declaration(root, ROOT)
    )

    wrong_engine = copy.deepcopy(candidate)
    wrong_engine["engine"]["engine_id"] = "baobab-regulations"
    candidate_file.write_text(yaml.safe_dump(wrong_engine, sort_keys=False))
    assert any(
        "engine.engine_id" in failure
        for failure in rtd.validate_trade_docs_candidate_declaration(root, ROOT)
    )

    forged = copy.deepcopy(candidate)
    forged["status"] = "ACTIVE"
    candidate_file.write_text(yaml.safe_dump(forged, sort_keys=False))
    assert rtd.validate_trade_docs_candidate_declaration(root, ROOT), (
        "Candidates cannot publish runtime authority fields"
    )

    uncensused = copy.deepcopy(candidate)
    uncensused["planned_capabilities"][0] = {
        "capability_key": "documents.trade-document.manage",
        "proposal_status": "CONTRACTED",
    }
    candidate_file.write_text(yaml.safe_dump(uncensused, sort_keys=False))
    assert any(
        "not a canonical Shared capability" in failure
        for failure in rtd.validate_trade_docs_candidate_declaration(root, ROOT)
    ), "CONTRACTED must not invent an unregistered capability"
