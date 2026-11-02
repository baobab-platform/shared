"""DEV-11 canonical OTel projection schema source tests; no runtime certification."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "contracts/observability/v1/dev11-trace-evidence.schema.json"
CORRELATION = "a1234567-89ab-cdef-0123-456789abcdef"
EVENT = "e1234567-89ab-cdef-0123-456789abcdef"


def fixture():
    ta, tb = "a"*32, "b"*32
    def ref(trace, span):
        return {"trace_id":trace,"span_id":f"{span:016x}"}
    def node(role, trace, span, parent, boundary="HTTP", links=None, event_id=None):
        return {"service_role":role,
                "traceparent":f"00-{trace}-{span:016x}-01",
                "parent":parent,"links":links or [],
                "correlation_id":CORRELATION,"boundary":boundary,
                "event_id":event_id,"result":"PASS","cause":"NONE"}
    return {"schema":"infrastructure.dev11.graph.v1",
            "source_sha":"c"*40,"profile":"DEV-07",
            "scenario":"DEV11-ASYNC-01","correlation_id":CORRELATION,
            "spans":[node("bff",ta,1,None),
                     node("issuer",ta,2,ref(ta,1)),
                     node("cp",ta,3,ref(ta,2)),
                     node("engine",ta,4,ref(ta,3)),
                     node("outbox",ta,5,ref(ta,4),"EVENT_PUBLISH",event_id=EVENT),
                     node("consumer",tb,1,None,"EVENT_CONSUME",[ref(ta,5)],EVENT)],
            "runtime_observed":True,"teardown_verified":True,
            "evidence_class":"REAL_COMPONENT_SYNTHETIC_DATA"}


class TraceSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def assert_rejected(self, transform):
        sample = fixture()
        transform(sample)
        self.assertFalse(self.validator.is_valid(sample))

    def test_closed_async_reference_projection(self):
        self.assertTrue(self.validator.is_valid(fixture()))

    def test_unknown_data_and_payload_fields_rejected(self):
        for change in (
            lambda x:x.update(authorization="Bearer secret"),
            lambda x:x["spans"][0].update(url="/customer@example.com"),
            lambda x:x["spans"][3].update(raw_body={"payment":"private"}),
            lambda x:x["spans"][5].update(headers={"cookie":"session=secret"}),
        ):
            with self.subTest(change=change):
                self.assert_rejected(change)

    def test_malformed_context_or_unknown_roles_rejected(self):
        for change in (
            lambda x:x["spans"][1].update(traceparent="00-invalid"),
            lambda x:x["spans"][1].update(service_role="privileged_admin"),
            lambda x:x["spans"][2]["parent"].update(trace_id="BAD"),
            lambda x:x["spans"][5].update(links=[{"trace_id":"a"*32,"span_id":"BAD"}]),
        ):
            self.assert_rejected(change)

    def test_message_boundary_and_event_identity_closed(self):
        for change in (
            lambda x:x["spans"][4].update(event_id=None),
            lambda x:x["spans"][5].update(event_id=None),
            lambda x:x["spans"][5].update(links=[]),
            lambda x:x["spans"][5].update(service_role="engine"),
            lambda x:x["spans"][0].update(event_id=EVENT),
        ):
            self.assert_rejected(change)

    def test_pass_cause_and_negative_statuses(self):
        self.assert_rejected(lambda x:x["spans"][3].update(result="PASS",cause="INCORRECT_RESULT"))
        self.assert_rejected(lambda x:x["spans"][3].update(result="FAIL",cause="NONE"))
        for status,cause in (("FAIL","INCORRECT_RESULT"),
                             ("BLOCKED","AUTHORITY_UNQUALIFIED"),
                             ("NOT_RUN","NOT_EXECUTED")):
            doc = fixture()
            doc["spans"][3].update(result=status,cause=cause)
            self.assertTrue(self.validator.is_valid(doc))

    def test_runtime_claims_cannot_create_acceptance_fields(self):
        self.assert_rejected(lambda x:x.update(runtime_qualified=True))
        self.assert_rejected(lambda x:x.update(production_authorized=True))
        self.assert_rejected(lambda x:x.update(protected_acceptance=True))

    def test_schema_has_explicit_semantic_verification_boundary(self):
        description=self.schema["description"]
        self.assertIn("verified separately",description)
        self.assertNotIn("runtime_qualified",self.schema["properties"])
        self.assertFalse(self.validator.is_valid({"schema":"infrastructure.dev11.graph.v1"}))


if __name__ == "__main__":
    unittest.main()
