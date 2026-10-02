---
tags: [项目笔记]
项目: yichen-skills
类别: 开源项目类（Skill 合集仓库）
上游: https://github.com/mcncarl/yichen-skills
完成日期: 2026-10-03
任务: 拾遗 task 87966c7a（X 推文 https://x.com/gengdaJ/status/2097960663616471410）
---

# yichen-skills：逸尘微信生态 Skill 合集

## 这是什么

内容创作者逸尘（X @gengdaJ / GitHub mcncarl）的开源 Skill 仓库，**22 个 Agent Skill**（Claude Code / Codex 通用）：微信赛道 4 个（local-vault / mp-batch-exporter / mac-dual-open / windows-reader 融合版）+ 企微 2 个 + X 内容切片与文章上传 + ASR + 网页调研 + 剪映草稿等。推文只宣传了 4 个，仓库实际远超。许可：个人使用免费，商用须书面授权，TradeWinds 付费社群解锁商用——开源当漏斗上层的个人商业模式。

## 微信赛道四件套机制

| Skill | 机制 | 平台 |
|---|---|---|
| wechat-local-vault | Frida 首次取钥 → SQLCipher 解密到私密 vault → 全量/增量 + vault_cli 统一查询 + digest-source 群聊摘要素材包（history.json 锚点"从上次继续"） | Mac 4.x |
| wecom-local-vault | 企微 5.x 四条取钥路线（attach / 重签副本 / VM 扫描 / 已有 key），每条独立 `--confirm-*` 授权硬门，候选 key 须与库第一页验证成功才保存 | Mac |
| wechat-mp-batch-exporter | 公众号批量导出；三层计数口径铁律（publish_groups / expanded_url_items / original_articles）；完全体只对付费社群开放 | 跨平台 |
| wechat-windows-reader | Windows 明文快照只读：[[快照契约与不可变只读]] + [[派生会话ID与结构脱敏]]，不碰进程/密钥/解密/网络 | Windows（实验性） |

## 带来的概念

- 新增：[[快照契约与不可变只读]]（WAL sidecar 拒收 + UUIDv4 manifest + `mode=ro&immutable=1`）、[[派生会话ID与结构脱敏]]（sha256 域分离派生 chat_id + 只出 display_name）
- 关联强化：[[CleanRoom只读读取器]]（快照契约是其交接面加强版）、[[进程取钥与副本解密]]（local-vault 的 Mac 路线）、[[技能路由器与授权硬门]]（wecom 的 `--confirm-*` 分级闸门）、[[提示注入]]（`untrusted_snapshot_data` 标记）、[[证据优先质检ProofOverClaims]]（公众号三层计数口径）

## 四方位对比（本批次的定位功课）

| | intelligence-hub | wechat-ai-memory | Memmy | **yichen-skills** |
|---|---|---|---|---|
| 定位 | 情报库（CleanRoom） | 记忆流水线 | 记忆仓库 | **Skill 合集工作流** |
| 取数 | 授权 salt-key | Frida 取钥 | — | 四路线可插拔 + Windows 快照 |
| 独门 | 边界最干净 | 适配器隔离 | 记忆组织 | **工程化护栏最全** |

结论：边界干净度 hub > yichen > ai-memory，功能广度正好相反。yichen 的增量是**把护栏写进代码契约**而非文档建议。

## 实验做了什么（隐私红线内，全部真跑通）

`exercise/run_experiment.py`：用仓库自带 fixture_factory（wxid_alice_fixture 等纯虚构账号）生成合成快照，七步：validate PASS → chats（4 会话，仅 display_name）→ history（3 条）→ search 命中 zstd 压缩正文 → export Markdown（演示后即删）→ **负向×2：伪造 .db-wal 被拒 / 非 UUIDv4 manifest 被拒** → 修复恢复 PASS。上游测试套件 windows-reader 与 local-vault 各 21 用例全过。

## 坑与结论

1. **推文 ≠ 仓库**：推文 4 个 Skill，仓库 22 个，看仓库别只看宣传。
2. chats 输出找不到原始 wxid 是**脱敏设计**不是 bug（实验断言踩过）。
3. Windows 侧只有"明文快照"路线，取钥缺位；全量解析仍是 Mac 主场。
4. 批量导出完全体在私域（上游仓库曾被关、作者自维护版只对社群开放），公开版仅"已知 URL 下载正文"。
5. 双开 Skill 作者自述已弃用（弹出登录）——局限性写进文档是 Skill 工程的加分项。

产出：`yichen-skills/微信生态Skill合集-小白指南.pdf`（8 页，HTML 源同目录）
