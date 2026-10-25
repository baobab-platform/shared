# frozen_string_literal: true

require "json"
require "yaml"
require "pathname"

ROOT = File.expand_path("..", __dir__)
CODE_PATTERN = /\A[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\z/

def fail_contract(message)
  warn "authorization contract validation failed: #{message}"
  exit 1
end

def load_json(path)
  JSON.parse(File.read(File.join(ROOT, path)))
end

def load_yaml(path)
  YAML.safe_load_file(File.join(ROOT, path), aliases: false)
end

# 1. reason-code-registry.yaml: every entry is well-formed, every code is
#    unique, every category is one this registry documents, and
#    every code matches the same UPPER_SNAKE_CASE convention
#    contracts/errors/v1/problem-details.schema.json already enforces for
#    Baobab machine-readable codes generally.
registry = load_yaml("contracts/authorization/v1/reason-code-registry.yaml")
entries = registry.fetch("reason_codes")
fail_contract("reason-code-registry.yaml declares no codes") if entries.empty?

known_categories = %w[authorization_denial lifecycle_revocation capability_resolution_denial provisioning_blocker health_observation administrative_denial provider_migration_blocker provider_migration_task_failure changeset_blocker market_validation engine_release release_drift]
seen_codes = {}
entries.each do |entry|
  code = entry["code"]
  category = entry["category"]
  description = entry["description"]

  fail_contract("a reason-code entry is missing code, category, or description: #{entry.inspect}") if code.nil? || category.nil? || description.nil?
  fail_contract("reason code #{code.inspect} does not match the Baobab machine-readable code convention") unless CODE_PATTERN.match?(code)
  fail_contract("reason code #{code.inspect} has unknown category #{category.inspect} (expected one of #{known_categories.join(', ')})") unless known_categories.include?(category)
  fail_contract("reason code #{code.inspect} has an empty description") if description.strip.empty?

  if seen_codes.key?(code)
    fail_contract("reason code #{code.inspect} is duplicated (categories: #{seen_codes[code]}, #{category})")
  end
  seen_codes[code] = category
end

# 2. AuthorizationContext's optional `delegation` field resolves to the new
#    Delegation schema, and Delegation's own self-reference (chaining) is a
#    same-document fragment, not a dangling path.
context_schema = load_json("contracts/authorization/v1/context.schema.json")
delegation_ref = context_schema.dig("properties", "delegation", "$ref")
fail_contract("context.schema.json's delegation property must $ref delegation.schema.json") unless delegation_ref == "delegation.schema.json"

delegation_schema = load_json("contracts/authorization/v1/delegation.schema.json")
chain_ref = delegation_schema.dig("properties", "delegation", "$ref")
fail_contract("delegation.schema.json's own delegation property must self-reference via $ref \"#\" for chaining") unless chain_ref == "#"
%w[subject_id subject_actor_type actor_id audience].each do |field|
  fail_contract("delegation.schema.json is missing required field #{field.inspect}") unless delegation_schema.fetch("required", []).include?(field)
end

# 3. AuthenticationAssurance / AssuranceRequirement carry the fields
#    ADR-0015 §180-181 specifies, not a differently-shaped stand-in.
assurance = load_json("contracts/identity/v1/authentication-assurance.schema.json")
%w[actor_type acr authenticated_at issuer client_id].each do |field|
  fail_contract("authentication-assurance.schema.json is missing required field #{field.inspect}") unless assurance.fetch("required", []).include?(field)
end
# amr is optional method evidence: a provider that proves strong authentication
# through its acr alone (no custom extension to emit amr) must remain valid.
fail_contract("authentication-assurance.schema.json must not require amr (ACR-or-AMR evidence, architecture owner 2026-10-02)") if assurance.fetch("required", []).include?("amr")
fail_contract("authentication-assurance.schema.json must still describe amr") unless assurance.dig("properties", "amr")

requirement = load_json("contracts/identity/v1/assurance-requirement.schema.json")
fail_contract("assurance-requirement.schema.json requires exactly minimum_acr") unless requirement.fetch("required", []) == ["minimum_acr"]
%w[accepted_acr_values accepted_methods max_authentication_age_seconds phishing_resistant_required].each do |field|
  fail_contract("assurance-requirement.schema.json is missing property #{field.inspect}") unless requirement.dig("properties", field)
end

# 4. workload-registry.yaml (ADR-0007 §§22-25, §42): every workload is
#    least-privilege and audience-bound. Each allowed scope is registered,
#    usable by workloads, never privileged, and issued for one of the
#    workload's audiences; each audience is used by at least one scope.
scopes = load_yaml("contracts/authorization/v1/scope-registry.yaml").fetch("scopes").to_h { |s| [s.fetch("name"), s] }
workloads = load_yaml("contracts/identity/v1/workload-registry.yaml").fetch("workloads")
fail_contract("workload-registry.yaml declares no workloads") if workloads.nil? || workloads.empty?
# A profile label (e.g. INT-02 integration) cannot invent an identity
# environment that conforming IAM/CP consumers cannot represent.
known_environments = load_json("contracts/identity/v1/workload-identity.schema.json").fetch("properties").fetch("environment").fetch("enum")
known_statuses = %w[PROVISIONED ACTIVE SUSPENDED REVOKED RETIRED]
known_credentials = %w[client_credentials federated_workload_token]
workloads.each do |client_id, entry|
  %w[repository owner runtime environment allowed_audiences allowed_scopes credential_type rotation_owner status].each do |field|
    fail_contract("workload #{client_id} is missing #{field}") if entry[field].nil? || entry[field].to_s.strip.empty?
  end
  fail_contract("workload #{client_id} has noncanonical environment #{entry['environment'].inspect}") unless known_environments.include?(entry["environment"])
  fail_contract("workload #{client_id} has unknown status #{entry['status'].inspect}") unless known_statuses.include?(entry["status"])
  fail_contract("workload #{client_id} has unknown credential_type #{entry['credential_type'].inspect}") unless known_credentials.include?(entry["credential_type"])
  audiences = entry.fetch("allowed_audiences")
  fail_contract("workload #{client_id} must name at least one audience and one scope") if audiences.empty? || entry.fetch("allowed_scopes").empty?
  used = []
  entry.fetch("allowed_scopes").each do |name|
    scope = scopes[name]
    fail_contract("workload #{client_id} allows unregistered scope #{name}") if scope.nil?
    fail_contract("workload #{client_id} allows #{name}, which is not a workload scope") unless Array(scope["allowed_actors"]).include?("workload")
    # ADR-SHARED-044 current reads/preflight are sensitive workload-only ports,
    # not human administration. Permit only this exact ADR-043 proof client;
    # its complete row is pinned below and no positive financial scope exists.
    subscription_probe = client_id == "baobab-dev-subscriptions-assessor" &&
      entry["environment"] == "development" &&
      %w[subscription:current-workload-read subscription:commercial-authority].include?(name)
    fail_contract("workload #{client_id} allows privileged scope #{name}") if scope["privileged"] && !subscription_probe
    shared = Array(scope["audience"]) & audiences
    fail_contract("workload #{client_id} allows #{name}, which is not issued for any of its audiences #{audiences}") if shared.empty?
    used.concat(shared)
  end
  (audiences - used).each do |audience|
    fail_contract("workload #{client_id} allows audience #{audience} but no scope issued for it")
  end
  # docs/architecture/context-authority-for-workloads.md: the validator-to-subject-audience relationship is explicit and
  # registered, never inferred from allowed_audiences and never chosen by a request. Required of exactly the workloads that
  # may hold context:validate, and nobody else.
  validates = entry["validates_audiences"]
  if entry.fetch("allowed_scopes").include?("context:validate")
    unless validates.is_a?(Array) && !validates.empty? && validates.uniq.size == validates.size && validates.all? { |a| a.is_a?(String) && !a.strip.empty? }
      fail_contract("workload #{client_id} allows context:validate, so it must list validates_audiences (distinct, non-empty)")
    end
    validates.each do |audience|
      fail_contract("workload #{client_id} validates_audiences must not include baobab-control-plane") if audience == "baobab-control-plane"
      unless scopes.values.any? { |scope| Array(scope["audience"]).include?(audience) }
        fail_contract("workload #{client_id} validates audience #{audience}, which no registered scope is issued for")
      end
    end
  elsif !validates.nil?
    fail_contract("workload #{client_id} lists validates_audiences but does not allow context:validate")
  end
  # ADR-SHARED-042 section 3: delegated human Principal resolution needs a registered validator relationship scoped to the
  # expected human audience. Required of exactly the workloads holding a principal-resolution scope, and nobody else.
  # The estate client binding resolution (CAA-04) verifies the BFF's evidence for the same audience, so it needs it too.
  principal_scopes = %w[identity:principal:resolve identity:principal:register-buyer estate:client-binding:resolve]
  subject_audiences = entry["subject_principal_audiences"]
  if (entry.fetch("allowed_scopes") & principal_scopes).any?
    unless subject_audiences.is_a?(Array) && !subject_audiences.empty? && subject_audiences.uniq.size == subject_audiences.size &&
           subject_audiences.all? { |a| a.is_a?(String) && !a.strip.empty? }
      fail_contract("workload #{client_id} allows a principal-resolution scope, so it must list subject_principal_audiences (distinct, non-empty)")
    end
    subject_audiences.each do |audience|
      fail_contract("workload #{client_id} subject_principal_audiences must not include baobab-control-plane") if audience == "baobab-control-plane"
      unless scopes.values.any? { |scope| Array(scope["audience"]).include?(audience) && Array(scope["allowed_actors"]) == ["human"] }
        fail_contract("workload #{client_id} subject audience #{audience} is not one any human-only registered scope is issued for")
      end
    end
  elsif !subject_audiences.nil?
    fail_contract("workload #{client_id} lists subject_principal_audiences but holds no principal-resolution scope")
  end
  # ADR-SHARED-042 section 14 (CAA-03/CAA-04): a confidential estate BFF that obtains human buyer tokens registers the human
  # resource scopes and audiences it may request as human_token_profile, and holds trade:buyer-handoff so it can authenticate
  # to Trade as itself when presenting them. Neither is held without the other, and only a confidential client qualifies.
  human_profile = entry["human_token_profile"]
  holds_handoff = entry.fetch("allowed_scopes").include?("trade:buyer-handoff")
  if human_profile.nil?
    fail_contract("workload #{client_id} holds trade:buyer-handoff but registers no human_token_profile") if holds_handoff
  else
    unless human_profile.is_a?(Hash) && human_profile.keys.sort == %w[audiences purpose scopes]
      fail_contract("workload #{client_id} human_token_profile must name exactly purpose, audiences and scopes")
    end
    fail_contract("workload #{client_id} human_token_profile purpose must be ESTATE_BFF_BUYER") unless human_profile["purpose"] == "ESTATE_BFF_BUYER"
    fail_contract("workload #{client_id} human_token_profile requires a client_credentials (confidential) client") unless entry["credential_type"] == "client_credentials"
    fail_contract("workload #{client_id} human_token_profile requires trade:buyer-handoff") unless holds_handoff
    profile_audiences, profile_scopes = human_profile["audiences"], human_profile["scopes"]
    [profile_audiences, profile_scopes].each do |values|
      unless values.is_a?(Array) && !values.empty? && values.uniq.size == values.size && values.all? { |v| v.is_a?(String) && !v.strip.empty? }
        fail_contract("workload #{client_id} human_token_profile audiences and scopes must be distinct, non-empty lists")
      end
    end
    fail_contract("workload #{client_id} human_token_profile must not include baobab-control-plane") if profile_audiences.include?("baobab-control-plane")
    profile_scopes.each do |name|
      scope = scopes[name]
      unless scope && Array(scope["allowed_actors"]) == ["human"] && (Array(scope["audience"]) & profile_audiences).any?
        fail_contract("workload #{client_id} human_token_profile scope #{name} is not a human-only scope issued for its audiences")
      end
    end
    profile_audiences.each do |audience|
      unless profile_scopes.any? { |name| Array(scopes[name] && scopes[name]["audience"]).include?(audience) }
        fail_contract("workload #{client_id} human_token_profile audience #{audience} has no human scope")
      end
    end
  end
  # docs/architecture/context-authority-for-workloads.md section 13: a context purpose other than the implicit RUNTIME is
  # explicit, distinct and known. TENANT_PROVISIONING (pre-activation provisioning authority) belongs to a provisioner that
  # can never also be a runtime resolver or a validator, and that has no client secret to leak.
  purposes = entry["context_purposes"]
  unless purposes.nil?
    unless purposes.is_a?(Array) && !purposes.empty? && purposes.uniq.size == purposes.size && (purposes - %w[RUNTIME TENANT_PROVISIONING]).empty?
      fail_contract("workload #{client_id} context_purposes must be a distinct, non-empty list of RUNTIME or TENANT_PROVISIONING")
    end
    if purposes.include?("TENANT_PROVISIONING")
      %w[context:resolve context:validate].each do |held|
        fail_contract("workload #{client_id} may provision tenants before activation, so it must not allow #{held}") if entry.fetch("allowed_scopes").include?(held)
      end
      fail_contract("workload #{client_id} may provision tenants before activation, so it must use federated_workload_token") unless entry["credential_type"] == "federated_workload_token"
      fail_contract("workload #{client_id} may provision tenants before activation, so it must not also list RUNTIME") if purposes.include?("RUNTIME")
    end
  end
  # ADR-BCP-025 section 2.9: a reporter is registered for the environments
  # and regions it may report on. Its environment is `environment`; its
  # regions are `deployment_regions`, required of exactly the workloads that
  # may hold deployment:observe, and nobody else.
  regions = entry["deployment_regions"]
  if entry.fetch("allowed_scopes").include?("deployment:observe")
    unless regions.is_a?(Array) && !regions.empty? && regions.uniq.size == regions.size && regions.all? { |r| r.is_a?(String) && r.match?(/\A[a-z][a-z0-9]*(?:-[a-z0-9]+)*\z/) && r.length <= 63 }
      fail_contract("workload #{client_id} allows deployment:observe, so it must list its deployment_regions (distinct, lower-case region names)")
    end
  elsif !regions.nil?
    fail_contract("workload #{client_id} lists deployment_regions but does not allow deployment:observe")
  end
end

# Owner decision 2026-10-18: one named, disposable development evidence
# producer may bootstrap its own proof. Exact hash equality also rejects new
# authority-bearing fields; this does not relax any other workload lifecycle.
int02_expected = {
  "repository" => "baobab-platform/infrastructure",
  "owner" => "baobab-platform/infrastructure",
  "runtime" => "INT-02 disposable real-component Pulse qualification consumer",
  "environment" => "development",
  "allowed_audiences" => %w[baobab-control-plane baobab-pulse],
  "allowed_scopes" => %w[context:resolve intelligence:evidence:search],
  "credential_type" => "client_credentials",
  "rotation_owner" => "baobab-platform/infrastructure",
  "status" => "ACTIVE"
}
fail_contract("INT-02 proof-bootstrap identity must match its exact owner-approved boundary") unless workloads["baobab-int02-pulse-consumer"] == int02_expected

# Accepted INT-03C proof-bootstrap exception is exactly TWO development-only
# identities. Unlike a normal resource-server validator, the issuer verifier
# needs only independent OAuth introspection at IAM and NO context:validate
# privilege. Extra registry powers require a new explicit architecture decision.
int03c_expected = {
  "baobab-int03c-issuer-owner" => {
    "repository" => "baobab-platform/infrastructure",
    "owner" => "baobab-platform/infrastructure",
    "runtime" => "INT-03C supervised disposable issuer proof owner",
    "environment" => "development",
    "allowed_audiences" => %w[baobab-control-plane],
    "allowed_scopes" => %w[context:resolve],
    "credential_type" => "client_credentials",
    "rotation_owner" => "baobab-platform/infrastructure",
    "status" => "ACTIVE"
  },
  "baobab-int03c-issuer-verifier" => {
    "repository" => "baobab-platform/infrastructure",
    "owner" => "baobab-platform/infrastructure",
    "runtime" => "INT-03C independent disposable issuer verifier",
    "environment" => "development",
    "allowed_audiences" => %w[baobab-control-plane],
    "allowed_scopes" => %w[context:resolve],
    "credential_type" => "client_credentials",
    "rotation_owner" => "baobab-platform/infrastructure",
    "status" => "ACTIVE"
  }
}
int03c_expected.each do |name, expected|
  fail_contract("INT-03C proof-bootstrap identity #{name} exceeds approved ceiling") unless workloads[name] == expected
end
int03c_actual = workloads.keys.grep(/\Abaobab-int03c-/)
fail_contract("INT-03C identity count exceeds the two named proof clients") unless int03c_actual.sort == int03c_expected.keys.sort


# ADR-SHARED-043: these isolated development callers are exact ceilings,
# not a production activation or a wildcard administrative bootstrap.
development_expected = JSON.parse(<<~JSON)
{
  "baobab-int03-cms-consumer": {
    "repository": "baobab-platform/infrastructure",
    "owner": "baobab-platform/infrastructure",
    "runtime": "ADR-SHARED-043 disposable development baobab-int03-cms-consumer",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane",
      "baobab-cms"
    ],
    "allowed_scopes": [
      "context:resolve",
      "content:entry:resolve"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/infrastructure",
    "status": "ACTIVE"
  },
  "baobab-int03-cms-validator": {
    "repository": "baobab-platform/baobab-cms",
    "owner": "baobab-platform/baobab-cms",
    "runtime": "ADR-SHARED-043 disposable development baobab-int03-cms-validator",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane"
    ],
    "allowed_scopes": [
      "context:validate"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/baobab-cms",
    "status": "ACTIVE",
    "validates_audiences": [
      "baobab-cms"
    ]
  },
  "baobab-dev-nabhold-estate": {
    "repository": "baobab-platform/nabhold",
    "owner": "baobab-platform/nabhold",
    "runtime": "ADR-SHARED-043 disposable development baobab-dev-nabhold-estate",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane",
      "baobab-cms"
    ],
    "allowed_scopes": [
      "context:resolve",
      "content:entry:resolve"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/nabhold",
    "status": "ACTIVE"
  },
  "baobab-dev-zuribeans-estate": {
    "repository": "baobab-platform/zuribeans",
    "owner": "baobab-platform/zuribeans",
    "runtime": "ADR-SHARED-043 disposable development baobab-dev-zuribeans-estate",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane",
      "baobab-cms"
    ],
    "allowed_scopes": [
      "context:resolve",
      "content:entry:resolve"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/zuribeans",
    "status": "ACTIVE"
  },
  "baobab-dev-thamani-estate": {
    "repository": "baobab-platform/thamani",
    "owner": "baobab-platform/thamani",
    "runtime": "ADR-SHARED-043 disposable development baobab-dev-thamani-estate",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane",
      "baobab-cms"
    ],
    "allowed_scopes": [
      "context:resolve",
      "content:entry:resolve"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/thamani",
    "status": "ACTIVE"
  },
  "baobab-dev-equator-estate-estate": {
    "repository": "baobab-platform/equator-estate",
    "owner": "baobab-platform/equator-estate",
    "runtime": "ADR-SHARED-043 disposable development baobab-dev-equator-estate-estate",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane",
      "baobab-cms"
    ],
    "allowed_scopes": [
      "context:resolve",
      "content:entry:resolve"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/equator-estate",
    "status": "ACTIVE"
  }
}
JSON
# DEV-06 extends the closed development registry, never its production identities.
development_expected.merge!(JSON.parse(<<~'JSON'))
{
  "baobab-dev-external-api": {
    "repository": "baobab-platform/infrastructure",
    "owner": "baobab-platform/infrastructure",
    "runtime": "DEV-06 synthetic EXTERNAL_CLIENT API-only workload",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane",
      "baobab-pulse"
    ],
    "allowed_scopes": [
      "context:resolve",
      "intelligence:evidence:search"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/infrastructure",
    "status": "ACTIVE"
  },
  "baobab-dev-pulse-validator": {
    "repository": "baobab-platform/baobab-pulse",
    "owner": "baobab-platform/baobab-pulse",
    "runtime": "DEV-06 independent disposable Pulse context validator",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane"
    ],
    "allowed_scopes": [
      "context:validate"
    ],
    "validates_audiences": [
      "baobab-pulse"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/baobab-pulse",
    "status": "ACTIVE"
  }
}
JSON
# Subscriptions development proof has exact ceilings, not production activation.
development_expected.merge!(JSON.parse(<<~'JSON'))
{
  "baobab-dev-cp-subscriptions": {
    "repository": "baobab-platform/baobab-cp",
    "owner": "baobab-platform/baobab-cp",
    "runtime": "ADR-SHARED-043 disposable CP subscription command and event producer",
    "environment": "development",
    "allowed_audiences": [
      "baobab-subscriptions"
    ],
    "allowed_scopes": [
      "billing:manage",
      "billing:read",
      "billing:observe",
      "usage:record"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/baobab-cp",
    "status": "ACTIVE"
  },
  "baobab-dev-subscriptions-assessor": {
    "repository": "baobab-platform/baobab-subscriptions",
    "owner": "baobab-platform/baobab-subscriptions",
    "runtime": "ADR-SHARED-043 disposable Subscriptions current CP authority reader",
    "environment": "development",
    "allowed_audiences": [
      "baobab-control-plane"
    ],
    "allowed_scopes": [
      "subscription:internal-authority",
      "subscription:current-workload-read",
      "subscription:commercial-authority"
    ],
    "credential_type": "client_credentials",
    "rotation_owner": "baobab-platform/baobab-subscriptions",
    "status": "ACTIVE"
  }
}
JSON
development_expected.each do |name, expected|
  fail_contract("development identity #{name} exceeds its exact ADR-043 ceiling") unless workloads[name] == expected
end
unless workloads.keys.grep(/\Abaobab-dev-/).sort == development_expected.keys.grep(/\Abaobab-dev-/).sort
  fail_contract("unregistered development estate identity")
end

# 5. Every scope an OpenAPI operation requires is registered, and a
#    Control Plane operation's scope is issued for the Control Plane's
#    audience (ADR-BCP-022 section 18: the contract never names a scope the
#    registry does not govern).
# Trade's B2B API declares its requirement once at the top level, which every
# operation without its own `security` inherits (OpenAPI 3.1).
# The private identity/v1 Principal resolution and control-plane/v1 estate binding APIs are Control Plane surfaces.
{ "contracts/control-plane/v1/openapi.yaml" => "baobab-control-plane",
  "contracts/identity/v1/principal-resolution.openapi.yaml" => "baobab-control-plane",
  "contracts/control-plane/v1/estate-client-binding.openapi.yaml" => "baobab-control-plane",
  "contracts/trade/v1/openapi.yaml" => "baobab-trade" }.each do |path, audience|
  document = load_yaml(path)
  document.fetch("paths").each do |route, item|
    item.each do |method, operation|
      next unless operation.is_a?(Hash)
      security = operation.fetch("security", document["security"])
      next if security.nil?
      security.each do |requirement|
        requirement.each_value do |required|
          required.each do |name|
            scope = scopes[name]
            fail_contract("#{path} #{method.upcase} #{route} requires unregistered scope #{name}") if scope.nil?
            unless Array(scope["audience"]).include?(audience)
              fail_contract("#{path} #{method.upcase} #{route} requires #{name}, which is not issued for #{audience}")
            end
          end
        end
      end
    end
  end
end

puts "Authorization contract validation passed"
