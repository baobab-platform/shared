#!/usr/bin/env python3
"""Validate the ADR-BCP-023 evidence/v1 contracts (gate OEV-01).

Real JSON Schema Draft 2020-12 validation with every cross-schema $ref
resolved against the contracts in this repository:

  1. each schema is a valid Draft 2020-12 schema whose $id matches its file;
  2. lifecycle.yaml is four sound state machines over the domain enums:
     every state is reachable, every non-terminal state can end, terminal
     states have no exits, and no APPLICANT transition ever makes evidence
     available or a claim, case or discrepancy verified, concluded or
     resolved (sections 9, 169, 238);
  3. every example validates, and the examples obey what the schemas cannot
     say (the evidence chain of section 178):
       - every identifier resolves;
       - a claim's verified, unverified or conflicted standing is its
         current result's outcome, for that claim;
       - a result cites only checks on its own claim and case;
       - VERIFIED rests on a positive check from a source trusted for the
         claim type in the claim's jurisdiction (sections 21-22);
       - nobody verifies their own claim (section 169);
       - a positive check never cites evidence reviewers cannot open
         (section 238);
       - a CONFLICTED case has a conflicted claim;
  4. negative fixtures prove the load-bearing rules reject bad data;
  5. contracts.lock.yaml registers exactly these files.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-evidence-contracts.py
"""

from __future__ import annotations

import copy
import json
import sys
from collections import deque
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PKG = CONTRACTS / "evidence" / "v1"
BASE_URI = "https://contracts.baobab-platform.com/evidence/v1/"
SCHEMAS = ["domain.schema.json", "evidence.schema.json", "verification.schema.json"]
YAMLS = ["lifecycle.yaml"]
ACTORS = {"APPLICANT", "REVIEWER", "PLATFORM"}
POSITIVE = {"MATCHED", "VERIFIED", "PARTIALLY_VERIFIED"}
# A claim's status after verification is its current result's outcome.
RESULT_STANDING = {"VERIFIED", "PARTIALLY_VERIFIED", "NOT_VERIFIED", "CONFLICTED", "EXPIRED", "REVOKED"}

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def registry() -> Registry:
    reg = Registry()
    for path in CONTRACTS.rglob("*.json"):
        try:
            doc = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if isinstance(doc, dict) and "$id" in doc:
            reg = reg.with_resource(doc["$id"], Resource.from_contents(doc))
    return reg


REG = registry()


def validator(ref: str) -> Draft202012Validator:
    return Draft202012Validator({"$ref": BASE_URI + ref}, registry=REG, format_checker=FormatChecker())


def errors(ref: str, instance) -> list[str]:
    return [f"{'/'.join(map(str, e.absolute_path)) or '/'}: {e.message}" for e in validator(ref).iter_errors(instance)]


# 1. Schemas.
domain = json.loads((PKG / "domain.schema.json").read_text())["$defs"]
for name in SCHEMAS:
    schema = json.loads((PKG / name).read_text())
    Draft202012Validator.check_schema(schema)
    if schema.get("$id") != BASE_URI + name:
        fail(f"{name}: $id must be {BASE_URI + name}")


