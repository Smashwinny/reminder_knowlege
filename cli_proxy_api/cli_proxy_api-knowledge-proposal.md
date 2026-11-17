# cli_proxy_api 知识入库提案（worker w2）

> 本文件只是协调者合并建议。worker 未修改任何已有概念笔记或总览；仅另建 `vault/项目笔记/cli_proxy_api.md`。

## 查重结论

已只读核对：`负载均衡与反向代理`、`Provider适配层与错误契约`、`BYOK模型网关与用量归因`、`控制面与数据面`、`能力层与后端路由`、`统一数据网关` 和项目笔记 `magpie_gateway`。

不建议新建重复概念。CLIProxyAPI 与 magpie 同属多协议模型网关，但本项目提供以下可复核增量：

- 官方 `router-for-me/CLIProxyAPI` v8.0.47，commit `90c447d3`，Windows 官方发布包 SHA-256 与 GitHub Release digest 一致。
- 真实运行而非仅源码结构检查：Claude Messages → OpenAI Chat Completions 的请求/响应双向翻译、Claude SSE 生命周期、alias 映射、客户端鉴权。
- 用本机 mock 的 Authorization 与 payload 证明 round-robin 为 A/B/A/B，改 `fill-first` 重启后为 A/A。
- v8 配置树将客户端 `access.api-keys`、上游 `api-keys.*`、OAuth `oauth.auth-dir` 和管理 `management.secret-key` 分开；`/v8/management` 与数据面权限不同。
- 明确版本差异：go.mod 已为 `/v8`，旧中文 SDK 文档仍有 `/v6` 示例，不能照抄。

## 建议合并到已有概念（由协调者执行）

### `BYOK模型网关与用量归因`

可追加 CLIProxyAPI 实证样本：它既能接 API key，也能把 CLI/OAuth 凭证作为上游，但不是推理引擎，不创造模型能力或额度；v6.10.0 起完整用量统计由外部工具承担，不能把管理面等同完整账单。链接 `[[项目笔记/cli_proxy_api]]` 与 `[[项目笔记/magpie_gateway]]` 互相对照。

### `Provider适配层与错误契约`

可补充 Executor/Translator 分工：Translator 负责请求、非流式响应和流式响应格式；ProviderExecutor 负责出站 HTTP、凭证注入与 provider 细节。协议兼容是逐特性工程，字段、内容块、工具参数、SSE 生命周期、停止原因与 usage 都要验证。

### `负载均衡与反向代理`

可补充本机实测序列：round-robin A/B/A/B 与 fill-first A/A；同时区分候选起点选择、会话亲和、冷却与额外重试轮数，不能把这些统称为“负载均衡”。

### `控制面与数据面`

可补充三个权限边界：客户端 key 管数据面入口，上游 key/OAuth 管真实模型调用，management key 管配置与凭证控制面；管理路由留空 secret 可关闭，remote 默认受限。

### `能力层与后端路由`

可关联模型注册表与 alias：客户端稳定名称与上游真实 name 解耦；路由只选择可用上游，不替 Agent 发明新能力。

## 不建议新建的独立概念

- “CLIProxyAPI”本身放项目笔记，不新建概念。
- “协议翻译”已由 `Provider适配层与错误契约` 覆盖，增补即可。
- “多账号轮询”已由 `负载均衡与反向代理` 覆盖，增补即可。
- “BYSOL/订阅凭证化”已在 magpie/BYOK 笔记出现，避免另起同义笔记。

## 来源

- https://x.com/0xlangeai/status/2106264636198908382 （原帖 WebFetch HTTP 402，未读到逐字正文）
- https://github.com/router-for-me/CLIProxyAPI
- https://github.com/router-for-me/CLIProxyAPI/releases/tag/v8.0.47
- https://help.router-for.me/

## 证据文件

- `cli_proxy_api/exercise/experiment_log.txt`
- `cli_proxy_api/exercise/experiment_results.json`
- `cli_proxy_api/exercise/runtime/upstream_requests.jsonl`
- `cli_proxy_api/exercise/runtime/proxy_stdout.log`
- `cli_proxy_api/exercise/artifact_validation.json`
