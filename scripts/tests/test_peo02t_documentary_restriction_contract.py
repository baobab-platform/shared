"""PEO-02T canonical negative-only CP restriction conformance tests."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from documentary_restriction_binding import (
    RestrictionDecisionRejected, verify_current_restriction_pair,
)

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "contracts/admission/v2/documentary-restriction.schema.json"
SCHEMA = json.loads(PATH.read_text())
DEFS = SCHEMA["$defs"]
CTX = "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6b"
ORG = "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6c"
NOW = datetime(2026, 10, 11, tzinfo=timezone.utc)


def request():
    return {
        "context_id": CTX,
        "capability": "accounting.customer-invoice.post",
        "market": "ZA",
        "operation_reference": "synthetic/invoice/post-123",
    }


def response():
    return {
        **request(),
        "organisation_id": ORG,
        "blocked": True,
        "authority_granted": False,
        "policy_reference": "ADR-BCP-026/PEO-02T:negative-only",
        "evaluated_at": NOW.isoformat(),
        "expires_at": (NOW + timedelta(seconds=1)).isoformat(),
    }


class ContractTests(unittest.TestCase):
    def test_schema_version_and_exact_valid_boundaries(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.assertEqual(
            SCHEMA["$id"],
            "https://contracts.baobab-platform.com/admission/v2/documentary-restriction.schema.json",
        )
        for definition, example in (
            ("DocumentaryRestrictionAssessmentRequest", request()),
            ("DocumentaryRestrictionAssessmentResponse", response()),
        ):
            with self.subTest(definition=definition):
                Draft202012Validator(DEFS[definition], format_checker=FormatChecker()).validate(example)

    def test_temporal_and_original_request_pair_must_match(self):
        self.assertTrue(verify_current_restriction_pair(
            request(), response(), organisation_id=ORG,
            now=NOW + timedelta(milliseconds=500),
        ))
        self.assertFalse(verify_current_restriction_pair(
            request(), {**response(), "blocked": False}, organisation_id=ORG,
            now=NOW + timedelta(milliseconds=500),
        ))
        wrong = [
            {"context_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a99"},
            {"capability": "payments.capture"},
            {"market": "UG"},
            {"operation_reference": "synthetic/different-operation"},
            {"organisation_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a99"},
            {"blocked": "false"},
            {"authority_granted": True},
            {"evaluated_at": (NOW - timedelta(seconds=5)).isoformat()},
            {"evaluated_at": (NOW + timedelta(seconds=3)).isoformat()},
            {"expires_at": (NOW - timedelta(seconds=1)).isoformat()},
            {"expires_at": (NOW + timedelta(minutes=10)).isoformat()},
            {"evaluated_at": (NOW + timedelta(seconds=1)).isoformat(),
             "expires_at": (NOW + timedelta(milliseconds=700)).isoformat()},
        ]
        for mutation in wrong:
            with self.subTest(mutation=mutation):
                with self.assertRaises(RestrictionDecisionRejected):
                    verify_current_restriction_pair(
                        request(), {**response(), **mutation},
                        organisation_id=ORG, now=NOW + timedelta(milliseconds=500),
                    )

    def test_applicant_cannot_select_authority_in_request(self):
        validator = Draft202012Validator(
            DEFS["DocumentaryRestrictionAssessmentRequest"], format_checker=FormatChecker(),
        )
        for forbidden in ("organisation_id", "tenant_id", "legal_entity_id", "mandate_id",
                          "provider_id", "authority_granted", "blocked"):
            with self.subTest(field=forbidden):
                self.assertFalse(validator.is_valid({**request(), forbidden: "forged"}))
        self.assertFalse(validator.is_valid({**request(), "context_id": "not-uuid"}))
        self.assertFalse(validator.is_valid({**request(), "market": "Za"}))

    def test_response_cannot_grant_positive_provider_authority(self):
        validator = Draft202012Validator(
            DEFS["DocumentaryRestrictionAssessmentResponse"], format_checker=FormatChecker(),
        )
        self.assertTrue(validator.is_valid({**response(), "blocked": False}))
        for bad in (
            {"authority_granted": True},
            {"authority_granted": "false"},
            {"policy_reference": "applicant/claimed"},
            {"organisation_id": "not-uuid"},
            {"expires_at": ""},
            {"legal_actor_resolution": {"outcome": "AUTHORIZED"}},
        ):
            with self.subTest(bad=bad):
                self.assertFalse(validator.is_valid({**response(), **bad}))


if __name__ == "__main__":
    unittest.main()
