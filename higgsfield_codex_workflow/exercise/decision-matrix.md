# Higgsfield 创作通路决策矩阵（2026-11-22 审核修订）

> 依据：higgsfield.ai/cli 与帮助页当前读取。费用/责任边界适用于全部通路；本地 `route_contract.py` 与 8 项测试只验证自写契约，不连接平台。

## 三场景 × 三通路

| 场景 | 首选通路 | 理由 | 独立验收证据 |
|---|---|---|---|
| 电商批量视频 | CLI（coding agent） | 脚本化批量与轮询可编排 | 命令、任务回执、尺寸/内容/音轨/Assets |
| 店铺视觉升级 | Computer Use（GUI） | 复杂界面流一次性操作 | 与手动流程逐步对照截图 |
| 无脸账号内容 | MCP（chat agent） | 对话内迭代，人在环 | 工具回执、风格一致性、肖像/版权检查 |

三种证据互不等价：CLI 成功不证明 GUI 完整复现，MCP 回执也不证明网页端每个功能一致。

## 当前官方边界

- 同一账号同一积分率；**Unlimited/免费生成不适用**。
- Developer Terms：保护会话，agent 经账号生成的内容由账号主体负责。
- CLI Skills ≠ Supercomputer 内置 Skill（同名不同体）。
- 当前 CLI 页明确生成异步、agent 轮询；帮助页产出落 Assets。
- 具体任务状态枚举、任务 ID 查询命令未公开；本地通用五态不是 Higgsfield 官方状态机。

## 本地契约实验

- 三通路字段与不同证据类型校验；Unlimited 假设和未知通路 fail-closed。
- 预算示例 500，两次 120 后余额 260，再预留 300 被拒且余额不变。
- 通用五态只有 succeeded 可验收 Assets；failed/cancelled 不可，终态不可重开。
- `python -I exercise/route_contract.py` 与 `python -I exercise/test_route_contract.py` 实际运行，8 项测试通过。

## 真实生成验收（本轮未做）

尺寸/分辨率、brief 内容、音轨与合规、Assets 文件与链接时效、积分消耗。阈值和批量大小应按账号价格另定，示例值不是官方建议。
