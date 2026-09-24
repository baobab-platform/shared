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
%w[BadRequest Unauthorized Forbidden NotFound Conflict].each do |response|
  ref = openapi.dig("components", "responses", response, "content", "application/problem+json", "schema", "$ref")
  fail_contract("#{response} does not use canonical problem details") unless ref == "#/components/schemas/ProblemDetails"
end
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
