#!/usr/bin/env python3
"""MP2-B publication invariants; no authentication, activation or mapping approval."""
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / 'contracts/identity/v1'
BASE = 'https://contracts.baobab-platform.com/identity/v1/'
SCHEMAS = ('federation-domain.schema.json', 'federation-trust.schema.json',
           'external-principal.schema.json', 'federated-assurance.schema.json')


def registry():
    resources = []
    for path in (ROOT / 'contracts').rglob('*.schema.json'):
        schema = json.loads(path.read_text())
        if '$id' in schema:
            resources.append((schema['$id'], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def timestamp(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})', value):
        raise ValueError('timestamp')
    return datetime.fromisoformat(value.upper().replace('Z', '+00:00'))


def validate_bundle(bundle):
    errors = []
    if not isinstance(bundle, dict) or set(bundle) != {'trust', 'external_principal', 'assurance'}:
        return ['bundle fields']
    reg = registry()
    for key, name in zip(('trust', 'external_principal', 'assurance'), SCHEMAS[1:]):
        schema = json.loads((IDENTITY / name).read_text())
        errors.extend('schema:' + key + ':' + '/'.join(map(str, e.absolute_path)) + ':' + str(e.validator)
                      for e in Draft202012Validator(schema, registry=reg, format_checker=FormatChecker()).iter_errors(bundle[key]))
    if errors:
        return errors
    t, p, a = (bundle[k] for k in ('trust', 'external_principal', 'assurance'))
    for field in ('protocol', 'issuer', 'subject', 'trust_id', 'provider_id', 'engine_instance_id', 'authentication_event_id'):
        if p[field] != a[field]:
            errors.append('assurance provenance mismatch:' + field)
    if p['trust_id'] != t['id'] or p['protocol'] != t['protocol'] or p['issuer'] != t['upstream_issuer']:
        errors.append('principal trust mismatch')
    for field in ('provider_id', 'engine_instance_id'):
        if p[field] != t['provider_binding'][field]:
            errors.append('provider binding mismatch:' + field)
    if a['assurance_policy_reference'] != t['assurance_policy_reference']:
        errors.append('assurance policy mismatch')
    issuer = urlsplit(t['upstream_issuer'])
    if re.search(r'\s', t['upstream_issuer']):
        errors.append('issuer whitespace')
    if t['protocol'] == 'OIDC' and (issuer.scheme != 'https' or not issuer.hostname or issuer.username is not None or issuer.password is not None or issuer.query or issuer.fragment):
        errors.append('OIDC issuer requires exact HTTPS issuer without credentials/query/fragment')
    # The subject remains an opaque exact identifier, even if it resembles an email.
    # Email linking is prohibited by mapping_basis and authoritative lookup, not heuristics.
    try:
        def dates(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k.endswith('_at'):
                        timestamp(v)
                    elif isinstance(v, (dict, list)):
                        dates(v)
            elif isinstance(node, list):
                for item in node:
                    dates(item)
        dates(bundle)
        created, updated = timestamp(t['created_at']), timestamp(t['updated_at'])
        if created > updated:
            errors.append('trust timestamp order')
        for key in ('activated_at', 'revoked_at'):
            if key in t and not created <= timestamp(t[key]) <= updated:
                errors.append('trust lifecycle timestamp order')
        if 'activated_at' in t and 'revoked_at' in t and timestamp(t['activated_at']) > timestamp(t['revoked_at']):
            errors.append('revocation precedes activation')
        observed, expires = timestamp(p['observed_at']), timestamp(p['expires_at'])
        evaluated, assurance_expiry = timestamp(a['evaluated_at']), timestamp(a['expires_at'])
        if not observed <= evaluated < assurance_expiry <= expires:
            errors.append('event assurance timestamp bounds')
        if p['resolution']['status'] == 'RESOLVED' and not observed <= timestamp(p['resolution']['resolved_at']) < expires:
            errors.append('resolution outside event lifetime')
        evidence = a['upstream_evidence']['oidc' if t['protocol'] == 'OIDC' else 'saml']
        authenticated = timestamp(evidence['authenticated_at'])
        if authenticated > observed:
            errors.append('authentication after observation')
        if t['protocol'] == 'OIDC':
            if evidence['issuer'] != p['issuer'] or evidence['actor_type'] != 'human':
                errors.append('OIDC upstream provenance mismatch')
            if 'step_up_at' in evidence and not authenticated <= timestamp(evidence['step_up_at']) <= evaluated:
                errors.append('invalid step-up time')
        elif timestamp(evidence['session_expires_at']) < assurance_expiry:
            errors.append('assurance outlives SAML session')
    except (ValueError, TypeError):
        errors.append('invalid timestamp')
    return errors


def trust_allows_new_authentication(trust):
    """Necessary lifecycle predicate only; never sufficient authentication approval."""
    return trust.get('status') == 'ACTIVE'


def validate_transition(previous, current):
    """Contract transition checks; approval/evidence lookup is a consumer duty."""
    policy = yaml.safe_load((IDENTITY / 'federation-lifecycle.yaml').read_text())
    if previous['id'] != current['id'] or current['revision'] <= previous['revision']:
        return ['trust identity or revision rollback']
    if any(previous[field] != current[field] for field in ('protocol', 'upstream_issuer')):
        return ['issuer/protocol change requires a new trust']
    if timestamp(current['updated_at']) < timestamp(previous['updated_at']):
        return ['trust update rollback']
    before, after = previous['status'], current['status']
    if before == 'REVOKED' or (before != after and after not in policy['transitions'].get(before, [])):
        return ['prohibited trust lifecycle transition']
    return []


def main():
    for name in SCHEMAS:
        schema = json.loads((IDENTITY / name).read_text())
        Draft202012Validator.check_schema(schema)
        assert schema['$id'] == BASE + name
    lock = yaml.safe_load((ROOT / 'contracts.lock.yaml').read_text())
    entry = next(x for x in lock['contracts'] if x['domain'] == 'identity' and x['version'] == 'v1')
    assert all(entry['schemas'].count(name) == 1 for name in SCHEMAS)
    assert entry['schemas'].count('federation-lifecycle.yaml') == 1
    policy = yaml.safe_load((IDENTITY / 'federation-lifecycle.yaml').read_text())
    statuses = json.loads((IDENTITY / SCHEMAS[0]).read_text())['$defs']['trustStatus']['enum']
    assert set(policy['transitions']) == set(statuses)
    assert all(set(targets) <= set(statuses) for targets in policy['transitions'].values())
    assert policy['initial_status'] == 'REQUESTED'
    assert policy['new_authentication_statuses'] == ['ACTIVE']
    assert policy['terminal_statuses'] == ['REVOKED'] and policy['transitions']['REVOKED'] == []
    examples = sorted((IDENTITY / 'examples').glob('federation-*.json'))
    assert len(examples) == 2
    for path in examples:
        bundle = json.loads(path.read_text())
        errors = validate_bundle(bundle)
        assert not errors, f'{path.name}: {errors}'
        assert bundle['trust']['status'] == 'VERIFYING'
        assert bundle['external_principal']['resolution']['status'] == 'UNRESOLVED'
        assert bundle['assurance']['mapping_status'] == 'UNKNOWN'
        assert not trust_allows_new_authentication(bundle['trust'])
    print('Federation contracts: schemas, lock and synthetic OIDC/SAML bundles valid')


if __name__ == '__main__':
    main()
