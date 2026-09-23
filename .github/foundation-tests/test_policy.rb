# frozen_string_literal: true

require "json"
require "yaml"

require "open3"
require "tmpdir"

GATES = %w[classify baseline reproducibility runtime environment security container].freeze
entry_workflow = YAML.safe_load_file(".github/workflows/foundation-repository-gates.yml", aliases: true)
RESULT_SCRIPT = entry_workflow.dig("jobs", "result", "steps", 0, "run")

# Executes the real Foundation / Result script; returns true when it passes.
def aggregate(results, profile: "full", exceptions: "{}", require_zero: "false")
  Dir.mktmpdir do |dir|
    needs = results.to_h { |name, result| [name.to_s, { "result" => result }] }
    env = {
      "RESULTS" => JSON.generate(needs),
      "PROFILE" => profile,
      "EXCEPTIONS" => exceptions,
      "REQUIRE_ZERO" => require_zero,
      "GITHUB_STEP_SUMMARY" => File.join(dir, "summary.md")
    }
    _, status = Open3.capture2e(env, "ruby", "-e", RESULT_SCRIPT, chdir: dir)
    status.success?
  end
end

def outcome(active, overrides = {})
  GATES.to_h { |gate| [gate, active.include?(gate) ? "success" : "skipped"] }.merge(overrides)
end

full = GATES
contract = %w[classify baseline reproducibility runtime environment]
security = %w[classify security]

cases = {
  "all successful" => [outcome(full), {}, true],
  "failure" => [outcome(full, "security" => "failure"), {}, false],
  "cancelled" => [outcome(full, "security" => "cancelled"), {}, false],
  "unexplained skip" => [outcome(full, "security" => "skipped"), {}, false],
  "missing/misconfigured" => [outcome(full, "security" => "action_required"), {}, false],
  "timed out" => [outcome(full, "runtime" => "timed_out"), {}, false],
  "neutral is not success" => [outcome(full, "security" => "neutral"), {}, false],
  "contract profile skips security" => [outcome(contract), { profile: "contract" }, true],
  "contract profile rejects skipped runtime" => [outcome(contract, "runtime" => "skipped"), { profile: "contract" }, false],
  "security profile rejects gate outside profile that ran" => [outcome(security, "container" => "success"), { profile: "security-pr" }, false],
  "deep profile skips contract gates" => [outcome(security), { profile: "security-deep" }, true],
  "unknown profile" => [outcome(full), { profile: "everything" }, false],
  "release rejects active exceptions" => [
    outcome(full),
    { exceptions: JSON.generate("sast" => { "approved_by" => "a", "expires" => "2099-01-01" }), require_zero: "true" },
    false
  ]
}

cases.each do |name, (results, options, expected)|
  actual = aggregate(results, **options)
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
  "stage name used before declaration" => ["FROM build\nFROM node:24 AS build\n", false],
  "global ARG default with tag" => ["ARG BASE=node:24-alpine\nFROM ${BASE}\n", true],
  "bare ARG reference" => ["ARG BASE=node:24\nFROM $BASE AS runtime\n", true],
  "ARG concatenated with tag" => ["ARG IMAGE=node\nFROM $IMAGE:24\n", true],
  "quoted ARG default" => ["ARG BASE=\"node:24\"\nARG OTHER='x'\nFROM ${BASE}\n", true],
  "ARG without default" => ["ARG BASE\nFROM ${BASE}\n", false],
  "ARG default without tag" => ["ARG BASE=node\nFROM ${BASE}\n", false],
  "ARG default using latest" => ["ARG BASE=node:latest\nFROM ${BASE}\n", false],
  "ARG after FROM is not global" => ["FROM node:24 AS first\nARG BASE=node:24\nFROM ${BASE}\n", false]
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

# Executes the real reproducibility step against Node manifests. A
# package.json without a packageManager field must not crash the check.
reproducibility_workflow = YAML.safe_load_file(".github/workflows/reusable-foundation-reproducibility.yml", aliases: true)
reproducibility_step = reproducibility_workflow["jobs"].values.flat_map { |job| job["steps"] }
                                                   .find { |step| step["name"].to_s.start_with?("Validate workspace reproducibility") }
abort "reproducibility step not found" unless reproducibility_step

node_manifests = {
  "no packageManager field" => [{ "name" => "app" }, true],
  "matching packageManager" => [{ "name" => "app", "packageManager" => "npm@10.9.7" }, true],
  "mismatched packageManager" => [{ "name" => "app", "packageManager" => "pnpm@11.24.0" }, false]
}

node_manifests.each do |name, (manifest, expected)|
  passed = Dir.mktmpdir do |dir|
    File.write(File.join(dir, "package.json"), JSON.generate(manifest))
    File.write(File.join(dir, "package-lock.json"), "{}")
    env = {
      "PYTHON" => "false", "NODE" => "true", "GO" => "false", "JAVA" => "false",
      "RUST" => "false", "INFRASTRUCTURE" => "false",
      "PACKAGE_MANAGERS" => JSON.generate("node" => "npm")
    }
    _, status = Open3.capture2e(env, "ruby", "-e", reproducibility_step["run"], chdir: dir)
    status.success?
  end
  abort "reproducibility #{name}: expected #{expected}, got #{passed}" unless passed == expected
end

puts "Reproducibility packageManager fixtures passed"
