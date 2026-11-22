import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("rss_companion_demo.py")
SPEC = importlib.util.spec_from_file_location("rss_companion_demo", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
FIXTURE = MODULE_PATH.with_name("fixtures") / "python-insider-sample.xml"


class RssScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feed = MODULE.parse_feed(FIXTURE.read_bytes())
        cls.content = MODULE.clean_markup(cls.feed["items"][0]["description"])

    def test_parses_five_synthetic_items(self):
        self.assertEqual(len(self.feed["items"]), 5)
        self.assertIn("合成离线夹具", self.feed["title"])

    def test_long_background_is_explicitly_truncated(self):
        scope = MODULE.build_scope(self.content, 1500)
        self.assertGreater(scope["total_chars"], 1500)
        self.assertEqual(len(scope["background"]), 1500)
        self.assertTrue(scope["truncated"])

    def test_short_background_is_complete(self):
        scope = MODULE.build_scope("短合成内容", 1500)
        self.assertEqual(scope["background"], "短合成内容")
        self.assertFalse(scope["truncated"])

    def test_selection_is_real_source_text(self):
        scope = MODULE.build_scope(self.content, 1500)
        self.assertGreater(scope["selected_chars"], 40)
        self.assertIn(scope["selected"], self.content)

    def test_smaller_limit_reports_exact_counts(self):
        scope = MODULE.build_scope(self.content, 100)
        self.assertEqual((len(scope["background"]), scope["total_chars"], scope["truncated"]),
                         (100, len(self.content), True))

    def test_invalid_limit_fails_closed(self):
        with self.assertRaises(ValueError):
            MODULE.build_scope(self.content, 0)


if __name__ == "__main__":
    unittest.main()
