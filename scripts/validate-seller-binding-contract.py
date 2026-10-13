#!/usr/bin/env python3
"""P0-04B-02 closed command admission and unassigned vocabulary."""
import copy
import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker
root = Path(__file__).resolve().parents[1]
schema = json.loads((root / 'contracts/commerce/v1/seller-binding.schema.json').read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator({'$defs': schema['$defs'], '$ref': '#/$defs/AuthorizeBindingRequest'}, format_checker=FormatChecker())
value = {'scope': {'cartId':'cart-test','tenantId':'tn_test01','organisationId':'00000000-0000-4000-8000-000000000001','responsibleLegalEntityId':'le_test','marketCode':'ZA','currencyCode':'ZAR','salesChannelId':'channel-test','regionId':'region-test'}, 'command_digest': 'a'*64}
validator.validate(value)
for key in value['scope']:
    bad = copy.deepcopy(value)
    del bad['scope'][key]
    assert not validator.is_valid(bad), key
for key in ['actor','context_id','token_id','legal_activity','decision_id']:
    assert not validator.is_valid({**value, key: 'forged'}), key
scopes = yaml.safe_load((root/'contracts/authorization/v1/scope-registry.yaml').read_text())['scopes']
permissions = yaml.safe_load((root/'contracts/administration/v1/permission-registry.yaml').read_text())['permissions']
profiles = (root/'contracts/administration/v1/profile-registry.yaml').read_text()
workloads = (root/'contracts/identity/v1/workload-registry.yaml').read_text()
for op in ['propose','approve','activate','revoke']:
    name = 'trade-binding:'+op
    s = next(x for x in scopes if x['name']==name)
    assert s['audience']==['baobab-control-plane'] and s['allowed_actors']==['human']
    assert not s['grants_authority'] and name not in workloads
    p = next(x for x in permissions if x['key']=='organisation.trade-binding.'+op)
    assert p['scope_levels']==['ORGANISATION'] and not p['delegable']
    assert p['key'] not in profiles
print('Seller binding schema, negative fixtures and nonassignment passed')
