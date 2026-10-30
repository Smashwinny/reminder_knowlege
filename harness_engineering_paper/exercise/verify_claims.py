# -*- coding: utf-8 -*-
"""Harness Engineering 论文宣称核对器 —— 学习实验。

对论文（arXiv:2609.00006v1，CC BY 4.0，本机已存 paper.html）的宣称逐条
用纯文本证据核对，输出证据行号与上下文：
  T1 论文拆解 11 个生产级 harness + Omnigent 元对照
  T2 七个子系统（Loop/LLM集成/工具/记忆上下文/安全/编排/扩展）+ Table 1 最小/最大实现
  T3 双缺席：无一用 agentic 框架（LangChain/LangGraph/AutoGen 等，Gemini CLI 连自家都不用）
  T4 双缺席之二：无一代码检索用向量嵌入（field runs on ripgrep/tree-sitter/glob）
  T5 扩展标准：SKILL.md 9/11 领先 MCP 8/11；ACP 6 系统
  T6 极小存在证明：Mini-SWE-Agent ~100 行实现全部七子系统
  T7 方法论声明：不 benchmark 不排名，只描述比较；13 条横切观察 + 29 个设计模式目录

用法： python verify_claims.py
"""
import re
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parent / "paper.html"

text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", PAPER.read_text(encoding="utf-8", errors="ignore")))
text = text.replace("&amp;", "&")

ELEVEN = ["Claude Code", "Codex CLI", "Gemini CLI", "Mistral Vibe", "OpenHands",
          "Aider", "Mini-SWE-Agent", "Hermes", "Pi", "OpenCode", "OpenClaw"]


def has(needle, near=None, window=400):
    if near is None:
        return needle.lower() in text.lower()
    i = text.lower().find(near.lower())
    return i >= 0 and needle.lower() in text[i:i + window].lower()


def main():
    cases = []

    def check(name, ok, detail):
        print(f"  {'✅' if ok else '❌'} {name}: {detail}")
        cases.append(ok)

    # T1 eleven systems
    found = [s for s in ELEVEN if s in text]
    omni = "Omnigent" in text and "meta-harness" in text
    check(f"T1 十一系统 {len(found)}/11 + Omnigent={omni}",
          len(found) == 11 and omni, ",".join(found[:5]) + "…")

    # T2 seven subsystems + minimal/maximal mapping
    seven = ["Agent loop", "LLM integration", "Tools", "Memory & context",
             "Safety", "Orchestration", "Extensibility"]
    hits = [s for s in seven if s.lower() in text.lower()]
    minimal_ok = "Mini-SWE-Agent : a linear while over one bash tool" in text
    maximal_ok = "event-sourced conversation" in text
    check(f"T2 七子系统 {len(hits)}/7 + Table1 最小/最大实现",
          len(hits) == 7 and minimal_ok and maximal_ok,
          f"minimal(mini-swe linear while)={minimal_ok}, maximal(OpenHands event-sourced)={maximal_ok}")

    # T3 no agentic frameworks
    check("T3 双缺席1：无 agentic 框架",
          "no agent runtime imports a general-purpose agentic framework" in text
          and "LangChain" in text and "Gemini CLI uses neither" in text,
          "原句命中（含 Gemini CLI 不用自家框架）")

    # T4 no vector retrieval
    check("T4 双缺席2：无向量代码检索",
          "none retrieves code with vector embeddings" in text
          and "ripgrep" in text and "tree-sitter" in text,
          "原句命中（deterministic retrieval: ripgrep/tree-sitter/glob）")

    # T5 extensibility standards
    check("T5 SKILL.md 9/11 领先 MCP 8/11；ACP 6 系统",
          "SKILL.md skills lead MCP in adoption (9/11 vs. 8/11)" in text
          and "ACP ships in six systems" in text,
          "原句命中")

    # T6 minimal harness
    check("T6 Mini-SWE-Agent ~100 行七子系统存在证明",
          "implements all seven subsystems in roughly 100 lines" in text
          and "SWE-bench Verified" in text,
          "原句命中（floor is low）")

    # T7 methodology
    check("T7 不 benchmark 不排名；13 观察 + 29 模式",
          "It does not benchmark or rank" in text
          and "13 cross-cutting observations" in text
          and "29 recurring design patterns" in text,
          "原句命中")

    passed = sum(cases)
    print(f"\n核对结果：{passed}/{len(cases)} 通过")
    return passed == len(cases)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
