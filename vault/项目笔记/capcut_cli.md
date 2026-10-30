---
tags: [项目笔记, 视频编辑, 文件格式自动化, Agent 集成]
created: 2026-10-27
---
# capcut-cli 剪映草稿命令行

renezander030/capcut-cli（MIT，v0.31.1，master@f3d6c75）：非官方剪映草稿 JSON 命令行，Node≥18 零运行时依赖，让 Agent 直接创建和编辑工程文件。

## 核心概念
- [[工程文件自动化（File-format Automation）]]：GUI 软件无 API 时，直接读写其工程格式。
- [[版本感知 schema 读写]]：先探测版本，再按对应 schema 与多时间线目标对齐。

## 实测
源码构建通过。自造 PNG/WAV 后 quickstart 创建草稿并注册工程索引，lint 0 错误 0 警告；add-text 新增独立文本轨道；trim --dry-run 不写盘；每次写入自动保留 .bak。无 ffprobe 时图片用 5 秒占位并明确告知。

未验证：真实打开 CapCut 人工核验、8.7 多时间线路径、caption 和 render（分别需 Whisper/ffmpeg）。注意旧版命令注入问题，应使用新版本。
