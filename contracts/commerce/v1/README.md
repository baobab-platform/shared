# Native Trade seller binding command admission

P0-04B-02 registers `trade-binding:propose/approve/activate/revoke` at the CP
resource-server audience and exact `organisation.trade-binding.*` administrative
permissions. All are human only; no client, profile or workload is assigned them.
The CP authorization route is `/internal/trade-binding/v1/{operation}/authorize`.
The scope tuple and SHA-256 of the deterministic Trade command are echoed; the
human identity, grants and five-second maximum validity are CP-owned.

This response must be read directly by Trade using the actual human token. Never
accept a caller-supplied response or use it as a portable grant. It verifies current
command admission, not documentary evidence. Trade retains each CP decision in its
append-only local command receipt. CP rechecks identity, grant and assurance on
all calls; Trade rechecks after context/legal/native I/O and bounds DB COMMIT.

Maker, checker and activation operator are separate canonical principals. The
original native cart/seller tuple cannot be replaced. Only the Trade workload
resolves its own bounded RUNTIME context and obtains a fresh SELLER_OF_RECORD
assessment. This does not admit a workload, activate a mandate, certify a merchant,
publish a canonical event, or open production checkout.
