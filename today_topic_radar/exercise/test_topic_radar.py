import copy
import datetime
import importlib.util
import json
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("topic_radar.py")
SPEC = importlib.util.spec_from_file_location("topic_radar", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
FIXTURE = json.loads(MODULE_PATH.with_name("fixtures").joinpath("topic_candidates.json").read_text(encoding="utf-8"))
TODAY = datetime.date(2026, 11, 22)


class TopicRadarTests(unittest.TestCase):
    def evaluate(self, index):
        return MODULE.score(FIXTURE["candidates"][index], TODAY, FIXTURE["recent_topics"])

    def test_all_five_dimensions_present(self):
        evaluation = self.evaluate(0)
        self.assertEqual(evaluation["score"], 5)
        self.assertEqual([item[0] for item in evaluation["reasons"]],
                         ["时效", "目标受众", "直接信号", "标题脱水初筛", "叙事轮换"])

    def test_narrative_rotation_is_not_free_point(self):
        self.assertEqual(self.evaluate(1)["score"], 4)
        self.assertFalse(self.evaluate(1)["reasons"][4][1])

    def test_stale_candidate_loses_timeliness(self):
        self.assertEqual(self.evaluate(2)["score"], 4)
        self.assertFalse(self.evaluate(2)["reasons"][0][1])

    def test_hype_and_second_hand_source_lose_points(self):
        evaluation = self.evaluate(3)
        self.assertEqual(evaluation["score"], 3)
        self.assertFalse(evaluation["reasons"][2][1])
        self.assertFalse(evaluation["reasons"][3][1])

    def test_non_ai_audience_loses_only_audience_point(self):
        self.assertEqual(self.evaluate(4)["score"], 4)
        self.assertFalse(self.evaluate(4)["reasons"][1][1])

    def test_missing_date_fails_timeliness_closed(self):
        candidate = copy.deepcopy(FIXTURE["candidates"][0])
        del candidate["published_at"]
        evaluation = MODULE.score(candidate, TODAY, [])
        self.assertFalse(evaluation["reasons"][0][1])
        self.assertEqual(evaluation["score"], 4)

    def test_render_preserves_source_and_marks_draft(self):
        original = copy.deepcopy(FIXTURE["candidates"])
        document, _ = MODULE.render(FIXTURE["candidates"], TODAY, FIXTURE["recent_topics"])
        self.assertIn("只产草稿", document)
        self.assertIn("https://example.com/cache-cost-lab", document)
        self.assertIn("叙事轮换", document)
        self.assertEqual(FIXTURE["candidates"], original)


if __name__ == "__main__":
    unittest.main()