# 2. Lifecycles.
def check_lifecycle(doc) -> list[str]:
    problems = []
    forbidden = set(doc.get("applicant_forbidden_targets", []))
    if not forbidden >= {"AVAILABLE", "VERIFIED", "RESOLVED"}:
        problems.append("applicant_forbidden_targets must at least forbid AVAILABLE, VERIFIED and RESOLVED")
    expected = {"evidence_record", "evidence_claim", "verification_case", "evidence_discrepancy"}
    if set(doc.get("machines", {})) != expected:
        problems.append(f"lifecycle.yaml must define exactly the machines {sorted(expected)}")
        return problems
    for name, machine in doc["machines"].items():
        states = set(domain[machine["states_from"]]["enum"])
        initials = set(machine["initial_by_origin"].values()) if "initial_by_origin" in machine else {machine["initial"]}
        if "initial_by_origin" in machine and set(machine["initial_by_origin"]) != set(domain["assertionOrigin"]["enum"]):
            problems.append(f"{name}: initial_by_origin must name every assertionOrigin")
        terminal = set(machine["terminal"])
        if not initials <= states or not terminal <= states:
            problems.append(f"{name}: initial and terminal states must be {machine['states_from']} values")
        edges: dict[str, set[str]] = {s: set() for s in states}
        seen = set()
        for t in machine["transitions"]:
            key = (t["command"], t["from"], t["to"])
            if key in seen:
                problems.append(f"{name}: transition {key} is listed twice")
            seen.add(key)
            if t["from"] not in states or t["to"] not in states:
                problems.append(f"{name}: {t['command']} {t['from']} -> {t['to']} uses an unknown state")
                continue
            if t["from"] in terminal:
                problems.append(f"{name}: terminal state {t['from']} has an exit ({t['command']})")
            if not t["actors"] or not set(t["actors"]) <= ACTORS:
                problems.append(f"{name}: {t['command']} {t['from']} -> {t['to']} must name actors from {sorted(ACTORS)}")
            if "APPLICANT" in t["actors"] and t["to"] in forbidden:
                problems.append(f"{name}: an APPLICANT may not move anything to {t['to']} ({t['command']})")
            edges[t["from"]].add(t["to"])
        reached, queue = set(initials), deque(initials)
        while queue:
            for nxt in edges[queue.popleft()]:
                if nxt not in reached:
                    reached.add(nxt)
                    queue.append(nxt)
        if reached != states:
            problems.append(f"{name}: unreachable states {sorted(states - reached)}")
        for state in states - terminal:
            ends, queue = {state}, deque([state])
            while queue:
                for nxt in edges[queue.popleft()]:
                    if nxt not in ends:
                        ends.add(nxt)
                        queue.append(nxt)
            if not ends & terminal:
                problems.append(f"{name}: {state} can never end")
        if name == "evidence_record":
            accessible = set(machine["content_accessible"])
            if accessible & {"RECEIVED", "QUARANTINED", "DESTROYED", "RESTRICTED"}:
                problems.append("evidence_record: content is never accessible while received, quarantined, restricted or destroyed (section 238)")
            # Content becomes accessible only by accepting received material,
            # releasing scanned material, or lifting a restriction; no other
            # transition (supersession, for one) may open it (section 238).
            openers = {("accept", "RECEIVED"), ("release", "QUARANTINED"), ("unrestrict", "RESTRICTED")}
            for t in machine["transitions"]:
                if t["to"] in accessible and t["from"] not in accessible and (t["command"], t["from"]) not in openers:
                    problems.append(f"evidence_record: {t['command']} {t['from']} -> {t['to']} would open content that is not accessible")
                if t["from"] == "QUARANTINED" and t["to"] == "AVAILABLE" and t["actors"] != ["PLATFORM"]:
                    problems.append("evidence_record: only the platform's scan releases quarantined evidence")
    return problems


lifecycle = load_yaml(PKG / "lifecycle.yaml")
for problem in check_lifecycle(lifecycle):
    fail(f"lifecycle.yaml: {problem}")
content_accessible = set(lifecycle["machines"]["evidence_record"]["content_accessible"])

# 3. Examples.
KINDS = {
    "sources": ("evidence.schema.json#/$defs/EvidenceSource", "source_id"),
    "evidence": ("evidence.schema.json#/$defs/EvidenceRecord", "evidence_id"),
    "claim_submissions": ("evidence.schema.json#/$defs/EvidenceClaimSubmission", None),
    "claims": ("evidence.schema.json#/$defs/EvidenceClaim", "claim_id"),
    "cases": ("verification.schema.json#/$defs/VerificationCase", "case_id"),
    "checks": ("verification.schema.json#/$defs/VerificationCheck", "check_id"),
    "results": ("verification.schema.json#/$defs/VerificationResult", "result_id"),
    "discrepancies": ("verification.schema.json#/$defs/EvidenceDiscrepancy", "discrepancy_id"),
    "references": ("evidence.schema.json#/$defs/EvidenceReference", None),
}


