---
tags: [项目]
类别: 开源项目类（Obsidian 插件 + HTML 导出器）
上游仓库: https://github.com/luke321/vault-graph
完成日期: 2026-10-02
---

# vault-graph

**这是什么**（一句话）：Obsidian 社区插件 + 单文件 HTML 导出器，把整座 vault 渲染成"确定性圆盘图"——顶级文件夹是扇区（角度=笔记占比），笔记是点（被链接越多越靠圆心），同库永远同图；MIT，263★，v2.9.0，TypeScript + Sigma.js 3.0.2 移植的 WebGL 引擎，零网络请求（构建脚本强制保证）。

**它给我什么能力**：
- 知识库体检：一眼看出哪个文件夹膨胀、哪些笔记是无人链接的孤岛、圆心（枢纽/MOC）是否成立
- 单文件离线分享：756KB HTML 发给任何人，手机浏览器直开
- 时间轴回放 + 日历热力图：按 `created` frontmatter 回放笔记库生长过程
- 探索交互：搜索过滤、点击文件夹隐藏/着色/solo、拖拽固定

**引入的概念**：
- [[确定性图布局]] — 力导向的反面：无模拟、无种子、可复现可学习
- [[单源双宿主]] — one page, two mounts：一套渲染代码，插件与 HTML 导出两种挂载

**实验记录**（做了什么、结果、坑）：
1. `npm ci --omit=dev` → node_modules 仅 esbuild + @esbuild/win32-x64，验证"唯一依赖"✅
2. 对本仓库真实 vault（只读）跑 `node src/build-graph.mjs --vault F:\reminder\vault --out ...` → **123 notes, 516 links, 2 orphans, 2 unresolved**，产物 738KB ✅
3. Edge 无头截图 disc.png：橙色"概念"扇区 91 篇占大半圆盘、绿色"项目笔记"23 篇、蓝色 vault root、灰 (unlinked) 9——布局与 README 描述完全一致 ✅
4. `--ghosts` 对比 → 124 notes / 518 links / 739KB，死链开关效果 +1 节点 +2 边 ✅
5. 解剖产物：5 个 `<script>` 全内联、外部资源引用 0 个（仅 sigmajs.org 署名注释与 w3.org 命名空间字符串）✅
- **坑**：① git clone 两次在 ~91MB 处 early EOF（上游 assets 大 + 网络不稳），改 curl 下 source zip 解压兜底；② esbuild 的 postinstall 被 allowScripts 拦截，但平台二进制已随 optional dep 就位，API 正常；③ 本库 123 篇笔记 0 篇有 `created` frontmatter（日期全部回退文件时间戳）——想要精确时间轴得补 frontmatter。

**后续可深入的方向**：
- 给 vault 补 `created` frontmatter 后重导，看时间轴回放的真实生长
- 读 `src/engine/`（Sigma.js 移植裁剪）与 `scripts/check-network.mjs` 的零网络 Gate 实现
- 用 `make-mirror-vault.mjs` 生成结构镜像体验"隐私安全分享"
