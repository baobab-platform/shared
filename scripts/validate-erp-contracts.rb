# frozen_string_literal: true

require "json"
require "time"
require "uri"
require "yaml"

ROOT = File.expand_path("..", __dir__)
ERP_ROOT = File.join(ROOT, "contracts/erp/v1")
UUID_PATTERN = /\A[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\z/i

def fail_contract(message)
  warn "ERP contract validation failed: #{message}"
  exit 1
end

def load_json(path)
  JSON.parse(File.read(path))
rescue JSON::ParserError => error
  fail_contract("#{path} is invalid JSON: #{error.message}")
end

def load_yaml(path)
  YAML.safe_load_file(path, aliases: false)
rescue Psych::Exception => error
  fail_contract("#{path} is invalid or uses YAML aliases: #{error.message}")
end

def walk_keys(value, path = [], &block)
  case value
  when Hash
    value.each do |key, child|
      block.call(key, path + [key])
      walk_keys(child, path + [key], &block)
    end
  when Array
    value.each_with_index { |child, index| walk_keys(child, path + [index], &block) }
  end
end

json_paths = Dir[File.join(ERP_ROOT, "**/*.json")].sort
yaml_paths = Dir[File.join(ERP_ROOT, "**/*.{yaml,yml}")].sort
fail_contract("ERP package contains no JSON schemas") if json_paths.empty?
json_documents = json_paths.to_h { |path| [path, load_json(path)] }
yaml_paths.each { |path| load_yaml(path) }

schemas = json_documents.select { |_path, document| document.key?("$schema") }
schemas.each do |path, schema|
  fail_contract("#{path} must use JSON Schema 2020-12") unless schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
  fail_contract("#{path} must have an immutable contract URI") unless schema.fetch("$id", "").start_with?("https://contracts.baobab-platform.com/erp/v1/")
  walk_keys(schema) do |key, key_path|
    if key.match?(/\A(?:AD_Client_ID|AD_Org_ID|C_BPartner_ID|C_Order_ID|C_Invoice_ID|C_Payment_ID|M_Product_ID|M_Warehouse_ID)\z/i)
      fail_contract("#{path} exposes vendor field #{key.inspect} at #{key_path.join('.')}")
    end
  end
end

domain = schemas.fetch(File.join(ERP_ROOT, "domain.schema.json"))
mapping = schemas.fetch(File.join(ERP_ROOT, "mapping.schema.json"))
canonical_ref = domain.dig("$defs", "canonicalReference")
unless canonical_ref.fetch("required") == %w[owner resource_type resource_id]
  fail_contract("canonical references must identify owner, resource type and resource ID")
end

legal_entity_scoped_schemas = %w[
  business-partner-projection.schema.json
  commerce-order-consequence.schema.json
  customer-projection.schema.json
  inventory-availability.schema.json
  invoice-outcome.schema.json
  order-consequence-status.schema.json
  payment-outcome.schema.json
  warehouse-projection.schema.json
]
legal_entity_scoped_schemas.each do |schema_name|
  required = schemas.fetch(File.join(ERP_ROOT, schema_name)).fetch("required")
  fail_contract("#{schema_name} lacks legal-entity context") unless required.include?("legal_entity_id")
end
unless mapping.fetch("required").include?("tenant_id") &&
       mapping.fetch("required").include?("legal_entity_id") &&
       mapping.fetch("required").include?("effective_from") &&
       mapping.dig("properties", "erp_resource_id", "$ref") == "./domain.schema.json#/$defs/erpResourceId"
  fail_contract("mapping is not tenant-scoped, legal-entity-aware, temporal and vendor-neutral")
end

envelope = load_json(File.join(ROOT, "contracts/events/v1/envelope.schema.json"))
envelope_required = envelope.fetch("required")
envelope_properties = envelope.fetch("properties")
tenant_pattern = Regexp.new(load_json(File.join(ROOT, "contracts/control-plane/v1/domain.schema.json")).dig("$defs", "tenantId", "pattern"))
registry = load_yaml(File.join(ROOT, "contracts/legal-entity/registry.yaml"))
legal_entity_ids = registry.fetch("entities").map { |entity| entity.fetch("id") }

examples = json_documents.reject { |_path, document| document.key?("$schema") }
fail_contract("ERP event examples are missing") if examples.empty?
examples.each do |path, event|
  missing = envelope_required - event.keys
  unknown = event.keys - envelope_properties.keys
  fail_contract("#{path} misses envelope fields: #{missing.join(', ')}") unless missing.empty?
  fail_contract("#{path} has unknown envelope fields: #{unknown.join(', ')}") unless unknown.empty?
  fail_contract("#{path} is not tenant scoped") unless event["baobabscope"] == "tenant"
  fail_contract("#{path} has a noncanonical tenant") unless tenant_pattern.match?(event.fetch("tenantid"))
  fail_contract("#{path} event id is not a UUID") unless UUID_PATTERN.match?(event.fetch("id"))
  fail_contract("#{path} correlationid is not a UUID") unless UUID_PATTERN.match?(event.fetch("correlationid"))
  fail_contract("#{path} has an invalid causationid") if event.key?("causationid") && !UUID_PATTERN.match?(event["causationid"])
  fail_contract("#{path} time is not UTC") unless event.fetch("time").end_with?("Z")
  begin
    Time.iso8601(event.fetch("time"))
  rescue ArgumentError
    fail_contract("#{path} time is not ISO 8601")
  end

  schema_name = URI.parse(event.fetch("dataschema")).path.split("/").last
  payload_schema_path = File.join(ERP_ROOT, schema_name)
  payload_schema = schemas[payload_schema_path]
  fail_contract("#{path} references missing payload schema #{schema_name}") unless payload_schema
  payload = event.fetch("data")
  payload_missing = payload_schema.fetch("required") - payload.keys
  payload_unknown = payload.keys - payload_schema.fetch("properties").keys
  fail_contract("#{path} payload misses: #{payload_missing.join(', ')}") unless payload_missing.empty?
  fail_contract("#{path} payload has unknown fields: #{payload_unknown.join(', ')}") unless payload_unknown.empty?
  payload_entity_ids = if payload.key?("legal_entity_id")
                         [payload.fetch("legal_entity_id")]
                       else
                         payload.fetch("legal_entity_ids", [])
                       end
  unless !payload_entity_ids.empty? && (payload_entity_ids - legal_entity_ids).empty?
    fail_contract("#{path} lacks canonical legal-entity context")
  end

  walk_keys(payload) do |key, key_path|
    next unless key == "currency"
    parent = key_path[0...-1].reduce(payload) { |memo, segment| memo.fetch(segment) }
    value = parent.fetch(key)
    fail_contract("#{path} has invalid currency #{value.inspect}") unless value.is_a?(String) && value.match?(/\A[A-Z]{3}\z/)
  end
end

asyncapi = load_yaml(File.join(ERP_ROOT, "asyncapi.yaml"))
messages = asyncapi.dig("components", "messages") || {}
fail_contract("AsyncAPI message set and example set differ") unless messages.length == examples.length
message_names = messages.values.map { |message| message.fetch("name") }.sort
example_types = examples.values.map { |event| event.fetch("type") }.sort
fail_contract("AsyncAPI message names do not match example event types") unless message_names == example_types
messages.each do |name, message|
  all_of = message.dig("payload", "allOf") || []
  fail_contract("#{name} does not consume the canonical event envelope") unless all_of.first == { "$ref" => "../../events/v1/envelope.schema.json" }
  data_ref = all_of.dig(1, "properties", "data", "$ref")
  fail_contract("#{name} does not bind a versioned ERP data schema") unless data_ref&.match?(/\A\.\/[a-z0-9-]+\.schema\.json\z/)
end

openapi = load_yaml(File.join(ERP_ROOT, "openapi.yaml"))
fail_contract("ERP OpenAPI must be version 3.1") unless openapi["openapi"] == "3.1.0"
problem_ref = "../../errors/v1/problem-details.schema.json"
unless openapi.dig("components", "schemas", "ProblemDetails", "$ref") == problem_ref
  fail_contract("ERP OpenAPI does not consume canonical problem details")
end
%w[BadRequest Unauthorized Forbidden NotFound Conflict ServiceUnavailable NotImplemented].each do |response|
  ref = openapi.dig("components", "responses", response, "content", "application/problem+json", "schema", "$ref")
  fail_contract("#{response} does not use canonical problem details") unless ref == "#/components/schemas/ProblemDetails"
end
# 501 is a narrow, transitional response (ERP OpenAPI 1.0.1): the provider recognises the canonical operation but
# the backing capability is absent in this engine release. Exactly these operations may declare it; it is never a
# readiness outcome and is distinct from 503 (an implemented capability temporarily unavailable).
# ERP OpenAPI 1.0.5: ERP serves every operation of the contract, so none declares 501 now. The NotImplemented response
# stays defined, with its wording pinned, for an operation a later contract declares before an engine builds it.
not_implemented_operations = []
declaring_501 = openapi.fetch("paths").flat_map do |path, item|
  item.select { |method, operation| operation.is_a?(Hash) && operation.fetch("responses", {}).key?("501") }
      .keys.map { |method| [method, path] }
end
unless declaring_501.sort == not_implemented_operations.sort
  fail_contract("only #{not_implemented_operations.inspect} may declare 501; found #{declaring_501.inspect}")
end
not_implemented_operations.each do |method, path|
  unless openapi.dig("paths", path, method, "responses", "501", "$ref") == "#/components/responses/NotImplemented"
    fail_contract("#{method.upcase} #{path} must reference the reusable NotImplemented response")
  end
end
not_implemented_text = openapi.dig("components", "responses", "NotImplemented", "description").to_s.gsub(/\s+/, " ")
unless not_implemented_text.include?("not implemented in this engine release") &&
       not_implemented_text.include?("not a transient outage") &&
       not_implemented_text.include?("503") &&
       not_implemented_text.include?("must not be certified")
  fail_contract("NotImplemented must state that 501 is an absent capability, not an outage or a readiness outcome")
end
[["get", "/mappings/{mapping_id}"], ["get", "/mappings"]].each do |method, path|
  unless openapi.dig("paths", path, method, "responses", "400", "$ref") == "#/components/responses/BadRequest"
    fail_contract("#{method.upcase} #{path} must declare 400 BadRequest for malformed identifiers and query parameters")
  end
end
# ERP provisioning is authorised by one exact Control Plane plan (ERP OpenAPI 1.0.2). The request must name it with
# the full approval-binding tuple, not only the provisioning, so a replan cannot change what ERP executes.
provisioning_request = JSON.parse(File.read(File.join(ERP_ROOT, "provisioning-request.schema.json")))
authority = provisioning_request.dig("properties", "control_plane_authority")
fail_contract("provisioning request must require control_plane_authority") unless provisioning_request.fetch("required").include?("control_plane_authority") && authority
authority_members = %w[tenant_provisioning_id plan_id plan_version plan_digest]
unless authority.fetch("required").sort == authority_members.sort && authority.fetch("properties").keys.sort == authority_members.sort && authority["additionalProperties"] == false
  fail_contract("control_plane_authority must be exactly #{authority_members.inspect} and closed")
end
{ "tenant_provisioning_id" => "#/$defs/tenantProvisioningId", "plan_id" => "#/$defs/provisioningPlanId", "plan_digest" => "#/$defs/planDigest" }.each do |member, definition|
  unless authority.dig("properties", member, "$ref") == "../../control-plane/v1/domain.schema.json" + definition
    fail_contract("control_plane_authority.#{member} must reuse the Control Plane #{definition}")
  end
end
fail_contract("control_plane_authority.plan_version must be an integer >= 1") unless authority.dig("properties", "plan_version") == { "type" => "integer", "minimum" => 1 }
if provisioning_request.fetch("properties").key?("approval_id")
  fail_contract("the provisioning request must not carry an approval id: approval semantics are Control Plane's")
end
post_text = openapi.dig("paths", "/provisioning-operations", "post", "description").to_s.gsub(/\s+/, " ")
["control_plane_authority", "PLAN_AUTHORITY_MISMATCH", "provisions nothing", "intent, not authority", "Finance-approved baseline"].each do |phrase|
  fail_contract("POST /provisioning-operations must document #{phrase.inspect}") unless post_text.include?(phrase)
end
# 503 (ERP OpenAPI 1.0.3) is the implemented-but-temporarily-unavailable counterpart of 501: provisioning needs
# Control Plane's ERP assignment and the Finance baseline store, and a retry with the same Idempotency-Key is safe.
# Only the provisioning command declares it, and the by-id read declares 400 for a malformed operation id.
declaring_503 = openapi.fetch("paths").flat_map do |path, item|
  item.select { |method, operation| operation.is_a?(Hash) && operation.fetch("responses", {}).key?("503") }
      .keys.map { |method| [method, path] }
end
unless declaring_503.sort == [["get", "/inventory-availability"], ["post", "/provisioning-operations"]]
  fail_contract("only POST /provisioning-operations and GET /inventory-availability may declare 503; found #{declaring_503.inspect}")
end
unless openapi.dig("paths", "/provisioning-operations", "post", "responses", "503", "$ref") == "#/components/responses/ServiceUnavailable"
  fail_contract("POST /provisioning-operations must reference the reusable ServiceUnavailable response")
end
# ERP OpenAPI 1.0.4: the inventory read depends on the engine's physical stock, so it too can be temporarily unavailable
# (503) and rejects a malformed sku_id or warehouse_id (400); neither answer carries a figure.
%w[400 503].each do |status|
  expected = status == "400" ? "BadRequest" : "ServiceUnavailable"
  unless openapi.dig("paths", "/inventory-availability", "get", "responses", status, "$ref") == "#/components/responses/#{expected}"
    fail_contract("GET /inventory-availability must declare #{status} #{expected}")
  end
end
inventory_text = openapi.dig("paths", "/inventory-availability", "get", "description").to_s.gsub(/\s+/, " ")
["physical inventory", "never from a Baobab-side stock ledger", "never from Trade", "not a commerce reservation", "no stale or estimated quantity"].each do |phrase|
  fail_contract("GET /inventory-availability must document #{phrase.inspect}") unless inventory_text.include?(phrase)
end
# Operations ERP serves do not declare the transitional 501 (ERP OpenAPI 1.0.4 and 1.0.5).
[["post", "/provisioning-operations"], ["get", "/provisioning-operations/{operation_id}"], ["get", "/order-consequences/{commerce_order_id}"], ["get", "/inventory-availability"]].each do |method, path|
  fail_contract("#{method.upcase} #{path} is served and must not declare 501") if openapi.dig("paths", path, method, "responses").key?("501")
end
unless openapi.dig("paths", "/provisioning-operations/{operation_id}", "get", "responses", "400", "$ref") == "#/components/responses/BadRequest"
  fail_contract("GET /provisioning-operations/{operation_id} must declare 400 BadRequest for a malformed operation id")
end
unavailable = openapi.dig("components", "responses", "ServiceUnavailable")
unavailable_text = unavailable.fetch("description").to_s.gsub(/\s+/, " ")
["temporarily unavailable", "nothing was provisioned", "same Idempotency-Key", "distinct from 501"].each do |phrase|
  fail_contract("ServiceUnavailable must state #{phrase.inspect}") unless unavailable_text.include?(phrase)
end
unless unavailable.dig("headers", "Retry-After", "schema", "type") == "integer"
  fail_contract("ServiceUnavailable must carry an integer Retry-After header")
end
# The two scopes the Boundary API requires are registered, workload-only and audience-bound to ERP, grant no authority of their own,
# and are allowed to the ERP workload and to no other workload (the tenant authority is the token's tenant_id claim, never the scope).
registry_scopes = load_yaml(File.join(ROOT, "contracts/authorization/v1/scope-registry.yaml")).fetch("scopes").to_h { |scope| [scope.fetch("name"), scope] }
required_scopes = openapi.fetch("paths").values.flat_map { |item| item.values.grep(Hash).flat_map { |operation| Array(operation["security"]).flat_map { |requirement| requirement["workloadOidc"] || [] } } }
required_scopes = (required_scopes + Array(openapi["security"]).flat_map { |requirement| requirement["workloadOidc"] || [] }).uniq.sort
fail_contract("the Boundary API must require exactly erp:read and erp:provision; found #{required_scopes.inspect}") unless required_scopes == %w[erp:provision erp:read]
required_scopes.each do |name|
  scope = registry_scopes[name]
  fail_contract("#{name} is required by the ERP Boundary API but is not in the scope registry") if scope.nil?
  unless scope["audience"] == ["baobab-erp"] && scope["allowed_actors"] == ["workload"] && scope["grants_authority"] == false && !scope["privileged"]
    fail_contract("#{name} must be a non-privileged workload-only scope for baobab-erp that grants no authority")
  end
  fail_contract("#{name} must say it grants no tenant authority") unless scope.fetch("description").include?("grants no tenant authority")
end
holders = load_yaml(File.join(ROOT, "contracts/identity/v1/workload-registry.yaml")).fetch("workloads").select { |_, entry| (entry["allowed_scopes"] & required_scopes).any? }.keys
fail_contract("only baobab-erp-workload may be allowed the ERP Boundary API scopes; found #{holders.inspect}") unless holders == ["baobab-erp-workload"]

idempotency = load_yaml(File.join(ROOT, "contracts/idempotency/v1/policy.yaml"))
header = openapi.dig("components", "parameters", "IdempotencyKey", "schema")
policy_key = idempotency.dig("http_commands", "key")
unless header["pattern"] == policy_key["allowed_pattern"] &&
       header["minLength"] == policy_key["min_length"] &&
       header["maxLength"] == policy_key["max_length"]
  fail_contract("ERP Idempotency-Key has drifted from the canonical policy")
end
side_effect_parameters = openapi.dig("paths", "/provisioning-operations", "post", "parameters") || []
unless side_effect_parameters.any? { |parameter| parameter["$ref"] == "#/components/parameters/IdempotencyKey" }
  fail_contract("ERP provisioning command must require canonical idempotency metadata")
end

sor = load_yaml(File.join(ERP_ROOT, "system-of-record.yaml"))
required_concepts = ["Tenant", "Legal Entity", "Organisation", "User", "Customer", "Business Partner", "Supplier", "Product", "SKU", "Price", "Currency", "Tax", "Sales Order", "Purchase Order", "Invoice", "Payment", "Inventory", "Warehouse", "Shipment", "Accounting Entry", "Asset", "Market", "Region", "Country"]
concepts = sor.fetch("concepts")
names = concepts.map { |entry| entry.fetch("concept") }
fail_contract("system-of-record concepts differ from the required set") unless names.sort == required_concepts.sort
required_sor_fields = %w[canonical_owner producer consumers external_identifier idempiere_representation medusa_representation synchronisation_direction consistency mechanism conflict_resolution]
concepts.each do |entry|
  missing = required_sor_fields - entry.keys
  fail_contract("#{entry['concept']} SOR entry misses: #{missing.join(', ')}") unless missing.empty?
  serialised = entry.values.join(" ").downcase
  fail_contract("#{entry['concept']} authorises bidirectional synchronisation") if serialised.include?("bidirectional")
end
organisation = concepts.find { |entry| entry["concept"] == "Organisation" }
unless organisation["canonical_owner"] == "control-plane"
  fail_contract("organisation canonical_owner must be control-plane (ADR-BCP-018)")
end
legal_entity = concepts.find { |entry| entry["concept"] == "Legal Entity" }
unless legal_entity["canonical_owner"] == "control-plane"
  fail_contract("legal entity canonical_owner must be control-plane runtime (ADR-BCP-018); Shared remains contract/first-party governance authority")
end

puts "ERP API, event, mapping, internationalisation and system-of-record contracts passed"
