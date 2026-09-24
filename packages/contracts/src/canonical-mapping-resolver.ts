// Baobab Canonical Mapping Resolution Algorithm
// Implements §23-24 of the Canonical Mapping Model specification.
//
// This module provides a deterministic, auditable mapping resolution implementation
// for resolving canonical entities to their external representations in scoped contexts.

/**
 * Mapping resolution request parameters (§23, step 1-4)
 */
export interface ResolutionInput {
  canonical_entity_id: string;
  target_capability?: string;
  target_system?: string;
  context: ResolutionContext;
  effective_timestamp?: Date;
}

/**
 * Runtime context determining which representations are applicable (§17)
 */
export interface ResolutionContext {
  tenant_id: string;
  legal_entity_id?: string;
  market_id?: string;
  country?: string;
  estate_id?: string;
  digital_property_id?: string;
  channel_id?: string;
  currency?: string;
  locale?: string;
  environment?: string;
  [key: string]: string | undefined;
}

/**
 * Mapping record structure matching canonical-mapping.schema.json
 */
export interface Mapping {
  mapping_id: string;
  tenant_id: string;
  legal_entity_id?: string;
  mapping_type: string;
  canonical_entity_id?: string;
  external_reference_id?: string;
  target_canonical_entity_id?: string;
  scope_id: string;
  direction: 'BIDIRECTIONAL' | 'CANONICAL_TO_EXTERNAL' | 'EXTERNAL_TO_CANONICAL' | 'SOURCE_TO_TARGET';
  cardinality: 'ONE_TO_ONE' | 'ONE_TO_MANY' | 'MANY_TO_ONE' | 'MANY_TO_MANY';
  authority: string;
  confidence: 'CONFIRMED' | 'PROBABLE' | 'CANDIDATE' | 'REJECTED';
  resolution_priority?: number;
  status: 'DRAFT' | 'VALIDATED' | 'ACTIVE' | 'DEPRECATED' | 'SUSPENDED' | 'MIGRATING' | 'QUARANTINED' | 'RETIRED';
  effective_from: Date;
  effective_to?: Date;
  revision: number;
}

/**
 * Mapping scope defining applicability constraints (§10)
 */
export interface MappingScope {
  scope_id: string;
  tenant_id: string;
  legal_entity_id?: string;
  market_id?: string;
  country?: string;
  estate_id?: string;
  digital_property_id?: string;
  channel_id?: string;
  currency?: string;
  locale?: string;
  environment?: string;
  engine_id?: string;
  engine_instance_id?: string;
  deployment_region?: string;
  include_countries?: string[];
  exclude_countries?: string[];
}

/**
 * Resolution result with provenance (§23, step 10)
 */
export interface ResolutionResult {
  mapping_id: string;
  canonical_entity_id: string;
  external_reference_id?: string;
  scope_id: string;
  status: string;
  resolution_reason: 'active_binding' | 'scope_matched' | 'temporal_valid' | 'priority_applied' | 'default_mapping' | 'fallback_applied';
  effective_timestamp: Date;
  mapping_version: number;
  resolved_at: Date;
  cached: boolean;
}

/**
 * Resolution failure details
 */
export interface ResolutionFailure {
  reason: 'not_found' | 'ambiguous' | 'invalid_context' | 'invalid_temporal' | 'no_candidate' | 'scope_mismatch' | 'confidence_insufficient';
  message: string;
  context?: string;
}

/**
 * Baobab Canonical Mapping Resolver
 *
 * Implements the deterministic resolution algorithm from §23-24:
 * 1. validate Context
 * 2. identify candidate mappings
 * 3. remove mappings outside temporal validity
 * 4. remove inactive mappings
 * 5. remove mappings whose scope does not match Context
 * 6. evaluate engine/capability compatibility
 * 7. rank by scope specificity
 * 8. apply explicit resolution priority
 * 9. reject ambiguous authoritative results
 * 10. return resolved mapping plus resolution provenance
 */
export class CanonicalMappingResolver {
  private mappingStore: Map<string, Mapping> = new Map();
  private scopeStore: Map<string, MappingScope> = new Map();

  /**
   * Register a mapping in the resolver's runtime cache
   */
  registerMapping(mapping: Mapping): void {
    this.mappingStore.set(mapping.mapping_id, mapping);
  }

  /**
   * Register a scope constraint
   */
  registerScope(scope: MappingScope): void {
    this.scopeStore.set(scope.scope_id, scope);
  }

