# DEV-08 — Thamani logistics admission and provider readiness

Accepted EA-DEV DEV-08 depends on DEV-03 and actual TMS provider readiness.
The original INT-04 meaning remains authoritative. Thamani's current Accepted
ADR-THA-0018 establishes organisation-centric B2B logistics; an individual
recipient gains no B2B Organisation, merchant or purchasing authority through
customer status. Retired retail checkout must not become an integration fallback.

## Current source observation — 25 October 2026

Baobab TMS at
[`9a4761f6a4c039cb000eb29503a748faa369d691`](https://github.com/baobab-platform/baobab-tms/tree/9a4761f6a4c039cb000eb29503a748faa369d691)
contains architecture and Foundation-0 template material. Its
[README](https://github.com/baobab-platform/baobab-tms/blob/9a4761f6a4c039cb000eb29503a748faa369d691/README.md)
expressly reports no runnable TMS service, carrier integration or active canonical
provider. Accepted TMS-0001/0002 establish mission and domain semantics;
TMS-TECH-01 is Proposed. Thamani's lock records that no canonical logistics wire
contract is consumed. A proposed endpoint/key or matching receipt object is not
an authenticated, governed provider invocation.

DEV-08 engineering can proceed on estate safety without claiming the missing
provider. Thamani #42 strengthens its existing BGX-03 read-admission seam:

- A server-only module requires current IAM identity and CP legal entity,
  Organisation, tenant, Market, capability/binding and transport-actor authority.
- A native object-policy decision must attest the exact shipment, Principal,
  context and binding, plus a sourced owner/custodian/intended-recipient
  relationship and an explicit tracking/event-proof read permission.
- The clock and upstream leases are rechecked after awaited calls. Future,
  stale or impossible snapshots and future/unsourced event occurrences refuse.
- A frozen display projection copies only admitted reference/time fields;
  invented carrier, ETA, custody, coordinates and arbitrary provider metadata
  cannot pass through a native-object spread.
- Unconfigured adapters and all outages return the same generic refusal.
  Prototype fixtures cannot become a fallback. No production endpoint,
  transport write, canonical contract, carrier acknowledgement or provider is
  activated by this source change.

Internal receipt types describe verified-adapter projections for future mapping
from accepted owning contracts. They are not new Shared/TMS network contracts.
The existing import seam is retained but its adapter requirements are stronger;
there are no connected production consumers to migrate. Thamani's runbook
`docs/frontend/dev08-logistics-admission.md` documents policy, scope, tests,
integration prerequisites, maintenance and rollback.

## Evidence classification

The local unit/component tests use synthetic receipts and UX fixtures. Type,
lint and formatting checks pass. The local package registry returned 401;
source checks used Shared Experience 0.3.1 at exact source commit
`83e5a4a5db7111fa4fbd3603559b1ef6136eaae3` in a temporary workspace while retaining
Thamani's immutable Shared package pins. CI subsequently identified vulnerable
Zod/Undici leaves; Thamani #42 pins the supported patched releases and registry
integrities without adding audit exceptions. Authenticated CI must independently prove the
published dependency archives install and all normal build/browser/security gates
pass before source merge.

## Final reviewed source

[Thamani #42](https://github.com/baobab-platform/thamani/pull/42) merged at
`8a18b0b1613b236f6107b3a6e2e76f9339184b46` after review of
`ae59299e0dc5bfacd8bfec61ed3cacbb341266d9`. All 32 reported checks completed:
25 successful checks and seven applicable skips. Authenticated frozen-lock
installation, dependency audits/security scans, source/type/unit/build/image
checks and browser keyboard/accessibility journeys passed. The final source
suite contains 60 synthetic unit/component tests; local register validation and
all 21 reporting regressions pass. The intermediate-clock-rollback review
finding is fixed and its regression passes.

Owner evidence is linked by the immutable `dev08-tha` baseline in the
implementation register, including [application/browser CI](https://github.com/baobab-platform/thamani/actions/runs/40160408847)
and [Foundation/security CI](https://github.com/baobab-platform/thamani/actions/runs/40160409478).
The patched dependency leaves install from their registry integrity hashes;
private Shared 0.3.1 archive pins remain unchanged. No new audit exception was
added. These are source/UX gates, with all twenty native INT-04 engineering
obligations still BLOCKED and no actual transport or host-teardown receipt.

This is source evidence. There is no real TMS runtime receipt, no transport
operation PASS and no native transport/host teardown observation. The mutable
EA-DEV register retains all twenty engineering obligations as BLOCKED, with
their original INT-04 parent scenario, no package completion date, and false
provider/protected/production acceptance. Source CI cannot promote those cells.
The finite engineering labels are not new canonical scenario IDs.

## Remaining execution order

Implement and qualify the real TMS runtime and accepted wire contracts, normal
IAM/CP provider/Organisation/Market/legal authority and native object policy.
Then compose Thamani's commercial quote/service-order responsibilities with
TMS-owned booking, tracking and sourced physical events. Trade Docs owns actual
document/proof versions and Regulations owns regulatory decisions; neither may
be inferred from a TMS read or frontend label. Conditional B2C interfaces remain
unqualified where accepted owner interfaces are unavailable; recipient status
never silently restores retail commitments.

Execute actual separate customer/partner, quote, booking, own/unrelated tracking
and proof-of-event cases under Infrastructure's guarded lifecycle. Exercise
wrong Market/legal actor, absent/revoked grant, invented carrier/ETA/custody,
recipient scope, duplicate/replay, dependency outage/recovery and full teardown.
Use original actual source/receipt hashes and preserve unavailable provider cases
as BLOCKED. Independent protected staging and production acceptance remains a
later promotion decision; it does not freeze ordinary development.
