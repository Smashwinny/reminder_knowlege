---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/crewAIInc/crewAI
完成日期: 2026-10-01
---

# crewAI

**这是什么**（一句话）：开源 Python 多智能体编排框架——给每个 AI 写岗位说明书（Agent）、派工单（Task）、串流水线（Crew），或用事件驱动的 Flow 做确定性控制。

**它给我什么能力**：
- 十几行代码搭"研究→写作→审校"式 AI 工作组，无需手写编排代码
- 继承 BaseTool 给 Agent 发工具（查库/调 API/读文件）
- litellm 统一网关：GLM/GPT/Claude/Ollama 改个模型名全队换装
- expected_output / output_pydantic 让产出格式可验收
- Flow（@start/@listen/@router 状态机）+ 内嵌 Crew = 生产级架构

**引入的概念**：
- [[多智能体协作]]、[[角色提示]]（本项目新立）
- 复用合并：[[Agent循环]]（=ReAct，langchain 已立）、[[LLM工具调用]]（langchain 已立）、[[RAG检索增强生成]]（Knowledge/Memory）
- 对照：[[LangGraph与Agent编排]]、[[构建流水线与Pass]]、[[确定性脚本]]

**实验记录**（做了什么、结果、坑）：
全部实验在 exercise/first_crew/，模型走 Z.ai Anthropic 兼容中转（GLM-4.6），四步全部实测通过：
1. step2_crew.py：研究员→撰稿人 sequential 流水线 ✅（产出 200 字大白话介绍，成品质量好）
2. step3_role_change.py：改 role 为"武侠小说家"看人格切换 ✅
3. step4_tool.py：自定义菜单工具（假数据库）✅（日志 Tool Output 出现菜价，推荐正确）
4. step5_flow.py：@start/@listen Flow 零 LLM 调用跑通 ✅

**坑与结论**：
- crewAI 要求 Python >=3.10,<3.14，系统 3.14 不行 → `py -3.12 -m venv`
- 1.x 起 litellm 是可选依赖 → 装 `"crewai[litellm]"`，否则接第三方模型 ImportError
- 中文 Windows GBK 控制台打印 emoji 日志报错/乱码 → `sys.stdout.reconfigure(encoding="utf-8")` + PYTHONUTF8=1
- Z.ai 中转限流（1302）→ 多实验并行会撞车，串行跑即可；限流重试耗尽会触发框架内 asyncio 报错（Task Failed），重跑即好

**后续可深入的方向**：
- hierarchical 模式 + manager_llm（经理 Agent 验收）
- output_pydantic 结构化输出接下游程序
- 用 Flow+重做 img2threejs 式任务拆解（对照 [[构建流水线与Pass]]）
- crewai create crew 的 JSONC 项目脚手架（agents/*.jsonc + crew.jsonc）
