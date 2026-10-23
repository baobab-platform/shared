#!/usr/bin/env python3
"""Offline BFG-SED v1 synthetic scenario generator.

This is NOT a CP bootstrap, IAM issuer, CMS importer, Payments adapter, or market
activation tool. It generates versioned, untrusted development INPUT ONLY.
No network, DB connection, production secret, token, money transfer or registry
document is created. Native-engine seed adapters must independently enforce
IAM/CP and their own domain contracts in disposable development environments.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "fixtures" / "development" / "bfg-sed" / "v1" / "blueprint.json"
SCALES = {"small": (1, 1), "medium": (5, 3), "large": (40, 12)}
# These are the only CP bootstrap scenario profiles presently accepted, regardless
# of which proposed markets appear in this separate OFFLINE fixture overlay.
CP_PROFILES = {"nabhold", "zuribeans", "thamani", "equator-estate", "external-client"}
PROTECTED_ENVIRONMENTS = {"staging", "production", "prod", "protected"}
SCHEMA = "baobab.fixture.bfg-sed.generated.v1"


def _ordinal(seed: int, key: str, index: int, ceiling: int) -> int:
    digest = hashlib.sha256(f"{seed}|{key}|{index}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % ceiling


def fixture_ref(run_id: str, seed: int, kind: str, key: str, index: int = 0) -> str:
    """Non-canonical human-readable ID. Not an OrganisationID/PrincipalID/UUID."""
    h = hashlib.sha256(f"{run_id}|{seed}|{kind}|{key}|{index}".encode()).hexdigest()[:16]
    return f"SYN-{kind.upper()}-{h}"


def load_blueprint(path: Path = BLUEPRINT) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_blueprint(data)
    return data


def validate_blueprint(b: dict[str, Any]) -> None:
    if (b.get("schema") != "baobab.fixture.bfg-sed.v1"
            or b.get("kind") != "DEVELOPMENT_SCENARIO_BLUEPRINT_ONLY"
            or b.get("synthetic_only") is not True
            or b.get("protected_acceptance") is not False
            or b.get("real_data") is not False
            or b.get("source_of_canonical_ids") != "CONTROL_PLANE_ONLY"
            or b.get("lease_max_seconds", 0) > 86400):
        raise ValueError("refuse blueprint without complete disposable/synthetic guardrails")
    mk = {m["code"] for m in b["markets"]}
    if len(mk) != len(b["markets"]) or len(mk) < 18 or any(len(x) != 2 for x in mk):
        raise ValueError("market code set is invalid or incomplete")
    for m in b["markets"]:
        if not all(m.get(k) for k in ("currency", "locale", "timezone", "name")):
            raise ValueError("market lacks locale/currency/timezone")
    enterprises = {e["key"]: e for e in b["enterprises"]}
    if set(enterprises) != CP_PROFILES or any(e["profile"] != k for k, e in enterprises.items()):
        raise ValueError("cannot change canonical CP profile roster via an overlay")
    if b["enterprises"][0]["key"] != "nabhold" or enterprises["nabhold"]["business_model"] != "NON_TRADING_HOLDING":
        raise ValueError("Nabhold must remain non-trading")
    # Freeze declared legal-model *semantics* for the baseline. The overlay
    # cannot quietly turn an operating business into an incorporated company.
    expected_legal = {
        "nabhold": "DECLARED_HOLDING_UNVERIFIED_FOR_TEST",
        "zuribeans": "OPERATING_ORGANISATION_NO_SEPARATE_INCORPORATION",
        "thamani": "DECLARED_SEPARATELY_INCORPORATED_UNVERIFIED_FOR_TEST",
        "equator-estate": "OPERATING_ORGANISATION_NO_SEPARATE_INCORPORATION",
        "external-client": "INDEPENDENT_EXTERNAL_ORGANISATION_REGISTRATION_UNVERIFIED",
    }
    for key, legal_model in expected_legal.items():
        if enterprises[key]["legal_model"] != legal_model:
            raise ValueError(f"illegal synthetic legal-model drift: {key}")
    if enterprises["external-client"]["estate"] is not None or enterprises["external-client"]["primary_market"] != "UG":
        raise ValueError("external pharma client must be independent, UG-based and API-only")
    if set(enterprises["external-client"]["source_markets"]) != {"CN", "IN"}:
        raise ValueError("external pharma fixture requires CN/IN import origins")
    if set(enterprises["equator-estate"]["operating_markets"]) != {"UG", "ZA"}:
        raise ValueError("Equator operating markets differ from approved synthetic scenario")
    if set(enterprises["thamani"]["operating_markets"]) != {
        "ZA","EG","DE","GB","UG","KE","TZ","GH","MZ","AO","NG","ET","DJ","SZ"
    }:
        raise ValueError("Thamani scenario operating markets are incomplete")
    for e in enterprises.values():
        for k in ("operating_markets", "footprint_markets", "source_markets"):
            if not set(e[k]) <= mk:
                raise ValueError(f"unknown {k} country code in {e['key']}")
        if not e["roles"] or not e["capability_requests"]:
            raise ValueError("role/capability test coverage missing")
        if not e["legal_model"] or "VERIFIED" not in e["legal_model"] and "INCORPORATION" not in e["legal_model"]:
            raise ValueError("explicit unverified legal model required")
    keys = [s["key"] for s in b["scenario_inputs"]]
    if len(keys) != len(set(keys)) or len(keys) < 30:
        raise ValueError("scenario keys not unique or insufficient")
    for s in b["scenario_inputs"]:
        if s["enterprise_key"] not in enterprises or s["origin"] not in mk or s["destination"] not in mk:
            raise ValueError(f"invalid scenario {s['key']}")
    for key, rows in b["products"].items():
        if key not in enterprises or key == "nabhold":
            raise ValueError("product data may not make holding company a seller")
        for p in rows:
            if len(p) != 5 or p[4] not in mk:
                raise ValueError("invalid product template")


def generate(b: dict[str, Any], *, scale: str, seed: int, run_id: str) -> dict[str, Any]:
    validate_blueprint(b)
    if scale not in SCALES:
        raise ValueError("unknown scale")
    if len(run_id) != 32 or any(c not in "0123456789abcdef" for c in run_id):
        raise ValueError("run_id must be 32 lowercase hex chars")
    repeat, person_repeat = SCALES[scale]
    markets = {x["code"]: x for x in b["markets"]}
    start = datetime.fromisoformat(b["reference_date"] + "T09:00:00+00:00")
    enterprise_refs = {e["key"]: fixture_ref(run_id, seed, "tenantref", e["key"]) for e in b["enterprises"]}

    orgs: list[dict[str, Any]] = []
    people: list[dict[str, Any]] = []
    facilities: list[dict[str, Any]] = []
    counterparties: list[dict[str, Any]] = []
    items: list[dict[str, Any]] = []
    transactions: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []

    for e in b["enterprises"]:
        orgs.append({
            "fixture_key": e["key"],
            "fixture_tenant_ref": enterprise_refs[e["key"]],
            "display_name": e["name"],
            "cp_profile_key": e["profile"],
            "business_model": e["business_model"],
            "primary_market_scenario": e["primary_market"],
            "operating_markets_scenario": e["operating_markets"],
            "footprint_markets_scenario": e["footprint_markets"],
            "sourcing_origins_scenario": e["source_markets"],
            "digital_estate_profile_key": e["estate"],
            "legal_model_assertion": e["legal_model"],
            "incorporation_verified": False,
            "commercially_authorised": False,
            "provider_activated": False,
            "market_grants": [],
            "requested_canonical_capabilities_only": e["capability_requests"],
            "scenario_intents_not_capability_keys": e["scenario_intents"],
            "canonical_tenant_id": None,  # CP must allocate on real bootstrap.
            "canonical_organisation_id": None,
            "canonical_legal_entity_id": None,
        })
        # Scenario market presence is not a CP Market record, approved branch,
        # legal incorporation, market grant or commercial operational right.
        market_repeats = 1 if scale == "small" else (2 if scale == "medium" else 10)
        for country in e["operating_markets"]:
            for n in range(market_repeats):
                facilities.append({
                    "fixture_ref": fixture_ref(run_id, seed, "site", e["key"] + country, n),
                    "enterprise_fixture_key": e["key"],
                    "market_scenario": country,
                    "display_name": f"Synthetic {e['key']} Site {country}-{n:02d}",
                    "address": None,  # Never generate a plausible real address.
                    "geocodable": False,
                    "actual_location_verified": False,
                    "market_activated": False,
                    "engine_site_id": None,
                })
        # Source and footprint countries create prospective counterparties,
        # not local legal entities or automatic cross-market authority.
        for country in sorted(set(e["source_markets"] + e["footprint_markets"])):
            for n in range(market_repeats):
                role = ("supplier" if e["key"] in {"zuribeans", "external-client"} else
                        "prospective_business_partner")
                counterparties.append({
                    "fixture_ref": fixture_ref(run_id, seed, "counterparty", e["key"] + country, n),
                    "customer_tenant_fixture_ref": enterprise_refs[e["key"]],
                    "display_name": f"Synthetic {markets[country]['name']} {role.replace('_', ' ').title()} {n+1}",
                    "relationship_type": role,
                    "country_scenario": country,
                    "email": f"counterparty-{e['key']}-{country.lower()}-{n}@example.invalid",
                    "cp_organisation_id": None,
                    "legal_entity_verified": False,
                    "market_granted": False,
                    "provider_qualified": False,
                    "pharmaceutical_supplier_gmp_verified": False if e["key"] == "external-client" else None,
                })
        for role in e["roles"]:
            for n in range(person_repeat):
                username = f"{e['key']}-{role}-{n}".replace("_", "-")
                people.append({
                    "fixture_ref": fixture_ref(run_id, seed, "persona", username),
                    "enterprise_fixture_key": e["key"],
                    "display_name": f"Synthetic {role.replace('_', ' ').title()} {n + 1}",
                    "email": f"synthetic-{username}@example.invalid",
                    "scenario_role": role,
                    "iam_subject": None,
                    "cp_principal_id": None,
                    "registered_grant": False,
                    "maker_checker_pair": "CHECKER" if "reviewer" in role or "approver" in role else "MAKER",
                    "fictional": True,
                })
        for product in b["products"].get(e["key"], []):
            code, name, category, unit, origin = product
            variants = 1 if scale == "small" else (3 if scale == "medium" else 12)
            for variant in range(variants):
                items.append({
                    "fixture_ref": fixture_ref(run_id, seed, "item", code, variant),
                    "owner_enterprise_key": e["key"],
                    "sku": f"SYN-{code}-{variant:03d}",
                    "name": name,
                    "category": category,
                    "unit": unit,
                    "country_of_origin_scenario": origin,
                    "synthetic_batch": f"SIM-BATCH-{code}-{variant:04d}",
                    "provider_catalogue_id": None,
                    "document_status": "SYNTHETIC_UNVERIFIED",
                    "price_minor_units": 1000 + _ordinal(seed, code, variant, 9000000),
                    "price_currency": markets[origin]["currency"],
                    "fx_rate": None,
                    "actual_inventory": False,
                    "pharma_product_registered": False if e["key"] == "external-client" else None,
                })

    for scenario in b["scenario_inputs"]:
        ek = scenario["enterprise_key"]
        dest_market = markets[scenario["destination"]]
        for i in range(repeat):
            ref = fixture_ref(run_id, seed, "scenario", scenario["key"], i)
            case_kind = ("BASE", "AUDIENCE_DENY", "CROSS_TENANT_DENY", "EXPIRED_MANDATE",
                         "MISSING_GRANT", "STALE_PROVIDER", "DUPLICATE_REPLAY", "DEPENDENCY_OUTAGE")[
                             i % 8]
            when = start + timedelta(hours=_ordinal(seed, scenario["key"], i, 1200))
            simulated_cost = 1200 + _ordinal(seed, scenario["key"], i + 7, 90000000)
            tx = {
                "fixture_ref": ref,
                "source_scenario": scenario["key"],
                "case_variant": case_kind,
                "owner_enterprise_key": ek,
                "owner_tenant_fixture_ref": enterprise_refs[ek],
                "origin_country": scenario["origin"],
                "destination_country": scenario["destination"],
                "origin_timezone": markets[scenario["origin"]]["timezone"],
                "destination_timezone": dest_market["timezone"],
                "currency": dest_market["currency"],
                "amount_minor_units": simulated_cost,
                "fx_quote": None,
                "quantity": 1 + _ordinal(seed, scenario["key"], i, 1000),
                "scenario_type": scenario["scenario_type"],
                "expected_precondition": scenario["expected_precondition"],
                "expected_engine_result": "NOT_EXECUTED",
                "runtime_qualification": False,
                "synthetic_only": True,
                "money_moved": False,
                "canonical_owner_tenant_id": None,
                "utc_scenario_time": when.isoformat().replace("+00:00", "Z"),
            }
            transactions.append(tx)
            # Evidence is intentionally either absent or unverified. Never a
            # real permit, customs release, licensed product or bank reference.
            status = "MISSING" if "PH-" in scenario["key"] or case_kind == "EXPIRED_MANDATE" else "UNVERIFIED"
            evidence.append({
                "fixture_ref": fixture_ref(run_id, seed, "evidence", scenario["key"], i),
                "transaction_fixture_ref": ref,
                "category": "FAKE_DOCUMENTARY_ASSERTION",
                "verification_status": status,
                "actual_document": None,
                "official_registration": None,
                "import_permit_id": None,
                "nda_verification_certificate": None,
                "simulated_document_label": "SYNTHETIC TEST DATA - NOT A LICENSE",
            })
            # A blocked prerequisite cannot become a permitted BASE operation.
            # Conditional scenarios remain conditional; this offline expectation
            # never grants authority or asserts that a native call succeeded.
            precondition = scenario["expected_precondition"]
            blocked = precondition.startswith("BLOCK_UNTIL")
            denied = "DENY" in precondition or case_kind != "BASE"
            expectation = "BLOCKED" if blocked else ("DENY" if denied else "CONDITIONAL")
            observations.append({
                "fixture_ref": fixture_ref(run_id, seed, "observation", scenario["key"], i),
                "transaction_fixture_ref": ref,
                "classification": "SCENARIO_EXPECTATION_NOT_RUNTIME_EVIDENCE",
                "expected_outcome": expectation,
                "expected_denial": blocked or denied,
                "observed_result": None,
                "runtime_evidence_link": None,
            })

    return {
        "schema": SCHEMA,
        "profile": scale,
        "seed": seed,
        "run_id": run_id,
        "synthetic_only": True,
        "protected_acceptance": False,
        "can_import_directly_to_cp": False,
        "can_promote_to_staging_or_production": False,
        "actual_identity_issuance": False,
        "real_market_authorisation": False,
        "reference_date": b["reference_date"],
        "declarative_market_catalogue": b["markets"],
        "legal_evidence_status": "UNVERIFIED",
        "engine_capability_status": "REQUEST_ONLY_NOT_ACTIVATED",
        "organisations": orgs,
        "personas": people,
        "facilities": facilities,
        "counterparties": counterparties,
        "catalogue_items": items,
        "scenario_transactions": transactions,
        "documentary_evidence_inputs": evidence,
        "test_case_expectations": observations,
        "counts": {
            "organisations": len(orgs), "personas": len(people),
            "facilities": len(facilities), "counterparties": len(counterparties),
            "catalogue_items": len(items),
            "scenario_transactions": len(transactions),
            "documentary_evidence_inputs": len(evidence),
            "test_case_expectations": len(observations),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Offline synthetic BFG-SED fixture generator (no CP/production writes)")
    ap.add_argument("--scale", choices=sorted(SCALES), default="small")
    ap.add_argument("--seed", type=int, default=20261023)
    ap.add_argument("--run-id", default="00000000000000000000000000000001")
    ap.add_argument("--output", type=Path, help="Write UTF-8 JSON fixture (stdout when omitted)")
    args = ap.parse_args()
    if os.getenv("BAOBAB_ENVIRONMENT", "").lower() in PROTECTED_ENVIRONMENTS:
        ap.error("BFG-SED offline fixture generation prohibited in staging or production")
    if args.seed < 0:
        ap.error("seed must be a nonnegative integer")
    output = generate(load_blueprint(), scale=args.scale, seed=args.seed, run_id=args.run_id)
    data = json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
        print(f"Wrote {args.output} ({len(output['scenario_transactions'])} cases)")
    else:
        print(data, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
