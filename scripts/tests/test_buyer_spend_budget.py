#!/usr/bin/env python3
"""Buyer spend budget and reservation ledger (trade/v2, ADR-SHARED-042 section 14, Decision 5).

Static boundary plus a reference model of the rules JSON Schema cannot
express: calendar-month periods in a governing time zone, available capacity,
reservation-to-commitment conversion without double counting, and release of
only the unused portion. Trade's implementation must agree with this model; a
schema-valid entry is never authority by itself.
"""
import copy
from datetime import datetime, timedelta
import json
from pathlib import Path
import unittest
from zoneinfo import ZoneInfo

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
SCHEMA_ID = "https://contracts.baobab-platform.com/trade/v2/buyer-spend-budget.schema.json"
EXAMPLES = CONTRACTS / "trade/v2/examples"
POLICY = json.loads((EXAMPLES / "buyer-spend-budget-membership-monthly.json").read_text())
RESERVE = json.loads((EXAMPLES / "buyer-spend-ledger-reserve.json").read_text())
CAPACITY = json.loads((EXAMPLES / "buyer-spend-budget-capacity.json").read_text())


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


REGISTRY = registry()


def validator(definition):
    return Draft202012Validator({"$ref": f"{SCHEMA_ID}#/$defs/{definition}"}, registry=REGISTRY, format_checker=FormatChecker())


def errors(definition, document):
    return list(validator(definition).iter_errors(document))


def changed(document, **change):
    result = copy.deepcopy(document)
    for key, value in change.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = value
    return result


def calendar_month(instant, timezone):
    """The calendar month containing instant: local midnight on the 1st, end exclusive."""
    local = instant.astimezone(ZoneInfo(timezone))
    start = local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = (start.replace(year=start.year + 1, month=1) if start.month == 12 else start.replace(month=start.month + 1))
    return start, end


def is_calendar_month(period):
    if period["period_kind"] != "CALENDAR_MONTH":
        return False
    starts = datetime.fromisoformat(period["starts_at"])
    ends = datetime.fromisoformat(period["ends_at"])
    expected = calendar_month(starts, period["timezone"])
    return (starts, ends) == expected


class Ledger:
    """Reference model: per-period balance plus per-reservation remaining amounts."""

    def __init__(self, limit):
        self.limit, self.committed, self.reserved = limit, 0, 0
        self.reservations = {}
        self.seen = {}

    @property
    def available(self):
        return self.limit - self.committed - self.reserved

    def apply(self, kind, reservation, amount, key):
        if key in self.seen:  # an idempotent retry returns the original outcome
            return self.seen[key]
        held = self.reservations.get(reservation, 0)
        if amount <= 0:
            outcome = "REFUSED"
        elif kind == "RESERVE":
            outcome = "REFUSED" if amount > self.available else "APPLIED"
            if outcome == "APPLIED":
                self.reserved += amount
                self.reservations[reservation] = held + amount
        elif kind == "COMMIT":
            # Conversion only: committed rises by exactly what reserved falls.
            outcome = "REFUSED" if amount > held else "APPLIED"
            if outcome == "APPLIED":
                self.reserved -= amount
                self.committed += amount
                self.reservations[reservation] = held - amount
        elif kind == "RELEASE":
            outcome = "REFUSED" if amount > held else "APPLIED"
            if outcome == "APPLIED":
                self.reserved -= amount
                self.reservations[reservation] = held - amount
        else:
            outcome = "REFUSED"
        self.seen[key] = outcome
        return outcome


