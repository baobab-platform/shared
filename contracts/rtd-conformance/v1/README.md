# RTD-10 cross-repository conformance profile v1

This package implements the portable declaration used by ADR-SHARED-026.

Each participating repository carries `.baobab/rtd-conformance.yaml`, pins an
immutable Shared commit and selects exactly one Shared-owned role policy:

| Role | Repository | Required maturity |
|---|---|---|
| `REGULATIONS_AUTHORITY` | `baobab-regulations` | `DOMAIN_RUNTIME` |
| `TRADE_DOCUMENT_AUTHORITY` | `baobab-trade-docs` | `ARCHITECTURE_ONLY` |
| `INTELLIGENCE_CONSUMER` | `baobab-pulse` | `IMPLEMENTED_CONSUMER` |

The profile does **not** let a consumer invent conformance rules. It supplies
identity, a Shared pin and evidence locations; `scripts/rtd_conformance.py`
owns the normative role checks.

Conformance means the repository respects ADR-SHARED-019/026 at its declared
maturity. It does not mean deployed, production-ready, certified, ACTIVE,
entitled or operationally healthy.
