# Baobab Trade B2B contracts v1

These schemas define the provider-neutral boundary required by the ZuriBeans B2B purchasing, RFQ and quotation journeys. Baobab Trade owns the business state and authorization; Shared owns the wire grammar. IAM authentication, IAM organisation membership, a client-supplied buyer identifier, or a successful Control Plane resolution is never sufficient business authority on its own.

All operations require server-resolved platform context and active Trade buyer membership. Prices and quotations are confidential to the resolved buyer organisation, market, currency and legal seller. They must not enter a public or cross-buyer cache.

Quick-order validation is advisory and expires. Cart mutation and checkout must repeat authoritative availability, eligibility, minimum-order, pricing and approval checks. RFQ and quotation commands require `Idempotency-Key`; lifecycle transitions use optimistic version checks. A quotation can create an order only from an unexpired accepted version, and the resulting order keeps an immutable commercial snapshot.

The browser may request a buyer organisation or market context. It cannot assert one. A Digital Estate or BFF consumes these contracts through the capability resolved by Control Plane and never integrates IAM, Control Plane and Trade directly in browser code.
