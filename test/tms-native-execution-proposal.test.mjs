import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import Ajv2020 from "./tms-native-authority/node_modules/ajv/dist/2020.js";
import addFormats from "./tms-native-authority/node_modules/ajv-formats/dist/index.js";
import { decisionSemanticErrors } from "../proposals/tms-native-execution/v1/decision-semantics.mjs";

const schema = JSON.parse(
  readFileSync(
    "proposals/tms-native-execution/v1/decision.schema.json",
    "utf8",
  ),
);
const domain = JSON.parse(
  readFileSync("contracts/control-plane/v1/domain.schema.json", "utf8"),
);
// Required fields live at the root; conditional/not branches refer to those
// declarations. strictRequired is a lint rule, not the required validator.
const ajv = new Ajv2020({
  strict: true,
  strictRequired: false,
  allErrors: true,
});
addFormats(ajv);
ajv.addSchema(domain);
const validate = ajv.compile(schema);
const now = Date.parse("2026-10-29T12:00:00Z");
const uuid = (n) => `019a0000-0000-7000-8000-${String(n).padStart(12, "0")}`;
const hash = `sha256:${"a".repeat(64)}`;
const base = {
  decision_id: uuid(1),
  decision: "ALLOW",
  operation: "tms.booking.submit",
  authority_plane: "DATA",
  resource_type: "TransportBooking",
  resource_id: "booking_opaque123",
  resource_revision: 2,
  intent_digest: hash,
  subject_issuer: "https://issuer.example",
  subject_id: "subject-opaque",
  subject_audience: "baobab-tms",
  subject_client_id: "registered-caller",
  subject_actor_type: "WORKLOAD",
  validator_client_id: "baobab-dev-tms-validator",
  correlation_id: uuid(2),
  issued_at: new Date(now).toISOString(),
  expires_at: new Date(now + 5000).toISOString(),
  environment: "development",
  context_id: uuid(3),
  principal_id: uuid(4),
  validator_principal_id: uuid(5),
  tenant_id: "tn_opaque123",
  primary_organisation_id: uuid(6),
  operating_organisation_id: uuid(7),
  legal_entity_id: "LEGAL-ACTOR-ONE",
  market_id: "market_opaque",
  market_participation_reference: "participation:opaque",
  isolation_profile_id: "dedicated_native_database",
  cp_provider_id: "provider:baobab-tms",
  cp_engine_instance_id: "ei_opaque123",
  capability_binding_id: "binding:opaque",
  capability_binding_revision: 3,
  native_binding_id: uuid(8),
  native_binding_revision: 2,
  native_provider_kind: "OPEN_TMS",
  provider_release_digest: hash,
  native_deployment_id: "deployment:opaque",
  policy_digest: hash,
  claim_id: uuid(9),
  fencing_generation: 8,
  execution_attempt_id: uuid(10),
  transport_plan_id: "transportplan_opaque123",
  transport_plan_revision: 4,
  transport_plan_digest: hash,
  transport_plan_approval_reference: "approval:transportplan",
  carrier_purchase_approval_reference: "approval:carrier-purchase",
};
const options = { now, expected: base, evidenceExpiresAt: now + 5000 };
const valid = (value, opts = options) =>
  validate(value) && decisionSemanticErrors(value, opts).length === 0;
const remove = (keys, value = base) =>
  Object.fromEntries(
    Object.entries(value).filter(([key]) => !keys.includes(key)),
  );
const transport = [
  "transport_plan_id",
  "transport_plan_revision",
  "transport_plan_digest",
  "transport_plan_approval_reference",
  "carrier_purchase_approval_reference",
];

test("actual Draft 2020-12 validation accepts the exact development decision", () => {
  assert.equal(validate(base), true, JSON.stringify(validate.errors));
  assert.deepEqual(decisionSemanticErrors(base, options), []);
  assert(schema.$id.includes("/proposals/"));
  assert.equal(schema.additionalProperties, false);
});

test("every required ALLOW binding is mandatory", () => {
  const keys = [
    ...schema.required,
    ...schema.allOf[0].then.required,
    ...transport,
  ];
  for (const key of keys) assert.equal(valid(remove([key])), false, key);
});

test("all operation/resource and control/data combinations are closed", () => {
  const pairs = {
    "tms.plan.revise": "TransportPlan",
    "tms.booking.intent.create": "TransportBooking",
    "tms.booking.submit": "TransportBooking",
    "tms.booking.reconcile": "TransportBooking",
    "tms.capacity.hold": "CapacityReservation",
    "tms.capacity.release": "CapacityReservation",
    "tms.movement.dispatch": "TransportMovement",
    "tms.native.provision": "NativeProviderInstance",
    "tms.native.suspend": "NativeProviderInstance",
    "tms.native.deprovision": "NativeProviderInstance",
  };
  for (const [operation, resource_type] of Object.entries(pairs)) {
    const control = operation.startsWith("tms.native.");
    let value = {
      ...base,
      operation,
      resource_type,
      authority_plane: control ? "CONTROL" : "DATA",
    };
    if (control)
      value = {
        ...remove(transport, value),
        operation_id: "op_opaque123",
        execution_attempt: 3,
        plan_id: "plan_opaque123",
        plan_digest: hash,
        desired_state_digest: hash,
        approval_reference: "apd_opaque123",
      };
    assert.equal(
      valid(value, { ...options, expected: value }),
      true,
      operation,
    );
    for (const type of Object.values(pairs))
      if (type !== resource_type)
        assert.equal(
          validate({ ...value, resource_type: type }),
          false,
          operation + ":" + type,
        );
    assert.equal(
      validate({ ...value, authority_plane: control ? "DATA" : "CONTROL" }),
      false,
    );
    if (control) {
      for (const key of [
        "operation_id",
        "execution_attempt",
        "plan_id",
        "plan_digest",
        "desired_state_digest",
        "approval_reference",
      ])
        assert.equal(validate(remove([key], value)), false, key);
      assert.equal(validate({ ...value, subject_actor_type: "HUMAN" }), false);
    }
  }
  assert.equal(validate({ ...base, operation_id: "op_opaque123" }), false);
  assert.equal(
    validate({ ...base, operation: "tms.arbitrary.execute" }),
    false,
  );
});

