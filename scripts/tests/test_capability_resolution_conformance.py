"""Validate the portable capability resolution wire corpus against Shared."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from capability_catalogue import Contracts


class CapabilityResolutionConformanceTests(unittest.TestCase):
    def test_response_corpus(self):
        contracts = Contracts(ROOT / "contracts")
        corpus = json.loads(
            (contracts.root / "capability/v1/resolution-conformance.json").read_text()
        )
        self.assertEqual(corpus["schema_ref"], "capability/v1/resolution.schema.json#/$defs/resolution")
        self.assertEqual({case["valid"] for case in corpus["cases"]}, {False, True})
        for case in corpus["cases"]:
            with self.subTest(case=case["id"]):
                errors = contracts.errors(corpus["schema_ref"], case["response"])
                self.assertEqual(not errors, case["valid"], errors)


if __name__ == "__main__":
    unittest.main()
