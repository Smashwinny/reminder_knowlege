#!/usr/bin/env python3
"""公式与标签纪律的单元测试。使用固定合成输入，不读取原帖营收当实测。"""
import json
import math
import unittest
from pathlib import Path

import unit_econ as ue

HERE = Path(__file__).resolve().parent


class TestFormulas(unittest.TestCase):
    def test_funnel_counts(self):
        c = ue.funnel_counts(20000, 0.03, 0.08, 0.15)
        self.assertAlmostEqual(c["clicks"], 600.0)
        self.assertAlmostEqual(c["inquiries"], 48.0)
        self.assertAlmostEqual(c["paid"], 7.2)

    def test_unit_economics_hand_calc(self):
        out = ue.unit_economics(
            n_paid=10,
            price=100,
            refund_rate=0.10,
            fee_rate=0.05,
            delivery_cost_ratio=0.20,
            traffic_cost=80,
            fulfillment_per_order=2,
        )
        # revenue=1000, refunds=100, net=900, fees=45, delivery=180, fulfillment=10*0.9*2=18
        # contribution=900-45-180-18-80=577
        self.assertAlmostEqual(out["revenue"], 1000)
        self.assertAlmostEqual(out["refunds"], 100)
        self.assertAlmostEqual(out["net_revenue"], 900)
        self.assertAlmostEqual(out["fees"], 45)
        self.assertAlmostEqual(out["delivery"], 180)
        self.assertAlmostEqual(out["fulfillment"], 18)
        self.assertAlmostEqual(out["contribution"], 577)
        self.assertAlmostEqual(out["cac"], 8)
        self.assertAlmostEqual(out["contribution_margin"], 577 / 1000)
        self.assertAlmostEqual(out["contribution_per_order"], 57.7)

    def test_contribution_linear_in_traffic(self):
        a = ue.unit_economics(
            n_paid=5, price=100, refund_rate=0, fee_rate=0, delivery_cost_ratio=0, traffic_cost=0
        )
        b = ue.unit_economics(
            n_paid=5, price=100, refund_rate=0, fee_rate=0, delivery_cost_ratio=0, traffic_cost=40
        )
        self.assertAlmostEqual(a["contribution"] - b["contribution"], 40)

    def test_break_even_traffic_equals_zero_traffic_contribution(self):
        kwargs = dict(
            n_paid=8,
            price=200,
            refund_rate=0.05,
            fee_rate=0.06,
            delivery_cost_ratio=0.25,
            traffic_cost=123,
            fulfillment_per_order=0,
        )
        t_star = ue.break_even_traffic_cost(kwargs)
        zero = dict(kwargs)
        zero["traffic_cost"] = 0
        self.assertAlmostEqual(t_star, ue.unit_economics(**zero)["contribution"])
        at = dict(kwargs)
        at["traffic_cost"] = t_star
        self.assertAlmostEqual(ue.unit_economics(**at)["contribution"], 0.0, places=9)

    def test_break_even_close_rate_non_negative(self):
        rate = ue.break_even_close_rate(
            impressions=10000,
            ctr=0.02,
            inquiry_rate=0.1,
            price=3000,
            refund_rate=0.05,
            fee_rate=0.066,
            delivery_cost_ratio=0.25,
            cpc=1.5,
        )
        self.assertGreaterEqual(rate, 0)
        self.assertLessEqual(rate, 1)
        # just below should be negative or closer to zero from below; at rate should be >= 0
        def contrib(c):
            counts = ue.funnel_counts(10000, 0.02, 0.1, c)
            return ue.unit_economics(
                n_paid=counts["paid"],
                price=3000,
                refund_rate=0.05,
                fee_rate=0.066,
                delivery_cost_ratio=0.25,
                traffic_cost=counts["clicks"] * 1.5,
            )["contribution"]

        self.assertGreaterEqual(contrib(rate), -1e-6)
        if rate > 0:
            self.assertLess(contrib(max(0.0, rate - 1e-4)), 1e-3)

    def test_impossible_close_rate_is_inf(self):
        rate = ue.break_even_close_rate(
            impressions=1000,
            ctr=0.01,
            inquiry_rate=0.01,
            price=1,
            refund_rate=0.0,
            fee_rate=0.0,
            delivery_cost_ratio=0.0,
            cpc=1000,  # traffic cost dwarfs even 100% close
        )
        self.assertTrue(math.isinf(rate))

    def test_rejects_negative(self):
        with self.assertRaises(ue.AssumptionError):
            ue.unit_economics(
                n_paid=-1, price=1, refund_rate=0, fee_rate=0, delivery_cost_ratio=0, traffic_cost=0
            )
        with self.assertRaises(ue.AssumptionError):
            ue.funnel_counts(10, -0.1, 0.1, 0.1)

    def test_assumptions_all_tagged(self):
        data = ue.load_assumptions()
        for section in ("funnel_teaching", "economics"):
            for key, item in data[section].items():
                self.assertIn("value", item, key)
                self.assertIn("source", item, key)
                self.assertIn(item["source"], {"author_claim", "author_claim_derived", "teaching_assumption"})

    def test_claimed_aov_matches_division(self):
        data = ue.load_assumptions()
        gmv, src_g, _ = ue.field(data["economics"], "claimed_year_gmv")
        orders, src_o, _ = ue.field(data["economics"], "claimed_year_orders")
        aov, src_a, _ = ue.field(data["economics"], "custom_aov_from_claim")
        self.assertEqual(src_g, "author_claim")
        self.assertEqual(src_o, "author_claim_derived")
        self.assertEqual(src_a, "author_claim_derived")
        self.assertAlmostEqual(aov, gmv / orders)

    def test_sensitivity_identity_at_zero_delta(self):
        kwargs = dict(
            n_paid=7.2,
            price=3000,
            refund_rate=0.05,
            fee_rate=0.066,
            delivery_cost_ratio=0.25,
            traffic_cost=900,
            fulfillment_per_order=0,
        )
        base = ue.unit_economics(**kwargs)
        rows = ue.sensitivity_table(kwargs, {"price": 3000}, deltas=(0.0,))
        self.assertAlmostEqual(rows[0]["contribution"], base["contribution"])
        self.assertAlmostEqual(rows[0]["contribution_change"], 0)

    def test_investment_not_in_unit_econ_signature(self):
        # 融资不是 unit_economics 的参数，防止有人把它加进贡献利润
        import inspect
        sig = inspect.signature(ue.unit_economics)
        self.assertNotIn("investment", sig.parameters)
        self.assertNotIn("gmv", sig.parameters)


if __name__ == "__main__":
    unittest.main(verbosity=2)
