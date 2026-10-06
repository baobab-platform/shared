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

print("RTD-10 conformance profile self-tests passed")
