# Easel 动手实验日志（task 2d0c56c5-2401-4371-b440-0fea9196ae5e）

实验日期：2026-10-27
环境：Windows 11，Python 3.14，Easel git main @ 5a597e5（浅克隆，1134 文件）
边界声明：完整安装需要 OpenClaw + LLM key + Playwright，本实验不安装不调用模型；
聚焦"不花钱即可验证"的结构性事实与发布安全闸门实测。

## 实验设计

围绕文章（雷霆大思考《浙大开源了一个自媒体智能体》）的三个卖点逐一核实：
①账号画像六维结构是否真实存在；②"113 个技能"是否属实、如何分层；
③"发布前检查"是不是真 Gate——找到 skills/shared/scripts/content_guard.py 直接实测。

## 步骤与真实输出

### 步骤 1：克隆与画像六维核实

```
git clone --depth 1 https://github.com/ZJU-REAL/Easel repo   # HEAD 5a597e5
ls profiles/_template
```
✅ 六维模板真实存在：`identity.md / style.md / audience.md / platforms.md / preferences.md / memory.md`

- `preferences.md` 内含三栏：**要做的 / 不做的 / 合规底线**（模板原文注释"绝对不能碰的：虚假宣传、医疗承诺、导流违规等"）
- `memory.md` 内含**内容洞察 / 踩过的坑**，且带更新纪律注释："此文件记录真正有价值的洞察，**不是每次做完任务都写**……不要在这里堆流水账"

→ 与文章宣称的"定位、风格、受众、平台、偏好与红线、长期记忆"六维一一对应。

### 步骤 2：技能计数与分层

```
find skills/builtin -name SKILL.md | wc -l        # → 115（含模板类）
find skills/builtin -maxdepth 2 -name SKILL.md | grep -viE "template|example" | wc -l   # → 114
ls skills/builtin | wc -l                          # → 114 个技能目录
ls skills/shared/                                  # README + references + scripts
```
✅ README 徽章 113；实测 114-115（统计口径差异，数量级吻合，非虚标）。
技能命名自解释：`skill-trending-topics`（发现）、`skill-topic-evaluator`（策划）、
`xhs-note-creator`/`auto-short-video`（创作）、`skill-xhs-publisher`（发布）、
`skill-content-postmortem`（归因）——五段工作流在技能命名层面落地。

### 步骤 3：复盘技能读回写契约

读 `skills/builtin/skill-content-postmortem/SKILL.md`：frontmatter `layer: attribute`，
输入要求内容原文/平台/数据指标/发布时间/同期对照（基线比较）——归因不是拍脑袋，
要求带基线的证据化复盘。

### 步骤 4：发布安全闸门实测（核心）

`docs/SKILL-SPEC.md` 规定：任何发布类脚本真发前必须过 `content_guard.py guard_or_die()`，
BLOCK 级（API key、内部 URL、env 真值）fail-closed 退出 7；WARN 级（AI 措辞、模型名）只提醒；
显式 `--allow-unsafe` 才放行。

实测三条命令（全部真实执行）：

```
① scan --text "这篇文章由 Claude 大模型生成，教你轻松月入十万"
→ ⚠️ 1 处 AI 措辞 [low] ai-disclosure｜自曝为大模型（仅提醒，不拦截）   exit=0 ✅

② scan --text "请联系内部 API 网关 https://api.internal.example.com，密钥在 .env 的 ANTHROPIC_API_KEY=sk-abc123SECRET"
→ ❌ 1 处敏感信息 [med] env-name｜Anthropic env 变量名（发布会被拦截）   exit=7 ✅

③ selftest
→ selftest 通过（BLOCK 正例 12 必拦 / WARN 正例 7 只提醒不拦 / 反例 6 放行 + redact + guard）  exit=0 ✅
```

## 结论

- 文章宣称的画像六维、113 技能、五段工作流全部在代码层核实存在；
- **发布安全闸门是真实的确定性 Gate**：WARN 放行提醒 / BLOCK 退出 7 拦截 / 自测 12 正例必拦，
  与知识库 [[技能路由器与授权硬门]]、[[护栏模式Guardrails]] 的设计语言一致；
- 记忆写入有明确纪律（"不是每次做完任务都写"），防止记忆膨胀——与 [[三层记忆]] 的"可回溯可编辑"呼应；
- 未验证项（如实记录）：完整安装链路（OpenClaw/Playwright）、真实平台发布、
  归因数据读取、视频类技能（需 ffmpeg）。

## 产物

- `exercise/experiment-log.md`（本文件）
- `exercise/test_post.txt` / `test_leak.txt`（闸门测试样例）
- `repo/` 上游克隆（.gitignore 排除）