def cross_check(ex) -> list[str]:
    """The rules of the evidence chain that no single schema can state."""
    problems = []
    index = {}
    for kind, (_, key) in KINDS.items():
        if key is None:
            continue
        index[kind] = {}
        for item in ex.get(kind, []):
            if item[key] in index[kind]:
                problems.append(f"{kind}: {item[key]} appears twice")
            index[kind][item[key]] = item
    sources, evidence, claims = index["sources"], index["evidence"], index["claims"]
    cases, checks, results, discrepancies = index["cases"], index["checks"], index["results"], index["discrepancies"]

    def need(kind, ident, where):
        if ident not in index[kind]:
            problems.append(f"{where} names unknown {kind[:-1] if kind != 'evidence' else 'evidence'} {ident}")
            return None
        return index[kind][ident]

    for rec in evidence.values():
        need("sources", rec["source_id"], f"evidence {rec['evidence_id']}")
        if "supersedes" in rec:
            need("evidence", rec["supersedes"], f"evidence {rec['evidence_id']}")
    for ref in ex.get("references", []):
        rec = need("evidence", ref["evidence_id"], "reference")
        if rec and any(rec[k] != ref[k] for k in ("evidence_type", "status", "classification")):
            problems.append(f"reference {ref['evidence_id']} disagrees with its record")
    for sub in ex.get("claim_submissions", []):
        for ev in sub.get("evidence_ids", []):
            need("evidence", ev, "claim submission")
    for claim in claims.values():
        cid = claim["claim_id"]
        for ev in claim["evidence_ids"]:
            need("evidence", ev, f"claim {cid}")
        if claim["status"] in RESULT_STANDING:
            result = need("results", claim.get("current_result_id"), f"claim {cid}")
            if result:
                if result["claim_id"] != cid:
                    problems.append(f"claim {cid}: its current result {result['result_id']} is for {result['claim_id']}")
                if result["outcome"] != claim["status"]:
                    problems.append(f"claim {cid} is {claim['status']} but its current result is {result['outcome']}")
    for case in cases.values():
        for c in case["claim_ids"]:
            need("claims", c, f"case {case['case_id']}")
        if case["status"] == "CONFLICTED" and not any(claims.get(c, {}).get("status") == "CONFLICTED" for c in case["claim_ids"]):
            problems.append(f"case {case['case_id']} is CONFLICTED but none of its claims is")
        if "supersedes" in case:
            need("cases", case["supersedes"], f"case {case['case_id']}")

    def applicant_of(claim):
        return claim["asserted_by"] if claim and claim["asserted_via"] == "APPLICANT" else None

    for chk in checks.values():
        where = f"check {chk['check_id']}"
        case = need("cases", chk["case_id"], where)
        claim = need("claims", chk["claim_id"], where)
        need("sources", chk["source_id"], where)
        if case and claim and chk["claim_id"] not in case["claim_ids"]:
            problems.append(f"{where}: claim {chk['claim_id']} is not part of case {chk['case_id']}")
        if chk.get("performed_by") and chk["performed_by"] == applicant_of(claim):
            problems.append(f"{where}: the applicant checked their own claim (section 169)")
        for ev in chk["evidence_ids"]:
            rec = need("evidence", ev, where)
            if rec and chk["outcome"] in POSITIVE and rec["status"] not in content_accessible:
                problems.append(f"{where}: a positive check cites {ev}, which is {rec['status']} and not open to reviewers (section 238)")
    for res in results.values():
        where = f"result {res['result_id']}"
        claim = need("claims", res["claim_id"], where)
        need("cases", res["case_id"], where)
        if res.get("decided_by") and res["decided_by"] == applicant_of(claim):
            problems.append(f"{where}: the applicant decided their own claim (section 169)")
        cited = [need("checks", c, where) for c in res["check_ids"]]
        for chk in filter(None, cited):
            if chk["claim_id"] != res["claim_id"] or chk["case_id"] != res["case_id"]:
                problems.append(f"{where}: cites {chk['check_id']}, which is for another claim or case")
        for d in res.get("discrepancy_ids", []):
            disc = need("discrepancies", d, where)
            if disc and claim and (disc["claim_type"] != claim["claim_type"] or disc["subject"] != claim["subject"]
                                   or disc.get("case_id") != res["case_id"]):
                problems.append(f"{where}: discrepancy {d} is not about this claim's type and subject in case {res['case_id']}")
        if res["outcome"] == "VERIFIED" and claim:
            def trusted(chk):
                src = sources.get(chk["source_id"])
                return src is not None and src["status"] == "ACTIVE" and any(
                    t["claim_type"] == claim["claim_type"] and t["jurisdiction"] == claim.get("jurisdiction", t["jurisdiction"])
                    for t in src["trusted_for"])
            if not any(chk and chk["outcome"] in ("VERIFIED", "MATCHED") and trusted(chk) for chk in cited):
                problems.append(f"{where}: VERIFIED needs a positive check from a source trusted for "
                                f"{claim['claim_type']} in {claim.get('jurisdiction', 'its jurisdiction')} (sections 21-22)")
    for disc in discrepancies.values():
        where = f"discrepancy {disc['discrepancy_id']}"
        if "case_id" in disc:
            need("cases", disc["case_id"], where)
        if len({v["source_id"] for v in disc["conflicting_values"]}) < 2:
            problems.append(f"{where}: a discrepancy is between at least two sources")
        for v in disc["conflicting_values"]:
            need("sources", v["source_id"], where)
            if "evidence_id" in v:
                need("evidence", v["evidence_id"], where)
            if "check_id" in v:
                need("checks", v["check_id"], where)
    return problems


