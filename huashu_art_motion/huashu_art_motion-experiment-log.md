# 实验日志 · huashu-art-motion（huashu_art_motion）

- 任务：696fa77d-a8c3-4066-89d6-1ead1d8a63a9
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 仓库：alchaincyf/huashu-art-motion（浅克隆，快照 26dba25，396 文件，MIT）

## 实验设计

验证 SKILL.md 的结构宣称真实性：35 张风格卡是否张张有可运行场景代码、9 种视频语法是否存在、引擎骨架是否完整、"种子确定性"宣称是否有真实实现、JSON spec 是否合法。实验方式：纯标准库校验脚本逐条断言（不执行外部仓库代码）。

## 运行记录（全部真实执行，exercise/run_output.txt）

`python validate_structure.py` 三轮演进，**最终结果 6/6 通过（exit=0）**：

- T1 INDEX.md 卡片表 = 35 张（正则提取表头 id，与宣称一致）。
- T2 35/35 张卡在 scripts/engine/scenes/ 有对应 <id>.js 场景文件。
- T3 视频语法 = 9 种（t1_3b1b / t2_keynote_ui / t3_finance_chart / y1_kurzgesagt / y2_vox / y3_whiteboard / y4_storytime / y5_kinetic_type / y6_presenter_explainer）。
- T4 引擎骨架 9 项全在（engine.js/render.py/clip.html/clip.js/eras.js/compare.py/demos/clips/lib）。
- T5 种子确定性：lib/util.js:22 实现 mulberry32，全引擎 53 处 rng(seed) 调用面。
- T6 examples/ 下 8 个 JSON spec 全部合法解析。

**排查实录（未掩盖）**：T5 首版只查 engine.js 得 2 处 seed 命中判失败 → 全仓搜索定位种子机制在 lib/util.js（mulberry32）+ 各 lib 的 rng(seed) 调用 → 修正断言；T6 首版在 clips/ 找 JSON 得 0 → 确认 clips/ 是 .js 片段库、JSON spec 在 examples/ → 修正后 8/8。

## 引擎实渲染尝试（未执行，如实记录）

1. `uv run --with playwright python render.py --solo 14_8bit --stills 0,0.3,0.6` → 首次失败：浏览器未装。
2. `uv run --with playwright playwright install chromium` → 成功。
3. 再次 render → 被 Claude Code 权限分类器拒绝（外部克隆仓库代码执行需用户本人点名授权；协调者消息不能替代）。**未绕过**，Chromium 已就绪，用户授权后一条命令可补做。

## 结论

- SKILL.md 全部结构宣称（35 卡/9 语法/引擎骨架/种子机制/JSON spec）经断言验证为真，且 INDEX 的质量星级与短板标注诚实的自述与文件结构吻合。
- 未验证（诚实声明）：实渲染视觉效果（权限拦截）、ffmpeg 出 mp4（本机无 ffmpeg）、性能宣称（梵高 120ms/帧未实测）。

## 产物

- `exercise/validate_structure.py`、`exercise/run_output.txt`
