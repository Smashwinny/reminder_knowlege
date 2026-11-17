# Easel 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：2d0c56c5-2401-4371-b440-0fea9196ae5e（与同项目 a39cd206 记录合并为同一项目，勿重复建项目笔记）
> 项目目录：F:\reminder\easel ｜ 实测 main@5a597e5

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 账号画像六维模板
- 一句话定义：用六个 Markdown 文件（identity 定位 / style 风格 / audience 受众 / platforms 平台 / preferences 偏好与红线 / memory 长期记忆）把一个"账号是谁"资产化，换号即换目录，创作时整体注入上下文。
- 领域：AI 工具生态 / Agent 记忆
- 已有概念关联：[[角色提示]]（长期化文件版）；[[三层记忆]]（memory.md 即其 L3 层的显式实现）；[[决策记忆结算反思闭环]]（写回机制同构）
- 来源项目：easel（profiles/_template 实测六文件齐备）

### 2. 出站内容分级闸门
- 一句话定义：AI 内容发布前的确定性安检分两级——BLOCK 级（真实敏感信息：密钥/内部地址/env 真值）fail-closed 退出 7 必拦；WARN 级（AI 措辞/模型名）只提醒不拦；显式 --allow-unsafe 才放行。
- 领域：AI 工具生态 / 安全
- 已有概念关联：[[护栏模式Guardrails]]（出站特化版）；[[技能路由器与授权硬门]]（同语言：硬拦 vs 提醒）；[[代码管边界提示词管判断]]（边界归代码的实例）
- 来源项目：easel（content_guard.py 实测：WARN exit 0 / BLOCK exit 7 / selftest 12 正例必拦）

## 二、项目笔记（建议新建 vault\项目笔记\easel.md，合并两条来源记录）
- 项目是什么：ZJU-REAL/Easel，4.1K★，Apache-2.0——浙大 REAL Lab 的自媒体全流程 Agent 工作台（OpenClaw 底座 + 113 技能 + 七平台），五段工作流：发现/策划/创作/发布/归因
- 带来的概念：[[账号画像六维模板]]、[[出站内容分级闸门]]
- 实验做了什么：六维画像核实、技能计数（实测 114-115）、content_guard 闸门三命令实测（WARN 放行/BLOCK 拦截/selftest 通过）
- 坑与结论：完整安装需 OpenClaw+Playwright+LLM key（未验证）；小红书官方建议人工发布；"自进化"=记忆写回非权重更新

## 三、合并建议（不新建，增补已有笔记）
- [[技能路由器与授权硬门]]：增补 BLOCK/WARN 分级设计的发布域实例
- [[决策记忆结算反思闭环]]：增补内容运营域的同款闭环
- [[三层记忆]]：增补"反膨胀写入纪律"（不是每次做完任务都写）
- [[AI热点长视频生产流水线]] 项目笔记：可互链（单点 deep workflow vs 全家桶 workbench）

## 四、MOC 更新建议
"AI 工具生态"或"AI / LLM 应用"分区增补两条新概念；项目索引加 easel。
