# Metrik 真实组件实验日志

历史记录：以下命令、时间与结果来自 2026-10-05 UTC 的原学习实验。公开整理只调整文档，不代表再次执行。配套 ZIP 中的代码、测试、输入、输出和许可保持原样。

固定源码：keros68/metrik@637444bdc8d91475f66f5319a15dda0e4be1c652，版本 v0.21.1。上游许可 AGPL-3.0-or-later。

## 结论与范围

- 上游 23 项测试与新增 27 个合成场景全部通过；后者另逐场景重放两次。两类计数分开，四个后端阅读例子不计为实测。
- 15% 边界、正常不取全局最小、缺失与真零、陈旧与跨重置点、余额类型保护均在真实 JS 函数上复现。
- compactTokens(null) 返回 "0"，与真 0 的格式相同。格式化器不能独自证明数据可用性；本次没有据此判断完整 UI 存在缺陷。
- 重复窗口输入保留不变不等于用量事件去重。Rust 解析、Token 组成归一化、账本事务、后端时效派生仍只有源码审阅。
- ZIP 从全新目录解压后，按指南打印的五条命令全部执行成功；不依赖上层工作目录或父级辅助脚本。

Linux x64 / Node.js v24.19.0 / Bash；不需 npm 安装；其他 Node 主版本与 Windows 命令环境未验证。
全部输入为合成数据。程序不读取个人日志、不触碰凭据、不发起提供方查询。权限参数限制文件与子进程等能力，不作为网络隔离保证；审阅到的执行代码没有网络调用。

## 执行记录

首轮由源码实验任务在 2026-10-05T06:07:26Z 至 06:07:27Z 实际执行，原日志随 ZIP 保存。下面是作者对最终 ZIP 全新解压后，逐条执行指南所印命令的真实记录。
配套公开 ZIP SHA-256：b22bacfed5a62b38c45834b92af0a8486f3564afa1bcff526d96d9cf015bacb0（文档整理后；历史测试记录未改写）

### 第 1 步：确认 Node 运行环境

目的：确保本机正在使用本实验实际验证过的运行时。
UTC：2026-10-05T06:11:23.474172+00:00 至 2026-10-05T06:11:23.480141+00:00
退出码：0

```bash
node --version
```

```text
v24.19.0

```

实现结果：读取运行时版本，没有安装依赖或更改设置。
检测标准及实际结果：实际输出 v24.19.0。若版本不同，不把本报告当兼容性证明。

### 第 2 步：核验上游原文件与许可

目的：确认执行的是固定版本原函数，避免把改写示例误当上游行为。
UTC：2026-10-05T06:11:23.480234+00:00 至 2026-10-05T06:11:23.542962+00:00
退出码：0

```bash
node --permission --allow-fs-read=. verify-source.mjs
```

```text
{
  "checkedAt": "2026-10-05T06:11:23.538Z",
  "status": "PASS",
  "checkedFiles": 6,
  "commit": "637444bdc8d91475f66f5319a15dda0e4be1c652",
  "license": "AGPL-3.0-or-later",
  "runtime": "v24.19.0",
  "platform": "linux",
  "dependencyInstallRequired": false
}

```

实现结果：核对三个模块、两份测试与完整许可证，共六个文件。
检测标准及实际结果：实际 status=PASS，checkedFiles=6；提交与 source-manifest.json 一致。

### 第 3 步：运行上游自己的测试

目的：先确认配额和托盘纯逻辑在受控环境下的既有断言。
UTC：2026-10-05T06:11:23.543151+00:00 至 2026-10-05T06:11:23.637234+00:00
退出码：0

```bash
node --permission --allow-fs-read=. --test --test-isolation=none \
  upstream/src/quotaWindows.test.js upstream/src/trayBadge.test.js
```

