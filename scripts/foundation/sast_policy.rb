# frozen_string_literal: true

require "date"

# Resolves which SAST provider a repository gets, from its own declaration
# (security.sast_provider in .baobab/repository.yaml) and the repository's
# visibility. Loaded by the Foundation classifier from the pinned Foundation
# checkout, and exercised directly by .github/foundation-tests/test_policy.rb.
#
#   codeql   — CodeQL runs. A private repository must carry an approved,
#              unexpired security.ghas record (GitHub Advanced Security).
#   fallback — CodeQL does not run; the result is SAST / Fallback and the
#              portable Trivy scans remain the evidence. Default when nothing
#              is declared.
#   disabled — no SAST at all. Only allowed with an approved exceptions.sast.
#
# The deprecated advanced_security_enabled input still selects codeql for a
# repository that declares nothing, and warns when it disagrees with a
# declaration. It never lets a private repository reach CodeQL without the
# approval record.
module FoundationSast
  PROVIDERS = %w[codeql fallback disabled].freeze
  Resolution = Struct.new(:provider, :ghas_approved, :warnings, :error, keyword_init: true)

  module_function

  def resolve(visibility:, declaration: nil, legacy_advanced_security: false, sast_exception: false, today: Date.today)
    warnings = []
    security = declaration || {}
    declared = security["sast_provider"]
    ghas = security["ghas"]

    return failure("security.sast_provider must be one of #{PROVIDERS.join(', ')}") if declared && !PROVIDERS.include?(declared)

    ghas_approved = false
    if ghas
      problem = ghas_problem(ghas, today)
      return failure("security.ghas #{problem}") if problem

      ghas_approved = true
    end

    provider =
      if declared
        if legacy_advanced_security && declared != "codeql"
          warnings << "advanced_security_enabled=true disagrees with security.sast_provider=#{declared}; the declaration wins"
        end
        declared
      else
        legacy_advanced_security ? "codeql" : "fallback"
      end
    if legacy_advanced_security
      warnings << "advanced_security_enabled is deprecated; declare security.sast_provider in .baobab/repository.yaml"
    end

    # Anything other than an explicit "public" is treated as private, so an
    # unknown visibility can never unlock CodeQL without approval.
    private_repository = visibility.to_s.strip != "public"
    if provider == "codeql" && private_repository && !ghas_approved
      return failure("CodeQL on a private repository requires an approved security.ghas record (approved_by, reason, expires)")
    end
    if provider == "disabled" && !sast_exception
      return failure("security.sast_provider: disabled requires an approved exceptions.sast record")
    end

    Resolution.new(provider: provider, ghas_approved: ghas_approved, warnings: warnings, error: nil)
  end

  def ghas_problem(ghas, today)
    return "must be an object" unless ghas.is_a?(Hash)

    unknown = ghas.keys - %w[approved_by reason expires]
    return "contains unknown fields: #{unknown.join(', ')}" unless unknown.empty?
    return "requires an @handle approver" unless ghas["approved_by"].to_s.match?(/\A@[A-Za-z0-9-]+\z/)
    return "reason must be at least 12 characters" unless ghas["reason"].to_s.length >= 12

    expiry = ghas["expires"].is_a?(Date) ? ghas["expires"] : Date.iso8601(ghas["expires"].to_s)
    return "expired on #{expiry}" if expiry < today

    nil
  rescue Date::Error
    "has an invalid expiry"
  end

  def failure(message)
    Resolution.new(provider: nil, ghas_approved: false, warnings: [], error: message)
  end
end
