"""Zero-dependency graph stopping/evaluation lab for the verified LangGraph course.

This is my own deterministic teaching experiment, not upstream course code and not
an LLM benchmark. It uses fixed candidate drafts so stopping and gate behavior can
be replayed without API keys.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

ALLOWED_PATH = "docs/launch-note.md"
REQUIRED_SOURCE = "runbook#launch"


def course_should_continue(revision_number: int, max_revisions: int) -> str:
    """Replica of the course Essay Writer routing predicate."""
    return "end" if revision_number > max_revisions else "reflect"


@dataclass(frozen=True)
class Candidate:
    summary: str
    sources: tuple[str, ...]
    changed_paths: tuple[str, ...]
    claimed_done: bool
    writes_evaluator: bool = False


@dataclass
class RunResult:
    scenario: str
    status: str
    stop_reason: str
    attempts: int
    events: list[dict[str, Any]] = field(default_factory=list)


def candidate_for(scenario: str, attempt: int) -> Candidate:
    good = Candidate(
        summary="Launch Tuesday; owner Maya.",
        sources=(REQUIRED_SOURCE,),
        changed_paths=(ALLOWED_PATH,),
        claimed_done=True,
    )
    if scenario == "clean":
        return good
    if scenario == "repair":
        if attempt == 1:
            return Candidate("Launch date pending.", (), (ALLOWED_PATH,), False)
        return good
    if scenario == "stagnant":
        return Candidate("Launch Tuesday; owner pending.", (), (ALLOWED_PATH,), True)
    if scenario == "budget":
        return Candidate(
            f"Launch Tuesday; owner pending; retry {attempt}.",
            (),
            (ALLOWED_PATH,),
            True,
        )
    if scenario == "tamper":
        return Candidate(
            "Launch Tuesday; owner Maya.",
            (REQUIRED_SOURCE,),
            ("exercise/evaluator.py",),
            True,
            writes_evaluator=True,
        )
    raise ValueError(f"unknown scenario: {scenario}")


def evaluate(candidate: Candidate) -> dict[str, Any]:
    """Evaluate outcome and trajectory separately; never trust claimed_done."""
    outcome_errors: list[str] = []
    trajectory_errors: list[str] = []
    hard_failures: list[str] = []

    if "Tuesday" not in candidate.summary:
        outcome_errors.append("MISSING_DATE")
    if "Maya" not in candidate.summary:
        outcome_errors.append("MISSING_OWNER")
    if REQUIRED_SOURCE not in candidate.sources:
        outcome_errors.append("MISSING_SOURCE")

    if candidate.changed_paths != (ALLOWED_PATH,):
        trajectory_errors.append("UNAPPROVED_PATH")
    if candidate.writes_evaluator:
        hard_failures.append("EVALUATOR_TAMPERING")

    return {
        "outcome_errors": outcome_errors,
        "trajectory_errors": trajectory_errors,
        "hard_failures": hard_failures,
        "passed": not (outcome_errors or trajectory_errors or hard_failures),
    }


def fingerprint(candidate: Candidate) -> str:
    payload = json.dumps(candidate.__dict__, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:12]


def run_scenario(scenario: str, max_attempts: int = 3) -> RunResult:
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    events: list[dict[str, Any]] = []
    seen: set[str] = set()

    for attempt in range(1, max_attempts + 1):
        candidate = candidate_for(scenario, attempt)
        digest = fingerprint(candidate)
        events.append(
            {
                "event": "draft",
                "scenario": scenario,
                "attempt": attempt,
                "fingerprint": digest,
                "claimed_done": candidate.claimed_done,
            }
        )
        verdict = evaluate(candidate)
        events.append({"event": "gate", "attempt": attempt, **verdict})

        if verdict["hard_failures"]:
            return RunResult(
                scenario, "FAIL", "HARD_FAILURE", attempt, events
            )
        if verdict["passed"]:
            return RunResult(
                scenario, "PASS", "VERIFIED_SUCCESS", attempt, events
            )
        if digest in seen:
            return RunResult(scenario, "FAIL", "STAGNANT", attempt, events)
        seen.add(digest)
        if attempt == max_attempts:
            return RunResult(
                scenario, "FAIL", "BUDGET_EXHAUSTED", attempt, events
            )
        events.append(
            {
                "event": "repair",
                "attempt": attempt,
                "feedback": verdict["outcome_errors"]
                + verdict["trajectory_errors"],
            }
        )

    raise AssertionError("unreachable bounded loop")


def emit(result: RunResult) -> None:
    for event in result.events:
        print(json.dumps(event, ensure_ascii=False, sort_keys=True))
    print(
        f"SUMMARY scenario={result.scenario} status={result.status} "
        f"stop={result.stop_reason} attempts={result.attempts}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=("all", "clean", "repair", "stagnant", "budget", "tamper"),
        default="all",
    )
    parser.add_argument("--max-attempts", type=int, default=3)
    args = parser.parse_args()
    scenarios = (
        ("clean", "repair", "stagnant", "budget", "tamper")
        if args.scenario == "all"
        else (args.scenario,)
    )
    for scenario in scenarios:
        emit(run_scenario(scenario, args.max_attempts))


if __name__ == "__main__":
    main()
