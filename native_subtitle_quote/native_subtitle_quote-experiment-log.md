# 实验日志 · native-subtitle-quote-image（native_subtitle_quote）

- 任务：1b82f918-879f-4579-856d-c33c819488fd
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 仓库：chengyi-ai/native-subtitle-quote-image（浅克隆 08d6990，1832 stars，MIT）

## 实验设计

验证目标：测试套件真实运行（含合成视频端到端渲染）+ 成品目检。

## 运行记录（全部真实执行，exercise/run_output.txt）

1. 环境：Windows 11，Python 3.14.7，**无系统 ffmpeg**——模块经 imageio-ffmpeg.get_ffmpeg_exe() 取捆绑二进制（native_subtitle_stitch.py:20），测试通过证明兜底有效。
2. `python -m pytest tests/ -q -p no:cacheprovider --basetemp=<干净临时目录>`：**39 passed, 17 subtests passed in 9.12s，0 失败 0 错误**（本批首个全绿）。
3. 关键端到端用例（test_sample_band_and_render_with_synthetic_video）：ffmpeg lavfi 生成合成视频（testsrc2 640×360/10fps/3s）→ 脚本 sample 子命令真实取帧出候选 JPG → stitch 渲染。真实跑通。
4. 目检：仓库自带成品 chen-shu-simple-life.jpg（3:4，主图 70%+5 字幕条，文字清晰、人像无变形）已复制 exercise/example_output.jpg。

## 结构阅读实证（纯读取）

- SKILL.md 任务路由 + references/（端到端工作流/视觉风格/yt-dlp 与字幕）+ scripts/（check_environment/check_update/native_subtitle_stitch）。
- 双字幕模式伦理红线："原生字幕不重绘 · 脚本字幕不冒充原字幕"。
- 版式三细节：先拼源像素再统一缩放（防首句变形）/脚本模式主图 70% 起（句多降至 48%）/字幕条零间隙。
- 测试名即需求：几何保持（圆形不变形）、crop 不切字幕、窄字幕无黑边、未知模式回退 padding。

## 结论

- 工程质量高（39 项全绿+端到端合成视频实测），"自带 ffmpeg 运行时"免除环境地狱是值得抄的交付决策。
- 未验证（诚实声明）：真实视频出图（合成视频已证管线，版权考虑未用真实素材）；yt-dlp YouTube 路径未实测；涨粉故事属单方案例主张。

## 产物

- `exercise/run_output.txt`、`exercise/example_output.jpg`
