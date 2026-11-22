import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("static_dataflow_audit.py")
SPEC = importlib.util.spec_from_file_location("static_dataflow_audit", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DataflowAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = MODULE.scan(MODULE_PATH.parents[1] / "repo-manager")

    def test_daily_endpoint_marker_present(self):
        self.assertTrue(self.result["matches"]["daily-cloudcode-pa.googleapis.com"])

    def test_cloudcode_endpoint_marker_present(self):
        self.assertTrue(self.result["matches"]["cloudcode-pa.googleapis.com"])

    def test_sandbox_endpoint_marker_present(self):
        self.assertTrue(self.result["matches"]["cloudcode-pa.sandbox.googleapis.com"])

    def test_oauth_token_filename_marker_present_without_reading_token(self):
        self.assertTrue(self.result["matches"]["antigravity-oauth-token"])

    def test_license_marker_matches_cc_by_nc_sa(self):
        self.assertTrue(self.result["license_is_cc_by_nc_sa"])

    def test_scope_does_not_claim_runtime_proof(self):
        self.assertIn("不证明运行行为", self.result["scope"])


if __name__ == "__main__":
    unittest.main()
