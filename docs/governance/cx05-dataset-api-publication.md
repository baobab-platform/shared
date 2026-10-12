# CX-05 — dataset API publication and contract/consumer convergence

The dataset API is published in `contracts/control-plane/v1/openapi.yaml`
with strict schemas in `console-dataset.schema.json`. It is a
**versioned contract**, not a deployed authenticated service or a grant.

The API covers redacted preview, independently approved immutable plans,
durable execution receipts, reviewer-visible change details, and governed
CSV retrieval. Independent `organisation.export`,
`organisation.bulk.propose` and `organisation.bulk.approve` privileges
remain separate from `organisation.view`.

## Source of truth and consumers

| Concern | Authority | Consumer responsibility |
| --- | --- | --- |
| API / JSON Schema | Shared `control-plane/v1` | Pin exact Shared commit and regenerate types |
| Permission registry | Shared `administration/v1` | CP exact-grant and risk/assurance evaluation |
| Authentication/step-up | Baobab IAM | CP validates issuer, token and current assurance |
| Proposal, approval, audit, CSV | Control Plane | Durable transactional and encrypted enforcement |
| Browser | Next.js CP Console | Server-held session, CSRF, fixed BFF paths |
| Infrastructure | Infrastructure repo | Real protected staging, key management, retention proof |

## Compatibility and change discipline

The `ReviewReceipt` response is **distinct** from the compact `Receipt`
returned by propose, approve and execute. Reviewers must see purpose,
recipient, targets, expiry, hashes and versioned changes *before*
authorising; never collapse it to an opaque digest.

When changing a field, risk condition or path, audit all consuming
repositories and pin the accepted Shared revision before updating the
embedded contract. Version breaking changes rather than silently narrowing
existing consumers; preserve the negative security tests.

## Evidence that remains external

Contract publication does not establish that an IAM-issued CRITICAL assurance
is deployable, that independently admitted workloads exist, that real
PostgreSQL/Postgres encryption/backup retention is compliant, or that the
protected CX-05 staging flow has met its operational latency and revocation
criteria. A deployment can only be approved against recorded live evidence.

See [Control Plane v1 contract README](../../contracts/control-plane/v1/README.md).
