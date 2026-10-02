# Memmy 动手实验日志（全部真实运行，2026-10-03，Windows 11 / Node v24.21.0 / Git Bash）

环境：源码构建（无 systemd，纯 Node 直启），本地 Ollama 提供 LLM，Memmy local embedding（transformers.js + Xenova/all-MiniLM-L6-v2），SQLite 存储。全程无云端 API，数据不出本机。

## 实验A（主实验）：五步跑通"写入→摘要→嵌入→语义找回"

### Step 1 构建 + 启动本地记忆服务
```bash
git clone https://github.com/MemTensor/memmy-agent.git repo && cd repo
npm install && npm run memory:build        # 产出 Memory/dist/src/server/index.js 和 cli/index.js
node Memory/dist/src/server/index.js --config ../exercise/config.yaml --port 18960
```
config.yaml（注意：README/docs 里带 `profiles/activeProfile` 的写法在 v1.2.0 代码里已判为 legacy 直接抛错，必须用扁平格式）：
```yaml
memmyMemory:
  version: 1
  storage:
    mode: local
    backend: sqlite
    sqlitePath: F:/reminder/memmy/exercise/memory.sqlite
    endpoint: http://127.0.0.1:18960
    token: local-token
  summary:
    provider: openai_compatible
    endpoint: http://127.0.0.1:11434/v1
    model: qwen2.5:0.5b
    apiKey: ollama
  evolution:
    provider: openai_compatible
    endpoint: http://127.0.0.1:11434/v1
    model: qwen2.5:0.5b
    apiKey: ollama
  embedding:
    provider: local
```
✅ 预期结果（真实输出）：`GET /api/v1/health` 返回 `"ok":true`，`storage.fullText:"fts5"`、`storage.vector:"native"`、`memoryLayers:["L1","L2","L3","Skill"]`，embedding 显示 `provider:"local", model:"Xenova/all-MiniLM-L6-v2"`。

### Step 2 写入三条 L1 记忆（手动 memory.add）
```bash
node Memory/dist/src/cli/index.js add "img2threejs 项目的坑：中文 Windows 默认 GBK 编码，跑 Python 前必须先 setx PYTHONUTF8 1，否则测试大量假失败" --token local-token
```
✅ 真实结果：返回 `stored:1`，trace id 如 `trace_47b1bd7666f4eaf61655`。
**坑（重要发现）**：刚写入时 processing state=`summary_pending`（"摘要排队中"）。`embedding-job-processor.ts` L362：摘要必须 LLM，未配置直接抛 `SummaryModelUnconfiguredError`——**没有 LLM 时记忆会永远卡在不可检索状态**，search 返回 0 candidates。

### Step 3 配置本地摘要模型，重试流水线
`memmy-memory reload-config` 热加载后对卡住的 trace 调 `POST /api/v1/memory/<id>/processing/retry`。
✅ 真实结果：45 秒内日志依次出现
```
[capture.summarize] 摘要成功（qwen2.5:0.5b 生成中文摘要）
[embedding] Embedding request succeeded, provider=local, model=Xenova/all-MiniLM-L6-v2, batchSize=3, durationMs=21
[worker] Worker drain completed, leased=3, succeeded=3, failed=0
```
再查 trace：`title:"如何在 Windows 上设置正确的编码以支持 Pyt..."`，`processing.state:"ready"`。
qwen2.5:0.5b 给出的摘要（真实输出）：「在 Windows 上设置正确的编码，以支持 Python 测试，可以通过在 Python 前先设置 x PYTHONUTF8 为 1。」

### Step 4 语义检索：换词查询也能找回（跨工具记忆找回的核心演示）
```bash
node Memory/dist/src/cli/index.js search "之前中文环境下Python 运行报错乱码怎么解决的" --verbose --token local-token
```
查询与原记忆**零词重叠**（"报错/乱码" vs "GBK/假失败"），仍命中。
✅ 真实结果：`injectedContext` 含 `trace_47b1bd7666f4eaf61655`（手动写入的 GBK 坑）+ `trace_8cfe2a490b43ab7ae1fb`（**服务自动扫描本机 Claude Code 历史导入的 deeptutor PATH 坑轨迹**，autoScanKnownAgents 默认开启，本次实验库自动导入 54 条真实轨迹 + 1 个 learn-project Skill）。检索日志统计：`raw 24 → ranked 6 → droppedByThreshold 18 → LLM终筛 → final 4`。

### Step 5 跨层写入与检索（L2 Policy）
```bash
node Memory/dist/src/cli/index.js add "Windows 中文系统跑任何 Python 项目前先 setx PYTHONUTF8 1，能预防 90% 的编码假失败" --layer L2 --token local-token
node Memory/dist/src/cli/index.js search "编码假失败怎么预防" --verbose --token local-token
```
✅ 真实结果：返回 `policy_6e46e78ebf5b967f402f`；检索 hits 排序 `Skill(1.082) → L2 policy(0.662) → UserMemory(0.531) → L1 trace(0.262)`——**四层记忆在同一检索里分层召回、按质量加分排序**。

## 实验B：LLM 终筛的坑（小模型误杀）
`search "PYTHONUTF8"`（精确标识符）：机械排序有 5 个候选、包含目标 L1 trace，但 qwen2.5:0.5b 终筛后只剩 Skill 和一条 UserMemory，**目标 trace 被小模型误杀**（`llm_filter:llm_filtered`，kept 2 / dropped 3）。
结论：`llmFilterEnabled` 默认 true，**终筛模型太弱会乱杀正确记忆**。实战要么配强模型，要么在 config.yaml 设 `retrieval.llmFilterEnabled: false`（保留机械排序 top6 fallback）。

## 实验C：其他真实踩坑记录
1. **config 格式**：README.zh-CN、docs/*/reference/memory-api.mdx 里的 `profiles/activeProfile` 示例已过期，直接抛 `memmyMemory legacy profiles require the registered runtime config migration`。以 `Memory/src/config/index.ts` 的 `resolveRuntimeMemmyMemoryConfig` 为准（扁平格式）。
2. **ollama pull 被代理打断**：fake-ip DNS（198.18.x）触发 Ollama 服务端 `redirect target not allowed` 保护，CLI 挂 `HTTP_PROXY` 无效（校验在常驻服务端）。旁路：`curl -x http://127.0.0.1:7890` 直下 GGUF（Qwen2.5-0.5B-Instruct Q4_K_M，491MB）+ `ollama create qwen2.5:0.5b -f Modelfile` 本地导入成功。
3. **Windows 无 systemd**：官方 install.sh 面向 Linux（systemd --user 服务），Windows 上源码构建 + `node` 直启即可，全部功能可用；CLI 的 `install --service-only` 在 Git Bash 下理论上支持（README 明确写了 Windows 请在 Git Bash 执行）。
4. 检索日志面板：`GET /api/v1/memory/logs` 能看到每次 search 的完整漏斗数字（raw/ranked/droppedByThreshold/llmFilter/final），调参非常有用。
