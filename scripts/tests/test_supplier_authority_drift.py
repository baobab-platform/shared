#!/usr/bin/env python3
"""ADR-SHARED-006/010: supplier authority and message-contract consistency."""
from __future__ import annotations
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
SUPPLIER = ROOT / "contracts/supplier-onboarding/v1"
ERP = ROOT / "contracts/erp/v1/system-of-record.yaml"
PACKAGE_GUIDE = ROOT / "packages/supplier-domain/README.md"

class SupplierAuthorityDrift(unittest.TestCase):
    def test_current_organisation_and_supplier_owners(self):
        erp = yaml.safe_load(ERP.read_text())
        concepts = {c["concept"]: c for c in erp["concepts"]}
        self.assertEqual("control-plane", concepts["Organisation"]["canonical_owner"])
        self.assertEqual("erp", concepts["Supplier"]["canonical_owner"])
        supplier = yaml.safe_load((SUPPLIER / "system-of-record.yaml").read_text())
        for concept in supplier["concepts"]:
            self.assertEqual("hosting-estate", concept["canonical_owner"])
        descriptive = str(supplier).lower()
        self.assertNotIn("organisation concept remains canonical_owner unassigned", descriptive)
        self.assertNotIn("organisation concept is assigned an owner", descriptive)
        self.assertIn("cp-attested", descriptive)

    def test_all_six_messages_are_registered_and_versioned(self):
        doc = yaml.safe_load((SUPPLIER / "asyncapi.yaml").read_text())
        messages = doc["components"]["messages"]
        self.assertEqual({
            "SupplierApplicationSubmitted", "SupplierApplicationDecided",
            "SupplierQualificationUpdated", "SupplierCapabilityVerified",
            "SupplierKybEvidenceRecorded", "SupplierKybDecisionRecorded",
        }, set(messages))
        exposed = doc["channels"]["supplierOnboardingEvents"]["messages"]
        self.assertEqual(set(messages), {v["$ref"].split("/")[-1] for v in exposed.values()})
        for key, message in messages.items():
            with self.subTest(key=key):
                self.assertTrue(message["name"].startswith("com.baobab-platform.supplier-onboarding."))
                self.assertTrue(message["name"].endswith(".v1"))
                refs = message["payload"]["allOf"]
                self.assertEqual("../../events/v1/envelope.schema.json", refs[0]["$ref"])
                payload_ref = refs[1]["properties"]["data"]["$ref"]
                self.assertTrue((SUPPLIER / payload_ref).is_file(), payload_ref)

    def test_docs_do_not_claim_absent_organisation_or_transport(self):
        for path in (SUPPLIER / "README.md", SUPPLIER / "asyncapi.yaml", PACKAGE_GUIDE):
            with self.subTest(path=path.name):
                content = path.read_text().lower()
                self.assertNotIn("no message broker exists yet", content)
                self.assertNotIn("no broker exists", content)
                self.assertNotIn("canonical_owner explicitly", content)
                self.assertNotIn("does not yet have a canonical organisation", content)
        guide = PACKAGE_GUIDE.read_text()
        self.assertIn("not KYB", guide)
        self.assertIn("domain-owned service", guide)
        self.assertIn("ADR-SHARED-007", guide)

    def test_kyb_is_not_inferred_from_metadata(self):
        supplier = yaml.safe_load((SUPPLIER / "system-of-record.yaml").read_text())
        concepts = {c["concept"]: c for c in supplier["concepts"]}
        self.assertIn("declared evidence is not verification", concepts["Supplier KYB Evidence"]["consistency"])
        self.assertIn("verified is required before approval", concepts["Supplier KYB Decision"]["consistency"])

if __name__ == "__main__":
    unittest.main()
