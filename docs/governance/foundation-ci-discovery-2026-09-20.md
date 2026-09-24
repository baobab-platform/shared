# Foundation CI discovery — 2026-09-20

The authoritative GitHub App installation exposed 16 active repositories in `baobab-platform`: seven public and nine private. The estate includes Go, Node with pnpm, Node with npm, Python with uv, Java with Maven, container-only components, infrastructure, digital estates, shared contracts, and early metadata-only engines.

## Material findings

- `shared` is private and organisation Actions access is enabled for Baobab repositories.
- The organisation and reusable workflow references use `baobab-platform`; historical `nabhold/shared` references are obsolete.
- `shared`, `baobab-dev`, and `zuribeans` use `.baobab/environment.yaml`; most existing consumers still carry `.nabhold/environment.yaml` and require cohort migration.
- The old workflow treats every repository as a Baobab development-environment consumer and embeds profile rules in the orchestrator.
- Reproducibility checks cover Node and Go only, despite live Python/uv and Java/Maven repositories.
- Filesystem security, container build/scan, environment validation, and dependency review are combined in one workflow, obscuring applicability and failure ownership.
- Repository visibility is mixed. GitHub Advanced Security-dependent behaviour cannot be assumed across private repositories.
- Consumers already use immutable `shared` SHAs. The migration must publish a new shared commit before consumer pins can move.

## Representative rollout set

| Class | Repository |
|---|---|
| Shared contracts and Actions | `shared` |
| Go engine | `baobab-cp` |
| Node engine | `baobab-trade` |
| Python service | `baobab-pulse` |
| Java/container engine | `baobab-erp` |
| Private digital estate | `zuribeans` |
| Infrastructure | `infrastructure` |

The remaining repositories should migrate only after these pilots establish that failures are correctly classified as repository defects, Foundation defects, or compatibility defects.
