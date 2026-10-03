---
tags: [项目笔记]
项目: hypit
类别: 开源项目类
完成日期: 2026-10-03
上游: https://github.com/hypit-ai/hypit
---

# Hypit（hypit-ai/hypit）

**这是什么**：给 Claude Code、Codex 等编程 Agent 用的「视频语言 + 系统」（18.9k★，TypeScript，v0.2.17，2026-07-29 创建，修改版 Apache-2.0）——把参考视频"复刻"成一份完整的、纯文本的可编辑工作流（SVML 源文件），而不是一条钉死时间线的成片；换脸/换话/换语言只动对应部分，可批量出变体。来源：Rachel🥥 实测帖（用小Lin说参考视频 + Hypit 丢给 Codex 复刻爆款口播视频，产出"成片+可复用 Workflow"）。

**它给我什么能力**：① 读懂/手写一套视频源码（SVML/SVS/SVRUN 三种文件各司其职：源、外观包、运行清单）；② 让 Agent 当导演复刻爆款（约 $1/条 20s 口播，免费层可先验证创意）；③ 词锚定设计思想迁移到任何"多媒体跟数据走"的场景；④ 组件包复用（ranking/chat/interview 板子都是版本化包）。

**引入的概念**（2 个）：
- [[词锚定语义时间]] — 事件锚在词上而非秒上，配音一换画面自动重踩点
- [[声明式视频源语言]] — 视频当源码写，Agent 当作者，编译系统兜底

**互链的已有概念**：[[分镜表驱动生成]]（同构上游）、[[角色一致性锚定]]（锚定家族的空间维）、[[补间动画与缓动函数]]（事件怎么演 vs 何时演）、[[JSON-IR类型化中间表示]]（类型化中间表示同族）、[[AgentSkills技能包]]（分发形态）、[[内容型开源与双许可]]（许可模式）、[[机制流与资产流隔离]]（资产与触发分离）、[[人机协同Interrupt]]（plan 报价=花钱前的人工闸门）

**实验做了什么**（2026-10-03，Windows 11，零依赖路线——pnpm install 被安全分类器拦截，改用 Python 标准库直接解剖仓库源文件，诚实记录）：
1. **exp1 SVML 解剖器**（exercise/exp1_svml_anatomy.py）：解剖 reference.svml（329 行）——21 个 @hypit 官方能力包 + 1 本地组件包、8 个词锚事件配对 PASS、22 个 || 停顿、2 处读音可选 `<D|Dee>`、**硬编码秒数 = 0**；坑：SVML Script 文本允许裸 `<|>` 字符，标准 XML 解析器报 ParseError → 改用标签正则统计（方言自有词法）
2. **exp2 变体对账**（exp2_variant_diff.py）：reference vs 三个官方变体行级 diff——swap-host 相似度 **79.4%**（改动集中 presenter/提示词＝"换主持人只动相关镜头"实锤）；swap-topic 34.7%、swap-effect 35.5%（台词/B-roll 重写，排行榜组件与骨架保留）
3. **exp3 语义时间模拟器**（exp3_semantic_time.py）：ronaldo 段 37 实词+11 停顿+5 事件按 130/160/190wpm 展开——语速变化时锚点词时刻移动 0.4~2.6s，钉死秒数将全部错位穿帮；诚实说明：简化模型（固定 WPM），真实系统由 WhisperX 按实际音频对齐（官方 hypit measure --pace fast 估同段 9s）

**坑与结论**：
- ① "已开源"是**修改版 Apache-2.0**：产出归用户，但禁多租户 SaaS（两个外部用户各持 workspace 即算）、禁商用转售、禁去 LOGO——看见 Apache 徽章别当无约束
- ② 生成模型不是必须的：字幕/动效/代码画面免费可渲染；真人感口播才需要 Seedance/语音（$1/条级别）；`hypit plan` 强制先报价后花钱
- ③ SVML 不是严格 XML（Script 内联记号含裸 <、|），自己的解析器要按方言处理
- ④ 环境：Node 22.15+/pnpm 10.33/TS 5.9；`npx skills add hypit-ai/hypit -g` 装 Skill 即可用，不必克隆仓库

**后续可深入的方向**：真装可执行体跑 `hypit build` 渲染 semantic-composition 的纯代码示例（零生成费）；照 minimal-author-package 写一个"股票行情板"自定义组件；用 WhisperX 本地对齐做真词级时间轴复刻实验。
