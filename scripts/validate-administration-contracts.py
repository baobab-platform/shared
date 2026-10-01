#!/usr/bin/env python3
"""Validate the ADR-BCP-020 administration/v1 contracts.

Real JSON Schema Draft 2020-12 validation with every cross-schema $ref
resolved against the contracts in this repository:

  1. each schema is a valid Draft 2020-12 schema whose $id matches its file;
  2. permission-registry.yaml is a sound vocabulary: unique keys in the
     permission grammar, known domains, risk classes and scope levels, and
     CRITICAL and EMERGENCY permissions never delegable (section 49);
  3. profile-registry.yaml only names registered permissions grantable at
     the profile's level, never a CRITICAL or EMERGENCY one, and there is no
     universal "admin" profile (sections 21-23);
  4. lifecycle.yaml is a sound state machine over grantStatus in which only
     ACTIVE is eligible for evaluation (sections 57-62);
  5. every example validates, and the examples obey what the schemas cannot
     say: nobody grants to themselves, a scope is one the permission allows,
     a delegation never exceeds its source in permission, scope, duration or
     depth, and denial reasons are registered;
  6. negative fixtures prove the load-bearing rules reject bad data;
  7. the control-plane OpenAPI serves EffectiveAuthority at
     /admin/effective-authority under authority:self, a non-privileged,
     human-only scope;
  8. contracts.lock.yaml registers exactly these files.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-administration-contracts.py
"""

from __future__ import annotations

import copy
import json
import sys
from collections import deque
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PKG = CONTRACTS / "administration" / "v1"
BASE_URI = "https://contracts.baobab-platform.com/administration/v1/"
SCHEMAS = ["domain.schema.json", "scope.schema.json", "grant.schema.json", "grant-administration.schema.json"]
YAMLS = ["permission-registry.yaml", "profile-registry.yaml", "lifecycle.yaml"]
RISK_ORDER = ["LOW", "MODERATE", "HIGH", "CRITICAL"]

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


