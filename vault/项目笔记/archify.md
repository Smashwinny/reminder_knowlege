---
tags: [项目笔记]
项目: archify
类别: 开源项目类（Agent Skill）
完成日期: 2026-10-03
仓库: https://github.com/tt-a1i/archify
---

# archify — 代码/一句话 → 交互式架构图（76.2k stars）

## 它是什么
Agent Skill 形态的画图工具：SKILL.md（107 行作业指导书）+ 本地 CLI（`bin/archify.mjs`，约 6900 行）。AI 读指导书，按五种图类型（architecture / workflow / sequence / dataflow / lifecycle）的路由读对应 JSON Schema 与示例，写一份**类型化候选 JSON**，再跑 `finalize` 命令过四道门禁（validate → deliver → check → browser-check，见 `bin/finalize.mjs` 的 `FINALIZE_STAGES` 常量），产出**单文件自包含交互 HTML**（实测官方示例各 744KB，外部依赖 0 个）。

## 带来的新概念
- [[JSON-IR类型化中间表示]] — LLM 只填语义表（节点 type 七选一），几何交给确定性渲染器
- [[源码取证图]] — 画真实仓库时钉 commit SHA + sourceReferences 逐条取证，防 AI 编造调用关系

## 关联的已有概念
- [[AgentSkills技能包]]（archify 是 76k 级标杆实例）、[[质检Gate与自我纠错循环]]（finalize 门禁 + 修复重跑上限）、[[修改与约束分离]]、[[确定性图布局]]

## 实验做了什么（exercise\）
1. **exp1_artifact_check.py**：静态体检官方示例 HTML——外部 script/link/img = 0，主题/导出/Route Probe/Node Finder/键盘可达/深链全命中，节点带原生 `<title>` 无障碍提示。
2. **exp2_schema_validate.py**：用 jsonschema 4.26 + 官方 workflow.schema.json 校验自编候选（拾遗流水线图）：首跑 7 错（type 用了流程图词汇）→ 按语义改后 0 错；反例（删 lanes、type=magic-box）均被拦。
3. **finalize 生成**（命令已给）：本机安全策略禁止执行刚克隆的外部代码，未真实运行，如实标注。

## 坑与结论
- 推文来源是"保存这份清单"带货帖，7 个仓库 **2 个不存在**（omnivoice-studio、deepseek-ai/dsh）——清单必先逐个验证。
- 节点 type 是语义不是形状：审批门用 `security`、远端同步用 `cloud`，别按流程图习惯填。
- viewer 特性（主题/路径探测/导出）默认内置于产物，无需额外配置；`meta.animation: "trace"` 才是选装。
- 对本仓库的价值：learn-project 出 PDF 前可先用 archify 出交互图，导 PNG 进 PDF 双份产出；finalize"真浏览器门禁"思想可反哺 PDF 质检。
