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
#    unique, every category is one of the three this registry documents, and
#    every code matches the same UPPER_SNAKE_CASE convention
#    contracts/errors/v1/problem-details.schema.json already enforces for
#    Baobab machine-readable codes generally.
registry = load_yaml("contracts/authorization/v1/reason-code-registry.yaml")
entries = registry.fetch("reason_codes")
fail_contract("reason-code-registry.yaml declares no codes") if entries.empty?

known_categories = %w[authorization_denial lifecycle_revocation capability_resolution_denial]
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
%w[actor_type acr amr authenticated_at issuer client_id].each do |field|
  fail_contract("authentication-assurance.schema.json is missing required field #{field.inspect}") unless assurance.fetch("required", []).include?(field)
end

requirement = load_json("contracts/identity/v1/assurance-requirement.schema.json")
%w[minimum_acr accepted_methods].each do |field|
  fail_contract("assurance-requirement.schema.json is missing required field #{field.inspect}") unless requirement.fetch("required", []).include?(field)
end

# 4. workload-registry.yaml (ADR-0007 §§22-25, §42): every workload is
#    least-privilege and audience-bound. Each allowed scope is registered,
#    usable by workloads, never privileged, and issued for one of the
#    workload's audiences; each audience is used by at least one scope.
scopes = load_yaml("contracts/authorization/v1/scope-registry.yaml").fetch("scopes").to_h { |s| [s.fetch("name"), s] }
workloads = load_yaml("contracts/identity/v1/workload-registry.yaml").fetch("workloads")
fail_contract("workload-registry.yaml declares no workloads") if workloads.nil? || workloads.empty?
known_statuses = %w[PROVISIONED ACTIVE SUSPENDED REVOKED RETIRED]
known_credentials = %w[client_credentials federated_workload_token]
workloads.each do |client_id, entry|
  %w[repository owner runtime environment allowed_audiences allowed_scopes credential_type rotation_owner status].each do |field|
    fail_contract("workload #{client_id} is missing #{field}") if entry[field].nil? || entry[field].to_s.strip.empty?
  end
  fail_contract("workload #{client_id} has unknown status #{entry['status'].inspect}") unless known_statuses.include?(entry["status"])
  fail_contract("workload #{client_id} has unknown credential_type #{entry['credential_type'].inspect}") unless known_credentials.include?(entry["credential_type"])
  audiences = entry.fetch("allowed_audiences")
  fail_contract("workload #{client_id} must name at least one audience and one scope") if audiences.empty? || entry.fetch("allowed_scopes").empty?
  used = []
  entry.fetch("allowed_scopes").each do |name|
    scope = scopes[name]
    fail_contract("workload #{client_id} allows unregistered scope #{name}") if scope.nil?
    fail_contract("workload #{client_id} allows #{name}, which is not a workload scope") unless Array(scope["allowed_actors"]).include?("workload")
    fail_contract("workload #{client_id} allows privileged scope #{name}") if scope["privileged"]
    shared = Array(scope["audience"]) & audiences
    fail_contract("workload #{client_id} allows #{name}, which is not issued for any of its audiences #{audiences}") if shared.empty?
    used.concat(shared)
  end
  (audiences - used).each do |audience|
    fail_contract("workload #{client_id} allows audience #{audience} but no scope issued for it")
  end
end

puts "Authorization contract validation passed"
