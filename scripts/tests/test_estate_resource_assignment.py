#!/usr/bin/env python3
"""Governed estate resource assignment (ADR-SHARED-042 section 14, Decision 9).

Static boundary plus a reference model of the governed lifecycle: a
non-BFF native commitment's Digital Estate is proven only by an ACTIVE,
four-eyes approved CP assignment of an authenticated workload or an attested
Trade native configuration, attested for at most 60 seconds. A Medusa key,
sales channel or asserted estate is never provenance, and nothing is
allocated or activated.
"""
import copy
from datetime import datetime, timedelta
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
ID = "https://contracts.baobab-platform.com/control-plane/v1/estate-resource-assignment.schema.json"
PROFILE_ID = "https://contracts.baobab-platform.com/control-plane/v1/estate-commerce-profile.schema.json"
SCHEMA = json.loads((CONTRACTS / "control-plane/v1/estate-resource-assignment.schema.json").read_text())
API = yaml.safe_load((CONTRACTS / "control-plane/v1/estate-resource-assignment.openapi.yaml").read_text())
SCOPES = {s["name"]: s for s in yaml.safe_load((CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]}
WORKLOADS = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())
EXAMPLES = CONTRACTS / "control-plane/v1/examples"
ASSIGNMENT = json.loads((EXAMPLES / "estate-resource-assignment-native.json").read_text())
ATTESTATION = json.loads((EXAMPLES / "estate-resource-assignment-attestation.json").read_text())
RESOLVE = json.loads((EXAMPLES / "estate-resource-assignment-resolve-workload.json").read_text())
ADR = (ROOT / "docs/adr/ADR-SHARED-042 — Canonical Commercial Actor Authority and Buyer Execution Context.md").read_text()
RESOLVE_PATH = "/internal/estate/v1/resource-assignments/resolve"
NEW_SCOPES = ("estate:resource-assignment:resolve", "estate:resource-assignment:write",
              "estate:resource-assignment:approve", "trade:native-commitment:submit")


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


REGISTRY = registry()


def errors(definition, document, schema_id=ID):
    validator = Draft202012Validator({"$ref": f"{schema_id}#/$defs/{definition}"}, registry=REGISTRY,
                                     format_checker=FormatChecker())
    return list(validator.iter_errors(document))


def changed(document, **change):
    result = copy.deepcopy(document)
    for key, value in change.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = value
    return result


