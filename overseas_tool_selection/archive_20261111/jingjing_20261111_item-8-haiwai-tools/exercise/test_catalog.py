#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class TestCatalog(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((HERE / "tools.json").read_text(encoding="utf-8"))
        self.tools = self.data["tools"]

    def test_missing_number_fourteen(self):
        missing = [t for t in self.tools if t["article_no"] == "14"]
        self.assertEqual(len(missing), 1)
        self.assertIsNone(missing[0]["official_url"])
        self.assertEqual(missing[0]["confidence"], "missing")

    def test_number_53_appears_twice_as_different_tools(self):
        names = [t["name"] for t in self.tools if t["article_no"] in {"53", "53-early"}]
        self.assertIn("Fiverr", names)
        self.assertIn("Feedlog", names)

    def test_adsy_is_in_chapter_two(self):
        adsy = next(t for t in self.tools if t["name"] == "Adsy")
        self.assertTrue(adsy["chapter"].startswith("二"))

    def test_customer_is_inferred(self):
        c = next(t for t in self.tools if t["name"] == "Customer")
        self.assertEqual(c["confidence"], "inferred")
        self.assertIn("customer.io", c["official_url"])

    def test_no_referral_in_probe_urls(self):
        blob = json.dumps(self.data, ensure_ascii=False).lower()
        # 目录说明可以提到「不使用推荐码」，但 official_url 本身禁止带邀请参数
        for t in self.tools:
            url = (t["official_url"] or "").lower()
            self.assertNotIn("mppk02p", url)
            self.assertNotIn("invitecode", url)
            self.assertNotIn("invite_code", url)

    def test_probe_results_if_present(self):
        path = HERE / "url-probe-results.json"
        if not path.exists():
            self.skipTest("探测尚未运行")
        results = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("checked_at", results)
        self.assertTrue(results["checked_at"].endswith("Asia/Shanghai") or "Asia/Shanghai" in results["checked_at"])
        # 缺号项不应被当成可达
        fourteen = next(r for r in results["rows"] if r["article_no"] == "14")
        self.assertEqual(fourteen["classification"], "原文缺号未探测")
        # 独立文章链接按 API 预期可能是 404，若探测结果不同也必须被记录
        article = next(r for r in results["rows"] if r["article_no"] == "article-id")
        self.assertIsNotNone(article["result"]["status"] or article["result"]["error"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
