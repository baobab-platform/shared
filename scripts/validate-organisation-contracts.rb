#!/usr/bin/env ruby
# frozen_string_literal: true

# Target path: baobab-platform/shared/scripts/validate-organisation-contracts.rb
# ADR-BCP-018 — structural governance checks for organisation/v1 contracts.

require "json"
require "yaml"

ROOT = File.expand_path("..", __dir__)
ORG = File.join(ROOT, "contracts", "organisation", "v1")
failures = []

def fail_contract(msg, failures)
  failures << msg
  warn "FAIL: #{msg}"
end

%w[domain.schema.json relationship.schema.json platform.schema.json mapping.schema.json].each do |name|
  path = File.join(ORG, name)
  unless File.file?(path)
    fail_contract("missing #{name}", failures)
    next
  end
  begin
    data = JSON.parse(File.read(path))
  rescue JSON::ParserError => e
    fail_contract("#{name} is not valid JSON: #{e.message}", failures)
    next
  end
  id = data["$id"].to_s
  unless id.start_with?("https://contracts.baobab-platform.com/organisation/v1/")
    fail_contract("#{name} $id must use https://contracts.baobab-platform.com/organisation/v1/ namespace (got #{id.inspect})", failures)
  end
  defs = data["$defs"]
  fail_contract("#{name} must define $defs", failures) unless defs.is_a?(Hash) && !defs.empty?
end

rel = JSON.parse(File.read(File.join(ORG, "relationship.schema.json")))
vocab = rel.dig("$defs", "corporateRelationshipType", "enum") || []
required_vocab = %w[OWNS CONTROLS BRANCH_OF AFFILIATE_OF JOINT_VENTURE_WITH SUCCESSOR_OF]
required_vocab.each do |v|
  fail_contract("corporateRelationshipType missing #{v}", failures) unless vocab.include?(v)
end
%w[PARENT_OF SUBSIDIARY_OF SISTER_OF RELATED_TO JOINT_VENTURE].each do |forbidden|
  fail_contract("corporateRelationshipType must not include redundant/non-ADR value #{forbidden}", failures) if vocab.include?(forbidden)
end

group = rel.dig("$defs", "CorporateGroup") || {}
group_req = group["required"] || []
fail_contract("CorporateGroup.root_organisation_id must not be required", failures) if group_req.include?("root_organisation_id")

membership = rel.dig("$defs", "CorporateGroupMembership") || {}
mem_req = membership["required"] || []
%w[basis_relationship_ids derived_at derivation_version].each do |f|
  fail_contract("CorporateGroupMembership must require #{f}", failures) unless mem_req.include?(f)
end

corp = rel.dig("$defs", "CorporateRelationship") || {}
corp_req = corp["required"] || []
fail_contract("CorporateRelationship must require source_authority", failures) unless corp_req.include?("source_authority")

plat = JSON.parse(File.read(File.join(ORG, "platform.schema.json")))
pr = plat.dig("$defs", "PlatformRelationship") || {}
pr_req = pr["required"] || []
%w[platform_id organisation_id source_authority].each do |f|
  fail_contract("PlatformRelationship must require #{f}", failures) unless pr_req.include?(f)
end

map = JSON.parse(File.read(File.join(ORG, "mapping.schema.json")))
tom = map.dig("$defs", "TenantOrganisationMapping") || {}
tlem = map.dig("$defs", "TenantLegalEntityMapping") || {}
fail_contract("TenantOrganisationMapping must require mapping_role and provenance", failures) unless (tom["required"] || []).include?("mapping_role") && (tom["required"] || []).include?("provenance")
fail_contract("TenantLegalEntityMapping must require mapping_role and provenance", failures) unless (tlem["required"] || []).include?("mapping_role") && (tlem["required"] || []).include?("provenance")

lock = YAML.load_file(File.join(ROOT, "contracts.lock.yaml"))
org_entry = (lock["contracts"] || []).find { |c| c["domain"] == "organisation" && c["version"] == "v1" }
fail_contract("contracts.lock.yaml must register organisation v1", failures) if org_entry.nil?

if failures.empty?
  puts "OK: organisation/v1 contracts"
  exit 0
else
  warn "#{failures.length} organisation contract failure(s)"
  exit 1
end
