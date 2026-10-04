#!/usr/bin/env python3
import copy
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'validate-federation-contracts.py'
spec = importlib.util.spec_from_file_location('federation_contracts', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class FederationContracts(unittest.TestCase):
    def fixture(self, protocol='oidc'):
        return json.loads((m.IDENTITY / 'examples' / f'federation-{protocol}.json').read_text())

    def mapped(self, protocol='oidc'):
        b = self.fixture(protocol)
        b['trust'].update(status='ACTIVE', activated_at=b['trust']['created_at'],
                          activation_evidence_reference='ref_ciactivation')
        b['external_principal']['resolution'].update(status='RESOLVED',
            principal_id='33333333-3333-4333-8333-333333333333',
            external_identity_id='44444444-4444-4444-8444-444444444444',
            mapping_reference='ref_cimapping', mapping_basis='ISSUER_SUBJECT',
            resolved_at=b['external_principal']['observed_at'])
        b['assurance'].update(mapping_status='MAPPED', level='BAOBAB-A1',
                              mapping_evidence_reference='ref_cidecision')
        return b

    def reject(self, b):
        self.assertTrue(m.validate_bundle(b))

    def test_examples_and_mapped_protocols(self):
        m.main()
        for protocol in ('oidc', 'saml2'):
            self.assertEqual([], m.validate_bundle(self.mapped(protocol)))

    def test_all_nonactive_states_deny_new_authentication(self):
        for status in ('REQUESTED', 'CONFIGURING', 'VERIFYING', 'SUSPENDED', 'ROTATING', 'REVOKED', ' ACTIVE ', 'UNKNOWN'):
            self.assertFalse(m.trust_allows_new_authentication({'status': status}))
        self.assertTrue(m.trust_allows_new_authentication({'status': 'ACTIVE'}))
        self.assertFalse(m.trust_allows_new_authentication({}))

    def test_active_and_revoked_need_evidence_and_time(self):
        for status in ('ACTIVE', 'REVOKED'):
            b = self.fixture(); b['trust']['status'] = status; self.reject(b)
        b = self.mapped(); b['trust']['revoked_at'] = b['trust']['updated_at']; self.reject(b)

    def test_unresolved_cannot_fabricate_canonical_id(self):
        for key, value in [('principal_id', '33333333-3333-4333-8333-333333333333'),
                           ('external_identity_id', '44444444-4444-4444-8444-444444444444'),
                           ('mapping_reference', 'ref_cimapping'), ('mapping_basis', 'ISSUER_SUBJECT')]:
            b = self.fixture(); b['external_principal']['resolution'][key] = value; self.reject(b)

    def test_resolution_needs_authoritative_mapping_not_email(self):
        b = self.fixture(); b['external_principal']['resolution']['status'] = 'RESOLVED'; self.reject(b)
        for value in ('EMAIL', 'PROVIDER_SUBJECT', ' ISSUER_SUBJECT '):
            b = self.mapped(); b['external_principal']['resolution']['mapping_basis'] = value; self.reject(b)
        b = self.mapped(); b['external_principal']['resolution']['principal_id'] = 'orphan:pending-review'; self.reject(b)

    def test_issuer_subject_remain_exact_distinct_keys(self):
        b = self.fixture()
        # An email-shaped stable subject is legal evidence, never linking permission.
        for obj in (b['external_principal'], b['assurance']): obj['subject'] = 'same@example.test'
        self.assertEqual([], m.validate_bundle(b))
        other = copy.deepcopy(b)
        other['trust']['upstream_issuer'] = 'https://another.example.test/issuer'
        other['external_principal']['issuer'] = other['assurance']['issuer'] = other['trust']['upstream_issuer']
        other['assurance']['upstream_evidence']['oidc']['issuer'] = other['trust']['upstream_issuer']
        self.assertEqual([], m.validate_bundle(other))
        self.assertNotEqual((b['external_principal']['issuer'], b['external_principal']['subject']),
                            (other['external_principal']['issuer'], other['external_principal']['subject']))
        self.assertEqual({'status': 'UNRESOLVED'}, other['external_principal']['resolution'])

    def test_provenance_cannot_mix_event_trust_provider_or_identity(self):
        changes = {'authentication_event_id':'55555555-5555-4555-8555-555555555555',
                   'trust_id':'55555555-5555-4555-8555-555555555555', 'subject':'different',
                   'issuer':'https://other.example.test', 'provider_id':'provider_ciother',
                   'engine_instance_id':'ei_ciother', 'assurance_policy_reference':'ref_ciotherpolicy'}
        for key, value in changes.items():
            b = self.fixture(); b['assurance'][key] = value; self.reject(b)
        b = self.fixture(); b['assurance']['upstream_evidence']['oidc']['issuer']='https://other.example.test'; self.reject(b)
        b = self.fixture(); b['trust']['provider_binding']['provider_id']='provider_ciother'; self.reject(b)

    def test_unknown_cannot_claim_level_or_decision(self):
        for key, value in [('level', 'BAOBAB-A1'), ('mapping_evidence_reference', 'ref_cidecision')]:
            b = self.fixture(); b['assurance'][key] = value; self.reject(b)
        b = self.fixture(); b['assurance']['mapping_status']='MAPPED'; self.reject(b)

    def test_upstream_cannot_claim_a4_or_unrecognised_assurance(self):
        for value in ('BAOBAB-A4', 'BAOBAB-A0', 'BAOBAB-A3 ', 'MFA'):
            b = self.mapped(); b['assurance']['level']=value; self.reject(b)

    def test_protocol_evidence_is_exclusive(self):
        b = self.fixture(); b['assurance']['upstream_evidence']['saml']=self.fixture('saml2')['assurance']['upstream_evidence']['saml']; self.reject(b)
        b = self.fixture(); b['assurance']['upstream_evidence']=self.fixture('saml2')['assurance']['upstream_evidence']; self.reject(b)
        b = self.fixture(); b['trust']['protocol']=' OIDC '; self.reject(b)

    def test_no_secrets_or_business_authority(self):
        for target in ('trust', 'external_principal', 'assurance'):
            for key in ('tenant_id', 'roles', 'email', 'client_secret', 'private_key', 'assertion'):
                b = self.fixture(); b[target][key]='sensitive-test-value'; errors=m.validate_bundle(b)
                self.assertTrue(errors); self.assertNotIn('sensitive-test-value', str(errors))
        b=self.fixture(); b['trust']['provider_binding']['idp_alias']='native'; self.reject(b)

    def test_invalid_references_and_unbounded_scope(self):
        for key, value in [('estate_ids', []), ('estate_ids', ['*']), ('organisation_ids', []),
                           ('assurance_policy_reference', 'https://example.test/key'), ('revision', 0)]:
            b=self.fixture(); b['trust'][key]=value; self.reject(b)
        b=self.fixture(); b['trust']['estate_ids']*=2; self.reject(b)

    def test_issuer_and_subject_fail_closed(self):
        for issuer in ('http://idp.example.test', 'https://user:pass@idp.example.test',
                       'https://idp.example.test?query=x', 'https://idp.example.test#fragment'):
            b=self.fixture(); b['trust']['upstream_issuer']=issuer; self.reject(b)
        for subject in ('', ' ', ' padded '):
            b=self.fixture(); b['external_principal']['subject']=subject; self.reject(b)

    def test_terminal_revocation_reactivation_and_revision(self):
        before=self.fixture()['trust']; after=copy.deepcopy(before)
        after.update(status='ACTIVE', revision=2)
        self.assertEqual([], m.validate_transition(before, after))
        for previous, current in [('REVOKED','ACTIVE'), ('REVOKED','REVOKED'),
                                  ('SUSPENDED','ACTIVE'), ('ROTATING','ACTIVE'),
                                  ('REQUESTED','ACTIVE')]:
            before['status']=previous; after['status']=current
            self.assertTrue(m.validate_transition(before, after))
        before['status']='VERIFYING'; after['status']='ACTIVE'; after['upstream_issuer']='https://different.example.test'
        self.assertTrue(m.validate_transition(before, after))
        after['upstream_issuer']=before['upstream_issuer']; after['revision']=1
        self.assertTrue(m.validate_transition(before, after))

    def test_temporal_bounds(self):
        for target, key, value in [('trust','updated_at','2026-10-03T10:00:00Z'),
                                   ('external_principal','expires_at','2026-10-04T10:00:00Z'),
                                   ('assurance','expires_at','2026-10-04T10:11:00Z'),
                                   ('assurance','evaluated_at','2026-10-04T09:59:00Z'),
                                   ('assurance','evaluated_at','2026-10-04T10:00:00')]:
            b=self.fixture(); b[target][key]=value; self.reject(b)
        b=self.fixture('saml2'); b['assurance']['upstream_evidence']['saml']['session_expires_at']='2026-10-04T10:01:00Z'; self.reject(b)
        b=self.fixture(); b['assurance']['upstream_evidence']['oidc']['step_up_at']='2026-10-04T11:00:00Z'; self.reject(b)


if __name__ == '__main__': unittest.main()
