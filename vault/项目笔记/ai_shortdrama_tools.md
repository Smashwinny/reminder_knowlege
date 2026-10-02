---
tags: [项目]
类别: 开源项目类（AI 短剧工具链清单 + 深挖 Pixelle-Video）
上游仓库: https://github.com/ATH-MaaS/Pixelle-Video
完成日期: 2026-10-03
---

# ai_shortdrama_tools（AI 短剧工厂）

**这是什么**（一句话）：推主 @denziideng 整理的 8 个高星 AI 短剧开源项目清单，逐一 GitHub API 验货（8/8 全真，2 个因组织改名 301 重定向），并深挖其中最高星的 Pixelle-Video（28,581★，阿里国际 AIDC 团队，Apache-2.0）——"输入一个主题，自动写文案、配图、配音、加 BGM、合成视频"的全自动短视频引擎。

**它给我什么能力**：
- 零 API 费离线跑通"主题→成片"六阶段流水线（文案→配图规划→逐帧处理→片段合成→拼接→BGM 后期）
- 解说短视频可直接商用产出（书单号/科普号）
- 流水线+分镜表模式可平移到任何批量生成场景
- 8 项目选型地图：解说向（Pixelle/ViMax/huobao）vs 剧情向（BigBanana/Jellyfish/moyin/Toonflow）

**引入的概念**：
- [[分镜表驱动生成]]
- [[角色一致性锚定]]
- [[抽卡式与工业化生成]]

**实验记录**（做了什么、结果、坑）：
- exercise/ 五脚本（ex1~ex5）离线复刻流水线：预写分镜 JSON（字段对齐上游 StoryboardFrame）→ PIL 生成 5 张 1080×1920 配图并烧字幕 → edge-tts 7.2.7 真实联网合成 5 段 zh-CN-XiaoxiaoNeural 语音 → ffmpeg 逐帧 loop+shortest 切段（4.94/6.02/6.72/5.59/5.02s）→ concat -c copy 无缝拼接 → 上游自带 bgm/default.mp3 以 0.15 音量 amix 混音 → 成片 28.36s / 846 帧 / 590KB，体检脚本解码计数+分镜表闭环校验全 PASS。全程 0 元、约 2 分钟。
- 坑1：ffmpeg-python 两个 `input()` 不能链式连写，须分别建流再一起传 `output()`。
- 坑2：BGM 混音只把 amix 音频流传给输出会**丢掉视频流**，成片变纯音频；必须 video+audio 两路都写。
- 坑3：imageio-ffmpeg 不带 ffprobe，时长/帧数用 `ffmpeg -i` stderr 解析；统计行（video:316KiB）与进度行（frame= 846）是两行，倒序找含 `frame=` 的行。
- 坑4：Python `subprocess.run(["chcp",...])` 报 FileNotFoundError，删掉靠 PYTHONUTF8=1 即可。
- 验货方法论：链接失效≠项目造假——`saturndec/waoowaoo`→`waooAI/waoowaoo`、`AIDC-AI/Pixelle-Video`→`ATH-MaaS/Pixelle-Video` 都是 GitHub 组织改名 301；用 `api.github.com/repositories/{id}` 跟随重定向可确认真身。

**后续可深入的方向**：
- 装 ComfyUI/DashScope key 跑上游原版"真 AI 配图"流水线
- `uv run start_web.bat` 起 WebUI 浏览器内跑全流程
- 依 fastmcp 把"出片"注册成 MCP 工具给其他 Agent 调用
- huobao-drama 的 Mastra+SKILL.md Agent 技能架构值得另开一篇（注意 CC BY-NC-SA 禁商用）
