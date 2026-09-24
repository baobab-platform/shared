# frozen_string_literal: true

require "json"
require "yaml"

require "open3"
require "tmpdir"
require "fileutils"

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

# SAST provider resolution (H2). Every combination of visibility and declared
# provider, plus the approval record, the sast exception and the deprecated
# advanced_security_enabled override.
require "date"
load "scripts/foundation/sast_policy.rb"

today = Date.new(2026, 9, 24)
ghas = { "approved_by" => "@platform-security", "reason" => "GHAS licensed for this repository", "expires" => "2027-03-31" }
sast_cases = {
  # [visibility, declaration, legacy flag, sast exception] => provider, or :error
  "public codeql" => [["public", { "sast_provider" => "codeql" }, false, false], "codeql"],
  "public fallback" => [["public", { "sast_provider" => "fallback" }, false, false], "fallback"],
  "public disabled with exception" => [["public", { "sast_provider" => "disabled" }, false, true], "disabled"],
  "public disabled without exception" => [["public", { "sast_provider" => "disabled" }, false, false], :error],
  "private codeql without ghas" => [["private", { "sast_provider" => "codeql" }, false, false], :error],
  "private codeql with ghas" => [["private", { "sast_provider" => "codeql", "ghas" => ghas }, false, false], "codeql"],
  "private codeql with expired ghas" => [["private", { "sast_provider" => "codeql", "ghas" => ghas.merge("expires" => "2026-01-01") }, false, false], :error],
  "private codeql with unsigned ghas" => [["private", { "sast_provider" => "codeql", "ghas" => ghas.merge("approved_by" => "someone") }, false, false], :error],
  "private fallback" => [["private", { "sast_provider" => "fallback" }, false, false], "fallback"],
  "private disabled with exception" => [["private", { "sast_provider" => "disabled" }, false, true], "disabled"],
  "private disabled without exception" => [["private", { "sast_provider" => "disabled" }, false, false], :error],
  "undeclared defaults to fallback" => [["public", nil, false, false], "fallback"],
  "legacy flag selects codeql when undeclared" => [["public", nil, true, false], "codeql"],
  "legacy flag cannot unlock private codeql" => [["private", nil, true, false], :error],
  "declaration beats legacy flag" => [["public", { "sast_provider" => "fallback" }, true, false], "fallback"],
  "unknown visibility is private" => [["", { "sast_provider" => "codeql" }, false, false], :error],
  "unknown provider" => [["public", { "sast_provider" => "semgrep" }, false, false], :error]
}
sast_cases.each do |name, ((visibility, declaration, legacy, exception), expected)|
  result = FoundationSast.resolve(visibility: visibility, declaration: declaration,
                                  legacy_advanced_security: legacy, sast_exception: exception, today: today)
  actual = result.error ? :error : result.provider
  abort "sast #{name}: expected #{expected.inspect}, got #{actual.inspect} (#{result.error})" unless actual == expected
end
abort "ghas approval not reported" unless FoundationSast.resolve(visibility: "private", declaration: { "sast_provider" => "fallback", "ghas" => ghas }, today: today).ghas_approved
disagreement = FoundationSast.resolve(visibility: "public", declaration: { "sast_provider" => "fallback" }, legacy_advanced_security: true, today: today)
abort "legacy disagreement not warned" unless disagreement.warnings.any? { |message| message.include?("the declaration wins") }

# The real classifier step, run against sample contracts with this checkout
# standing in for the pinned Foundation revision.
classifier = YAML.safe_load_file(".github/workflows/reusable-foundation-classify.yml", aliases: true)
resolve_step = classifier.dig("jobs", "classify", "steps").find { |step| step["id"] == "resolve" }
abort "classifier resolve step not found" unless resolve_step
base_contract = {
  "schema_version" => 1, "repository" => { "lifecycle" => "active" }, "capabilities" => ["node"],
  "environment" => { "baobab_dev" => { "required" => false } }, "artifacts" => { "container" => false }
}
classifier_cases = {
  "public, declares codeql" => ["public", { "security" => { "sast_provider" => "codeql" } }, "codeql"],
  "private, declares fallback" => ["private", { "security" => { "sast_provider" => "fallback" } }, "fallback"],
  "private, codeql without approval" => ["private", { "security" => { "sast_provider" => "codeql" } }, :error],
  "unknown security field" => ["public", { "security" => { "provider" => "codeql" } }, :error],
  "nothing declared" => ["public", {}, "fallback"]
}
classifier_cases.each do |name, (visibility, extra, expected)|
  actual = Dir.mktmpdir do |dir|
    FileUtils.mkdir_p(File.join(dir, ".baobab"))
    File.write(File.join(dir, ".baobab/repository.yaml"), YAML.dump(base_contract.merge(extra)))
    File.symlink(Dir.pwd, File.join(dir, ".foundation"))
    output = File.join(dir, "output")
    env = { "VISIBILITY" => visibility, "ADVANCED_SECURITY_ENABLED" => "false",
            "GITHUB_OUTPUT" => output, "GITHUB_STEP_SUMMARY" => File.join(dir, "summary") }
    _, status = Open3.capture2e(env, "ruby", "-e", resolve_step["run"], chdir: dir)
    next :error unless status.success?

    File.readlines(output).find { |line| line.start_with?("sast_provider=") }.to_s.strip.delete_prefix("sast_provider=")
  end
  abort "classifier #{name}: expected #{expected.inspect}, got #{actual.inspect}" unless actual == expected
end

puts "SAST provider resolution fixtures passed"
