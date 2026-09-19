// Baobab Context Resolution Flow
// Implements §17 (Context), §22 (Context Resolution Flow) of the Canonical Mapping Model.
//
// The context resolution flow is the canonical request-resolution sequence:
// Authenticate → Tenant → Property → Estate → Legal Entity → Market → Country/Locale/Currency →
// Authorize → Construct → Capability → Binding → Mappings → Engine

import { ResolutionContext } from './canonical-mapping-resolver';

/**
 * Trust boundary for context provenance tracking (§17.3)
 */
export type ContextSource = 'identity_token' | 'hostname' | 'binding' | 'inherited' | 'user_selection' | 'default';

/**
 * Context field with provenance metadata (§17.4)
 */
export interface ContextField<T> {
  value: T;
  source: ContextSource;
  constrained_by?: string[];
  verified_at?: Date;
}

/**
 * Full context with provenance for every field (§17.4)
 */
export interface ContextWithProvenance {
  // Identity
  tenant_id: ContextField<string>;
  legal_entity_id?: ContextField<string>;
  organisation_id?: ContextField<string>;
  business_unit_id?: ContextField<string>;

  // Geography & Market
  operating_region_id?: ContextField<string>;
  market_id?: ContextField<string>;
  country_code?: ContextField<string>;

  // Digital Presence
  estate_id?: ContextField<string>;
  digital_property_id?: ContextField<string>;
  channel_id?: ContextField<string>;

  // Locale & Currency (§31-32)
  currency?: ContextField<string>;
  accounting_currency?: ContextField<string>;
  locale?: ContextField<string>;
  timezone?: ContextField<string>;

  // Actor & Tracing
  actor_id?: ContextField<string>;
  subject_id?: ContextField<string>;
  request_id: ContextField<string>;
  correlation_id?: ContextField<string>;
  causation_id?: ContextField<string>;
  trace_id?: ContextField<string>;

  // Operational
  environment: ContextField<string>;
  contract_version?: ContextField<string>;
}

/**
 * Resolved context for downstream consumption (§17.2)
 */
export interface ResolvedContext extends ResolutionContext {
  timezone?: string;
  accounting_currency?: string;
  // Additional fields from ContextWithProvenance values
}

/**
 * Initial request evidence (§22: Incoming Request → Authenticate)
 */
export interface ContextResolutionRequest {
  // From authentication (§22: step 1-2)
  authenticated_principal: {
    subject: string;
    issuer: string;
    token_type: 'identity' | 'workload' | 'delegated';
  };

  // From HTTP request
  request_hostname?: string;
  request_path?: string;
  user_agent?: string;
  x_forwarded_for?: string;

  // Optional explicit hints (untrusted; must be validated)
  product_id?: string;
  preferred_market?: string;
  preferred_locale?: string;
  preferred_currency?: string;

  // Tracing
  correlation_id?: string;
  causation_id?: string;
  trace_id?: string;
}

/**
 * Registry data needed for context resolution
 */
export interface ContextRegistry {
  // Property → Estate → Tenant → Legal Entity mappings
  property_bindings: Map<string, PropertyBinding>;
  estate_registry: Map<string, EstateRecord>;
  tenant_registry: Map<string, TenantRecord>;
  entity_registry: Map<string, EntityRecord>;
  market_registry: Map<string, MarketRecord>;

  // Default/fallback values
  default_environment: 'local' | 'development' | 'staging' | 'production';
  default_timezone: string;
  default_locale: string;
}

/**
 * Digital property to estate binding (§12.3)
 */
export interface PropertyBinding {
  digital_property_id: string;
  domain: string;
  subdomain?: string;
  estate_id: string;
  market_id?: string;
  tenant_id: string;
}

/**
 * Digital estate record
 */
export interface EstateRecord {
  estate_id: string;
  tenant_id: string;
  legal_entity_id: string;
  brand_id?: string;
  default_market_id?: string;
  default_locale: string;
  default_currency: string;
  markets: string[];
}

/**
 * Tenant record
 */
export interface TenantRecord {
  tenant_id: string;
  legal_entity_id: string;
  name: string;
  status: 'active' | 'suspended' | 'provisioning' | 'decommissioning';
}

/**
 * Legal entity record
 */
export interface EntityRecord {
  legal_entity_id: string;
  name: string;
  country?: string;
  status: 'active' | 'suspended' | 'retired';
}

/**
 * Market record
 */
