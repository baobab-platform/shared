#!/usr/bin/env python3
"""Tests for scripts/capability_catalogue.py (ADR-SHARED-017, EA-02).

Catalogue tests mutate a copy of contracts/; declaration tests build an
engine repository in a temporary directory and validate it against the real
Shared catalogue.

  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/tests/test_capability_catalogue.py
"""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import capability_catalogue as cc  # noqa: E402

SHARED = cc.Contracts()

# Mirrors the placeholder shape of engine-template/.baobab/capability-provider.yaml.example.
TEMPLATE = """
schema:
  name: baobab-capability-provider-declaration
  version: "1.0"
engine:
  engine_id: <engine-id>
providers:
  - provider_key: <engine-id>.<provider-name>
    name: <provider-display-name>
    provider_type: BAOBAB_ENGINE
    implementation_key: <implementation-key>
    simulated: false
    production_permitted: false
    invocation:
      service_reference: service://<engine-id>/<service-name>
      protocol: http
    support:
      - capability_key: <canonical-capability-key>
        contract_versions:
          - <contract-major>
        implementation_status: IMPLEMENTED
        provenance:
          authority:
            repository: <owning-repository>
            decision: <governing-adr>
        implementation_evidence:
          - type: source
            path: <evidence-path>
planned_capabilities:
  - proposed_key: <proposed-capability-key>
    proposal_status: CANDIDATE
    provenance:
      authority:
        repository: <owning-repository>
"""


def declaration(**overrides) -> dict:
    document = {
        "schema": {"name": "baobab-capability-provider-declaration", "version": "1.0"},
        "engine": {"engine_id": "baobab-payments"},
        "providers": [{
            "provider_key": "baobab-payments.sandbox",
            "name": "Sandbox payment provider",
            "provider_type": "BAOBAB_ENGINE",
            "implementation_key": "sandbox",
            "simulated": True,
            "production_permitted": False,
            "invocation": {"service_reference": "service://baobab-payments/payments", "protocol": "http"},
            "support": [
                {"capability_key": "payment.intent.create", "contract_versions": [1], "implementation_status": "IMPLEMENTED",
                 "provenance": {"authority": {"repository": "baobab-platform/baobab-payments", "decision": "ADR-PAY-0002"}},
                 "implementation_evidence": [{"type": "source", "path": "src/service.rs"},
                                             {"type": "test", "path": "tests/payment_capture.rs"}]},
                {"capability_key": "payment.payment.capture", "contract_versions": [1], "implementation_status": "PARTIAL"},
            ],
        }],
        "planned_capabilities": [{"proposed_key": "payment.payout.execute", "proposal_status": "CANDIDATE",
                                  "provenance": {"authority": {"repository": "baobab-platform/baobab-payments",
                                                               "decision": "ADR-PAY-0021"}}}],
    }
    document.update(overrides)
    return document


def provider(document: dict, index: int = 0) -> dict:
    return document["providers"][index]


class CatalogueTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "contracts"
        shutil.copytree(cc.CONTRACTS, self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def edit_yaml(self, rel: str, change) -> None:
        path = self.root / rel
        document = yaml.safe_load(path.read_text())
        change(document)
        path.write_text(yaml.safe_dump(document, sort_keys=False))

    def failures(self) -> list[str]:
        return cc.validate_shared(cc.Contracts(self.root))

    def assertFails(self, fragment: str):
        failures = self.failures()
        self.assertTrue(any(fragment in f for f in failures), f"expected a failure containing {fragment!r}, got {failures}")

    def test_valid_catalogue(self):
        self.assertEqual(self.failures(), [])

    def test_catalogue_indexes_payments_subscriptions_and_trade(self):
        owners = {d["owner"] for d, _ in cc.Contracts(self.root).definitions().values()}
        self.assertEqual(owners, {"baobab-payments", "baobab-subscriptions", "baobab-trade"})

    def test_duplicate_catalogue_entry_rejected(self):
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"].insert(0, copy.deepcopy(c["capabilities"][0])))
        self.assertFails("more than once")

    def test_unsorted_catalogue_rejected(self):
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"].reverse())
        self.assertFails("sorted by capability_key")

    def test_duplicate_definition_rejected(self):
        def duplicate(document):
            document["capabilities"].append(copy.deepcopy(yaml.safe_load(
                (self.root / "payments/v1/capabilities.yaml").read_text())["capabilities"][0]))
        self.edit_yaml("subscriptions/v1/capabilities.yaml", duplicate)
        self.assertFails("payment.intent.create is defined more than once")

    def test_unknown_domain_rejected(self):
        def rename(document):
            document["capabilities"][0].update(capability_key="regulations.rule.query", domain="regulations")
        self.edit_yaml("trade/v1/capabilities.yaml", rename)
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"].__setitem__(
            2, {"capability_key": "regulations.rule.query", "owner": "baobab-trade", "source": "../../trade/v1/capabilities.yaml"}))
        self.assertFails("regulations")

    def test_domain_enum_and_namespace_registry_must_agree(self):
        self.edit_yaml("capability/v1/namespace-registry.yaml", lambda r: r["domains"].pop())
        self.assertFails("must declare identical domains")

    def test_missing_source_rejected(self):
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"][0].update(source="../../subscriptions/v1/missing.yaml"))
        self.assertFails("does not exist")

    def test_entry_not_defined_in_its_source_rejected(self):
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"][0].update(source="../../trade/v1/capabilities.yaml"))
        self.assertFails("does not resolve")

    def test_owner_mismatch_rejected(self):
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"][0].update(owner="baobab-trade"))
        self.assertFails("differs from its definition's owner")

    def test_invalid_owner_rejected(self):
        self.edit_yaml("trade/v1/capabilities.yaml", lambda d: d["capabilities"][0].update(owner="medusa"))
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"][2].update(owner="medusa"))
        self.assertFails("is not a Baobab engine/service repository")

    def test_unindexed_definition_in_indexed_source_detected(self):
        self.edit_yaml(cc.CATALOGUE, lambda c: c["capabilities"].pop())
        self.assertFails("payment.refund.create is defined in")

    def test_unindexed_definition_document_detected_whatever_its_name(self):
        document = {"schema": {"name": "baobab-capability-definitions", "version": "1.0"},
                    "capabilities": [yaml.safe_load((self.root / "trade/v1/capabilities.yaml").read_text())["capabilities"][0]
                                     | {"capability_key": "commerce.order.create"}]}
        (self.root / "trade/v1/more-definitions.json").write_text(json.dumps(document))
        failures = self.failures()
        self.assertTrue(any("is not a catalogue source" in f for f in failures), failures)
        self.assertTrue(any("commerce.order.create is defined" in f and "not indexed" in f for f in failures), failures)

    def test_ad_hoc_capability_manifest_shape_rejected(self):
        (self.root / "trade/v1/extra.yaml").write_text("version: 1\ncapabilities:\n  - capability_key: commerce.order.create\n")
        self.assertFails("unrecognised manifest shape")

    def test_missing_request_schema_rejected(self):
        self.edit_yaml("trade/v1/capabilities.yaml",
                       lambda d: d["capabilities"][0]["contracts"][0].update(request_schema="missing.schema.json"))
        self.assertFails("request_schema 'missing.schema.json' does not resolve")

    def test_missing_response_schema_rejected(self):
        self.edit_yaml("trade/v1/capabilities.yaml",
                       lambda d: d["capabilities"][0]["contracts"][0].update(response_schema="quick-order.schema.json#/$defs/nope"))
        self.assertFails("response_schema")

    def test_missing_error_schema_rejected(self):
        self.edit_yaml("trade/v1/capabilities.yaml",
                       lambda d: d["capabilities"][0]["contracts"][0].update(error_schema="../../errors/v1/nope.schema.json"))
        self.assertFails("error_schema")

    def test_missing_event_schema_rejected(self):
        self.edit_yaml("payments/v1/capabilities.yaml",
                       lambda d: d["capabilities"][0]["contracts"][0]["event_schemas"].append("events.schema.json#/$defs/Nope"))
        self.assertFails("event_schema")

    def test_unknown_dependency_rejected(self):
        self.edit_yaml("trade/v1/capabilities.yaml", lambda d: d["capabilities"][0].update(
            dependencies=[{"capability_key": "commerce.order.create", "dependency_type": "REQUIRED"}]))
        self.assertFails("which is not catalogued")

    def test_required_dependency_cycle_rejected(self):
        def cycle(document):
            document["capabilities"][1]["dependencies"] = [{"capability_key": "commercial.quotation.manage", "dependency_type": "REQUIRED"}]
            document["capabilities"][2]["dependencies"] = [{"capability_key": "commercial.rfq.manage", "dependency_type": "REQUIRED"}]
        self.edit_yaml("trade/v1/capabilities.yaml", cycle)
        self.assertFails("form a cycle")

    def test_optional_dependency_cycle_allowed(self):
        def cycle(document):
            document["capabilities"][1]["dependencies"] = [{"capability_key": "commercial.quotation.manage", "dependency_type": "OPTIONAL"}]
            document["capabilities"][2]["dependencies"] = [{"capability_key": "commercial.rfq.manage", "dependency_type": "REQUIRED"}]
        self.edit_yaml("trade/v1/capabilities.yaml", cycle)
        self.assertEqual(self.failures(), [])

    def test_vendor_tenant_and_region_identity_rejected(self):
        for key, expected in (("commerce.medusa-cart.manage", "vendor/provider"), ("commerce.zuribeans-cart.manage", "tenant"),
                              ("commerce.kenya-cart.manage", "country/region")):
            with self.subTest(key=key):
                self.assertTrue(any(expected in e for e in cc.key_identity_errors(key)))
        self.assertEqual(cc.key_identity_errors("identity.authentication.perform"), [])

    def test_unindexed_registration_bundle_detected(self):
        shutil.copy(self.root / "payments/v1/capabilities.json", self.root / "payments/v1/registration.json")
        self.assertFails("not listed in capability/v1/registration-bundles.yaml")

    def test_bundle_drift_from_canonical_definition_detected(self):
        path = self.root / "payments/v1/capabilities.json"
        bundle = json.loads(path.read_text())
        bundle["capabilities"][0]["maturity"] = "SUPPORTED"
        path.write_text(json.dumps(bundle))
        self.assertFails("differs from its canonical definition")

    def test_bundle_supporting_uncatalogued_capability_detected(self):
        path = self.root / "subscriptions/v1/capabilities.json"
        bundle = json.loads(path.read_text())
        bundle["support"].append({"capability_key": "billing.credit.apply", "contract_versions": [1]})
        path.write_text(json.dumps(bundle))
        self.assertFails("billing.credit.apply, which is not in the canonical catalogue")


class DeclarationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        for rel in ("src/service.rs", "tests/payment_capture.rs"):
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text("// evidence\n")

    def tearDown(self):
        self.tmp.cleanup()

    def failures(self, document: dict, engine_id: str | None = "baobab-payments") -> list[str]:
        return cc.validate_declaration(SHARED, document, self.repo, engine_id)

    def assertFails(self, document: dict, fragment: str, **kwargs):
        failures = self.failures(document, **kwargs)
        self.assertTrue(any(fragment in f for f in failures), f"expected a failure containing {fragment!r}, got {failures}")

    def test_valid_declaration(self):
        self.assertEqual(self.failures(declaration()), [])

    def test_shipped_example_is_valid(self):
        example = yaml.safe_load((cc.CONTRACTS / cc.DECLARATION_EXAMPLE).read_text())
        self.assertEqual(cc.validate_declaration(SHARED, example), [])

    def test_multiple_providers_per_engine_and_capabilities_per_provider(self):
        document = declaration()
        second = copy.deepcopy(provider(document))
        second.update(provider_key="baobab-payments.hyperswitch", implementation_key="hyperswitch", simulated=False,
                      production_permitted=True)
        document["providers"].append(second)
        self.assertEqual(self.failures(document), [])

    def test_same_capability_on_two_providers_supports_migration(self):
        document = declaration(engine={"engine_id": "baobab-iam"}, planned_capabilities=[])
        keycloak = provider(document)
        keycloak.update(provider_key="baobab-iam.keycloak", implementation_key="keycloak", simulated=False,
                        invocation={"service_reference": "service://baobab-iam/identity", "protocol": "http"})
        ory = copy.deepcopy(keycloak)
        ory.update(provider_key="baobab-iam.ory", implementation_key="ory")
        document["providers"].append(ory)
        self.assertEqual(self.failures(document, engine_id="baobab-iam"), [])

    def test_invalid_engine_identity_rejected(self):
        self.assertFails(declaration(engine={"engine_id": "Baobab_Payments"}), "engine_id")

    def test_engine_identity_must_match_repository(self):
        self.assertFails(declaration(), "not this repository's engine id", engine_id="baobab-trade")

    def test_invalid_provider_identity_rejected(self):
        document = declaration()
        provider(document)["provider_key"] = "sandbox"
        self.assertFails(document, "provider_key")

    def test_provider_of_another_engine_rejected(self):
        document = declaration()
        provider(document)["provider_key"] = "baobab-trade.sandbox"
        self.assertFails(document, "does not belong to engine baobab-payments")

    def test_duplicate_provider_rejected(self):
        document = declaration()
        document["providers"].append(copy.deepcopy(provider(document)))
        self.assertFails(document, "declared more than once")

    def test_known_capability_support_accepted_unknown_rejected(self):
        document = declaration()
        provider(document)["support"][0]["capability_key"] = "payment.payout.execute"
        self.assertFails(document, "not a canonical Shared capability")

    def test_unknown_contract_major_rejected(self):
        document = declaration()
        provider(document)["support"][0]["contract_versions"] = [1, 2]
        self.assertFails(document, "has no contract major [2]")

    def test_duplicate_provider_support_rejected(self):
        document = declaration()
        provider(document)["support"].append(copy.deepcopy(provider(document)["support"][0]))
        self.assertFails(document, "more than once")

    def test_simulated_provider_cannot_be_production_permitted(self):
        document = declaration()
        provider(document)["production_permitted"] = True
        self.assertFails(document, "production_permitted")

    def test_production_permission_must_be_explicit(self):
        document = declaration()
        del provider(document)["production_permitted"]
        self.assertFails(document, "production_permitted")

    def test_implementation_status_is_not_lifecycle_certification_or_health(self):
        for status in ("ACTIVE", "CERTIFIED", "HEALTHY", "SCAFFOLDED", "implemented"):
            with self.subTest(status=status):
                document = declaration()
                provider(document)["support"][0]["implementation_status"] = status
                self.assertFails(document, "implementation_status")

    def test_implemented_support_requires_evidence(self):
        document = declaration()
        del provider(document)["support"][0]["implementation_evidence"]
        self.assertFails(document, "implementation_evidence")

    def test_declaration_cannot_self_certify_or_carry_runtime_state(self):
        for field, value in (("certified", True), ("lifecycle", "ACTIVE"), ("health", "HEALTHY"), ("bindings", []),
                             ("grants", []), ("engine_instances", [])):
            with self.subTest(field=field):
                document = declaration()
                provider(document)[field] = value
                self.assertFails(document, f"/{field} is not a provider declaration's to state")
        document = declaration()
        provider(document)["support"][0]["certified"] = True
        self.assertFails(document, "certified is not a provider declaration's to state")

    def test_logical_service_uri_accepted(self):
        self.assertEqual(self.failures(declaration()), [])

    def test_invalid_invocation_rejected(self):
        for reference in ("https://payments.internal:8443/", "service://payments.svc.cluster.local/x",
                          "service://user:secret@baobab-payments/payments", "10.0.0.4:8080"):
            with self.subTest(reference=reference):
                document = declaration()
                provider(document)["invocation"]["service_reference"] = reference
                self.assertFails(document, "service_reference")
        document = declaration()
        provider(document)["invocation"] = {"service_reference": "service://baobab-payments/payments", "protocol": "amqp"}
        self.assertFails(document, "protocol")

    def test_invocation_must_name_own_engine(self):
        document = declaration()
        provider(document)["invocation"]["service_reference"] = "service://baobab-trade/orders"
        self.assertFails(document, "must name engine baobab-payments")

    def test_evidence_path_must_exist(self):
        document = declaration()
        provider(document)["support"][0]["implementation_evidence"][0]["path"] = "src/missing.rs"
        self.assertFails(document, "does not exist in the repository")

    def test_evidence_path_must_be_repository_relative(self):
        for path in ("/etc/passwd", "../outside.rs", "src/../../outside.rs", "https://example.com/x", "./src/service.rs",
                     "src/./service.rs", "src//service.rs", "C:/src/service.rs"):
            with self.subTest(path=path):
                document = declaration()
                provider(document)["support"][0]["implementation_evidence"][0]["path"] = path
                self.assertFails(document, "path")

    def test_hidden_directory_evidence_accepted(self):
        document = declaration()
        provider(document)["support"][0]["implementation_evidence"][0]["path"] = ".github/workflows/contract-tests.yml"
        self.assertEqual(cc.validate_declaration(SHARED, document), [])

    def test_evidence_paths_not_checked_without_repository(self):
        self.assertEqual(cc.validate_declaration(SHARED, declaration()), [])

    def test_planned_capability_must_not_already_be_canonical(self):
        document = declaration()
        document["planned_capabilities"][0]["proposed_key"] = "payment.refund.create"
        self.assertFails(document, "is already canonical")

    def test_planned_capability_may_use_unregistered_namespace(self):
        document = declaration(engine={"engine_id": "baobab-regulations"}, providers=[], planned_capabilities=[
            {"proposed_key": "regulations.assessment.evaluate", "proposal_status": "PROPOSED",
             "provenance": {"authority": {"repository": "baobab-platform/baobab-regulations", "decision": "ADR-REG-0002"}}}])
        self.assertEqual(self.failures(document, engine_id="baobab-regulations"), [])

    def test_planned_only_declaration_needs_something_to_declare(self):
        self.assertFails(declaration(providers=[], planned_capabilities=[]), "schema")

    def test_contracted_plan_references_canonical_key_only(self):
        document = declaration()
        document["planned_capabilities"] = [{"capability_key": "payment.refund.create", "proposal_status": "CONTRACTED"}]
        self.assertEqual(self.failures(document), [])
        document["planned_capabilities"] = [{"proposed_key": "payment.refund.create", "proposal_status": "CONTRACTED"}]
        self.assertFails(document, "schema")
        document["planned_capabilities"] = [{"capability_key": "payment.payout.execute", "proposal_status": "CANDIDATE"}]
        self.assertFails(document, "schema")

    def test_planned_capability_cannot_also_be_supported(self):
        document = declaration()
        document["planned_capabilities"] = [{"capability_key": "payment.intent.create", "proposal_status": "CONTRACTED"}]
        self.assertFails(document, "both planned and supported")

    def test_planned_capability_never_becomes_runtime_support(self):
        document = declaration()
        document["planned_capabilities"].append({"capability_key": "payment.refund.create", "proposal_status": "CONTRACTED"})
        registration = cc.generate_registration(SHARED, document, "baobab-payments.sandbox")
        registered = {s["capability_key"] for s in registration["support"]}
        self.assertEqual(registered, {"payment.intent.create"})
        self.assertNotIn("payment.payout.execute", json.dumps(registration))
        self.assertNotIn("payment.refund.create", registered)

    def test_partial_support_is_never_registered(self):
        registration = cc.generate_registration(SHARED, declaration(), "baobab-payments.sandbox")
        self.assertNotIn("payment.payment.capture", {s["capability_key"] for s in registration["support"]})

    def test_generated_registration_defaults_to_draft(self):
        registration = cc.generate_registration(SHARED, declaration(), "baobab-payments.sandbox")
        self.assertEqual(registration["provider"]["lifecycle"], "DRAFT")
        self.assertEqual(SHARED.errors(cc.REGISTRATION_REF, registration), [])

    def test_example_regenerates_the_committed_payments_bundle(self):
        example = yaml.safe_load((cc.CONTRACTS / cc.DECLARATION_EXAMPLE).read_text())
        generated = cc.generate_registration(SHARED, example, "baobab-payments.sandbox", "ACTIVE")
        committed = json.loads((cc.CONTRACTS / "payments/v1/capabilities.json").read_text())
        self.assertEqual({k: v for k, v in generated["provider"].items() if k != "engine_key"},
                         {k: v for k, v in committed["provider"].items() if k != "engine_key"})
        self.assertEqual(generated["capabilities"], committed["capabilities"])
        self.assertEqual(generated["support"], committed["support"])

    def test_engine_template_placeholders_substitute_to_a_valid_declaration(self):
        text = cc.substitute_template(TEMPLATE, SHARED)
        self.assertEqual(cc.PLACEHOLDER.findall(text), [])
        self.assertEqual(cc.validate_declaration(SHARED, yaml.safe_load(text), engine_id="baobab-example"), [])

    def test_cli_reports_unknown_template_placeholders(self):
        path = self.repo / "capability-provider.yaml"
        path.write_text(TEMPLATE.replace("<service-name>", "<unknown-placeholder>"))
        self.assertEqual(cc.main(["validate-declaration", str(path), "--template"]), 1)
        path.write_text(TEMPLATE)
        self.assertEqual(cc.main(["validate-declaration", str(path), "--template", "--engine-id", "baobab-example"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
