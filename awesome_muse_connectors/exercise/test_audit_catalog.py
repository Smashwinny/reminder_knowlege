import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("audit_catalog.py")
SPEC = importlib.util.spec_from_file_location("audit_catalog", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ROOT = MODULE_PATH.parents[1] / "repo" / "connectors"


class CatalogAuditTests(unittest.TestCase):
    def test_fixed_catalog_has_159_skill_files(self):
        result = MODULE.audit(ROOT)
        self.assertEqual(result["skill_files"], 159)
        self.assertEqual(result["connector_entries"], 158)
        self.assertEqual(result["expected_commit"], MODULE.EXPECTED_COMMIT)

    def test_anthropic_has_five_sections_and_is_draft(self):
        record = MODULE.inspect_skill(ROOT / "anthropic" / "SKILL.md")
        self.assertEqual(record["missing_sections"], [])
        self.assertEqual(record["maturity"], "draft")

    def test_draft_is_majority_not_execution_proof(self):
        result = MODULE.audit(ROOT)
        self.assertGreater(result["maturity_counts"].get("draft", 0), 80)
        self.assertIn("不证明整个连接器", result["scope"])

    def test_template_is_not_counted_as_connector(self):
        record = MODULE.inspect_skill(ROOT / "_template" / "SKILL.md")
        self.assertEqual(record["maturity"], "template")

    def test_missing_maturity_is_explicit(self):
        text = "## Auth\n## Operating Rules\n## Files\ncatalog_hosts: []\n"
        self.assertEqual(MODULE.maturity(text), "missing")

    def test_live_label_is_scoped_to_specific_commands(self):
        text = "## Maturity\n✅ Live-tested against real API on 2026-10-04: models only\n"
        self.assertEqual(MODULE.maturity(text), "live-tested-specific-commands")

    def test_records_do_not_copy_auth_or_file_contents(self):
        record = MODULE.inspect_skill(ROOT / "anthropic" / "SKILL.md")
        self.assertEqual(set(record), {"id", "missing_sections", "maturity"})


if __name__ == "__main__":
    unittest.main()
