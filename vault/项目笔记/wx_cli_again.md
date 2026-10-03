---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/jackwener/wx-cli-again （Apache-2.0，771 stars，Rust；原 jackwener/wx-cli 于 2026-07 被 DMCA 下架）
完成日期: 2026-10-03
拾遗任务: 1c5dba8b-86f6-479a-be3c-9f1b5076c71b
---

# wx-cli-again（微信本地数据 CLI）

**这是什么**（一句话）：kabikabi（jackwener）的微信 4.x 本地数据命令行工具在 DMCA 下架后的重生版——单一 Rust 二进制（wx），查询/解密/导出会话、消息、联系人、朋友圈、公众号、收藏、附件图片，AI 友好输出 + SKILL.md 可装进 Claude Code/Cursor/Codex。支持 macOS/Linux/Windows 三平台。

**它给我什么能力**：
- 毫秒级查自己的聊天历史/全文搜索/按时段导出 markdown/JSON
- 给 Agent 接微信数据源：meta wrapper 新鲜度声明 + npx skills add 一键装技能
- .dat 聊天图片三档解码还原（兼容微信三代图片加密）
- 架构范本：daemon 缓存 + 在线打开 SQLCipher 的本地数据 CLI 范式

**引入的概念**：
- [[微信图片dat三档解码]] — legacy XOR magic 反推 / V1 固定 AES key / V2 AES+XOR 平台派生 key
- [[daemon缓存与在线解密]] — mtime 缓存复用 + 在线打开加密库不落明文副本
- [[meta新鲜度声明]] — `{data, meta}` wrapper：status/unknown_shards/双源时间对账，写给 agent 看的成色标签
- 关联强化：[[进程取钥与副本解密]]（wx 取钥是它的 task_for_pid+LLDB 变体，且声称不关 SIP）、[[CleanRoom只读读取器]]（query_only 只读边界）

**实验做了什么**（exercise\decoder_lab\，全程零真实微信数据）：
1. rustup 装工具链；Windows 首坑：GNU 工具链调 D:\MinGW 的坏 dlltool（Invalid bfd target）→ 改 MSVC（VS BuildTools 18 + vcvars64）编译通过
2. `wx --version` / `wx --help` / `wx doctor` 真实输出：无密钥环境如实体检（未复验取钥路径）
3. 核心实验 decoder_lab：上游 decoder 源码原样拷贝进独立小 crate，合成 87 字节 PNG 往返——legacy_xor（key=0x5A 自动反推）✅、v1_aes（真实容器格式 + 固定 key cfcd208495d565ef）✅；负向三拒（全零垃圾/空文件/V2 缺 key）✅

**坑与结论**：
- 原仓库 jackwener/wx-cli 已被 GitHub DMCA 封锁（gh API 451，2026-07-13 微信投诉），学习对象是其公开重生版；README 宣称的发布仓库 botiverse/wx-cli 当前 private，实际安装路径只有源码自编译
- vendored OpenSSL 编译还需 perl（Strawberry Perl）；Windows 完整构建链 = MSVC + perl
- "取钥不需要关 SIP"（macOS task_for_pid + LLDB hook CCCryptorCreate）只能源码级研读，本机 Windows 无 macOS/SIP/LLDB 环境复验，诚实记录
- 结论：工程性能（daemon 毫秒级 + 在线解密）是赛道最强；护栏是"只读 + 免责声明"的口头契约级，精细度不如 [[项目笔记/yichen-skills]]，边界干净度不如 [[项目笔记/wechat-intelligence-hub]]；三平台支持是独家

**产出**：`wx_cli_again/wx-cli-again-小白指南.pdf`（彩色图文 12 问 + 5 步实验）

**首次接触于**：拾遗队列 task 1c5dba8b（X 推文 https://x.com/jakevin7/status/2100948204263202891，kabikabi"再度 public wx-cli"帖）
