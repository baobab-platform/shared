# DEV-00 — Decision and gate reconciliation

**Authority:** Accepted ADR-SHARED-043 and the Accepted EA-DEV programme.
**Observation:** 24 October 2026. **Delivery:** Shared source gate; no runtime
qualification, protected approval, provider certification or identity grant.

## Precedence and execution lanes

This is the single DEV-00 precedence table. It applies only to conflicting
development execution/acceptance restrictions. Domain authority, credentials,
tenancy, legal actors and native enforcement retain their owning contracts.

| Conflicting or retained rule | Ordinary isolated synthetic development | Optional Infrastructure #49 exercise | Protected staging / production |
| --- | --- | --- | --- |
| INT-03C independent-human topology prerequisite | Superseded by [ADR-043](../adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md); one technical owner may drive distinct synthetic actors through CP-owned bootstrap | Retained within this voluntarily selected exercise only | Actual independent authorised operators and environment approvals required |
| Shared #354 CMS development activation hold | Lifted by ADR-043; named consumer/validator rows are ACTIVE in the observed Shared registry; audience/scope/owner ceilings unchanged | Historical packet cannot broaden the selected frozen identity ceiling | Development identities cannot be promoted or reused; production caller lifecycle unchanged |
| Missing, failing or historical #49 packet | Cannot veto standing development authorisation; no appointment, signature or external WORM ceremony required | Blocks this optional exercise until its own reviewed conditions pass | A #49 development packet cannot authorise protected staging or production |
| Independent issuer/CP read-back and teardown | Automated distinct checking processes may observe actual issuer/CP facts and cleanup; source/image pins and retained redacted receipts required | Additional independent people/custody required as selected | Independent protected verification and custody required |
| Distinct maker/checker | One developer may operate two synthetic Principals; same-Principal consequential self-approval still denied | Independent authorised people as specified by the optional exercise | Actual authorised independent people where required by owner policy |
| Official incorporation and legal documents | Synthetic unverified initial facts allowed; no fictitious VERIFIED legal evidence | Optional worksheet does not verify real legal status | Current genuine legal/provider evidence required for the operation concerned |
| Seven INT-03C / fourteen NAB-03 cases | Meanings unchanged; individual PASS only for actual current real-component observations; unsupported or unexecuted cases BLOCKED | No older receipt is reclassified by this document | Separate protected acceptance; development PASS supplies no protected GO |
| Same-Principal denial, native PEP, current grants/actor scope, issuer audiences, lease and cleanup | Remain mandatory | Remain mandatory | Remain mandatory; no development bootstrap or synthetic credential path |

Missing/unknown environment fails closed. Ordinary development means an
explicitly marked isolated development database and private resources, not an
unlabelled nonproduction host. CP's guarded command is default-off, excluded
from its production image and has no production HTTP bootstrap route. IAM must
issue real scoped credentials. No orchestrator writes CP canonical tables.
The reusable development lease ceiling is 24 hours; narrower existing issuer
or profile limits, including the INT-03C 90-minute window, remain binding.

## Source reconciliation and concrete handoff

The [machine-readable register](ea-dev-implementation-register.json) pins each
inspected baseline, reviewed PR head and actual successful CI run URLs. Its
[readable view](ea-dev-implementation-register.md) is generated and checked in
CI. This is a scoped observation, not a new twenty-repository audit.

