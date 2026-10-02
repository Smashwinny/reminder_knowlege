# -*- coding: utf-8 -*-
"""Demo: drive the implemented 11-768 ReAct harness offline.

A scripted stand-in plays the LLM (no network, no API key), a fake
environment plays the sandbox. Shows:
  1. the ReAct loop (action -> observation -> next prompt)
  2. observation truncation of a 26,000-char output
  3. progressive skill disclosure (catalog in prompt, body only on invoke)
  4. context compaction (working memory replaces the old raw prefix)

Usage: run from repo root with PYTHONPATH=src
  .venv/Scripts/python ../exercise/demo_react_loop.py
"""

import json
import os
import string
import sys
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "demo-not-a-real-key")
os.environ.setdefault("OPENAI_BASE_URL", "http://localhost:0/v1")
os.environ.setdefault("OPENAI_MODEL", "scripted")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "repo" / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from openai.types.chat import ChatCompletion  # noqa: E402

from assignment.agent import CodeAgent, StepLimitError  # noqa: E402

LONG_FILE = "".join(letter * 1000 for letter in string.ascii_lowercase)  # 26,000
OUTPUTS = {
    "cat f.txt": LONG_FILE,
    "ls -la": "total 4\ndrwxr-xr-x 2 root root 4096 Jan  1 00:00 .\n",
    "python hello.py": "hello, world\n",
}


class FakeEnvironment:
    cwd = "/testbed"
    system, release, version, machine = "Linux", "6.1.0", "#1 SMP", "x86_64"

    def __init__(self):
        self.commands = []

    def execute(self, command, **kwargs):
        self.commands.append(command)
        return {"output": OUTPUTS.get(command, ""), "returncode": 0}


def action(call_id, name, arguments, content="Thinking..."):
    return {
        "role": "assistant",
        "content": content,
        "tool_calls": [
            {
                "id": call_id,
                "type": "function",
                "function": {"name": name, "arguments": arguments},
            }
        ],
    }


def completion(message):
    return ChatCompletion.model_validate(
        {
            "id": "demo",
            "object": "chat.completion",
            "created": 0,
            "model": "scripted",
            "choices": [{"index": 0, "finish_reason": "tool_calls", "message": message}],
        }
    )


def tokens(messages):
    return len(json.dumps(messages, ensure_ascii=False)) // 4


SCRIPT = [
    action("call_1", "execute", json.dumps({"command": "cat f.txt"}),
           "First, inspect the big generated file."),
    action("call_2", "execute", json.dumps({"command": "ls -la"}),
           "Now list the directory."),
    action("call_3", "execute", json.dumps({"command": "python hello.py"}),
           "Run the script."),
    action("call_4", "invoke_skill", json.dumps({"name": "submit-task"}),
           "Task looks done; load the submission skill."),
    action("call_5", "send_message", json.dumps({"summary": "hello.py prints hello, world; task complete."}),
           "Submitting."),
]

env = FakeEnvironment()
agent = CodeAgent(
    "print hello, world to the terminal",
    env,
    model="scripted",
    logs_save_path="demo_trajectory.json",
    step_limit=8,
    skills_path="../repo/tasks/code-skills/",
    compact_threshold_tokens=600,
    compaction_keep_recent_steps=1,
)

plan = list(SCRIPT)


def scripted_create(**kwargs):
    if "tools" not in kwargs:  # compaction request
        print(f"  [compaction] prompt tokens ~= {tokens(kwargs['messages'])} -> summarize old steps")
        return completion({
            "role": "assistant",
            "content": "Inspected a 26k-char generated file (letters a-z x1000). "
                       "Ran ls and hello.py; hello.py prints 'hello, world'. "
                       "Next: submit via the submit-task skill.",
        })
    return completion(plan.pop(0))


agent.client.chat.completions.create = scripted_create

print("=== system prompt (first 500 chars) ===")
print(agent.system_prompt[:500])
print("...")
print("\n=== progressive disclosure check ===")
flat = json.dumps(agent.build_prompt(), ensure_ascii=False)
print("catalog names submit-task in prompt:", "submit-task" in flat)
print("skill body (patch.txt) hidden until invoked:", "patch.txt" not in flat)

print("\n=== run ===")
try:
    agent.run()
except StepLimitError as exc:
    print("stopped:", exc)

print("\n=== trajectory ===")
for i, prompt in enumerate(agent.api_prompts, 1):
    print(f"step {i}: prompt tokens ~= {tokens(prompt)}")
print("commands executed:", env.commands)
print("compaction events:", len(agent.compaction_events))
for event in agent.compaction_events:
    print(f"  compaction at step {event['step']}: "
          f"{event['estimated_tokens_before']} -> {event['estimated_tokens_after']} tokens (rough)")
final = agent.build_prompt()
print("long file content absent from final prompt:", "aaaaaaaa" not in json.dumps(final))
print("summary present in final prompt:", "working_memory" in json.dumps(final))
print("trajectory saved:", Path("demo_trajectory.json").exists())
