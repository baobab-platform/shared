#!/usr/bin/env python3
"""Validate the ADR-BCP-025 topology/v1 contracts (gate ER-01).

Real JSON Schema Draft 2020-12 validation with every cross-schema $ref
resolved against the contracts in this repository:

  1. each schema is a valid Draft 2020-12 schema whose $id matches its file;
  2. the identifiers the Control Plane mints (engineReleaseId,
     deploymentObservationId) have one grammar, in control-plane/v1, and
     the drift model knows ENGINE_INSTANCE_RELEASE (section 3);
  3. release-policy.yaml is a sound lifecycle over releaseStatus: every
     status is reachable, REVOKED is terminal and reachable from every other
     status, only APPROVED may become desired and a revoked release is never
     readable as desired; approval policy names every environment; every
     drift reason has a grace period and a severity (sections 2.4-2.7);
  4. the reason-code registry registers exactly the drift reasons, and
     every engine_release code the schemas name;
  5. deployment:observe is a workload-only, unprivileged Control Plane
     scope, so an engine or a human never reports a deployment (section 2.9);
  6. metric labels are bounded: no digest, version, release, instance or
     tenant label (section 2.10);
  7. every example validates, and obeys what the schemas cannot say:
       - each provider belongs to the release's engine and each capability
         is catalogued (section 2.1.2);
       - a digest belongs to one release (section 2.1 rule 3);
       - a desired release is APPROVED or DEPRECATED and of the instance's
         engine (sections 2.4-2.5);
       - each observed release is what its observation's digests derive
         (section 2.6), with windows inside the policy's TTL bounds;
       - release drift names an instance and the reason its state implies;
  8. negative fixtures prove the load-bearing rules reject bad data;
  9. every event payload is published by asyncapi.yaml and registered to
     baobab-cp;
 10. contracts.lock.yaml registers exactly these files;
 11. the Control Plane's engine release routes (gate ER-02) record only the
     record request, return EngineRelease, and are open to release tooling
     only under the workload-only engine-release:record scope.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-topology-contracts.py
"""

from __future__ import annotations

import copy
import json
import re
import sys
from collections import deque
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PKG = CONTRACTS / "topology" / "v1"
CP = CONTRACTS / "control-plane" / "v1"
BASE_URI = "https://contracts.baobab-platform.com/topology/v1/"
CP_URI = "https://contracts.baobab-platform.com/control-plane/v1/"
SCHEMAS = [
    "domain.schema.json",
    "release.schema.json",
    "deployment-observation.schema.json",
    "events.schema.json",
]
YAMLS = ["release-policy.yaml", "asyncapi.yaml"]
SEVERITIES = {"INFO", "WARNING", "DEGRADED", "CRITICAL"}
FORBIDDEN_LABELS = {
    "digest", "artifact_digest", "release_id", "release_version", "version", "source_revision",
    "engine_instance_id", "instance", "tenant_id", "tenant", "observation_id", "region",
}

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


def errors(ref: str, instance, base: str = BASE_URI) -> list[str]:
    validator = Draft202012Validator({"$ref": base + ref}, registry=REG, format_checker=FormatChecker())
    return [f"{'/'.join(map(str, e.absolute_path)) or '/'}: {e.message}" for e in validator.iter_errors(instance)]


def accepts(ref: str, instance, label: str, base: str = BASE_URI) -> None:
    for problem in errors(ref, instance, base):
        fail(f"{label}: {ref} rejected it: {problem}")


def rejects(ref: str, instance, label: str, base: str = BASE_URI) -> None:
    if not errors(ref, instance, base):
        fail(f"negative fixture accepted by {ref}: {label}")


