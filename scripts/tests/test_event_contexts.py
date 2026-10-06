#!/usr/bin/env python3
"""Tests for scripts/event_contexts.py (ADR-SHARED-018 SS3.5).

Each test mutates a copy of the real registries and checks the one rule it
targets.

  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/tests/test_event_contexts.py
"""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import event_contexts as ec  # noqa: E402

CONTEXTS = ec.load_yaml(ec.EVENTS / "context-registry.yaml")
EVENTS = ec.load_yaml(ec.EVENTS / "event-registry.yaml")
DOMAINS = {d["key"] for d in ec.load_yaml(ec.CONTRACTS / "capability" / "v1" / "namespace-registry.yaml")["domains"]}
MESSAGES = ec.asyncapi_messages(ec.CONTRACTS)
PAYMENT = "com.baobab-platform.payments.payment.created.v1"


class RegistryTest(unittest.TestCase):
    def run_validate(self, contexts=None, events=None, messages=None) -> list[str]:
        return ec.validate(contexts or contexts_copy(), events or events_copy(), DOMAINS,
                           MESSAGES if messages is None else messages)

    def assertFails(self, failures: list[str], fragment: str):
        self.assertTrue(any(fragment in f for f in failures), f"expected {fragment!r} in {failures}")


def contexts_copy():
    return copy.deepcopy(CONTEXTS)


def events_copy():
    return copy.deepcopy(EVENTS)


def context(doc, key):
    return next(c for c in doc["contexts"] if c["key"] == key)


def event(doc, event_type):
    return next(e for e in doc["events"] if e["type"] == event_type)


class ShippedRegistriesTest(RegistryTest):
    def test_shipped_registries_pass(self):
        self.assertEqual(self.run_validate(), [])

    def test_regulations_is_active_and_erp_deprecated(self):
        self.assertEqual(context(CONTEXTS, "regulations")["status"], "ACTIVE")
        self.assertEqual(context(CONTEXTS, "regulations")["stewards"], ["baobab-regulations"])
        self.assertEqual(context(CONTEXTS, "regulations")["capability_domains"], ["regulations"])
        self.assertEqual(context(CONTEXTS, "erp")["status"], "DEPRECATED")
        self.assertEqual(context(CONTEXTS, "payments")["capability_domains"], ["payment"])


class ContextRulesTest(RegistryTest):
    def test_unsorted_contexts_fail(self):
        doc = contexts_copy()
        doc["contexts"].reverse()
        self.assertFails(self.run_validate(contexts=doc), "not sorted")

    def test_engine_named_active_context_fails(self):
        doc = contexts_copy()
        doc["contexts"].append({"key": "zz-medusa", "status": "ACTIVE", "stewards": [], "description": "vendor-named context"})
        self.assertFails(self.run_validate(contexts=doc), "names ['medusa']")

    def test_unregistered_capability_domain_fails(self):
        doc = contexts_copy()
        context(doc, "commerce")["capability_domains"] = ["not-a-domain"]
        self.assertFails(self.run_validate(contexts=doc), "not-a-domain is not registered")

    def test_deprecated_context_needs_frozen_types(self):
        doc = contexts_copy()
        del context(doc, "erp")["frozen_types"]
        self.assertFails(self.run_validate(contexts=doc), "frozen_types")

    def test_new_type_in_deprecated_context_fails(self):
        doc = contexts_copy()
        context(doc, "erp")["frozen_types"].remove("com.baobab-platform.erp.warehouse.changed.v1")
        self.assertFails(self.run_validate(contexts=doc), "accepts no new types")

    def test_reserved_context_carries_no_types(self):
        doc = contexts_copy()
        context(doc, "payments")["status"] = "RESERVED"
        self.assertFails(self.run_validate(contexts=doc), "is RESERVED")


class EventRulesTest(RegistryTest):
    def test_registry_and_asyncapi_correspond(self):
        doc = events_copy()
        doc["events"] = [e for e in doc["events"] if e["type"] != PAYMENT]
        self.assertFails(self.run_validate(events=doc), "is not in event-registry.yaml")
        messages = dict(MESSAGES)
        del messages[PAYMENT]
        self.assertFails(self.run_validate(messages=messages), "defined by no AsyncAPI document")

    def test_wrong_asyncapi_document_fails(self):
        doc = events_copy()
        event(doc, PAYMENT)["asyncapi"] = "contracts/erp/v1/asyncapi.yaml"
        self.assertFails(self.run_validate(events=doc), "defined in contracts/payments/v1/asyncapi.yaml")

    def test_active_type_needs_producer(self):
        doc = events_copy()
        del event(doc, PAYMENT)["producer"]
        self.assertFails(self.run_validate(events=doc), "producer")

    def test_producer_must_steward_the_context(self):
        doc = events_copy()
        event(doc, PAYMENT)["producer"] = "baobab-trade"
        self.assertFails(self.run_validate(events=doc), "not a steward of context payments")

    def test_proposed_type_has_no_producer(self):
        doc = events_copy()
        proposed = next(e for e in doc["events"] if e["lifecycle"] == "PROPOSED")
        proposed["producer"] = "baobab-cp"
        self.assertFails(self.run_validate(events=doc), "PROPOSED type has no producer yet")

    def test_engine_token_needs_naming_exception(self):
        doc = events_copy()
        del event(doc, "com.baobab-platform.customer.buyer-erp-projection.requested.v1")["naming_exception"]
        self.assertFails(self.run_validate(events=doc), "names ['erp'] without a naming_exception")

    def test_unregistered_context_fails(self):
        messages = dict(MESSAGES)
        messages["com.baobab-platform.nowhere.thing.created.v1"] = "contracts/payments/v1/asyncapi.yaml"
        doc = events_copy()
        doc["events"].append({"type": "com.baobab-platform.nowhere.thing.created.v1",
                              "asyncapi": "contracts/payments/v1/asyncapi.yaml", "lifecycle": "PROPOSED"})
        doc["events"].sort(key=lambda e: e["type"])
        self.assertFails(self.run_validate(events=doc, messages=messages), "context nowhere is not registered")

    def test_legacy_type_superseded_once(self):
        doc = events_copy()
        legacy = "com.nabhold.commerce.payment.initiated.v1"
        event(doc, PAYMENT)["supersedes"] = [legacy]
        event(doc, "com.baobab-platform.payments.payment.failed.v1")["supersedes"] = [legacy]
        self.assertFails(self.run_validate(events=doc), "superseded by both")

    def test_legacy_type_only_inside_supersedes(self):
        doc = events_copy()
        event(doc, PAYMENT)["supersedes"] = ["com.nabhold.commerce.payment.initiated.v1"]
        text = "com.nabhold.commerce.payment.initiated.v1\n# stray com.nabhold.commerce.tax.determined.v1\n"
        failures = ec.validate(contexts_copy(), doc, DOMAINS, MESSAGES, text)
        self.assertFails(failures, "outside a `supersedes` list")
        self.assertEqual(ec.validate(contexts_copy(), doc, DOMAINS, MESSAGES,
                                     "com.nabhold.commerce.payment.initiated.v1\n"), [])

    def test_supersedes_accepts_only_legacy_types(self):
        doc = events_copy()
        event(doc, PAYMENT)["supersedes"] = ["com.baobab-platform.payments.payment.failed.v1"]
        self.assertFails(self.run_validate(events=doc), "supersedes")


if __name__ == "__main__":
    unittest.main(verbosity=1)
