"""DEV-14 source contract tests. No runtime, certification or financial claim."""
import copy
import json
from pathlib import Path
import sys
import unittest
from jsonschema import ValidationError

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import engine_integration_profile as profile


class EngineIntegrationProfiles(unittest.TestCase):
    def setUp(self):
        self.pulse=json.loads((ROOT/'contracts/development/v1/examples/engines/pulse-intelligence.json').read_text())
        self.payments=json.loads((ROOT/'contracts/development/v1/examples/engines/payments-sandbox.json').read_text())

    def rejects(self,change):
        data=copy.deepcopy(self.pulse);change(data)
        with self.assertRaises((ValueError,ValidationError)):profile.validate(data)

    def test_every_shipped_engine_profile_is_semantically_validated(self):
        # Do not let a later profile pass catalogue schema checks without
        # running DEV-14 semantic authority, owner, and service-graph checks.
        examples = sorted((ROOT / 'contracts/development/v1/examples/engines').glob('*.json'))
        self.assertGreaterEqual(len(examples), 2)
        for path in examples:
            with self.subTest(profile=path.name):
                receipt = profile.validate(profile.read_profile(path))
                self.assertEqual(receipt['scope'], 'SOURCE_PROFILE_VALIDATION_ONLY')
                self.assertFalse(receipt['production_authorized'])

    def test_payments_startup_registration_retains_native_invocation(self):
        # CP reloads this complete registration at startup. Missing invocation
        # removes an owner's route; metadata drift also churns provider version.
        import capability_catalogue as catalogue
        import development_environment as environment
        declaration=environment.yaml_file(ROOT/'contracts/capability/v1/examples/provider-declaration.yaml')
        generated=catalogue.generate_registration(catalogue.Contracts(ROOT/'contracts'),declaration,'baobab-payments.sandbox')
        committed=json.loads((ROOT/'contracts/payments/v1/capabilities.json').read_text())
        self.assertEqual(generated['provider'],committed['provider'])
        self.assertEqual(committed['provider']['invocation'],{'service_reference':'service://baobab-payments/payments','protocol':'http'})
        self.assertEqual(committed['provider']['lifecycle'],'DRAFT')
        self.assertTrue(committed['provider']['simulated'])
        self.assertFalse(committed['provider']['production_permitted'])

    def test_headless_profiles_reference_existing_authorities_and_minimal_services(self):
        for p in (self.pulse,self.payments):
            actual=profile.validate(p)
            self.assertNotIn('baobab-cms',actual['service_order'])
            self.assertFalse(actual['protected_acceptance']);self.assertFalse(actual['production_authorized'])
            self.assertEqual(actual['owner_support'],'NOT_INSPECTED')
            self.assertEqual(set(p['reporting']['case_ids']) & profile.CRITERIA,profile.CRITERIA)

    def test_unknown_authority_and_secret_fields_are_rejected_at_every_boundary(self):
        for field in ('certified','force_active','allow_all_tenants','skip_security','accept_as_staging','production_permitted_override','password','sql','endpoint'):
            for location in ('root','policy','adapter','reporting'):
                def mutate(p,field=field,location=location):
                    target=p if location=='root' else p[{'policy':'run_policy','adapter':'adapter','reporting':'reporting'}[location]]
                    target[field]='forbidden'
                with self.subTest(field=field,location=location):self.rejects(mutate)

    def test_protected_environment_real_data_and_unbounded_lease_are_refused(self):
        for key,value in [('environment','production'),('environment','staging'),('synthetic_only',False),('max_lease_seconds',86401),('expose_admin_ports',True),('network','host'),('cleanup','optional')]:
            with self.subTest(key=key,value=value):self.rejects(lambda p:p['run_policy'].update({key:value}))

    def test_graph_cycle_duplicate_missing_dependency_and_optional_dependency_refuse(self):
        self.rejects(lambda p:p['services']['required'][0]['depends_on'].append('subject'))
        self.rejects(lambda p:p['services']['required'].append(copy.deepcopy(p['services']['required'][0])))
        self.rejects(lambda p:p['services']['required'][2]['depends_on'].append('unavailable'))
        self.rejects(lambda p:p['services']['optional'].append(p['services']['required'].pop()))
        self.rejects(lambda p:p['services']['required'][3].update(owner='baobab-cp'))
        for key in ('iam','control-plane','subject'):
            self.rejects(lambda p:next(s for s in p['services']['required'] if s['key']==key).update(kind='redis',owner=p['subject_engine']))

    def test_iam_clients_cannot_expand_registry_or_borrow_validator_rights(self):
        self.rejects(lambda p:p['iam']['caller']['scopes'].append('context:validate'))
        self.rejects(lambda p:p['iam']['caller']['audiences'].append('baobab-payments'))
        self.rejects(lambda p:p['iam']['caller'].update(client_id='baobab-subscriptions-workload'))
        self.rejects(lambda p:p['iam']['validator']['scopes'].append('context:resolve'))
        self.rejects(lambda p:p['iam'].update(neighbour=p['iam']['caller']))

    def test_canonical_capabilities_versions_and_engine_owner_cannot_be_invented(self):
        self.rejects(lambda p:p['capabilities'][0].update(capability_key='vendor.fake.operation'))
        self.rejects(lambda p:p['capabilities'][0].update(contract_version=99))
        self.rejects(lambda p:p['capabilities'].append(p['capabilities'][0]))
        self.rejects(lambda p:p.update(provider_key='baobab-payments.sandbox'))

    def test_cases_never_alias_existing_scenarios_or_omit_common_obligations(self):
        for case in profile.CRITERIA:self.rejects(lambda p:p['reporting']['case_ids'].remove(case))
        self.rejects(lambda p:p['reporting']['case_ids'].append('NAB-03'))
        self.rejects(lambda p:p.update(neighbour_seed=p['enterprise_seed']))

    def test_adapter_cannot_reference_host_paths_endpoints_credentials_or_foreign_stores(self):
        for path in ('/etc/passwd','../private.py','.baobab/../../private.py'):
            self.rejects(lambda p:p['adapter'].update(path=path))
        for name,value in [('SKIP_AUTH',{'constant':'true'}),('PASSWORD',{'constant':'literal'}),('TARGET_URL',{'constant':'production'}),('BAOBAB_ENVIRONMENT',{'constant':'staging'}),('DATABASE_URL',{'source':'native.control-plane.url'})]:
            self.rejects(lambda p:p['adapter']['environment'].update({name:value}))


if __name__=='__main__':unittest.main()
