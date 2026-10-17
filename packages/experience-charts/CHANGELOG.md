# @baobab-platform/experience-charts

## 0.1.0

### Minor Changes

- 5a08ce1: Introduce a bounded, source-labelled chart display model with defensive
  runtime validation and accessible table fallback rows. Reject forbidden data
  in restricted/unavailable views, malformed source timestamps, duplicate IDs and
  non-finite numbers; keep missing values distinct from zero. This does not
  calculate domain KPIs, grant access or certify a provider or release.
