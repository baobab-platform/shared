---
"@baobab-platform/supplier-domain": minor
---

Add the initial `@baobab-platform/supplier-domain` package: a generic lifecycle
state-machine mechanism plus Zod shapes for a supplier organisation, its
contacts, capabilities, certifications, and status-change audit trail.
Generalized from baobab-platform/zuribeans' proven supplier-registration vertical
slice (ADR-0006) so other digital estates (starting with baobab-platform/thamani)
can adopt the same mechanism instead of duplicating it from scratch.
