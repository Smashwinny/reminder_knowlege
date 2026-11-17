# cobalt_tools 知识入库提案

> worker：main-k3-w3  
> task：eb718d22-5026-44e2-af3d-86385cb4db84  
> 上游：imputnet/cobalt@a636575b09de1fc55d9b8cd98cac88f5f2f16b42  
> 边界：仅提出合并建议；未修改既有概念、总览或其他 vault 文件。

## 查重结论

已只读检索 `vault/00-总览.md`、`vault/概念/` 与 `vault/项目笔记/`，未发现 cobalt 既有项目笔记，也未发现与下列三个候选概念同义的已有笔记。

可复用并互链的已有概念：

- [[构建流水线与Pass]]：cobalt 的 normalizeRequest → extract → match → matchAction → createResponse 是具体媒体管线。
- [[统一数据网关]]：统一 JSON 出口聚合多平台差异，但 cobalt 面向公开媒体流而非商业数据 API。
- [[能力层与后端路由]]：按服务把统一请求交给不同适配器。
- [[负载均衡与反向代理]]：公网自托管的流量入口与多实例运维。
- [[缓存]]：隧道元数据可短期存内存或 Redis；不等于长期缓存媒体内容。
- [[数据源降级链]]：都需隔离上游不稳定，但本次没有验证 cobalt 自动跨服务降级，不能写成同一机制。
- [[证据优先质检ProofOverClaims]]：本学习只宣称跑通官方模块与本机 HTTP 契约，不把 fixture 成功写成平台下载成功。

## 建议新增概念 1：媒体处理响应契约

**一句话定义**：用 `tunnel / redirect / local-processing / picker / error` 五种状态，把“接下来由谁、对哪些媒体、执行什么动作”显式交给客户端，而不是假定每次只返回一个下载 URL。

**领域**：媒体工程 / API 设计。

**关键事实**：

- `tunnel`：经实例代理，必要时 remux/transcode。
- `redirect`：返回上游直接 URL。
- `local-processing`：返回输入隧道和输出说明，由客户端 merge/remux/transcode。
- `picker`：返回多个媒体项及可选音频。
- `error`：机器可读 code，可选 service/limit context。

**实测锚点**：同一自写 merge 夹具在 `localProcessing=disabled` 时为 tunnel，改为 `preferred` 后为 local-processing；单 URL Vimeo 形态夹具在 `alwaysProxy` 从 false 改 true 后由 redirect 变 tunnel。

**关联**：[[构建流水线与Pass]]、[[统一数据网关]]、[[项目笔记/cobalt_tools]]。

## 建议新增概念 2：短期签名媒体隧道

**一句话定义**：把媒体流处理计划短期保存，并用带身份、到期时间、HMAC 签名和解密参数的临时 URL 提供给客户端的流式代理入口。

**领域**：媒体工程 /  Web 安全 / 临时资源管理。

**关键事实**：cobalt 隧道 URL 含 `id / exp / sig / sec / iv`；默认 TTL 90 秒；缓存的是上游 URL、文件名、头部和处理参数等元数据，不是长期媒体内容。签名篡改实测返回 401。

**关联**：[[缓存]]、[[项目笔记/cobalt_tools]]。

## 建议新增概念 3：端侧媒体处理分流

**一句话定义**：通过请求偏好和实例策略，在服务端 FFmpeg 与客户端 libav.js 之间分配 merge、remux、mute、audio、gif 等媒体处理工作。

**领域**：媒体工程 / 前后端协同 / 边缘计算。

**关键事实**：`localProcessing=disabled/preferred/forced` 表达客户端意图，`FORCE_LOCAL_PROCESSING=never/session/always` 表达实例策略；最终响应还受动作类型约束。localProcessing 不是“是否下载到本地”的同义词，而是“合成/转码在哪里执行”。

**关联**：[[能力层与后端路由]]、[[项目笔记/cobalt_tools]]。

## 项目笔记处理建议

- 新文件已按授权写入：`vault/项目笔记/cobalt_tools.md`。
- 请协调者合并上述概念并更新总览；worker 未执行这些共享写入。
- 总览可将 cobalt_tools 放在“媒体工程 / Web API / 自托管”相关区域。
- 不要把 tiktokio.bio、greenvideo.cc 合并成 cobalt 的组件或官方实例；它们只是来源中的独立服务对照。