test("identity and canonical grammar cannot be replaced by vendor/native fields", () => {
  for (const change of [
    { principal_id: "native-user-1" },
    { operating_organisation_id: "fleetbase-company" },
    { legal_entity_id: "zuribeans_ug" },
    { market_id: "ZA" },
    { tenant_id: "ZURIBEANS" },
    { cp_engine_instance_id: "open-tms" },
    { provider_release_digest: "latest" },
    { native_provider_kind: "DEFAULT" },
    { subject_issuer: "http://issuer.example" },
    { subject_issuer: "https://user:secret@issuer.example" },
    { subject_issuer: "https://issuer.example?token=secret" },
    { subject_audience: "baobab-control-plane" },
    { capability_binding_revision: "3" },
    { native_binding_revision: 0 },
    { fencing_generation: 0 },
    { fencing_generation: 9007199254740992 },
    { resource_revision: true },
    { native_admin_token: "forbidden" },
    { subject_client_id: "x".repeat(257) },
    { environment: "production" },
    { environment: "staging" },
  ])
    assert.equal(valid({ ...base, ...change }), false, JSON.stringify(change));
});

test("DENY is a minimal refusal with no reusable positive scope or lease", () => {
  const denial = Object.fromEntries(
    schema.required.map((key) => [key, base[key]]),
  );
  Object.assign(denial, {
    decision: "DENY",
    denial_reason: "PRINCIPAL_NOT_RESOLVED",
  });
  assert.equal(valid(denial, { now, expected: denial }), true);
  assert.equal(validate(remove(["denial_reason"], denial)), false);
  assert.equal(
    validate({ ...denial, denial_reason: "arbitrary provider error" }),
    false,
  );
  for (const key of Object.keys(base).filter(
    (key) => !schema.required.includes(key),
  ))
    assert.equal(validate({ ...denial, [key]: base[key] }), false, key);
  assert.equal(
    validate({ ...base, denial_reason: "AUTHORITY_UNAVAILABLE" }),
    false,
  );
});

test("time, lease and evidence comparisons are explicit beyond schema validation", () => {
  for (const change of [
    { expires_at: new Date(now).toISOString() },
    { issued_at: new Date(now + 1).toISOString() },
    { expires_at: new Date(now + 5001).toISOString() },
    { expires_at: new Date(now - 1).toISOString() },
    { issued_at: "invalid" },
  ])
    assert.equal(valid({ ...base, ...change }), false);
  for (const opts of [
    { ...options, now: NaN },
    { ...options, expected: undefined },
    { ...options, evidenceExpiresAt: undefined },
    { ...options, evidenceExpiresAt: now + 4999 },
    { ...options, now: now + 5000 },
  ])
    assert.equal(valid(base, opts), false);
});

test("each independently current identity, scope, resource, binding, plan and generation must match", () => {
  for (const key of Object.keys(base).filter(
    (key) =>
      !["decision_id", "decision", "issued_at", "expires_at"].includes(key),
  )) {
    const expected = {
      ...base,
      [key]:
        typeof base[key] === "number"
          ? base[key] + 1
          : "different-authoritative-state",
    };
    assert.equal(valid(base, { ...options, expected }), false, key);
  }
  assert.equal(
    valid({ ...base, subject_issuer: base.subject_issuer + "/" }),
    false,
  );
  assert.equal(
    valid(
      { ...base, principal_id: base.validator_principal_id },
      {
        ...options,
        expected: { ...base, principal_id: base.validator_principal_id },
      },
    ),
    false,
  );
  assert.equal(
    valid(
      { ...base, subject_client_id: base.validator_client_id },
      {
        ...options,
        expected: { ...base, subject_client_id: base.validator_client_id },
      },
    ),
    false,
  );
});

test("acceptance remains architecture-only with no active issuer or operation registration", () => {
  const doc = readFileSync(
    "docs/architecture/proposals/tms-native-execution-authority-v1.md",
    "utf8",
  );
  assert(
    doc.includes(
      "ACCEPTED — architecture and development contract design only",
    ),
  );
  assert(doc.includes("remain HELD"));
  assert(doc.includes("not an authority SDK"));
  const operation = JSON.parse(
    readFileSync(
      "contracts/control-plane/v1/execution-operation.schema.json",
      "utf8",
    ),
  );
  assert.equal(
    operation.$defs.operationType.enum.some((x) => x.startsWith("TMS_")),
    false,
  );
});
