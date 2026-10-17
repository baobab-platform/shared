# Experience 0.3.0 release candidate

Changesets prepares experience-tokens, experience-geo-core and experience-ui 0.3.0 from merged implementation #332. This review commit requests ordinary PR CI on the versioned source; the bot-created branch alone is not a substitute for package/browser/security receipts.

Acceptance must include the exact versioned build, 18 package regression tests, Chromium Dialog/Tabs keyboard and accessibility tests, and committed desktop/mobile pixel comparisons. Inspect all generated exports, including strict timestamp code and client-only interaction entry points. Existing consumers stay on immutable 0.2.0 until this candidate is merged, deliberately published through the repository release process, and verified by the registry SHA512/export workflow.

This candidate grants no brand, provider, staging or production authorisation. Human visual and assistive-technology review remain separate acceptance records.
