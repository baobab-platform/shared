#!/usr/bin/env python3
"""DEV10-R5 fail-closed source packet validator; NOT an attestation verifier.

Checks truthful current engineering observations against the retained R1
source-only inventory. An accepted result cannot be produced from editable
JSON or CI statuses; it additionally requires independent cryptographic
validation, native runtime testing, and an explicitly approved gate change.
"""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / ".baobab/dev10-r5-acceptance.json"
MATRIX = ROOT / ".baobab/dev10-toolchain-matrix.json"

REQUIRED_CONTROLS = (
    "R1-MERGED-SOURCE",
    "R2-HOSTED-CODESPACE-CREATE",
    "R2-GHCR-USER-ENTITLEMENT",
    "R2-BXS-NPM-USER-ENTITLEMENT",
    "R2-REVOKE-NEGATIVE-AND-TEARDOWN",
    "R3-ALL-OWNERS-NATIVE",
    "R3-PLAYWRIGHT-ALL-ESTATES",
    "R4-PREFERRED-STABLE-LOCK",
    "R4-MULTIARCH-BUILD-READBACK",
    "R4-SBOM-PROVENANCE-AND-SIGNATURE",
    "R4-UNWAIVED-SECURITY",
    "R4-LOCKED-PRIVATE-CONSUMER-INSTALL",
    "R4-ROLLBACK-AND-PG17-SEPARATION",
    "R5-INDEPENDENT-REVIEW-AND-ACCEPTANCE",
)
ALLOWED_STATES = {"SOURCE_VERIFIED", "NOT_OBSERVED", "BLOCKED", "FAILED"}
SHA = re.compile(r"[0-9a-f]{40}\Z")
SAFE_URL = re.compile(r"https://github\.com/baobab-platform/[a-z0-9-]+/(?:actions/runs/[0-9]+|pull/[0-9]+|commit/[0-9a-f]{40})\Z")


def require(ok: bool, message: str):
    if not ok:
        raise ValueError(message)


