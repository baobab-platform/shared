"""DEV-06 registry ceilings confer no canonical entitlement or estate."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]

class DevelopmentAPIWorkloads(unittest.TestCase):
    def test_separate_development_only_caller_and_validator(self):
        registry = yaml.safe_load((ROOT / 'contracts/identity/v1/workload-registry.yaml').read_text())
        entries = registry['workloads']
        caller = entries['baobab-dev-external-api']
        validator = entries['baobab-dev-pulse-validator']
        for entry in (caller, validator):
            self.assertEqual(entry['environment'], 'development')
            self.assertEqual(entry['status'], 'ACTIVE')
            self.assertEqual(entry['credential_type'], 'client_credentials')
        self.assertEqual(set(caller['allowed_audiences']), {'baobab-control-plane','baobab-pulse'})
        self.assertEqual(set(caller['allowed_scopes']), {'context:resolve','intelligence:evidence:search'})
        self.assertNotIn('validates_audiences', caller)
        self.assertEqual(validator['allowed_audiences'], ['baobab-control-plane'])
        self.assertEqual(validator['allowed_scopes'], ['context:validate'])
        self.assertEqual(validator['validates_audiences'], ['baobab-pulse'])
        self.assertNotEqual(caller['owner'], validator['owner'])

if __name__ == '__main__': unittest.main()
