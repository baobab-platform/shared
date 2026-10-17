# BXS-05 — Registry acceptance and consumer release gate

Accepted ADR-SHARED-040 requires evidence of real, version-pinned publication.

Source-versioned 0.2.0 packages do NOT imply that GitHub Packages contains
installable artifacts. An authorised maintainer runs the existing
Publish Shared Packages workflow on main after protected gates pass. Do not
use a release tag outside the approved source/release process.

Then run the new, read-only Verify Experience Registry Releases workflow on
main. It obtains all three package names and exact versions from main,
downloads metadata and actual tarballs with GitHub Packages read access,
checks SHA512 archive bytes, published name, source version, registry scope
and the required compiled JavaScript, CSS and TypeScript outputs. It has no
packages-write permission and no release trigger. Negative unit tests
exercise forged names, digests, versions and missing exports.

When both runs are green, record artifact integrity and approve separate,
exact-version Nabhold and ZuriBeans installation PRs, which themselves
need browser keyboard, WCAG/axe, visual, performance and authorised-view-model
acceptance. A package version or registry success never confers tenant
identity, fleet tracking, price authority, or a new corporate brand identity.

The future Thamani logistics theme remains separately subject to approval.