def at(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def transition(assignment, action, *, actor, expected_revision):
    """Reference model of the governed lifecycle. Returns the new record or a refusal code."""
    if expected_revision != assignment["revision"]:
        return "REVISION_CONFLICT"
    status = assignment["status"]
    if status == "REVOKED":
        return "ASSIGNMENT_TERMINAL"
    allowed = {"APPROVE": {"PROPOSED"}, "REINSTATE": {"SUSPENDED"}, "SUSPEND": {"ACTIVE"},
               "REVOKE": {"PROPOSED", "ACTIVE", "SUSPENDED"}}
    if status not in allowed[action]:
        return "INVALID_TRANSITION"
    if action in ("APPROVE", "REINSTATE") and actor == assignment["proposed_by"]:
        return "SELF_APPROVAL"
    after = {"APPROVE": "ACTIVE", "REINSTATE": "ACTIVE", "SUSPEND": "SUSPENDED", "REVOKE": "REVOKED"}[action]
    result = changed(assignment, status=after, revision=assignment["revision"] + 1)
    if action == "APPROVE":
        result.update(approved_by=actor, approval_reference="approval:synthetic-next")
    return result


PROPOSED = changed(ASSIGNMENT, status="PROPOSED", revision=1, approved_by=None, approval_reference=None)
PROPOSER = ASSIGNMENT["proposed_by"]
APPROVER = ASSIGNMENT["approved_by"]


class EstateResourceAssignment(unittest.TestCase):
    def test_examples_are_valid_and_consistent(self):
        self.assertEqual([], errors("EstateResourceAssignment", ASSIGNMENT))
        self.assertEqual([], errors("EstateResourceAssignment", PROPOSED))
        self.assertEqual([], errors("EstateResourceAssignmentAttestation", ATTESTATION))
        self.assertEqual([], errors("EstateResourceAssignmentResolveRequest", RESOLVE))
        for key in ("assignment_id", "digital_estate_id", "tenant_id", "trade_engine_instance_id", "scope"):
            self.assertEqual(ATTESTATION[key], ASSIGNMENT[key])
        self.assertEqual(ATTESTATION["assignment_revision"], ASSIGNMENT["revision"])
        self.assertIn(ATTESTATION["market_id"], ASSIGNMENT["market_scope"])
        self.assertIn(ATTESTATION["operation"], ASSIGNMENT["permitted_operations"])

    def test_attestation_is_short_lived_provenance_for_the_commerce_profile(self):
        issued, expires = at(ATTESTATION["issued_at"]), at(ATTESTATION["expires_at"])
        self.assertTrue(issued < expires <= issued + timedelta(seconds=60))
        for key in SCHEMA["$defs"]["EstateResourceAssignmentAttestation"]["required"]:
            with self.subTest(missing=key):
                self.assertNotEqual([], errors("EstateResourceAssignmentAttestation", changed(ATTESTATION, **{key: None})))
        for change in ({"commerce_model": "B2B"}, {"status": "ACTIVE"}, {"operation": "trade.cart.modify"},
                       {"workload_client_id": "synthetic-server"}):  # a NATIVE_RESOURCE attestation names no workload
            with self.subTest(change=change):
                self.assertNotEqual([], errors("EstateResourceAssignmentAttestation", changed(ATTESTATION, **change)))
        # Its id is exactly the GOVERNED_RESOURCE_ASSIGNMENT provenance resolveEstateCommerceProfile accepts.
        request = {"digital_estate_id": ATTESTATION["digital_estate_id"], "engine_instance_id": ATTESTATION["trade_engine_instance_id"],
                   "market_id": ATTESTATION["market_id"], "correlation_id": RESOLVE["correlation_id"],
                   "estate_provenance": {"kind": "GOVERNED_RESOURCE_ASSIGNMENT", "reference": ATTESTATION["attestation_id"]}}
        self.assertEqual([], errors("EstateCommerceProfileResolveRequest", request, PROFILE_ID))

    def test_scope_names_exactly_one_subject(self):
        workload = changed(ASSIGNMENT, scope="WORKLOAD", native_resource=None, workload_client_id="synthetic-server-checkout")
        self.assertEqual([], errors("EstateResourceAssignment", workload))
        for document in (changed(ASSIGNMENT, native_resource=None),
                         changed(ASSIGNMENT, workload_client_id="synthetic-server-checkout"),
                         changed(workload, workload_client_id=None),
                         changed(ASSIGNMENT, scope="SALES_CHANNEL"),
                         changed(ASSIGNMENT, native_resource={"native_configuration_reference": "x", "native_configuration_digest": "abc"})):
            with self.subTest(scope=document.get("scope")):
                self.assertNotEqual([], errors("EstateResourceAssignment", document))
        native = changed(RESOLVE, scope="NATIVE_RESOURCE", workload_evidence=None, workload_evidence_type=None,
                         native_resource=ASSIGNMENT["native_resource"])
        self.assertEqual([], errors("EstateResourceAssignmentResolveRequest", native))
        for document in (changed(RESOLVE, workload_evidence=None), changed(RESOLVE, native_resource=ASSIGNMENT["native_resource"]),
                         changed(native, native_resource=None), changed(native, workload_evidence=RESOLVE["workload_evidence"])):
            with self.subTest(request=document["scope"]):
                self.assertNotEqual([], errors("EstateResourceAssignmentResolveRequest", document))

    def test_the_caller_cannot_assert_the_estate_authority(self):
        for extra in ({"tenant_id": "tn_other01"}, {"assignment_id": ASSIGNMENT["assignment_id"]}, {"revision": 9},
                      {"publishable_key": "pk_synthetic"}, {"sales_channel_id": "sc_synthetic"}, {"commerce_model": "B2C"}):
            with self.subTest(extra=extra):
                self.assertNotEqual([], errors("EstateResourceAssignmentResolveRequest", {**RESOLVE, **extra}))
        for change in ({"operation": "trade.cart.modify"}, {"workload_evidence_type": "medusa-secret-key"},
                       {"workload_evidence": "short"}):
            with self.subTest(change=change):
                self.assertNotEqual([], errors("EstateResourceAssignmentResolveRequest", changed(RESOLVE, **change)))
        self.assertNotIn("tenant_id", SCHEMA["$defs"]["EstateResourceAssignmentProposal"]["properties"])
        self.assertNotIn("proposed_by", SCHEMA["$defs"]["EstateResourceAssignmentProposal"]["properties"])

    def test_record_is_governed(self):
        for change in ({"status": "PENDING"}, {"revision": 0}, {"market_scope": []}, {"permitted_operations": []},
                       {"permitted_operations": ["trade.cart.modify"]}, {"proposed_by": None}, {"approved_by": None},
                       {"tenant_id": "tenant-1"}):
            with self.subTest(change=change):
                self.assertNotEqual([], errors("EstateResourceAssignment", changed(ASSIGNMENT, **change)))

    def test_lifecycle_is_four_eyes_revisioned_and_terminal(self):
        self.assertEqual("SELF_APPROVAL", transition(PROPOSED, "APPROVE", actor=PROPOSER, expected_revision=1))
        self.assertEqual("REVISION_CONFLICT", transition(PROPOSED, "APPROVE", actor=APPROVER, expected_revision=2))
        active = transition(PROPOSED, "APPROVE", actor=APPROVER, expected_revision=1)
        self.assertEqual(("ACTIVE", 2, APPROVER), (active["status"], active["revision"], active["approved_by"]))
        self.assertEqual([], errors("EstateResourceAssignment", active))
        suspended = transition(active, "SUSPEND", actor=PROPOSER, expected_revision=2)
        self.assertEqual(("SUSPENDED", 3), (suspended["status"], suspended["revision"]))
        self.assertEqual("SELF_APPROVAL", transition(suspended, "REINSTATE", actor=PROPOSER, expected_revision=3))
        reinstated = transition(suspended, "REINSTATE", actor=APPROVER, expected_revision=3)
        self.assertEqual("ACTIVE", reinstated["status"])
        revoked = transition(reinstated, "REVOKE", actor=PROPOSER, expected_revision=4)
        for action in ("APPROVE", "REINSTATE", "SUSPEND", "REVOKE"):
            with self.subTest(after_revoke=action):
                self.assertEqual("ASSIGNMENT_TERMINAL", transition(revoked, action, actor=APPROVER, expected_revision=5))
        self.assertEqual("INVALID_TRANSITION", transition(active, "APPROVE", actor=APPROVER, expected_revision=2))
        actions = SCHEMA["$defs"]["EstateResourceAssignmentTransition"]["properties"]["action"]["enum"]
        self.assertEqual({"APPROVE", "SUSPEND", "REINSTATE", "REVOKE"}, set(actions))

    def test_denials_are_closed_and_mapped(self):
        codes = set(SCHEMA["$defs"]["EstateResourceAssignmentDenialCode"]["enum"])
        responses = API["paths"][RESOLVE_PATH]["post"]["responses"]
        self.assertLessEqual({"200", "400", "401", "403", "404", "409", "503"}, set(responses))
        self.assertIn("ASSIGNMENT_AMBIGUOUS", responses["409"]["description"])
        self.assertIn("ASSIGNMENT_NOT_FOUND", responses["404"]["description"])
        for code in codes - {"ASSIGNMENT_AMBIGUOUS", "ASSIGNMENT_NOT_FOUND", "RESOLUTION_UNAVAILABLE"}:
            with self.subTest(code=code):
                self.assertIn(code, responses["403"]["description"])

    def test_operations_are_scoped_and_unallocated(self):
        api = API["paths"]
        self.assertEqual([{"EstateAssignmentWorkload": ["estate:resource-assignment:resolve"]}],
                         api[RESOLVE_PATH]["post"]["security"])
        self.assertEqual([{"adminOidc": ["estate:resource-assignment:write"]}],
                         api["/v1/estate/resource-assignments"]["post"]["security"])
        for name in NEW_SCOPES:
            with self.subTest(scope=name):
                self.assertIn(name, SCOPES)
        self.assertEqual((["workload"], False), (SCOPES["estate:resource-assignment:resolve"]["allowed_actors"],
                                                 SCOPES["estate:resource-assignment:resolve"]["grants_authority"]))
        self.assertEqual(["baobab-trade"], SCOPES["trade:native-commitment:submit"]["audience"])
        for name in ("estate:resource-assignment:write", "estate:resource-assignment:approve"):
            self.assertEqual((["human"], True), (SCOPES[name]["allowed_actors"], SCOPES[name]["privileged"]))
        for client_id, entry in WORKLOADS["workloads"].items():
            for name in NEW_SCOPES:
                with self.subTest(workload=client_id, scope=name):
                    self.assertNotIn(name, entry.get("allowed_scopes", []))

    def test_decision_is_recorded_with_the_thamani_reconciliation(self):
        self.assertIn("Decision 9: governed estate resource assignment and the universal native commit fence", ADR)
        self.assertIn("ADR-THA-0018", ADR)
        self.assertIn("inactive enforcement gate", ADR)
        self.assertIn("Amended by Decision 9 (5)", ADR)


if __name__ == "__main__":
    unittest.main()
