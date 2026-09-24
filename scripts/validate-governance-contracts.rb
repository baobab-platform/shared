# frozen_string_literal: true

require "json"
require "yaml"

ROOT = File.expand_path("..", __dir__)

def fail_contract(message)
  warn "contract validation failed: #{message}"
  exit 1
end

def load_yaml(path)
  YAML.safe_load_file(File.join(ROOT, path), aliases: false)
end

def load_json(path)
  JSON.parse(File.read(File.join(ROOT, path)))
end

registry = load_yaml("contracts/legal-entity/registry.yaml")
tenancy = load_yaml("contracts/tenancy/tenancy.yaml")
domain = load_json("contracts/control-plane/v1/domain.schema.json")
registration_schema = load_json("contracts/control-plane/v1/tenant-registration.schema.json")
context_schema = load_json("contracts/control-plane/v1/context-resolution.schema.json")
openapi = load_yaml("contracts/control-plane/v1/openapi.yaml")
register_example = load_json("contracts/control-plane/v1/examples/register-tenant.json")
registration_response_example = load_json("contracts/control-plane/v1/examples/register-tenant-accepted.json")
context_example = load_json("contracts/control-plane/v1/examples/resolve-context.json")
provisioning_example = load_json("contracts/control-plane/v1/examples/provisioning-started.json")

entities = registry.fetch("entities")
entity_ids = entities.map { |entity| entity.fetch("id") }
fail_contract("legal-entity identifiers must be unique") unless entity_ids.uniq == entity_ids

canonical_entity_pattern = Regexp.new(domain.dig("$defs", "canonicalLegalEntityId", "pattern"))
legacy_entity_pattern = Regexp.new(domain.dig("$defs", "legacyLegalEntityAlias", "pattern"))
legal_entity_input_refs = domain.dig("$defs", "legalEntityIdInput", "oneOf").map { |entry| entry.fetch("$ref") }
expected_input_refs = ["#/$defs/canonicalLegalEntityId", "#/$defs/legacyLegalEntityAlias"]
fail_contract("legalEntityIdInput must contain only canonical and legacy input definitions") unless legal_entity_input_refs == expected_input_refs
fail_contract("legalEntityId must resolve to canonical output identity") unless domain.dig("$defs", "legalEntityId", "$ref") == "#/$defs/canonicalLegalEntityId"
fail_contract("legacy legal-entity aliases must remain lowercase snake case") unless legacy_entity_pattern.match?("zuribeans_za")

legacy_aliases = entities.flat_map { |entity| entity.fetch("legacy_aliases", []) }
fail_contract("legacy legal-entity aliases must be unique") unless legacy_aliases.uniq == legacy_aliases
legacy_aliases.each do |legacy_alias|
  fail_contract("#{legacy_alias.inspect} is not a valid legacy legal-entity alias") unless legacy_entity_pattern.match?(legacy_alias)
end

entity_ids.each do |entity_id|
  fail_contract("#{entity_id.inspect} is not a canonical legal-entity identifier") unless canonical_entity_pattern.match?(entity_id)
end

product_pattern = Regexp.new(domain.dig("$defs", "productId", "pattern"))
entities.each do |entity|
  products = entity.fetch("baobab_products", [])
  if entity.fetch("baobab_tenant") && products.empty?
    fail_contract("#{entity.fetch('id')} declares tenant intent without a product-consumption intent")
  end

  products.each do |entry|
    product_id = entry.fetch("product")
    fail_contract("#{product_id.inspect} is not a valid product identifier") unless product_pattern.match?(product_id)
  end
end

definition = tenancy.fetch("tenant_definition")
fail_contract("legal entity must remain the default tenant boundary") unless definition["legal_entity_is_default_boundary"] == true
fail_contract("legal entity and tenant must not be synonyms") unless definition["legal_entity_is_tenant_synonym"] == false
fail_contract("digital estates must not confer tenancy") unless definition["digital_estate_confers_tenancy"] == false
fail_contract("product consumption must require tenancy") unless definition["product_consumption_requires_tenant"] == true

