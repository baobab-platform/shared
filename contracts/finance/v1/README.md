# Finance F1 — corporate ledger, journal and statement wire contracts

**Lifecycle: DRAFT / EXPERIMENTAL. Semantic owner: baobab-erp.**
Shared publishes vocabulary and wire validation. ADR-SHARED-033 remains Proposed;
merging these draft files does not accept that ADR, certify ERP support, allocate
an IAM scope, activate a CP binding, pass L4 or authorise production.

## Interfaces

| Capability | Request / response | Purpose |
|---|---|---|
| `finance.ledger.read` | `ledger-read-*.schema.json` | One authorised book: chart, period balances or dated entries |
| `finance.journal.manage` | `journal-manage-*.schema.json` | Restricted draft/submit/approve/post/reverse commands |
| `finance.statement.read` | `statement-read-*.schema.json` | Trial balance and policy-defined income/balance-sheet/cash-flow statements |

`domain.schema.json` reuses ERP boundary IDs, decimal strings, currency and the
existing immutable FinanceBaseline reference. `examples/manifest.json` indexes
all synthetic examples, including the shared RFC 9457 denial shape. No example
is real accounting, legal evidence or a provider approval.

## Authority and placement

CP/IAM establishes the current caller, Tenant, PRIMARY Organisation, operation,
market, effective legal actor/mandate, entitlement, binding and provider instance.
ERP independently validates its approved book/FinanceBaseline, document policy
and native posting veto. A browser cannot provide those permissions in JSON.
No Principal, Tenant, legal-actor identity, approval assertion, native Client/Org
or provider selector is accepted in a request. `book_ref`, `account_ref` and
`journal_ref` are opaque ERP boundary references, never native database IDs.

A corporate relationship grants no subsidiary access. Every selected book and
account must belong to the exact currently authorised legal entity. Existing
`erp:read` or another scope must not be assumed to grant these new finance
capabilities; resource-server permission policy requires its own accepted change.
No new scope allocation is made here.

## Read and historical semantics

Every query names an ERP-owned `book_ref`, inclusive `period_start`/`period_end`,
`as_of` and explicit currency. F1 currency means the selected book's functional
currency, not a Tenant/market default or implicit FX conversion. Reporting in a
different currency requires a later approved reporting/FX policy. ERP validates
ordered periods, cut-off/freshness, account membership and book currency.

Ledger responses echo `view` and `posting_state` and use distinct closed shapes:

| View | Returned facts |
|---|---|
| `chart_of_accounts` | Boundary reference, code, name, account type, normal balance, postability and status |
| `balances` | Opening balance, debit/credit activity and closing balance, each explicit Money |
| `entries` | Entry/journal/account references, accounting date, posting state, signed debit/credit, currency; posted rows also carry posting instant and exact historical baseline |

Signed native correction/reversal facts remain signed on reads. The positive
magnitude rule for **manual draft instructions** must not erase legitimate
historical ledger facts or negative period activity. Accounting date and actual
posting instant are different facts (ADR-ERP-008).

A read snapshot names every approved historical baseline version represented in
`finance_baselines`; a period may span several versions. A baseline superseded
today is not rewritten as the current version. ERP must verify that all listed
baselines belong to the same authorised legal entity and that posted entry
lineage is included in that set. Missing historical lineage requires an explicit partial/withheld/denied
outcome under ERP policy, never a fabricated current-baseline attribution.
Current access checks still apply to historical reads. New writes need the effective approved baseline under current policy.

Pagination carries opaque `cursor` **and** `snapshot_id` together. ERP must bind
them to scope, view, posting state, principal and current authority; changing the
query or losing authority invalidates continuation. Responses retain immutable
snapshot/data versions. Default posting selection is POSTED; a JSON Schema
`default` is only an annotation, so the provider must apply and echo that policy.
DRAFT/ALL requires independently established extra authority. Never sum a single
page as if it were the whole ledger.

`complete`, `partial`, `stale` and `withheld` describe source quality, independently
of pagination. Withheld responses contain no financial rows or continuation.
Partial/stale results cannot be displayed as certified totals.

