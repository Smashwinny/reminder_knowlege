---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/MemTensor/memmy-agent
完成日期: 2026-10-03
---

# memmy（Memmy 跨工具AI记忆系统）

**这是什么**（一句话）：跑在本机的开源个人记忆中枢（MIT，~2k★，MemTensor/MemOS 团队），让 Claude Code/Codex/Cursor 等所有 AI Agent 共享同一份长期记忆——四层记忆 + 奖励进化 + 4 通道混合检索，口号 "All AI remember the same you"。

**它给我什么能力**：
- 换工具不清零：新会话一句"帮我把这个项目找回来"，恢复目标/判断演变/产物/下一步
- 个人规矩只教一次（如 PYTHONUTF8、PDF 彩色偏好），所有工具都记得
- 本地 SQLite 存储、模型可全本地（Ollama + MiniLM 嵌入），数据零出机
- 当自研 Agent 的现成记忆后端：HTTP API（:18960）+ memmy-memory CLI + OpenAI 兼容网关（:18990）+ /viewer 面板

**引入的概念**：
- [[跨工具个人记忆层]]
- [[记忆四层模型]]（L1 Trace/L2 Policy/L3 World Model/Skill）
- [[混合检索与RRF融合]]

**实验记录**（详见 `F:\reminder\memmy\exercise\experiment-log.md`，全部真实运行）：
- Windows 源码构建跑通（npm run memory:build + node 直启，无 systemd），health 显示 sqlite+FTS5+sqlite-vec、四层 memoryLayers
- 五步闭环：手动 add L1 → 发现不配摘要 LLM 永远卡 summary_pending 不可检索 → 本地 Ollama qwen2.5:0.5b 做摘要 → local MiniLM 嵌入（21ms）→ 换词语义检索零词重叠命中
- 跨层验证：手写 L2 Policy，检索中四层同场排序 Skill(1.08)>L2(0.66)>UserMemory(0.53)>L1(0.26)
- 检索漏斗实测 raw 24 → ranked 6 → 阈值砍 18 → LLM 终筛留 4
- 坑：①config 带 profiles/activeProfile 的文档示例已是 legacy 直接报错，要用扁平格式；②ollama pull 被代理 fake-ip 触发 redirect 保护，curl 代理直下 GGUF + ollama create 旁路解决；③终筛模型太弱会误杀正确记忆（llmFilterEnabled:false 可关）；④autoScanKnownAgents 默认开，会自动导入本机 Claude Code 真实历史（实验库进了 54 条轨迹+1 个 Skill）

**后续可深入的方向**：
- 正式 `memmy-memory init --agent claude` 接入本机 Claude Code，验证 Hook 自动抓取 + turn 注入的日常体验
- Dream 定时整理与 L2→Skill 结晶参数调优（minGain/minSupport）
- 把 Gateway(:18990) 当 OpenAI 兼容记忆增强端点给其他客户端用
