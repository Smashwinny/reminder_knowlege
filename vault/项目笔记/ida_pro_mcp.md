---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/HexRaysSA/ida-mcp
完成日期: "2026-11-18（worker ready，待独立审核）"
---

# ida_pro_mcp

**这是什么**（一句话）：Hex-Rays 官方 IDA MCP Server，把 AI 宿主通过 MCP 发出的请求适配到 IDA Nexus 管理的数据库与 IDAPython/IDA Domain 查询能力。

**范围声明**：原帖 https://x.com/realNyarime/status/2104608677772804580 只表达作者对“IDA Pro MCP”的体验，正文和附图均未给出实际插件仓库、版本或样例。本次经授权**重新定范围**为官方 HexRaysSA/ida-mcp 的独立学习，不能称为原帖同款已证实。学习固定提交为 `391c2f0606a773050fbafcd3ff62942688a0713b`（20261028.0.3）。

**它给我什么能力**：
- 用六个 MCP 工具打开/列出/保存/释放数据库、查询 Domain API 参考、执行 IDAPython/Domain Python。
- 在自己的二进制上枚举函数、反汇编、伪代码、字符串、导入与交叉引用，并把调用结论回溯到地址和指令。
- 通过 Nexus 在 GUI、idalib/idat worker 和多个客户端租约之间共享数据库；关闭一个客户端不等于关闭别人的 GUI。
- 用语义 JSONL 追踪、dashboard 和 logs 复核工具调用与结果。

**引入/关联的概念**：
- [[MCP协议]]、[[JSON-RPC与stdio传输]]：initialize、tools/list、tools/call 与 stdio 通道。
- [[证据优先质检ProofOverClaims]]、[[事实与判断分离]]：AI 评价不能替代哈希、地址和原始指令。
- [[沙箱与审批正交]]：本地连接、工具能力和目标授权是不同维度。
- 待协调者查重后决定的新概念：IDA Domain 数据库与交叉引用、逆向结论证据链、数据库租约与共享 worker。worker 未直接创建概念笔记。

**实验记录**（做了什么、结果、坑）：
- 环境：Windows 11、Python 3.14.7、MinGW GCC 6.3.0、GNU Objdump 2.28；常见路径未发现 IDA，uv 不在 PATH。
- 自写 `demo.c`，以 `-O0 -g -fno-inline -fno-omit-frame-pointer` 编译，仅运行该自编译程序。输入 7 得 `decision=1 token=66 exit=0`；输入 27 得 `decision=0 token=0 exit=2`。
- 对真实 Objdump 输出运行限制输入的本地 MCP stdio 教学桩；完成 initialize、六工具发现和 5 次工具调用。`ida_queries.py` 使用官方文档中的 `db.functions.get_all/get_at/get_name`、`db.xrefs.calls_to_ea`、`db.instructions.get_at/get_disassembly` 形状，在本地兼容层实际运行。
- 4/4 条预期直接静态调用边均有地址证据：`main→authorize@0x4014ef`、`authorize→check@0x401499`、`authorize→mix@0x4014b2`、`check→mix@0x40147d`；5 个 tool_call 均有对应 tool_result。
- 本次二进制 SHA-256：`b1b330389e3c5b2c9d744167f1f0887797893d8dd66f4aed4fe8da38ac193560`。重编译可能改变 PE 时间戳与哈希，重跑须以新日志为准。
- 实际踩坑：32 位 MinGW 给 C 符号加前导 `_`，第一轮未归一化导致函数匹配失败；终端 tee 使中文日志不是 UTF-8，改为脚本自行 UTF-8 双写；负例最初误选 1，真实输出纠正预期后改选 27。

**限制**：
- 本地桩不是官方 ZeroMCP/Nexus 实现，不是通用安全沙箱，不提供反编译；只允许固定自编译二进制、Objdump 文本和固定查询脚本哈希。
- 未验证 IDA/idalib/idat 实机、官方 MCP 服务器、自动分析、Hex-Rays 伪代码、Nexus 租约/取消/GUI 集成。
- 直接静态调用边不证明运行时必达、数据流或语义正确性；动态输入对照只用于自建程序 sanity check。
- 未验证原帖“更快、更准、更全面”，未运行未知二进制或针对第三方目标。
- PDF 回读为 18 页；浏览器截图确认 HTML 封面渲染。当前环境不能直接逐页渲染 PDF，headless PDF 查看器截图为空白，因此逐页视觉验收留给独立审核。

**产物**：
- `ida_pro_mcp/ida_pro_mcp-小白指南.pdf`
- `ida_pro_mcp/ida-pro-mcp-guide.html`
- `ida_pro_mcp/exercise/experiment_log.txt`
- `ida_pro_mcp/exercise/analysis_result.json`
- `ida_pro_mcp/exercise/mcp_trace.jsonl`

**后续可深入的方向**：在自有 IDA 9.4+ 许可证环境重放同一自编译样例，对照 Domain xrefs 与 Objdump；验证自动分析、伪代码、GUI/headless、save/close、取消和追踪；再讨论混淆、间接调用和运行时覆盖率，当前实验不覆盖这些主题。

**来源**：官方 ida-mcp、ida-nexus、ida-domain 文档与示例；社区 mrexodia/ida-pro-mcp 仅用于辨析候选身份，其当前 README 推荐官方项目。
