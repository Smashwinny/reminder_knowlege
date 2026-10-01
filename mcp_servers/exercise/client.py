# -*- coding: utf-8 -*-
"""最小的 MCP 客户端：像 Claude Desktop 那样连接 server.py 并调用工具。

它做的事 = MCP 完整生命周期：
  1. 把 server.py 作为子进程启动（stdio 传输）
  2. initialize 握手（交换协议版本与能力）
  3. tools/list 列出服务器提供的工具
  4. tools/call 实际调用工具并拿到结果
"""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    # 1) 声明"如何启动服务器"：用当前解释器（venv 里的 python）运行 server.py
    #    坑：写死 "python" 会用 PATH 里的系统解释器，它没装 mcp 包 → 连接直接关闭
    params = StdioServerParameters(command=sys.executable, args=["server.py"])

    # 2) stdio_client 负责"启动子进程 + 收发 JSON-RPC"，ClientSession 管协议状态
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            # 3) 握手：双方协商协议版本、交换能力声明
            info = await session.initialize()
            print(f"[握手成功] 服务器: {info.server_info.name}")
            print(f"[协议版本] {info.protocol_version}")

            # 4) 列出工具
            tools = await session.list_tools()
            print(f"[工具清单] {[t.name for t in tools.tools]}")

            # 5) 调用工具
            r1 = await session.call_tool("add", {"a": 20, "b": 22})
            print(f"[调用 add(20, 22)] -> {r1.content[0].text}")

            r2 = await session.call_tool("count_servers", {})
            print(f"[调用 count_servers()] -> {r2.content[0].text}")

            # 6) 读一个资源（tools 之外的另一种能力）
            res = await session.read_resource("lab://greeting/小明")
            print(f"[读取资源] -> {res.contents[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
