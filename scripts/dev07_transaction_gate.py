#!/usr/bin/env python3
"""DEV-07 independently reviewable transaction readback (no authority promotion).

This verifies cross-record consistency in a redacted observer projection, not
the authenticity of the observer or the reality of a remote database. Only an
independent current-source owner can qualify the evidence and canonical cases.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts/development/v1/dev07-transaction-readback.schema.json"
NEGATIVE_IDS = frozenset((
    "wrong_tenant_company", "invalid_audience", "revoked_mandate",
    "stale_buyer_authority", "changed_event_payload", "duplicate_delivery",
    "expired_lease", "simultaneous_reservation", "publisher_outage",
    "post_commit_pre_ack_crash", "ambiguous_erp_outcome",
))
RECOVERY_CASES = frozenset((
    "duplicate_delivery", "expired_lease", "simultaneous_reservation",
    "publisher_outage", "post_commit_pre_ack_crash", "ambiguous_erp_outcome",
))
DENIAL_CASES = NEGATIVE_IDS - RECOVERY_CASES
SCHEMA_OBJECT = json.loads(SCHEMA.read_text(encoding="utf-8"))
Draft202012Validator.check_schema(SCHEMA_OBJECT)
VALIDATOR = Draft202012Validator(SCHEMA_OBJECT, format_checker=FormatChecker())


def check_report(report: object) -> list[str]:
    """Return closed fail-closed findings; never return an acceptance grant."""
    errors = sorted(
        ("schema: " + "/".join(str(p) for p in err.absolute_path) + ": " + err.message)
        for err in VALIDATOR.iter_errors(report)
    )
    if errors:
        return errors
    assert isinstance(report, dict)  # established by the schema
    obs = report["observations"]
    if obs is not None:
        order = obs["order"]
        tx = order["txid"]
        for name in ("seller", "buyer", "spend", "outbox"):
            fact = obs[name]
            if fact["txid"] != tx:
                errors.append(f"{name}: different PostgreSQL transaction ID")
            if fact["order_id"] != order["id"]:
                errors.append(f"{name}: different native order ID")
            if fact["count"] != 1:
                errors.append(f"{name}: multiplicity is not one")
        for name in ("seller", "buyer"):
            if obs[name]["operation_reference"] != order["operation_reference"]:
                errors.append(f"{name}: operation reference mismatch")
        if obs["seller"]["receipt_id"] == obs["buyer"]["receipt_id"]:
            errors.append("seller/buyer receipts must be distinct facts")
        if obs["spend"]["amount_minor"] != order["amount_minor"]:
            errors.append("spend commitment differs from final native obligation")
        if obs["spend"]["currency"] != order["currency"]:
            errors.append("spend commitment currency differs from order currency")
    downstream = report["downstream"]
    if downstream["status"] == "OBSERVED":
        if obs is None:
            errors.append("downstream observed without a native buyer commitment")
        else:
            if downstream["event_id"] != obs["outbox"]["event_id"]:
                errors.append("ERP event identity is not the original Trade outbox event")
            if downstream["payload_sha256"] != obs["outbox"]["payload_sha256"]:
                errors.append("ERP event payload differs from the original Trade outbox")
        for field in ("publisher_confirmed", "broker_delivered", "erp_inbox_durable",
                      "exported_trace_observed"):
            if downstream[field] is not True:
                errors.append(f"downstream: {field} not independently observed")
        if downstream["erp_native_effect_count"] != 1:
            errors.append("downstream: exactly one native ERP effect required")
    else:
        if any((downstream["event_id"] is not None, downstream["payload_sha256"] is not None,
                downstream["publisher_confirmed"], downstream["broker_delivered"],
                downstream["erp_inbox_durable"], downstream["erp_native_effect_count"] != 0,
                downstream["exported_trace_observed"])):
            errors.append("BLOCKED downstream cannot masquerade as observed success")
    for name in NEGATIVE_IDS:
        case = report["negatives"][name]
        if case["status"] != "PASS":
            if case["status"] == "FAIL":
                errors.append(f"{name}: explicitly failed")
            continue
        if case["prohibited_effect_count"] != 0:
            errors.append(f"{name}: prohibited business effect observed")
        if case["retry_count"] > case["retry_limit"]:
            errors.append(f"{name}: retries exceeded budget")
        expected = 1 if name in RECOVERY_CASES else 0
        if case["eligible_effect_count"] != expected:
            errors.append(f"{name}: expected {expected} eligible business effects")
    return errors


def disposition(report: object) -> tuple[str, list[str]]:
    errors = check_report(report)
    if errors:
        return "INVALID", errors
    assert isinstance(report, dict)
    if report["evidence_class"] == "SCHEMA_TEST_VECTOR":
        return "TEST_VECTOR_ONLY", []
    if report["positive_status"] != "OBSERVED" or report["downstream"]["status"] != "OBSERVED":
        return "BLOCKED", []
    if any(item["status"] != "PASS" for item in report["negatives"].values()):
        return "BLOCKED", []
    # A current-source independent verifier must still authenticate run custody,
    # IAM/CP grants, the native reads, source tuple and original canonical case IDs.
    return "CANDIDATE_INDEPENDENT_REVIEW", []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="JSON projection from independent observer")
    parser.add_argument("--require-candidate", action="store_true",
                        help="nonzero unless all structural gates qualify for independent review")
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    state, errors = disposition(report)
    print(json.dumps({"disposition": state, "errors": errors}, indent=2))
    if errors or (args.require_candidate and state != "CANDIDATE_INDEPENDENT_REVIEW"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