tenant_pattern = Regexp.new(tenancy.dig("identifiers", "tenant_id", "exact_format"))
tenant_schema_pattern = domain.dig("$defs", "tenantId", "pattern")
fail_contract("tenantId schema and tenancy governance must use one exact grammar") unless tenant_schema_pattern == tenancy.dig("identifiers", "tenant_id", "exact_format")
fail_contract("registration commands must not accept caller-selected tenant_id") if registration_schema.fetch("required").include?("tenant_id") || registration_schema.fetch("properties").key?("tenant_id")
fail_contract("registration legal_entity_id must be the compatibility input boundary") unless registration_schema.dig("properties", "legal_entity_id", "$ref") == "domain.schema.json#/$defs/legalEntityIdInput"
fail_contract("context responses must emit canonical legal-entity IDs") unless context_schema.dig("$defs", "response", "properties", "entity_id", "$ref") == "domain.schema.json#/$defs/legalEntityId"
fail_contract("registration example must let the Control Plane mint tenant_id") if register_example.key?("tenant_id")
example_tenant_ids = [
  registration_response_example.fetch("tenant_id"),
  context_example.dig("response", "tenant_id"),
  provisioning_example.fetch("tenantid"),
  provisioning_example.dig("data", "tenant_id")
]
example_tenant_ids.each do |tenant_id|
  fail_contract("#{tenant_id.inspect} is not an opaque tenant identifier") unless tenant_pattern.match?(tenant_id)
end
fail_contract("examples must use one tenant identity") unless example_tenant_ids.uniq.length == 1

example_entity_id = register_example.fetch("legal_entity_id")
fail_contract("registration example references an unknown legal entity") unless entity_ids.include?(example_entity_id)
generated_tenant_id = provisioning_example.fetch("tenantid")
fail_contract("tenant_id must not equal legal_entity_id") if generated_tenant_id == example_entity_id
semantic_entity_tokens = entity_ids.map { |id| id.downcase.delete("-") }
if semantic_entity_tokens.any? { |token| generated_tenant_id.include?(token) }
  fail_contract("new tenant identifiers must not embed a legal-entity name")
end

example_products = register_example.fetch("requested_products") + [
  context_example.dig("request", "product_id"),
  context_example.dig("response", "product_id")
]
example_products.each do |product_id|
  fail_contract("#{product_id.inspect} is not a valid product identifier") unless product_pattern.match?(product_id)
end
fail_contract("context example request and response products differ") unless context_example.dig("request", "product_id") == context_example.dig("response", "product_id")
registered_entity = entities.find { |entity| entity.fetch("id") == example_entity_id }
confirmed_products = registered_entity.fetch("baobab_products", []).select { |entry| entry["confirmed"] }.map { |entry| entry.fetch("product") }
unregistered_products = example_products.uniq - confirmed_products
fail_contract("examples request products absent from the legal-entity registry: #{unregistered_products.join(', ')}") unless unregistered_products.empty?
fail_contract("registration response and provisioning event use different operation IDs") unless registration_response_example.fetch("operation_id") == provisioning_example.dig("data", "operation_id")
documented_registration_response = openapi.dig("paths", "/tenants", "post", "responses", "202", "content", "application/json", "examples", "controlPlaneMintedTenant", "value")
fail_contract("OpenAPI registration response example has drifted from its fixture") unless documented_registration_response == registration_response_example

nabhold = entities.find { |entity| entity.fetch("id") == "NABHOLD" }
fail_contract("NABHOLD registry entry is required") unless nabhold
fail_contract("NABHOLD must declare approved tenant intent") unless nabhold["baobab_tenant"] == true
nabhold_erp = nabhold.fetch("baobab_products").find { |entry| entry["product"] == "baobab-erp" }
fail_contract("NABHOLD must declare confirmed baobab-erp consumption") unless nabhold_erp&.fetch("confirmed") == true

puts "Governance contract validation passed"