  /**
   * Resolve a canonical entity to an external representation in context.
   *
   * Returns ResolutionResult on success, throws ResolutionFailure on failure.
   * Failures are preferable to silent incorrect resolution (§24).
   */
  resolve(input: ResolutionInput): ResolutionResult | ResolutionFailure {
    const timestamp = input.effective_timestamp || new Date();

    // Step 1: Validate Context
    const contextError = this.validateContext(input.context);
    if (contextError) {
      return contextError;
    }

    // Step 2: Identify candidate mappings
    const candidates = this.identifyCandidates(input.canonical_entity_id);
    if (candidates.length === 0) {
      return {
        reason: 'no_candidate',
        message: `No mappings found for canonical entity ${input.canonical_entity_id}`,
        context: JSON.stringify(input.context),
      };
    }

    // Step 3: Remove mappings outside temporal validity
    const temporallyValid = this.filterTemporalValidity(candidates, timestamp);
    if (temporallyValid.length === 0) {
      return {
        reason: 'invalid_temporal',
        message: `No mappings valid at ${timestamp.toISOString()}`,
      };
    }

    // Step 4: Remove inactive mappings
    const active = this.filterByStatus(temporallyValid, ['ACTIVE', 'DEPRECATED']);
    if (active.length === 0) {
      return {
        reason: 'no_candidate',
        message: 'No active or deprecated mappings found after temporal filtering',
      };
    }

    // Step 5: Remove mappings whose scope does not match Context
    const scopeMatched = this.filterByScopeMatch(active, input.context);
    if (scopeMatched.length === 0) {
      return {
        reason: 'scope_mismatch',
        message: 'No mappings match the provided context scope',
        context: JSON.stringify(input.context),
      };
    }

    // Step 6: Evaluate engine/capability compatibility (future: when binding data exists)
    // For now, pass through; engine-instance and capability constraints will be added
    // when CapabilityBinding data becomes available.

    // Step 7: Rank by scope specificity (§10.4)
    const ranked = this.rankBySpecificity(scopeMatched, input.context);

    // Step 8: Apply explicit resolution priority
    const prioritized = this.applyResolutionPriority(ranked);

    // Step 9: Reject ambiguous authoritative results (§23, §24)
    const result = this.selectAuthoritative(prioritized);
    if ('reason' in result) {
      return result; // Ambiguity detected
    }

    // Step 10: Return resolved mapping plus resolution provenance
    return {
      mapping_id: result.mapping_id,
      canonical_entity_id: result.canonical_entity_id!,
      external_reference_id: result.external_reference_id,
      scope_id: result.scope_id,
      status: result.status,
      resolution_reason: 'active_binding',
      effective_timestamp: timestamp,
      mapping_version: result.revision,
      resolved_at: new Date(),
      cached: false,
    };
  }

  /**
   * Validate that the Context is well-formed and contains minimum required fields
   */
  private validateContext(context: ResolutionContext): ResolutionFailure | null {
    if (!context.tenant_id) {
      return {
        reason: 'invalid_context',
        message: 'Context must specify tenant_id',
      };
    }
    return null;
  }

  /**
   * Step 2: Identify all mappings for the canonical entity (regardless of scope/status)
   */
  private identifyCandidates(canonicalEntityId: string): Mapping[] {
    return Array.from(this.mappingStore.values()).filter(
      (m) => m.canonical_entity_id === canonicalEntityId
    );
  }

  /**
   * Step 3: Filter by temporal validity [effective_from, effective_to)
   */
  private filterTemporalValidity(mappings: Mapping[], timestamp: Date): Mapping[] {
    return mappings.filter((m) => {
      const fromOk = m.effective_from <= timestamp;
      const toOk = m.effective_to === undefined || m.effective_to > timestamp;
      return fromOk && toOk;
    });
  }

  /**
   * Step 4: Filter by lifecycle status
   */
  private filterByStatus(mappings: Mapping[], allowedStatuses: string[]): Mapping[] {
    return mappings.filter((m) => allowedStatuses.includes(m.status));
  }

  /**
   * Step 5: Filter mappings whose scope matches the provided Context
   *
   * A mapping matches Context when every explicitly declared scope dimension
   * is compatible with that Context (§10.3).
   */
  private filterByScopeMatch(mappings: Mapping[], context: ResolutionContext): Mapping[] {
    return mappings.filter((mapping) => {
      const scope = this.scopeStore.get(mapping.scope_id);
      if (!scope) {
        // Scope not found; conservatively exclude
        return false;
      }
      return this.scopeMatches(scope, context);
    });
  }

