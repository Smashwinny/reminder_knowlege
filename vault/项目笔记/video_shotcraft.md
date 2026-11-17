---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/Vincentwei1021/video-shotcraft
固定版本: 1266a3e
学习日期: 2026-10-31
---

# video_shotcraft（video-shotcraft）

**这是什么**：面向 Claude Code / Codex 的产品宣传片制作 skill 与资产库。Agent 采集真实页面与文案，从 124 张配方卡/150 个镜头中选择运动语法，使用 Remotion 完成动画、音乐卡点、音效和逐帧验收，交付 MP4、可编辑源码、Motion Workbench，以及可选剪映草稿。它不是视频生成模型；当前 focus 是 Web/桌面产品宣传片。

**来源核验**：原 X 主帖本轮直连 HTTP 402；FxTwitter 镜像读到同作者主帖和引用开源帖，引用帖明确出链到精确仓库。历史 404 已变化，本轮成功克隆 `Vincentwei1021/video-shotcraft` 并固定在 `1266a3e`。没有绑定同名搜索项目；星数和 opus5.5 能力仅为作者陈述。

**本次增量**：
- [[镜头配方三读契约]]（提案）— Gallery 索引 → 配方卡全文 → 准确 demo TSX；demo 是缓动、时值和命门的参数真相。
- [[音画双偏移钉帧]]（提案）— 目标峰值帧同时减音源内部峰值滞后和当前输出音轨偏移，旧常数不可跨管线搬运。
- [[同源可编辑视频清单]]（提案）— Main 与 Workbench 共享时间表，component+props+schema 拆多轨，original/imported 同帧对照验证无损。
- 产品镜头：单主角完整动作弧、真实截图三件套、PageCam 2.5D、hold/rest 帧预算；转场按接缝语义三选一，不叠加炫技。

**复用的旧知识**：[[React逐帧视频渲染]]、[[分镜表驱动生成]]、[[声明式视频源语言]]、[[补间动画与缓动函数]]、[[证据优先质检ProofOverClaims]]。本笔记不重复解释通用 Remotion。

**真实实验**：`exercise/shotcraft-lab` 独立渲染 180 帧/6.016 秒、960×540、30fps、H.264+AAC 产品片。完成产品主角镜头、10f 暖白闪、3 条相对钉帧 SFX 和 Workbench 清单；查看 f36/f89/f120/f140 四张 QA 帧。三音源 10ms RMS 峰值滞后分别为 21.75/16.65/13.65f；三探针测得 Remotion 4.0.532 管线输出偏移 +0.01/+0.01/-0.01f。真实 TS 清单执行断言通过 2 镜头+1 转场+1 字幕+3 音效。详见 `exercise/experiment-log.md`。

**产物**：`video_shotcraft/video_shotcraft-小白指南.pdf`（13 页）与 `video-shotcraft-guide.html`。

**限制与坑**：
1. npm 安装被权限层拒绝，实验复用本机 Remotion 4.0.532；未原样渲染上游 4.0.484 Ink Press 模板。
2. 未启动完整 Workbench UI、未跑官方像素 parity；清单执行通过不等于官方无损验收通过。
3. 实验音频为模板中授权记录可回查的 Mixkit 历史回归素材，保留 attribution；未执行 Freesound 在线选音。
4. 10ms RMS/sample peak 不是 LUFS/true peak，也不自动等于语义落点；未宣称主观试听通过。
5. Windows 剪映导出、模型效果比较未验证。worker 仅 ready，等待协调者独立审核与共享知识合并。
