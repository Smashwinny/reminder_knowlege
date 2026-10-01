# -*- coding: utf-8 -*-
"""
mcp_handshake.py —— 不借助任何 AI 客户端，亲手和 MCP 服务器完成一次"握手-列工具-调工具"。

用法:
    python mcp_handshake.py

它做四件事:
  1. 启动官方文件系统 MCP 服务器 (@modelcontextprotocol/server-filesystem)，
     只允许它访问 exercise/sandbox 目录;
  2. 发 initialize 请求 —— MCP 协议握手第一步;
  3. 发 tools/list —— 看看这个服务器提供了哪些工具;
  4. 发 tools/call 调用 write_file 工具写一个文件，再去磁盘上验证。
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SANDBOX = os.path.join(HERE, "sandbox")


def main():
    os.makedirs(SANDBOX, exist_ok=True)

    npx = shutil.which("npx")
    if not npx:
        sys.exit("未找到 npx，请先安装 Node.js")
    print(f"[1] 启动 MCP 服务器 (只授权访问 {SANDBOX}) ...")
    proc = subprocess.Popen(
        [npx, "-y", "@modelcontextprotocol/server-filesystem", SANDBOX],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
    )

    def send(msg):
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()

    def recv():
        while True:
            line = proc.stdout.readline()
            if not line:
                raise RuntimeError("服务器提前退出，握手失败")
            line = line.strip()
            if line:  # 跳过空行
                return json.loads(line)

    # ---- 握手: initialize ----
    send({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "handshake-demo", "version": "0.1.0"},
        },
    })
    init = recv()
    info = init["result"]["serverInfo"]
    print(f"[2] 握手成功! 服务器: {info['name']} v{info['version']} "
          f"(协议版本 {init['result']['protocolVersion']})")
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    # ---- 问它有哪些工具 ----
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    tools = recv()["result"]["tools"]
    print(f"[3] 该服务器提供 {len(tools)} 个工具:")
    for t in tools:
        print(f"      - {t['name']}: {t.get('description', '')[:60]}...")

    # ---- 调用 write_file 工具 ----
    target = os.path.join(SANDBOX, "hello.txt")
    send({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {
            "name": "write_file",
            "arguments": {"path": target, "content": "Hello from MCP! 这行字是 MCP 工具写的。"},
        },
    })
    call = recv()
    ok = not call["result"].get("isError", False)
    print(f"[4] tools/call(write_file) 返回 isError={call['result'].get('isError', False)}")

    proc.stdin.close()
    proc.terminate()

    # ---- 磁盘验证 ----
    with open(target, encoding="utf-8") as f:
        content = f.read()
    print(f"[5] 磁盘验证: {target} 存在，内容 = {content!r}")
    print("全部通过 ✅" if ok and content else "有步骤失败 ❌")


if __name__ == "__main__":
    main()
