#!/usr/bin/env python3
"""ADR-ERP-024 / ADR-SHARED-017 WMS DRAFT canonical conformance, not admission."""
from __future__ import annotations
import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "contracts/wms/v1"
EXPECTED = (
    "inventory.custody.read",
    "inventory.warehouse-operation.manage",
)
SCHEMAS = (
    "custody-read-request.schema.json",
    "custody-read-response.schema.json",
    "warehouse-operation-manage-request.schema.json",
    "warehouse-operation-manage-response.schema.json",
)

def check():
    definitions = yaml.safe_load((PACKAGE / "capabilities.yaml").read_text())["capabilities"]
    assert [x["capability_key"] for x in definitions] == list(EXPECTED)
    catalogue = yaml.safe_load((ROOT / "contracts/capability/v1/catalogue.yaml").read_text())["capabilities"]
    selected = [x for x in catalogue if x["capability_key"] in EXPECTED]
    assert [x["capability_key"] for x in selected] == list(EXPECTED), "WMS canonical catalogue drift"
    for x in selected:
        assert x["owner"] == "baobab-erp"
        assert x["source"] == "../../wms/v1/capabilities.yaml"
    for entry in definitions:
        assert (entry["owner"], entry["lifecycle"], entry["maturity"], entry["data_classification"]) == ("baobab-erp", "DRAFT", "EXPERIMENTAL", "RESTRICTED")
        assert len(entry["contracts"]) == 1 and entry["contracts"][0]["major"] == 1
    for name in SCHEMAS:
        schema = json.loads((PACKAGE / name).read_text())
        assert schema["$id"] == f"https://contracts.baobab-platform.com/wms/v1/{name}"
        Draft202012Validator.check_schema(schema)
        props = schema["properties"]
        for forbidden in ("tenant_id", "legal_entity_id", "ad_client_id", "ad_org_id", "provider_id"):
            assert forbidden not in props, f"{name} trusts caller-provided authority"
        assert schema["additionalProperties"] is False
    operation = json.loads((PACKAGE / SCHEMAS[2]).read_text())
    validator = Draft202012Validator(operation, format_checker=FormatChecker())
    good = dict(operation_ref="obs-1", warehouse_ref="warehouse-1", inventory_owner_ref="owner-1",
                operation="RECEIPT_OBSERVED", sku_ref="sku-1", quantity="10.500", uom="KG",
                observed_at="2026-11-10T10:00:00Z", evidence_ref="evidence-1")
    validator.validate(good)
    for mutation in (dict(good, tenant_id="forged"), dict(good, ad_client_id=11),
                     dict(good, quantity=-10), dict(good, quantity=10.5),
                     dict(good, operation="POST_GL"), dict(good, evidence_ref=None)):
        assert not validator.is_valid(mutation), f"dangerous operation accepted: {mutation}"
    lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())["contracts"]
    selected_lock = [x for x in lock if x["domain"] == "wms" and x["version"] == "v1"]
    assert len(selected_lock) == 1 and set(selected_lock[0]["schemas"]) == set(SCHEMAS) | {"capabilities.yaml"}
    return 4

if __name__ == "__main__":
    print(f"WMS DRAFT source qualification PASS: {check()} schemas; no provider/CP runtime enabled")
