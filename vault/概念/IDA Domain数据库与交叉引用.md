---
tags: [概念, 逆向工程, IDA Domain, 交叉引用]
---
# IDA Domain数据库与交叉引用

**一句话定义**：把二进制分析结果作为数据库对象查询：函数、地址、指令、调用边与 xrefs（交叉引用）都可按对象和地址检索，并能回到原始反汇编证据。

**领域**：逆向工程 / 程序分析。来源：[[项目笔记/ida_pro_mcp]]（官方 HexRaysSA/ida-mcp 与 Domain 文档）。

典型查询包括 `db.functions.get_all/get_at/get_name`、`db.xrefs.calls_to_ea`、`db.instructions.get_at/get_disassembly`。MCP 只负责调用通道（[[MCP协议]]、[[JSON-RPC与stdio传输]]）；函数或调用边存在不等于运行时必达，语义正确性仍需独立验证。
