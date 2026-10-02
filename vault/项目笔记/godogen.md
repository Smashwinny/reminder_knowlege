---
tags: [项目]
类别: 开源项目类（AI 游戏开发生成器）
上游仓库: https://github.com/htdt/godogen
完成日期: 2026-10-02
---

# godogen

**这是什么**（一句话）：一套"源码即 prompt"的自主游戏开发生成器——仓库里只有 Markdown 说明书 + 发布脚本，发布到空游戏仓库后由 Claude Code/Codex 照说明书自动完成架构设计、AI 美术、写码、引擎截图与视觉质检，交付可运行的 Godot 4 / Bevy / Babylon.js 游戏（GitHub ~7k 星，MIT）。

**它给我什么能力**：
- 一句话描述 → 完整可玩游戏（挂机托管收 15~20s 实机录像，或盯直播随时改需求）
- AI 美术全流水线：2D 图（Gemini/Grok ~6-7¢/张）、3D 模型+骨骼动画（Tripo）、帧动画（Grok 视频）、抠图（rembg），带成本治理（花钱前确认、kit 贴图集省生成费、资产尺寸登记表）
- 三份"静默失败陷阱"引擎指南，任何引擎的 AI 开发都能直接抄
- "发布期渲染"范本：一套 Markdown 模板 × 变量 → 6 种引擎/宿主口味

**引入的概念**：
- [[源码即Prompt]]（thin runtime + 发布期渲染）
- [[证据优先质检ProofOverClaims]]（proof over claims 视觉质检闭环）
- 构建期场景生成（build-time scene generation）：Godot 场景不用编辑器搭，写成 C# SceneTree 构建脚本无头跑一次吐 .tscn——AI 原生工作流的样本（owner 链设置、pack 后 Instantiate 数节点防静默丢节点）

**实验记录**（2026-10-02，本机无 Godot/无 API key，走轻量验证，全部真实运行）：
1. `exercise/publish_lite.py`（shutil 替代 rsync 复现 publish.sh）：发布 godot×claude 口味成功，CLAUDE.md/godot.md/.claude/skills/asset-gen 结构与变量替换全对
2. 发布 babylon×codex 口味 + 上游 generate_codex_metadata.py：AGENTS.md/.agents/skills + agents/openai.yaml 从 frontmatter 正确生成
3. `make_atlas.py` 画 1024² 四格道具集 → 上游 `grid_slice.py --grid 2x2` 切出 4 个 512² sprite，成功/失败 JSON 输出均验证
- 坑：Windows Git Bash 无 rsync，publish.sh 跑不了 → 用 shutil.copytree 等价复现；msedge 不在 PATH → 用全路径 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" 打印 PDF

**后续可深入的方向**：
- 装 Node 20+ 走 Babylon.js 路线（门槛最低）：publish 出仓库让 Claude Code 现场生成一个浏览器小游戏
- 云 VM + tmux 挂一次完整 Godot 生成，观察 README 状态落盘与视觉质检循环的实际行为
- 把"状态落盘 + 证据优先 + 静默陷阱清单"三板斧平移到自己的 Agent 项目运行时清单
