# frozen_string_literal: true

require "json"
require "yaml"

ROOT = File.expand_path("..", __dir__)
TRADE_ROOT = File.join(ROOT, "contracts/trade/v1")

def fail_contract(message)
  warn "trade contract validation failed: #{message}"
  exit 1
end

json_paths = Dir[File.join(TRADE_ROOT, "*.json")].sort
fail_contract("trade contract package is empty") if json_paths.empty?

documents = json_paths.to_h { |path| [File.basename(path), JSON.parse(File.read(path))] }
documents.each do |name, schema|
  fail_contract("#{name} must use JSON Schema 2020-12") unless schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
  expected_id = "https://contracts.baobab-platform.com/trade/v1/#{name}"
  fail_contract("#{name} has a mutable or incorrect contract URI") unless schema["$id"] == expected_id
end

domain = documents.fetch("domain.schema.json")
buyer_context = domain.dig("$defs", "buyerContext", "required")
required_context = %w[principal_id tenant_id legal_entity_id digital_estate_id market_id buyer_organisation_id]
fail_contract("buyer context must keep every authority boundary distinct") unless buyer_context == required_context

capabilities = YAML.safe_load_file(File.join(TRADE_ROOT, "capabilities.yaml"), aliases: false).fetch("capabilities")
openapi = YAML.safe_load_file(File.join(TRADE_ROOT, "openapi.yaml"), aliases: false)
expected = %w[commerce.cart.manage commercial.rfq.manage commercial.quotation.manage]
actual = capabilities.map { |entry| entry.fetch("capability_key") }
fail_contract("capability registry does not expose the complete v1 boundary") unless actual == expected
capabilities.each do |capability|
  fail_contract("#{capability.fetch('capability_key')} must be owned by baobab-trade") unless capability["owner"] == "baobab-trade"
  fail_contract("#{capability.fetch('capability_key')} must never be PUBLIC") if capability["data_classification"] == "PUBLIC"
end

quotation = documents.fetch("quotation.schema.json")
quotation_statuses = quotation.dig("properties", "status", "enum")
fail_contract("quotation lifecycle must distinguish acceptance, expiry and order conversion") unless %w[ACCEPTED EXPIRED CONVERTED].all? { |status| quotation_statuses.include?(status) }
fail_contract("quotation must carry an optimistic version") unless quotation.fetch("required").include?("version")

rfq_create = documents.fetch("rfq-create.schema.json")
server_owned_rfq_fields = %w[rfq_id status version created_at updated_at]
leaked_fields = server_owned_rfq_fields & rfq_create.fetch("properties").keys
fail_contract("RFQ create command exposes server-owned fields: #{leaked_fields.join(', ')}") unless leaked_fields.empty?
fail_contract("RFQ create command must require buyer context and lines") unless rfq_create.fetch("required") == %w[context lines]

quick_order = documents.fetch("quick-order.schema.json")
limit = quick_order.dig("$defs", "request", "properties", "lines", "maxItems")
fail_contract("quick order must have a bounded line count") unless limit.is_a?(Integer) && limit.positive? && limit <= 100

mutating_operations = [
  openapi.dig("paths", "/rfqs", "post"),
  openapi.dig("paths", "/quotations/{quotation_id}/accept", "post")
]
mutating_operations.each do |operation|
  parameter_refs = operation.fetch("parameters").map { |parameter| parameter["$ref"] }
  fail_contract("every commercial command must require Idempotency-Key") unless parameter_refs.include?("#/components/parameters/IdempotencyKey")
end
unless openapi.dig("paths", "/buyer-context", "post", "responses", "200", "headers", "Cache-Control", "schema", "const") == "private, no-store"
  fail_contract("authorized buyer context must declare private, no-store caching")
end

puts "Trade B2B buyer-context, purchasing, RFQ and quotation contracts passed"