export interface MarketRecord {
  market_id: string;
  default_country?: string;
  countries: string[];
  default_currency: string;
  allowed_currencies: string[];
  default_locale: string;
  supported_locales: string[];
  timezone: string;
}

/**
 * Baobab Context Resolver
 *
 * Implements the canonical request-resolution sequence from §22:
 * Incoming Request → Authenticate → Tenant → Property → Estate → Legal Entity →
 * Market → Country/Locale/Currency → Authorise → Construct → Capability → Binding → Mappings
 */
export class ContextResolver {
  constructor(private registry: ContextRegistry) {}

  /**
   * Main entry point: resolve full context from request evidence
   *
   * Returns ResolvedContext on success; throws error on unresolvable state.
   */
  async resolve(request: ContextResolutionRequest): Promise<ResolvedContext> {
    // §22: Step 1 - Authenticate
    const principal = this.validateAuthentication(request.authenticated_principal);

    // §22: Step 2 - Resolve Tenant (from identity token or explicitly)
    const tenant = await this.resolveTenant(principal, request);

    // §22: Step 3 - Resolve Digital Property
    const property = await this.resolveProperty(request, tenant);

    // §22: Step 4 - Resolve Digital Estate
    const estate = await this.resolveEstate(property, tenant);

    // §22: Step 5 - Resolve Legal Entity
    const legalEntity = await this.resolveLegalEntity(estate, tenant);

    // §22: Step 6 - Resolve Market
    const market = await this.resolveMarket(estate, request.preferred_market);

    // §22: Step 7 - Resolve Country / Locale / Currency
    const locale = this.resolveLocale(market, request.preferred_locale);
    const currency = this.resolveCurrency(market, request.preferred_currency);
    const country = this.resolveCountry(market);

    // §22: Step 8 - Validate Authorisation
    const authorized = this.validateAuthorization(principal, tenant, estate, market);
    if (!authorized) {
      throw new Error(`Principal ${principal.subject} not authorized for tenant ${tenant.tenant_id}`);
    }

    // §22: Step 9 - Construct Context
    const context = this.constructContext({
      tenant_id: tenant.tenant_id,
      legal_entity_id: legalEntity.legal_entity_id,
      estate_id: estate.estate_id,
      digital_property_id: property?.digital_property_id,
      market_id: market?.market_id,
      country_code: country,
      locale,
      currency,
      accounting_currency: currency, // TODO: distinguish accounting currency
      timezone: market?.timezone || this.registry.default_timezone,
      environment: this.registry.default_environment,
      actor_id: principal.subject,
      request_id: this.generateRequestId(request),
      correlation_id: request.correlation_id,
      causation_id: request.causation_id,
      trace_id: request.trace_id,
    });

    return context;
  }

  /**
   * §22 Step 1: Validate authentication
   */
  private validateAuthentication(
    principal: ContextResolutionRequest['authenticated_principal']
  ): { subject: string; issuer: string; token_type: string } {
    if (!principal.subject || !principal.issuer) {
      throw new Error('Authentication failed: missing subject or issuer');
    }
    return principal;
  }

  /**
   * §22 Step 2: Resolve Tenant
   *
   * Tenant can come from:
   * - authenticated identity token claims
   * - product_id → tenant binding
   * - digital property binding → estate → tenant
   */
  private async resolveTenant(
    principal: { subject: string; issuer: string; token_type: string },
    request: ContextResolutionRequest
  ): Promise<TenantRecord> {
    // First, try product_id
    if (request.product_id) {
      // In real implementation, look up product → tenant binding
      // For now, placeholder
    }

    // Then try property binding
    if (request.request_hostname) {
      const property = this.findPropertyByHostname(request.request_hostname);
      if (property) {
        const estate = this.registry.estate_registry.get(property.estate_id);
        if (estate) {
          return this.registry.tenant_registry.get(estate.tenant_id)!;
        }
      }
    }

    throw new Error(`Unable to resolve tenant for principal ${principal.subject}`);
  }

  /**
   * §22 Step 3: Resolve Digital Property
   *
   * From hostname or digital_property_id claim
   */
  private async resolveProperty(
    request: ContextResolutionRequest,
    tenant: TenantRecord
  ): Promise<PropertyBinding | undefined> {
    if (request.request_hostname) {
      return this.findPropertyByHostname(request.request_hostname);
    }
    return undefined;
  }

