---
tags: [项目笔记]
项目: nihaixia_tcm_skill
类别: 开源项目类（AI Agent Skill / 领域知识包）
完成日期: 2026-10-02
来源: 拾遗队列 task 1787578542746（x.com 推文）
---

# nihaixia_tcm_skill — 倪海厦中医 Agent Skill

## 这是什么
[jangviktor-web/nihaixia](https://github.com/jangviktor-web/nihaixia)（v2.3.1，MulanPSL-2.0，约 3.4k stars，基于 huoyalong/nihaisha-skill 二次开发）：把倪海厦（1954-2012）的教学体系（伤寒论/金匮/内经/本草/医案/讲义，README 宣称 2452 页）整理成 Claude Code 等 Agent 可加载的 **Agent Skill**，用激活词（倪海厦/海厦视角/倪师/经方思维）触发"人格化"回答。**本仓库只做技术层面学习与验证，不涉及医疗效果评价。**

## 带来的概念
- [[分层按需加载]]（新）：入口层 2.71% 常驻 + 蒸馏速查层 + 模块层，实测 token 账本成立
- [[AgentSkills技能包]]（已有关联强化）：本项目是其"大规模领域知识"实例
- [[角色提示]]（关联扩展）：剧本级人格——几万字表达规则 + 输出前八查自检
- 思想呼应：速查层 ≈ 缓存前置（见 [[缓存]]）；八查 Gate ≈ [[质检Gate与自我纠错循环]]；输出格式 v2.1→v2.3 迭代史是活的提示词工程教材

## 实验做了什么（exercise\skill_checkup.py，全部真实运行）
1. frontmatter 合规：name=nihaixia 合规、description 340 字符含全部 4 触发词 → PASS
2. 结构盘点：modules 14 / cases 7 / distilled 8 与 README 一致；全仓 44 md / 6.1MB / 230 万字符
3. 引用完整性：SKILL.md 引用 29 个路径，0 死链 → PASS
4. 检索测试："小柴胡汤"命中 12 文件（伤寒论太阳篇 86 次最多）、可溯源到具体行；"真寒假热"入口层直接命中
5. token 账本：SKILL.md 62,481 字符 ≈ 3.8万~6.2万 token，占全库 2.71%，证明分层必要性

## 坑与结论
- 推文判断：同主题仓库多（nihaixia / nihaisha-nishi-tcm / Nihx_TCM / nihaixia-unified），推文数字口径指向 jangviktor-web/nihaixia
- README 宣称 3.5M 字精萃 vs 实测 2.3M 字符——宣传数字要自己 wc
- Edge 无头打印：需完整路径 + `--headless=new` + 独立 `--user-data-dir`，旧 `--headless` flags 会静默失败不出 PDF
- 通用模式可复用："领域专家 → Agent Skill"五步流水线：收素材 → 结构化 → 蒸馏速查 → 人格规则 → 审计对账
