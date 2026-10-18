#!/usr/bin/env python3
"""Offline MP2-A structural validation; does not approve runtime eligibility."""
import json
import re
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / 'contracts/identity/v1'
SCHEMAS = ('runtime-capability.schema.json', 'provider-runtime-profile.schema.json')
BASE = 'https://contracts.baobab-platform.com/'


def validator():
    resources = []
    for path in (ROOT / 'contracts').rglob('*.schema.json'):
        schema = json.loads(path.read_text())
        resource = Resource.from_contents(schema)
        if '$id' in schema:
            resources.append((schema['$id'], resource))
        resources.append((BASE + path.relative_to(ROOT / 'contracts').as_posix(), resource))
    registry = Registry().with_resources(resources)
    schema = json.loads((IDENTITY / SCHEMAS[1]).read_text())
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def validate_profile(profile):
    # Do not include user-supplied values in diagnostics.
    errors = ['schema:' + '/'.join(map(str, e.absolute_path)) + ':' + str(e.validator)
              for e in validator().iter_errors(profile)]
    if errors:
        return errors
    observations = profile['capability_observations']
    facets = [item['capability'] for item in observations]
    if len(set(facets)) != len(facets):
        errors.append('duplicate runtime capability')
    def timestamp(value):
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})', value):
            raise ValueError('timestamp requires RFC3339 timezone')
        return datetime.fromisoformat(value.upper().replace('Z', '+00:00'))

    try:
        published = timestamp(profile['published_at'])
        for item in observations:
            if 'evidence' in item:
                timestamp(item['evidence']['observed_at'])
                timestamp(item['evidence']['expires_at'])
    except ValueError:
        return errors + ['invalid timestamp']
    for item in observations:
        if item['verification_status'] != 'VERIFIED':
            continue
        evidence = item['evidence']
        if evidence['artifact_digest'] != profile['artifact_digest']:
            errors.append('evidence artifact mismatch')
        observed = timestamp(evidence['observed_at'])
        expires = timestamp(evidence['expires_at'])
        if not observed <= published < expires:
            errors.append('evidence not valid at publication')
    return errors


def validate_authority_policy():
    # Transport scopes never confer canonical authority or silently extend the
    # federation-only permission. Keep the initial allocation explicitly empty.
    policy = yaml.safe_load((IDENTITY / 'runtime-authority-policy.yaml').read_text())
    assert policy['permission'] == 'security.identity-runtime.view'
    assert policy['transport'] == {
        'scope': 'identity-runtime:read', 'actors': ['workload'],
        'audiences': ['baobab-control-plane']}
    assert policy['facets'] == {
        'HUMAN_AUTHENTICATION': 'identity.authentication.perform',
        'WORKLOAD_TOKEN_ISSUANCE': 'identity.workload-token.issue',
        'OAUTH_AUTHORIZATION_SERVER': 'identity.workload-token.issue'}
    native = policy['composition_requirements']['native_handoff']
    assert native == {
        'human_capability': 'identity.authentication.perform',
        'human_facet': 'HUMAN_AUTHENTICATION',
        'issuer_capability': 'identity.workload-token.issue',
        'issuer_facets': ['WORKLOAD_TOKEN_ISSUANCE', 'OAUTH_AUTHORIZATION_SERVER'],
        'exact_same_issuer_provider_instance_artifact_and_profile_revision': True,
        'exact_same_organisation_estate_security_domain_and_caller': True,
        'repeat_checks_before_provider_acceptance': True,
        'grants_human_resource_audience': False}
    scopes = yaml.safe_load((ROOT / 'contracts/authorization/v1/scope-registry.yaml').read_text())['scopes']
    scope = next(x for x in scopes if x['name'] == policy['transport']['scope'])
    assert scope['audience'] == policy['transport']['audiences']
    assert scope['allowed_actors'] == ['workload'] and scope['grants_authority'] is False
    permissions = yaml.safe_load((ROOT / 'contracts/administration/v1/permission-registry.yaml').read_text())['permissions']
    permission = next(x for x in permissions if x['key'] == policy['permission'])
    assert permission['read_only'] is True and permission['delegable'] is False
    assert permission['risk_class'] == 'LOW'
    assert permission['scope_levels'] == ['PLATFORM', 'ORGANISATION', 'DIGITAL_ESTATE']
    assert policy['references']['configuration'] == {
        'system_namespace': 'baobab_iam', 'engine_id': 'baobab-iam',
        'native_entity_type': 'identity_runtime_configuration'}
    assert policy['requirements']['creates_authority'] is False
    assert policy['requirements']['reference_existence_is_approval'] is False
    registry = yaml.safe_load((IDENTITY / 'workload-registry.yaml').read_text())
    # The registry's clients stay unchanged: definition is not activation.
    for workload in registry['workloads'].values():
        assert policy['transport']['scope'] not in workload.get('allowed_scopes', [])
    profiles = yaml.safe_load((ROOT / 'contracts/administration/v1/profile-registry.yaml').read_text())
    for profile in profiles['profiles']:
        assert policy['permission'] not in profile.get('permissions', [])


def main():
    validate_authority_policy()
    for name in SCHEMAS:
        schema = json.loads((IDENTITY / name).read_text())
        Draft202012Validator.check_schema(schema)
        assert schema['$id'] == BASE + 'identity/v1/' + name
    lock = yaml.safe_load((ROOT / 'contracts.lock.yaml').read_text())
    entry = next(x for x in lock['contracts'] if x['domain'] == 'identity' and x['version'] == 'v1')
    assert all(name in entry['schemas'] for name in SCHEMAS)
    examples = sorted((IDENTITY / 'examples').glob('runtime-profile-*.json'))
    assert len(examples) == 3
    for path in examples:
        profile = json.loads(path.read_text())
        errors = validate_profile(profile)
        assert not errors, f'{path.name}: {errors}'
        assert all(x['verification_status'] == 'UNVERIFIED' for x in profile['capability_observations'])
    print('Identity runtime contracts: schemas, lock and 3 synthetic profiles valid')


if __name__ == '__main__':
    main()
