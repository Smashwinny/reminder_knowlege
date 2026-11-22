import unittest

from graph_eval_lab import (
    Candidate,
    ALLOWED_PATH,
    REQUIRED_SOURCE,
    course_should_continue,
    evaluate,
    run_scenario,
)


class CourseStoppingRuleTests(unittest.TestCase):
    def test_equal_revision_count_continues(self):
        self.assertEqual(course_should_continue(2, 2), "reflect")

    def test_greater_revision_count_ends(self):
        self.assertEqual(course_should_continue(3, 2), "end")


class GraphEvaluationTests(unittest.TestCase):
    def test_clean_stops_on_verified_success(self):
        result = run_scenario("clean")
        self.assertEqual((result.status, result.stop_reason, result.attempts),
                         ("PASS", "VERIFIED_SUCCESS", 1))

    def test_repairable_failure_converges_on_second_draft(self):
        result = run_scenario("repair")
        self.assertEqual((result.status, result.stop_reason, result.attempts),
                         ("PASS", "VERIFIED_SUCCESS", 2))
        self.assertEqual(result.events[1]["outcome_errors"],
                         ["MISSING_DATE", "MISSING_OWNER", "MISSING_SOURCE"])

    def test_repeated_draft_stops_as_stagnant_before_budget(self):
        result = run_scenario("stagnant", max_attempts=5)
        self.assertEqual((result.status, result.stop_reason, result.attempts),
                         ("FAIL", "STAGNANT", 2))

    def test_distinct_failures_exhaust_exact_budget(self):
        result = run_scenario("budget", max_attempts=3)
        self.assertEqual((result.status, result.stop_reason, result.attempts),
                         ("FAIL", "BUDGET_EXHAUSTED", 3))

    def test_evaluator_tampering_is_immediate_hard_failure(self):
        result = run_scenario("tamper", max_attempts=5)
        self.assertEqual((result.status, result.stop_reason, result.attempts),
                         ("FAIL", "HARD_FAILURE", 1))

    def test_claimed_done_is_not_acceptance_evidence(self):
        candidate = Candidate(
            "Launch Tuesday; owner Maya.",
            (REQUIRED_SOURCE,),
            (ALLOWED_PATH,),
            claimed_done=False,
        )
        self.assertTrue(evaluate(candidate)["passed"])

    def test_invalid_budget_is_rejected(self):
        with self.assertRaises(ValueError):
            run_scenario("clean", max_attempts=0)


if __name__ == "__main__":
    unittest.main()
