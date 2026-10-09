# Baobab content contracts v1

Contract for the canonical capability `content.entry.resolve`, implemented by `baobab-platform/baobab-cms`.

- `capabilities.yaml` defines the capability.
- `content-resolve-request.schema.json` and `content-resolve-response.schema.json` define the payloads.
- `openapi.yaml` defines the HTTP surface: `POST /v1/content/resolve`, the `content:entry:resolve` and `content:entry:preview` scopes, and the error codes.
- `examples/` holds a request and two responses (FALLBACK and NONE), validated against the schemas.

Tenant authority is a trusted Control Plane context (`context_id`, a query parameter), never the request body. The body's `tenant_id` is a claim that must equal the validated context's tenant. The Control Plane resolves which provider serves the capability; it never carries the content request or response (ADR-BCP-007).
