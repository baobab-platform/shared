"""Closed development credential ceilings; production profiles never downgraded."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]

class SubscriptionWorkloads(unittest.TestCase):
    def test_exact_separate_development_ceilings(self):
        workloads = yaml.safe_load((ROOT / 'contracts/identity/v1/workload-registry.yaml').read_text())['workloads']
        expected = {'baobab-dev-cp-subscriptions': {'repository': 'baobab-platform/baobab-cp', 'owner': 'baobab-platform/baobab-cp', 'runtime': 'ADR-SHARED-043 disposable CP subscription command and event producer', 'environment': 'development', 'allowed_audiences': ['baobab-subscriptions'], 'allowed_scopes': ['billing:manage', 'billing:read', 'billing:observe', 'usage:record'], 'credential_type': 'client_credentials', 'rotation_owner': 'baobab-platform/baobab-cp', 'status': 'ACTIVE'}, 'baobab-dev-subscriptions-assessor': {'repository': 'baobab-platform/baobab-subscriptions', 'owner': 'baobab-platform/baobab-subscriptions', 'runtime': 'ADR-SHARED-043 disposable Subscriptions current CP authority reader', 'environment': 'development', 'allowed_audiences': ['baobab-control-plane'], 'allowed_scopes': ['subscription:internal-authority', 'subscription:current-workload-read', 'subscription:commercial-authority'], 'credential_type': 'client_credentials', 'rotation_owner': 'baobab-platform/baobab-subscriptions', 'status': 'ACTIVE'}}
        for client, row in expected.items():
            self.assertEqual(row, workloads[client])
        for client in ('baobab-cp-workload', 'baobab-subscriptions-workload'):
            self.assertEqual('production', workloads[client]['environment'])
            self.assertEqual('PROVISIONED', workloads[client]['status'])
            self.assertEqual('federated_workload_token', workloads[client]['credential_type'])
        self.assertTrue(set(expected['baobab-dev-cp-subscriptions']['allowed_scopes']).isdisjoint(
            expected['baobab-dev-subscriptions-assessor']['allowed_scopes']))

if __name__ == '__main__': unittest.main()
