---
tags: [项目]
类别: 开源项目类 / 媒体工程 / Web API
上游仓库: https://github.com/imputnet/cobalt
完成日期: 2026-10-31
---

# cobalt_tools

**这是什么**（一句话）：cobalt 是 imputnet/cobalt 的开源公开媒体保存 Web + API 项目，用统一 JSON 契约隐藏不同平台的 URL、媒体和处理差异；本指南只把它作为主学习对象，tiktokio.bio 与 greenvideo.cc 仅是独立服务对照。

**它给我什么能力**：
- 在获授权的自托管实例上，用 `POST /` 统一提交公开媒体 URL，并控制质量、音轨、文件名、元数据、代理和处理位置。
- 正确消费五种响应：`tunnel`、`redirect`、`local-processing`、`picker`、`error`，而不是假设所有请求都返回一个直接文件地址。
- 在服务端 FFmpeg 与浏览器 libav.js 之间分流 merge/remux 等工作。
- 用短期签名隧道传递流式处理计划，并通过限流、API Key、Turnstile、反向代理保护公开实例。
- 复用“规范化 → 服务适配 → 动作决策 → 统一响应”的架构到其他公开文件处理工具。

**引入的概念**：
- [[媒体处理响应契约]]（候选新笔记，详见项目内知识提案）
- [[短期签名媒体隧道]]（候选新笔记）
- [[端侧媒体处理分流]]（候选新笔记）
- 关联已有：[[构建流水线与Pass]]、[[统一数据网关]]、[[能力层与后端路由]]、[[负载均衡与反向代理]]、[[缓存]]、[[证据优先质检ProofOverClaims]]

**实验记录**（做了什么、结果、坑）：

固定上游版本 `a636575b09de1fc55d9b8cd98cac88f5f2f16b42`（API 11.7.1），Windows 11、Node 24.21.0、pnpm 12.8.1。`pnpm --dir repo install --frozen-lockfile` 成功；可选 `syscall-napi` 因 Windows 缺少 node-gyp 构建失败，但对应 Linux freebind 路径未用于本实验。

1. 官方 `pnpm --dir repo/api test get-services` 实际列出 21 个服务键；只验证配置/fixture 存在，不宣称平台下载可用。
2. `node exercise/contract-lab.mjs` 调用官方 normalizeRequest、matchAction、createStream/verifyStream，21 项断言通过：短链规范化、默认值、严格 schema、文件名、redirect/tunnel/local-processing/picker、签名篡改 401。自写夹具全部使用保留 `.example` 域名，未发媒体请求。
3. `node exercise/api-smoke.mjs` 真实启动官方 Express API 到 `127.0.0.1:19100`，10 项 HTTP/schema 断言通过：GET 版本/commit/21 服务，以及 link.missing、header.accept、link.invalid 三种错误契约；随后关闭子进程。
4. 首轮契约脚本因 cwd 不在 package root 报 `no package root found`；脚本改为导入官方模块前切到 `repo/api` 后通过，故障与修复已记录。
5. 完整真实输出见 `cobalt_tools/exercise/experiment-log.txt`；指南为 14 页中文 PDF，HTML 含 Q1–Q10 与 10 张内联 SVG。

**范围与限制**：未调用托管 cobalt API，未下载任何第三方媒体，未验证各平台当前可用性，未测试 Docker、Redis、多实例、Turnstile 或实际 FFmpeg 转码。只研究公开内容的合法获取、工具架构和本地使用，不涉及 DRM、付费墙、登录限制或其他访问控制绕过。X 原帖实时读取返回 HTTP 402；本笔记仅使用任务队列已保存摘要和官方一手资料。尚未经过独立 review。

**后续可深入的方向**：
- 在获得明确授权的公开测试素材上，验证完整 tunnel 流、Range 请求和实际封装输出字节。
- 用 Docker + Redis 验证多实例共享隧道元数据及限流行为。
- 对前端 local-processing 的浏览器计算成本、大文件内存和失败恢复做性能实验。

**主要来源**：
- https://github.com/imputnet/cobalt/tree/a636575b09de1fc55d9b8cd98cac88f5f2f16b42
- https://github.com/imputnet/cobalt/blob/a636575b09de1fc55d9b8cd98cac88f5f2f16b42/docs/api.md
- https://github.com/imputnet/cobalt/blob/a636575b09de1fc55d9b8cd98cac88f5f2f16b42/docs/run-an-instance.md
- https://github.com/imputnet/cobalt/blob/a636575b09de1fc55d9b8cd98cac88f5f2f16b42/docs/protect-an-instance.md
