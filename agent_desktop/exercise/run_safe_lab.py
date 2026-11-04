#!/usr/bin/env python3
"""No-desktop checks: run only version/skills and inspect pinned source contracts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

EXERCISE = Path(__file__).resolve().parent
PROJECT = EXERCISE.parent
REPO = PROJECT / "repo"
RESULTS = EXERCISE / "results"
BINARY = EXERCISE / "runtime/node_modules/agent-desktop/bin/agent-desktop"
STATE = EXERCISE / "state"
HOME = EXERCISE / "home"
EXPECTED_COMMIT = "6660fbac768dc7e7332837b90ed465684859afa3"


def isolated_environment() -> dict[str, str]:
    """Defense in depth only; command-path source checks prove no adapter call."""
    env = os.environ.copy()
    for name in ("DISPLAY", "WAYLAND_DISPLAY", "DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"):
        env.pop(name, None)
    env["HOME"] = str(HOME)
    env["AGENT_DESKTOP_HOME"] = str(STATE)
    return env


def run_cli(arguments: list[str]) -> dict:
    """Only version/skills may be passed: all other commands can probe the desktop."""
    if arguments != ["version"] and arguments[:2] != ["skills", "get"]:
        raise AssertionError(f"Refusing adapter-bound command in no-desktop lab: {arguments!r}")
    completed = subprocess.run(
        [str(BINARY), *arguments],
        env=isolated_environment(),
        text=True,
        capture_output=True,
        timeout=15,
        check=False,
    )
    try:
        envelope = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError(f"stdout is not one JSON envelope: {completed.stdout!r}") from error
    assert completed.stderr == "", completed.stderr
    return {"kind": "cli", "arguments": arguments, "exit_code": completed.returncode, "envelope": envelope}


def source_check(name: str, requirements: dict[str, list[str]]) -> dict:
    files = []
    for relative, markers in requirements.items():
        path = REPO / relative
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            require(marker in text, f"{relative}: missing source marker {marker!r}")
        files.append({
            "path": relative,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "matched_markers": markers,
        })
    main = (REPO / "src/main.rs").read_text(encoding="utf-8")
    version_branch = main.index("Commands::Version =>")
    skills_branch = main.index("Commands::Skills(a) =>")
    adapter_branch = main.index("cmd => {", skills_branch)
    require(version_branch < skills_branch < adapter_branch, "version/skills must bypass adapter dispatch")
    if name.startswith("snapshot-qualified"):
        permission = main.index("adapter.permission_report(deadline)")
        preflight = main.index("command_policy::preflight(&cmd, &report)?;")
        require(permission < preflight, "Linux permission probing happens before ref preflight")
    return {"kind": "pinned_source", "check": name, "files": files, "passed": True}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(BINARY.is_file(), "Run the local npm install described in exercise/README.md first")
    require(not BINARY.is_symlink(), "The lab expects the packaged native executable")
    require((REPO / ".git").exists(), "Clone the pinned official source described in exercise/README.md")
    revision = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        text=True, capture_output=True, timeout=15, check=True,
    ).stdout.strip()
    require(revision == EXPECTED_COMMIT, f"Unexpected source revision: {revision}")
    STATE.mkdir(mode=0o700, exist_ok=True)
    HOME.mkdir(mode=0o700, exist_ok=True)
    STATE.chmod(0o700)
    HOME.chmod(0o700)
    require(stat.S_IMODE(STATE.stat().st_mode) == 0o700, "State root must be private")

    version = run_cli(["version"])
    require(version["exit_code"] == 0 and version["envelope"]["ok"] is True, "version failed")
    require(version["envelope"]["data"]["version"] == "1.1.0", "Unexpected CLI version")
    require(version["envelope"]["version"] == "2.6", "Unexpected envelope version")

    skills = []
    for name, minimum_chars in (("desktop", 6000), ("platform", 15000)):
        result = run_cli(["skills", "get", name])
        require(result["exit_code"] == 0 and result["envelope"]["ok"] is True, f"skill {name} failed")
        content = result["envelope"]["data"]["content"]
        require(len(content) >= minimum_chars, f"skill {name} is unexpectedly short")
        result["envelope"]["data"]["content"] = {
            "characters": len(content),
            "sha256": hashlib.sha256(content.encode()).hexdigest(),
        }
        skills.append(result)

    refs = source_check("snapshot-qualified refs and pre-action ordering", {
        "crates/core/src/refs/ref_token.rs": [
            "ref_id.strip_prefix('@')",
            'rsplit_once(":e")',
            "validate_snapshot_id(snapshot_id)?;",
            "if !is_local_ref(&local_ref)",
        ],
        "src/main.rs": ["adapter.permission_report(deadline)", "command_policy::preflight(&cmd, &report)?;"],
        "crates/linux/src/system/permissions/mod.rs": ["bus", "probe_registry"],
    })
    policies = source_check("headless policy and retry semantics", {
        "crates/core/src/actions/interaction_policy.rs": [
            "allow_focus_steal: false",
            "allow_cursor_move: false",
        ],
        "crates/core/src/actions/delivery_semantics.rs": [
            "Self::NotDelivered => RetryDisposition::Safe",
            "Self::Unknown => RetryDisposition::Unknown",
            "RetryDisposition::Unsafe",
        ],
    })

    report = {
        "schema": 2,
        "binary": "agent-desktop 1.1.0 / envelope 2.6",
        "binary_sha256": hashlib.sha256(BINARY.read_bytes()).hexdigest(),
        "source_revision": revision,
        "desktop_access": "not exercised: only version/skills CLI branches execute; adapter-bound commands are forbidden by the harness",
        "executed_cli_commands": ["version", "skills get desktop", "skills get platform"],
        "forbidden_cli_commands": "all snapshot/status/action/window/input/clipboard commands",
        "environment_note": "session variables are removed only as defense in depth, not as proof of desktop isolation",
        "state_root": "exercise/state (mode 0700)",
        "checks": [version, *skills, refs, policies],
        "passed": 5,
    }
    RESULTS.mkdir(exist_ok=True)
    output = RESULTS / "safe-lab.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "passed": 5, "output": str(output), "desktop_commands": "version_and_skills_only"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