  /**
   * Determine if a scope matches a context
   */
  private scopeMatches(scope: MappingScope, context: ResolutionContext): boolean {
    // Check each explicitly set scope dimension against context
    if (scope.tenant_id && scope.tenant_id !== context.tenant_id) {
      return false;
    }
    if (scope.legal_entity_id && scope.legal_entity_id !== context.legal_entity_id) {
      return false;
    }
    if (scope.market_id && scope.market_id !== context.market_id) {
      return false;
    }
    if (scope.country && scope.country !== context.country) {
      // Check country inclusions/exclusions
      if (scope.exclude_countries?.includes(scope.country)) {
        return false;
      }
      if (scope.include_countries && !scope.include_countries.includes(scope.country)) {
        return false;
      }
      if (scope.country !== context.country) {
        return false;
      }
    }
    if (scope.estate_id && scope.estate_id !== context.estate_id) {
      return false;
    }
    if (scope.digital_property_id && scope.digital_property_id !== context.digital_property_id) {
      return false;
    }
    if (scope.channel_id && scope.channel_id !== context.channel_id) {
      return false;
    }
    if (scope.currency && scope.currency !== context.currency) {
      return false;
    }
    if (scope.locale && scope.locale !== context.locale) {
      return false;
    }
    if (scope.environment && scope.environment !== context.environment) {
      return false;
    }
    if (scope.engine_id && scope.engine_id !== context.target_system) {
      return false;
    }
    // All checked dimensions match
    return true;
  }

  /**
   * Step 7: Rank by scope specificity (§10.4)
   *
   * More constrained scopes outrank broader compatible scopes.
   * Specificity is measured by the number of explicitly set dimensions.
   */
  private rankBySpecificity(mappings: Mapping[], context: ResolutionContext): Mapping[] {
    return mappings.sort((a, b) => {
      const scopeA = this.scopeStore.get(a.scope_id);
      const scopeB = this.scopeStore.get(b.scope_id);

      const countA = this.countScopeDimensions(scopeA);
      const countB = this.countScopeDimensions(scopeB);

      // Higher specificity (more dimensions) sorts first
      return countB - countA;
    });
  }

  /**
   * Count the number of explicitly set scope dimensions
   */
  private countScopeDimensions(scope: MappingScope | undefined): number {
    if (!scope) return 0;

    let count = 0;
    const keys: (keyof MappingScope)[] = [
      'tenant_id',
      'legal_entity_id',
      'market_id',
      'country',
      'estate_id',
      'digital_property_id',
      'channel_id',
      'currency',
      'locale',
      'environment',
      'engine_id',
      'engine_instance_id',
      'deployment_region',
    ];

    keys.forEach((key) => {
      if (scope[key] !== undefined && scope[key] !== null) {
        count++;
      }
    });

    return count;
  }

  /**
   * Step 8: Apply explicit resolution priority (§9.7)
   *
   * Specificity normally outranks manual priority, but we apply priority
   * as a secondary sort within equivalent specificity levels.
   */
  private applyResolutionPriority(mappings: Mapping[]): Mapping[] {
    return mappings.sort((a, b) => {
      const priorityA = a.resolution_priority || 500;
      const priorityB = b.resolution_priority || 500;
      return priorityB - priorityA; // Higher priority sorts first
    });
  }

  /**
   * Step 9: Select the authoritative result and reject ambiguity
   *
   * If multiple equally specific, equally prioritized authoritative mappings exist,
   * return failure rather than random selection (§23, §24).
   */
  private selectAuthoritative(
    mappings: Mapping[]
  ): Mapping | ResolutionFailure {
    if (mappings.length === 0) {
      return {
        reason: 'no_candidate',
        message: 'No candidate mappings after filtering',
      };
    }

    if (mappings.length === 1) {
      return mappings[0];
    }

    // Check if top candidates have equal specificity and priority
    const first = mappings[0];
    const second = mappings[1];

    const firstScope = this.scopeStore.get(first.scope_id);
    const secondScope = this.scopeStore.get(second.scope_id);

    const firstSpecificity = this.countScopeDimensions(firstScope);
    const secondSpecificity = this.countScopeDimensions(secondScope);

    const firstPriority = first.resolution_priority || 500;
    const secondPriority = second.resolution_priority || 500;

    if (firstSpecificity === secondSpecificity && firstPriority === secondPriority) {
      return {
        reason: 'ambiguous',
        message: `Ambiguous equally specific authoritative mappings: ${first.mapping_id} vs ${second.mapping_id}. Resolution is non-deterministic.`,
      };
    }

    return first;
  }
}

/**
 * Factory function to create a resolver with pre-loaded mappings and scopes.
 *
 * In a real implementation, these would be loaded from a database.
 */
export function createResolver(
  mappings: Mapping[],
  scopes: MappingScope[]
): CanonicalMappingResolver {
  const resolver = new CanonicalMappingResolver();
  mappings.forEach((m) => resolver.registerMapping(m));
  scopes.forEach((s) => resolver.registerScope(s));
  return resolver;
}
