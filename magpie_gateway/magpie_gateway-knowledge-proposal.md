# 知识入库提案 · magpie_gateway

- 任务：3fee3059-7297-47f6-9ba8-e0ba5fb8b635
- worker：kimi-pool-20261007-w1（2026-10-09）
- 查重范围：`vault/概念/`、`vault/项目笔记/`（magpie 零命中；[[BYOK模型网关与用量归因]] 概念已存在=本次学习为其旗舰实现样本）

## 提案 1：新建项目笔记（worker 已按裁定直接新建）

`vault/项目笔记/magpie_gateway.md` —— 已写入：定位（127.0.0.1:3425 网关+菜单栏面板）、四协议互译架构、订阅凭证化（claude 二进制+MCP 桥）、配置手术（80 适配器）、1425 测试密度、6/6 校验、ToS 灰区风险。

## 提案 2：概念更新建议（请协调者终审，非新建）

**更新 `vault/概念/BYOK模型网关与用量归因.md`**：追加"旗舰实现样本 magpie"一节——

- 能力三段进阶：BYOK（自带 key）→ BYSOL（自带订阅凭证化，驱动真实客户端二进制+MCP 桥接）→ 四协议翻译网关（OpenAI Chat/Responses+Anthropic+Gemini 归一化互译）。
- 架构通解：M×N 集成压成 M+N（一切代理化到本地网关，M 适配器+N 供应商插件）。
- 配置手术原则：改配置保注释保格式可回滚。
- 风险注记：订阅共享 ToS 灰区、凭证集中。
- 链接：`[[项目笔记/magpie_gateway]]`、对照 LiteLLM/One-API。

## 总览/索引更新

请协调者在 `vault/00-总览.md` 项目清单补一行 magpie_gateway（worker 不动总览）。
