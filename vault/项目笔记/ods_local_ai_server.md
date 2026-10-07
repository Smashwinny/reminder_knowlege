---
tags: [项目笔记, 开源项目, 服务编排, 本地AI, 集成层]
created: 2026-10-07
---

# ODS（私有 AI 服务器编排层）

- 仓库：https://github.com/Osmantic/ODS（Apache-2.0，快照 ac1fd24，5460 文件；2026-10-07 克隆实测 7107 stars，V3 预发布）
- 来源：@Gk 推文 https://x.com/0xGky/status/2106681985502744777

## 是什么

把电脑变成私有 AI 服务器的集成编排层：一行命令装好 Ollama+Open WebUI+n8n+ComfyUI 并互相接好，按硬件自动推荐模型，localhost:3000 即用；无显卡切云端 API 模式。数据不出机（本地模式），不用订阅。

## 架构增量（相对单个组件）

- 编排三职责：生命周期（装/起/重启）、拓扑（端口/发现）、能力映射。
- 硬件→模型三段映射：model_selection.py（显存档位→模型档→量化档）。
- 7+ 服务组件（dashboard-api 203 测试/model-router/token-spy/pixel-agent/pixel-edge/ape）各自带独立测试——集成项目≠脚本合集。
- 自带 CLAUDE.md（agent 仓库指南）+ ARCHITECTURE.md。

## 本机实证

ods/tests 1046 collected → **2500 passed / 187 failed / 1018 errors in 189s**（Windows 裸机）。归因：≈980 FileNotFoundError/WinError（缺 docker/ollama/Unix 路径）+ 35 ModuleNotFoundError（pwd）——macOS/Linux-first 实证（install.ps1 存在但 Windows 走 WSL）。模型选择专项 437 passed。未真实安装（Docker 全家桶+系统服务变更超出 worker 范围）。

## 祛魅

"一行命令"省集成工序不省运维（模型下载几十 GB/驱动/升级兼容自理）；V3 预发布生产慎用；Windows 二等公民。

## 关联

- [[ollama]]（被编排组件，发动机 vs 装配线）、[[本地推理引擎]]、[[BYOK模型网关与用量归因]]（token-spy 用量归因）、[[能力地板选型]]
- 概念提案：集成编排层（见项目目录 knowledge-proposal.md，协调者终审）
