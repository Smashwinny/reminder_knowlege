---
tags: [项目笔记, 提示词工程, 手绘风格, Agent Skill]
created: 2026-10-27
---
# hand-drawn-styles 手绘风格配方库

threerocks/hand-drawn-styles（MIT，main@5a2f91f）：23 种手绘风格提示词配方库，输出 prompt/JSON 调用包，不直接生成图像。

## 核心概念
- [[提示词配方真源（STYLES.md 模式）]]：单一 Markdown 真源，工具只机械提取，防止文档与实现漂移。
- [[槽位 fail-closed 渲染]]：缺必填槽位或未知画风即拒绝输出半成品。

## 实测
`check_skill.py` 输出 23 套配方、116 个别名、23 项完整调用通过；水墨、像素、蜡笔三套渲染成功。缺主色调等槽位和未知画风均明确报错。需锚图的 3.1/19/20/22 画风未验证。

注意：README About 的"5 种画风"与真源 23 种不一致，以 STYLES.md 和 main 版本为准。
