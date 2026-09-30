#!/usr/bin/env python3
"""Canonical Capability Catalogue and provider declaration tooling (ADR-SHARED-017, EA-02).

One tool, three uses:

  validate-catalogue
      Shared CI. The catalogue (contracts/capability/v1/catalogue.yaml) is
      the only index of canonical capabilities. Checks that it is sorted and
      duplicate free; every entry resolves to exactly one definition in its
      source document with the same owner; every definition validates
      (Draft 2020-12), sits in a registered domain whose key names no
      vendor, tenant, country or region, and has contract majors whose
      request, response, error and event schemas resolve; every dependency
      targets a catalogued capability and REQUIRED dependencies are acyclic;
      and no capability definition exists anywhere in contracts/ that the
      catalogue does not index, whatever its file name or serialization.
      It also checks the transitional EngineRegistration bundles against
      registration-bundles.yaml and the catalogue, validates the shipped
      provider-declaration example, and proves that example regenerates the
      Payments bundle.

  validate-declaration PATH [--repository-root DIR] [--engine-id ID] [--template]
      Engine and Foundation CI. Validates an engine's
      .baobab/capability-provider.yaml against provider-declaration.schema.json
      and against this Shared checkout's catalogue: known capabilities and
      contract majors only, provider keys owned by the engine, no duplicate
      support, logical invocation for the engine only, planned capabilities
      kept apart from implemented support, and evidence paths that exist in
      the repository. --template first substitutes the placeholder
      vocabulary used by baobab-platform/engine-template.

  generate-registration PATH --provider-key KEY [--provider-lifecycle L]
      Transitional compatibility (ADR-SHARED-017 SS32). Generates the
      capability/v1 EngineRegistration the Control Plane ingests today from
      the canonical definitions plus one provider of a declaration. Only
      IMPLEMENTED support is registered; PARTIAL support and planned
      capabilities never are. The provider lifecycle defaults to DRAFT
      (SS33); pass ACTIVE only to reproduce today's bootstrap bundles.

A provider declaration never certifies, activates, binds, grants or reports
health; nothing here infers any of those facts from it.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/capability_catalogue.py validate-catalogue
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
BASE = "https://contracts.baobab-platform.com/"
CATALOGUE = "capability/v1/catalogue.yaml"
BUNDLE_INDEX = "capability/v1/registration-bundles.yaml"
DECLARATION_EXAMPLE = "capability/v1/examples/provider-declaration.yaml"

CATALOGUE_REF = "capability/v1/catalogue.schema.json#/$defs/CapabilityCatalogue"
DEFINITIONS_REF = "capability/v1/capability.schema.json#/$defs/CapabilityDefinitionDocument"
DECLARATION_REF = "capability/v1/provider-declaration.schema.json#/$defs/CapabilityProviderDeclaration"
REGISTRATION_REF = "capability/v1/registration.schema.json#/$defs/EngineRegistration"
BUNDLE_INDEX_REF = "capability/v1/registration.schema.json#/$defs/RegistrationBundleIndex"
DEFINITIONS_NAME = "baobab-capability-definitions"

# Capability identity survives provider replacement and serves tenants not
# yet onboarded, so keys never name any of these (ADR-SHARED-017 SS14,
# namespace-registry.yaml). Checked per dot/hyphen token; extend as the
# estate grows. A geographic token that is inherently semantic needs an
# architecture decision and an explicit exception here, not a quiet edit.
VENDOR_TOKENS = {"medusa", "medusajs", "idempiere", "payload", "haystack", "keycloak", "ory", "kratos", "hydra",
                 "hyperswitch", "killbill", "stripe", "opa", "frappe", "erpnext", "sandbox"}
TENANT_TOKENS = {"zuribeans", "thamani", "nabhold", "equator"}
GEOGRAPHIC_TOKENS = {"uganda", "kenya", "tanzania", "rwanda", "burundi", "ethiopia", "nigeria", "ghana", "egypt",
                     "africa", "europe", "asia", "america", "emea", "apac", "eu", "uk", "usa", "china", "india"}
GEOGRAPHIC_EXCEPTIONS: set[str] = set()

# The Control Plane-owned and EA-09-owned facts a declaration must never
# carry (ADR-SHARED-017 SS21, SS26, SS50-52). The schema already rejects
# them; naming them gives an actionable message.
FORBIDDEN_DECLARATION_FIELDS = {
    "certified", "certification", "certification_status", "lifecycle", "status", "active", "health",
    "health_status", "binding", "bindings", "grant", "grants", "entitlement", "entitlements", "tenant",
    "tenants", "engine_instance", "engine_instances", "instances", "release", "engine_release", "routing",
    "endpoint", "host", "hostname", "url", "credentials", "secret", "secrets",
}

# Substitutions for baobab-platform/engine-template's placeholders. Capability
# placeholders take the first catalogued capability and its first major, so a
# template is validated against real canonical vocabulary.
TEMPLATE_PLACEHOLDERS = {
    "<engine-id>": "baobab-example",
    "<provider-name>": "example",
    "<implementation-key>": "example-technology",
    "<provider-display-name>": "Example provider",
    "<service-name>": "example",
    "<owning-repository>": "baobab-platform/baobab-example",
    "<governing-adr>": "ADR-EXAMPLE-0001",
    "<proposed-capability-key>": "example.resource.act",
    "<evidence-path>": "src/example",
}
PLACEHOLDER = re.compile(r"<[a-z][a-z0-9-]*>")
OWNER = re.compile(r"^baobab-[a-z0-9]+(?:-[a-z0-9]+)*$")

FORMATS = FormatChecker()


def load_document(path: Path):
    text = path.read_text()
    return json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)


def contract_documents(contracts: Path):
    """Every parseable JSON/YAML document under contracts/, keyed by its path relative to contracts/."""
    for path in sorted(contracts.rglob("*")):
        if path.suffix not in {".json", ".yaml", ".yml"} or not path.is_file():
            continue
        try:
            yield path.relative_to(contracts).as_posix(), load_document(path)
        except (json.JSONDecodeError, yaml.YAMLError):
            continue


def build_registry(contracts: Path) -> Registry:
    registry = Registry()
    for path in sorted(contracts.rglob("*.json")):
        try:
            document = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if isinstance(document, dict) and isinstance(document.get("$id"), str):
            registry = registry.with_resource(document["$id"], Resource.from_contents(document))
    return registry


class Contracts:
    """A Shared contracts/ tree: its schema registry and canonical catalogue."""

    def __init__(self, root: Path = CONTRACTS):
        self.root = root
        self.registry = build_registry(root)
        self._definitions: dict[str, tuple[dict, str]] | None = None

    def errors(self, ref: str, instance: object) -> list[str]:
        validator = Draft202012Validator({"$ref": BASE + ref}, registry=self.registry, format_checker=FORMATS)
        return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
                for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))]

    def resolves(self, base_rel: str, ref: str) -> bool:
        try:
            self.registry.resolver(base_uri=BASE + base_rel).lookup(ref)
        except Exception:  # noqa: BLE001 - any resolution failure is a dangling reference
            return False
        return True

    def domains(self) -> tuple[set[str], set[str]]:
        registered = {entry["key"] for entry in load_document(self.root / "capability/v1/namespace-registry.yaml")["domains"]}
        enum = set(json.loads((self.root / "capability/v1/domain.schema.json").read_text())["$defs"]["capabilityDomain"]["enum"])
        return registered, enum

    def definitions(self) -> dict[str, tuple[dict, str]]:
        """Catalogued capability_key -> (canonical definition, source path under contracts/). Assumes a valid catalogue."""
        if self._definitions is None:
            catalogue = load_document(self.root / CATALOGUE)
            found: dict[str, tuple[dict, str]] = {}
            for entry in catalogue["capabilities"]:
                source = source_rel(entry["source"])
                for definition in load_document(self.root / source)["capabilities"]:
                    if definition["capability_key"] == entry["capability_key"]:
                        found[entry["capability_key"]] = (definition, source)
            self._definitions = found
        return self._definitions


def source_rel(source: str) -> str:
    """A catalogue source (relative to capability/v1/) as a path under contracts/."""
    parts: list[str] = ["capability", "v1"]
    for part in PurePosixPath(source).parts:
        if part == "..":
            if not parts:
                raise ValueError(f"{source} escapes contracts/")
            parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts)


def key_tokens(key: str) -> set[str]:
    return set(re.split(r"[.-]", key))


def key_identity_errors(key: str) -> list[str]:
    tokens = key_tokens(key)
    problems = []
    for label, denied in (("vendor/provider", VENDOR_TOKENS), ("tenant", TENANT_TOKENS)):
        if tokens & denied:
            problems.append(f"{key} names {label} identity {sorted(tokens & denied)}")
    geographic = (tokens & GEOGRAPHIC_TOKENS) - GEOGRAPHIC_EXCEPTIONS
    if geographic:
        problems.append(f"{key} names country/region identity {sorted(geographic)} without an approved exception")
    return problems


def required_cycles(definitions: dict[str, tuple[dict, str]]) -> list[list[str]]:
    graph = {key: [d["capability_key"] for d in definition.get("dependencies", []) if d["dependency_type"] == "REQUIRED"]
             for key, (definition, _) in definitions.items()}
    cycles, state = [], {}

    def visit(node: str, stack: list[str]) -> None:
        state[node] = "open"
        for target in graph.get(node, []):
            if state.get(target) == "open":
                cycles.append(stack[stack.index(target):] + [target] if target in stack else [node, target])
            elif target in graph and target not in state:
                visit(target, stack + [target])
        state[node] = "done"

    for node in sorted(graph):
        if node not in state:
            visit(node, [node])
    return cycles


def validate_catalogue(contracts: Contracts) -> list[str]:
    failures: list[str] = []
    catalogue_path = contracts.root / CATALOGUE
    if not catalogue_path.is_file():
        return [f"contracts/{CATALOGUE} is missing"]
    catalogue = load_document(catalogue_path)
    schema_errors = contracts.errors(CATALOGUE_REF, catalogue)
    if schema_errors:
        return [f"contracts/{CATALOGUE}: {e}" for e in schema_errors]

    entries = catalogue["capabilities"]
    keys = [entry["capability_key"] for entry in entries]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        failures.append(f"catalogue lists {duplicates} more than once")
    if keys != sorted(keys):
        failures.append("catalogue entries must be sorted by capability_key")

    registered, enum = contracts.domains()
    if registered != enum:
        failures.append("namespace-registry.yaml and domain.schema.json capabilityDomain must declare identical domains")

    # Load each source document once; every definition in it is accounted for.
    sources: dict[str, list[dict]] = {}
    for entry in entries:
        try:
            rel = source_rel(entry["source"])
        except ValueError as error:
            failures.append(f"catalogue entry {entry['capability_key']}: {error}")
            continue
        if rel in sources:
            continue
        path = contracts.root / rel
        if not path.is_file():
            failures.append(f"catalogue entry {entry['capability_key']}: source {entry['source']} does not exist")
            sources[rel] = []
            continue
        document = load_document(path)
        errors = contracts.errors(DEFINITIONS_REF, document)
        if errors:
            failures.extend(f"contracts/{rel}: {e}" for e in errors)
            sources[rel] = []
            continue
        sources[rel] = document["capabilities"]

    defined_at: dict[str, list[str]] = {}
    for rel, definitions in sources.items():
        for definition in definitions:
            defined_at.setdefault(definition["capability_key"], []).append(rel)

    # Definitions anywhere in contracts/, found by content rather than name,
    # so a definition cannot hide from the catalogue in an unindexed file.
    for rel, document in contract_documents(contracts.root):
        if rel in sources or not isinstance(document, dict):
            continue
        if isinstance(document.get("schema"), dict) and document["schema"].get("name") == DEFINITIONS_NAME:
            failures.append(f"contracts/{rel} defines capabilities but is not a catalogue source")
            for definition in document.get("capabilities") or []:
                if isinstance(definition, dict) and "capability_key" in definition:
                    defined_at.setdefault(definition["capability_key"], []).append(rel)
        elif not is_registration_bundle(document) and rel != CATALOGUE and has_capability_list(document):
            failures.append(f"contracts/{rel} lists capabilities in an unrecognised manifest shape; canonical "
                            "definitions use capability.schema.json#/$defs/CapabilityDefinitionDocument")

    by_key = {entry["capability_key"]: entry for entry in entries}
    for key, places in sorted(defined_at.items()):
        if len(places) > 1:
            failures.append(f"{key} is defined more than once: {sorted(places)}")
        if key not in by_key:
            failures.append(f"{key} is defined in {sorted(set(places))} but not indexed by the catalogue")

    definitions: dict[str, tuple[dict, str]] = {}
    for key, entry in by_key.items():
        try:
            rel = source_rel(entry["source"])
        except ValueError:
            continue
        matches = [d for d in sources.get(rel, []) if d["capability_key"] == key]
        if sources.get(rel) and not matches:
            failures.append(f"catalogue entry {key} does not resolve: {entry['source']} does not define it")
        if matches:
            definitions[key] = (matches[0], rel)
            failures.extend(definition_errors(contracts, matches[0], rel, entry, registered, set(by_key)))

    for cycle in required_cycles(definitions):
        failures.append(f"REQUIRED capability dependencies form a cycle: {' -> '.join(cycle)}")
    return failures


def has_capability_list(document: dict) -> bool:
    items = document.get("capabilities")
    return isinstance(items, list) and any(isinstance(item, dict) and "capability_key" in item for item in items)


def is_registration_bundle(document: object) -> bool:
    return isinstance(document, dict) and {"repository", "capabilities", "provider", "support"} <= set(document)


def definition_errors(contracts: Contracts, definition: dict, rel: str, entry: dict, registered: set[str],
                      catalogued: set[str]) -> list[str]:
    key = definition["capability_key"]
    failures = []
    if definition["owner"] != entry["owner"]:
        failures.append(f"{key}: catalogue owner {entry['owner']} differs from its definition's owner {definition['owner']}")
    if not OWNER.match(definition["owner"]) or key_tokens(definition["owner"]) & VENDOR_TOKENS:
        failures.append(f"{key}: owner {definition['owner']!r} is not a Baobab engine/service repository")
    domain = key.split(".")[0]
    if domain != definition["domain"]:
        failures.append(f"{key}: key domain {domain} differs from its declared domain {definition['domain']}")
    if domain not in registered:
        failures.append(f"{key}: domain {domain} is not registered in namespace-registry.yaml")
    failures.extend(key_identity_errors(key))
    majors = [contract["major"] for contract in definition["contracts"]]
    if len(majors) != len(set(majors)):
        failures.append(f"{key}: contract majors {majors} are not unique")
    for contract in definition["contracts"]:
        refs = [("request_schema", contract["request_schema"]), ("response_schema", contract["response_schema"])]
        if "error_schema" in contract:
            refs.append(("error_schema", contract["error_schema"]))
        refs += [("event_schema", ref) for ref in contract.get("event_schemas", [])]
        for label, ref in refs:
            if not contracts.resolves(rel, ref):
                failures.append(f"{key}@{contract['major']}: {label} {ref!r} does not resolve")
    for dependency in definition.get("dependencies", []):
        if dependency["capability_key"] not in catalogued:
            failures.append(f"{key}: depends on {dependency['capability_key']}, which is not catalogued")
        if dependency["capability_key"] == key:
            failures.append(f"{key}: depends on itself")
    return failures


# The fields an EngineRegistration carries for each capability.
BUNDLE_CAPABILITY_FIELDS = ("capability_key", "name", "description", "domain", "owner", "lifecycle", "maturity",
                            "contracts", "data_classification")


def bundle_capability(definition: dict) -> dict:
    return {field: definition[field] for field in BUNDLE_CAPABILITY_FIELDS if field in definition}


def validate_bundles(contracts: Contracts) -> list[str]:
    """The transitional EngineRegistration bundles agree with their index and with the catalogue."""
    failures: list[str] = []
    index_path = contracts.root / BUNDLE_INDEX
    if not index_path.is_file():
        return [f"contracts/{BUNDLE_INDEX} is missing"]
    index = load_document(index_path)
    errors = contracts.errors(BUNDLE_INDEX_REF, index)
    if errors:
        return [f"contracts/{BUNDLE_INDEX}: {e}" for e in errors]
    indexed = {bundle["path"]: bundle for bundle in index["bundles"]}
    if len(indexed) != len(index["bundles"]):
        failures.append(f"contracts/{BUNDLE_INDEX} lists a bundle more than once")
    found = {rel for rel, document in contract_documents(contracts.root) if is_registration_bundle(document)}
    for rel in sorted(found - set(indexed)):
        failures.append(f"contracts/{rel} is an EngineRegistration bundle not listed in {BUNDLE_INDEX}")
    definitions = contracts.definitions()
    for rel, entry in sorted(indexed.items()):
        path = contracts.root / rel
        if not path.is_file():
            failures.append(f"{BUNDLE_INDEX}: bundle {rel} does not exist")
            continue
        bundle = load_document(path)
        errors = contracts.errors(REGISTRATION_REF, bundle)
        if errors:
            failures.extend(f"contracts/{rel}: {e}" for e in errors)
            continue
        if bundle["repository"] != entry["engine_id"] or bundle["provider"]["ownership"] != entry["engine_id"]:
            failures.append(f"contracts/{rel}: repository and provider ownership must be {entry['engine_id']}")
        if bundle["provider"]["provider_key"] != entry["provider_key"]:
            failures.append(f"contracts/{rel}: provider {bundle['provider']['provider_key']} is indexed as {entry['provider_key']}")
        if not bundle["provider"]["provider_key"].startswith(entry["engine_id"] + "."):
            failures.append(f"contracts/{rel}: provider {bundle['provider']['provider_key']} does not belong to {entry['engine_id']}")
        for capability in bundle["capabilities"]:
            key = capability["capability_key"]
            if key not in definitions:
                failures.append(f"contracts/{rel}: registers {key}, which is not in the canonical catalogue")
            elif capability != bundle_capability(definitions[key][0]):
                failures.append(f"contracts/{rel}: {key} differs from its canonical definition in "
                                f"contracts/{definitions[key][1]}")
        for support in bundle["support"]:
            key = support["capability_key"]
            if key not in definitions:
                failures.append(f"contracts/{rel}: provider supports {key}, which is not in the canonical catalogue")
                continue
            majors = {c["major"] for c in definitions[key][0]["contracts"]}
            if not set(support["contract_versions"]) <= majors:
                failures.append(f"contracts/{rel}: {key} contract versions {support['contract_versions']} exceed {sorted(majors)}")
    return failures


def substitute_template(text: str, contracts: Contracts) -> str:
    catalogue = load_document(contracts.root / CATALOGUE)
    first = catalogue["capabilities"][0]["capability_key"]
    definition = contracts.definitions()[first][0]
    values = dict(TEMPLATE_PLACEHOLDERS, **{"<canonical-capability-key>": first,
                                            "<contract-major>": str(definition["contracts"][0]["major"])})
    for placeholder, value in values.items():
        text = text.replace(placeholder, value)
    return text


def walk_keys(node: object, path: str = ""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield f"{path}/{key}", key
            yield from walk_keys(value, f"{path}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_keys(value, f"{path}/{index}")


def walk_strings(node: object):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(key)
            yield from walk_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_strings(value)


def validate_declaration(contracts: Contracts, declaration: object, repository_root: Path | None = None,
                         engine_id: str | None = None) -> list[str]:
    failures = [f"{path} is not a provider declaration's to state (owned by the Control Plane, EA-09 or runtime observation)"
                for path, key in walk_keys(declaration) if key in FORBIDDEN_DECLARATION_FIELDS]
    errors = contracts.errors(DECLARATION_REF, declaration)
    if errors or failures:
        return failures + [f"schema: {e}" for e in errors]

    engine = declaration["engine"]["engine_id"]
    if engine_id is not None and engine != engine_id:
        failures.append(f"engine.engine_id {engine} is not this repository's engine id {engine_id}")
    definitions = contracts.definitions()
    providers = declaration.get("providers", [])
    provider_keys = [provider["provider_key"] for provider in providers]
    for key in sorted({k for k in provider_keys if provider_keys.count(k) > 1}):
        failures.append(f"provider {key} is declared more than once")

    supported: set[str] = set()
    for provider in providers:
        key = provider["provider_key"]
        if key.split(".")[0] != engine:
            failures.append(f"provider {key} does not belong to engine {engine}: provider keys are <engine-id>.<provider-name>")
        invocation = provider.get("invocation")
        if invocation and invocation["service_reference"][len("service://"):].split("/")[0] != engine:
            failures.append(f"provider {key}: service reference {invocation['service_reference']} must name engine {engine}")
        seen: set[str] = set()
        for support in provider["support"]:
            capability = support["capability_key"]
            if capability in seen:
                failures.append(f"provider {key} declares support for {capability} more than once")
            seen.add(capability)
            supported.add(capability)
            if capability not in definitions:
                failures.append(f"provider {key} claims {capability}, which is not a canonical Shared capability; "
                                "propose it under planned_capabilities instead")
                continue
            majors = {c["major"] for c in definitions[capability][0]["contracts"]}
            unknown = sorted(set(support["contract_versions"]) - majors)
            if unknown:
                failures.append(f"provider {key}: {capability} has no contract major {unknown} (Shared defines {sorted(majors)})")
            for evidence in support.get("implementation_evidence", []):
                failures.extend(evidence_errors(key, capability, evidence["path"], repository_root))

    proposed = [plan.get("proposed_key") for plan in declaration.get("planned_capabilities", []) if plan.get("proposed_key")]
    for key in sorted({k for k in proposed if proposed.count(k) > 1}):
        failures.append(f"planned capability {key} is declared more than once")
    for plan in declaration.get("planned_capabilities", []):
        target = plan.get("target_provider_key")
        if target and target.split(".")[0] != engine:
            failures.append(f"planned capability target provider {target} does not belong to engine {engine}")
        if "proposed_key" in plan and plan["proposed_key"] in definitions:
            failures.append(f"planned {plan['proposed_key']} is already canonical: declare it CONTRACTED by capability_key, "
                            "or as provider support once implemented")
        if "capability_key" in plan:
            if plan["capability_key"] not in definitions:
                failures.append(f"planned CONTRACTED {plan['capability_key']} is not a canonical Shared capability")
            if plan["capability_key"] in supported:
                failures.append(f"{plan['capability_key']} is both planned and supported; a planned capability is never runtime support")
    return failures


DECLARATION_PATH = ".baobab/capability-provider.yaml"
REPOSITORY_CONTRACT_PATH = ".baobab/repository.yaml"
POLICY_MODES = ("warn", "enforce")


def declaration_policy(repository_contract: dict, declaration: object | None) -> list[str]:
    """G-FCI-1 lifecycle policy (ADR-SHARED-017; G-FCI-1 decision, 2026-09-30).

    An active repository with the Foundation engine trait must declare what it
    provides; an experimental engine may declare planned capabilities only.
    A repository without the engine trait has nothing to declare here.
    Validity of a declaration that exists is validate_declaration's job.
    """
    lifecycle = (repository_contract.get("repository") or {}).get("lifecycle")
    if "engine" not in (repository_contract.get("capabilities") or []):
        return []
    findings = []
    if lifecycle == "active" and declaration is None:
        findings.append(f"{DECLARATION_PATH} is required: this repository is an active engine "
                        "(repository.lifecycle: active with the engine trait). Declare what it provides, "
                        "or classify it experimental until it does")
    if lifecycle == "experimental" and isinstance(declaration, dict) and declaration.get("providers"):
        findings.append(f"{DECLARATION_PATH} declares provider support, but this engine is experimental: "
                        "an experimental engine declares planned_capabilities only. Promote the repository "
                        "to lifecycle active once its support is real, or move the support to planned capabilities")
    return findings


def evidence_errors(provider: str, capability: str, path: str, repository_root: Path | None) -> list[str]:
    if repository_root is None:
        return []
    root = repository_root.resolve()
    target = (root / path).resolve()
    if root not in target.parents and target != root:
        return [f"provider {provider}: {capability} evidence {path} escapes the repository"]
    if not target.exists():
        return [f"provider {provider}: {capability} evidence {path} does not exist in the repository"]
    return []


def generate_registration(contracts: Contracts, declaration: dict, provider_key: str,
                          provider_lifecycle: str = "DRAFT") -> dict:
    """The transitional EngineRegistration for one declared provider (ADR-SHARED-017 SS32-33)."""
    errors = validate_declaration(contracts, declaration)
    if errors:
        raise ValueError("declaration is invalid: " + "; ".join(errors))
    provider = next((p for p in declaration.get("providers", []) if p["provider_key"] == provider_key), None)
    if provider is None:
        raise ValueError(f"the declaration has no provider {provider_key}")
    for field in ("name", "implementation_key"):
        if field not in provider:
            raise ValueError(f"provider {provider_key} needs {field} to generate an EngineRegistration")
    implemented = [s for s in provider["support"] if s["implementation_status"] == "IMPLEMENTED"]
    if not implemented:
        raise ValueError(f"provider {provider_key} has no IMPLEMENTED support to register")
    definitions = contracts.definitions()
    engine = declaration["engine"]["engine_id"]
    registered_provider = {
        "provider_key": provider_key,
        "name": provider["name"],
        "provider_type": provider["provider_type"],
        # engine_key is the deprecated v1 field (domain.schema.json engineKey);
        # the implementation family is its closest non-ambiguous meaning.
        "engine_key": provider["implementation_key"],
        "lifecycle": provider_lifecycle,
        "ownership": engine,
        "simulated": provider["simulated"],
        "production_permitted": provider["production_permitted"],
    }
    if "invocation" in provider:
        registered_provider["invocation"] = dict(provider["invocation"])
    registration = {
        "repository": engine,
        "capabilities": [bundle_capability(definitions[s["capability_key"]][0]) for s in implemented],
        "provider": registered_provider,
        "support": [{"capability_key": s["capability_key"], "contract_versions": list(s["contract_versions"])}
                    for s in implemented],
    }
    errors = contracts.errors(REGISTRATION_REF, registration)
    if errors:
        raise ValueError("generated registration is invalid: " + "; ".join(errors))
    return registration


def validate_shared(contracts: Contracts) -> list[str]:
    failures = validate_catalogue(contracts)
    if failures:
        return failures
    failures += validate_bundles(contracts)
    example = load_document(contracts.root / DECLARATION_EXAMPLE)
    failures += [f"contracts/{DECLARATION_EXAMPLE}: {e}" for e in validate_declaration(contracts, example)]
    if failures:
        return failures
    # Canonical definitions + provider declaration regenerate today's bundle.
    generated = generate_registration(contracts, example, "baobab-payments.sandbox", provider_lifecycle="ACTIVE")
    committed = load_document(contracts.root / "payments/v1/capabilities.json")
    generated["provider"]["engine_key"] = committed["provider"]["engine_key"]  # deprecated, see engineKey
    if generated != committed:
        failures.append("payments/v1/capabilities.json is not what its canonical definitions and the example "
                        "sandbox provider declaration generate")
    return failures


def report(failures: list[str], success: str) -> int:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    if failures:
        print(f"{len(failures)} failure(s)", file=sys.stderr)
        return 1
    print(success)
    return 0


def check_declaration_policy(repository_root: Path, mode: str) -> int:
    contract_path = repository_root / REPOSITORY_CONTRACT_PATH
    if not contract_path.is_file():
        return report([f"{contract_path} is missing: Foundation classification needs it"], "")
    declaration_path = repository_root / DECLARATION_PATH
    declaration = yaml.safe_load(declaration_path.read_text()) if declaration_path.is_file() else None
    findings = declaration_policy(yaml.safe_load(contract_path.read_text()) or {}, declaration)
    if mode == "warn":
        for finding in findings:
            print(f"::warning title=Capability declaration policy (G-FCI-1)::{finding}")
        print(f"capability declaration policy: {len(findings)} finding(s), reported as warnings")
        return 0
    return report(findings, "capability declaration policy passed")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--contracts-root", type=Path, default=CONTRACTS, help="a Shared contracts/ directory")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate-catalogue", help="validate Shared's canonical catalogue (Shared CI)")
    declaration = commands.add_parser("validate-declaration", help="validate an engine's .baobab/capability-provider.yaml")
    declaration.add_argument("path", type=Path)
    declaration.add_argument("--repository-root", type=Path, help="engine repository root; checks evidence paths exist")
    declaration.add_argument("--engine-id", help="the engine id the declaration must name, e.g. baobab-payments")
    declaration.add_argument("--template", action="store_true", help="substitute engine-template placeholders first")
    policy = commands.add_parser("check-declaration-policy",
                                 help="check the G-FCI-1 lifecycle policy for an engine repository (Foundation)")
    policy.add_argument("--repository-root", type=Path, default=Path("."), help="engine repository root")
    policy.add_argument("--mode", choices=POLICY_MODES, default="enforce",
                        help="warn reports findings and passes; enforce fails on any finding")
    generate = commands.add_parser("generate-registration", help="generate a transitional EngineRegistration")
    generate.add_argument("path", type=Path)
    generate.add_argument("--provider-key", required=True)
    generate.add_argument("--provider-lifecycle", default="DRAFT", choices=["DRAFT", "ACTIVE"])
    args = parser.parse_args(argv)
    if args.command == "check-declaration-policy":
        return check_declaration_policy(args.repository_root, args.mode)
    contracts = Contracts(args.contracts_root.resolve())

    if args.command == "validate-catalogue":
        definitions = len(contracts.definitions()) if not validate_catalogue(contracts) else 0
        return report(validate_shared(contracts), f"capability catalogue passed ({definitions} canonical capabilities)")
    catalogue_failures = validate_catalogue(contracts)
    if catalogue_failures:
        return report(["the Shared catalogue itself is invalid: " + m for m in catalogue_failures], "")
    text = args.path.read_text()
    if args.command == "validate-declaration":
        if args.template:
            text = substitute_template(text, contracts)
        document = yaml.safe_load(text)
        if args.template:
            left = sorted({p for value in walk_strings(document) for p in PLACEHOLDER.findall(value)})
            if left:
                return report([f"{args.path}: unknown template placeholders {left}"], "")
        return report([f"{args.path}: {m}" for m in validate_declaration(contracts, document, args.repository_root, args.engine_id)],
                      f"{args.path}: capability provider declaration passed")
    try:
        registration = generate_registration(contracts, yaml.safe_load(text), args.provider_key, args.provider_lifecycle)
    except ValueError as error:
        return report([str(error)], "")
    print(json.dumps(registration, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
