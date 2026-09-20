# frozen_string_literal: true

require "json"
require "yaml"

def aggregate(results)
  failed = results.select { |_, result| result != "success" }
  [failed.empty?, failed.keys]
end

cases = {
  "all successful" => [{ classify: "success", baseline: "success", security: "success" }, true],
  "failure" => [{ classify: "success", security: "failure" }, false],
  "cancelled" => [{ classify: "success", security: "cancelled" }, false],
  "unexplained skip" => [{ classify: "success", security: "skipped" }, false],
  "missing/misconfigured" => [{ classify: "success", security: "action_required" }, false]
}

cases.each do |name, (results, expected)|
  actual, = aggregate(results)
  abort "#{name}: expected #{expected}, got #{actual}" unless actual == expected
end

schema = JSON.parse(File.read(".baobab/repository.schema.json"))
capabilities = schema.dig("properties", "capabilities", "items", "enum")
abort "Rust capability is not represented in the schema" unless capabilities.include?("rust")
container_variants = schema.dig("properties", "artifacts", "properties", "container", "oneOf")
object_variant = container_variants.find { |variant| variant["type"] == "object" }
abort "container runtime semantics are absent" unless object_variant.dig("properties", "runtime", "type") == "boolean"

entry = File.read(".github/workflows/foundation-repository-gates.yml")
abort "aggregator still accepts arbitrary skipped gates" if entry.include?("%w[success skipped]")
%w[classify baseline reproducibility environment security container].each do |gate|
  abort "result does not depend on #{gate}" unless entry.include?(gate)
end

%w[
  reusable-foundation-dependency-review.yml
  reusable-foundation-sast.yml
  reusable-foundation-security.yml
  reusable-foundation-container.yml
].each do |workflow|
  path = File.join(".github/workflows", workflow)
  abort "missing decomposed workflow #{path}" unless File.file?(path)
end

puts "Foundation policy fixtures passed"
