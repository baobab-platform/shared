# DEV-01 — verified Actions lifecycle evidence

Observed 24 October 2026. Scope: native Keycloak setup plus CP-owned guarded
bootstrap, lifecycle and recovery only; no full authorisation, provider,
INT-03C/NAB-03 or protected qualification.

- Engineering PR: https://github.com/baobab-platform/infrastructure/pull/53
- Merged source: `1445195e5304accaf38b29617dc223d12680cd03`
- Reviewed head: `97c6a65cdf0ae191ef9d96c2b9beaa118f2476b4`
- Actual CI harness merge SHA: `7963d837b64b9315334afd7c039ad101f00cb625`
- Run: https://github.com/baobab-platform/infrastructure/actions/runs/40052631759
- Artifact: https://github.com/baobab-platform/infrastructure/actions/runs/40052631759/artifacts/12544247579
- Original archive digest: `sha256:7887679e5a72a81535d328d0e2d3c331ebafc02cf28820910b311f349155065f`

The archive and both receipt hashes were checked after download. JSON bytes are
retained unchanged here so expiry of the CI artifact does not erase the scoped
observations. The interrupted run remains `lifecycle_passed=false`; both runs
show verified teardown. The successful suite records all six observed drills.
The simulated interrupted-start checkpoint uses an actual owned Docker volume;
it does not claim a host-SIGKILL or disaster-recovery qualification. The tested
CI merge commit and later squash commit identify different Git objects; source
review and final-head checks establish the engineering merge, while the receipts
retain the exact actually executed harness identity.

The same dedicated integration container/entrypoints are exposed for Codespaces;
an independently observed interactive Codespaces execution is not asserted.
All domain and protected acceptance flags remain false. No private run state,
subjects, passwords, DSNs or bearer material is retained in this directory.
