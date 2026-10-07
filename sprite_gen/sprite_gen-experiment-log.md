# 实验日志 · sprite-gen（sprite_gen）

- 任务：24190ae4-948d-4d21-94d4-2e2a5cfa21ec
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 仓库：aldegad/sprite-gen（浅克隆 ece1ac8，包版本 2.39.0，Apache-2.0，2575 stars）

## 实验设计

验证目标：测试套件真实运行 + 本地段管线实跑。生成侧需外部模型 API（无 key 不跑），本地可跑段 = extract/compose/curation。

## 运行记录（全部真实执行，exercise/run_output.txt）

1. 环境检查：Python 3.14.7 / PIL 12.3.0 / numpy 2.5.3，满足 pyproject（pillow≥12.3、numpy≥2.2.6 且 <3——为 NEP 50 字节契约 pinning）。
2. **全量测试**：`python -m pytest tests/ -q -p no:cacheprovider`，9741 collected → **8210 passed, 6 failed, 18 skipped, 1507 errors in 426.37s**。
3. **归因**（--tb=line 逐条）：1507 errors = pytest 临时目录 PermissionError（本机环境顽疾第三批）；6 failed 全部平台相关（POSIX 路径 ×1、v2.32.0 字节冻结 ×2、参数化 ×3）；有效通过率 99.93%。
4. **compose-atlas 实跑**：对自带 fixture（tests/fixtures/run）执行被权限分类器拒绝（直接执行外部仓库脚本需用户点名授权；跑测试被允许）。未绕过。chroma 提取/图集/manifest 的真实出图验证留待授权后补做。

## 结构阅读实证（纯读取）

- 双管线：A 图集行式（prepare→gen/gen-set→extract→compose-atlas，curation 可选回路）；B 视频→循环（视频模型→帧门→自动循环点，--facing 一致性）。
- 契约：manifest.json.frame_layout 机器可读帧布局。
- 安全默认：方向检测 record-only（--facing-fix none），纠错 opt-in（mirror/regen）。
- 工程纪律：pyproject 注释记录 setuptools 77 版本坑与 NEP 50 pinning 理由；9741 项测试。
- 生成侧依赖外部 API（Grok Imagine 等），README 明示赞助覆盖 API 成本、Wanted 赛事拉票段。

## 结论

- 作为"AI 生图后处理管线"样本工程质量极高（测试密度/契约设计/安全默认/字节回归四件套齐全）。
- Windows 是二等公民（6 failed 平台相关），macOS/Linux 才是目标环境。
- 未验证（诚实声明）：生成侧 API 路径、compose-atlas 实跑出图（权限拦截）、curation webview。

## 产物

- `exercise/run_output.txt`
