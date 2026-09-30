# G-REG-NS — Regulations Namespace: Open Decision

**Status:** **Open. Not decided.**
**Date:** 2026-09-30 (supersedes the "resolved" record merged in shared#150)
**Related:** `g-reg-ns-regulations-namespace-proposal.md`, ADR-SHARED-007, ADR-SHARED-008, ADR-SHARED-017 §43, ADR-0018, ADR-0021, `baobab-regulations` ADR-REG-0001 to ADR-REG-0030 (all *Proposed*)

## Why this record was reopened

shared#150 recorded G-REG-NS as resolved. It said that no Regulations engine
is needed, that Trade owns tax, customs and regulatory determinations, and
that the Regulations census is deferred indefinitely. That conclusion came
with capability contract work, not from an architecture decision. It also
contradicts the `baobab-regulations` ADR family, which describes Regulations
as an independently deployable headless capability provider and a
Regulatory Context and Execution Engine (ADR-REG-0001, -0002, -0017, -0018).
Those ADRs are *Proposed*, not rejected.

An architecture review under ADR-SHARED-007 cannot close a fork between two
bodies of proposed architecture by implication. This record therefore
withdraws the earlier conclusion. The question stays open until an explicit
decision either accepts the ADR-REG family, or rejects or supersedes it.

## The fork

| | Option A | Option B |
|---|---|---|
| Summary | Trade owns tax, customs and regulatory orchestration | Trade owns operational enforcement; Regulations owns regulatory meaning, context and evaluation |
| Regulatory authority | ADR-0018 and ADR-0021 as they stand | ADR-REG family accepted; ADR-0018/0021 amended at the boundary (ADR-REG-0019 PDP/PEP separation, ADR-REG-0026 integration boundary) |
| `regulations` capability domain | Not registered | Registered after ADR-SHARED-007 review, alongside `tax` and `customs` |
| Regulations engine | Not a capability provider; the ADR-REG family is rejected or superseded explicitly | A capability provider with its own census and `.baobab/capability-provider.yaml` |

Either option needs an explicit decision record. Option A needs one that
rejects or supersedes the ADR-REG family. Option B needs the ADR-REG family
accepted and ADR-0018/0021 amended.

## Interim state (no decision implied)

- `regulations` stays unregistered in `namespace-registry.yaml`. That is the
  status quo before G-REG-NS, not an outcome of it.
- `tax` and `customs` stay registered under Trade authority per ADR-SHARED-008.
- The Regulations census is **paused pending this decision**, not deferred
  indefinitely.
- Regulations may list `proposed_key: regulations.*` candidates in a
  planned-only declaration (EA-02 record §3.11), but declares no support.
- No catalogue entry in the `tax` or `customs` domains that presumes Option A
  is added while this decision is open.

## Decision owner

The platform architecture owner, with baobab-trade and baobab-regulations as
parties. This is recorded in the EA-02 implementation record as an open user
decision.
