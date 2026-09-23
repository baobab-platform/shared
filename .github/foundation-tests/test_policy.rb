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
  "missing/misconfigured" => [{ classify: "success", security: "action_required" }, false],
  "timed out" => [{ classify: "success", runtime: "timed_out" }, false],
  "neutral is not success" => [{ classify: "success", security: "neutral" }, false]
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
%w[classify baseline reproducibility runtime environment security container].each do |gate|
  abort "result does not depend on #{gate}" unless entry.include?(gate)
end

%w[
  reusable-foundation-dependency-review.yml
  reusable-foundation-sast.yml
  reusable-foundation-runtime.yml
  reusable-foundation-security.yml
  reusable-foundation-container.yml
].each do |workflow|
  path = File.join(".github/workflows", workflow)
  abort "missing decomposed workflow #{path}" unless File.file?(path)
end

puts "Foundation policy fixtures passed"

# Container base-image policy: run the real step against sample Dockerfiles.
require "open3"
require "tmpdir"

container_workflow = YAML.safe_load_file(".github/workflows/reusable-foundation-container.yml", aliases: true)
policy_step = container_workflow.dig("jobs", "container", "steps").find do |step|
  step["name"] == "Validate artifact coordinates and Dockerfile policy"
end
abort "container policy step not found" unless policy_step

dockerfiles = {
  "stage reference" => ["FROM node:24-alpine AS dependencies\nFROM dependencies AS build\nFROM node:24-alpine\n", true],
  "platform flag with tag" => ["FROM --platform=$BUILDPLATFORM golang:1.27 AS build\nFROM build\n", true],
  "lowercase stage reference" => ["from golang:1.27 as build\nfrom build\n", true],
  "scratch" => ["FROM scratch\n", true],
  "digest" => ["FROM alpine@sha256:#{'a' * 64}\n", true],
  "untagged base" => ["FROM node\n", false],
  "untagged base behind platform flag" => ["FROM --platform=linux/amd64 node AS build\n", false],
  "latest" => ["FROM node:latest\n", false],
  "latest behind platform flag" => ["FROM --platform=linux/amd64 node:latest\n", false],
  "stage name used before declaration" => ["FROM build\nFROM node:24 AS build\n", false]
}

dockerfiles.each do |name, (content, expected)|
  passed = Dir.mktmpdir do |dir|
    File.write(File.join(dir, "Dockerfile"), content)
    env = { "DOCKERFILE" => "Dockerfile", "BUILD_CONTEXT" => "." }
    _, status = Open3.capture2e(env, "bash", "-c", policy_step["run"], chdir: dir)
    status.success?
  end
  abort "container policy #{name}: expected #{expected}, got #{passed}" unless passed == expected
end

puts "Container base-image policy fixtures passed"
