"""Redacted source projection checks; no fresh runtime acceptance is inferred."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/architecture/evidence/dev07-bff-http-2026-10-29'
CHECKS = {
    'csrf-denial', 'current-cp-trade-http-context', 'custody-outage-and-recovery',
    'issuer-consent-revocation', 'membership-suspension-denial',
    'native-fixture-cleanup', 'native-next-iam-session', 'wrong-organisation-denial',
}


class BffEvidenceProjectionTests(unittest.TestCase):
    def test_digest_linked_component_scope_has_no_config_or_acceptance_promotion(self):
        report = json.loads((EVIDENCE / 'custody-projection.json').read_bytes())
        self.assertEqual('9577f9d1ea9fc0a957899bbee2d8d1d96044b937d84e664418791b7c16e3ca9a', report['original_archive_sha256'])
        self.assertEqual('96736c8bac5991db04ae964136b6422701b1b4873d362649c85588edb8881a3b', report['original_suite_sha256'])
        self.assertEqual('dceafb576160fa71252d5c799c6a67482c52a5eea63d8423a12cbe1fc7de125f', report['original_lifecycle_sha256'])
        self.assertEqual(CHECKS, set(report['checks']))
        self.assertTrue(all(v is True for v in report['checks'].values()))
        for key in ('bff_http_component_qualified', 'teardown_verified', 'issuer_cleanup_verified',
                    'binding_revocation_verified', 'runtime_identity_verified'):
            self.assertIs(True, report[key])
        for key in ('int05_qualified', 'provider_qualified', 'protected_acceptance',
                    'production_authorized', 'projection_is_original_receipt'):
            self.assertIs(False, report[key])
        for key in ('native_config_hashes', 'dev07_bff_config_hashes', 'lifecycle', 'subject_token', 'credentials'):
            self.assertNotIn(key, report)
        self.assertEqual('REAL_COMPONENT_SYNTHETIC_DATA', report['evidence_class'])

    def test_historical_inventory_has_not_been_rewritten(self):
        path = ROOT / 'docs/architecture/evidence/dev07-2026-10-25/final-report-40157210941.json'
        report = json.loads(path.read_bytes())
        self.assertEqual(25, len(report['cases']))
        self.assertEqual(16, sum(c['result'] == 'PASS' for c in report['cases'].values()))
        self.assertEqual(9, sum(c['result'] == 'BLOCKED' for c in report['cases'].values()))


if __name__ == '__main__':
    unittest.main()
