---
tags: [项目笔记]
项目: RuiC-card-skill
类别: 开源项目类（Agent Skill）
完成日期: 2026-10-03
来源: "抖音 @AI整活家 短视频（拾遗队列 task 8f9a2254）"
上游: "https://github.com/HRuiCcc/RuiC-card-skill (466★, MIT, clone 于 712fc9f)"
---

# RuiC-card-skill · 全息闪卡 Agent Skill

## 这是什么
一个**通用 Agent Skill**（不挑宿主，多模态模型都能用）：一句话或一张参考图 → 四层图 → 自动流水线 → 一张"会随视角流光、带层次景深"的 3D 闪卡网页 + 可编辑 Blender 工程。复刻的是小时候文具店门口的光栅闪卡。本批学习由抖音短视频入口溯源而来：视频文案与仓库描述逐字吻合，作者 HRuiCcc 为真实活跃开发者（另有 music-geshizhuanhuan 111★ 等）。

## 架构一分钟
- **SKILL.md**（宿主读的操作手册）：五层图职责表、七步工作序列、非显然不变量（材质名契约 / 视差公式 / "箔是材质不是画"）
- **scripts/**（确定性工具链）：validate_assets 体检门 → run_pipeline 一键（自动装 SHA-256 校验的便携版 Blender 到项目目录）→ build_card/export_web（场景+GLB 导出）→ verify_web.mjs（609 行零依赖 E2E 验收）
- **assets/web-template/**：Three.js 查看器，app.bundle.js 1.3MB 预打包**单文件**（防广告拦截插件误杀 per-module 请求——真实血泪注释），无 WebGL 时 CSS-3D 分层兜底；暴露 window.__holo 测试钩子

## 本次实验（全部真实运行，材料在 ruic_card_skill/exercise/）
| 实验 | 内容 | 结果 |
|---|---|---|
| 1 | Pillow 确定性自绘锦鲤卡四层图 + 体检门 | 首跑通过（subject 透明占比 90.05%）；四反例 3 拦 1 盲区 |
| 1b | 反例：尺寸不齐/无alpha/反色线稿/画布过小 | 前 3 拦截；**反色线稿骗过数值检查**（只查有暗有亮）→ 人眼复核不可省 |
| 2 | 棋盘格假透明确定性抠图 + 官方回归测试 | 与原始真 alpha **98.3% 像素一致**（平均差 1.93/255）；ALL TESTS PASSED |
| 3 | 手写 1512 字节契约 GLB + 无 Blender 无 AI 全链出卡 | WebGL 真渲染；两帧帧差 73.86 证动画；**官方 verify_web.mjs 33/33 全绿** |

实验 3 的关键：viewer 只依赖"几何 + 材质名"契约，所以几何可以是手写 GLB 里的两块平面（web_front/web_back）。两个首跑 FAIL（无 effects 层→1×1 占位纹理混入同画布检查；config 未写 appearance.finish→初始珠光点珠光无变化）都是**验收器前置假设**而非 viewer 缺陷——读判定行源码定位后补配置即全绿。

## 带来的概念
- [[分层UV视差公式]] — 立体感 = 层按带符号景深随视线平移，两层同 depth 即塌
- [[材质名契约重建]] — glTF 搬不动节点图 → 最小契约 + 双端各自重建
- [[棋盘格假透明修复]] — 假透明确定性还原 + 数值 Gate 的人眼双保险

## 坑与结论
1. **两层同景深 = 卡片变扁**：SKILL.md 点名的头号失败方式。
2. **全息效果画死进素材 = 材质变汤**：箔是材质不是画；相位必须跟视角，只跟时间像循环视频。
3. **线稿必须与主体同源派生**，重画必然漂移（[[角色一致性锚定]] 同款思想）。
4. **"ready"旗标不证明好看**：验收要比对真实渲染帧哈希，不是控件读数。
5. 中文 Windows 出 PDF：ASCII 临时名打印再改名（本指南照例踩过，guide.html → Edge 无头打印）。

## 产出
- `ruic_card_skill/RuiC-card-skill全息闪卡-小白指南.pdf`（12 问彩色，含 2 张真渲染实拍图）
- `ruic_card_skill/exercise/`：make_layers.py / make_glb.py / card/ / web/ / verification/（官方验收报告+20 截图）
