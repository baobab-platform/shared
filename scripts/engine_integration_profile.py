#!/usr/bin/env python3
"""DEV-14 unprivileged profile validation/planning. Never issues authority."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import stat
import sys

from jsonschema import Draft202012Validator
import capability_catalogue as catalogue
import development_environment as environment

ROOT=Path(__file__).resolve().parents[1]
SCHEMA_PATH='development/v1/engine-integration-profile.schema.json'
CRITERIA=frozenset('ENG-ONB-0'+str(i) for i in range(1,10))


def require(ok, code):
    if not ok:raise ValueError(code)


def read_profile(path):
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=65536,'PROFILE_FILE_REFUSED')
    return json.loads(path.read_text(),object_pairs_hook=environment.unique)


def owned_file(root, relative):
    path=root/relative
    require(path.resolve().is_relative_to(root.resolve()),'OWNER_PATH_ESCAPE')
    current=root
    for part in Path(relative).parts:
        current=current/part
        require(not current.is_symlink(),'OWNER_SYMLINK_REFUSED')
    require(stat.S_ISREG(path.stat().st_mode) and path.stat().st_size<=262144,'OWNER_FILE_REFUSED')
    return path


def validate(profile, *, shared_root=ROOT, engine_root=None):
    """Schema and semantic checks; ownership/current authority still belong to owners."""
    schema=json.loads((shared_root/'contracts'/SCHEMA_PATH).read_text())
    Draft202012Validator(schema).validate(profile)
    engine=profile['subject_engine']
    require(profile['provider_key'].split('.')[0]==engine,'PROVIDER_OWNER_MISMATCH')
    require(profile['enterprise_seed']!=profile['neighbour_seed'],'DISTINCT_TENANTS_REQUIRED')
    enterprises=json.loads((shared_root/'contracts'/profile['references']['enterprise_profiles']).read_text())
    known={e['key'] for e in enterprises['profiles']}
    require({profile['enterprise_seed'],profile['neighbour_seed']}<=known,'UNKNOWN_ENTERPRISE_SEED')
    nodes=profile['services']['required']+profile['services']['optional']
    keyed={s['key']:s for s in nodes}
    require(len(keyed)==len(nodes),'DUPLICATE_SERVICE')
    required={s['key'] for s in profile['services']['required']}
    if profile['mode']=='l4':require({'iam','control-plane','subject'}<=required,'L4_BACKBONE_REQUIRED')
    require(len([s for s in nodes if s['kind']=='engine'])==1 and keyed.get('subject',{}).get('owner')==engine,'ONE_SUBJECT_REQUIRED')
    for s in nodes:
        require(set(s['depends_on'])<=set(keyed),'MISSING_SERVICE_DEPENDENCY')
        if s['kind']=='iam':require(s['key']=='iam' and s['owner']=='baobab-iam','IAM_OWNER_MISMATCH')
        elif s['kind']=='control-plane':require(s['key']=='control-plane' and s['owner']=='baobab-cp','CP_OWNER_MISMATCH')
        else:require(s['owner']==engine,'NATIVE_STORE_OWNER_MISMATCH')
        if s['key'] in required:require(set(s['depends_on'])<=required,'REQUIRED_DEPENDENCY_OPTIONAL')
    visiting=set();visited=set();order=[]
    def visit(key):
        require(key not in visiting,'SERVICE_CYCLE')
        if key in visited:return
        visiting.add(key)
        for dep in sorted(keyed[key]['depends_on']):visit(dep)
        visiting.remove(key);visited.add(key);order.append(key)
    for key in sorted(required):visit(key)
    require(CRITERIA<=set(profile['reporting']['case_ids']),'MANDATORY_CRITERIA_OMITTED')
    require(not any(re.match(r'^(INT-|NAB-)',x) for x in profile['reporting']['case_ids']),'CANONICAL_CASE_ALIAS_REFUSED')
    clients=profile['iam'];ids=[v['client_id'] for v in clients.values()]
    require(len(set(ids))==3,'DISTINCT_ISSUER_CLIENTS_REQUIRED')
    registry=environment.yaml_file(shared_root/'contracts/identity/v1/workload-registry.yaml')['workloads']
    for role,identity in clients.items():
        row=registry.get(identity['client_id'],{})
        require(row.get('environment')=='development' and row.get('status')=='ACTIVE' and row.get('credential_type')=='client_credentials','REGISTERED_DEVELOPMENT_IDENTITY_REQUIRED')
        require(set(identity['audiences'])<=set(row.get('allowed_audiences',[])) and set(identity['scopes'])<=set(row.get('allowed_scopes',[])),'IAM_CEILING_EXCEEDED')
        if role=='validator':
            require(identity['audiences']==['baobab-control-plane'] and identity['scopes']==['context:validate'] and engine in row.get('validates_audiences',[]),'VALIDATOR_CEILING_REFUSED')
        else:
            require(set(identity['audiences'])=={'baobab-control-plane',engine} and 'context:resolve' in identity['scopes'] and 'context:validate' not in identity['scopes'],'CALLER_CEILING_REFUSED')
    contracts=catalogue.Contracts(shared_root/'contracts');definitions=contracts.definitions()
    keys=[]
    for cap in profile['capabilities']:
        key=cap['capability_key'];keys.append(key)
        require(key in definitions and cap['contract_version'] in {v['major'] for v in definitions[key][0]['contracts']},'UNKNOWN_CANONICAL_CAPABILITY_OR_VERSION')
    require(len(keys)==len(set(keys)),'DUPLICATE_CAPABILITY')
    for name,binding in profile['adapter']['environment'].items():
        require(not re.search(r'(?:SKIP|BYPASS|ALLOW_ALL|FORCE_ACTIVE|TLS_REJECT_UNAUTHORIZED|INSECURE)',name),'UNSAFE_ENVIRONMENT_BINDING')
        if 'constant' in binding:
            value=binding['constant']
            require(value.lower() not in {'production','staging','protected','verified','certified'} and not re.search(r'(SECRET|PASSWORD|TOKEN|CREDENTIAL|CLIENT_ID|URL|URI|ORIGIN|HOST)',name),'LITERAL_SECRET_OR_ENDPOINT_REFUSED')
            if name.endswith('ENVIRONMENT'):require(value=='development','WRONG_ENVIRONMENT')
        if binding.get('source','').startswith('native.'):
            node=keyed.get(binding['source'].split('.')[1],{})
            require(node.get('owner')==engine and node.get('kind') in {'postgresql','qdrant','redis'},'FOREIGN_NATIVE_STORE_REFUSED')
    owner_status='NOT_INSPECTED'
    if engine_root is not None:
        engine_root=Path(engine_root)
        for relative in (*profile['references'].values(),):
            if relative.startswith('.baobab/'):owned_file(engine_root,relative)
        owned_file(engine_root,profile['adapter']['path']);owned_file(engine_root,profile['adapter']['dockerfile'])
        env=environment.yaml_file(engine_root/profile['references']['environment'])
        require(env.get('application',{}).get('name')==engine,'ENVIRONMENT_OWNER_MISMATCH')
        environment.check(engine_root,json.loads((shared_root/'.baobab/environment-profiles.json').read_text()))
        declaration=environment.yaml_file(engine_root/profile['references']['capability_provider'])
        require(not catalogue.validate_declaration(contracts,declaration,engine_root,engine),'OWNER_DECLARATION_INVALID')
        provider=next((p for p in declaration['providers'] if p['provider_key']==profile['provider_key']),None)
        require(provider is not None,'PROVIDER_NOT_DECLARED')
        for cap in profile['capabilities']:
            require(any(s['capability_key']==cap['capability_key'] and s['implementation_status']=='IMPLEMENTED' and cap['contract_version'] in s['contract_versions'] for s in provider['support']),'OWNER_CAPABILITY_NOT_IMPLEMENTED')
        owner_status='DECLARED_IMPLEMENTATION_ONLY'
    return {'profile_key':profile['profile_key'],'subject_engine':engine,'mode':profile['mode'],
        'service_order':order,'optional_services':{s['key']:'NOT_STARTED' for s in profile['services']['optional']},
        'capabilities':keys,'owner_support':owner_status,'scope':'SOURCE_PROFILE_VALIDATION_ONLY',
        'protected_acceptance':False,'production_authorized':False}


def registration(profile,engine_root,shared_root=ROOT):
    validate(profile,shared_root=shared_root,engine_root=engine_root)
    declaration=environment.yaml_file(Path(engine_root)/profile['references']['capability_provider'])
    return catalogue.generate_registration(catalogue.Contracts(shared_root/'contracts'),declaration,profile['provider_key'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile',type=Path);parser.add_argument('--engine-root',type=Path)
    args=parser.parse_args()
    try:print(json.dumps(validate(read_profile(args.profile),engine_root=args.engine_root),sort_keys=True));return 0
    except Exception:
        print('ENGINE_PROFILE_REFUSED: check closed schema, service graph, canonical references and IAM ceilings',file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