def validate(packet: dict, matrix: dict, require_final: bool = False) -> str:
    require(packet.get("schema") == "dev10-r5-final-acceptance.v1", "R5_SCHEMA_INVALID")
    require(packet.get("classification") == "DEVELOPMENT_ONLY_SOURCE_SNAPSHOT_NOT_RUNTIME_PROOF", "R5_SOURCE_CLAIM_REQUIRED")
    base = packet.get("source_baseline", {})
    require(base.get("source_sha") == matrix["provider"]["source_sha"], "R5_PROVIDER_SOURCE_MISMATCH")
    require(base.get("repo") == "baobab-dev" and base.get("source_only") is True, "R5_SOURCE_SCOPE_INVALID")
    require(base.get("shared_r1_pr") == 426 and base.get("shared_r2_pr") == 427, "R5_MERGED_BASELINE_MISSING")
    candidate = packet.get("candidate_provider", {})
    require(candidate.get("repo") == "baobab-dev" and candidate.get("pull_request") == 57, "R5_CANDIDATE_PR_INVALID")
    require(isinstance(candidate.get("observed_head_sha"), str) and SHA.fullmatch(candidate["observed_head_sha"]) is not None, "R5_HEAD_SHA_INVALID")
    require(candidate.get("state") == "DRAFT_UNMERGED" and candidate.get("published_candidate_digest") is None, "R5_UNQUALIFIED_IMAGE_CLAIM")
    targets = packet.get("preferred_technologies", {})
    expected = {
        "node": "26.13.0", "pnpm": "12.16.1", "python": "3.14.10",
        "java": "21", "postgresql": "17", "playwright": "1.64.1", "corepack": "0.36.0",
    }
    require(targets == expected, "R5_PREFERRED_STABLE_TARGET_DRIFT")
    expected_repos = {row["repo"] for row in matrix["repositories"]}
    owners = packet.get("owners", [])
    require(isinstance(owners, list) and len(owners) == len(expected_repos), "R5_OWNER_COUNT_INVALID")
    require({row.get("repo") for row in owners} == expected_repos, "R5_MISSING_OR_DUPLICATE_OWNER")
    source_map = {row["repo"]: row["source_sha"] for row in matrix["repositories"]}
    for row in owners:
        require(row.get("baseline_main_sha") == source_map[row["repo"]], "R5_OWNER_SOURCE_MISMATCH")
        require(row.get("native_upgrade_accepted") is False, "R5_NATIVE_OWNER_UNQUALIFIED")
        require(row.get("fresh_hosted_codespace_accepted") is False, "R5_CODESPACE_OWNER_UNQUALIFIED")
        require(row.get("readiness") == "HELD", "R5_OWNER_FALSE_PASS")
        prs = row.get("related_pull_requests")
        require(isinstance(prs, list) and all(type(pr) is int and pr > 0 for pr in prs), "R5_PR_REFERENCE_INVALID")
    controls = packet.get("controls", [])
    require(isinstance(controls, list) and [row.get("id") for row in controls] == list(REQUIRED_CONTROLS), "R5_CONTROL_INVENTORY_CHANGED")
    require(controls[0]["state"] == "SOURCE_VERIFIED", "R5_MERGED_SOURCE_NOT_RECONCILED")
    for index, row in enumerate(controls):
        require(row.get("state") in ALLOWED_STATES, "R5_UNVERIFIED_GATE_CLAIM")
        if index:
            require(row["state"] != "SOURCE_VERIFIED", "R5_RUNTIME_MASQUERADING_AS_SOURCE")
        require(isinstance(row.get("reason"), str) and len(row["reason"]) >= 30, "R5_CONTROL_REASON_REQUIRED")
        urls = row.get("evidence_urls")
        require(isinstance(urls, list) and all(isinstance(url, str) and SAFE_URL.fullmatch(url) for url in urls), "R5_INVALID_EVIDENCE_URL")
    require(next(row for row in controls if row["id"] == "R4-UNWAIVED-SECURITY")["state"] == "FAILED", "R5_SECURITY_HOLD_REQUIRED")
    sec = packet.get("observed_security", {})
    require(sec.get("strict_dev10_cve_gate") == "FAILED", "R5_SECURITY_CHECK_NOT_CLEAR")
    require(sec.get("production_security_waiver") is False, "R5_PRODUCTION_WAIVER_FORBIDDEN")
    require(sec.get("temporary_foundation_exception_expires") == "2026-11-12", "R5_SECURITY_EXCEPTION_MUTATED")
    decision = packet.get("decision", {})
    require(decision.get("engineering_acceptance") == "HELD", "R5_FALSE_ACCEPTANCE")
    require(decision.get("actual_completion_date") is None, "R5_COMPLETION_FABRICATED")
    require(decision.get("dev10_source_accepted") is True, "R5_SOURCE_R1_NOT_ACCEPTED")
    for field in (
        "independent_evidence_custodian_verified", "all_gates_pass", "dev10_runtime_accepted",
        "staging_approved", "production_approved", "user_approved_merge", "release_authorized",
    ):
        require(decision.get(field) is False, "R5_UNAUTHORIZED_ACCEPTANCE_" + field.upper())
    evidence = packet.get("evidence_policy", {})
    for key in ("git_checks_not_hosted_codespaces", "ci_skipped_not_pass", "fixture_provider_not_real_psp"):
        require(evidence.get(key) is True, "R5_EVIDENCE_TYPE_CONFUSION_" + key.upper())
    require(evidence.get("raw_tokens_in_evidence") is False, "R5_CREDENTIALS_IN_RECEIPTS")
    for key in (
        "signed_provenance_attestation", "independent_codespace_creation_receipt",
        "independent_codespace_teardown_receipt", "rehearsed_rollback_receipt",
    ):
        require(evidence.get(key) is None, "R5_UNVERIFIED_EXTERNAL_RECEIPT_" + key.upper())
    if require_final:
        raise ValueError("R5_NOT_ACCEPTED_INDEPENDENT_PROOF_AND_OWNER_APPROVAL_REQUIRED")
    return "DEV10_R5_HELD_PACKET_VALID; no runtime/release acceptance"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-final", action="store_true",
                        help="Fail unless final engineering acceptance is independently established")
    args = parser.parse_args()
    try:
        result = validate(json.loads(PACKET.read_text()), json.loads(MATRIX.read_text()), args.require_final)
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print("DEV10_R5_DENIED: " + str(error), file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
