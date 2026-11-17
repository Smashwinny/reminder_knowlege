---
tags: [项目笔记, 开源项目, 模型网关, 协议翻译, 多账号路由]
created: 2026-10-30
---

# CLIProxyAPI（本地多协议模型网关）

- 官方仓库：https://github.com/router-for-me/CLIProxyAPI （MIT）
- 固定版本：v8.0.47，commit `90c447d3`，发布于 2026-10-29
- 官方文档：https://help.router-for.me/
- 原始线索：https://x.com/0xlangeai/status/2106264636198908382 （蓝哥 AI；原帖 WebFetch 返回 HTTP 402，逐字正文未读到；项目身份由官方来源独立核实）

## 是什么

Go 编写的本地代理服务器，把客户端使用的 OpenAI / Gemini / Claude / Codex 等兼容 API，连接到 CLI/OAuth 或 API-key 上游。它做客户端鉴权、模型目录与 alias、协议翻译、多凭据选择、重试/冷却、响应还原和管理，不在本机运行模型权重。

v8.0.47 README 的上游矩阵包括 Kimi、OpenAI/Codex、Claude、Gemini/Antigravity、Grok、Meta Muse、Devin 及 OpenAI 兼容端点；实际可用模型与功能取决于具体账户和上游，不等于免费或全特性无损。

## 核心机制

1. **两类以上凭证分权**：`access.api-keys` 管客户端进入网关；`api-keys.*` / OAuth 管网关访问上游；`management.secret-key` 管配置和凭证控制面。三者不能混为一把 key。
2. **Translator × Executor**：Translator 在入站协议与 provider 格式之间转换请求、非流式响应和 SSE；ProviderExecutor 构造真实出站 HTTP、注入凭证并处理 provider 细节。模型注册表把客户端 `alias` 映射为上游 `name`。
3. **路由不是一个旋钮**：round-robin / weighted-round-robin / fill-first 决定候选起点；session affinity 决定会话粘性；retry / cooldown 决定故障后的换路与恢复。已经输出给客户端的流不能简单无痕换路。
4. **控制面独立**：v8 管理基路径 `/v8/management`，配置路径对应 v8 YAML 树。管理 secret 留空可关闭管理路由，remote 默认受限；配置和凭证目录支持 watcher。
5. **可嵌入 Go SDK**：可复用 Builder、模型注册、Executor 与 Translator 扩展点。当前 go.mod 是 `/v8`；旧中文 SDK 文档仍有 `/v6` 示例，需以固定源码为准。

## 本机真实实验（2026-10-30）

环境：Windows 11，Python 3.14.7，官方 Windows amd64 发布包。未安装 Go，因此未从源码构建；使用官方二进制。发布 ZIP SHA-256：

`8e23cbb2f9f695411b7df46320855820b352fb886c3c3bdf45ab4634f2f14632`

与 GitHub Release digest 完全一致。实验只监听 `127.0.0.1`，Python 标准库 mock 上游 + 官方 CPA，所有 key 均为假值，真实外部模型调用 0。

实测结果：

- 无客户端 key `GET /v1/models` → 401 `Missing API key`；带 key → 200，目录只有 `demo-alias`，`owned_by=local-mock`。
- Claude `POST /v1/messages` → CPA → mock `POST /v1/chat/completions`。上游真实收到 `model=mock-model`、`messages=[system,user]`、`max_tokens=64`，证明 alias 和 Claude system/content 映射发生。
- OpenAI `choices[0].message.content` 返回为 Claude `content[0].text`；`finish_reason=stop` → `stop_reason=end_turn`；`prompt_tokens/completion_tokens` → `input_tokens/output_tokens`。
- OpenAI chunk/[DONE] 转为 Claude SSE，实际观察到 `message_start`、`content_block_start/delta/stop`、`message_delta`、`message_stop`。
- round-robin 四次连续上游请求为 **A/B/A/B**；改 `fill-first` 并明确重启后两次为 **A/A**。依据是 mock 捕获的 Authorization，不是猜测。
- 共 6 次上游请求，结构化断言全通过。命令与原始响应见 `cli_proxy_api/exercise/experiment_log.txt`，机器结果见 `experiment_results.json`，上游捕获见 `runtime/upstream_requests.jsonl`。

## 与已有知识的关系

- [[BYOK模型网关与用量归因]]：同属自托管模型入口；CLIProxyAPI 也可使用 CLI/OAuth 凭证。README 说明 v6.10.0 起不再内置完整用量统计，不能把管理面板当完整账单。
- [[Provider适配层与错误契约]]：提供 Executor/Translator 的真实 Go 实现与端到端协议证据。
- [[负载均衡与反向代理]]：补充 A/B/A/B 与 A/A 的可重复本机证据，并区分选择、亲和、重试和冷却。
- [[控制面与数据面]]：客户端数据面、上游凭证和管理控制面分权。
- [[能力层与后端路由]]：alias 和模型目录把稳定门面与上游实现解耦。
- [[项目笔记/magpie_gateway]]：同族但不重复；magpie 批次只做源码结构检查且未运行，本批次真实运行官方 CPA v8 并验证协议/SSE/路由。

## 坑与边界

- “OpenAI compatible”不保证工具调用、多模态、推理签名、缓存和错误语义全部一一对应；本实验只实测文本、非流式与 SSE，没有冒称验证工具/多模态/真实 OAuth。
- 多账号不创造额度，也不授权绕过提供方限制；订阅/OAuth 自动化调用和共享应核对当前服务条款。
- 请求正文、工具参数和响应都可能敏感；request-log/debug、凭证目录、管理 API 和远程监听要最小化开放。
- 本实验为确定性关闭额外重试；未验证真实 429、配额重置、OAuth 刷新或云故障转移。
- PDF 为 Edge 无头打印 22 页，Q1-Q10 均有内联 SVG。HTML 封面已截图检查；本机缺 pdftoppm，隔离安装 PyMuPDF 被权限层拒绝，未绕过，故 PDF 逐页像素审阅仍留给独立 reviewer。

## 产物

- 指南：`cli_proxy_api/cli_proxy_api-小白指南.pdf`
- HTML：`cli_proxy_api/cli_proxy_api-guide.html`
- 实验：`cli_proxy_api/exercise/`
- 入库合并建议：`cli_proxy_api/cli_proxy_api-knowledge-proposal.md`
