# frozen_string_literal: true

require "json"
require "yaml"
require "pathname"
require "uri"

ROOT = File.expand_path("..", __dir__)

def fail_contract(message)
  warn "identity-events contract validation failed: #{message}"
  exit 1
end

def load_json(path)
  JSON.parse(File.read(File.join(ROOT, path)))
end

def load_yaml(path)
  YAML.safe_load_file(File.join(ROOT, path), aliases: false)
end

def relative(path)
  Pathname.new(path).relative_path_from(Pathname.new(ROOT))
end

# 1. Every $ref in every contracts/**/*.schema.json must resolve to a file that
#    actually exists on disk. This is a generic check across the whole contracts
#    tree, not just identity-events: it's exactly the class of bug that shipped
#    undetected here (identity-created/-disabled/membership-revoked all $ref'd
#    a ../../common/event-envelope.schema.json that has never existed).
# Resolve absolute references only through exact schema IDs present in this
# checkout. No network retrieval and no arbitrary URL-to-path conversion.
schema_ids = {}
Dir.glob(File.join(ROOT, "contracts/**/*.schema.json")).each do |path|
  id = JSON.parse(File.read(path))["$id"]
  next unless id
  fail_contract("duplicate schema $id") if schema_ids.key?(id)
  schema_ids[id] = path
end

collect_refs = lambda do |node, refs|
  case node
  when Hash
    refs << node["$ref"] if node["$ref"].is_a?(String)
    node.each_value { |value| collect_refs.call(value, refs) }
  when Array
    node.each { |value| collect_refs.call(value, refs) }
  end
end

Dir.glob(File.join(ROOT, "contracts/**/*.schema.json")).sort.each do |schema_path|
  schema = JSON.parse(File.read(schema_path))
  refs = []
  collect_refs.call(schema, refs)

  refs.each do |ref|
    file_part = ref.split("#").first
    next if file_part.nil? || file_part.empty? # in-document fragment only

    uri = URI.parse(file_part)
    resolved = if uri.absolute?
                 schema_ids[file_part]
               else
                 File.expand_path(File.join(File.dirname(schema_path), file_part))
               end
    next if resolved && File.file?(resolved)

    fail_contract("#{relative(schema_path)}: $ref #{ref.inspect} does not resolve to a file on disk")
  end
end

# 2. identity-events payload schemas are standalone `data` schemas: composition
#    with the envelope happens in asyncapi.yaml, not inside the payload schema.
event_schema_files = %w[identity-created.schema.json identity-disabled.schema.json identity-suspended.schema.json identity-reactivated.schema.json membership-revoked.schema.json entitlement-revoked.schema.json credential-compromised.schema.json session-revoked.schema.json workload-revoked.schema.json]
event_schema_files.each do |file|
  schema = load_json("contracts/identity-events/v1/#{file}")
  fail_contract("#{file} must not wrap the envelope internally (composition happens in asyncapi.yaml)") if schema.key?("allOf")
  fail_contract("#{file} must set additionalProperties: false") unless schema["additionalProperties"] == false
  fail_contract("#{file} must declare a properties object") unless schema["properties"].is_a?(Hash)
end

# 3. asyncapi.yaml wires every message through the canonical envelope, and each
#    message's `data` field points at one of the schema files above.
asyncapi_path = "contracts/identity-events/v1/asyncapi.yaml"
asyncapi = load_yaml(asyncapi_path)
messages = asyncapi.dig("components", "messages") || {}
fail_contract("identity-events asyncapi.yaml declares no messages") if messages.empty?

canonical_envelope_ref = "../../events/v1/envelope.schema.json"
messages.each do |name, message|
  layers = message.dig("payload", "allOf") || []
  envelope_layer = layers.find { |layer| layer.is_a?(Hash) && layer.key?("$ref") }
  fail_contract("#{name} does not reference the canonical envelope") unless envelope_layer && envelope_layer["$ref"] == canonical_envelope_ref

  data_ref = layers.filter_map { |layer| layer.dig("properties", "data", "$ref") }.first
  fail_contract("#{name} does not wire a data schema") unless data_ref

  resolved = File.expand_path(File.join(ROOT, File.dirname(asyncapi_path), data_ref))
  fail_contract("#{name}'s data $ref #{data_ref.inspect} does not resolve to a file on disk") unless File.exist?(resolved)
end

# 4. Every example validates against the envelope's required/unknown fields and
#    against its own event's data schema.
envelope = load_json("contracts/events/v1/envelope.schema.json")
required_event_fields = envelope.fetch("required")
event_properties = envelope.fetch("properties")

Dir.glob(File.join(ROOT, "contracts/identity-events/v1/examples/*.json")).sort.each do |example_path|
  example = JSON.parse(File.read(example_path))

  missing = required_event_fields - example.keys
  unknown = example.keys - event_properties.keys
  fail_contract("#{relative(example_path)} misses envelope fields: #{missing.join(', ')}") unless missing.empty?
  fail_contract("#{relative(example_path)} has fields unknown to the envelope: #{unknown.join(', ')}") unless unknown.empty?

  if example.fetch("baobabscope") == "tenant"
    fail_contract("#{relative(example_path)} is tenant-scoped but has no tenantid") unless example.key?("tenantid")
  else
    fail_contract("#{relative(example_path)} is platform-scoped but carries a tenantid") if example.key?("tenantid")
  end

  data_schema_file = File.basename(URI.parse(example.fetch("dataschema")).path)
  data_schema = load_json("contracts/identity-events/v1/#{data_schema_file}")

  data = example.fetch("data")
  data_missing = data_schema.fetch("required", []) - data.keys
  data_unknown = data.keys - data_schema.fetch("properties", {}).keys
  fail_contract("#{relative(example_path)} data misses: #{data_missing.join(', ')}") unless data_missing.empty?
  fail_contract("#{relative(example_path)} data has unknown fields: #{data_unknown.join(', ')}") unless data_unknown.empty?
end

puts "Identity-events contract validation passed"
