# 第2项：LCU状态化MCP桥接

**状态：学习交付真实完成；原始运行时与真实GUI待验证。** 访问2026-11-11 Asia/Shanghai。没有安装/启动ChatGPT、登录、账号/密钥、真实桌面或安全配置变更。

## 核心交付
1. `LCU-状态化MCP学习指南.html`：单文件彩色中文，12问逐问内联SVG、5用途、6步真实实验。
2. `LCU-状态化MCP学习指南.pdf`：实际Chrome打印的12页A4；已pdftoppm导图并Read逐页检查12/12，中文/图形正常，无截断/溢出。
3. `LCU-exercise.zip`：最小状态化js/js_reset模拟服务、真实stdio驱动、上游原样客户端及7项纯测试、合成结果；CRC通过。
4. `experiment-log.md`：真实命令、stdout/stderr、退出码与失败后恢复记录。
5. `knowledge-proposal.md`：建议合入vault的项目/增量条目，未自动合入。
6. `sources.md`：原帖与两层引用、固定源码/规范、日期、SHA与可读性。

## 补充证据
- `pdf-review.md`、`pdf-pages/`、`artifact-validation.json`：12页逐页自查与中文文本验证，非独立审核。
- `sources/x-reading.md`：原文人工转录、配图与视频抽样边界；引用中的自动放行建议未执行。
- `exercise/results/`：真实协议wire、41项命名检查和纯合成状态。不是41次真实桌面动作。
- `_tools/`：从01-elyterminal复制并局部扩展的模板、日志、打印/生成/核验/打包脚本。未改共享_common。
- `SHA256SUMS`：交付与证据校验；`02-lcu-deliverables.zip`为本项便携包（不含完整Git与浏览器profile）。

上游LCU SHA：a7e30c1862707214dfe748d410854771ab4f4494；知识库main未变：a8674777e18302b8804b137212b1396cbfe5a747。

## 摘要
LCU复用本机官方Computer Use运行时，并不重新实现桌面引擎；双工具入口将复杂度转移到代码状态、宿主回合与权限边界。当前无需Python，与历史引用帖不同；Linux逐应用审批边界也不能照搬macOS。真实完成模拟stdio、重置/副作用与错误实验，并运行上游原样纯逻辑组件；原始GUI、宿主适配与生命周期效果仍待验证。
