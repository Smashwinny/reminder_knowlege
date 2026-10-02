---
tags: [项目笔记]
类别: 开源项目类
上游: https://github.com/bryllim/workout-guide
任务: 拾遗 4e83f48a（抖音 JavaPub《做健身 App 必备！302 个动作全部开源》）
完成日期: 2026-10-03
---

# workout-guide

## 它是什么
开源健身动作插画库：302 个动作 × 3 帧（起-中-止）= 906 张 512×512 统一风格 SVG（另发 PNG 兜底），附类型化 manifest 元数据（20 主肌群/17 器械/5 种计次类型/逐帧 CC BY-SA 4.0 溯源）和一个 80 行的框架无关 TypeScript npm 包 `@bryllim/workout-guide`（getExercise / searchExercises / getAssetUrl / normalizeSearchText），外加 Astro 在线画廊。GitHub 1.3k★，曾登周榜第 5。作者 Bryl Lim 在 Everkinetic 数据集（CC BY-SA 4.0）基础上重绘补帧，76/906 帧保留上游溯源标注。仓库为 npm workspaces monorepo：packages/workout-guide + apps/site + scripts（validate-catalog 等校验）+ Playwright e2e。

## 带来的概念
- [[内容型开源与双许可]] — 代码 MIT / 资产 CC BY-SA 4.0 按内容划界，逐帧 attribution 承接署名义务
- [[npm包即CDN源]] — jsDelivr 自动镜像 npm 包，版本号即灰度；坑：仓库内容 ≠ 包内容
- [[三帧关键帧插画法]] — 7KB/动作表达完整示范，钟摆式轮播；与 [[补间动画与缓动函数]] 互补

## 实验做了什么（全部真跑）
1. **manifest 对账 + 质检 Gate**（`exercise/01_manifest_audit.py`，零依赖）：302 动作 = 906 帧记录 = 906 磁盘 SVG；器械 Bodyweight 111/Dumbbell 45/Machine 35；肌群 Core 45/Glutes 38/Quads 35；质检 7 项 0 异常
2. **npm 包真装真调**（`exercise/npm-demo/02_api_demo.mjs`，Node 24）：装包 4 秒 35MB；search('press',{Dumbbell})=6、(chest,bodyweight)=12；normalize("Café & Lunge!")="cafe and lunge"；查无返回 null
3. **302 动作图鉴浏览器**（`exercise/03_build_gallery.py` → `exercise_gallery.html` 139KB + assets_svg 2.3MB）：302 卡片、肌群/器械筛选、CSS 三帧 steps 悬停播放；Edge 无头截图验证全渲染

## 坑与结论
- **npm 发布的 manifest 帧路径是 .png**，仓库内才有 svg（svg 是矢量源，包只发 PNG）——"仓库内容 ≠ 包内容"
- **getAssetUrl 自定义 baseUrl 拼出 assets/assets/ 双前缀**——frame.path 自带 assets/ 前缀，baseUrl 应指向包根
- **SVG 白色线稿+透明底**，浅色背景上直接隐身，官方画廊是深色主题；自建 UI 给深色容器
- 结论：做健身 App"图的部分"成本可归零；数据集项目的可信度 = 声明数/文件数/字段值三方对账，不靠宣传

## 产出
- `workout-guide/workout-guide-小白指南.pdf`（12 问彩色 + 实验卡 + 记忆卡）
- `workout-guide/wg_guide.html`（PDF 源）
- `workout-guide/exercise/`（3 个实验脚本 + npm-demo + 图鉴 HTML + 906 帧 SVG 资产）
