"""Private scanner wire invariants; no synthetic fixture grants trust or ACTIVE."""
import base64
import copy
import json
from pathlib import Path
import unittest
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / 'contracts/evidence/v1/scanner-intake.schema.json').read_text())
REG = Registry()
for file in (ROOT / 'contracts').rglob('*.schema.json'):
    doc = json.loads(file.read_text())
    REG = REG.with_resource(doc['$id'], Resource.from_contents(doc))

def valid(name, value):
    return Draft202012Validator({'$ref': SCHEMA['$id']+'#/$defs/'+name},
        registry=REG, format_checker=FormatChecker()).is_valid(value)

class ScannerIntake(unittest.TestCase):
    def test_private_route_and_exact_workload_scope(self):
        spec=yaml.safe_load((ROOT/'contracts/evidence/v1/scanner-intake.openapi.yaml').read_text())
        self.assertEqual(list(spec['paths']),['/internal/evidence/v1/scanned-artifacts'])
        operation=spec['paths']['/internal/evidence/v1/scanned-artifacts']['post']
        self.assertEqual(operation['security'],[{'ScannerWorkload':['verification:scan-attest']}])
        self.assertEqual(operation['requestBody']['content']['application/json']['schema']['$ref'],
            'scanner-intake.schema.json#/$defs/ScanSubmission')
        self.assertEqual(operation['responses']['201']['content']['application/json']['schema']['$ref'],
            'scanner-intake.schema.json#/$defs/ScanReceipt')

    def test_closed_signed_payload_and_non_authority(self):
        proof = dict(evidence_id='evr_synthetic', artifact_id='eart_synthetic',
            media_type='application/pdf', digest='sha256:'+'a'*64,
            scanner_id='synthetic-scanner', scanner_version='v1', outcome='CLEAN',
            scanned_at='2026-10-12T17:00:00.123456Z',
            signature_base64=base64.b64encode(bytes(64)).decode())
        request = dict(verification_case_id='vcase_synthetic', claim_id='ecl_synthetic',
            proof=proof, document_base64=base64.b64encode(b'%PDF-1.7\nsynthetic').decode())
        self.assertTrue(valid('ScanSubmission', request))
        for key, value in [('outcome','VERIFIED'),('signature_base64','unsigned'),
                           ('media_type','application/javascript'),('digest','sha256:invalid')]:
            bad=copy.deepcopy(request); bad['proof'][key]=value
            self.assertFalse(valid('ScanSubmission',bad),key)
        for injected in ('tenant_id','actor_id','verified','source_id','custody_path'):
            bad=copy.deepcopy(request);bad[injected]='forged'
            self.assertFalse(valid('ScanSubmission',bad),injected)
        bad=copy.deepcopy(request);bad['proof']['public_key']='self-signed'
        self.assertFalse(valid('ScanSubmission',bad))
        receipt={key:request[key] for key in ('verification_case_id','claim_id')}
        receipt.update({key:proof[key] for key in ('evidence_id','artifact_id','digest')})
        receipt.update(standing='SCAN_PROOF_RECORDED',authority_granted=False)
        self.assertTrue(valid('ScanReceipt',receipt))
        for key,value in [('authority_granted',True),('standing','VERIFIED'),
                          ('document_base64',request['document_base64']),('signature_base64',proof['signature_base64'])]:
            bad=dict(receipt);bad[key]=value
            self.assertFalse(valid('ScanReceipt',bad),key)

if __name__=='__main__':unittest.main()