def when(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


# 1. Schemas.
domain = json.loads((PKG / "domain.schema.json").read_text())["$defs"]
for name in SCHEMAS:
    schema = json.loads((PKG / name).read_text())
    Draft202012Validator.check_schema(schema)
    if schema.get("$id") != BASE_URI + name:
        fail(f"{name}: $id must be {BASE_URI + name}")

# 2. Permission registry.
permissions = {}
for entry in load_yaml(PKG / "permission-registry.yaml")["permissions"]:
    key = entry["key"]
    if key in permissions:
        fail(f"permission {key} is registered twice")
    permissions[key] = entry
    if errors("domain.schema.json#/$defs/administrativePermissionKey", key):
        fail(f"permission {key} does not match the permission grammar")
    if entry["domain"] not in domain["permissionDomain"]["enum"]:
        fail(f"permission {key} has unknown domain {entry['domain']}")
    if entry["risk_class"] not in domain["riskClass"]["enum"]:
        fail(f"permission {key} has unknown risk class {entry['risk_class']}")
    if not entry["scope_levels"] or any(l not in domain["scopeLevel"]["enum"] for l in entry["scope_levels"]):
        fail(f"permission {key} must name known scope levels")
    if entry["delegable"] and (entry["risk_class"] == "CRITICAL" or entry["domain"] == "EMERGENCY"):
        fail(f"permission {key} is {entry['risk_class']}/{entry['domain']} and must not be delegable (section 49)")
    if entry["read_only"] != key.endswith(".view"):
        fail(f"permission {key}: read_only must be true exactly for .view permissions")

# 3. Profiles.
profiles = {}
for profile in load_yaml(PKG / "profile-registry.yaml")["profiles"]:
    key = profile["key"]
    profiles[key] = profile
    if key in ("admin", "administrator", "super-admin", "superuser"):
        fail(f"profile {key}: no universal admin profile (section 23)")
    if errors("domain.schema.json#/$defs/administrativeProfileKey", key):
        fail(f"profile {key} does not match the profile grammar")
    if len(set(profile["permissions"])) != len(profile["permissions"]):
        fail(f"profile {key} repeats a permission")
    for permission in profile["permissions"]:
        entry = permissions.get(permission)
        if entry is None:
            fail(f"profile {key} names unregistered permission {permission}")
            continue
        if profile["scope_level"] not in entry["scope_levels"]:
            fail(f"profile {key} grants {permission} at {profile['scope_level']}, which it may not be granted at")
        if entry["risk_class"] == "CRITICAL" or entry["domain"] == "EMERGENCY":
            fail(f"profile {key} would confer standing {permission}; CRITICAL and EMERGENCY authority is granted explicitly")

# 4. Lifecycle.
lifecycle = load_yaml(PKG / "lifecycle.yaml")
states = set(domain["grantStatus"]["enum"])
transitions = lifecycle["transitions"]
named = {t["from"] for t in transitions} | {t["to"] for t in transitions} | {lifecycle["initial"]} | set(lifecycle["terminal"])
if named != states:
    fail(f"lifecycle.yaml states {sorted(named)} differ from grantStatus {sorted(states)}")
for t in transitions:
    if t["from"] in lifecycle["terminal"]:
        fail(f"lifecycle.yaml leaves terminal state {t['from']}")
reached, queue = {lifecycle["initial"]}, deque([lifecycle["initial"]])
while queue:
    state = queue.popleft()
    for t in transitions:
        if t["from"] == state and t["to"] not in reached:
            reached.add(t["to"])
            queue.append(t["to"])
if reached != states:
    fail(f"lifecycle.yaml cannot reach {sorted(states - reached)}")
if lifecycle["eligible_for_evaluation"] != ["ACTIVE"]:
    fail("lifecycle.yaml: only ACTIVE is eligible for evaluation (section 59)")

# 5. Examples.
examples = json.loads((PKG / "examples" / "administrative-grants.json").read_text())
grants = {g["grant_id"]: g for g in examples["grants"]}
for grant in examples["grants"]:
    gid = grant["grant_id"]
    for problem in errors("grant.schema.json#/$defs/AdministrativeGrant", grant):
        fail(f"example {gid}: {problem}")
    if grant["granted_by"] == grant["principal_id"]:
        fail(f"example {gid}: a principal never grants to themselves (section 39)")
    if "valid_until" in grant and when(grant["valid_until"]) <= when(grant["valid_from"]):
        fail(f"example {gid}: valid_until must be later than valid_from")
    entry = permissions.get(grant["permission"])
    if entry is None:
        fail(f"example {gid}: permission {grant['permission']} is not registered")
        continue
    if grant["scope"]["level"] not in entry["scope_levels"]:
        fail(f"example {gid}: {grant['permission']} may not be granted at {grant['scope']['level']}")
    if RISK_ORDER.index(grant["risk_class"]) < RISK_ORDER.index(entry["risk_class"]):
        fail(f"example {gid}: risk_class is below the permission's {entry['risk_class']}")
    if grant["source"] == "PROFILE" and grant["permission"] not in profiles.get(grant["profile_key"], {}).get("permissions", []):
        fail(f"example {gid}: profile {grant['profile_key']} does not include {grant['permission']}")
    if grant["source"] == "DELEGATION":
        source = grants.get(grant["delegated_from_grant_id"])
        if source is None:
            fail(f"example {gid}: delegates from an unknown grant")
            continue
        if not permissions[source["permission"]]["delegable"] or source.get("delegable_depth", 0) < grant["delegation_depth"]:
            fail(f"example {gid}: its source does not allow delegation this deep (section 48)")
        if grant["permission"] != source["permission"] or grant["scope"] != source["scope"]:
            fail(f"example {gid}: a delegation never widens permission or scope (sections 43-45)")
        if grant["granted_by"] != source["principal_id"]:
            fail(f"example {gid}: only the source grant's holder delegates it")
        if "valid_until" in source and ("valid_until" not in grant or when(grant["valid_until"]) > when(source["valid_until"])):
            fail(f"example {gid}: a delegation never outlives its source (section 46)")

reason_codes = {
    e["code"] for e in load_yaml(CONTRACTS / "authorization" / "v1" / "reason-code-registry.yaml")["reason_codes"]
    if e["category"] == "administrative_denial"
}
for decision in examples["decisions"]:
    did = decision["decision_id"]
    for problem in errors("grant.schema.json#/$defs/AdministrativeDecision", decision):
        fail(f"example {did}: {problem}")
    for code in decision["reason_codes"]:
        if code not in reason_codes:
            fail(f"example {did}: {code} is not registered under administrative_denial")
    for gid in decision["matched_grants"]:
        matched = grants.get(gid)
        if matched and (matched["permission"] != decision["action"] or matched["principal_id"] != decision["principal_id"]):
            fail(f"example {did}: matched grant {gid} does not grant this action to this principal")
authority = examples["effective_authority"]
for problem in errors("grant.schema.json#/$defs/EffectiveAuthority", authority):
    fail(f"example effective_authority: {problem}")
for g in authority["grants"]:
    if g.get("elevated") != (g["grant_type"] == "JUST_IN_TIME"):
        fail(f"example effective_authority: {g['grant_id']} elevated must be true exactly for JUST_IN_TIME grants")
    source = grants.get(g["grant_id"])
    if source is None or source["status"] != "ACTIVE" or source["principal_id"] != authority["principal_id"]:
        fail(f"example effective_authority: {g['grant_id']} is not an ACTIVE grant of this principal")
jit = [when(g["valid_until"]) for g in authority["grants"] if g["grant_type"] == "JUST_IN_TIME"]
if jit and ("elevated_until" not in authority or when(authority["elevated_until"]) != min(jit)):
    fail("example effective_authority: elevated_until must be the earliest JUST_IN_TIME valid_until")

# 6. Negative fixtures.
tenant_grant = grants["agr_01k7tenantadmin"]
bootstrap = grants["agr_01k7bootstrap"]
revoked = grants["agr_01k7groupstatic"]


def must_reject(label: str, ref: str, instance) -> None:
    if not errors(ref, instance):
        fail(f"negative fixture accepted: {label}")


def mutate(base, **changes):
    out = copy.deepcopy(base)
    for key, value in changes.items():
        if value is None:
            out.pop(key, None)
        else:
            out[key] = value
    return out


G = "grant.schema.json#/$defs/AdministrativeGrant"
S = "scope.schema.json#/$defs/AdministrativeScope"
must_reject("a STANDING grant with valid_until", G, mutate(tenant_grant, valid_until="2027-01-01T00:00:00Z"))
must_reject("a TIME_BOUND grant without valid_until", G, mutate(tenant_grant, grant_type="TIME_BOUND"))
must_reject("a STANDING bootstrap grant", G, mutate(bootstrap, grant_type="STANDING", valid_until=None))
must_reject("a bootstrap grant below platform scope", G, mutate(bootstrap, scope={"level": "TENANT", "tenant_id": "tn_acmeug"}))
must_reject("a PROFILE grant without its profile", G, mutate(tenant_grant, profile_key=None))
must_reject("a DELEGATION grant without its source", G, mutate(tenant_grant, source="DELEGATION", profile_key=None))
must_reject("a REVOKED grant without who revoked it", G, mutate(revoked, revoked_by=None))
must_reject("an ACTIVE grant carrying revocation", G, mutate(revoked, status="ACTIVE"))
must_reject("a grant naming its grantee by email", G, mutate(tenant_grant, principal_id="jane@acme.example"))
must_reject("a scope with no anchor", S, {"level": "TENANT"})
must_reject("a tenant scope also naming an organisation", S, {"level": "TENANT", "tenant_id": "tn_acmeug", "organisation_id": "ORG-ACME"})
must_reject("a platform scope naming a tenant", S, {"level": "PLATFORM", "tenant_id": "tn_acmeug"})
must_reject("STATIC_MEMBERSHIP without its organisations", S, {"level": "CORPORATE_GROUP", "corporate_group_id": "cgrp_acme", "mode": "STATIC_MEMBERSHIP"})
must_reject("a group mode outside a corporate group", S, {"level": "ORGANISATION", "organisation_id": "ORG-ACME", "mode": "DYNAMIC_GROUP_DESCENDANTS"})
must_reject("organisation_ids without STATIC_MEMBERSHIP", S, {"level": "CORPORATE_GROUP", "corporate_group_id": "cgrp_acme", "organisation_ids": ["ORG-ACME"]})
allow = examples["decisions"][0]
deny = examples["decisions"][1]
D = "grant.schema.json#/$defs/AdministrativeDecision"
must_reject("ALLOW without a matched grant", D, mutate(allow, matched_grants=[]))
must_reject("ALLOW with a reason", D, mutate(allow, reason_codes=["SCOPE_MISMATCH"]))
must_reject("DENY without a reason", D, mutate(deny, reason_codes=[]))
must_reject("DENY naming matched grants", D, mutate(deny, matched_grants=["agr_01k7tenantadmin"]))
must_reject("STEP_UP_REQUIRED without the step-up obligation", D, mutate(examples["decisions"][2], obligations=[]))
must_reject("an effective grant exposing who granted it", "grant.schema.json#/$defs/EffectiveAuthority",
            mutate(authority, grants=[dict(authority["grants"][0], granted_by="prn_platformops")]))

# 6b. Metrics: the catalogue's labels are closed, and the permission label
#     can only take registered keys or "unregistered", so series stay bounded.
if domain["administrativeMetricLabel"]["enum"] != ["permission", "legacy", "grants", "agreement"]:
    fail("administrativeMetricLabel must be exactly permission, legacy, grants and agreement")
for name in domain["administrativeMetric"]["enum"]:
    if not name.endswith("_total") or errors("domain.schema.json#/$defs/administrativeMetric", name):
        fail(f"metric {name} must be a counter name ending _total")
outcome_labels = {"ALLOW": "allow", "DENY": "deny", "STEP_UP_REQUIRED": "step_up",
                  "APPROVAL_REQUIRED": "approval_required", "NOT_READY": "not_ready"}
if set(outcome_labels) != set(domain["decisionOutcome"]["enum"]):
    fail("every decisionOutcome needs a shadowGrantsOutcome label")
for outcome, label in outcome_labels.items():
    if label not in domain["shadowGrantsOutcome"]["enum"]:
        fail(f"decisionOutcome {outcome} has no shadowGrantsOutcome label {label}")
if "unregistered" in permissions:
    fail("unregistered is reserved as the permission label of an unmapped route")

# 7. OpenAPI and scope.
openapi = load_yaml(CONTRACTS / "control-plane" / "v1" / "openapi.yaml")
operation = openapi["paths"].get("/admin/effective-authority", {}).get("get")
if operation is None:
    fail("control-plane openapi.yaml does not serve GET /admin/effective-authority")
else:
    schema_ref = operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    if schema_ref != "../../administration/v1/grant.schema.json#/$defs/EffectiveAuthority":
        fail(f"GET /admin/effective-authority returns {schema_ref}, not EffectiveAuthority")
    if operation["security"] != [{"adminOidc": ["authority:self"]}]:
        fail("GET /admin/effective-authority must require adminOidc authority:self")
scopes = {s["name"]: s for s in load_yaml(CONTRACTS / "authorization" / "v1" / "scope-registry.yaml")["scopes"]}
self_scope = scopes.get("authority:self")
if self_scope is None or self_scope.get("allowed_actors") != ["human"] or self_scope.get("privileged"):
    fail("authority:self must be registered for humans only and must not be privileged")

# 8. Lock file.
lock = load_yaml(ROOT / "contracts.lock.yaml")
entry = next((c for c in lock["contracts"] if c["domain"] == "administration" and c["version"] == "v1"), None)
expected = sorted(SCHEMAS + YAMLS)
if entry is None or sorted(entry["schemas"]) != expected:
    fail(f"contracts.lock.yaml must register administration v1 as exactly {expected}")

if failures:
    for message in failures:
        print(f"administration contract validation failed: {message}", file=sys.stderr)
    sys.exit(1)
print("Administration contract validation passed")
