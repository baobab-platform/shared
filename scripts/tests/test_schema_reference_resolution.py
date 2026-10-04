#!/usr/bin/env python3
"""Exercise the actual generic Ruby checker without unrelated event fixtures."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
CHECKER = (ROOT / 'scripts/validate-identity-events-contracts.rb').read_text().split('# 2. identity-events')[0]


class SchemaReferences(unittest.TestCase):
    def check(self, ref, duplicate=False):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); folder=root/'contracts/test/v1'; folder.mkdir(parents=True)
            (folder/'target.schema.json').write_text(json.dumps({'$id':'https://contracts.example.test/target.schema.json'}))
            (folder/'source.schema.json').write_text(json.dumps({'$id':'https://contracts.example.test/source.schema.json','$ref':ref}))
            if duplicate:
                (folder/'duplicate.schema.json').write_text((folder/'target.schema.json').read_text())
            code=CHECKER.replace('ROOT = File.expand_path("..", __dir__)', 'ROOT = '+json.dumps(str(root)))
            return subprocess.run(['ruby','-e',code],capture_output=True,text=True).returncode

    def test_relative_and_exact_published_ids(self):
        self.assertEqual(0,self.check('target.schema.json'))
        self.assertEqual(0,self.check('https://contracts.example.test/target.schema.json#/$defs/id'))

    def test_unknown_url_missing_file_and_duplicate_ids(self):
        self.assertNotEqual(0,self.check('https://untrusted.example.test/target.schema.json'))
        self.assertNotEqual(0,self.check('missing.schema.json'))
        self.assertNotEqual(0,self.check('target.schema.json',duplicate=True))


if __name__ == '__main__': unittest.main()
