import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("space_export.py")
SPEC = importlib.util.spec_from_file_location("space_export", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
DOCUMENT = MODULE_PATH.with_name("space-demo.html").read_text(encoding="utf-8")


class SpaceExportTests(unittest.TestCase):
    def setUp(self):
        self.exported = MODULE.export_document(DOCUMENT)

    def test_six_blocks_preserved_in_order(self):
        self.assertEqual(self.exported.count("\n\n"), 5)
        self.assertLess(self.exported.index("# 季度选题复盘"), self.exported.index("```viz"))
        self.assertLess(self.exported.index("```viz"), self.exported.index("引用行"))
        self.assertLess(self.exported.index("引用行"), self.exported.index("附件引用"))

    def test_viz_is_explicit_static_placeholder(self):
        self.assertIn("本地模拟：静态导出仅保留占位", self.exported)

    def test_reference_does_not_claim_live_context(self):
        self.assertIn("不带实时聊天上下文", self.exported)

    def test_attachment_is_not_copied(self):
        self.assertIn("未复制或修改原文件", self.exported)

    def test_source_is_not_modified(self):
        before = MODULE_PATH.with_name("space-demo.html").read_bytes()
        MODULE.export_document(DOCUMENT)
        self.assertEqual(MODULE_PATH.with_name("space-demo.html").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
