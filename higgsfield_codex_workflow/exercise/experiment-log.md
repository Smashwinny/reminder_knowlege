# Higgsfield × Codex 创作工作流 · 实验日志（task 61eededa-7107-4f33-ad1c-a287c1520ce4）

初跑：2026-10-28；审核修订：2026-11-22。
性质：官方接口/责任边界 + 自写离线契约。无账号、未安装 CLI、未真实生成。

## 当前官方复核

2026-11-22 读取：
- https://higgsfield.ai/cli
- https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-access-higgsfield-via-cli

确认 CLI 安装 `npm i -g @higgsfield/cli`、`npx skills add higgsfield-ai/skills`、`higgsfield auth login`；CLI/MCP 为账号登录，不是 Higgsfield API key。帮助页给出同一账号同一积分率、Unlimited/免费生成不适用、Developer Terms 责任、CLI Skills 与 Supercomputer Skills 不同、产出落 Assets。

当前 CLI 页已明确异步生成与 agent 轮询，因此初稿“异步工作流未文档化”过宽。两页仍无具体任务状态枚举或任务 ID 查询命令，通用五态只能作为本地模型。

## 修订后的离线实验

初稿只有 decision-matrix.md，没有可执行实验。新增 `route_contract.py` 与 8 项 unittest：

- CLI/MCP/GUI 三通路和不同证据类型；Unlimited 假设、未知通路 fail-closed。
- 预算 500，两次 120 后余额 260，再预留 300 被拒且余额不变；非正估算拒绝。
- 通用 queued/running/succeeded/failed/cancelled 模型；仅 succeeded 可验收 Assets，终态不可重开。

实际命令：

```bash
python -I higgsfield_codex_workflow/exercise/route_contract.py
python -I higgsfield_codex_workflow/exercise/test_route_contract.py
```

主程序断言与 8 项 unittest 全部通过。五态借用 [[异步任务五态契约]] 的通用方法，不表示 Higgsfield 使用相同状态值。批量条数与预算阈值均为示例，不是官方建议。

## PDF 与边界

修订 HTML 后新增 v2 PDF，共 8 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→能力/总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `78757225e83252a32c52c33283bbe0f5482db38ebc5de9cf4aab6a3e4fc789e5`。未验证 Computer Use 当前账号可用性、真实生成、积分扣费、Assets 或 30 秒演示。
