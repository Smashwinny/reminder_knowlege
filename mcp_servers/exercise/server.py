# -*- coding: utf-8 -*-
"""我的第一个 MCP 服务器 — 官方 SDK（mcp 2.x）版。

坑位记录：网上老教程写 `from mcp.server.fastmcp import FastMCP`，
那是 mcp 1.x 的写法；mcp 2.x 已改名为 MCPServer（用法基本一致）。
"""
from pathlib import Path

from mcp.server.mcpserver import MCPServer

# MCPServer 实例 = 一个 MCP 服务器。name 会出现在 initialize 握手结果里。
mcp = MCPServer("awesome-mcp-lab")

README = Path(__file__).resolve().parent.parent / "repo" / "README.md"


@mcp.tool()
def add(a: int, b: int) -> int:
    """把两个整数相加。最小的"工具"示例：证明 AI 能调用我们的代码。"""
    return a + b


@mcp.tool()
def count_servers() -> dict:
    """统计 awesome-mcp-servers 清单：总条目数、分类数、官方实现数。"""
    text = README.read_text(encoding="utf-8")
    entries = [ln for ln in text.splitlines() if ln.startswith("- [")]
    categories = [ln for ln in text.splitlines() if ln.startswith("### ")]
    official = [ln for ln in entries if "🎖️" in ln]
    return {
        "总条目数": len(entries),
        "分类数": len(categories),
        "官方实现数": len(official),
    }


@mcp.resource("lab://greeting/{name}")
def greeting(name: str) -> str:
    """一个 resource（资源）：与 tool 的区别是"只读数据" vs "可执行动作"。"""
    return f"你好 {name}！这是从 MCP 资源 lab://greeting/{name} 读到的内容。"


if __name__ == "__main__":
    mcp.run()  # 默认 stdio 传输
