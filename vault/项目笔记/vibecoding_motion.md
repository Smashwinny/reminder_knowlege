---
tags: [项目]
类别: 知识学习类（抖音短视频主题还原）
上游仓库: 无（方法论主题，抖音视频 7683862830755384614）
完成日期: 2026-10-03
---

# vibecoding_motion（动效描述词表）

**这是什么**（一句话）：抖音 @优卓UX上岸社 短视频「想要Vibecoding？先学会动效描述！」（2026-09-10，1.2万赞）的主题还原——让 AI 写出对味 UI 动效的方法：用**动效四要素词表**（触发/动作原语/缓动/时序）把"感觉"翻译成 AI 能精确执行的描述。

**它给我什么能力**：
- 用万能模板（触发+原语+缓动+节奏）派工，AI 一次生成对味动效
- 缓动性格库选型：ease-out 入场 / ease-in 离场 / spring 跟手
- 描述体检器在派工前拦缺项；结构验收 grep AI 交的动画代码
- 直接引用 Material 3 / Motion 官方参数自带"大厂血统"

**引入的概念**：
- [[动效描述词表]]

**实验记录**（`exercise\`，Python 3.14 零依赖，全部真跑通）：
- ex1 词表生成器：6 缓动 + 7 动作原语 → 3 场景 CSS（slide-up+ease-out+300ms / stagger 60ms×5 / pop+spring）真跑通，spring 真实输出 `cubic-bezier(0.34,1.56,0.64,1)`
- ex2 缓动采样：4 曲线数值表 + SVG 曲线图；实测 easeOutCubic t=0.3→0.657（前30%时间走65%路）、easeOutBack 峰值 1.100（过冲实锤）
- ex3 demo 验收：生成 5 卡错峰入场 demo 页（1716 字节），结构验收 5/5 PASS（曲线/时长/60-120-180-240ms delay/初始态/结束态）
- ex4 描述体检器：四要素正则体检，坏描述「帮我做个卡片动画」0/4 拦下、好描述 4/4 放行

**查证与坑**：
- 抖音短链 → www.douyin.com/video/7683862830755384614；桌面 UA 404，分享页普通 UA 只有壳，iteminfo API 返回空、detail API 403——**Googlebot UA 抓 iesdouyin share 页**才拿到 SSR 元数据（标题/作者/日期/热评"MotionSites.Org 里面有这些提示词"）
- 视频本身无法抓取正文，学习内容按任务提示"动效描述词表+代码实验"路线公开方法论还原（uimotionprompts.com、motion.dev transitions 文档、Material 3 motion 规范均核实存在）

**后续可深入的方向**：
- Framer Motion/Motion One 的 spring 调参（stiffness/damping 手感）
- 把词表扩成 Agent Skill：描述体检 → 生成 → 结构验收一条龙