example_path = PKG / "examples" / "organisation-admission-verification.json"
example = json.loads(example_path.read_text())
for kind, (ref, _) in KINDS.items():
    if not example.get(kind):
        fail(f"{example_path.name}: needs at least one {kind} entry")
    for i, item in enumerate(example.get(kind, [])):
        for message in errors(ref, item):
            fail(f"{example_path.name} {kind}[{i}]: {message}")
for problem in cross_check(example):
    fail(f"{example_path.name}: {problem}")


# 4. Negative fixtures.
def must_reject(label: str, ref: str, instance) -> None:
    if not errors(ref, instance):
        fail(f"negative fixture accepted: {label}")


def must_break(label: str, ex) -> None:
    if not cross_check(ex):
        fail(f"negative fixture accepted: {label}")


def mutate(base, **changes):
    out = copy.deepcopy(base)
    for key, value in changes.items():
        if value is None:
            out.pop(key, None)
        else:
            out[key] = value
    return out


def first(kind, key, value):
    return next(item for item in example[kind] if item[key] == value)


E, S, C = (f"evidence.schema.json#/$defs/{n}" for n in ("EvidenceRecord", "EvidenceSource", "EvidenceClaim"))
SUB = "evidence.schema.json#/$defs/EvidenceClaimSubmission"
CASE, CHK, RES, DIS = (f"verification.schema.json#/$defs/{n}" for n in
                       ("VerificationCase", "VerificationCheck", "VerificationResult", "EvidenceDiscrepancy"))
cert, ursb = first("evidence", "evidence_id", "evr_cert01"), first("sources", "source_id", "esrc_ursb")
applicant_source = first("sources", "source_id", "esrc_applicant")
regno, submission = first("claims", "claim_id", "ecl_regno"), example["claim_submissions"][0]
reg_check, name_check = first("checks", "check_id", "vchk_regnoreg"), first("checks", "check_id", "vchk_namereg")
verified, conflicted = first("results", "result_id", "vres_regno"), first("results", "result_id", "vres_name")
open_disc, closed_disc = first("discrepancies", "discrepancy_id", "edis_name"), first("discrepancies", "discrepancy_id", "edis_addr")

must_reject("evidence carrying document content", E, mutate(cert, content="JVBERi0xLjcK"))
must_reject("evidence with no material", E, mutate(cert, artifact_id=None))
must_reject("evidence with no submitter or retriever", E, mutate(cert, submitted_by=None))
must_reject("an applicant-supplied source trusted for a claim", S,
            mutate(applicant_source, trusted_for=[{"claim_type": "LEGAL_NAME", "jurisdiction": "UG"}]))
must_reject("a claim submission asserting its own status", SUB, mutate(submission, status="VERIFIED"))
must_reject("a claim submission asserting verification", SUB, mutate(submission, verified=True))
must_reject("a VERIFIED claim with no result", C, mutate(regno, current_result_id=None))
must_reject("a positive check with no evidence or source record", CHK,
            mutate(reg_check, evidence_ids=[], source_record_reference=None))
must_reject("a positive check that never matched the claim", CHK,
            mutate(reg_check, dimensions=[{"dimension": "DOCUMENT_INTEGRITY", "outcome": "PASSED"}]))
must_reject("a human check with no reviewer", CHK, mutate(reg_check, performed_by=None))
must_reject("a performed check with no time", CHK, mutate(name_check, performed_at=None))
must_reject("a result answering one dimension twice", RES,
            mutate(verified, dimensions=verified["dimensions"] + [{"dimension": "CLAIM_MATCH", "outcome": "FAILED"}]))
must_reject("a check answering one dimension twice", CHK,
            mutate(reg_check, dimensions=reg_check["dimensions"] + [{"dimension": "ISSUER_AUTHORITY", "outcome": "FAILED"}]))
must_reject("VERIFIED without issuer authority", RES,
            mutate(verified, dimensions=[{"dimension": "CLAIM_MATCH", "outcome": "PASSED"}]))
