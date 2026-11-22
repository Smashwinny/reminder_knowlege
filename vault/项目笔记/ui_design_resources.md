---
tags: [项目笔记, UI 设计系统, 确定性检测, 设计规范]
created: 2026-10-27
---
# UI 设计四资源组合

getdesign.md（视觉规范）、libraries.dev（局部组件）、pbakaus/impeccable（审查修改）、nexu-io/open-design（持续工作流）的组合。

## 核心概念
- [[AI味确定性规则检测]]：字体、色相、对比度公式与结构模式机检化，命中即 fail-closed。
- [[产品事实与视觉方向分离]]：PRODUCT.md 存稳定产品事实，DESIGN.md 存易变视觉方向，分文件避免改配色污染定位。

## 实测
impeccable README 的 1 skill/24 命令/62 规则与源码一致，ai-color-palette/low-contrast/gradient-text/side-tab 等规则 ID 真实存在；PRODUCT.md 带 `impeccable:product-schema 1` 注释，四段结构齐全。自写迷你检测器对示例页 6/6 命中 AI 味，WCAG 对比度实算 2.85:1。

官方 Rust 引擎构建被权限层拒绝，未运行；其他三资源实操效果未验证。
