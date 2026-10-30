# 知识入库提案 · mesh_avatar_studio

- 任务：06ac032d-cdee-4bda-9f23-55e454bc34a6
- worker：kimi-pool-20261007-w1（2026-10-09，主控模式）
- 查重：子 agent 已核实 vault/队列无重复（img2threejs 为图生 3D，主题相邻不同）

## 提案 1：项目笔记提案（按新边界留待协调者合入）

`mesh_avatar_studio-vault-note-proposal.md` 已在本目录，请协调者转正为 `vault/项目笔记/mesh_avatar_studio.md`。

## 提案 2：概念更新建议（请协调者终审，非新建）

**更新 `vault/概念/人机协同Interrupt.md`（或 AgentHarness智能体挽具）**：追加"能力前置验证"模式——

- vision-check 模式：agent 开工前先跑标定测试量化自身能力（视觉坐标读取精度），不达标主动停下告知用户，把返工成本压缩为 10 秒标定。
- 与 [[Checkpoint存档与持久执行]] 的区别：校准的不是状态而是模型能力资质。
- 出处：mesh-avatar-studio docs/agent-guide.md（2026-10-09 学习，102/107 测试实测）。

另建议 [[AgentSkills技能包]] 追加"agent 指令文件两种体裁"注记：SKILL.md=路由型（huashu/dsh），agent-guide.md=作业型（顺序+检查+资质声明，mesh-avatar-studio）。

## 总览/索引更新

请协调者在 `vault/00-总览.md` 补一行 mesh_avatar_studio。
