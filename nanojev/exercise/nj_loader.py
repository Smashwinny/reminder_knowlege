# -*- coding: utf-8 -*-
"""共享加载器：在 RTX 4070 / torch 2.11 上加载 NanoJev checkpoint。

坑记录：repo 的 predict_toy_decisions.DecisionPredictor 在 disable_native_triton=True
时会 `from torch._native import triton_utils`（torch 2.14 才有的模块）。本机 torch 2.11
没有该模块，因此这里用 sys.modules 打桩替换（triton 覆盖注册在 2.11 里本就不存在，
deregister 是空操作，语义安全）。
"""
import sys
import types
from pathlib import Path

REPO_SCRIPTS = Path(__file__).resolve().parent.parent / "repo" / "scripts"
CHECKPOINT = Path(__file__).resolve().parent.parent / "repo" / "checkpoints" / "NanoJev-unified"
TEST_JSONL = Path(__file__).resolve().parent.parent / "repo" / "data" / "NanoJev-unified" / "unified" / "hard" / "test.jsonl"


def _stub_triton_utils():
    m = types.ModuleType("torch._native")
    tu = types.ModuleType("torch._native.triton_utils")
    tu.deregister_op_overrides = lambda: None
    m.triton_utils = tu
    sys.modules.setdefault("torch._native", m)
    sys.modules.setdefault("torch._native.triton_utils", tu)


def load_engine():
    _stub_triton_utils()
    sys.path.insert(0, str(REPO_SCRIPTS))
    from predict_toy_decisions import DecisionPredictor
    return DecisionPredictor(str(CHECKPOINT), precision="bf16", disable_native_triton=True)


def question_target(row):
    """返回 (目标动作字符串, 目标来源说明)。

    shooting（hard target=expert_action）→ metadata.conditioned_action；
    maze/snake（api_policy_distribution）→ teacher.native_probs 的 argmax。
    """
    meta = row["metadata"]
    if meta.get("task") == "shooting":
        return meta["conditioned_action"], "expert_action"
    probs = row["teacher"]["native_probs"]["action"]
    return max(probs, key=probs.get), "jev_api_argmax"


def shooting_subtask(row):
    return row["metadata"]["spec"]["scenario"]
