---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/img2threejs/img2threejs
完成日期: 2026-10-01
---

# img2threejs

**这是什么**：一张参考图 → AI 编程助手写 TypeScript → 代码在浏览器里生成可旋转、可动画的**纯程序化** Three.js 模型（不是网格文件）。方法论项目：v2.0.0，Apache-2.0，本地路径 `F:\reminder\img2threejs\repo\`。

**它给我什么能力**：
- 一套"AI + 客观质检"的编程工作流范式，可迁移到任何 AI 编程项目；
- 约 90 个零依赖 Python 确定性脚本组成的工具链（probe → spec → validate → generate 全链路）；
- `grimoire\` 评分标准文档：如何给 AI 的产出写"客观可执行的验收标准"。

**引入的概念**：
- [[程序化建模]]
- [[Three.js与场景图]]
- [[构建流水线与Pass]]
- [[质检Gate与自我纠错循环]]
- [[确定性脚本]]
- [[零依赖编程]]

**实验记录**（详见 `F:\reminder\img2threejs\img2threejs-动手练习.pdf`，4 练习 14 步全部实测）：
- B1–B6 命令链全通：probe_image → new_pre_spec_assessment → new_sculpt_spec → validate --strict-quality（会拦空壳规格书）→ fixture PASS → generate_threejs_factory；
- `forge/state.py init` + `forge/next.py --state` 断点续作可用。

**坑与结论**：
- 中文 Windows 默认 GBK：先 `setx PYTHONUTF8 1`，否则测试套件 20+ 个 UnicodeDecodeError 假失败；
- 修复后 1408/1416 通过，剩余 8 个全是符号链接/子进程类 Windows 边缘情况，不影响主流程。

**后续可深入的方向**：
- 读 grimoire 评分文档的写法，提炼"如何给 AI 写验收标准"；
- 把 8 层 Pass 的分工映射到自己的其他 AI 编程项目。