```text
✔ Claude：5h 还满着但每周快见底时，显示每周 (1.549823ms)
✔ GLM：两个窗口都还满着时显示 5h，不因几个百分点的高低来回跳 (0.159429ms)
✔ 较长窗口只是略低时不接管——差值属于噪声 (0.173991ms)
✔ 越过告急线才接管 (0.118417ms)
✔ 两个窗口都告急时取更少的那个 (0.156985ms)
✔ Codex 没有 5h 窗口，落到每周 (0.188693ms)
✔ 任一窗口归零就显示它——那时这个 Agent 已经用不了了 (0.182184ms)
✔ 都告急且并列时取周期更短的（列表顺序即周期顺序） (0.157947ms)
✔ 已过重置点的读数属于上一个周期，不参与比较 (0.240741ms)
✔ 没有来源的窗口不参与比较 (0.46388ms)
✔ isBalanceWindow 只认 balance_ 前缀 (0.145258ms)
✔ DeepSeek：余额是金额不是百分比，¥8.4 不该被告急规则顶到行首 (0.122654ms)
✔ 余额窗口是唯一的有效窗口时照常返回（live[0]） (0.068412ms)
✔ 全部失效时返回 null，由调用方显示「已重置，等待刷新」 (0.064917ms)
✔ 重置倒计时：小数分钟先取整再拆分，不出现 60 分 (0.190606ms)
✔ badge spec picks the first agent from the shared status list (0.721552ms)
✔ badge spec survives empty or malformed lists (0.115232ms)
✔ badge spec normalizes the percentage (0.102815ms)
✔ percent normalization keeps only finite clamped integers (0.066099ms)
✔ badge text shows -- only when the quota is unavailable (0.059879ms)
✔ badge tooltip reuses the menu-bar wording (0.068493ms)
✔ badge key changes only when agent, percent, or staleness changes (0.109173ms)
✔ hidden refresh cadence matches the visible compact widget (0.132058ms)
ℹ tests 23
ℹ suites 0
ℹ pass 23
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 25.322878

```

实现结果：两份未修改上游测试共 23 项通过，失败、跳过均为 0。
检测标准及实际结果：实际 tests=23、pass=23、fail=0。托盘画布函数未调用，不能当作原生视觉测试。

### 第 4 步：运行合成场景，观察主读数切换

目的：在同一套真实函数中改变额度、有效性、单位和格式化输入，看输出如何变化。
UTC：2026-10-05T06:11:23.637437+00:00 至 2026-10-05T06:11:23.719780+00:00
退出码：0

```bash
node --permission --allow-fs-read=. --allow-fs-write=./run-output run-scenarios.mjs
```

```text
{
  "status": "PASS",
  "passed": 27,
  "failed": 0,
  "output": "run-output/results.json",
  "generatedAt": "2026-10-05T06:11:23.713Z"
}

```

实现结果：27 个合成场景通过，完整输入、期望、实际值与输入未改动标记写入 run-output/results.json。
检测标准及实际结果：实际 passed=27、failed=0。normal_short_window 选 five_hour 80%；low_threshold_inclusive 选 seven_day 15%。

### 第 5 步：重放两次，核对记录可信度

目的：检查结果记录对应实际输入与原函数输出，避免只凭漂亮的 PASS 摘要判断。
UTC：2026-10-05T06:11:23.719957+00:00 至 2026-10-05T06:11:23.799724+00:00
退出码：0

```bash
node --permission --allow-fs-read=. verify-results.mjs
```

```text
{
  "checkedAt": "2026-10-05T06:11:23.794Z",
  "status": "PASS",
  "deterministicCases": 27,
  "capturedInputsAndOutputsMatch": true,
  "backendReviewCasesExcludedFromPassCount": 4
}

```

实现结果：27 个场景各独立重放两次，输出及输入记录一致；四个后端阅读例子明确排除在通过数之外。
检测标准及实际结果：实际 deterministicCases=27，capturedInputsAndOutputsMatch=true，backendReviewCasesExcludedFromPassCount=4。

## 27 个合成场景的实际输出摘要

这些样本全部是虚构输入，quality 中的 official_snapshot 是被测结构的合成标签，不是本次取得官方数据。完整输入/输出在 ZIP 的 run-output/results.json；首轮副本在 evidence/。

