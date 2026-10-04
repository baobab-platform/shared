#!/usr/bin/env python3
import copy
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'validate-identity-runtime-contracts.py'
spec = importlib.util.spec_from_file_location('runtime_contracts', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RuntimeProfiles(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((m.IDENTITY / 'examples/runtime-profile-hydra.json').read_text())

    def verified(self):
        p = copy.deepcopy(self.profile)
        p['capability_observations'][0].update(verification_status='VERIFIED', evidence={
            'evidence_reference': 'ref_ciconformance', 'artifact_digest': p['artifact_digest'],
            'observed_at': '2026-10-04T09:00:00Z', 'expires_at': '2026-10-05T09:00:00Z'})
        return p

    def test_examples_and_verified(self):
        m.main()
        self.assertEqual([], m.validate_profile(self.verified()))

    def test_verified_requires_evidence(self):
        self.profile['capability_observations'][0]['verification_status'] = 'VERIFIED'
        self.assertTrue(m.validate_profile(self.profile))

    def test_nonverified_cannot_claim_evidence(self):
        for status in ('UNVERIFIED', 'UNSUPPORTED', 'DEPLOYMENT_DEPENDENT'):
            with self.subTest(status=status):
                p = self.verified()
                p['capability_observations'][0]['verification_status'] = status
                self.assertTrue(m.validate_profile(p))

    def test_evidence_artifact_and_dates(self):
        for key, value in [('artifact_digest', 'sha256:' + 'b'*64),
                           ('observed_at', '2026-10-06T09:00:00Z'),
                           ('expires_at', self.profile['published_at']),
                           ('expires_at', '2026-10-01T09:00:00Z'),
                           ('observed_at', '2026-10-04T09:00:00'),
                           ('evidence_reference', 'evr_wrongdomain')]:
            with self.subTest(key=key, value=value):
                p = self.verified()
                p['capability_observations'][0]['evidence'][key] = value
                self.assertTrue(m.validate_profile(p))

    def test_duplicate_facet_with_different_status(self):
        p = self.profile
        item = copy.deepcopy(p['capability_observations'][0])
        item['verification_status'] = 'UNSUPPORTED'
        p['capability_observations'].append(item)
        self.assertTrue(m.validate_profile(p))

    def test_enums_fail_closed(self):
        for key, value in [('verification_status', ' VERIFIED '), ('verification_status', 'ACTIVE'),
                           ('capability', 'PASSKEY '), ('capability', 'identity.authentication.perform')]:
            p = copy.deepcopy(self.profile)
            p['capability_observations'][0][key] = value
            self.assertTrue(m.validate_profile(p))

    def test_identifiers_and_bounds(self):
        for key, value in [('provider_id', 'keycloak'), ('engine_instance_id', 'provider_hydra'),
                           ('configuration_reference', 'https://example.com/secret'),
                           ('security_domain_reference', 'tenant_abc'), ('artifact_digest', 'latest'),
                           ('revision', 0), ('published_at', '2026-10-04'),
                           ('capability_observations', [])]:
            p = copy.deepcopy(self.profile)
            p[key] = value
            self.assertTrue(m.validate_profile(p))

    def test_business_health_and_credentials_rejected(self):
        for key in ('tenant_id', 'organisation_id', 'lifecycle', 'health', 'provider_type', 'client_secret'):
            p = copy.deepcopy(self.profile)
            p[key] = 'sensitive-value-must-not-appear'
            errors = m.validate_profile(p)
            self.assertTrue(errors)
            self.assertNotIn(p[key], str(errors))
        for key in ('token', 'private_key', 'logs'):
            p = self.verified()
            p['capability_observations'][0]['evidence'][key] = 'secret'
            self.assertTrue(m.validate_profile(p))

    def test_historical_publication_is_not_current_eligibility(self):
        # Static validation intentionally does not decide current runtime selection.
        p = self.verified()
        p['published_at'] = '2020-01-01T09:15:00Z'
        p['capability_observations'][0]['evidence'].update(
            observed_at='2020-01-01T09:00:00Z', expires_at='2020-01-02T09:00:00Z')
        self.assertEqual([], m.validate_profile(p))


if __name__ == '__main__':
    unittest.main()