class BuyerSpendBudget(unittest.TestCase):
    def test_examples_are_valid(self):
        self.assertEqual([], errors("BuyerSpendBudgetPolicy", POLICY))
        self.assertEqual([], errors("SpendLedgerEntry", RESERVE))
        self.assertEqual([], errors("BudgetCapacity", CAPACITY))
        self.assertTrue(is_calendar_month(RESERVE["period"]))
        self.assertEqual(CAPACITY["available_minor"], CAPACITY["limit_minor"] - CAPACITY["committed_minor"] - CAPACITY["reserved_minor"])

    def test_a_budget_is_never_absent_null_or_zero(self):
        for limit in (0, None, -1, 1.5, "10000"):
            with self.subTest(limit=limit):
                self.assertNotEqual([], errors("BuyerSpendBudgetPolicy", changed(POLICY, limit_minor=limit)))

    def test_scope_fixes_the_period_and_the_binding(self):
        refused = [
            changed(POLICY, buyer_membership_id=None),
            changed(POLICY, period_kind="AGREEMENT_TERM"),
            changed(POLICY, agreement_reference="AGR-2026-0001"),
            changed(POLICY, scope="ORGANISATION"),
            changed(POLICY, scope="AGREEMENT", agreement_reference="AGR-2026-0001", buyer_membership_id=None, period_kind="AGREEMENT_TERM"),
            changed(POLICY, scope="ROLE"),
            changed(POLICY, period_kind="ROLLING_30_DAYS"),
        ]
        for document in refused:
            with self.subTest(document=document):
                self.assertNotEqual([], errors("BuyerSpendBudgetPolicy", document))
        organisation = changed(POLICY, scope="ORGANISATION", buyer_membership_id=None)
        agreement = changed(POLICY, scope="AGREEMENT", buyer_membership_id=None, agreement_reference="AGR-2026-0001",
                            period_kind="AGREEMENT_TERM", effective_until="2027-10-01T00:00:00+02:00")
        self.assertEqual([], errors("BuyerSpendBudgetPolicy", organisation))
        self.assertEqual([], errors("BuyerSpendBudgetPolicy", agreement))

    def test_ledger_entries_are_bound_and_typed(self):
        for change in ({"idempotency_key": "short"}, {"transaction_digest": "md5:abc"}, {"amount_minor": 0},
                       {"resource_version": 0}, {"release_reason": "CANCELLED"}, {"commitment_reference": "order_1"},
                       {"entry_kind": "ADJUST"}, {"reservation_id": None}):
            with self.subTest(change=change):
                self.assertNotEqual([], errors("SpendLedgerEntry", changed(RESERVE, **change)))
        commit = changed(RESERVE, entry_kind="COMMIT", commitment_reference="order_synthetic0001")
        release = changed(RESERVE, entry_kind="RELEASE", release_reason="PERIOD_ROLLOVER")
        self.assertEqual([], errors("SpendLedgerEntry", commit))
        self.assertEqual([], errors("SpendLedgerEntry", release))
        self.assertNotEqual([], errors("SpendLedgerEntry", changed(commit, commitment_reference=None)))
        self.assertNotEqual([], errors("SpendLedgerEntry", changed(release, release_reason=None)))

    def test_calendar_months_are_local_and_end_exclusive(self):
        jhb = "Africa/Johannesburg"
        start, end = calendar_month(datetime.fromisoformat("2026-10-31T22:30:00+00:00"), jhb)
        # 22:30 UTC on 31 October is already 1 November in Johannesburg.
        self.assertEqual((start.isoformat(), end.isoformat()), ("2026-11-01T00:00:00+02:00", "2026-12-01T00:00:00+02:00"))
        start, end = calendar_month(datetime.fromisoformat("2026-12-15T12:00:00+00:00"), "UTC")
        self.assertEqual((start.isoformat(), end.isoformat()), ("2026-12-01T00:00:00+00:00", "2027-01-01T00:00:00+00:00"))
        rolling = changed(RESERVE["period"], ends_at="2026-10-31T00:00:00+02:00")
        self.assertFalse(is_calendar_month(rolling))
        self.assertFalse(is_calendar_month(changed(RESERVE["period"], starts_at="2026-10-02T00:00:00+02:00")))

    def test_capacity_matches_the_ruling_example(self):
        # Decision 5: limit R100,000, committed R55,000, reserved R30,000 -> R15,000 available;
        # a R20,000 request is refused even under a R50,000 per-order cap.
        ledger = Ledger(10_000_000)
        self.assertEqual("APPLIED", ledger.apply("RESERVE", "b2bres_a", 5_500_000, "k-a-reserve"))
        self.assertEqual("APPLIED", ledger.apply("COMMIT", "b2bres_a", 5_500_000, "k-a-commit"))
        self.assertEqual("APPLIED", ledger.apply("RESERVE", "b2bres_b", 3_000_000, "k-b-reserve"))
        self.assertEqual(1_500_000, ledger.available)
        self.assertEqual("REFUSED", ledger.apply("RESERVE", "b2bres_c", 2_000_000, "k-c-reserve"))
        self.assertEqual("APPLIED", ledger.apply("RESERVE", "b2bres_c", 1_500_000, "k-c-reserve-2"))
        self.assertEqual(0, ledger.available)

    def test_reservations_convert_once_and_release_only_unused(self):
        ledger = Ledger(1_000)
        ledger.apply("RESERVE", "b2bres_a", 600, "k1")
        # A retried submission does not reserve twice.
        self.assertEqual("APPLIED", ledger.apply("RESERVE", "b2bres_a", 600, "k1"))
        self.assertEqual((600, 0), (ledger.reserved, ledger.committed))
        # Commit converts; consumption is never counted twice.
        ledger.apply("COMMIT", "b2bres_a", 400, "k2")
        self.assertEqual((200, 400, 400), (ledger.reserved, ledger.committed, ledger.available))
        # Only the verified unused portion can be released, and never more.
        self.assertEqual("REFUSED", ledger.apply("RELEASE", "b2bres_a", 201, "k3"))
        self.assertEqual("APPLIED", ledger.apply("RELEASE", "b2bres_a", 200, "k4"))
        self.assertEqual("REFUSED", ledger.apply("COMMIT", "b2bres_a", 1, "k5"))
        self.assertEqual((0, 400, 600), (ledger.reserved, ledger.committed, ledger.available))
        # Committed consumption is never released by the ledger: reversal needs its own policy.
        self.assertEqual("REFUSED", ledger.apply("RELEASE", "b2bres_unknown", 1, "k6"))

    def test_capacity_is_never_negative(self):
        self.assertNotEqual([], errors("BudgetCapacity", changed(CAPACITY, available_minor=-1)))


if __name__ == "__main__":
    unittest.main()
