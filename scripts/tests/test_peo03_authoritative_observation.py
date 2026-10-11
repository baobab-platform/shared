"""PEO-03A: authoritative observations are not verification decisions."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "contracts/evidence/v1"
SCHEMA = json.loads((DOCS / "authoritative-observation.schema.json").read_text())
SOURCE_REGISTRY = yaml.safe_load((DOCS / "source-registry.yaml").read_text())
SOURCES = {s["source_id"]: s for s in SOURCE_REGISTRY["sources"]}
REG = Registry()
for file in DOCS.glob("*.schema.json"):
    doc = json.loads(file.read_text())
    REG = REG.with_resource(doc["$id"], Resource.from_contents(doc))


def check(name: str, obj: dict) -> list[str]:
    validator = Draft202012Validator(
        {"$ref": SCHEMA["$id"] + "#/$defs/" + name},
        registry=REG, format_checker=FormatChecker(),
    )
    return [error.message for error in validator.iter_errors(obj)]


def request():
    return {
        "verification_case_id": "vcase_synthetic01",
        "claim_id": "ecl_synthetic01",
        "source_id": "esrc_cipc",
        "claim_type": "LEGAL_NAME",
        "jurisdiction": "ZA",
        "purpose": "ORGANISATION_ADMISSION",
        "subject": {"subject_type": "ORGANISATION",
                    "subject_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6b"},
        "correlation_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6c",
    }


def observation():
    data = request()
    del data["correlation_id"]
    return {
        **data, "observation_id": "aobs_synthetic01",
        "method": "SOURCE_API_LOOKUP", "outcome": "MATCHED",
        "source_observed_at": "2026-10-11T07:30:00Z",
        "recorded_at": "2026-10-11T07:30:01Z",
        "freshness_until": "2026-10-12T07:30:00Z",
        "source_record_reference": "synthetic/cipc/case-001",
        "response_digest": "sha256:" + "a" * 64,
        "provenance_reference": "test-artifact/synthetic-cipc-001",
        "provider_adapter_id": "baobab.cipc.synthetic",
        "evidence_reference": "evr_synthetic01",
        "is_synthetic": True,
    }


class AuthoritativeObservationContractTests(unittest.TestCase):
    def test_schema_and_adapters_have_no_grant_field(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.assertFalse(check("SourceVerificationRequest", request()))
        self.assertFalse(check("SourceObservation", observation()))
        for illegal in ["authority_granted", "verification_result_id", "tenant_active",
                        "tax_pin", "raw_document", "access_token", "source_approved"]:
            with self.subTest(field=illegal):
                self.assertTrue(check("SourceObservation", {**observation(), illegal: True}))

    def test_assisted_tcs_is_recorded_as_witness_not_api(self):
        obs = {
            **observation(), "source_id": "esrc_sarstcs",
            "claim_type": "TAX_COMPLIANCE_STATUS",
            "method": "MANUAL_REGISTRY_LOOKUP",
            "provider_adapter_id": "not-authorised",
        }
        del obs["provider_adapter_id"]
        self.assertTrue(check("SourceObservation", obs))
        obs["witness_principal_id"] = "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6d"
        obs["witnessed_at"] = obs["source_observed_at"]
        self.assertFalse(check("SourceObservation", obs))
        self.assertEqual(SOURCES["esrc_sarstcs"]["status"], "SUSPENDED")

    def test_sars_vat_tcs_are_not_interchangeable(self):
        self.assertEqual(SOURCES["esrc_sarsvat"]["status"], "SUSPENDED")
        tcs = SOURCES["esrc_sarstcs"]["trusted_for"]
        vat = SOURCES["esrc_sarsvat"]["trusted_for"]
        self.assertEqual(tcs, [{"claim_type": "TAX_COMPLIANCE_STATUS", "jurisdiction": "ZA"}])
        self.assertEqual(vat, [{"claim_type": "VAT_REGISTRATION", "jurisdiction": "ZA"}])
        self.assertNotIn("TAX_COMPLIANCE_STATUS",
                         [x["claim_type"] for x in SOURCES["esrc_cipc"]["trusted_for"]])

    def test_canonical_witness_ids_and_subdivision_jurisdictions(self):
        assisted = {
            **observation(), "method": "MANUAL_REGISTRY_LOOKUP",
            "jurisdiction": "ZA-GP", "witness_principal_id": "prn_kato",
            "witnessed_at": "2026-10-11T07:30:00Z",
        }
        assisted.pop("provider_adapter_id")
        self.assertFalse(check("SourceObservation", assisted))
        self.assertFalse(check("SourceVerificationRequest", {
            **request(), "jurisdiction": "ZA-GP",
        }))

    def test_matched_evidence_id_must_resolve_canonical_identifier(self):
        for bad in ["", "https://untrusted.example/file", "evr_"]:
            with self.subTest(bad=bad):
                self.assertTrue(check("SourceObservation", {
                    **observation(), "evidence_reference": bad,
                }))

    def test_positive_observation_needs_provenance_and_freshness(self):
        for key in ("response_digest", "provenance_reference", "freshness_until",
                    "source_record_reference", "evidence_reference"):
            with self.subTest(key=key):
                obj = observation()
                del obj[key]
                self.assertTrue(check("SourceObservation", obj))
        obj = observation()
        obj["response_digest"] = "sha256:not-a-hash"
        self.assertTrue(check("SourceObservation", obj))


if __name__ == "__main__":
    unittest.main()