  /**
   * §22 Step 4: Resolve Digital Estate
   *
   * From property binding or estate_id
   */
  private async resolveEstate(
    property: PropertyBinding | undefined,
    tenant: TenantRecord
  ): Promise<EstateRecord> {
    if (property) {
      const estate = this.registry.estate_registry.get(property.estate_id);
      if (estate && estate.tenant_id === tenant.tenant_id) {
        return estate;
      }
    }

    // Fallback: use tenant's default estate (if exists)
    for (const estate of this.registry.estate_registry.values()) {
      if (estate.tenant_id === tenant.tenant_id) {
        return estate;
      }
    }

    throw new Error(`No estate found for tenant ${tenant.tenant_id}`);
  }

  /**
   * §22 Step 5: Resolve Legal Entity
   *
   * From estate or tenant record
   */
  private async resolveLegalEntity(
    estate: EstateRecord,
    tenant: TenantRecord
  ): Promise<EntityRecord> {
    const entity = this.registry.entity_registry.get(estate.legal_entity_id);
    if (entity && entity.status === 'active') {
      return entity;
    }

    throw new Error(`Legal entity ${estate.legal_entity_id} not found or inactive`);
  }

  /**
   * §22 Step 6: Resolve Market
   *
   * From estate default, property binding, or explicit preference
   */
  private async resolveMarket(
    estate: EstateRecord,
    preferredMarketId?: string
  ): Promise<MarketRecord | undefined> {
    // Try preferred market if provided
    if (preferredMarketId && estate.markets.includes(preferredMarketId)) {
      return this.registry.market_registry.get(preferredMarketId);
    }

    // Fall back to estate default
    if (estate.default_market_id) {
      return this.registry.market_registry.get(estate.default_market_id);
    }

    // If estate has markets, use first
    if (estate.markets.length > 0) {
      return this.registry.market_registry.get(estate.markets[0]);
    }

    return undefined;
  }

  /**
   * §22 Step 7a: Resolve Locale
   *
   * From market, preference, or defaults. Use BCP 47 format (§32).
   */
  private resolveLocale(market: MarketRecord | undefined, preference?: string): string {
    if (preference && market?.supported_locales.includes(preference)) {
      return preference;
    }

    if (market) {
      return market.default_locale;
    }

    return this.registry.default_locale;
  }

  /**
   * §22 Step 7b: Resolve Currency
   *
   * Must be constrained by market allowed_currencies (§31).
   */
  private resolveCurrency(market: MarketRecord | undefined, preference?: string): string {
    if (!market) {
      return 'USD'; // Fallback
    }

    // Validate preference against market constraints
    if (preference && market.allowed_currencies.includes(preference)) {
      return preference;
    }

    // User selection can be overridden by market policy
    return market.default_currency;
  }

  /**
   * §22 Step 7c: Resolve Country
   *
   * Derive from market or request context
   */
  private resolveCountry(market: MarketRecord | undefined): string | undefined {
    if (market) {
      return market.default_country || market.countries[0];
    }
    return undefined;
  }

  /**
   * §22 Step 8: Validate Authorisation
   *
   * Verify principal has access to tenant/estate/market combination
   */
  private validateAuthorization(
    principal: { subject: string; issuer: string; token_type: string },
    tenant: TenantRecord,
    estate: EstateRecord,
    market: MarketRecord | undefined
  ): boolean {
    // Placeholder: in real implementation, check RBAC/ABAC policies
    // For now, accept any valid combination
    return tenant.status === 'active';
  }

  /**
   * §22 Step 9: Construct Context
   *
   * Build final resolved context with all required fields
   */
  private constructContext(params: any): ResolvedContext {
    return {
      tenant_id: params.tenant_id,
      legal_entity_id: params.legal_entity_id,
      estate_id: params.estate_id,
      digital_property_id: params.digital_property_id,
      market_id: params.market_id,
      country: params.country_code,
      currency: params.currency,
      accounting_currency: params.accounting_currency,
      locale: params.locale,
      environment: params.environment,
      timezone: params.timezone,
    };
  }

  /**
   * Helper: find property binding by hostname
   */
  private findPropertyByHostname(hostname: string): PropertyBinding | undefined {
    for (const binding of this.registry.property_bindings.values()) {
      if (binding.domain === hostname || (binding.subdomain && `${binding.subdomain}.${binding.domain}` === hostname)) {
        return binding;
      }
    }
    return undefined;
  }

  /**
   * Generate request ID if not provided
   */
  private generateRequestId(request: ContextResolutionRequest): string {
    return request.correlation_id || `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

/**
 * Factory to create a context resolver with test data
 */
export function createContextResolver(registry: ContextRegistry): ContextResolver {
  return new ContextResolver(registry);
}
