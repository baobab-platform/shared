"""Actual workspace image/capability checks; never container acceptance."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('development_environment',ROOT/'scripts/development_environment.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAT=json.loads((ROOT/'.baobab/environment-profiles.json').read_text())
IMAGE='ghcr.io/baobab-platform/baobab-dev:1.4.4-frontend'


class EnvironmentTests(unittest.TestCase):
    def fixture(self, root, config, caps='languages.node'):
        (root/'.baobab').mkdir();(root/'.devcontainer').mkdir()
        (root/'.baobab/environment.yaml').write_text('''schema:
  name: baobab-development-environment-contract
  version: "1.0"
environment:
  provider: baobab-dev
  profile: frontend
  minimum_version: 1.4.4-frontend
validation:
  required_capabilities: ['''+caps+''']
''')
        (root/'.devcontainer/devcontainer.json').write_text(config)

    def test_actual_shared_declaration(self):
        self.assertEqual('SOURCE_ONLY',m.check(ROOT,CAT)['qualification'])

    def test_comments_and_unrelated_files_cannot_satisfy_image(self):
        for config in ('{"image":"ubuntu:26.04", "note":"'+IMAGE+'"}',
                       '{ // '+IMAGE+'\n "image":"ubuntu:26.04"}',
                       '{"image":"'+IMAGE+'-wrong"}'):
            with self.subTest(config=config),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);self.fixture(root,config)
                (root/'.devcontainer/README.md').write_text(IMAGE)
                with self.assertRaises(ValueError):m.check(root,CAT)

    def test_profile_does_not_supply_java_to_frontend(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root,json.dumps({'image':IMAGE}),caps='languages.java')
            with self.assertRaisesRegex(ValueError,'capability'):m.check(root,CAT)

    def test_jsonc_preserves_quoted_urls_and_trailing_commas(self):
        self.assertEqual({'image':IMAGE,'note':',}'},m.jsonc('{/*x*/ "image":"'+IMAGE+'", "note":",}",}'))
        self.assertEqual({'image':IMAGE},m.jsonc('{\"image\":\"'+IMAGE+'\", // trailing comment\n}'))
        with self.assertRaises(ValueError):m.jsonc('{"image":"a","image":"b"}')

    def test_compose_selects_workspace_only_and_refuses_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root,json.dumps({'dockerComposeFile':'compose.yml','service':'workspace'}))
            p=root/'.devcontainer/compose.yml'
            p.write_text('services:\n  workspace:\n    image: ubuntu:26.04\n  unused:\n    image: '+IMAGE+'\n')
            with self.assertRaises(ValueError):m.check(root,CAT)
            p.write_text('services:\n  workspace:\n    image: '+IMAGE+'\n')
            self.assertEqual(IMAGE,m.check(root,CAT)['image'])
            p.unlink();p.symlink_to('/etc/passwd')
            with self.assertRaises(ValueError):m.check(root,CAT)

    def test_final_docker_stage_must_inherit_the_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root,json.dumps({'build':{'dockerfile':'Dockerfile'}}))
            p=root/'.devcontainer/Dockerfile'
            p.write_text('FROM '+IMAGE+' AS unused\nFROM ubuntu:26.04\n')
            with self.assertRaises(ValueError):m.check(root,CAT)
            p.write_text('ARG BASE='+IMAGE+'\nFROM ${BASE} AS base\nFROM base AS workspace\n')
            self.assertEqual(IMAGE,m.check(root,CAT)['image'])

    def test_duplicate_yaml_and_old_versions_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root,json.dumps({'image':IMAGE}))
            p=root/'.baobab/environment.yaml';s=p.read_text()
            p.write_text(s.replace('profile: frontend','profile: full\n  profile: frontend'))
            with self.assertRaises(ValueError):m.check(root,CAT)
            p.write_text(s.replace('1.4.4-frontend','1.4.3-frontend'))
            with self.assertRaises(ValueError):m.check(root,CAT)

    def test_devcontainer_dockerfile_is_relative_to_config_not_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root,json.dumps({'build':{'context':'..','dockerfile':'Dockerfile'}}))
            (root/'Dockerfile').write_text('FROM ubuntu:26.04\n')
            (root/'.devcontainer/Dockerfile').write_text('FROM '+IMAGE+'\n')
            self.assertEqual(IMAGE,m.check(root,CAT)['image'])
            (root/'Dockerfile').write_text('FROM '+IMAGE+'\n')
            (root/'.devcontainer/Dockerfile').write_text('FROM ubuntu:26.04\n')
            with self.assertRaises(ValueError):m.check(root,CAT)

    def test_compose_build_args_override_preserves_actual_context_dockerfile_target(self):
        for shorthand in (False,True):
            with self.subTest(shorthand=shorthand),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);self.fixture(root,json.dumps({'dockerComposeFile':['base.yml','override.yml'],'service':'workspace'}))
                (root/'.devcontainer/actual').mkdir()
                (root/'.devcontainer/actual/Dockerfile').write_text('FROM ubuntu:26.04 AS actual\n')
                (root/'.devcontainer/Dockerfile').write_text('FROM '+IMAGE+'\n')
                build='actual' if shorthand else {'context':'actual','dockerfile':'Dockerfile','target':'actual'}
                (root/'.devcontainer/base.yml').write_text(json.dumps({'services':{'workspace':{'build':build}}}))
                (root/'.devcontainer/override.yml').write_text(json.dumps({'services':{'workspace':{'build':{'args':{'BASE':IMAGE}}}}}))
                with self.assertRaises(ValueError):m.check(root,CAT)
                (root/'.devcontainer/actual/Dockerfile').write_text('ARG BASE\nFROM ${BASE} AS actual\n')
                self.assertEqual(IMAGE,m.check(root,CAT)['image'])

    def test_stage_local_arg_cannot_select_later_from_and_sources_are_exclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root,json.dumps({'build':{'dockerfile':'Dockerfile'}}))
            (root/'.devcontainer/Dockerfile').write_text('FROM ubuntu:26.04 AS first\nARG BASE='+IMAGE+'\nFROM ${BASE}\n')
            with self.assertRaises(ValueError):m.check(root,CAT)
            (root/'.devcontainer/devcontainer.json').write_text(json.dumps({'image':IMAGE,'dockerComposeFile':'unused.yml'}))
            with self.assertRaises(ValueError):m.check(root,CAT)


if __name__=='__main__':unittest.main()

