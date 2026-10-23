"""BFG-SED offline synthetic fixtures: deterministic, isolated and fail-closed."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "development" / "generate_bfg_sed.py"
spec = importlib.util.spec_from_file_location("generate_bfg_sed", SRC)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SyntheticFixtureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.blueprint = module.load_blueprint()

    def generate(self, scale: str = "small", seed: int = 100) -> dict:
        return module.generate(self.blueprint, scale=scale, seed=seed, run_id="a" * 32)

    def test_blueprint_has_all_requested_markets(self) -> None:
        keys = {e["key"] for e in self.blueprint["enterprises"]}
        self.assertEqual(keys, {"nabhold", "zuribeans", "thamani", "equator-estate", "external-client"})
        e = {x["key"]: x for x in self.blueprint["enterprises"]}
        self.assertEqual(e["nabhold"]["operating_markets"], ["ZA"])
        self.assertEqual(set(e["nabhold"]["footprint_markets"]), {"UG", "NG", "KE"})
        self.assertEqual(set(e["zuribeans"]["footprint_markets"]), {"KE", "ET", "TZ", "UG", "AO", "CO", "VN"})
        self.assertEqual(set(e["thamani"]["operating_markets"]),
                         {"ZA","EG","DE","GB","UG","KE","TZ","GH","MZ","AO","NG","ET","DJ","SZ"})
        self.assertEqual(set(e["equator-estate"]["operating_markets"]), {"UG", "ZA"})
        self.assertEqual(e["external-client"]["primary_market"], "UG")
        self.assertEqual(set(e["external-client"]["source_markets"]), {"CN", "IN"})
        self.assertIsNone(e["external-client"]["estate"])

    def test_profiles_never_make_market_presence_into_grant(self) -> None:
        data = self.generate()
        for e in data["organisations"]:
            self.assertFalse(e["incorporation_verified"])
            self.assertFalse(e["provider_activated"])
            self.assertFalse(e["commercially_authorised"])
            self.assertFalse(e["market_grants"])
            self.assertIsNone(e["canonical_tenant_id"])
            self.assertIsNone(e["canonical_organisation_id"])
            self.assertIsNone(e["canonical_legal_entity_id"])
        self.assertTrue(data["synthetic_only"])
        self.assertFalse(data["protected_acceptance"])
        self.assertFalse(data["can_import_directly_to_cp"])
        self.assertFalse(data["can_promote_to_staging_or_production"])

    def test_independent_third_party_is_not_group_member(self) -> None:
        data = self.generate()
        external = next(e for e in data["organisations"] if e["fixture_key"] == "external-client")
        self.assertIsNone(external["digital_estate_profile_key"])
        self.assertNotIn("ZA", external["operating_markets_scenario"])
        self.assertIn("UG", external["operating_markets_scenario"])
        other_refs = [x["fixture_tenant_ref"] for x in data["organisations"] if x != external]
        self.assertNotIn(external["fixture_tenant_ref"], other_refs)

    def test_reference_data_is_deterministic_and_seed_scoped(self) -> None:
        self.assertEqual(self.generate("medium", 123), self.generate("medium", 123))
        first, second = self.generate("medium", 123), self.generate("medium", 456)
        self.assertNotEqual(first["scenario_transactions"][0]["fixture_ref"],
                            second["scenario_transactions"][0]["fixture_ref"])
        self.assertEqual(first["counts"], second["counts"])

    def test_small_medium_large_scales_increase_load(self) -> None:
        counts = [self.generate(k)["counts"]["scenario_transactions"] for k in ("small", "medium", "large")]
        self.assertEqual(counts, [34, 170, 1360])
        self.assertTrue(all(x < y for x,y in zip(counts, counts[1:])))
        self.assertEqual(self.generate("large")["counts"]["documentary_evidence_inputs"], 1360)

    def test_personas_are_non_real_and_not_preapproved(self) -> None:
        d = self.generate("medium")
        self.assertTrue(d["personas"])
        for p in d["personas"]:
            self.assertTrue(p["email"].endswith("@example.invalid"))
            self.assertIsNone(p["iam_subject"])
            self.assertIsNone(p["cp_principal_id"])
            self.assertFalse(p["registered_grant"])
            self.assertTrue(p["fictional"])

    def test_pharmaceutical_records_never_claim_licence(self) -> None:
        d = self.generate("medium")
        cases = [r for r in d["scenario_transactions"] if r["source_scenario"].startswith("PH-")]
        self.assertGreater(len(cases), 0)
        for r in cases:
            self.assertFalse(r["runtime_qualification"])
            self.assertEqual(r["expected_engine_result"], "NOT_EXECUTED")
            self.assertFalse(r["money_moved"])
        for doc in d["documentary_evidence_inputs"]:
            self.assertIn(doc["verification_status"], {"MISSING", "UNVERIFIED"})
            self.assertIsNone(doc["nda_verification_certificate"])
            self.assertIsNone(doc["import_permit_id"])
            self.assertIsNone(doc["actual_document"])
        pharma_products = [x for x in d["catalogue_items"] if x["owner_enterprise_key"] == "external-client"]
        self.assertTrue(all(p["pharma_product_registered"] is False for p in pharma_products))

    def test_holding_company_does_not_receive_trading_products(self) -> None:
        d = self.generate()
        self.assertFalse([p for p in d["catalogue_items"] if p["owner_enterprise_key"] == "nabhold"])

    def test_markets_preserve_currency_locale_and_timezone(self) -> None:
        d = self.generate()
        markets = {m["code"]: m for m in d["declarative_market_catalogue"]}
        self.assertEqual(markets["SZ"]["name"], "Eswatini (formerly Swaziland)")
        self.assertEqual(markets["GB"]["currency"], "GBP")
        self.assertEqual(markets["DE"]["currency"], "EUR")
        self.assertEqual(markets["UG"]["currency"], "UGX")
        self.assertEqual(markets["CN"]["currency"], "CNY")
        self.assertEqual(markets["IN"]["currency"], "INR")
        self.assertEqual(len(markets), 18)
        self.assertTrue(all(t["fx_quote"] is None for t in d["scenario_transactions"]))

    def test_rejects_unsafe_mutations(self) -> None:
        for key,value in (("synthetic_only",False),("protected_acceptance",True),
                          ("source_of_canonical_ids","EXTERNAL"),("lease_max_seconds", 86401)):
            b = copy.deepcopy(self.blueprint)
            b[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                module.validate_blueprint(b)
        b = copy.deepcopy(self.blueprint)
        b["enterprises"][4]["estate"] = {"key":"pharma"}
        with self.assertRaises(ValueError):
            module.validate_blueprint(b)
        b = copy.deepcopy(self.blueprint)
        b["enterprises"][0]["business_model"] = "B2B_TRADE"
        with self.assertRaises(ValueError):
            module.validate_blueprint(b)

    def test_reject_invalid_run_id(self) -> None:
        with self.assertRaises(ValueError):
            module.generate(self.blueprint, scale="small", seed=1, run_id="not-a-run-id")

    def test_cli_blocks_protected_environment(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "should_not_exist.json"
            env = os.environ.copy()
            env["BAOBAB_ENVIRONMENT"] = "production"
            p = subprocess.run(
                [sys.executable, str(SRC), "--scale", "small", "--output", str(out)],
                capture_output=True, text=True, env=env, check=False,
            )
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("prohibited", p.stderr)

    def test_cli_output_counts_and_json_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "fixture.json"
            env = os.environ.copy()
            env["BAOBAB_ENVIRONMENT"] = "development"
            p = subprocess.run(
                [sys.executable, str(SRC), "--scale", "medium", "--seed", "345",
                 "--run-id", "3"*32, "--output", str(out)],
                capture_output=True, text=True, env=env, check=True,
            )
            d = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(d["counts"]["scenario_transactions"], 170)
            self.assertTrue(d["synthetic_only"])
            self.assertIn("170 cases", p.stdout)


if __name__ == "__main__":
    unittest.main()
