/** Reference checks for the accepted development design, not an authority SDK.
 * JSON Schema MUST pass first. `expected` is independently verified CP/IAM/TMS
 * state; copying fields from an incoming decision does not establish authority.
 * No result here replaces authenticated online claim validation or native fencing.
 */
export const MAX_DECISION_LIFETIME_MS = 5000;
export function decisionSemanticErrors(
  value,
  { now, expected, evidenceExpiresAt } = {},
) {
  const errors = [];
  if (!value || typeof value !== "object" || !expected || !Number.isFinite(now))
    return ["INDEPENDENT_EXPECTATION_REQUIRED"];
  const issued = Date.parse(value.issued_at),
    expires = Date.parse(value.expires_at);
  if (
    !Number.isFinite(issued) ||
    !Number.isFinite(expires) ||
    issued > now ||
    expires <= now ||
    expires <= issued ||
    expires - issued > MAX_DECISION_LIFETIME_MS
  )
    errors.push("DECISION_NOT_CURRENT");
  for (const key of [
    "decision_id",
    "operation",
    "authority_plane",
    "resource_type",
    "resource_id",
    "resource_revision",
    "intent_digest",
    "subject_issuer",
    "subject_id",
    "subject_audience",
    "subject_client_id",
    "subject_actor_type",
    "validator_client_id",
    "correlation_id",
    "environment",
  ])
    if (!Object.hasOwn(expected, key) || value[key] !== expected[key])
      errors.push("REQUEST_BINDING_MISMATCH");
  if (value.decision === "ALLOW") {
    if (!Number.isFinite(evidenceExpiresAt) || expires > evidenceExpiresAt)
      errors.push("EVIDENCE_EXPIRED_OR_OUTLIVED");
    for (const key of [
      "context_id",
      "principal_id",
      "validator_principal_id",
      "tenant_id",
      "primary_organisation_id",
      "operating_organisation_id",
      "legal_entity_id",
      "market_id",
      "market_participation_reference",
      "isolation_profile_id",
      "cp_provider_id",
      "cp_engine_instance_id",
      "capability_binding_id",
      "capability_binding_revision",
      "native_binding_id",
      "native_binding_revision",
      "native_provider_kind",
      "provider_release_digest",
      "native_deployment_id",
      "policy_digest",
      "claim_id",
      "fencing_generation",
      "execution_attempt_id",
    ])
      if (!Object.hasOwn(expected, key) || value[key] !== expected[key])
        errors.push("CURRENT_AUTHORITY_MISMATCH");
    const bound =
      value.authority_plane === "CONTROL"
        ? [
            "operation_id",
            "execution_attempt",
            "plan_id",
            "plan_digest",
            "desired_state_digest",
            "approval_reference",
          ]
        : [];
    if (
      ["tms.booking.submit", "tms.movement.dispatch"].includes(value.operation)
    )
      bound.push(
        "transport_plan_id",
        "transport_plan_revision",
        "transport_plan_digest",
        "transport_plan_approval_reference",
      );
    if (value.operation === "tms.booking.submit")
      bound.push("carrier_purchase_approval_reference");
    for (const key of bound)
      if (!Object.hasOwn(expected, key) || value[key] !== expected[key])
        errors.push("PLAN_OR_APPROVAL_MISMATCH");
    if (
      value.principal_id === value.validator_principal_id ||
      value.subject_client_id === value.validator_client_id
    )
      errors.push("VALIDATOR_IS_NOT_SUBJECT");
  }
  return [...new Set(errors)];
}