- normal_short_window / bindingWindow：{"key":"five_hour","remaining":80,"stale":false,"selectedIndex":0,"isBalance":false}；PASS；inputUnchanged=true
- low_threshold_inclusive / bindingWindow：{"key":"seven_day","remaining":15,"stale":false,"selectedIndex":1,"isBalance":false}；PASS；inputUnchanged=true
- above_threshold / bindingWindow：{"key":"five_hour","remaining":80,"stale":false,"selectedIndex":0,"isBalance":false}；PASS；inputUnchanged=true
- multiple_low_minimum / bindingWindow：{"key":"seven_day","remaining":4,"stale":false,"selectedIndex":1,"isBalance":false}；PASS；inputUnchanged=true
- low_tie_first_ranked / bindingWindow：{"key":"five_hour","remaining":5,"stale":false,"selectedIndex":0,"isBalance":false}；PASS；inputUnchanged=true
- zero_is_valid / bindingWindow：{"key":"seven_day","remaining":0,"stale":false,"selectedIndex":1,"isBalance":false}；PASS；inputUnchanged=true
- missing_not_zero / bindingWindow：{"key":"seven_day","remaining":80,"stale":false,"selectedIndex":1,"isBalance":false}；PASS；inputUnchanged=true
- reset_expired_excluded / bindingWindow：{"key":"seven_day","remaining":60,"stale":false,"selectedIndex":1,"isBalance":false}；PASS；inputUnchanged=true
- all_expired / bindingWindow：{"key":null,"remaining":null,"stale":null,"selectedIndex":null,"isBalance":false}；PASS；inputUnchanged=true
- empty_windows / bindingWindow：{"key":null,"remaining":null,"stale":null,"selectedIndex":null,"isBalance":false}；PASS；inputUnchanged=true
- stale_retained / bindingWindow：{"key":"five_hour","remaining":72,"stale":true,"selectedIndex":0,"isBalance":false}；PASS；inputUnchanged=true
- balance_not_low_percent / bindingWindow：{"key":"seven_day","remaining":80,"stale":false,"selectedIndex":0,"isBalance":false}；PASS；inputUnchanged=true
- balance_over_100 / bindingWindow：{"key":"balance_cny","remaining":168.5,"stale":false,"selectedIndex":0,"isBalance":true}；PASS；inputUnchanged=true
- exact_duplicate_window / bindingWindow：{"key":"five_hour","remaining":50,"stale":false,"selectedIndex":0,"isBalance":false}；PASS；inputUnchanged=true
- badge_missing / trayBadge：{"spec":{"agent":"codex","percent":null,"stale":false},"text":"--","tooltip":"Metrik · ChatGPT 配额不可用","key":"codex:--:0"}；PASS；inputUnchanged=true
- badge_zero / trayBadge：{"spec":{"agent":"codex","percent":0,"stale":false},"text":"0","tooltip":"Metrik · ChatGPT 剩余 0%","key":"codex:0:0"}；PASS；inputUnchanged=true
- badge_stale / trayBadge：{"spec":{"agent":"claude","percent":42,"stale":true},"text":"42","tooltip":"Metrik · Claude 剩余 42% · 数据可能已过期","key":"claude:42:1"}；PASS；inputUnchanged=true
- badge_rounding / trayBadge：{"spec":{"agent":"codex","percent":94,"stale":false},"text":"94","tooltip":"Metrik · ChatGPT 剩余 94%","key":"codex:94:0"}；PASS；inputUnchanged=true
- badge_percent_clamped / trayBadge：{"spec":{"agent":"codex","percent":100,"stale":false},"text":"100","tooltip":"Metrik · ChatGPT 剩余 100%","key":"codex:100:0"}；PASS；inputUnchanged=true
- reset_round_hour / formatReset："2 小时 0 分"；PASS；inputUnchanged=true
- reset_round_day / formatReset："1 天 0 小时"；PASS；inputUnchanged=true
- reset_missing / formatReset："暂不可用"；PASS；inputUnchanged=true
- reset_negative / formatReset："0 小时 0 分"；PASS；inputUnchanged=true
- tokens_thousand / compactTokens："1.20K"；PASS；inputUnchanged=true
- tokens_million / compactTokens："1M"；PASS；inputUnchanged=true
- tokens_zero / compactTokens："0"；PASS；inputUnchanged=true
- tokens_missing_formatter / compactTokens："0"；PASS；inputUnchanged=true

## 未执行与不得外推

- Rust/Cargo 在本次环境不可用；后端解析、事件去重、SQLite 合并、Token 组成归一化、时效派生没有实测
- 未运行完整 npm/build/cargo 测试、Tauri 桌面、原生托盘画布、真实账号、官方余额、账单、网络认证或多设备同步
- 没有读取个人会话记录、凭据或改变系统全局设置
- 本实验不能证明所有现实日志格式、完整账单或跨平台行为正确
- PDF 使用 ReportLab 直接生成并逐页渲染查看；HTML 只有结构检查，无浏览器视觉验收

## 可复核来源

- src/quotaWindows.js：https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.js；SHA-256 ea74a919feaaf5d8d0654af12765b126315faaf6bc9adc7b1394dbafa46e89ff
- src/quotaWindows.test.js：https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.test.js；SHA-256 1feef71d3900752b89b31ae9a15416972c6d3a5ae4ff2aa6f07eaf444aaaaa7c
- src/trayBadge.js：https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/trayBadge.js；SHA-256 93515d57ef525fff13648853aedf2b83cbe96c24d53e209301047f562742e9b5
- src/trayBadge.test.js：https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/trayBadge.test.js；SHA-256 1c7e338b75ecc6336ed7a99f3ef1bc749568985cd99f1eeefc5fae509d4e1712
- src/tokenFormat.js：https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/tokenFormat.js；SHA-256 febb222407eb322e7771443bd1dee1d8a372d9fa4189ae0da03ab23ad02dc294
- LICENSE：https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/LICENSE；SHA-256 0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0
