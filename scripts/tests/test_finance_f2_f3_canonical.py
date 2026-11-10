#!/usr/bin/env python3
"""ADR-SHARED-033 F2/F3 wire tests: source-only, never provider or posting evidence."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
import yaml
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/"contracts/finance/v1"
spec=importlib.util.spec_from_file_location("finance_validator",ROOT/"scripts/validate-finance-contracts.py")
val=importlib.util.module_from_spec(spec);spec.loader.exec_module(val)
COMMANDS=["payable-manage","receivable-manage","bank-reconciliation-manage","expense-manage","budget-manage","reporting-export-create","consolidation-run"]
READS=["cash-position-read","project-cost-read"]
STEMS=COMMANDS+READS
class FinanceF2F3Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.registry=val.registry()
    def pair(self,stem,kind):
        schema=val.validator(stem+"-"+kind+".schema.json",self.registry)
        example=json.loads((PKG/"examples"/(stem+"-"+kind+".json")).read_text())
        return schema,example
    def test_each_request_response_schema_and_fixture(self):
        for stem in STEMS:
            for kind in ("request","response"):
                with self.subTest(stem=stem,kind=kind):
                    schema,doc=self.pair(stem,kind);schema.validate(doc)
    def test_never_trust_client_as_cp_or_native_actor(self):
        for stem in STEMS:
            schema,doc=self.pair(stem,"request")
            for name,bad in (("tenant_id","other"),("legal_entity_id","other"),("ad_client_id",123),
                             ("ad_org_id",456),("approver_id","self-approved"),("provider_id","other")):
                with self.subTest(stem=stem,name=name):
                    self.assertFalse(schema.is_valid(dict(doc,**{name:bad})))
    def test_money_is_exact_string_never_float(self):
        for stem in COMMANDS:
            schema,doc=self.pair(stem,"request")
            no_key=copy.deepcopy(doc);no_key.pop("idempotency_key")
            self.assertFalse(schema.is_valid(no_key))
            for key in ("gross_amount","statement_balance","claim_amount","allocated_amount"):
                if key in doc:
                    invalid=copy.deepcopy(doc);invalid[key]["amount"]=1.25
                    self.assertFalse(schema.is_valid(invalid),(stem,key))
            if "source_document" in doc:
                invalid=copy.deepcopy(doc);invalid["source_document"]["authority"]="baobab-payments"
                self.assertFalse(schema.is_valid(invalid),stem)
    def test_no_implicit_payment_or_gl_authority(self):
        for stem in COMMANDS:
            schema,doc=self.pair(stem,"request")
            for operation in ("CAPTURE","PAYMENT_EXECUTE","GL_POST","SELF_APPROVE"):
                self.assertFalse(schema.is_valid(dict(doc,operation=operation)))
    def test_subscriptions_invoice_and_trade_invoice_remain_distinct(self):
        schema,doc=self.pair("receivable-manage","request")
        schema.validate(doc)
        alt=copy.deepcopy(doc);alt["source_document"]={"type":"TRADE_INVOICE","id":"trade_invoice_synthetic01","authority":"baobab-trade"}
        schema.validate(alt)
        alt["source_document"]["authority"]="baobab-subscriptions"
        self.assertFalse(schema.is_valid(alt))
        alt["commerce_order_id"]="fabricated_trade_order"
        self.assertFalse(schema.is_valid(alt))
    def test_withheld_financial_rows_are_empty(self):
        for stem,key in (("cash-position-read","balances"),("project-cost-read","rows")):
            schema,doc=self.pair(stem,"response")
            bad=copy.deepcopy(doc);bad["completeness"]="withheld"
            self.assertFalse(schema.is_valid(bad))
            bad[key]=[];schema.validate(bad)
    def test_catalogue_has_exact_draft_schemas(self):
        self.assertEqual(val.validate_package(),44)
        defs=yaml.safe_load((PKG/"capabilities.yaml").read_text())["capabilities"]
        owned={x["capability_key"]:x for x in defs}
        for stem in STEMS:
            matches=[x for x in owned.values() if x["contracts"][0]["request_schema"]==stem+"-request.schema.json"]
            self.assertEqual(len(matches),1)
            self.assertEqual((matches[0]["lifecycle"],matches[0]["maturity"],matches[0]["data_classification"]),("DRAFT","EXPERIMENTAL","RESTRICTED"))
if __name__=="__main__":unittest.main()
