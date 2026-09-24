# ADR-0005: ERP System of Record and Boundary Contracts

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-01 |
| **Owner** | Chief Software Engineer, Baobab-Platform Group Africa |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-0002; ADR-0003; ADR-0004 |
| **Applies to** | `baobab-erp`, `baobab-cp`, `trade`, authorised digital estates and ERP infrastructure adapters |

## 1. Context

ERPNext-specific names, Frappe Site tenancy, local event envelopes and direct
commerce-to-ERP assumptions had escaped the intended ERP boundary. Replacing
the product without first fixing ownership and contracts would preserve that
coupling under iDempiere terminology.

Baobab tenancy is a platform concept. iDempiere Client, Organisation, Business
Partner, Warehouse and database identifiers are ERP implementation concepts.
Trade remains authoritative for commerce while the ERP Engine owns enterprise
financial, procurement, physical-stock and warehouse consequences.

## 2. Decision

### 2.1 Contract ownership

`contracts/erp/v1` is the canonical cross-engine ERP package. `baobab-erp`
implements it and may maintain private ERP models, vendor bindings and adapter
state. No consuming repository may copy these schemas or call iDempiere
internals directly.

### 2.2 Identity mapping

Mappings are explicit, tenant-scoped, legal-entity-aware, temporal, revisable
and many-capable. Their public side joins a canonical owner/reference to a
Baobab ERP-minted resource ID. Vendor bindings are private to the adapter.

The following equalities are forbidden:

- tenant = iDempiere Client;
- legal entity = iDempiere Organisation;
- business code or document number = canonical identity;
- digital estate = tenant.

The Shared contract does not mint `organisation_id`. Its canonical owner is
still unassigned, and ambiguity must be quarantined until a separate decision
assigns that ownership.

### 2.3 System-of-record boundaries

The complete approved matrix is machine-readable in
`contracts/erp/v1/system-of-record.yaml`. Its governing rule is that no record
is implicitly bidirectional. For split processes, ownership is fixed before
exchange:

| Concept | Authoritative boundary |
|---|---|
| Tenant lifecycle and entitlement | Control Plane |
| Legal-entity identity | Shared registry |
| Commerce customer/order/catalogue/price/reservation | Trade for commerce-origin records |
| GL, AP/AR, procurement, statutory posting, physical/financial stock, warehouse | ERP |
| Commerce payment capture | Payment provider/Trade |
| Payment accounting and allocation | ERP |
| User identity | External identity provider; engine permissions may deny |

### 2.4 Communication

Provisioning commands and queries use OpenAPI when an immediate acceptance or
observation is required. State propagation and business consequences use the
AsyncAPI messages and ADR-0004 envelope. Idempotency, retries, duplicate
delivery, reconciliation and explicit exception states replace distributed
transactions and exactly-once assumptions.

### 2.5 International operation

Core contracts use ISO country/currency codes, IANA timezones and decimal
strings. They define no default country, currency, language, market, tax rate,
warehouse or deployment topology. Country localisation and deployment policy
remain governed configuration referenced by opaque IDs.

## 3. Consequences

### Positive

- iDempiere can be replaced or upgraded without changing canonical identities.
- Baobab-Platform, ZuriBeans, Thamani and future organisations use the same
  configuration-driven onboarding contract.
- Trade can accept work while ERP is unavailable and recover without duplicate
  financial effects.
- Ownership conflicts become observable exceptions rather than silent reverse
  synchronisation.

### Costs

- The ERP gateway needs durable inbox/outbox and mapping stores.
- Adapters must translate canonical IDs and states instead of leaking vendor
  records.
- Consumers need event-version and reconciliation logic.
- Organisation ownership still requires a separate approval before a portable
  `organisation_id` can appear in contracts.

## 4. Rejected alternatives

- **Expose iDempiere REST models as the Baobab API.** This leaks vendor identity
  and prevents independent evolution.
- **Map each tenant one-to-one to a Client and each legal entity one-to-one to
  an Organisation.** This blocks reorganisation, multinational operation and
  varied isolation topologies.
- **Use synchronous REST for order propagation.** This couples commerce
  acceptance to ERP availability.
- **Synchronise shared records bidirectionally.** This creates unresolved dual
  authority for tax, payments, inventory and customer data.
- **Choose a shared iDempiere topology in this ADR.** Deployment isolation is an
  infrastructure policy and remains a separately approved decision.

## 5. Follow-up

1. Implement Control Plane context resolution in PR A4.
2. Migrate Trade producers/consumers to these contracts in PR A5.
3. Select the iDempiere/JDK/PostgreSQL baseline and isolation profile in a
   separately reviewed Phase 1 decision.
4. Implement adapter-private vendor mappings only after the public boundary has
   compatibility tests in consuming repositories.

