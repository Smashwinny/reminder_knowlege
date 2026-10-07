---
tags: [项目笔记, 图像处理, 像素画, 手工]
created: 2026-10-07
---

# bead_pattern（拼豆图纸生成）

- 来源：@红鱼 HYhongyu8 推文 https://x.com/HYhongyu8/status/2107169090737770771（配图=闲鱼"拼豆图纸定制"商品 ¥49–99）
- 实现：本仓库 exercise/beadify.py（231 行纯标准库，self-test 4/4，真实照片端到端实测）

## 是什么

把任意照片自动转成拼豆（perler beads）可施工的像素图纸：照片 → 盒式降采样到 W×H 豆格 → 24 色入门调色板最近色量化 → HTML 图纸（色块网格 + 符号 + 图例 + 用量 CSV）。

## 实测数据

- 945×2048 测试图（推文截图转 BMP）→ 48×104 格 4992 颗 21 色；29×29 单豆板 841 颗 17 色；端到端 <1s。
- 视觉目检通过（check29.png）：区域结构可指认对应。

## 关键经验

- 尺寸表：29×29 单豆板（钥匙扣级）/ 48×80 中幅（商品主流）/ 87×93 大图拼接；人脸辨认需脸部 ≥20 格宽，高度按照片高宽比自动算。
- 色差来源：RGB 欧氏距离非感知均匀 + 色板覆盖有限；对策 = 感知距离（CIEDE2000）、Floyd–Steinberg 抖动、真实品牌色卡、人工校对肤色/发色。
- 零依赖技巧：JPEG/PNG 解码要库 → 用 PowerShell System.Drawing 显式转 24 位 BMP 再手写解析（注意直接 Save 可能 GDI+ 报错，需 DrawImage 重绘）。
- 副业现实性：图纸边际成本近零但无壁垒、手工熨制产能封顶、平台压价——练手+赚材料费可行，稳定收入不现实。

## 复现

```bash
cd exercise
python beadify.py self-test
python beadify.py convert test_photo.bmp --width 29 --height 29 --out pattern29.html
```

## 关联

- [[像素化渲染管线]]（同族像素化思想，3D 渲染语境）
- [[证据优先质检ProofOverClaims]]（对"AI 接单赚钱"帖的态度）
- 概念提案：调色板量化与拼豆图纸（见项目目录 knowledge-proposal.md，协调者终审）
