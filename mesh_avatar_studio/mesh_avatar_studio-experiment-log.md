# 实验日志 · Mesh Avatar Studio（mesh_avatar_studio）

- 任务：06ac032d-cdee-4bda-9f23-55e454bc34a6（子 agent 分类上报，主控批复后主控执行完整学习）
- worker：kimi-pool-20261007-w1（主控模式）
- 日期：2026-10-09
- 仓库：shinshin86/mesh-avatar-studio（浅克隆 39d1625，v0.1.0，217 文件，540★，MIT+资产分层）

## 实验设计

四步人机管线中 step1/4 由 coding agent 完成（需真实插画+强视觉模型会话），超出本机实验面。实验面：依赖安装 + 单元测试套件实跑 + agent-guide/工程结构阅读。

## 运行记录（全部真实执行，exercise/run_output.txt）

1. `npm install --ignore-scripts` 成功（Node v24.21.0）。
2. `npx vitest run tests/`：23 文件 107 用例 → **102 passed, 5 failed in 9.73s**。
3. 失败归因（--tb 逐条）：local-projects ×3 + project-jobs ×1 = **EPERM symlink 被拒**（Windows 非管理员账户不能创建符号链接；测试用 symlink 构造路径逃逸攻击样本测自家 API 安全性）；expression-remote ×1 = token 私有性同类环境差异。有效通过率 95.3%。
4. e2e（Playwright）未跑（需浏览器+dev server）；端到端头像生成未做（如实声明）。

## 结构阅读实证（纯读取）

- docs/agent-guide.md（201 行）：写给 agent 的生产级作业书——顺序+每步检查+模型资质声明制（不在 Opus 5.5/GPT-6.1 Sol 清单就明说"可能不达标"询问是否继续）。
- tools/vision-check.py：**能力前置验证**——标定图评分，不达标就停，返工成本变 10 秒标定。
- src/engine（渲染/物理/表情/kana 口型）+ src/rig + live（摄像头追踪/推流）。
- 许可分层：代码 MIT / 样例角色 Miko 作者保留 / mediapipe Apache 2.0。
- 安全测试法：用 symlink 构造攻击样本测自己的 API（traversal/跨源拒绝）。

## 结论

- "Agent 备料+人工微调"的四步审核式分工是最值得学的设计；vision-check 能力校准是 harness 论文七子系统之外的新增子系统位置。
- 未验证（诚实声明）：端到端头像生成、e2e、5 个 symlink 测试的修复（需管理员/开发者模式）。

## 产物

- `exercise/run_output.txt`、`exercise/insert_svgs.py`
