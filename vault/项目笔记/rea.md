---
tags: [项目笔记, 逆向工程, MCP, 证据框架]
created: 2026-10-27
---
# REA（Reverse Engineer Anything）

morluto/rea（MIT，v6.8.0，commit b9d1a61）：逆向工程的 MCP 总调度台，按目标类型路由可用引擎，并输出统一证据包。

## 核心概念
- [[三态证据框架（SEEN-INFERRED-UNKNOWN）]]：语法事实、推导与未知分开记账。
- [[逆向工程工具路由层]]：目标类型→有序引擎列表→首个可用者，M 个 Agent 与 N 个引擎只需 M+N 对接。

## 实测
源码构建成功。自建 Electron 样本埋入隐藏快捷键、假验证后门、IPC 通道，REA 免商业引擎静态分析全部命中并给出源码行列；证据包含 162 节点/105 关系/63 unknowns，limitations 明示运行时行为未证实。doctor 17 项检查给出依赖与修复路径。

坑：Node 补丁版本不符需 `--force`；`build:cached` 不编译 TS，需 `npm run compile`；Git 源码不含 Windows 原生控件，需从官方 npm tarball 恢复。原生二进制深度分析仍需 Hopper/Ghidra/IDA 之一。