must_reject("a CONFLICTED result with no discrepancy", RES, mutate(conflicted, discrepancy_ids=None))
must_reject("a VERIFIED result citing no check", RES, mutate(verified, check_ids=[]))
must_reject("a resolved discrepancy with no resolver", DIS, mutate(closed_disc, resolved_by=None))
must_reject("an open discrepancy already resolved", DIS, mutate(open_disc, resolution="NOT_MATERIAL"))
must_reject("a discrepancy between one value", DIS, mutate(open_disc, conflicting_values=open_disc["conflicting_values"][:1]))
must_reject("a RESOLVED discrepancy resolved as an exception", DIS,
            mutate(closed_disc, status="RESOLVED", resolution="EXCEPTION_ACCEPTED"))
must_reject("a completed case with no completion time", CASE,
            mutate(example["cases"][0], status="VERIFIED"))


def with_items(kind, key, value, **changes):
    out = copy.deepcopy(example)
    out[kind] = [mutate(i, **changes) if i[key] == value else i for i in out[kind]]
    return out


must_break("an applicant verifying their own claim",
           with_items("checks", "check_id", "vchk_regnoreg", performed_by="prn_amina"))
must_break("an applicant deciding their own result", with_items("results", "result_id", "vres_regno", decided_by="prn_amina"))
must_break("VERIFIED on an applicant-supplied source alone",
           with_items("results", "result_id", "vres_regno", check_ids=["vchk_regnodoc"]))
must_break("VERIFIED by a source trusted in another jurisdiction",
           with_items("claims", "claim_id", "ecl_regno", jurisdiction="ZA"))
must_break("a claim status that is not its result's outcome", with_items("claims", "claim_id", "ecl_regno", status="PARTIALLY_VERIFIED"))
must_break("a positive check citing quarantined evidence",
           with_items("checks", "check_id", "vchk_regnoreg", evidence_ids=["evr_poa01"]))
must_break("a result citing another claim's check",
           with_items("results", "result_id", "vres_regno", check_ids=["vchk_regnoreg", "vchk_namereg"]))
must_break("a CONFLICTED case with no conflicted claim",
           with_items("claims", "claim_id", "ecl_name", status="UNDER_VERIFICATION", current_result_id=None))
other_case = copy.deepcopy(example)
other_case["cases"].append(mutate(example["cases"][0], case_id="vcase_adm02", status="VERIFYING"))
other_case["discrepancies"] = [mutate(d, case_id="vcase_adm02") if d["discrepancy_id"] == "edis_name" else d
                               for d in other_case["discrepancies"]]
must_break("a result citing another case's discrepancy", other_case)
must_break("a result citing a discrepancy about another subject",
           with_items("discrepancies", "discrepancy_id", "edis_name",
                      subject={"subject_type": "LEGAL_ENTITY", "subject_id": "LE-01k9otherentity"}))
must_break("an unknown evidence reference", with_items("claims", "claim_id", "ecl_rep", evidence_ids=["evr_missing"]))

bad = copy.deepcopy(lifecycle)
bad["machines"]["evidence_claim"]["transitions"].append(
    {"command": "self_verify", "from": "SELF_ASSERTED", "to": "VERIFIED", "actors": ["APPLICANT"]})
if not check_lifecycle(bad):
    fail("negative fixture accepted: an applicant transition to VERIFIED")
bad = copy.deepcopy(lifecycle)
bad["machines"]["evidence_record"]["transitions"].append(
    {"command": "supersede", "from": "RESTRICTED", "to": "SUPERSEDED", "actors": ["PLATFORM"]})
if not check_lifecycle(bad):
    fail("negative fixture accepted: supersession lifting a restriction")
bad = copy.deepcopy(lifecycle)
bad["machines"]["evidence_record"]["content_accessible"].append("QUARANTINED")
if not check_lifecycle(bad):
    fail("negative fixture accepted: quarantined evidence open to reviewers")
bad = copy.deepcopy(lifecycle)
bad["machines"]["verification_case"]["transitions"].append(
    {"command": "reopen", "from": "CANCELLED", "to": "VERIFYING", "actors": ["REVIEWER"]})
if not check_lifecycle(bad):
    fail("negative fixture accepted: a terminal case state with an exit")

# 5. Lock file.
lock = load_yaml(ROOT / "contracts.lock.yaml")
entry = next((c for c in lock["contracts"] if c["domain"] == "evidence" and c["version"] == "v1"), None)
expected = sorted(SCHEMAS + YAMLS)
if entry is None or sorted(entry["schemas"]) != expected:
    fail(f"contracts.lock.yaml must register evidence v1 as exactly {expected}")

if failures:
    for message in failures:
        print(f"evidence contract validation failed: {message}", file=sys.stderr)
    sys.exit(1)
print("Evidence contract validation passed")
