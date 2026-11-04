# agent-desktop 独立审核记录

## 初审：拒绝（安全问题）

初审交叉检查固定源码后发现：`src/main.rs` 对 `click` 先执行 `permission_report`，再进行 ref preflight；Linux 权限探测会连接 AT-SPI、注册 `window:activate` 监听并读取注册表 `ChildCount`。因此，初版运行 `click @e1` / `click @safetylab:e1` 的日志即使返回参数或快照错误，也不能证明“完全无桌面访问”。

处理：接受拒绝，不写入审核通过记录。撤除所有桌面适配器命令，不再把删除会话环境变量作为隔离证明。

## 修订与复审

修订版实验只允许：

1. `version`
2. `skills get desktop`
3. `skills get platform`
4. 严格 ref、权限探测顺序的固定源码静态契约检查
5. headless 交互与安全重试策略的固定源码静态契约检查

第二位审核者确认上述修订、PDF 与知识库均正确，但发现 `动作投递语义与安全重试.md` 仍残留“本次实测两个 not_delivered 失败”的旧句，因此拒绝。该句已改成仅做静态源码契约检查，未运行桌面动作或失败用例。

## 终审：通过

- 审核者：`claude-independent-review-desktop-v3`（不同于 owner `claude-live-w4`）
- 审核时间：2026-11-04T17:41:55+08:00
- 固定源码：`6660fbac768dc7e7332837b90ed465684859afa3`
- 审核产物指纹：`ad15f54127cc3079f2c3fc8b871b5368b8d4ba474a7ccb11d083cc45ac8d23b5`
- 审核者独立重算的指纹与 ready 记录一致。
- 实验：3 个无桌面 CLI 命令 + 2 组固定源码静态契约检查，5/5；harness 白名单拒绝 snapshot/status/动作/窗口/输入/剪贴板命令。
- PDF：逐页查看 17 页，15 问完整；9,557 个提取字符、无替换字符、无正文裁切，无位图拼接。
- 知识库：项目笔记、四个新概念与 MOC 已更新，旧实验声明已清除。
- 保留边界：真实 AT-SPI 观察与动作、权限弹窗、MCP 长驻服务、C FFI、macOS/Windows 行为和 Rust 编译均未验证；未使用 headed。

审核结论已写入流水线；没有调用网站发布或任务完成接口，网站勾选仍由用户本人确认。
