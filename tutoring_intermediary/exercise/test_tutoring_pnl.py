import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("tutoring_pnl", Path(__file__).with_name("tutoring_pnl.py"))
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
SCENARIOS, break_even, pnl = MODULE.SCENARIOS, MODULE.break_even, MODULE.pnl


class TutoringPnlTests(unittest.TestCase):
    def test_first_month_scenarios(self):
        expected = [4936, 14072, 8386]
        for scenario, value in zip(SCENARIOS.values(), expected):
            self.assertEqual(pnl(month="first", **scenario)["月净利"], value)

    def test_renewal_excludes_one_time_commission_and_acquisition(self):
        result = pnl(month="renewal", **SCENARIOS["A 有场地"])
        self.assertEqual(result["中介费"], 0)
        self.assertEqual(result["获客"], 0)
        self.assertEqual(result["固定"], 4200)
        self.assertEqual(result["月净利"], -1464)

    def test_renewal_scenarios(self):
        self.assertEqual(pnl(month="renewal", **SCENARIOS["B 有场地翻倍"])["月净利"], 1272)
        self.assertEqual(pnl(month="renewal", **SCENARIOS["C 无场地"])["月净利"], 1986)

    def test_break_even_is_period_specific(self):
        self.assertEqual(break_even("first"), 5)
        self.assertEqual(break_even("renewal"), 16)

    def test_invalid_period_fails_closed(self):
        with self.assertRaises(ValueError):
            pnl(month="every-month", **SCENARIOS["A 有场地"])

    def test_negative_students_rejected(self):
        kwargs = dict(SCENARIOS["A 有场地"], students=-1)
        with self.assertRaises(ValueError):
            pnl(**kwargs)


if __name__ == "__main__":
    unittest.main()
