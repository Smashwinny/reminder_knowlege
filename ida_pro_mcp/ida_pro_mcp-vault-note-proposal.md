# ida_pro_mcp 知识入库提案

- task_id：f7eeae1f-8a5a-4a22-8fa5-fb6e9c41c1e7
- owner：main-k3-w7
- 日期：2026-11-18
- 状态：worker 产物待协调者查重、合并和独立审核；本提案不代表任务完成。

## 范围与来源

原帖及附图仍不能绑定作者实际插件。经授权重新定范围为官方 `HexRaysSA/ida-mcp` 独立学习，固定提交 `391c2f0606a773050fbafcd3ff62942688a0713b`。不得把官方项目写成原帖已证实目标。

## 已做只读查重

- 已读 `vault/00-总览.md`、`vault/概念/MCP协议.md`、`vault/概念/证据优先质检ProofOverClaims.md`。
- 在 vault 搜索 `IDA Domain|IDAPython|交叉引用|调用图|反编译|ida-mcp|ida_pro_mcp`，未发现同名 IDA MCP 项目笔记或对应概念笔记。
- 可复用并互链：`[[MCP协议]]`、`[[JSON-RPC与stdio传输]]`、`[[证据优先质检ProofOverClaims]]`、`[[事实与判断分离]]`、`[[沙箱与审批正交]]`。

## 建议合并内容

1. 新项目笔记：`vault/项目笔记/ida_pro_mcp.md`（worker 已按本次边界新建，仅此一个 vault 文件）。
2. 若协调者复核后认为有必要，可新建/合并三个概念：
   - **IDA Domain 数据库与交叉引用**：函数对象、地址、指令、xrefs 的查询关系；链接 MCP协议。
   - **逆向结论证据链**：结论绑定输入 SHA-256、调用边、call 地址、原始指令和适用范围；链接证据优先质检与事实与判断分离。
   - **数据库租约与共享 worker**：GUI/idalib/idat 共享 IDB，close 释放单客户端租约而非关闭他人 GUI；链接构建流水线与Pass或相关生命周期概念。
3. 上述概念仅为提案，worker 未修改 `vault/概念/` 或 `vault/00-总览.md`。若已有同义概念，应合并而非新建。

## 真实实验摘要与限制

自编译 C 程序正负输入均实测；Objdump 真实静态反汇编；本地 MCP stdio 教学桩完成六工具发现、5 次调用与结果配对，4/4 直接调用边有地址证据。未验证 IDA 实机、官方 ZeroMCP/Nexus、反编译、自动分析、GUI/租约/取消，不证明原帖速度或准确率。完整证据见 `ida_pro_mcp/exercise/experiment_log.txt`、`analysis_result.json`、`mcp_trace.jsonl`。

## 建议 MOC 条目（由协调者决定）

`[[项目笔记/ida_pro_mcp]] — 官方六工具 MCP → Nexus 共享 IDB → Domain 函数/xrefs 查询 → 哈希/地址/指令证据回溯；本地桩实测，IDA 实机未验证。`
