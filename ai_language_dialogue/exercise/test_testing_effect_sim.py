import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("testing_effect_sim.py")
SPEC = importlib.util.spec_from_file_location("testing_effect_sim", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
simulate = MODULE.simulate


class TestingEffectModelTests(unittest.TestCase):
    def test_default_output_is_deterministic(self):
        first = simulate("restudy")
        second = simulate("restudy")
        self.assertEqual(first, second)
        self.assertEqual(round(first, 3), 0.217)
        self.assertEqual(round(simulate("test"), 3), 0.350)

    def test_result_is_probability(self):
        for mode in ["restudy", "test"]:
            result = simulate(mode, n=100)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 1)

    def test_advantage_is_parameter_assumption_not_discovery(self):
        stronger_test = simulate("test", test_success_gain=1.45, test_failure_gain=1.1)
        weaker_test = simulate("test", test_success_gain=1.0, test_failure_gain=0.5)
        self.assertNotEqual(stronger_test, weaker_test)

    def test_model_can_reverse_direction_under_other_assumptions(self):
        restudy = simulate("restudy")
        testing = simulate("test", test_success_gain=1.0, test_failure_gain=0.5)
        self.assertLessEqual(testing, restudy)

    def test_zero_delay_decay_forces_zero_recall(self):
        self.assertEqual(simulate("test", delay_decay=0), 0)

    def test_invalid_mode_fails_closed(self):
        with self.assertRaises(ValueError):
            simulate("watch")

    def test_invalid_sample_size_fails_closed(self):
        with self.assertRaises(ValueError):
            simulate("test", n=0)

    def test_invalid_decay_fails_closed(self):
        with self.assertRaises(ValueError):
            simulate("test", delay_decay=1.1)


if __name__ == "__main__":
    unittest.main()
