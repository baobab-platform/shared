# Shared #410–#413 and companion implementation audit — 29 October 2026

**Ruling:** the Platform Owner authorised comprehensive audit, correction, design acceptance and merge after satisfactory final-head review and green CI. Corrected Shared #413 is accepted **design**, merged at `1fce3c36783310f33d79ba0996a996d00c4c5abe`. All 30 EA-XB operational cases remain NOT_RUN. Historical XBE-01..18 and the canonical L4 registry remain unchanged. Design acceptance does not register capability keys, issue workloads, qualify native providers or approve protected/production operations.

## Scope and precedence

Reviewed Shared [#410](https://github.com/baobab-platform/shared/pull/410), [#411](https://github.com/baobab-platform/shared/pull/411), [#412](https://github.com/baobab-platform/shared/pull/412), [#413](https://github.com/baobab-platform/shared/pull/413), their conversation/review findings, merged [#409](https://github.com/baobab-platform/shared/pull/409), CP [#448](https://github.com/baobab-platform/baobab-cp/pull/448)/[#449](https://github.com/baobab-platform/baobab-cp/pull/449), IAM [#142](https://github.com/baobab-platform/baobab-iam/pull/142)/[#143](https://github.com/baobab-platform/baobab-iam/pull/143), and the entire TMS [#19](https://github.com/baobab-platform/baobab-tms/pull/19)–[#26](https://github.com/baobab-platform/baobab-tms/pull/26) stack.

Controlling boundaries remain Shared EA v2.3/EA-DEV, accepted Shared identity/capability/isolation/authority decisions, CP BCP-014/017/018, IAM ADR-0007/0033, Trade commercial/ERP separation and accepted TMS 0003/0004/0010/0013/0020/0021. A current context or generic successful ExecutionOperation is not native transport, purchasing, finance or document authority. Review comments were treated as defects to reproduce and correct, not as permission to waive failed checks.

## Shared reconciliation

| Finding | Correction and evidence |
| --- | --- |
| #410 records component DEV-07 progress, not full purchasing/ERP/provider completion | Preserve its historical findings. Trade v1 RFQ identity belongs to Trade under that exact contract; older standalone RFQ schemas are distinct resources. Buyer commitment and provider qualification remain separate gates. |
| #411 universally combines manufacturing with an external buyer whose ledger is unobservable | #413 preserves the execution objective and all historical IDs but makes future claims use CORE plus applicable AGR/MFG/NET/LOG, exact direction/product/actor/provider and evidence class. External seller AR never proves buyer AP. |
| #413 onboarding-only scenario implicitly requires all seven NET cases | Closed boolean claims, independently pinned case predicates, ordered applicable IDs and reasoned exclusions exactly partition all 30 cases. Onboarding requires XBN-01..03. Claimed bilateral accounting, heterogeneous providers and CRM still require XBN-04..07. |
| Optional CRM and agricultural processing cannot become universal requirements | CORE XBC-02 always requires the native commercial fence; XBN-07 proves an actual CRM handoff. Agricultural processing, cooperative representation and non-tenant exchange have explicit applicability. The coffee reference is explicitly non-tenant. |
| Old normative plan could override new scoped composition | Reconciled plan, adoption matrix, programme overlay, dashboard and index; original 18-case manifest preserved byte-for-byte. All design execution statuses/evidence remain NOT_RUN/null. |
| #412 exposed #409's runner-policy violation | Move the TMS design workflow to the required ubuntu-26.04; preserve the strict policy. |
| Dependency provenance comments and invalid Dependabot label | Verify four action SHA pins against upstream release tags, correct version annotations, remove the observed nonexistent github-actions label. Permissions and artifact retention were not widened. |

Both EA-XB validators and all 19 acceptance-design tests passed locally. Shared #413 final head `135bd1efdef25ea777bc68f9a86f7565028b5ca9` passed 33 checks with all review threads resolved. Shared #412 final head `f4d4de12fbe46800cf41025d91ca77a0c926c818` passed 37 checks and merged at `e6a8e1480ed0c40b471211b2d3880a73767de624`.

## CP and IAM source authority

| Finding | Correction |
| --- | --- |
| Overlapping CP #448/#449 duplicate boundary packages and stale “Shared not accepted” claims | Consolidate into one internal/tmsauthority package in #448. Port closed bounded duplicate-key-safe parser, corrected UUID grammar and full operation/resource mapping. Close #449 as superseded. |
| CP diagnostic lifetime allowed 30 seconds instead of accepted design's five | Enforce five-second ceiling. Every plausible or forged candidate still returns HELD, Executable=false, ActivatesProvider=false. No route or grant is installed. |
| CP registration test depends on another test seeding the catalogue | Explicitly project the pinned canonical catalogue before provider registration, matching startup order; do not invent keys or weaken registration validation. |
| Overlapping IAM guards each miss part of reserved TMS issuance | Consolidate development client prefixes, suffixed audiences, native scopes, nested human profiles/mappings and direct provider evidence. Guard Validate, workload Claims, HumanConsent and HumanClaims, retaining canonical request admission. |
| Direct hooks can serialize multiple native scopes from one unvalidated list entry | Reject noncanonical separators, Unicode/control bytes, wildcard and quote escapes in every workload/human profile and provider grant before serialization. Positive unrelated-profile and negative smuggling regressions pass. |
| Security gates expose vulnerable JOSE and Guava | Upgrade root/nested JOSE to 4.1.6; migrate isolated Hydra/Fosite/Oryx candidate from unsupported v3 consistently. Patch the pinned Keycloak Guava dependency with exact checksum-verified 33.7.2-jre jar before augmentation. No vulnerability ignore or scanner weakening. |
| CP consumer fixture security changes invalidate historical provenance | Preserve verifier/licence bytes, independently pin their hashes and original upstream lock hashes, reverse exactly two reviewed overrides. No edited snapshot is claimed to be unchanged upstream dependencies. |

CP #448 final head `b862e6a8bbbba6d054927171fe46ff1adf9077ef` passed all 32 checks and merged at `03e53eae95b6a277bd866a617653afb6634262bb`. Local Go 1.27.3 race tests and vet passed for its consolidated package. The source guard is not an implementation of the active Shared authority API.

**IAM #143: MERGED** at `7958a93808bf23dca8752598ca97fb0292a7ac4d`, reviewed head `d38d5f69c69770027b332da3e7f648f078cdca6f`, all **47 final-head checks passed**, with no unresolved review threads. All three Keycloak variants, both real Ory native flows, strict source/container scans, token-profile and federation checks passed. #142 is closed as superseded. Local tokenprofile race tests, exact snapshot verification and three tamper-rejection cases, isolated native Hydra and tagged package builds, JWT/token-bearer tests and upstream RSA/private-header regressions also passed. The final canonical-token scope hardening was verified by repository CI after the workspace connection became unavailable. No issuer/credential allocation or native TMS capability is activated.

## TMS review corrections and database proof

| Review defect | Enforced correction |
| --- | --- |
| Optional/untimed calls hide reversed chronology | Carry latest known instant across the complete ordered call list, including gaps. SQL checks all known arrival/departure instants. |
| Invalid calendar dates normalize to different dates | Check calendar components, leap years, clock and offset bounds before UTC conversion. |
| Legs can reverse progression or repeat a pair | Leg sequence matches its origin call position and adjacent destination; duplicate/out-of-order itineraries reject. |
| NULL predecessor bypasses linked revision history | Revision >1 explicitly requires a non-null immediately preceding revision and FK. |
| NULL estimate source/unit/policy bypasses provenance | Require all estimate provenance fields together; append-only incomplete estimates reject. |
| Call sequence mutation invalidates existing legs | Referenced call sequence is immutable; movement custody serializes schedule writers. |
| Movement-side repositioning change bypasses cargo veto | Validate both parent update and child insertion under the same movement lock. |
| Independent valid schedule writes combine into an impossible journey | Actual two-session PG17 test requires exactly one winner; parent custody and chronology checks preserve the invariant. |
| Capacity booking may consume another carrier's pool | Lock and match carrier identity as well as tenant/operating organisation/legal entity/market. |
| Rounded quantities break identical replay | Reject unrepresentable numeric precision, NaN/infinities and overflow before allocation; prove exact fractional replay and release. Check pool validity at wall-clock time. |
| String planRevision bypasses integer representation | Require a positive safe integer exclusively, including digest input. |
| Transaction-start now() misclassifies lease expiry | Recheck clock_timestamp() after locks, and test long-transaction expiry/recovery. The private SQL custody lease remains UNVERIFIED, separate from the five-second CP authority claim. |
| IAM may expire during asynchronous CP readback | Recheck the current clock and issuer lifetime after CP returns. |
| Cleanup errors could be hidden | Strict cleanup with project-scoped container/volume/network readback; secrets removed by trap. |

42 focused local Node tests passed. Actual PG17 CI exercised revision CAS, schedule race, complete provenance/history negatives, carrier/quantity replay and capacity race, bounded lease recovery, FORCE RLS and public-function denial. Source/SQL fixtures prove first-party custody only; synthetic signed carrier readback is not an external carrier qualification.

| PR | Reviewed head | Merge | Final checks |
| --- | --- | --- | --- |
| TMS #19 | `1cd168f3ea04d033f4aef71d4391ef938a692368` | `9d641b9e47f42bc2d623af42059611a7905746e4` | 10 |
| TMS #20 | `80d312d9032254cf5b8614a187ae6e686db70d76` | `6ef57ec106071b6d46b099d1669924e0b8b49a5c` | 8 |
| TMS #21 | `98e70ae28d38dcad7103694ebef8e9792b15f178` | `c695ae767b15ba7af72ab35306fd051001a635ce` | 8 |
| TMS #22 | `03b9af61823870dfbf8d8a8078199f67a256719d` | `5e92962a0011699a9e46ba256d5faeb79d53f99e` | 4 |
| TMS #23 | `b2616ddfbebf85ab4662917f29fdcfc1734d9c63` | `ea0ea8d66c415217cf044efd8e45dab22253ada0` | 8 |
| TMS #24 | `6ebf0bfb46fdd36969f6e769a56b082d526dfeb4` | `596561c70e198faa9dcb56892b89f7e506cfbb56` | 8 |
| TMS #25 | `568c549d41e4e2feb83a88f0f5c7695a5a5b958d` | `05060862c45194237ddc1b2509925fafc1d4162b` | 4 |
| TMS #26 | `9a5c10bace6219db99d58c86eeab071c40d1639f` | `aa0565a46b089d53ff6e9916df3ed0eec19dcf0d` | 8 |

All twelve substantive TMS inline review findings were corrected and resolved. Stacked branches were retargeted and merged into main in dependency order. No source helper can enable booking, dispatch, provisioning or capacity effects through a caller callback, vendor token, local flag or plausible fake CP result.

## Continuing engineering gates

ERP #116 remains manufacturing/costing; ERP #117 separately tracks provider-neutral CRM inside the ERP repository. Trade Docs #20 tracks exact-version external disclosure and proposed TDOC-0018 adoption. Regulations REG-0027 is not a reversed universal corridor rule. Those issues are not implemented or provider-qualified by accepting #413.

DEV-07 remains open for real RFQ/quotation lifecycle, actual atomic buyer commitment authority, native ERP/provider and documentary integration. Supplier outbox/row-lock/ERP identity corrections already merged in ZuriBeans #138/#139 remain valid component work. Trade #181's bounded workload transport passed 34 checks and merged at `c659dd933104f50cd9b6cebcf1f42ba1b2ce3d27`.

Infrastructure #67's earlier BFF HTTP attempt remained unqualified: its failed receipt had no accepted component report despite independent CP/issuer cleanup and host teardown. Closed cleanup-stage diagnostics identified native API-key deletion before revocation, which pinned Medusa 2.21.2 explicitly refuses. Trade #182 corrected the exact owned key's immediate revocation, independent revocation readback and deletion; foreign/secret keys and failed/future revocation remain errors. #182 is merged at `435207d3729efb1be5162bee15034584348ecb8b`. The failed attempt remains historical evidence; the fresh qualification below does not relabel it.

## Fresh DEV-07 BFF HTTP component qualification

Infrastructure #67 reviewed head `712c140eefb923408cf6d7fe08b2329f80f51940` passed the real [development qualification run 40831958591](https://github.com/baobab-platform/infrastructure/actions/runs/40831958591), including job `123308088424`. CI checked the candidate merge `d2ee4e8a2182d7b04b53a5bb858217b049ee5ef0` against base `0538e5040a9080a7dd9bd937bc24f2d892d6af22`. All eight associated workflows succeeded; all 35 applicable jobs passed, with six inapplicable jobs skipped. Both inline review threads are resolved; the edge recreation correction applies its new network alias before health probes. Infrastructure #67 merged at `ce81ca83574804b4f81c7cb0969d970310b6576d` after review of that unchanged head and base.

The retained [artifact 12879880298](https://github.com/baobab-platform/infrastructure/actions/runs/40831958591/artifacts/12879880298), `dev07-bff-http-evidence`, was downloaded independently and its ZIP digest and both JSON report/hash pairs verified. Run `2662afd16258eff15c628b2584831f4b` records all eight observations true: native Next/IAM session, current CP-matched Trade HTTP context, CSRF denial, foreign Organisation denial, membership suspension, Redis custody outage/recovery, issuer-consent revocation before session expiry, and native fixture cleanup. Independent runtime identity, CP binding withdrawal, issuer cleanup and host teardown are true.

| Evidence | SHA-256 |
| --- | --- |
| Artifact ZIP | `9577f9d1ea9fc0a957899bbee2d8d1d96044b937d84e664418791b7c16e3ca9a` |
| Final BFF suite | `96736c8bac5991db04ae964136b6422701b1b4873d362649c85588edb8881a3b` |
| Completed lifecycle receipt | `dceafb576160fa71252d5c799c6a67482c52a5eea63d8423a12cbe1fc7de125f` |

The exact tested owners remain Shared `2fde03e2f5f3a8a6cbc1e2081b4859fdccc1bb53`, CP `695f08112898f65b17a4ec90b680720526b64dc4`, IAM `f7c13704b3161e72075bd245ae439dc839624625`, Trade `99f819459ddd1b026f1bcc915856a56ee2acfbbc`, and ZuriBeans `71296d8a08b46074e0fdd95c60576ffceec478a5`. This proves those immutable versions, not later CP/IAM/TMS changes. Future owner changes require requalification.

**Outcome:** the final wrapper records `bff_http_qualified=true` only after independent disposal. The private component correctly retains `bff_http_qualified=false`, since it cannot witness host teardown. Evidence class remains `REAL_COMPONENT_SYNTHETIC_DATA`; `domain_qualification=NOT_EXECUTED`. INT-05, provider, protected and production qualification remain false. The original direct-handler cases, historical INT-05 evidence and all 30 EA-XB operational cases remain unchanged.

### Next DEV-07 engineering sequence

1. Implement and qualify the real Trade-owned RFQ/quotation lifecycle using current IAM/CP authority, supplier membership and tenant/Organisation/Market isolation.
2. Implement and prove buyer authority at the native database commitment boundary, including receipt/reservation, exact amount/currency, replay/concurrency and rollback negatives.
3. Connect native ERP and document providers with governed mappings and exact documentary versions; prove their positive and denial paths independently.

BFF HTTP context success cannot substitute for any of these commercial/provider gates. No purchasing operation or native commitment fence is activated by this component qualification.
