# REA 动手实验日志（task 84e16939-fb85-42df-a274-f2627a983a2b）

实验日期：2026-10-27
环境：Windows 11，Node v24.21.0 / npm 11.19.0，REA v6.8.0（源码构建，commit b9d1a61）

## 实验设计

自己写一个带"隐藏功能"的模拟 Electron 应用（`exercise/sample-app/`），
埋入三处谜题，再用 REA **不读源码**地做静态分析，检验它能否把谜题挖出来、
以及它的证据标签是否诚实：

| 埋入的谜题 | 位置 |
|---|---|
| ① 隐藏快捷键 `ctrl+shift+k` 解锁会员 | main.js 第 5、15 行 |
| ② `checkLicense()` 假装联网验证、实际永远返回 true（后门） | main.js 第 7-11 行 |
| ③ 主进程↔渲染进程 IPC 通道 `license:unlocked` | main.js 第 17 行 / renderer.js 第 18 行 |

## 步骤与真实输出

### 步骤 0：从源码构建 REA（真实的坑，全部实测）

1. `git clone --depth 1 https://github.com/morluto/rea repo` → 成功，HEAD = b9d1a61
2. `npm ci` → **失败**：package.json engines 要求 `^22.23.4 || ^24.22.1 || >=26.12.1`，本机 24.21.0 差一个补丁版本
3. `npm ci --force` → 成功（esbuild postinstall 被 npm 拦截为 warn，需手动 approve，暂未影响后续）
4. `npm run build:cached` → 只生成 skill 元数据，**不编译 TypeScript**；直接跑 CLI 报 "compiled runtime is missing"
5. `npm run compile` → 成功产出 dist/（两个 INEFFECTIVE_DYNAMIC_IMPORT 警告，无碍）
6. `node scripts/rea.mjs --version` → **6.8.0** ✅

### 步骤 1：doctor 体检（三态诊断的直观演示）

`node scripts/rea.mjs doctor` → `healthy: false`，17 项检查中：
- `node` → missing_dependency（版本 24.21.0 不达标，给出精确 remediation 文案）
- `hopper` / `ghidra` / `ida-registration` → missing_analysis_engine（深度原生分析需要至少一个引擎）
- `jadx` 等 → 缺 Windows 原生控件

### 步骤 2：分析自建样本（第一次失败 → 修复 → 成功）

1. `node scripts/rea.mjs analyze-javascript-application exercise\sample-app --detail summary --evidence_output exercise\evidence\run1`
2. 第一次运行报 `capability_unavailable`：**JS 静态分析依赖 Windows 原生控件，git 源码里不带**，
   错误信息明确指示"从 rea-agents@6.8.0 tarball 恢复 native/windows/build/ 两个文件"
3. 按官方指引 `npm pack rea-agents@6.8.0` + 解包复制 `manifest.json` 与 `rea-windows-x64.node` 到 repo → 重跑成功

### 步骤 3：验证挖出的谜题（对照上表）

完整证据包（309 KB JSON，162 节点 / 105 关系 / 63 条 unknown）中检索：

| 谜题 | REA 发现 | 证据定位 |
|---|---|---|
| ① 快捷键 | 节点[25] kind=literal label=`"ctrl+shift+k"` | main.js 第 5 行 source-range ✅ |
| ① 注册调用 | 节点[12] `globalShortcut` 表达式 + 节点[35] `read:/register` | main.js 第 15 行 ✅ |
| ② 后门函数 | 节点[107] kind=function label=`checkLicense` | main.js 第 7 行 ✅ |
| ③ IPC 通道（发送端） | 节点[36] properties.event_name=`license:unlocked` | main.js ✅ |
| ③ IPC 通道（接收端） | 节点[136] event_name=`license:unlocked` | renderer.js 第 18 行 ✅ |

**三处谜题全部命中**，且每个节点都带 artifact sha256 + 源码行列号，可回溯验证。

### 步骤 4：验证证据诚实性（这是 REA 最重要的特性）

证据包 limitations 原文（节选）：
- "Electron relationships are derived from inert syntax; **runtime registration, reachability, defaults, and enforcement remain unproven**."
- "Static imports, entrypoints, workers, endpoints ... **do not prove runtime execution**."
- 共记录 **63 条 unknowns**，按 family 统计

→ 静态分析只"看到"语法事实（SEEN），把运行时行为明确标为未知（UNKNOWN），
正是防幻觉的三态证据框架，与知识库 [[证据优先质检ProofOverClaims]] 同一精神。

## 结论

- REA v6.8.0 源码构建可跑通（Node 版本差一个补丁可 --force 绕过）
- 免商业引擎即可完成 JS/Electron 静态分析；原生二进制需要 Hopper/Ghidra/IDA 之一
- 自埋 3 谜题全部被静态发现，证据带行列号可复核；63 条未知项如实记录
- Windows 下 JS 分析需要发布 tarball 里的原生控件（git 源码不带）——官方错误文案即修复说明书

## 产物清单

- `exercise/sample-app/` — 待逆向样本（4 文件）
- `exercise/evidence/run1` — 完整证据包 JSON（309 KB）
- `exercise/evidence/run1-summary.json` — 摘要视图
