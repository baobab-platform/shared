# Baobab event contracts v1

| File | What it governs |
|---|---|
| `envelope.schema.json` | The canonical CloudEvents 1.0 envelope and the syntax of every event type, `com.baobab-platform.<context>.<...>.v<N>` (ADR-SHARED-008 §3). |
| `context-registry.yaml` | Which `<context>` values exist, their status (ACTIVE, RESERVED, DEPRECATED), their stewards, and their related capability domains (ADR-SHARED-018 §3.2). |
| `event-registry.yaml` | Every canonical event type, the AsyncAPI document that defines it, its one producer, and its lifecycle (ADR-SHARED-018 §3.3). |
| `compatibility/` | Legacy shapes the envelope must reject. |

The AsyncAPI documents under `contracts/<package>/v<N>/` still define each
message and its payload. The event registry indexes them. It does not
replace them.

Grammar (ADR-SHARED-018 §3.4): `com.baobab-platform.<context>.<aggregate>.<fact>.v<major>`.
An event is a past-tense business fact, never a command to another engine.
No segment names a vendor, engine, tenant, Digital Estate, country or
region.

A **PROPOSED** type is a defined contract whose producer authority is not
yet assigned. It becomes **ACTIVE** when a steward of its context is
recorded as its producer.

Validated in Shared CI by `scripts/validate-event-registry.py` (envelope,
payloads, examples) and `scripts/event_contexts.py` (contexts, producers,
naming, lifecycle).
