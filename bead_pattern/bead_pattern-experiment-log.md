# 实验日志 · 拼豆图纸生成（bead_pattern）

- 任务：9574dd67-500c-4867-b781-44349665f22e
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 实验位置：`exercise/beadify.py`（231 行纯 Python 标准库）

## 实验设计

原帖只给了"可以赚钱"的结论和商品截图，没有任何方法。实验目标：自建"照片→拼豆图纸"管线并端到端验证——手写 BMP 解码、盒式降采样、24 色调色板最近色量化、HTML 图纸（网格+色号+用量）输出。

## 运行记录（全部真实执行，完整输出 exercise/run_output.txt）

1. **测试素材**：推文原图（945×2048 JPG）经 PowerShell System.Drawing 显式转 24 位 BMP（直接 Save 报 GDI+ 通用错误，改用 Graphics.DrawImage 绘制到 Format24bppRgb 位图成功，5.8MB）。
2. **self-test**：4/4 通过（纯红→R、近白→W、4×4→2×2 盒式均值、降采样尺寸保持）。
3. **convert 48 宽**：945×2048 → 48×104 豆格（4992 颗），21 色，前 5：W 1697 / LG 745 / GY 610 / CR 576 / DGY 308。生成 pattern48.html + pattern48.csv。
4. **convert 29×29**（单豆板规格）：841 颗，17 色，前 5：W 214 / LG 169 / CR 147 / GY 120 / DGY 54。生成 pattern29.html + pattern29.csv。
5. **真实 bug 修复**：首版图例生成把调色板 p[2]（r 分量 int）当颜色元组用，TypeError 真实报错；改为 PALETTE_MAP 元组切片后重跑通过。修复过程未掩盖，重跑记录在原 run_output.txt 之上。
6. **视觉目检**（exercise/check29.png，Edge 无头截图）：网格、符号、图例、用量表全部正确；色块结构与原图区域可指认对应（顶部黑发区 K、中部蓝区 B/DB、粉区 HP）。

## 结论

- "照片→拼豆图纸"用朴素算法（区域均值+RGB 最近色）即可达到商品级图纸的起点质量；瓶颈在调色板覆盖与感知均匀性，不在算法复杂度。
- 测试图是手机截图（白/灰 UI 占比大），用色统计被 W/LG/GY 主导——算法行为符合预期，非缺陷。
- 未验证项（诚实声明）：实体铺豆/熨制环节、真实品牌色卡 RGB 值、感知距离改进收益。

## 产物

- `exercise/beadify.py`、`exercise/run_output.txt`
- `exercise/test_photo.bmp`（测试素材）、`exercise/pattern29.html/.csv`、`exercise/pattern48.html/.csv`、`exercise/check29.png`（目检证据）
