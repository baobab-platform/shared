# DEV-11 — engine-local qualification checkpoint, 4 November 2026

This dated evidence review records an engineering increment under EA v2.3 and EA-DEV. It is not an ADR, programme acceptance receipt or deployment approval. The original [Infrastructure #72 audit](https://github.com/baobab-platform/infrastructure/blob/65931ab9892b829b0e0b1ca23c53199ba1216e8b/docs/assessments/infrastructure-72-audit-20261104.md) remains an immutable audit of its recorded source. This checkpoint follows its implementation corrections and subsequent real runs.

## Reviewed source and CI

| Owner | Exact reviewed source | Result |
| --- | --- | --- |
| Infrastructure #72 | `65931ab9892b829b0e0b1ca23c53199ba1216e8b` | All 15 workflows pass; actual eight-owner dispatch-only join remains unexecuted. |
| Trade #188 | `55659409a7e4787c0d70a69d4c1301f13d7fc219` | Full CI and real broker workflow pass. Optional temporary formatter helper was skipped and is not counted as a pass. |
| ERP #125 | `a118cc16e930f1bb6e693eb9b28657d1395e0b88` | All seven workflows pass, including rebuilt real iDempiere 13 qualification. |

ERP's exact companions are accepted CP main `6fee9fe9537409df428a2e3dd7b8f78ff8d1d456` and current IAM #153 `fae32b20187b2201e6070c382f563e170773e692`. Local Python 3.12 checks pass 212 Infrastructure development tests (including 29 verifier tests), 94 INT-02 tests, 13 focused Trade tests and 397 ERP unit tests. Actual owner qualification uses the pinned Actions environments, including Python 3.14, PostgreSQL 17, Node 24 and the real iDempiere JVM where applicable.

## Independently reviewed original evidence

The following originals were downloaded independently, their ZIP SHA-256 values matched to GitHub, and their receipts checked with Infrastructure's verifier. Raw identifiers, credentials, topology files and provider logs are not copied into this assessment.

| Owner profile | Run | Original artifact | SHA-256 |
| --- | --- | --- | --- |
| IAM/CP authority, isolation and W3C | [41852352906](https://github.com/baobab-platform/infrastructure/actions/runs/41852352906) | 13336636653 | `59b1782ff73c09be6fb30518ec6ea7c16625996bae7ad7ead70a339a898f748a` |
| Trade/RabbitMQ/ERP inbox component | [41854342793](https://github.com/baobab-platform/baobab-trade/actions/runs/41854342793) | 13337126723 | `0f8fe5fc9619863f8bcc4aeb585cab98f83fbf87c422bd897d6c89a2e3c88638` |
| Native ERP engine-local effect and recovery | [41856464924](https://github.com/baobab-platform/baobab-erp/actions/runs/41856464924) | 13337154424 | `09eddbe312fe13662653b6224f065c385d1226617e04474a9b04198ba5d06262` |

IAM/CP passes all five existing L4 cases, including the own-record prerequisite and neighbour isolation, seven DEV-11 authority/W3C checks, exact harness readback and teardown.

Trade observes actual PostgreSQL outbox persistence, RabbitMQ confirms, both prescribed producer/consumer crash windows, fenced reclaim, immutable replay, DLX and unroutable negatives. The independent exported component graph contains seven spans and six parent edges across Trade, publisher and ERP. Its native-origin checker correctly records `NATIVE_ORDER_ABSENT`. Imported ERP `88c2cdca` and Infrastructure `a4cc31b1` are historical companions: the verifier independently refuses this receipt when presented as the current composite.

ERP now observes fresh real Hydra/CP authority and documentary checks, a real JVM-created native sales order, independent native and CP/JVM attribution readback, and one native order under redelivery. After a deliberately lost committed result the worker returns a retry, then independently adopts the same native order as `ADOPTED_NATIVE_ORDER`. Revocation blocks the next order. All five original native-effect/recovery/lineage/cleanup receipts pass. Cleanup records zero remaining run-owned containers, networks and volumes, and removal of the temporary directory.

## Corrections and maintenance boundaries

Infrastructure reuses #69's accepted-source reconciliation, aligns fixture grants with CP's runtime environment, and strengthens exact-source/original-receipt and merged-owner checks. It requires the actual native-origin refusal step and original receipt for this synthetic broker profile.

Trade binds the complete SQL LIKE pattern to avoid psycopg's literal-percent parsing failure. Its synthetic-origin refusal remains mandatory; no native B2B positive is inferred.

ERP preserves exact PostgreSQL numeric native IDs and foreign-company negatives, requests the already registered context-redemption scope, and retains strict native business comparisons with closed private diagnostics. It checks both live dictionary and physical reference widths before creation and refuses overlong canonical inputs without truncating them. Fresh synthetic fixture IDs fit the native reference from the outset. The cross-UID request-file correction applies only to the existing disposable bridge.

Long real Medusa IDs still need a reviewed native-reference mapping or native extension. Synthetic short IDs do not implement that production integration. Native sales-order creation also does not qualify financial-ledger posting.

This checkpoint supplies bounded progress for existing [BA-AUD-080, BA-AUD-087 and BA-AUD-092](../findings-register.md), and Infrastructure #72 F05. Their original broader closure requirements remain unchanged; no second acceptance register or new authority is created.

## Remaining acceptance gates

**Engine-local native ERP qualification is demonstrated. DEV-11/L4-OPS-01 remains BLOCKED.**

A genuine ENFORCED Medusa buyer/seller/spend commitment, its same-transaction event, the same event's authenticated cross-engine exported lineage, a reviewed source-compatibility resolution, and the actual independent eight-owner join remain required. Full N02/N07 browser/native booking qualification is separate. Source/component CI must not replace these gates.

The current PRs remain open because their remaining specification and cross-owner evidence requirements are unsatisfied. No protected deployment, staging/production authority or provider activation is granted. If an original expires or becomes unavailable, this dated digest record does not replace the required requalification or approved evidence custody.

The [machine-readable companion](2026-11-04-dev11-engine-local-qualification.json) preserves the exact sources, runs, artifact digests, bounded outcomes and remaining gates. Qualification is recorded here so reviewed runtime heads remain fixed; no executed source is relabelled by a later documentation commit.
