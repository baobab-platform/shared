#!/usr/bin/env python3
"""Validate real registered workload scope syntax, never runtime admission.

The scope registry already contains hierarchical CMS names. This regression
checks the canonical request schema against those actual inputs, while proving
that namespace syntax cannot leak provider/credential fields or wildcard grants.
Issuer status/audience/credential enforcement remains a separate IAM obligation.
"""
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts/identity/v1/workload-token-request.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


def request(scopes):
    return {"workload_id": "nabhold-backend", "audience": "baobab-cms", "scopes": scopes}


class WorkloadTokenContracts(unittest.TestCase):
    def test_existing_cms_and_context_scopes_are_representable(self):
        for scope in ("content:entry:resolve", "content:entry:preview", "context:resolve", "verification:source-capture"):
            with self.subTest(scope=scope):
                self.assertEqual([], list(VALIDATOR.iter_errors(request([scope]))))

    def test_every_workload_environment_fits_the_canonical_identity(self):
        schema = json.loads((ROOT / "contracts/identity/v1/workload-identity.schema.json").read_text())
        allowed = schema["properties"]["environment"]["enum"]
        registry = yaml.safe_load((ROOT / "contracts/identity/v1/workload-registry.yaml").read_text())
        for client, entry in registry["workloads"].items():
            with self.subTest(client=client):
                self.assertIn(entry["environment"], allowed)

    def test_every_declared_workload_scope_fits_the_canonical_contract(self):
        registry = yaml.safe_load((ROOT / "contracts/identity/v1/workload-registry.yaml").read_text())
        scopes = {scope for workload in registry["workloads"].values() for scope in workload.get("allowed_scopes", [])}
        self.assertIn("content:entry:resolve", scopes)
        for scope in sorted(scopes):
            with self.subTest(scope=scope):
                self.assertEqual([], list(VALIDATOR.iter_errors(request([scope]))))

    def test_malformed_segments_and_wildcards_are_refused(self):
        for scope in ("content::entry", "content:entry:", ":content:entry", "content:*", "content:entry:*", "Content:entry:resolve", "content:entry_resolve", "content:entry:resolve other:grant", "content:entry:resolve\n", "context:resolve\n", "content:entry:resolve\r\n", "content:entry:1resolve", "openid"):
            with self.subTest(scope=scope):
                self.assertTrue(list(VALIDATOR.iter_errors(request([scope]))))

    def test_workload_and_audience_cannot_hide_a_final_line_terminator(self):
        for field in ("workload_id", "audience"):
            for suffix in ("\n", "\r", "\r\n"):
                payload = request(["content:entry:resolve"])
                payload[field] += suffix
                self.assertTrue(list(VALIDATOR.iter_errors(payload)))

    def test_closed_shape_scope_uniqueness_and_limits_are_preserved(self):
        for payload in (
            request(["content:entry:resolve", "content:entry:resolve"]),
            request(["a:b" + str(i) for i in range(33)]),
            request(["content:" + "a" * 60]),
            {**request(["content:entry:resolve"]), "credential": "fixture-only"},
            {**request(["content:entry:resolve"]), "grant_type": "client_credentials"},
            {**request(["content:entry:resolve"]), "realm": "provider-only"},
            {**request(["content:entry:resolve"]), "status": "ACTIVE"},
            {**request(["content:entry:resolve"]), "allowed_scopes": ["content:entry:preview"]},
        ):
            self.assertTrue(list(VALIDATOR.iter_errors(payload)))


if __name__ == "__main__":
    unittest.main()
