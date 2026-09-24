# Contract versioning and compatibility policy

## Versioning

Published contract packages use Semantic Versioning. Contract identifiers also
include a major version, such as `baobab-platform.control-plane.tenant.v1`.

- **Patch:** clarification or fixture correction that changes no valid payload.
- **Minor:** backward-compatible optional fields, event types, or enum values
  whose consumers are required to handle an unknown value safely.
- **Major:** removal, rename, changed meaning, newly required field, or narrowed
  validation.

Schemas under an existing `v1` directory are never changed incompatibly. A
breaking revision is introduced under `v2` and supported in parallel during a
documented migration window.

For events, the final `vN` segment of `type` is the major semantic version and
`dataschema` identifies the exact payload schema. A breaking payload change must
change both. Reformatting a payload while retaining the old event type is not a
compatible change.

The cross-engine envelope is versioned independently from each domain payload.
Version 1 is a closed profile (`additionalProperties: false`) so strict
validators can reject ungoverned metadata. Adding or renaming a top-level
attribute, narrowing its grammar, or making it required therefore needs a new
envelope major version and a migration fixture. A domain payload may add an
optional field under its existing major version only when its own schema and
registered consumers explicitly permit unknown optional fields.

## Consumer rules

- Pin released package versions; never consume another repository's default
  branch as a production dependency.
- Validate at trust boundaries, not between every internal function.
- Preserve correlation, causation, subject, tenant, and idempotency metadata.
- Preserve the original `(source, id)` pair across delivery retries and replay.
- Validate `dataschema` before applying a business consequence.
- Do not branch business logic on fields a consumer does not own.
- Treat unknown event types as non-processable and route them to quarantine,
  not an infinite retry loop.

## Change workflow

1. Change schemas, examples, and compatibility fixtures in one pull request.
2. Run schema linting and backward-compatibility checks in `shared`.
3. Dispatch read-only compatibility tests in registered consumers.
4. Review and publish a versioned package.
5. Let automation open explicit dependency-update pull requests downstream.

A `shared` pull request must not deploy an environment or push directly to a
consumer branch.
