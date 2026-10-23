"""Executable development boundaries; no runtime or protected approval claims."""
import copy
import json
from pathlib import Path
import unittest

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts/development/v1/enterprise-profiles.schema.json").read_text())
PROFILES = json.loads((ROOT / "contracts/development/v1/examples/nabhold-group.json").read_text())


def validate(document):
    jsonschema.Draft202012Validator(SCHEMA).validate(document)
    keys = [p["key"] for p in document["profiles"]]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate enterprise profile")
    for profile in document["profiles"]:
        required, optional = set(profile["required_engines"]), set(profile["optional_engines"])
        if required & optional or not {"baobab-cp", "baobab-iam"} <= required:
            raise ValueError("ambiguous engine dependencies")
        if profile["estate"] and "baobab-cms" not in required:
            raise ValueError("estate requires CMS")
        if profile["key"] == "nabhold" and {"baobab-trade", "baobab-tms", "baobab-scf"} & (required | optional):
            raise ValueError("holding company must remain non-trading")


class DevelopmentProfiles(unittest.TestCase):
    def test_complete_group_and_no_estate_external_client(self):
        validate(PROFILES)
        self.assertEqual(len(PROFILES["profiles"]), 5)
        self.assertIsNone(PROFILES["profiles"][-1]["estate"])

    def test_refuses_protected_environment_or_real_data_or_unbounded_lease(self):
        for field, value in (("environment", "staging"), ("environment", "production"),
                             ("synthetic_only", False), ("max_lease_seconds", 86401)):
            document = copy.deepcopy(PROFILES)
            document[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(jsonschema.ValidationError):
                validate(document)

    def test_refuses_duplicate_profiles_and_wrong_business_or_estate(self):
        document = copy.deepcopy(PROFILES)
        document["profiles"][1] = document["profiles"][0]
        with self.assertRaises((ValueError, jsonschema.ValidationError)):
            validate(document)
        for index, field, value in ((0, "business_model", "B2B_TRADE"),
                                    (2, "business_model", "B2C"),
                                    (4, "estate", PROFILES["profiles"][0]["estate"])):
            document = copy.deepcopy(PROFILES)
            document["profiles"][index][field] = value
            with self.subTest(index=index, field=field), self.assertRaises(jsonschema.ValidationError):
                validate(document)

    def test_refuses_trading_holding_company_and_duplicate_engine_selection(self):
        for engine in ("baobab-trade", "baobab-tms", "baobab-cp"):
            document = copy.deepcopy(PROFILES)
            document["profiles"][0]["optional_engines"].append(engine)
            with self.subTest(engine=engine), self.assertRaises((ValueError, jsonschema.ValidationError)):
                validate(document)

    def test_each_estate_has_separate_bounded_development_caller(self):
        rows = yaml.safe_load((ROOT / "contracts/identity/v1/workload-registry.yaml").read_text())["workloads"]
        clients = []
        for profile in PROFILES["profiles"]:
            if not profile["estate"]:
                continue
            client = profile["estate"]["cms_client_id"]
            clients.append(client)
            row = rows[client]
            self.assertEqual(row["environment"], "development")
            self.assertEqual(row["status"], "ACTIVE")
            self.assertEqual(row["allowed_audiences"], ["baobab-control-plane", "baobab-cms"])
            self.assertEqual(row["allowed_scopes"], ["context:resolve", "content:entry:resolve"])
        self.assertEqual(len(clients), len(set(clients)))
        self.assertEqual(rows["nabhold-backend"]["status"], "PROVISIONED")
        self.assertEqual(rows["nabhold-backend"]["environment"], "production")
        self.assertEqual(rows["baobab-cms-workload"]["environment"], "production")


if __name__ == "__main__":
    unittest.main()