| Inspected source | Established fact | Remaining owner work |
| --- | --- | --- |
| Shared #373/#374/#375; current registry at `e1c0f4535e143a584dc8e03377129977d440a0cf` | Accepted programme and offline fixture source; named CMS development identities ACTIVE; production `nabhold-backend` remains PROVISIONED | Shared publishes this reconciliation/register; DEV-14 descriptor remains a later separate review |
| CP #433 at `3b1ca63f85dd18d9d82c162c2777ab3313091328` | Default-off guarded bootstrap; CP assigns canonical synthetic state; owner PostgreSQL CI passed | CP/Infrastructure compose with actual IAM subjects and current pins; no composed L4 inferred |
| IAM #137 at `ca5eb723c7845ed9a60e19fd0ef1a1e900d7b97a` | Native owner/verifier/deadline source and final-head workflows passed | DEV-03 integration and host-failure recovery still need actual proof; observed IAM main `0ad103606b9705fcb33c468ea01b54d8ce76f9ae` is newer and is not qualified by #137 evidence |
| Infrastructure #52 at `d573582e6302da40a68215746371980e096a8b3c` | #49 runbook explicitly makes its packet optional for development; exact-packet protections and CI passed | DEV-01 ordinary-development adapter must consume current Shared/CP/IAM locks and automate lifecycle/recovery |
| Infrastructure `int03c-lock.json` and `cms-lock.json` at that baseline | Historical source locks still predate ADR-043/CP #433; `cms_gate.py` describes the obsolete hold and returns nonzero for OPEN | Preserve historical locks/receipts; introduce a separately reviewed current development composition and update CI routing; never rewrite the old run as current qualification |

This Shared PR does not change Infrastructure execution. A technically blocked
adapter is **IMPLEMENTED_NOT_TESTED / NOT_IMPLEMENTED as applicable**, not a
new demand for independent development approval. DEV-00 Shared publication can
close while DEV-01 adoption stays open. Cross-repository execution closure is
not claimed until its owning implementation and receipts establish it.

## CI and merge policy

1. Shared CI validates the complete DEV-00..DEV-15 register, dependency graph,
   exact baseline SHAs/CI links, independent acceptance axes, stale observations,
   mandatory case inventory and generated readable view. Mutation tests reject
   missing cases, cycles, unknown fields and source-only runtime PASS claims.
2. The check runs on PRs and main when its script, tests, architecture records
   or workflow change. Passing it means **valid source reporting only**. It does
   not contact an issuer, CP, provider, database or #49 packet service.
3. Owning development CI must select the ordinary ADR-043 lane explicitly; it
   must not call the optional #49 packet as a universal prerequisite. An invalid
   selected optional exercise fails that exercise; it cannot change the
   ordinary lane's standing authorisation. Protected CI must reject development
   bootstrap/credentials and require its own independent approval evidence.
4. Source review and mandatory final-head CI must pass before merge. An absent
   provider, stale contract pin, failed native denial or missing cleanup blocks
   the affected runtime claim. Source-only CI cannot set an L4 case PASS.

The canonical [L4 matrix](ea-v2.2-integration-acceptance-matrix.md) remains the
scenario authority. The seven descriptive INT-03C labels and fourteen NAB-03
subcases in the register are obligation tracking, not new canonical IDs. The
fourteen CMS subcases follow Infrastructure's existing `cms_gate.py` inventory;
`draft-or-preview` is a denial for the narrow #354 caller. A later positive
editorial journey needs its own approved actor and cannot widen that caller.

## Register maintenance and gate closure

Each package records accountable team, dependencies, evidence/source baselines,
CI observation, environment, actual or missing scenario results, blockers, next
action, freshness, target/actual date, rollback and independent protected axes.
`NOT_ASSESSED` is an observation gap, not a progress milestone or a claim that
no implementation exists. Target dates are programme planning windows, not GO.
Missing completion dates remain null. DEV-13 dependencies apply only to the
selected protected release scope; unrelated providers cannot hold development.

DEV-00 is a source/reporting gate. This change's candidate snapshot truthfully
remains SOURCE_IN_PROGRESS pending review/CI; merging it establishes the Shared
delivery. At the next gate observation, record its exact PR/head/merge/CI in the
register and advance that row. Do not embed a guessed self-referential commit
SHA or claim a candidate merged before GitHub confirms it. The version history
and PR identify this change while it is under review. Other baselines are exact.

Update JSON, then run:

```sh
python3 scripts/ea_dev_register.py --write-view
python3 scripts/ea_dev_register.py --check
python3 scripts/tests/test_ea_dev_register.py
```

After seven days an observation is displayed STALE until rechecked; validation
does not refresh dates, fabricate receipts or globally freeze source work. A
stale record cannot be used as current release evidence. Runtime PASS requires
real-component evidence and complete cleanup; staging, external certification
and production remain false in this development-only register and belong to
separate protected records. Reverting this change restores the prior reporting
files only; it must not reopen a human approval hold superseded by ADR-043.
