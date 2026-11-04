# agent-desktop 无桌面安全实验

本实验只运行官方 CLI 的 `version` 与 `skills get`，并对固定源码做静态契约检查。脚本在代码层面拒绝执行所有会进入平台适配器的命令，包括 `snapshot`、`status`、`click`、`type`、窗口、输入和剪贴板命令。它不使用 `--headed`，也不以删除环境变量冒充隔离证明。

## 已核实环境

- 上游：`vercel-labs/agent-desktop`
- 固定源码提交：`6660fbac768dc7e7332837b90ed465684859afa3`
- 本地 npm 包：`agent-desktop@1.1.0`
- JSON envelope：`2.6`
- 本机：Linux x86_64，Node `v24.19.0`，npm `11.17.0`，Python `3.10.12`

## 复现

在 `agent_desktop/` 下准备固定源码和局部 npm 包（已有 `repo/` 时只需核实提交，不要拉成其他版本）：

```bash
git clone https://github.com/vercel-labs/agent-desktop repo
git -C repo checkout 6660fbac768dc7e7332837b90ed465684859afa3
mkdir -p exercise/runtime exercise/home exercise/state exercise/npm-cache
chmod 700 exercise/home exercise/state
HOME="$PWD/exercise/home" \
npm_config_cache="$PWD/exercise/npm-cache" \
npm install --prefix exercise/runtime --no-audit --no-fund agent-desktop@1.1.0
python3 exercise/run_safe_lab.py
```

预期：

```json
{"ok": true, "passed": 5, "desktop_commands": "version_and_skills_only"}
```

完整结果在 `results/safe-lab.json`。脚本还把 `HOME` 与 `AGENT_DESKTOP_HOME` 改到本实验目录，移除 `DISPLAY`、`WAYLAND_DISPLAY`、`DBUS_SESSION_BUS_ADDRESS`、`XDG_RUNTIME_DIR`，并检查状态目录权限为 `0700`；这些只是纵深防御。真正的“无桌面调用”依据是 `src/main.rs` 中 `Commands::Version` 和 `Commands::Skills` 在适配器分支之前直接返回，以及 harness 的命令白名单。

## 五项检查

1. `version`：退出码 0，返回 Linux x86_64、CLI 1.1.0、envelope 2.6。
2. `skills get desktop`：返回 6,997 字符的内嵌通用技能文档。
3. `skills get platform`：自动选择 `agent-desktop-linux`，返回 17,209 字符文档。
4. 固定源码契约：`ref_token.rs` 必须包含 `@` 前缀、`:e` 分隔、快照 ID 与本地 ref 校验；同时核实 `main.rs` 的权限探测先于 ref preflight，Linux 权限报告会访问总线。
5. 固定源码契约：headless 默认 `allow_focus_steal:false`、`allow_cursor_move:false`；只有 `NotDelivered` 映射 `RetryDisposition::Safe`，`Unknown` 保持未知，其余已投递/不确定状态为 unsafe。

> 不要把 `click @e1` 当成“必然无桌面副作用的参数错误实验”。固定源码会先执行 `permission_report`，Linux 下可能连接 AT-SPI、注册事件并读取注册表 `ChildCount`，然后才校验 ref。初版实验因此未通过独立审核，现版已彻底移除这类运行调用。

## 边界

本实验没有执行任何桌面适配器命令，所以没有验证真实 AT-SPI 树、权限弹窗、点击/输入效果、MCP 长驻服务或 C FFI。静态源码契约检查不等于 Rust 编译或运行时测试；本机未安装 Rust 1.89，不能声称做过这些验证。结构化命令错误通常退出 1，CLI 解析错误退出 2；本版不通过桌面动作命令演示二者。