def when(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


# 1. Schemas.
for name in SCHEMAS:
    schema = json.loads((PKG / name).read_text())
    Draft202012Validator.check_schema(schema)
    if schema.get("$id") != BASE_URI + name:
        fail(f"{name}: $id must be {BASE_URI + name}")
domain = json.loads((PKG / "domain.schema.json").read_text())["$defs"]
statuses = set(domain["releaseStatus"]["enum"])
drift_reasons = set(domain["releaseDriftReason"]["enum"])
observed_states = set(domain["observedReleaseState"]["enum"])

# 2. Control Plane identifiers and drift object type.
cp_domain = json.loads((CP / "domain.schema.json").read_text())["$defs"]
for name, prefix in (("engineReleaseId", "erl_"), ("deploymentObservationId", "dob_")):
    if cp_domain.get(name, {}).get("pattern") != f"^{prefix}[a-z0-9]+$":
        fail(f"control-plane/v1 domain.schema.json#/$defs/{name} must have pattern ^{prefix}[a-z0-9]+$")
if "ENGINE_INSTANCE_RELEASE" not in cp_domain["driftObjectType"]["enum"]:
    fail("control-plane/v1 driftObjectType must include ENGINE_INSTANCE_RELEASE (ADR-BCP-025 section 3)")
for name in SCHEMAS:
    text = (PKG / name).read_text()
    if re.search(r'"(engineReleaseId|deploymentObservationId)"\s*:', text):
        fail(f"{name} must reference the control-plane/v1 identifiers, not redefine them")

# 3. release-policy.yaml.
policy = load_yaml(PKG / "release-policy.yaml")
lifecycle = policy["status_transitions"]
edges: dict[str, set[str]] = {s: set() for s in statuses}
for t in lifecycle["transitions"]:
    if t["to"] not in statuses or not set(t["from"]) <= statuses:
        fail(f"release-policy.yaml: {t['command']} uses a status outside releaseStatus")
        continue
    for source in t["from"]:
        if source in lifecycle["terminal"]:
            fail(f"release-policy.yaml: terminal status {source} has an exit ({t['command']})")
        edges[source].add(t["to"])
if lifecycle["initial"] != "CANDIDATE" or lifecycle["terminal"] != ["REVOKED"]:
    fail("release-policy.yaml: a release starts CANDIDATE and only REVOKED is terminal (section 2.4)")
reached, queue = {lifecycle["initial"]}, deque([lifecycle["initial"]])
while queue:
    for nxt in edges[queue.popleft()]:
        if nxt not in reached:
            reached.add(nxt)
            queue.append(nxt)
if reached != statuses:
    fail(f"release-policy.yaml: unreachable statuses {sorted(statuses - reached)}")
for status in statuses - {"REVOKED"}:
    if "REVOKED" not in edges[status]:
        fail(f"release-policy.yaml: a {status} release must be revocable (section 2.4)")
desired = policy["desired_state"]
if desired["may_become_desired"] != ["APPROVED"]:
    fail("release-policy.yaml: only an APPROVED release may become desired (section 2.5)")
if set(desired["readable_as_desired"]) != {"APPROVED", "DEPRECATED"}:
    fail("release-policy.yaml: a desired-state read returns only APPROVED or DEPRECATED releases (section 2.4)")
if desired.get("revocation_requires_disposition_of_every_desiring_instance") is not True:
    fail("release-policy.yaml: revocation must dispose of every desiring instance (section 2.4)")
environments = set(cp_domain["environment"]["enum"])
for key in ("provenance_required", "certification_required"):
    values = policy["approval"][key]
    if set(values) != environments or not all(isinstance(v, bool) for v in values.values()):
        fail(f"release-policy.yaml: approval.{key} must give a boolean for every environment {sorted(environments)}")
ttl = policy["observation"]["ttl_seconds"]
if not (isinstance(ttl["minimum"], int) and isinstance(ttl["maximum"], int) and 0 < ttl["minimum"] < ttl["maximum"]):
    fail("release-policy.yaml: observation.ttl_seconds needs 0 < minimum < maximum")
if set(policy["observation"]["effective_state"].values()) != {"UNKNOWN"}:
    fail("release-policy.yaml: an expired, missing or future observation is UNKNOWN (section 2.6)")
order = [(o["field"], o["direction"]) for o in policy["observation"]["current_observation_order"]]
if order != [("observed_at", "descending"), ("ingestion_sequence", "descending")]:
    fail("release-policy.yaml: the current observation is the latest observed_at, then the highest ingestion_sequence")
reasons_policy = policy["drift"]["reasons"]
if set(reasons_policy) != drift_reasons:
    fail(f"release-policy.yaml: drift.reasons must be exactly releaseDriftReason {sorted(drift_reasons)}")
for reason, rule in reasons_policy.items():
    if not isinstance(rule.get("grace_seconds"), int) or rule["grace_seconds"] < 0 or rule.get("severity") not in SEVERITIES:
        fail(f"release-policy.yaml: {reason} needs a non-negative grace_seconds and a severity in {sorted(SEVERITIES)}")
if reasons_policy.get("REVOKED_RELEASE_RUNNING", {}).get("severity") != "CRITICAL":
    fail("release-policy.yaml: a revoked release running is critical drift (section 2.4)")

# 4. Reason codes.
codes = load_yaml(CONTRACTS / "authorization" / "v1" / "reason-code-registry.yaml")["reason_codes"]
by_category: dict[str, set[str]] = {}
for entry in codes:
    by_category.setdefault(entry["category"], set()).add(entry["code"])
if by_category.get("release_drift", set()) != drift_reasons:
    fail("reason-code-registry.yaml: the release_drift category must be exactly releaseDriftReason")
named = set()
for name in SCHEMAS:
    named |= set(re.findall(r"\b((?:RELEASE|DEPLOYMENT_OBSERVATION)_[A-Z_]+)\b", (PKG / name).read_text()))
named -= drift_reasons
missing = named - by_category.get("engine_release", set())
if missing:
    fail(f"reason codes named by the topology schemas are not registered as engine_release: {sorted(missing)}")

# 5. The reporter scope.
scopes = {s["name"]: s for s in load_yaml(CONTRACTS / "authorization" / "v1" / "scope-registry.yaml")["scopes"]}
observe = scopes.get("deployment:observe")
if observe is None:
    fail("scope-registry.yaml must register deployment:observe (section 2.9)")
elif observe.get("allowed_actors") != ["workload"] or observe.get("privileged") or observe.get("audience") != ["baobab-control-plane"]:
    fail("deployment:observe must be an unprivileged workload-only scope for baobab-control-plane (section 2.9)")

# 6. Metric labels.
labels = set(domain["topologyMetricLabel"]["enum"])
if labels & FORBIDDEN_LABELS:
    fail(f"topologyMetricLabel names unbounded labels {sorted(labels & FORBIDDEN_LABELS)} (section 2.10)")

# 7. Examples.
catalogue = {c["capability_key"] for c in load_yaml(CONTRACTS / "capability" / "v1" / "catalogue.yaml")["capabilities"]}
KINDS = {
    "record_requests": "release.schema.json#/$defs/EngineReleaseRecordRequest",
    "releases": "release.schema.json#/$defs/EngineRelease",
    "status_change_requests": "release.schema.json#/$defs/EngineReleaseStatusChangeRequest",
    "desired_releases": "release.schema.json#/$defs/EngineInstanceDesiredRelease",
    "observation_submissions": "deployment-observation.schema.json#/$defs/DeploymentObservationSubmission",
    "observations": "deployment-observation.schema.json#/$defs/DeploymentObservation",
    "observed_releases": "deployment-observation.schema.json#/$defs/ObservedRelease",
}


def support_problems(release: dict, label: str) -> list[str]:
    problems = []
    for support in release["provider_support"]:
        if support["provider_key"].split(".", 1)[0] != release["engine_id"]:
            problems.append(f"{label}: provider {support['provider_key']} does not belong to {release['engine_id']} (RELEASE_PROVIDER_NOT_OWNED)")
        if support["capability_key"] not in catalogue:
            problems.append(f"{label}: capability {support['capability_key']} is not catalogued (RELEASE_CAPABILITY_NOT_CATALOGUED)")
    digests = [a["digest"] for a in release["artifacts"]]
    if len(digests) != len(set(digests)):
        problems.append(f"{label}: an artifact digest is listed twice")
    return problems


def derive(observation: dict, owner: dict[str, dict], engine_of: dict[str, str]) -> tuple[str, set[str]]:
    engine = engine_of.get(observation["engine_instance_id"])
    releases = set()
    for artifact in observation["artifacts"]:
        release = owner.get(artifact["digest"])
        if release is None:
            return "UNKNOWN_ARTIFACT", set()
        if release["engine_id"] != engine:
            return "FOREIGN_ARTIFACT", set()
        releases.add(release["release_id"])
    return ("RELEASE" if len(releases) == 1 else "MIXED"), releases


def cross_check(ex: dict) -> list[str]:
    problems = []
    releases = {r["release_id"]: r for r in ex.get("releases", [])}
    owner: dict[str, dict] = {}
    for release in releases.values():
        problems += support_problems(release, f"release {release['release_id']}")
        for artifact in release["artifacts"]:
            if artifact["digest"] in owner:
                problems.append(f"digest {artifact['digest']} belongs to two releases (RELEASE_ARTIFACT_DIGEST_CONFLICT)")
            owner[artifact["digest"]] = release
        if release["status"] == "APPROVED" and "provenance" not in release:
            problems.append(f"release {release['release_id']}: the examples show provenance on every approved release")
    for request in ex.get("record_requests", []):
        problems += support_problems(request, f"record request {request['release_version']}")
    engine_of = {}
    for item in ex.get("desired_releases", []):
        engine_of[item["engine_instance_id"]] = item["engine_id"]
        target = item.get("desired_release_id")
        if target is None:
            continue
        release = releases.get(target)
        if release is None:
            problems.append(f"desired release {target} is not a recorded release")
            continue
        if release["status"] not in policy["desired_state"]["readable_as_desired"]:
            problems.append(f"instance {item['engine_instance_id']} desires {target}, which is {release['status']}")
        if release["engine_id"] != item["engine_id"]:
            problems.append(f"instance {item['engine_instance_id']} desires another engine's release (RELEASE_ENGINE_MISMATCH)")
        if item["desired_release"] != release:
            problems.append(f"instance {item['engine_instance_id']}: desired_release is not the recorded release {target}")
    for request in ex.get("status_change_requests", []):
        for disposition in request.get("desired_release_dispositions", []):
            replacement = disposition.get("replacement_release_id")
            if replacement is not None and releases.get(replacement, {}).get("status") != "APPROVED":
                problems.append(f"revocation replaces with {replacement}, which is not an APPROVED release")
    observations = {o["observation_id"]: o for o in ex.get("observations", [])}
    sequences = [o["ingestion_sequence"] for o in observations.values()]
    if len(sequences) != len(set(sequences)):
        problems.append("two observations share an ingestion_sequence")
    for item in list(observations.values()) + ex.get("observation_submissions", []):
        window = (when(item["expires_at"]) - when(item["observed_at"])).total_seconds()
        if not ttl["minimum"] <= window <= ttl["maximum"]:
            problems.append(f"observation of {item['engine_instance_id']} at {item['observed_at']}: window outside TTL bounds (DEPLOYMENT_OBSERVATION_WINDOW_INVALID)")
        if item["engine_instance_id"] not in engine_of:
            problems.append(f"observation names unknown instance {item['engine_instance_id']}")
    derived_state: dict[str, tuple[str, set[str], str]] = {}
    for item in ex.get("observed_releases", []):
        if item["state"] == "UNKNOWN":
            derived_state[item["engine_instance_id"]] = ("UNKNOWN", set(), item["evaluated_at"])
            continue
        observation = observations.get(item["observation_id"])
        if observation is None or observation["engine_instance_id"] != item["engine_instance_id"]:
            problems.append(f"observed release of {item['engine_instance_id']} cites a foreign or unknown observation")
            continue
        state, ids = derive(observation, owner, engine_of)
        claimed = {item["release_id"]} if "release_id" in item else set(item.get("release_ids", []))
        if (state, ids) != (item["state"], claimed):
            problems.append(f"observed release of {item['engine_instance_id']} from {item['observation_id']} is {state} {sorted(ids)}, not {item['state']} {sorted(claimed)}")
        derived_state[item["engine_instance_id"]] = (state, ids, item["evaluated_at"])
    desired_of = {d["engine_instance_id"]: d.get("desired_release_id") for d in ex.get("desired_releases", [])}
    for record in ex.get("drift_records", []):
        accepts("drift.schema.json#/$defs/driftRecord", record, f"drift record {record['drift_record_id']}", CP_URI)
        if record["object_type"] != "ENGINE_INSTANCE_RELEASE":
            continue
        instance = record["object_reference"]
        state, ids, _ = derived_state.get(instance, ("UNKNOWN", set(), ""))
        reason = record["reason_code"]
        if reason == "REVOKED_RELEASE_RUNNING":
            ok = state == "RELEASE" and releases[next(iter(ids))]["status"] == "REVOKED"
        elif reason == "UNKNOWN_ARTIFACT_RUNNING":
            ok = state in {"UNKNOWN_ARTIFACT", "FOREIGN_ARTIFACT"}
        elif reason == "RELEASE_UNOBSERVED":
            ok = state == "UNKNOWN" and desired_of.get(instance) is not None
        elif reason == "RELEASE_MISMATCH":
            ok = state == "MIXED" or (state == "RELEASE" and ids != {desired_of.get(instance)})
        else:
            ok = True
        if not ok:
            problems.append(f"drift record {record['drift_record_id']}: {reason} does not follow from {instance}'s observed state {state}")
    return problems


example_files = sorted(p for p in (PKG / "examples").glob("*.json"))
if not example_files:
    fail("topology/v1/examples has no lifecycle example")
for path in example_files:
    example = json.loads(path.read_text())
    for kind, ref in KINDS.items():
        for index, item in enumerate(example.get(kind, [])):
            accepts(ref, item, f"{path.name} {kind}[{index}]")
    for problem in cross_check(example):
        fail(f"{path.name}: {problem}")

# 8. Negative fixtures.
base = json.loads(example_files[0].read_text()) if example_files else {}
if base:
    release = next(r for r in base["releases"] if r["status"] == "APPROVED")
    request = base["record_requests"][0]
    submission = base["observation_submissions"][0]
    observed = next(o for o in base["observed_releases"] if o["state"] == "RELEASE")
    unknown = next(o for o in base["observed_releases"] if o["state"] == "UNKNOWN")
    drift = base["drift_records"][0]
    desired = next(d for d in base["desired_releases"] if d.get("desired_release_id"))

    def variant(item, mutate):
        clone = copy.deepcopy(item)
        mutate(clone)
        return clone

    R = "release.schema.json#/$defs/"
    D = "deployment-observation.schema.json#/$defs/"
    rejects(R + "EngineRelease", variant(release, lambda r: r["artifacts"][0].pop("digest")), "a tag-only artifact")
    rejects(R + "EngineRelease", variant(release, lambda r: r["artifacts"][0].update(digest=r["artifacts"][0]["digest"].upper())), "an uppercase digest")
    rejects(R + "EngineRelease", variant(release, lambda r: r["artifacts"][0].update(digest="sha1:" + "a" * 40)), "a non-sha256 digest")
    rejects(R + "EngineRelease", variant(release, lambda r: r.update(release_version="latest")), "release_version latest")
    rejects(R + "EngineRelease", variant(release, lambda r: r.update(release_version="1.4.0+build.7")), "build metadata in release_version")
    rejects(R + "EngineRelease", variant(release, lambda r: r.update(source_revision="main")), "a branch as source_revision")
    rejects(R + "EngineRelease", variant(release, lambda r: r.update(artifacts=[])), "a release with no artifact")
    rejects(R + "EngineRelease", variant(release, lambda r: r["provider_support"][0].update(contract_versions=["v1"])), "contract version v1 as text")
    rejects(R + "EngineRelease", variant(release, lambda r: r["provider_support"][0].update(contract_versions=[0])), "contract version 0")
    rejects(R + "EngineRelease", variant(release, lambda r: r.update(status="CERTIFIED")), "a CERTIFIED release status")
    rejects(R + "EngineRelease", variant(release, lambda r: r.pop("status_reason")), "an APPROVED release without a status reason")
    rejects(R + "EngineRelease", variant(release, lambda r: r["artifacts"][0].update(repository=r["artifacts"][0]["repository"] + ":1.4.0")), "a tag in the repository")
    for field, value in (("release_id", "erl_x1"), ("status", "APPROVED"), ("recorded_by", "wl:x"), ("recorded_at", "2026-09-20T08:00:00Z")):
        rejects(R + "EngineReleaseRecordRequest", {**request, field: value}, f"a record request that supplies {field}")
    rejects(R + "EngineReleaseStatusChangeRequest", {"target_status": "REVOKED", "reason": "Withdrawn."}, "a revocation without dispositions")
    rejects(R + "EngineReleaseStatusChangeRequest", {"target_status": "CANDIDATE", "reason": "Back to candidate."}, "a move back to CANDIDATE")
    rejects(R + "EngineReleaseStatusChangeRequest", {"target_status": "DEPRECATED", "reason": "ok", "desired_release_dispositions": []}, "dispositions on a deprecation")
    rejects(R + "EngineReleaseStatusChangeRequest", {"target_status": "APPROVED", "reason": "Passed staging."}, "an approval outside the ENGINE_RELEASE_APPROVAL changeset")
    rejects(R + "desiredReleaseDisposition", {"engine_instance_id": "ei_01k9x", "action": "REPLACE"}, "a REPLACE disposition without a replacement")
    rejects(R + "EngineInstanceDesiredRelease", variant(desired, lambda d: d["desired_release"].update(status="REVOKED")), "a revoked desired release")
    rejects(R + "EngineInstanceDesiredRelease", variant(desired, lambda d: d["desired_release"].update(status="CANDIDATE")), "a candidate desired release")
    rejects(R + "EngineInstanceDesiredRelease", variant(desired, lambda d: d.pop("desired_release")), "a desired release id without its release")
    for field, value in (("source", "wl:x"), ("recorded_at", "2026-09-22T09:40:01Z"), ("ingestion_sequence", 9), ("observation_id", "dob_01k9x")):
        rejects(D + "DeploymentObservationSubmission", {**submission, field: value}, f"a submission that supplies {field}")
    rejects(D + "DeploymentObservationSubmission", variant(submission, lambda s: s["artifacts"][0].update(tag="1.4.0")), "an observed artifact named by tag")
    rejects(D + "DeploymentObservationSubmission", {**submission, "artifacts": []}, "an observation of nothing")
    rejects(D + "DeploymentObservationSubmission", {**submission, "environment": "prod"}, "an unregistered environment")
    rejects(D + "ObservedRelease", variant(observed, lambda o: o.pop("release_id")), "RELEASE without release_id")
    rejects(D + "ObservedRelease", {**unknown, "observation_id": "dob_01k9x"}, "UNKNOWN citing an observation")
    rejects(D + "ObservedRelease", {**observed, "state": "MIXED"}, "MIXED with a single release_id")
    rejects("drift.schema.json#/$defs/driftRecord", variant(drift, lambda d: d.pop("reason_code")), "release drift without a reason", CP_URI)
    rejects("drift.schema.json#/$defs/driftRecord", {**drift, "reason_code": "PROVIDER_UNAVAILABLE"}, "release drift with a foreign reason", CP_URI)
    rejects("drift.schema.json#/$defs/driftRecord", {**drift, "object_reference": "baobab-payments"}, "release drift not naming an instance", CP_URI)
    accepts("drift.schema.json#/$defs/driftRecord", {k: v for k, v in drift.items() if k != "reason_code"} | {"object_type": "TENANT", "object_reference": "tn_01k8x"}, "existing drift without reason_code", CP_URI)
    rejects("events.schema.json#/$defs/EngineInstanceReleaseDriftDetected",
            {"engine_instance_id": "ei_01k9x", "engine_id": "baobab-payments", "drift_reason": "RELEASE_UNOBSERVED",
             "desired_release_id": "erl_01k9x", "observed_state": "RELEASE", "observed_release_id": "erl_01k9y",
             "detected_at": "2026-09-22T09:40:01Z"}, "RELEASE_UNOBSERVED with an observed release")
    rejects("events.schema.json#/$defs/EngineInstanceDesiredReleaseChanged",
            {"engine_instance_id": "ei_01k9x", "engine_id": "baobab-payments", "previous_release_id": None,
             "desired_release_id": "erl_01k9x", "version": 2, "changed_at": "2026-09-22T09:40:01Z"}, "a desired release change without artifacts")

# 9. Events.
asyncapi = load_yaml(PKG / "asyncapi.yaml")
published = set()
for message in asyncapi["components"]["messages"].values():
    for part in message["payload"]["allOf"]:
        data = part.get("properties", {}).get("data", {}).get("$ref", "")
        if data.startswith("./events.schema.json#/$defs/"):
            published.add(data.rsplit("/", 1)[1])
payloads = set(json.loads((PKG / "events.schema.json").read_text())["$defs"])
if published != payloads:
    fail(f"asyncapi.yaml must publish exactly the events.schema.json payloads; differs by {sorted(published ^ payloads)}")
registry_events = {e["type"]: e for e in load_yaml(CONTRACTS / "events" / "v1" / "event-registry.yaml")["events"]}
for message in asyncapi["components"]["messages"].values():
    entry = registry_events.get(message["name"])
    if entry is None or entry.get("producer") != "baobab-cp" or entry.get("asyncapi") != "contracts/topology/v1/asyncapi.yaml":
        fail(f"{message['name']} must be registered to baobab-cp with contracts/topology/v1/asyncapi.yaml")

# 10. contracts.lock.yaml.
lock = load_yaml(ROOT / "contracts.lock.yaml")
entry = next((c for c in lock["contracts"] if c["domain"] == "topology" and c["version"] == "v1"), None)
expected = set(SCHEMAS) | {"release-policy.yaml"}
if entry is None or set(entry.get("schemas", [])) != expected:
    fail(f"contracts.lock.yaml must register topology v1 with exactly {sorted(expected)}")

# 11. Engine release routes (ER-02).
openapi = load_yaml(CP / "openapi.yaml")
paths = openapi.get("paths", {})
record = paths.get("/engine-releases", {}).get("post")
if record is None:
    fail("control-plane openapi.yaml must serve POST /engine-releases (gate ER-02)")
else:
    body = record["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    if not body.endswith("topology/v1/release.schema.json#/$defs/EngineReleaseRecordRequest"):
        fail("POST /engine-releases must accept only EngineReleaseRecordRequest")
    for code in ("200", "201"):
        returned = record["responses"][code]["content"]["application/json"]["schema"]["$ref"]
        if not returned.endswith("topology/v1/release.schema.json#/$defs/EngineRelease"):
            fail(f"POST /engine-releases {code} must return EngineRelease")
    schemes = {name: required for requirement in record["security"] for name, required in requirement.items()}
    if schemes.get("workloadOidc") != ["engine-release:record"]:
        fail("POST /engine-releases must admit workloads only under engine-release:record")
recorder = scopes.get("engine-release:record")
if recorder is None or recorder.get("allowed_actors") != ["workload"] or recorder.get("privileged"):
    fail("engine-release:record must be an unprivileged workload-only scope")
for route in ("/engine-releases", "/engine-releases/{release_id}"):
    read = paths.get(route, {}).get("get")
    if read is None or read.get("security") != [{"adminOidc": ["topology:read"]}]:
        fail(f"GET {route} must be served under topology:read")

if failures:
    for message in failures:
        print(f"topology contract validation failed: {message}", file=sys.stderr)
    sys.exit(1)
print(f"topology contracts passed ({len(example_files)} example files)")
