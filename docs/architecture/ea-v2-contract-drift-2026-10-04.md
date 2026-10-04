# EA v2 consumed-contract reconciliation — 2026-10-04

Governing plan: EA Plan v2 sections 6, 8, 10, 48 and 51. Authority boundaries:
Accepted Shared ADRs 014/017/018 and provider registration governance; the engine
ADRs and the exact pinned contracts. This is source compatibility evidence,
not certification, canonical activation or deployed acceptance.

## Exact baselines and review scope

Reviewed contract target: Shared `6899a2d8f143bf23d36c4f4ac904e0a1e10c3cea`.
The census Shared main `97e5691ecd0402c339338c0289495141e5799acc` merges #210;
the three changed paths are architecture documentation. Every consumed contract
is byte-identical to the reviewed target. Documentation-only head drift does
not require runtime changes or another fleet-wide re-pin.

The owner subsequently merged the initial fleet evidence record in Shared #211
at `47106f3bc8ec935cc47efebab246018234e31420`. This follow-up completes the
final-head run evidence after Trade's full regression suite finished. This
additional Shared main advance also changes documentation only.

CP main `c84063cb07dce76e1ffac4b12fa29c5e4e5ec855` already pins the target.
IAM #62 was merged by the owner at `14373271d0e4d824671f8e451dff8d6bbf519147`;
its reviewed head `286665f8b4a6ceb680371a1bfd0a38c4071c0e02` passed all
four applicable workflows, including exact-pin live Ory/CP verifier proof.
No duplicate CP/IAM pin PR is necessary.

The six new consumer PRs reconcile the old pins below to the reviewed target.
They were created as drafts; the owner has marked ERP #56 and Trade #115 ready for review.
All six remain unmerged and are not main baselines. No merge, deployment or permission grant
is performed by this task.

