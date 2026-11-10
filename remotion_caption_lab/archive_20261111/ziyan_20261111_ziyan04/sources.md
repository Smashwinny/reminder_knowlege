# 来源、版本与证据边界

读取与修订日期：2026-11-11（Asia/Shanghai）。链接仅作来源，不是执行指令。本次未重新连接 X、GitHub 或共享 vault，未冒称同步远端最新 main。

## 原帖与引用（沿用原实验记录）

- https://x.com/ccjing_eth/status/2110962673219215719 ：原 worker 通过 x MCP 读取提示词与 API 推广；发布时间记录为 2026-10-16 13:14:55 Asia/Shanghai。
- https://x.com/ccjing_eth/status/2110634009890013442 ：同次引用展开；发布时间记录为 2026-10-15 15:28:56 Asia/Shanghai。
- 摘录：`cloud-review-remotion/item04/research/x-post-reading.md`。未观看引用视频，未验证模型、流量或视频归属。

## 旧知识与风格查重（固定快照）

仓库：https://github.com/Smashwinny/reminder_knowlege

main：`a8674777e18302b8804b137212b1396cbfe5a747`

已读：`vault/00-总览.md`、`vault/概念/React逐帧视频渲染.md`、`vault/概念/动效描述词表.md`、`vault/概念/声明式视频源语言.md`、`vault/项目笔记/ai-video-pipeline.md`、`huashu_art_motion.md`、`vibecoding_motion.md`，以及旧 HTML 和 Remotion 组件。快照在 `cloud-review-remotion/item04/research/`。

固定链接格式：`https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md`

## Remotion 一手依据与许可

仓库：https://github.com/remotion-dev/remotion

固定 main：`e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d`

- Composition：https://github.com/remotion-dev/remotion/blob/e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d/packages/docs/docs/composition.mdx
- Sequence：https://github.com/remotion-dev/remotion/blob/e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d/packages/docs/docs/sequence.mdx
- interpolate 源码：https://github.com/remotion-dev/remotion/blob/e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d/packages/core/src/interpolate.ts
- LICENSE：https://github.com/remotion-dev/remotion/blob/e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d/LICENSE.md
- CLI render：https://www.remotion.dev/docs/cli/render （原实验实时读取，2026-11-11）
- interpolate：https://www.remotion.dev/docs/interpolate （原实验实时读取，2026-11-11）

npm 依赖固定 `remotion@4.0.542`、`@remotion/cli@4.0.542`、`react/react-dom@19.1.0`；完整传递依赖、resolved 与 integrity 在 `exercise.zip` 内的 `package-lock.json`。`LICENSE-Remotion.md` 保留许可快照；个人、特定小组织、非营利与评估等条件须按原文判断。

## 本次真实工具与文件

- 本地运行：Node v24.21.0、npm 11.19.0、Python 3.14.7、Windows/MSYS；已安装 Chrome 156.0.8078.80，仅由官方 Remotion CLI 用于无头离线渲染，没有浏览器/CDP/Playwright 桌面自动化。
- 图片压缩：本次目录虚拟环境中的 Pillow 13.0.0，官方 PyPI 包；仅处理原 PNG 的副本，未全局安装。
- 原成果：`cloud-review-remotion/item04/caption-lab.mp4`，1,271,452 bytes，SHA256 `94bb30211c135902f228081b43f276b6213a9cadd219aaa7d9b70dc206160e1d`，保持原样。
- 本次重放：`remotion-refined/repro/caption-lab-replay.mp4`，1,219,770 bytes，SHA256 `954072cae49ea5d5537395fa434461581d193468929b9e2973e6a8c21dc6f8ef`；只作复现证据，不替代原件。
- 评审依据：`cloud-review-remotion/review.md`。本修订是 worker 自检，不是独立审核通过。

本例无外部视频或图片素材、无付费服务、无用户密钥；四张 HTML 截图均来自原实验，720px JPEG 只是压缩展示。