Statements discriminate trial-balance account/debit/credit lines from other
policy-defined signed Money lines. A `complete` statement structurally requires
RECONCILED status, trial-balance version and approved reporting-policy reference.
ERP/Finance must actually demonstrate numerical reconciliation, currency/version
agreement and policy correctness; schema validation cannot prove that claim.

## Journal commands

| Operation | Mandatory input beyond operation/idempotency key | Result status |
|---|---|---|
| CREATE_DRAFT | `draft`: book, period bounds, accounting date, currency and at least two lines | DRAFT |
| SUBMIT | `journal_ref`, `expected_version` | SUBMITTED |
| APPROVE | `journal_ref`, `expected_version` | APPROVED |
| POST | `journal_ref`, `expected_version` | POSTED |
| REVERSE | `journal_ref`, `expected_version`, nonblank reason and explicit reversal date | REVERSED, with distinct correcting-journal reference |

Draft instructions cannot be mixed into a transition, or a journal target into
a create. Each draft line explicitly supplies both decimal strings: one strictly
positive debit or credit, with zero on the opposite side. Both-positive,
zero-only, negative, numeric JSON, exponent and whitespace amounts are refused.
Precision is not fixed at two/eight decimal places; ERP's approved baseline and
currency policy determine permissible precision and rounding.

The provider must enforce account ownership, exactly balanced totals, valid/open
accounting dates/periods, optimistic concurrency, current independent approval
and the accepted CP/native COMMIT veto. Maker/checker uses distinct canonical
Principals, never role names or caller-supplied identifiers. CREATE_DRAFT never
posts; a payload's `operation: POST` is not a permit. Posted entries are immutable:
a reversal creates a separate governed correction, preserving original lineage.

The body key and HTTP `Idempotency-Key` must agree. Apply the canonical
`contracts/idempotency/v1/policy.yaml`: scope by service/operation/Tenant, bind
principal and canonical payload digest, arbitrate concurrent attempts atomically,
return the original terminal result for an authorised identical replay, and reject
changed payload with 409 `IDEMPOTENCY_KEY_REUSED`. Do not log keys or payloads.
An authorised replay must never cause another native financial effect.

## Wire proof versus provider acceptance

| Proved here | Still required in ERP/CP/Finance |
|---|---|
| Valid JSON Schema, local references, closed operation/view shapes | Real routes and native book/document placement |
| Exact string amounts, explicit currency/date shape and bounded payloads | Numerical balance, precision/rounding, currency equality and ordered/open periods |
| Required optimistic version/idempotency input | Durable atomic concurrency/replay handling and payload conflict |
| No request-body authority or native IDs | Live scope/current grant/legal actor, independent approval and cross-Tenant denial |
| Required baseline/reconciliation metadata | Trusted historical lineage, source-version equality and numerical trial-balance reconciliation |
| Shared RFC 9457 shape | Safe provider denials with no existence, secret, payroll or financial-record leakage |

[The provider acceptance plan](../../../docs/architecture/finance-f1-provider-acceptance.yaml) lists the remaining owner evidence. No provider
registration, HTTP route, native migration, accounting algorithm, ledger balance
calculation, IAM profile or event producer is implemented by this package.
Journal event envelopes/producer activation remain an explicit follow-up under
ADR-SHARED-008 and the ERP event owner; these schemas must not be published as
business events merely because a JSON shape exists. No payment, settlement,
Trade accounting or intercompany authority is transferred to F1.

## Validation and rollback

```sh
python -m pip install -r .github/foundation-tests/requirements.txt
python scripts/validate-finance-contracts.py
python scripts/tests/test_finance_f1_canonical.py
python scripts/tests/test_finance_f1_candidate.py
python scripts/capability_catalogue.py validate-catalogue
```

The mandatory CI job runs these plus the existing cross-package gates. The
validator refuses unknown schema URLs offline and fails if required format
validators are missing. Examples and negative mutations are structural evidence,
not live iDempiere or statutory signoff. Source work is independent of
Infrastructure #35; cross-engine qualification and activation remain later gates.

There are no conforming provider consumers to migrate in this draft increment.
Rollback is to revert the Shared source commit and keep providers unregistered.
A future consumer must pin an exact reviewed Shared revision before adoption;
DRAFT does not silently become STABLE or production-permitted.