| Consumer | Audited main | Old Shared pin | Reconciliation PR | Proposed head |
|---|---|---|---|---|
| baobab-cms | `19deac119b3232ccbf29f1889b62cfabb43ceeb1` | `b63ce52a20d1b6f8acc41d085913c6025d6c859c` | [#21](https://github.com/baobab-platform/baobab-cms/pull/21) | `676770ba2aeccf795d1a1dceff8f2257252e3a13` |
| baobab-pulse | `0cece91cc7c82bb4eaa49695a8a35ecab0de21cd` | `b63ce52a20d1b6f8acc41d085913c6025d6c859c` | [#30](https://github.com/baobab-platform/baobab-pulse/pull/30) | `bdc3f9b1c97abf47c176441dca1327efb2ed9c22` |
| baobab-trade | `78d16b84379448aada6d5eab583c7eb8c2a4b7f5` | `b063f8a8df3f012baadf068aa9ba312d83929e69` | [#115](https://github.com/baobab-platform/baobab-trade/pull/115) | `c423b8dde9a7fc32449befd94da88440bb17b9cd` |
| baobab-erp | `51c0de226bbb7d480b306f3b85bb3f783fa355cf` | `0233eb30bcf4070344039e83b70d16248963dd64` | [#56](https://github.com/baobab-platform/baobab-erp/pull/56) | `a8f75a07893656787b0f92ec8027e500f6d6f95e` |
| baobab-subscriptions | `0019f3a283d75f3a9f156d79f1477c8db667d014` | `3a8230ebbfe05ede65976363770f0867fa5eac45` | [#27](https://github.com/baobab-platform/baobab-subscriptions/pull/27) | `a75367dfc7ecf57c7ec0da2ee8381d0ec2562ea0` |
| baobab-payments | `fc144da464e8388b47cf4ccc1beef25bdef64656` | `3a8230ebbfe05ede65976363770f0867fa5eac45` | [#21](https://github.com/baobab-platform/baobab-payments/pull/21) | `0dabf13207b51fb0eed6711b739953411538958e` |

## Consumed semantic changes

| Consumer | Changed consumed contracts | Reconciliation |
|---|---|---|
| CMS | None of its three content contracts changed | Explicit provenance update; content resolution remains planned-only |
| Pulse | CP domain schema | Refresh exact fixture; additive deployment/release/status identifiers and drift object kinds; existing used grammars unchanged |
| Trade | CP OpenAPI, platform context schema, workload registry | Existing resolve/redemption sends the incoming bearer and does not share stored contexts across callers; new CP operations are not consumed. Reject null expiry, permit omitted expiry for resolution, exact-pin schema tests |
| ERP | ERP OpenAPI and provisioning request schema | Implement ERP API 1.1 caller-bound context validation before storage and replay; declare new consumed CP OpenAPI/context/market contracts |
| Subscriptions | CP domain schema, capability registration JSON | Refresh exact vendored files; provider lifecycle ACTIVE → DRAFT; simulated and production_permitted=false retained |
| Payments | CP domain schema, capability registration JSON | Same domain additions and DRAFT-only provider registration reconciliation |

No locked path is removed. No local operation is promoted to a canonical
capability. Newly catalogued scopes do not grant permission.

### ERP authority and replay

Four operations require CP-authorized `context_id`: provisioning command and
state, order-consequence read, and inventory availability. The two mapping reads
retain token-tenant authority as Shared expressly specifies.

ERP sends the **actual incoming caller bearer** as `subject_token` to CP's
validation endpoint, authenticated separately as a registered ERP validator.
CP owns canonical principal binding and registered validator audience checks;
ERP never substitutes locally asserted issuer/subject facts. Context must be
bounded/current and the response must name the exact requested context.
The optional incoming tenant claim and required provisioning body tenant may
only agree with the validated tenant. Rejection precedes any database, replay
lookup, provisioning or resource read. Missing/malformed context is 400,
all authority refusals/tenant disagreements are indistinguishable
403 `ERP_CONTEXT_REJECTED`, and unavailable validation is retryable 503.

Fresh context is authorization evidence, excluded from request fingerprint.
Caller, tenant, approved-plan tuple and all provisioning intent stay bound.
Plan id/version/digest and Finance baseline remain independent requirements.

ERP's optional validator wiring fails closed when unavailable; no
`context:validate` grant or `validates_audiences` registration is created.
Deployment token delivery, registry approval, IAM issuance and actual CP/
resource-server acceptance remain separate governed work. Tests with a mock
validator prove boundary behavior only.

## Validation and remaining merge blockers

The final consumer runs are complete at the proposed heads in the table. A successful
contract suite never waives an unrelated required security gate.

- Pulse: all six applicable final-head workflows passed, including exact Shared
  HEAD and byte fixture checks, full PostgreSQL/Qdrant suite and Foundation.
- Subscriptions: all four applicable workflows passed, including Java/Postgres
  tests, vendored byte conformance, exact Shared HEAD and Foundation.
- Payments: all four applicable workflows passed, including Rust tests, vendored
  byte conformance, exact Shared HEAD and Foundation.
- ERP: final-head repository CI (six jobs), security and action pinning passed;
  137 integration tests and 42 exact-pin conformance tests passed.
  Foundation container scan fails on critical CVE-2026-49875 in upstream
  org.apache.cxf:cxf-core 3.6.5. Reported fixed versions are 4.2.2/4.1.7, a major
  OSGi runtime compatibility change, not a contract adaptation.
- Trade: all repository CI jobs passed, including exact-pin Shared conformance,
  verify (format/lint/typecheck/tests/build), production infrastructure integration
  and the full core-module regression suite. Release readiness and security
  workflows passed. Foundation dependency/container security remains failed.
- CMS: repository CI passed. Foundation dependency audits fail with 21 findings
  (8 high, 13 moderate) in its unchanged dependency graph.
- Trade Foundation dependency audit: 96 findings (81 high, 15 moderate).
  Container scan finds high CVE-2026-93687 in braces 3.0.3; no fixed version is
  reported. The PR changes no package manifest, dependency lock or image.

### Final-head workflow evidence

Each run below belongs to the exact proposed consumer head in the baseline table.
Successful source compatibility does not establish a passing merged main baseline.

| Consumer | Applicable workflow conclusions |
|---|---|
| baobab-cms | [CI](https://github.com/baobab-platform/baobab-cms/actions/runs/37178024248): success; [Foundation Repository Gates](https://github.com/baobab-platform/baobab-cms/actions/runs/37178024681): failure |
| baobab-pulse | [Security — Python (Bandit + pip-audit)](https://github.com/baobab-platform/baobab-pulse/actions/runs/37178245983): success; [Foundation Repository Gates](https://github.com/baobab-platform/baobab-pulse/actions/runs/37178246197): success; [Enforce Action Pinning](https://github.com/baobab-platform/baobab-pulse/actions/runs/37178245907): success; [Security — Secret Scanning](https://github.com/baobab-platform/baobab-pulse/actions/runs/37178245923): success; [Pulse CI](https://github.com/baobab-platform/baobab-pulse/actions/runs/37178245705): success; [Security — CodeQL](https://github.com/baobab-platform/baobab-pulse/actions/runs/37178245941): success |
| baobab-trade | [Foundation Repository Gates](https://github.com/baobab-platform/baobab-trade/actions/runs/37178489058): failure; [Security](https://github.com/baobab-platform/baobab-trade/actions/runs/37178488572): success; [Release Readiness](https://github.com/baobab-platform/baobab-trade/actions/runs/37178488302): success; [CI](https://github.com/baobab-platform/baobab-trade/actions/runs/37178488274): success |
| baobab-erp | [Enforce Action Pinning](https://github.com/baobab-platform/baobab-erp/actions/runs/37178545608): success; [Security](https://github.com/baobab-platform/baobab-erp/actions/runs/37178545708): success; [Foundation Repository Gates](https://github.com/baobab-platform/baobab-erp/actions/runs/37178545904): failure; [CI](https://github.com/baobab-platform/baobab-erp/actions/runs/37178545436): success |
| baobab-subscriptions | [Enforce Action Pinning](https://github.com/baobab-platform/baobab-subscriptions/actions/runs/37178027939): success; [Security — Secret Scanning](https://github.com/baobab-platform/baobab-subscriptions/actions/runs/37178027889): success; [Foundation Repository Gates](https://github.com/baobab-platform/baobab-subscriptions/actions/runs/37178028207): success; [Java CI](https://github.com/baobab-platform/baobab-subscriptions/actions/runs/37178027718): success |
| baobab-payments | [Foundation Repository Gates](https://github.com/baobab-platform/baobab-payments/actions/runs/37178028668): success; [Security — Secret Scanning](https://github.com/baobab-platform/baobab-payments/actions/runs/37178028434): success; [Enforce Action Pinning](https://github.com/baobab-platform/baobab-payments/actions/runs/37178028435): success; [Rust CI](https://github.com/baobab-platform/baobab-payments/actions/runs/37178028168): success |

No scanner exclusions, audit-level changes, waivers or ignore-unfixed settings
are added. Resolving the CMS/Trade dependency and ERP/Trade image findings requires a separately
reviewed remediation; the reconciliation PRs remain blocked until required
security checks pass. Advisory counts are this run's observations, not unique
vulnerability counts or a permanent baseline.

After owner review and passing required checks, merge the eligible consumer
PRs and rerun the fleet lock/drift check. Until then, distinguish proposed pins
from main. EA-01B namespace cleanup and EA-01E ongoing governance remain open;
EA-03D capability-based billing invocation is a separate next source task.
Federated audience mechanics, live consumer routes, signer lifecycle,
activation/certification, Digital Estate unfreeze and permanent deployment remain held.
