#!/usr/bin/env python3
"""RTD-10 cross-repository conformance validator (ADR-SHARED-026).

A consumer profile selects one fixed Shared-owned role policy. The repository
cannot weaken the policy in its manifest; it can only identify itself, pin
Shared and point at reviewable evidence.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts/rtd-conformance/v1/profile.schema.json").read_text())
PROFILE = ".baobab/rtd-conformance.yaml"

ROLE_REPOSITORY = {
    "REGULATIONS_AUTHORITY": "baobab-regulations",
    "TRADE_DOCUMENT_AUTHORITY": "baobab-trade-docs",
    "INTELLIGENCE_CONSUMER": "baobab-pulse",
}
ROLE_MATURITY = {
    "REGULATIONS_AUTHORITY": "DOMAIN_RUNTIME",
    "TRADE_DOCUMENT_AUTHORITY": "ARCHITECTURE_ONLY",
    "INTELLIGENCE_CONSUMER": "IMPLEMENTED_CONSUMER",
}
ROLE_CONTRACTS = {
    "REGULATIONS_AUTHORITY": {
        "contracts/capability/v1/catalogue.yaml",
        "contracts/control-plane/v1/domain.schema.json",
        "contracts/cross-engine-reference/v1/domain.schema.json",
        "contracts/events/v1/envelope.schema.json",
        "contracts/regulations/v1/capabilities.yaml",
        "contracts/regulatory-decision/v1/domain.schema.json",
        "contracts/regulatory-decision/v1/regulations.openapi.yaml",
        "contracts/regulatory-document-exchange/v1/domain.schema.json",
        "contracts/regulatory-document-exchange/v1/events.schema.json",
    },
    "TRADE_DOCUMENT_AUTHORITY": {
        "contracts/control-plane/v1/domain.schema.json",
        "contracts/cross-engine-reference/v1/domain.schema.json",
        "contracts/events/v1/envelope.schema.json",
        "contracts/trade-document/v2/domain.schema.json",
        "contracts/trade-document/v2/events.schema.json",
        "contracts/regulatory-document-exchange/v1/domain.schema.json",
        "contracts/regulatory-document-exchange/v1/events.schema.json",
    },
    "INTELLIGENCE_CONSUMER": {
        "contracts/authorization/v1/scope-registry.yaml",
        "contracts/capability/v1/catalogue.yaml",
        "contracts/control-plane/v1/domain.schema.json",
        "contracts/cross-engine-reference/v1/domain.schema.json",
        "contracts/events/v1/envelope.schema.json",
        "contracts/intelligence/v1/capabilities.yaml",
        "contracts/intelligence/v1/domain.schema.json",
        "contracts/identity/v1/workload-registry.yaml",
        "contracts/regulatory-document-exchange/v1/domain.schema.json",
        "contracts/regulatory-document-exchange/v1/events.schema.json",
        "contracts/trade-document/v2/domain.schema.json",
        "contracts/trade-document/v2/events.schema.json",
    },
}

PULSE_FOREIGN_AGGREGATES = {
    "RegulatoryInstrument",
    "RegulatoryRule",
    "RegulatoryDecision",
    "DocumentRequirement",
    "PermitRequirement",
    "EvidenceRequirement",
    "TradeDocument",
    "DocumentVersion",
    "CustomsCase",
}
REGULATIONS_FOREIGN_AGGREGATES = {
    "TradeDocument",
    "DocumentVersion",
    "ContentArtifact",
    "DocumentDossier",
    "CustomsCase",
    "CustomsDeclaration",
    "AuthorityResponse",
    "EvidenceSet",
    "Insight",
    "Opportunity",
    "Forecast",
    "Recommendation",
}
PULSE_FORBIDDEN_PROJECTOR_IMPORTS = (
    "httpx",
    "requests",
    "asyncpg",
    "sqlalchemy",
    "haystack",
    "qdrant_client",
    "haystack_integrations",
    "baobab_regulations",
    "baobab_trade_docs",
)
REGULATIONS_FORBIDDEN_IMPORTS = ("baobab_trade_docs", "baobab_pulse")

PULSE_EVENTS = {
    "com.baobab-platform.regulations.document-requirements.determined.v1",
    "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1",
    "com.baobab-platform.documents.regulatory-evidence.offered.v1",
    "com.baobab-platform.documents.document-version.verification-changed.v2",
    "com.baobab-platform.documents.document-version.validity-changed.v2",
}


def load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text())


def schema_findings(profile: object) -> list[str]:
    return [
        f"{PROFILE}: {'/'.join(str(p) for p in error.absolute_path) or '(root)'}: {error.message}"
        for error in sorted(
            Draft202012Validator(SCHEMA).iter_errors(profile),
            key=lambda error: list(map(str, error.absolute_path)),
        )
    ]


def git_head(path: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def python_files(root: Path) -> Iterable[Path]:
    src = root / "src"
    return src.rglob("*.py") if src.is_dir() else ()


def class_names(paths: Iterable[Path]) -> set[str]:
    names: set[str] = set()
    for path in paths:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue
        names.update(node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    return names


def imports(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            result.add(node.module)
    return result


def require_text(path: Path, needles: Iterable[str], findings: list[str]) -> None:
    if not path.is_file():
        findings.append(f"required evidence file missing: {path}")
        return
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            findings.append(f"{path}: required RTD-10 boundary evidence missing: {needle!r}")


def validate_common(
    repository_root: Path,
    shared_root: Path,
    profile: dict,
    repository_id: str | None,
) -> list[str]:
    findings: list[str] = []
    role = profile["repository"]["role"]
    repo = profile["repository"]["id"]

    if ROLE_REPOSITORY[role] != repo:
        findings.append(f"{repo}: role {role} belongs to {ROLE_REPOSITORY[role]}")
    if ROLE_MATURITY[role] != profile["repository"]["maturity"]:
        findings.append(
            f"{repo}: {role} must declare maturity {ROLE_MATURITY[role]}, "
            f"not {profile['repository']['maturity']}"
        )
    if repository_id and repository_id != repo:
        findings.append(f"profile repository id {repo} does not match caller repository {repository_id}")

    pin = profile["shared"]["commit"]
    head = git_head(shared_root)
    if head != pin:
        findings.append(f"Shared checkout HEAD {head or 'unresolved'} does not equal profile pin {pin}")

    declared = set(profile["shared"]["required_contracts"])
    missing_required = ROLE_CONTRACTS[role] - declared
    if missing_required:
        findings.append(
            f"{repo}: RTD-10 profile omits mandatory Shared contracts: {sorted(missing_required)}"
        )
    for contract in sorted(declared):
        if not (shared_root / contract).is_file():
            findings.append(f"{repo}: Shared contract missing at pinned commit: {contract}")

    evidence = profile["evidence"]
    for category in ("adr_paths", "source_paths", "test_paths"):
        for raw in evidence[category]:
            path = repository_root / raw
            if not path.exists():
                findings.append(f"{repo}: declared {category[:-1]} evidence does not exist: {raw}")
    return findings


def validate_regulations_provider_support(
    root: Path,
    declaration: dict,
    canonical_keys: set[object],
) -> list[str]:
    """R-CAP-07 Regulations provider support rules layered on Shared schema validation.

    RTD-10 permits evidence-backed PARTIAL support for canonical Regulations
    capabilities after the first implementation tranche. IMPLEMENTED remains a
    later governed promotion so this cross-repository profile cannot silently
    jump from repository implementation evidence to runtime-registerable support.
    """

    findings: list[str] = []
    supported: set[object] = set()

    providers = declaration.get("providers") or []
    if not isinstance(providers, list):
        return ["Regulations providers must be a list"]

    for provider in providers:
        if not isinstance(provider, dict):
            findings.append("Regulations provider entry must be a mapping")
            continue
        provider_key = provider.get("provider_key")
        if not isinstance(provider_key, str) or not provider_key.startswith(
            "baobab-regulations."
        ):
            findings.append(
                f"Regulations provider key must belong to baobab-regulations: {provider_key!r}"
            )

        support_entries = provider.get("support") or []
        if not isinstance(support_entries, list):
            findings.append(f"{provider_key}: provider support must be a list")
            continue

        for support in support_entries:
            if not isinstance(support, dict):
                findings.append(f"{provider_key}: support entry must be a mapping")
                continue

            capability_key = support.get("capability_key")
            supported.add(capability_key)
            if capability_key not in canonical_keys:
                findings.append(
                    f"{provider_key}: {capability_key!r} is not a canonical Shared capability"
                )
            if not isinstance(capability_key, str) or not capability_key.startswith(
                "regulations."
            ):
                findings.append(
                    f"{provider_key}: support escapes regulations namespace: {capability_key!r}"
                )

            status = support.get("implementation_status")
            if status != "PARTIAL":
                findings.append(
                    f"{provider_key}: {capability_key} must remain PARTIAL during R-CAP-07; "
                    "IMPLEMENTED requires the later governed promotion increment"
                )

            evidence = support.get("implementation_evidence")
            if not isinstance(evidence, list) or not evidence:
                findings.append(
                    f"{provider_key}: {capability_key} PARTIAL support requires implementation evidence"
                )
                continue

            for item in evidence:
                if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                    findings.append(
                        f"{provider_key}: {capability_key} has malformed implementation evidence"
                    )
                    continue
                evidence_path = root / item["path"]
                if not evidence_path.exists():
                    findings.append(
                        f"{provider_key}: {capability_key} evidence does not exist: {item['path']}"
                    )

    for item in declaration.get("planned_capabilities") or []:
        if not isinstance(item, dict):
            continue
        capability_key = item.get("capability_key")
        if capability_key in supported:
            findings.append(
                f"{capability_key}: capability cannot be both planned and provider support"
            )

    return findings


def validate_regulations(root: Path, shared_root: Path, profile: dict) -> list[str]:
    findings: list[str] = []
    domain_root = root / "src/baobab_regulations/domain"
    names = class_names(domain_root.rglob("*.py") if domain_root.is_dir() else ())
    if "RegulatoryDecision" not in names:
        findings.append("Regulations must define its canonical RegulatoryDecision")
    foreign = names & REGULATIONS_FOREIGN_AGGREGATES
    if foreign:
        findings.append(f"Regulations defines forbidden foreign canonical aggregates: {sorted(foreign)}")

    bad_imports: set[str] = set()
    for path in python_files(root):
        for module in imports(path):
            if module.startswith(REGULATIONS_FORBIDDEN_IMPORTS):
                bad_imports.add(module)
    if bad_imports:
        findings.append(f"Regulations directly imports another RTD engine: {sorted(bad_imports)}")

    provider_path = root / ".baobab/capability-provider.yaml"
    if not provider_path.is_file():
        findings.append("Regulations must retain its capability-provider declaration")
    else:
        provider = load_yaml(provider_path)
        if not isinstance(provider, dict):
            findings.append("Regulations capability-provider declaration is not a mapping")
        else:
            catalogue = load_yaml(shared_root / "contracts/capability/v1/catalogue.yaml")
            canonical_keys = {
                item.get("capability_key")
                for item in (catalogue.get("capabilities") or [])
                if isinstance(item, dict)
            } if isinstance(catalogue, dict) else set()

            findings.extend(
                validate_regulations_provider_support(root, provider, canonical_keys)
            )

            for item in provider.get("planned_capabilities") or []:
                if not isinstance(item, dict):
                    findings.append("Regulations planned capability entry must be a mapping")
                    continue

                proposed_key = item.get("proposed_key")
                capability_key = item.get("capability_key")
                status = item.get("proposal_status")

                if proposed_key is not None:
                    if not str(proposed_key).startswith("regulations."):
                        findings.append(
                            f"Regulations planned capability escapes regulations namespace: {proposed_key!r}"
                        )
                    if status == "CONTRACTED":
                        findings.append(
                            f"{proposed_key}: CONTRACTED capabilities must use canonical capability_key"
                        )
                    continue

                if capability_key is not None:
                    if not str(capability_key).startswith("regulations."):
                        findings.append(
                            f"Regulations contracted capability escapes regulations namespace: {capability_key!r}"
                        )
                    if status != "CONTRACTED":
                        findings.append(
                            f"{capability_key}: canonical capability_key is allowed only with proposal_status CONTRACTED"
                        )
                    if capability_key not in canonical_keys:
                        findings.append(
                            f"{capability_key}: contracted capability is not present in the Shared catalogue"
                        )
                    continue

                findings.append("Regulations planned capability must name proposed_key or capability_key")

    local_events = root / "contracts/events"
    if local_events.is_dir():
        for path in local_events.glob("*.json"):
            text = path.read_text(encoding="utf-8")
            if "com.baobab-platform.regulations." in text:
                findings.append(f"{path}: repository-local v0 audit contract claims canonical Shared event authority")
            if not path.name.endswith(".v0.json"):
                findings.append(f"{path}: pre-Shared Regulations audit event must remain explicitly v0")

    require_text(
        root / "docs/adr/ADR-REG-0026 — Baobab Platform Integration and Canonical Context Boundary.md",
        (
            "Regulations determines regulatory meaning",
            "Trade Docs owns executable trade-document",
            "Trade Docs VERIFIED",
            "Regulations SATISFIED",
        ),
        findings,
    )
    require_text(
        root / "docs/adr/ADR-REG-0027 — Cross-Border Trade Regulatory Profile.md",
        ("Trade Docs", "DocumentRequirement", "TradeDocument"),
        findings,
    )
    return findings


def validate_trade_docs(root: Path, profile: dict) -> list[str]:
    findings: list[str] = []
    if (root / "src").exists():
        findings.append(
            "Trade Docs declares ARCHITECTURE_ONLY but src/ exists; change maturity only with a new governed implementation increment"
        )
    if (root / ".baobab/capability-provider.yaml").exists():
        findings.append(
            "Trade Docs architecture-only scaffold must not claim a real capability provider before capability/runtime implementation"
        )
    for forbidden in (
        "contracts/trade-document",
        "contracts/regulatory-document-exchange",
        "contracts/regulatory-document-evidence",
    ):
        if (root / forbidden).exists():
            findings.append(f"Trade Docs must consume Shared authority rather than fork canonical contracts: {forbidden}")

    require_text(
        root / "README.md",
        (
            "runtime implementation has not started",
            "Verification != Regulatory Sufficiency",
            "Regulations",
            "does not mean the application runtime/outbox/broker implementation already",
        ),
        findings,
    )
    require_text(
        root / "docs/adr/ADR-TDOC-0001 — Baobab Trade Docs Mission, Authority, Executable Trade Document and Customs Workflow Boundary.md",
        ("Baobab Regulations", "Requirement", "TradeDocument", "Evidence"),
        findings,
    )
    require_text(
        root / "docs/adr/ADR-TDOC-0002 — Canonical TradeDocument, Version, Content and Relationship Model.md",
        ("TradeDocument", "DocumentVersion", "ContentArtifact", "Regulations"),
        findings,
    )
    return findings


PULSE_FIRST_CENSUS_KEYS = {
    "intelligence.evidence.search",
    "intelligence.research-mission.manage",
}


def validate_pulse_provider_declaration(
    root: Path,
    declaration: dict,
    canonical_keys: set[object],
) -> list[str]:
    """ADR-SHARED-029/030/031 rules for Pulse capability promotion.

    P-CAP-07 is the full repository provider-readiness decision for the first
    Intelligence tranche. Once Pulse declares provider support against this
    authority, both first-census capabilities must be IMPLEMENTED with
    reviewable source, contract and integration evidence. This still does not
    imply EA-09 certification or Control Plane activation.
    """

    findings: list[str] = []
    supported: set[object] = set()

    providers = declaration.get("providers") or []
    if not isinstance(providers, list):
        return ["Pulse providers must be a list"]

    for provider in providers:
        if not isinstance(provider, dict):
            findings.append("Pulse provider entry must be a mapping")
            continue
        provider_key = provider.get("provider_key")
        if not isinstance(provider_key, str) or not provider_key.startswith("baobab-pulse."):
            findings.append(
                f"Pulse provider key must belong to baobab-pulse: {provider_key!r}"
            )
        if provider.get("simulated") is not False:
            findings.append(f"{provider_key}: P-CAP-07 provider must be non-simulated")
        if provider.get("production_permitted") is not True:
            findings.append(
                f"{provider_key}: P-CAP-07 provider must be production_permitted; "
                "permission is not activation"
            )
        invocation = provider.get("invocation")
        if not isinstance(invocation, dict):
            findings.append(
                f"{provider_key}: P-CAP-07 IMPLEMENTED provider requires logical invocation metadata"
            )
        else:
            if invocation.get("protocol") != "http":
                findings.append(f"{provider_key}: Pulse canonical provider invocation must use http")
            service_reference = invocation.get("service_reference")
            if not isinstance(service_reference, str) or not service_reference.startswith(
                "service://baobab-pulse/"
            ):
                findings.append(
                    f"{provider_key}: Pulse invocation must remain logical and owned by baobab-pulse"
                )

        support_entries = provider.get("support") or []
        if not isinstance(support_entries, list):
            findings.append(f"{provider_key}: provider support must be a list")
            continue

        for support in support_entries:
            if not isinstance(support, dict):
                findings.append(f"{provider_key}: support entry must be a mapping")
                continue

            capability_key = support.get("capability_key")
            supported.add(capability_key)
            if capability_key not in canonical_keys:
                findings.append(
                    f"{provider_key}: {capability_key!r} is not a canonical Shared capability"
                )
            if capability_key not in PULSE_FIRST_CENSUS_KEYS:
                findings.append(
                    f"{provider_key}: P-CAP-07 cannot promote uncensused Intelligence capability "
                    f"{capability_key!r}"
                )

            status = support.get("implementation_status")
            if status != "IMPLEMENTED":
                findings.append(
                    f"{provider_key}: {capability_key} must be IMPLEMENTED for P-CAP-07 "
                    "provider readiness"
                )

            evidence = support.get("implementation_evidence")
            if not isinstance(evidence, list) or not evidence:
                findings.append(
                    f"{provider_key}: {capability_key} IMPLEMENTED support requires implementation evidence"
                )
                continue

            evidence_types: set[str] = set()
            for item in evidence:
                if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                    findings.append(
                        f"{provider_key}: {capability_key} has malformed implementation evidence"
                    )
                    continue
                if isinstance(item.get("type"), str):
                    evidence_types.add(item["type"])
                evidence_path = root / item["path"]
                if not evidence_path.exists():
                    findings.append(
                        f"{provider_key}: {capability_key} evidence does not exist: {item['path']}"
                    )
            required_evidence = {"source", "contract-test", "integration-test"}
            missing_evidence = required_evidence - evidence_types
            if missing_evidence:
                findings.append(
                    f"{provider_key}: {capability_key} P-CAP-07 readiness evidence is missing "
                    f"{sorted(missing_evidence)}"
                )

    if providers and supported != PULSE_FIRST_CENSUS_KEYS:
        findings.append(
            "P-CAP-07 provider support must cover exactly the two first-census "
            f"capabilities: {sorted(PULSE_FIRST_CENSUS_KEYS)}"
        )

    planned = declaration.get("planned_capabilities") or []
    if not isinstance(planned, list):
        return findings + ["Pulse planned_capabilities must be a list"]

    for item in planned:
        if not isinstance(item, dict):
            findings.append("Pulse planned capability entry must be a mapping")
            continue

        proposed_key = item.get("proposed_key")
        capability_key = item.get("capability_key")
        status = item.get("proposal_status")

        if capability_key in supported:
            findings.append(
                f"{capability_key}: capability cannot be both planned and provider support"
            )

        if proposed_key is not None:
            if not str(proposed_key).startswith("intelligence."):
                findings.append(
                    f"Pulse proposed capability escapes intelligence namespace: {proposed_key!r}"
                )
            if status == "CONTRACTED":
                findings.append(
                    f"{proposed_key}: CONTRACTED capabilities must use canonical capability_key"
                )
            continue

        if capability_key is not None:
            if not str(capability_key).startswith("intelligence."):
                findings.append(
                    f"Pulse contracted capability escapes intelligence namespace: {capability_key!r}"
                )
            if status != "CONTRACTED":
                findings.append(
                    f"{capability_key}: canonical capability_key is allowed only with proposal_status CONTRACTED"
                )
            if capability_key not in canonical_keys:
                findings.append(
                    f"{capability_key}: contracted capability is not present in the Shared catalogue"
                )
            continue

        findings.append("Pulse planned capability must name proposed_key or capability_key")

    return findings

def validate_pulse(root: Path, shared_root: Path, profile: dict) -> list[str]:
    findings: list[str] = []
    lock_path = root / "contracts.lock.yaml"
    if not lock_path.is_file():
        findings.append("Pulse implemented consumer must carry contracts.lock.yaml")
    else:
        lock = load_yaml(lock_path)
        if not isinstance(lock, dict):
            findings.append("Pulse contracts.lock.yaml is not a mapping")
        else:
            if (lock.get("source") or {}).get("commit") != profile["shared"]["commit"]:
                findings.append("Pulse contract lock pin must equal the RTD-10 Shared profile pin")
            listed = set(lock.get("contracts") or [])
            missing = ROLE_CONTRACTS["INTELLIGENCE_CONSUMER"] - listed
            if missing:
                findings.append(f"Pulse contract lock omits RTD contracts: {sorted(missing)}")
            for contract in listed:
                fixture = root / "tests/fixtures" / contract
                shared = shared_root / contract
                if not fixture.is_file():
                    findings.append(f"Pulse vendored Shared fixture missing: tests/fixtures/{contract}")
                elif shared.is_file() and fixture.read_bytes() != shared.read_bytes():
                    findings.append(f"Pulse vendored fixture drifted from pinned Shared contract: {contract}")

    domain_root = root / "src/baobab_pulse/domain"
    names = class_names(domain_root.rglob("*.py") if domain_root.is_dir() else ())
    foreign = names & PULSE_FOREIGN_AGGREGATES
    if foreign:
        findings.append(f"Pulse defines forbidden foreign canonical aggregates: {sorted(foreign)}")

    projector = root / "src/baobab_pulse/application/services/upstream_fact_projection_service.py"
    if not projector.is_file():
        findings.append("Pulse RTD-09 upstream projector is missing")
    else:
        bad_imports = {
            module
            for module in imports(projector)
            if module.startswith(PULSE_FORBIDDEN_PROJECTOR_IMPORTS)
        }
        if bad_imports:
            findings.append(f"Pulse projector has forbidden synchronous/provider dependencies: {sorted(bad_imports)}")
        text = projector.read_text(encoding="utf-8")
        for event_type in sorted(PULSE_EVENTS):
            if event_type not in text:
                findings.append(f"Pulse projector no longer consumes canonical upstream event: {event_type}")
        for producer in (
            "urn:baobab-platform:service:baobab-regulations",
            "urn:baobab-platform:service:baobab-trade-docs",
        ):
            if producer not in text:
                findings.append(f"Pulse projector does not bind canonical logical producer: {producer}")

    projection = root / "src/baobab_pulse/domain/projections/models.py"
    require_text(
        projection,
        (
            "class UpstreamFactProjection(ValueObject)",
            "source_event_source",
            "return (self.source_event_source, self.source_event_id)",
        ),
        findings,
    )

    event_helper = root / "src/baobab_pulse/contracts/events.py"
    if event_helper.is_file():
        text = event_helper.read_text(encoding="utf-8")
        if "com.baobab-platform.pulse." in text:
            findings.append("Pulse must not mint repository-named canonical event types")
        if "com.baobab-platform.intelligence." not in text:
            findings.append("Pulse future event scaffold must use reserved intelligence context")
    else:
        findings.append("Pulse canonical event-envelope implementation is missing")

    provider = root / ".baobab/capability-provider.yaml"
    if provider.exists():
        data = load_yaml(provider)
        if not isinstance(data, dict):
            findings.append("Pulse capability-provider declaration is not a mapping")
        else:
            catalogue = load_yaml(shared_root / "contracts/capability/v1/catalogue.yaml")
            canonical_keys = {
                item.get("capability_key")
                for item in (catalogue.get("capabilities") or [])
                if isinstance(item, dict)
            } if isinstance(catalogue, dict) else set()
            findings.extend(
                validate_pulse_provider_declaration(root, data, canonical_keys)
            )
    return findings


def check(
    repository_root: Path,
    shared_root: Path,
    repository_id: str | None = None,
) -> list[str]:
    profile_path = repository_root / PROFILE
    if not profile_path.is_file():
        return [f"{PROFILE} is required for RTD-10 participants"]
    profile = load_yaml(profile_path)
    findings = schema_findings(profile)
    if findings or not isinstance(profile, dict):
        return findings or [f"{PROFILE} must contain a mapping"]

    findings += validate_common(repository_root, shared_root, profile, repository_id)
    role = profile["repository"]["role"]
    if role == "REGULATIONS_AUTHORITY":
        findings += validate_regulations(repository_root, shared_root, profile)
    elif role == "TRADE_DOCUMENT_AUTHORITY":
        findings += validate_trade_docs(repository_root, profile)
    elif role == "INTELLIGENCE_CONSUMER":
        findings += validate_pulse(repository_root, shared_root, profile)
    return findings


def validate_profile(path: Path) -> list[str]:
    if not path.is_file():
        return [f"profile does not exist: {path}"]
    return schema_findings(load_yaml(path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)

    check_cmd = commands.add_parser("check")
    check_cmd.add_argument("--repository-root", type=Path, default=Path("."))
    check_cmd.add_argument("--shared-repo", type=Path, required=True)
    check_cmd.add_argument("--repository-id")

    profile_cmd = commands.add_parser("validate-profile")
    profile_cmd.add_argument("profile", type=Path)

    args = parser.parse_args(argv)
    if args.command == "validate-profile":
        findings = validate_profile(args.profile)
    else:
        findings = check(args.repository_root, args.shared_repo, args.repository_id)

    for finding in findings:
        print(f"FAIL: {finding}", file=sys.stderr)
    if findings:
        print(f"{len(findings)} RTD-10 conformance failure(s)", file=sys.stderr)
        return 1
    print("RTD-10 cross-repository conformance passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
