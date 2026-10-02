---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/whyubel1eve/Mars-Editor (网页版) · https://github.com/whyubel1eve/Mars-Editor-APP (桌面版)
完成日期: 2026-10-02
---

# mars-editor（火星编辑器）

**这是什么**（一句话）：开源的 Markdown → 微信公众号排版工作台（官网 mars-editor.cc），核心原理是把 Markdown 渲染成全内联样式的富文本，粘贴进公众号后台一字不差；桌面版（Tauri）另有本地文件防丢失和 Claude Code / Codex CLI 接入。

**它给我什么能力**：Markdown 发公众号零手动排版；9-12 套主题一键切换；草稿本地 .md 零锁定；AI 在稿子文件夹里直接改稿、编辑器实时刷新；推公众号草稿箱 / 导长图 / 网页转 MD。

**引入的概念**：
- [[内联样式与富文本转换]] — 微信消毒机制 + markdown-it 全量规则覆盖 + 剪贴板双格式
- [[Tauri桌面应用框架]] — Rust 外壳 + 系统 WebView，对照 Electron
- [[本地优先与文件监听]] — 草稿即本地文件 + vault_watch 双向同步

**实验记录**（做了什么、结果、坑）：
1. 本地跑通网页版：`npm install && npx vite` → HTTP 200（Vite v7.3.6）。坑：workerd 的 postinstall 被脚本审批拦截致 npm install exit 2，但不影响 dev/build（workerd 仅 Cloudflare 部署用）。
2. 主实验：用项目自带 esbuild 把 `src/markdown.ts` 的 `renderArticle()` 打包成 Node 可跑模块（exercise\render_entry.ts → render.mjs），渲染含高亮/待办/提示条/脚注的样例文 → **4 项微信兼容性自动验证全 PASS**（0 class、0 <style>、0 <script>、块级标签 100% 带 style），内联 style 共 45 处。
3. 主题对比：classic/sakura/dark 三主题同一份 Markdown 输出色值完全不同（#2b2b2b / #ffe0ec / #c9d4c3），验证"主题=配色数据"。
4. 桌面版源码走读：agent.rs 确认 spawn `claude -p --output-format stream-json` / `codex exec --json`，JSONL 原样转发，AI 改 .md 文件靠 vault_watch 回灌界面。

**后续可深入的方向**：
- 桌面版本机跑通（需 Rust 1.95 工具链）+ 真机推公众号草稿箱（AppID/AppSecret + IP 白名单）
- 模仿 markdown-it 规则覆盖思路做自己的排版主题
- `cargo test` 走读 agent.rs 的 CLI 检测（PATH + npm 全局 bin + Homebrew + `.local\bin`）
