# DEV-06 — external API-only qualification

The Accepted EA-DEV plan and ADR-SHARED-043 authorise disposable synthetic
engineering, with the original INT-07 meaning unchanged. Shared #389 registers
a development-only external caller and independent Pulse validator. CP #437 adds
an explicit leased API-only Principal and read-only actual zero-estate checks.
Pulse #56 fixes explicit CP audience selection and OAuth Bearer case handling;
it also updates vulnerable locked dependencies without scan suppression.
Infrastructure #58 composes native Hydra/Kratos/CP/Pulse/PG17/Qdrant with no CMS
or frontend prerequisite. Its `development/INT07.md` is the operating runbook.

The external workload is not an estate service or a workforce membership. It
has a separate CP-generated Principal and tenant-local development lease, no
Nabhold group inheritance and no invented DigitalEstate. The independent Pulse
validator is not assigned to any tenant. Protected runtime and production
credentials cannot be admitted by selecting this profile.

The initial component increment reported real operations separately from the
then-missing canonical subscription/grant/binding prerequisite.
A direct authenticated Pulse read does not prove an entitled bound invocation
or its audited effect. Controlled absent-subscription, unentitled-resource and
retired-binding differentials require that valid positive first. Those cells
were BLOCKED, never fabricated PASS. All eighteen engineering observations
remain visible; they do not replace the one canonical INT-07 scenario.

The implementation register owns current source/CI and runtime status. A source
or component merge alone cannot accept DEV-06. The 26 October qualification below
adds owner-governed entitlement provenance, normal provider eligibility/binding
and current native execution checks, then reruns the same eighteen obligations.
No independent human ceremony is imposed on ordinary development.

## Evidence custody and DEV-05 reconciliation

Infrastructure run 40115479241, artifact 12568218233, retains the original
sanitized DEV-05 suite and completed receipt/hash pairs. Its archive SHA-256 is
`8820bc972722d72a88657e3f158aa59bb3162e3815e2a874c7695ec2d1f8afa5`.
The archive digest and every available receipt/suite hash pair were independently
checked after download. The observed result is 12 PASS, 2 canonical-provider
BLOCKED; native image identity, client deletion, issuer inactivity, private-state
and owned-resource absence and final teardown are recorded. Full NAB-03/provider,
protected and production qualification remain false.

Original bytes stay in the CI artifact; this read model links the run and records
the archive digest rather than republishing nested credential-file fingerprints.
The register validator now permits explicit mixed real-component/BLOCKED reports
only with linked real passes, declared blockers, completed cleanup and no package
completion date. A package PASS still requires every original case to pass.

## Historical DEV-06 component observation — 24 October

