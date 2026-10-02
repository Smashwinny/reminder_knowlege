---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/ikevss/wechat-ai-memory （README/Release 品牌名 LOGO127/wechat-ai-memory）
完成日期: 2026-10-03
拾遗任务: 1ae96a78-72fd-4ed8-9f38-0420e72b3cbf
---

# wechat-ai-memory（微信 AI 记忆库）

**这是什么**（一句话）：本地优先的开源 Windows 工具（MIT，v0.3.7-alpha，Python 3.11+ / PySide6 / Frida / ReportLab / faster-whisper），把 Windows 微信 4.x 聊天记录按会话/日期/关键词筛选后导出成 PDF + Markdown + 规范 JSON 三件套——目标是给 AI Agent 准备<b>可引用、可追溯的个人上下文记忆</b>，而非单纯备份聊天。

**它给我什么能力**：
- 给 Agent 补背景：新会话前把相关群聊筛出来导 JSON/MD 直接喂给模型，每条消息可回溯原文
- 自造对话语料：Version 1 JSON 格式简单，可手写虚构对话测试"聊天分析"想法，零隐私风险
- 项目复盘档案：带引用链（reply_to）的 PDF 归档材料
- 为记忆流水线备料：JSON 输出可被 Memmy 类系统摄入（见 [[个人记忆流水线]]）

**引入的概念**：
- [[进程取钥与副本解密]] — Frida attach 微信进程内存取钥，只在临时副本上解密（[[CleanRoom只读读取器]] 的对立路线）
- [[双数据源适配器隔离]] — wechat4_* 适配层与渲染导出解耦，JSON 备用入口给管线保活
- [[个人记忆流水线]] — 三个微信/记忆项目（本项目 × wechat-intelligence-hub × Memmy）的进料口-车间-仓库三层定位

**实验做了什么**（exercise\，全程未连真实微信，只用官方 demo_chat.json + 自造 my_chat.json）：
1. 最小环境（Pillow+reportlab+zstandard+pycryptodome，不装 Frida/whisper）→ CLI 列出样例 2 会话
2. 三格式导出 eco-project：2 页 8 消息 1 图片页，PDF 目检气泡/引用框/系统消息/300DPI 附件页齐全
3. `--query 过拟合` 关键词筛选：8 条精确命中 1 条
4. 自造 my_chat.json（虚构群聊+私聊，含 reply_to 链、system 消息、Pillow 画的附件图）→ 同管线导出成功，日期过滤/引用链无损
5. 体检规范化 JSON 六要素契约：id/sender/timestamp/type/content/is_outgoing/reply_to 全在

**坑与结论**：
- 包 `__init__.py` 连带 import 微信适配层 → JSON 入口也必须装 zstandard + pycryptodome（ModuleNotFoundError: zstandard）
- `kind` 只认 `direct`/`group`，写 `private` 被确定性护栏拒收（报错清晰）
- JSON 字符串内嵌 ASCII 双引号必须转义（用「」最省事）
- 语音转写首次需联网下载约 500MB whisper small 模型；AI 问答/RAG/OCR/MCP 全部未实现（v0.4~v0.8 路线图）
- 结论：数据层（进料口）已扎实可信，"变成真 Agent 记忆"的最后一公里（检索+MCP）还在路上；与 [[CleanRoom只读读取器]] 路线之争的关键差异是"自动化 vs 不碰进程"，隐私底线一致

**产出**：`wechat-ai-memory/wechat-ai-memory-小白指南.pdf`（彩色图文，10 疑问 + 5 步实验）

**首次接触于**：拾遗队列 task 1ae96a78（Denzii 推文推荐）
