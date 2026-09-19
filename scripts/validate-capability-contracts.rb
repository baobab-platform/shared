# frozen_string_literal: true

require "json"
require "yaml"

ROOT = File.expand_path("..", __dir__)
CAPABILITY_ROOT = File.join(ROOT, "contracts/capability/v1")
VENDOR_TOKENS = %w[medusa idempiere payload haystack keycloak].freeze
CANONICAL_BINDING_MODES = %w[PRIMARY FALLBACK SHADOW MIGRATION DISABLED].freeze

def fail_contract(message)
  warn "capability contract validation failed: #{message}"
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

json_paths = Dir[File.join(CAPABILITY_ROOT, "**/*.json")].sort
yaml_paths = Dir[File.join(CAPABILITY_ROOT, "**/*.{yaml,yml}")].sort
fail_contract("capability package contains no JSON schemas") if json_paths.empty?

json_documents = json_paths.to_h { |path| [path, load_json(path)] }
yaml_documents = yaml_paths.to_h { |path| [path, load_yaml(path)] }

# 1. Every capability schema is JSON Schema 2020-12 with an immutable
#    contract URI under this package's own namespace.
schemas = json_documents.select { |_path, document| document.key?("$schema") }
schemas.each do |path, schema|
  fail_contract("#{path} must use JSON Schema 2020-12") unless schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
  fail_contract("#{path} must have an immutable contract URI") unless schema.fetch("$id", "").start_with?("https://contracts.nabhold.com/capability/v1/")
end

# 2. No capability_key or composition_key value actually committed
#    anywhere in this package (examples, registries) embeds a vendor
#    name. A JSON Schema pattern cannot itself blocklist specific vendor
#    words without hardcoding them into the grammar -- that would forbid
#    a legitimate future engine literally named "medusa" from ever
#    describing itself in a code comment -- so this check scans actual
#    committed key values by field name instead (ADR-BCP-002 SS5.1,
#    ADR-SHARED-007 SS9). provider_key is deliberately exempt: a
#    CapabilityProviderKey is REQUIRED to embed its engine name, e.g.
#    "baobab-trade.medusa" (provider.schema.json).
domain = json_documents.fetch(File.join(CAPABILITY_ROOT, "domain.schema.json"))
VENDOR_SCOPED_FIELDS = %w[capability_key composition_key].freeze

def walk_pairs(value, &block)
  case value
  when Hash
    value.each do |key, child|
      block.call(key, child)
      walk_pairs(child, &block)
    end
  when Array
    value.each { |child| walk_pairs(child, &block) }
  end
end

(json_documents.values + yaml_documents.values).each do |document|
  walk_pairs(document) do |field, value|
    next unless VENDOR_SCOPED_FIELDS.include?(field) && value.is_a?(String)

    VENDOR_TOKENS.each do |token|
      fail_contract("#{field} #{value.inspect} embeds vendor name #{token.inspect}") if value.split(/[.-]/).include?(token)
    end
  end
end

# 3. binding_mode is locked to exactly the five-value canonical set
#    (BCP-TS-ONBOARDING-001 CR-002, confirmed against nabhold/baobab-cp's
#    actual migrations during the Phase-0 audit). The superseded
#    seven-value set (SECONDARY, READ_ONLY, MIGRATION_SOURCE,
#    MIGRATION_TARGET) must never be reintroduced here.
binding_modes = domain.dig("$defs", "bindingMode", "enum")
fail_contract("bindingMode enum must equal the locked canonical set, got #{binding_modes.inspect}") unless binding_modes == CANONICAL_BINDING_MODES

# 4. namespace-registry.yaml's governed domain list and
#    domain.schema.json's capabilityDomain enum must agree exactly --
#    a domain accepted by one and rejected by the other is a defect.
namespace_registry = yaml_documents.fetch(File.join(CAPABILITY_ROOT, "namespace-registry.yaml"))
registry_domains = namespace_registry.fetch("domains").map { |entry| entry.fetch("key") }
schema_domains = domain.dig("$defs", "capabilityDomain", "enum")
fail_contract("namespace-registry.yaml and domain.schema.json capabilityDomain must declare identical domains") unless registry_domains.sort == schema_domains.sort

# 5. scope-specificity.yaml's weight derivation actually holds: each
#    tier's per-dimension weight must exceed the maximum possible
#    combined contribution of every lower tier, or the "no accidental
#    cross-tier tie" guarantee the file documents does not actually hold.
specificity = yaml_documents.fetch(File.join(CAPABILITY_ROOT, "scope-specificity.yaml"))
tiers = specificity.fetch("scoring_tiers").sort_by { |tier| tier.fetch("tier") }
running_max = 0
tiers.each do |tier|
  weight = tier.fetch("weight_per_dimension")
  dimension_count = tier.fetch("dimensions").length
  fail_contract("scope-specificity.yaml tier #{tier.fetch('tier')} weight #{weight} does not exceed the combined maximum (#{running_max}) of all lower tiers") if weight <= running_max
  running_max += weight * dimension_count
end

# 6. Every reason_code referenced by a capability example actually exists
#    in the capability_resolution_denial category of the shared registry
#    -- an example using an unregistered code would silently document a
#    contract that does not exist.
registry = load_yaml(File.join(ROOT, "contracts/authorization/v1/reason-code-registry.yaml"))
capability_reason_codes = registry.fetch("reason_codes")
                                   .select { |entry| entry["category"] == "capability_resolution_denial" }
                                   .map { |entry| entry.fetch("code") }
examples = Dir[File.join(CAPABILITY_ROOT, "examples/*.json")].sort
examples.each do |path|
  example = load_json(path)
  reason_code = example["reason_code"]
  next if reason_code.nil?

  fail_contract("#{path} uses reason_code #{reason_code.inspect}, which is not registered under capability_resolution_denial") unless capability_reason_codes.include?(reason_code)
end

# 7. Every event message declared in asyncapi.yaml uses the shared
#    com.nabhold.<context>.<...>.v<N> convention -- this package must not
#    reintroduce the baobab.* convention an earlier draft specification
#    proposed and the Phase-0 audit deliberately did not adopt (see the
#    Capability Platform tracking issue).
event_type_pattern = /\Acom\.nabhold\.[a-z0-9]+(?:[.-][a-z0-9]+)*\.v[1-9][0-9]*\z/
asyncapi = yaml_documents.fetch(File.join(CAPABILITY_ROOT, "asyncapi.yaml"))
asyncapi.fetch("components").fetch("messages").each do |message_key, message|
  name = message.fetch("name")
  fail_contract("asyncapi.yaml message #{message_key} has event name #{name.inspect}, which does not match the com.nabhold.* convention") unless event_type_pattern.match?(name)
end

puts "Capability contract validation passed"