[Infrastructure run 40119777295](https://github.com/baobab-platform/infrastructure/actions/runs/40119777295)
retains artifact `12570975667` (`dev06-external-api-evidence`). Its archive SHA-256 is
`22069c7b8fcf460162b5cdc2005c42039f27d6db2752def36b5930a2b03c9e0a`.
The downloaded archive digest and every available receipt/suite hash pair were
independently verified. The tested harness merge SHA is
`9fb719570b0f884da75f28cabe8b3b6037afbe6d`, from reviewed Infrastructure head
`a45e4792614407eb0fc1ef55b1dc9482f7a993e0`.

Actual source pins are Shared `19769790d0bac4a625f1416ffbf6849e8219124d`,
CP `c0f9d7d684d4b57218d30efb918b4aae907aa42a`,
IAM `0ad103606b9705fcb33c468ea01b54d8ce76f9ae` and
Pulse `e8b41d4f5762bec8a19a40e3b1da4d6db2105208`.
The first two are ancestors of the corresponding final merged source heads;
the registry content and runtime implementation are retained unchanged.

The result is **14 PASS, 4 BLOCKED, no failures**. Actual checks cover own
context/resource reads, zero estates before and after, three unrelated tenant
denials, forged tenant/fake estate rejection, wrong owner/audience, actual token
expiry and revocation/replay, CP outage/recovery, native client deletion and
issuer inactivity, private-state/resource absence and completed teardown.
All thirteen component-check flags are true. Bound resource/audited effect,
controlled absent-subscription, unentitled-resource and retired-binding cases
remain blocked on canonical entitlement or binding prerequisites. INT-07,
canonical-provider, protected and production qualification remain false.

The native run also exposed strict Python 3.14 TLS verification rejecting the
old development root's missing key usage. Infrastructure now issues explicit
critical CA key usage and leaf key usage, subject/authority key identifiers;
a real strict TLS handshake regression verifies the correction. Verification
is never disabled. The source/failure/custody suite passes 49 tests.

## Bound-resource qualification — 26 October

[Infrastructure run 40280112921](https://github.com/baobab-platform/infrastructure/actions/runs/40280112921)
executed all **18 unchanged cases PASS**, with all **21 component observations
true**, using native IAM, CP, Pulse, PostgreSQL 17 and Qdrant. The actual Pulse
read resolves current CP authority first and persists its read audit. An
independent CP-store read joins that audit to the recorded resolution, grant,
binding and engine instance. The controlled missing subscription, revoked grant
and retired binding each deny actual resource access without an added read
effect; restored authority succeeds. Zero-estate, isolation, audience, expiry,
revocation and outage/recovery obligations remain in the same inventory.

CP #441/#442 supply current subscription provenance, provider eligibility and
guarded normal maker/checker activation. Pulse #58 supplies per-resource canonical
resolution and persisted read effects. The fixture uses an expiring nonmonetary
TRIAL source and normal composition expansion; no certification or commercial
permission is invented. Independent issuer client deletion/inactivity, owned
resource absence, private-state absence and host recovery passed.

Reviewed Infrastructure head: `5bac4b15b9873ea483d23083075e9f6df8854ed7`.
Executed PR merge: `cf8bd857e67392be88eae016a40490a9d8f61f8b`, whose parents are
the reviewed head and main `00e6cd37515d1be731fa9b1f8da03d43ad11f4bc`. The executed
tree `753355a5a965e6616059b8d1ceb01d6a1fc121f0` equals the reviewed head's tree.

Artifact `12631547492` archive SHA-256:
`87be57733b7ef87cfe4732010af914f9153054ca1795822ee70e088646757a93`.
Both original suite and completed receipt SHA-256:
`f74a8d5cab013000c4df6eac81fd4716bc49d25258bb75e690ddc19690cf4aca`.
The downloaded archive and both original-byte hash pairs were independently
verified. The [derived observation](evidence/dev06-2026-10-26/observation.json)
preserves source pins, case results, component checks and custody identifiers;
it is explicitly a read model, not an original receipt or an authority. It omits
nested credential-file fingerprints. Original bytes remain in the linked CI
artifact, whose published retention expires 9 November 2026; the summary remains
in this repository. Historical receipts and the failed run remain unchanged.

The earlier run 40256362565 built Pulse and published OCI successfully before
failure at the private proof handoff. The proof's 0600 file owner differed from
CP's default nonroot UID. Infrastructure #60 runs only that one-shot fixture as
the development operator UID/GID with the same read-only mount. It also retains
hashed failed-run evidence after verified cleanup and reports execution failure
separately from runtime readiness and teardown. The 61 source/custody tests pass.

Infrastructure #60 merged as `0d1ff64a537c0e287aa4a435e53f02e34c30f66a` after
32 applicable checks passed and six existing applicability skips. Its tree
matches the reviewed/tested tree. This closes the eighteen-case **development
engineering** prerequisite. Canonical INT-07's separate certified-provider
requirement, EA-09, protected staging and production remain unqualified; all
corresponding receipt flags remain false. No package here changes their meaning.
DEV-05 CMS normal provider/native enforcement is next; DEV-10 stays held.

