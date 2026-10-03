---
tags: [概念]
领域: AI/视频
别名: [Remotion, 组件化视频渲染]
首次来源: "[[项目笔记/ai-video-pipeline]]"
---

# React逐帧视频渲染

**一句话定义**：Remotion 把视频当成 React 组件来渲染——每一帧都是组件在给定帧时间点的一次绘制，props（数据）进、mp4 出。

**属于领域**：AI/视频（程序化视频生产）

**通俗理解**（比喻/例子，讲完落回术语）：传统剪辑像手工拼胶片（人拖时间轴），Remotion 像"视频版的网页开发"：写一个组件 `EvidenceCard`，传入"第几句台词、从第几秒到第几秒"，渲染引擎逐帧把它画出来再编码成 mp4。落回术语：Composition 声明画布与 fps，`calculateMetadata` 可由外部数据（如真实 TTS 音频时长）动态算总帧数，`<Sequence>` 按帧号排布子组件，`<Audio>` 挂音轨——时间轴完全由数据推导，不存在人工对齐。

**与已有概念的关联**：
- 相关：[[分镜表驱动生成]]（Pixelle 用 Storyboard JSON 当传送带——同样数据驱动，但 Remotion 的每一帧是组件代码自由绘制，表达力更强）
- 相关：[[声明式视频源语言]]（hypit SVML 把视频当源码写、台词锚词不锚秒——SVML 是 DSL，Remotion 是通用组件框架）
- 相关：[[补间动画与缓动函数]]（组件内插值动画的数学是同一套）
- 相关：[[JSON-IR类型化中间表示]]（LLM 只填数据表、确定性渲染器出画面——Remotion 是合格的确定性渲染器）

**首次接触于**：[[项目笔记/ai-video-pipeline]]（Simon聊AI 热点长视频流水线，ex3 实测：Remotion 4.0.532 真渲染 1002 帧 33.4s 成片）

**实测坑**：
- `--props` 传参必须按组件 props 的形状包一层（如 `{"timeline": {...}}`）；key 缺失会静默回退 defaultProps，渲染"成功"但画面是占位符——要靠抽帧检查才能发现
- 渲染引擎自动下载 Chrome Headless Shell，首跑要联网
