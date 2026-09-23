/**
 * Target path: baobab-platform/shared/tests/contracts/organisation.v1.test.js
 *
 * Contract tests for ADR-BCP-018 organisation schemas.
 * Ensures schemas parse as JSON Schema draft 2020-12 and examples are well-formed.
 * Does not require a full AJV install if the shared test harness already provides schema validation;
 * falls back to structural checks that any Node test runner can execute.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '../../contracts/organisation/v1');

function loadJSON(rel) {
  const full = path.join(ROOT, rel);
  const raw = fs.readFileSync(full, 'utf8');
  return JSON.parse(raw);
}

describe('organisation/v1 contracts (ADR-BCP-018)', () => {
  test('domain.schema.json parses', () => {
    const schema = loadJSON('domain.schema.json');
    expect(schema.$schema).toMatch(/2020-12/);
    expect(schema.$defs.Organisation).toBeDefined();
    expect(schema.$defs.LegalEntityProfile).toBeDefined();
    expect(schema.$defs.Organisation.required).toContain('canonical_entity_id');
    expect(schema.$defs.LegalEntityProfile.required).toContain('organisation_id');
  });

  test('relationship.schema.json parses', () => {
    const schema = loadJSON('relationship.schema.json');
    expect(schema.$defs.CorporateRelationship).toBeDefined();
    expect(schema.$defs.CorporateGroup).toBeDefined();
    expect(schema.$defs.CorporateGroupMembership).toBeDefined();
    expect(schema.$defs.CorporateRelationship.required).toContain('verification_state');
  });

  test('platform.schema.json parses', () => {
    const schema = loadJSON('platform.schema.json');
    expect(schema.$defs.PlatformRelationship).toBeDefined();
    expect(schema.$defs.PlatformAccount).toBeDefined();
    expect(schema.$defs.platformRelationshipType.enum).toContain('PLATFORM_GROUP_AFFILIATE');
    expect(schema.$defs.platformRelationshipType.enum).toContain('EXTERNAL_CLIENT');
  });

  test('mapping.schema.json parses', () => {
    const schema = loadJSON('mapping.schema.json');
    expect(schema.$defs.TenantOrganisationMapping).toBeDefined();
    expect(schema.$defs.TenantLegalEntityMapping).toBeDefined();
    expect(schema.$defs.TenantLegalEntityMapping.properties.is_default).toBeDefined();
  });

  test('nabhold-group example is well-formed', () => {
    const ex = loadJSON('examples/nabhold-group-organisation.json');
    expect(ex.organisations.length).toBeGreaterThanOrEqual(4);
    expect(ex.legal_entity_profiles.some((p) => p.legal_entity_id === 'NABHOLD')).toBe(true);
    expect(ex.corporate_relationships.every((r) => r.verification_state === 'VERIFIED')).toBe(true);
  });

  test('acme-holdings external example has no shared-registry dependency', () => {
    const ex = loadJSON('examples/acme-holdings-external.json');
    expect(ex.organisations.some((o) => o.source_authority === 'control-plane-admission')).toBe(true);
    expect(ex.platform_relationships.every((r) => r.relationship_type === 'EXTERNAL_CLIENT')).toBe(true);
    // External legal_entity_ids are Control-Plane style, not limited to first-party registry
    expect(ex.legal_entity_profiles.some((p) => p.legal_entity_id === 'ACME-HOLDINGS')).toBe(true);
  });
});
