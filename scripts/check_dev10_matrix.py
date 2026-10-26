"""Check a source-only toolchain snapshot against its immutable provider."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import yaml
ROOT = Path(__file__).resolve().parents[1]
REPOS = {'baobab-dev', 'shared', 'baobab-cp', 'baobab-pulse', 'baobab-erp', 'baobab-subscriptions', 'baobab-payments', 'baobab-trade', 'thamani', 'zuribeans', 'baobab-tms', 'infrastructure'}

def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(provider=None):
    matrix = json.loads((ROOT / '.baobab/dev10-toolchain-matrix.json').read_text())
    require(matrix['schema'] == 'dev10-toolchain-matrix.v1', 'invalid DEV-10 matrix')
    require(matrix['purpose'] == 'READ_MODEL_NOT_AUTHORITY', 'invalid DEV-10 matrix')
    for key in ('clean_codespace_qualified', 'fleet_upgrade_qualified', 'postgres_physical_migration_qualified', 'production_authorized'):
        require(matrix[key] is False, 'invalid DEV-10 matrix')
    rows = matrix['repositories']
    require(len(rows) == len(REPOS) and {r['repo'] for r in rows} == REPOS, 'invalid DEV-10 matrix')
    for r in rows:
        require(re.fullmatch('[a-f0-9]{40}', r['source_sha']), 'invalid DEV-10 matrix')
        require(r['fresh_codespace_observed'] is False and r['upgrade_branch_qualified'] is False, 'invalid DEV-10 matrix')
        require(r['evidence_urls'] == ['https://github.com/baobab-platform/' + r['repo'] + '/tree/' + r['source_sha']], 'invalid DEV-10 matrix')
    if provider is not None:
        source = matrix['provider']
        sha = subprocess.run(['git', '-C', str(provider), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
        require(sha == source['source_sha'], 'provider checkout must equal observed immutable source')
        for path, key in [('config/capabilities.yaml', 'capabilities_sha256'), ('config/versions.lock', 'versions_lock_sha256')]:
            require(hashlib.sha256((provider / path).read_bytes()).hexdigest() == source[key], 'invalid DEV-10 matrix')
        raw = yaml.safe_load((provider / 'config/capabilities.yaml').read_text())['capabilities']

        def flatten(value, prefix=''):
            return [cap for key, child in value.items() if key != 'extends' for cap in (flatten(child, prefix + key + '.') if isinstance(child, dict) else [prefix + key])]
        catalogue = json.loads((ROOT / '.baobab/environment-profiles.json').read_text())
        for name, policy in catalogue['profiles'].items():
            expected = flatten(raw[name])
            if 'extends' in raw[name]:
                expected += flatten(raw[raw[name]['extends']])
            require(set(policy['capabilities']) == set(expected), 'profile capability drift')
    print('VALID_DEV10_SOURCE_MATRIX; no Codespace, fleet upgrade or database migration qualification')
if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--provider-root', type=Path)
    check(p.parse_args().provider_root)

