# Antigravity 登录排查 · 实验日志（task 4e85eb0e-2d1a-4de4-a954-ec8faf1d5d13）

初跑：2026-10-28；审核修订：2026-11-22。
性质：官方当前政策 + 固定第三方源码静态标记。未登录账号、未读取真实 token、未运行 Manager/Bridge。

## 当前官方复核

2026-11-22 读取 https://antigravity.google/docs/faq/ 与 https://antigravity.google/terms ：

- FAQ 与 Terms §6 明确第三方软件/工具/服务访问 Antigravity 违反 ToS，可暂停/终止 Antigravity 和/或 Gemini CLI 账户。
- 当前 FAQ 给第三方 Gemini coding agent 的替代是 Gemini Enterprise 或 Google AI Studio API key；该页未提 Vertex，初稿已删除此归因。
- FAQ 有国家关联纠错和年龄验证入口，但没有一般封号申诉流程；支持页/法律入口不能混写成通用封禁申诉。
- 当前资格包括个人账号、支持地区、账号类型和年龄；未满 18 不可用。
- Terms 的账户范围不能证明“整个 Google 账号绝不受影响”；封禁潮、AI Ultra 用户 403 等只保留为社区报告，不作为官方事实。

## 固定源码与初稿边界

- Manager commit `0067fe045ddd77f4462ea8e2c25384839d869f32`。
- Bridge commit `2c8c12d7f515873e011a8c7a8d40c3a250a4a1a0`。

Manager 静态审计命中 daily-cloudcode-pa.googleapis.com（9 文件）、cloudcode-pa.googleapis.com（10 文件）、sandbox（3 文件）、`antigravity-oauth-token` 文件名（5 文件）；LICENSE 为 CC-BY-NC-SA 4.0。只证明源码标记和许可，不证明完整运行数据流。

Bridge README 自述 macOS 进程级代理、不开 TUN、非官方、不读取/保存/转发登录凭据、MIT。初稿“Bridge 不碰 token/边界清晰”过强，已改为维护者声明，未全量源码或运行验证。

## 真实离线复跑

```bash
python -I antigravity_login/exercise/static_dataflow_audit.py
python -I antigravity_login/exercise/test_static_dataflow_audit.py
```

新增 `dataflow-audit-v2.json`；6 项 unittest 全部通过：三类端点、token 文件名、许可与不冒称运行证明。没有读取任何真实 OAuth token 或用户配置。

## PDF

修订 HTML 后新增 v2 PDF，共 7 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `53b0b464a0bd5e14380efd5773aafe3a5ca8b7c02f0a35b50224f4cfa75f66cc`。
