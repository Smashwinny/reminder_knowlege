# Agent可信工作倒金字塔：增量提案
固定vault main已读00-总览、代码管边界提示词管判断及agent-engineering。只提案，不改仓库。
1. 既有硬边界概念补作者的投入顺序：架构/类型→自动检查→少量文字→高杠杆人工审查，不是取消人工，也不是测试比例定律。
2. 类型的证据边界：TS2345可拒绝Draft传Approved，但as any负对照仍编译通过；运行时JSON需unknown入口校验，不因静态标注自动可信。
3. 自动化层次分开：静态lint/类型、动态测试、CI执行环境、有限模型或TLA+不能混报。此次无TLA+/远端CI/模型Agent运行。
4. 状态迁移反例：无限制小模型6状态有未批准send与重复交付，收紧后3状态零当前模型违例。假设：count≤2，无崩溃、撤回、网络。不能推出生产恰好一次。
5. 固定pstack验证Skill的Launch/Doctor/Drive/Evidence/Cleanup要求，作为审查清单，不安装Skill、不执行查Slack/recall/创建Project。
六步实际运行、12自写测试；作者token/缺陷收益未测。状态部分待验证。
