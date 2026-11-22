import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("route_contract.py")
SPEC = importlib.util.spec_from_file_location("route_contract", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RouteContractTests(unittest.TestCase):
    def test_three_distinct_routes(self):
        self.assertEqual(set(MODULE.ROUTES), {"CLI", "MCP", "GUI"})
        self.assertNotEqual(MODULE.validate_route("CLI")["evidence"], MODULE.validate_route("GUI")["evidence"])

    def test_unlimited_assumption_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.validate_route("CLI", unlimited=True)

    def test_unknown_route_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.validate_route("MAGIC")

    def test_budget_stops_before_negative_balance(self):
        guard = MODULE.BudgetGuard(500)
        self.assertTrue(guard.reserve(120))
        self.assertTrue(guard.reserve(120))
        self.assertFalse(guard.reserve(300))
        self.assertEqual(guard.balance, 260)

    def test_nonpositive_estimate_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.BudgetGuard(500).reserve(0)

    def test_only_success_allows_asset_review(self):
        task = MODULE.GenericTask()
        task.advance("running")
        task.advance("succeeded")
        task.review_assets()
        self.assertTrue(task.assets_reviewed)

    def test_failed_task_cannot_review_assets(self):
        task = MODULE.GenericTask()
        task.advance("running")
        task.advance("failed")
        with self.assertRaises(ValueError):
            task.review_assets()

    def test_terminal_state_cannot_reopen(self):
        task = MODULE.GenericTask()
        task.advance("running")
        task.advance("succeeded")
        with self.assertRaises(ValueError):
            task.advance("running")


if __name__ == "__main__":
    unittest.main()
