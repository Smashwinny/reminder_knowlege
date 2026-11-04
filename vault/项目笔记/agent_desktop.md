---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/vercel-labs/agent-desktop
完成日期: 2026-11-04
状态: 学习产物与独立审核完成后，网站完成仍由用户确认
---

# agent_desktop

**这是什么**（一句话）：Vercel Labs 的 Apache-2.0 桌面观察/动作工具，以共享 Rust 核心适配 macOS AX、Windows UI Automation 和 Linux AT-SPI，并通过 CLI、stdio MCP 与 C FFI 给 Agent 使用；它不是 LLM，也不自带 Agent 决策循环。

**来源与版本**：官方仓库固定提交 `6660fbac768dc7e7332837b90ed465684859afa3`；本地运行 npm 原生包 `agent-desktop@1.1.0`，JSON envelope `2.6`，要求 Node 18+。共享 `PlatformAdapter` 组合 ObservationOps、ActionOps、InputOps、SystemOps；MCP 工具目录从同一 Clap CLI 命令树派生。

**它给我什么能力**：
- 用语义快照和快照限定 ref 观察、寻址桌面元素，并以严格身份检查降低误点。
- 用结构化 JSON 区分参数错误、快照缺失、部分观察、动作投递与验证状态。
- 在默认 headless 限制下接入桌面工作流；确需物理输入时显式选择 headed。
- 通过 CLI 做脚本、MCP 接 Agent 宿主、C FFI 接原生应用；三者复用同一平台适配层。
- 将截图、会话、trace、剪贴板和命令输出视作敏感产物，发布前审查而非默认公开。

**引入的概念**：
- [[概念/无障碍树语义桌面自动化]]
- [[概念/快照限定Ref与严格重识别]]
- [[概念/动作投递语义与安全重试]]
- [[概念/Headless与Headed交互策略]]

**实验记录**（做了什么、结果、坑）：
- 使用 `exercise/run_safe_lab.py` 隔离 HOME 和状态目录，并移除 DISPLAY、WAYLAND_DISPLAY、DBUS_SESSION_BUS_ADDRESS、XDG_RUNTIME_DIR；状态目录权限为 0700。
- 真实运行官方原生二进制 3 个无桌面命令，并完成 2 组固定源码静态契约检查，5/5 通过：`version` 证实 1.1.0/envelope 2.6；两个 `skills get` 分别取得通用和 Linux 内嵌文档；源码断言覆盖严格 ref/权限探测顺序及 headless/重试策略。
- 独立审核发现 Linux `click` 会在 ref 校验前探测 AT-SPI，初版两个 ref 运行用例不能证明无桌面访问，已撤除。现版 harness 只允许 version/skills，并以 `main.rs` 分支顺序证明不进入平台适配器；删除会话变量只作纵深防御。
- 结构化命令错误通常退出 1，CLI 解析错误退出 2；现版不通过桌面动作命令演示退出码。
- 原生二进制 SHA256：`e03d67b7e61d358eb62c411376fc7bbd3dc5923cb01131c968f3113c56687bbf`；完整证据在 `exercise/results/safe-lab.json`。
- 环境坑：本机没有 cargo，因此未做 Rust 编译或测试；npm 对 postinstall 的 allowScripts 警告不妨碍包内原生二进制运行，未改全局脚本策略。

**未验证与后续方向**：
- 没有运行真实 snapshot/status/click/type，没有读取 AT-SPI 总线，没有使用 --headed，也没有控制真实窗口、鼠标、键盘、焦点或剪贴板。
- MCP 长驻服务、C FFI、macOS/Windows 行为与 Rust 编译均未验证；后续必须在用户明确授权的隔离桌面和合成目标中单独验收。
- 已生成 17 页中文彩色指南及 HTML，pdftotext 回读 9,557 字符、无替换字符、15 个疑问编号齐全；PDF 是可选中文本。

**本地产物**：
- `agent_desktop/agent_desktop-小白指南.html`
- `agent_desktop/agent_desktop-小白指南.pdf`
- `agent_desktop/exercise/run_safe_lab.py`
- `agent_desktop/exercise/results/safe-lab.json`
- `agent_desktop/exercise/README.md`
