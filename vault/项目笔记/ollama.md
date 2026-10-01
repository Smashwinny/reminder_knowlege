---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/ollama/ollama
完成日期: 2026-10-01
---

# ollama（本地大模型运行器）

**这是什么**（一句话）：一条命令下载、一条命令对话的本地大模型"电饭煲"——模型下载器 + 推理引擎包装（llama.cpp 内核）+ 本地 OpenAI 兼容 API 服务器，三合一，Go 语言写成。

**它给我什么能力**：
- 隐私对话/文档分析（断网可用，数据不出本机）
- 给 LangChain、Claude Code 等当免费本地 LLM 后端（base_url 指到 `localhost:11434/v1` 即可）
- Modelfile 定制角色助手（类比 Dockerfile，配置进 git）
- 12GB 显存舒适跑 7~8B Q4 模型（每 1B 参数约 0.6GB）

**引入的概念**：
- [[本地推理引擎]] — 架构：CLI(遥控器) → server(Go 常驻，端口 11434，调度器) → 推理引擎子进程 → GPU
- [[量化与GGUF]] — Q4/Q8 有损压缩，模型体积的来源
- [[KV缓存与上下文]] — 显存账单 = 权重 + KV 缓存 + 缓冲
- [[内容寻址与镜像分层]] — models 目录 = manifests 清单 + sha256 blobs（照搬 Docker）
- [[LLM采样与温度]] — temperature/seed/thinking 三个旋钮

**实验记录**（7 个全部实测通过，详见 `ollama_local_llm\ollama-小白指南.pdf`）：
1. 手动按 registry v2 协议拉模型（manifest→blobs→sha256 校验→落盘），`ollama list` 认可
2. 首次对话 41s vs 常驻后 1s（调度器 keep-alive 默认 5 分钟）
3. `ollama ps`：0.6B 模型占 930MB（文件 522MB），100% GPU
4. think=true/false 对比：小模型关思考会胡言乱语（0.6B 实测）
5. 温度 0 + seed 42：三连发一字不差；温度 1.5 面目全非
6. `/v1/chat/completions` OpenAI 兼容接口验证通过
7. `ollama create poet`（Modelfile SYSTEM 诗人人设）生效

**坑与结论**：
- 本机代理 TUN fake-IP（198.18.x.x）触发 ollama 防 SSRF 检查 → `ollama pull` 报 "resolves to non-public"；`--insecure` 放松 TLS 校验不可取，改为 curl 手动按协议下载 + 自行 sha256 校验（脚本 `exercise\manual_pull.sh`）
- curl 访问 localhost 被代理拦截 502 → 必须 `--noproxy '*'`
- C 盘满导致下载中断（curl exit 23）→ `OLLAMA_MODELS=F:\ollama_models`（用户级已 setx）迁移模型库；重启 server 时要显式带此环境变量
- Windows 下中文 JSON 别内联进命令行（GBK 乱码）→ 存 UTF-8 文件 `--data-binary @file`
- bash 读 Windows Python 输出要 `tr -d '\r'`，否则 URL 带换车符 curl exit 3
- 显存不够先砍上下文（num_ctx）再考虑换小模型
