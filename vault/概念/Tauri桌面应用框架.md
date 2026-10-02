---
tags: [概念]
领域: 桌面应用 / 前端工程
别名: [Tauri, 桌面应用框架, Rust WebView]
首次来源: "[[项目笔记/mars-editor]]"
---

# Tauri桌面应用框架

**一句话定义**：用 Rust 做外壳 + 系统自带 WebView 渲染前端页面的桌面应用框架，给 Web 技术补上文件系统、子进程、系统托盘等原生能力。

**属于领域**：桌面应用开发

**通俗理解**：网页版应用住在浏览器"沙箱公寓"里——安全但什么都不让摸。Tauri 相当于**给网页盖一栋 Rust 结构的独栋房子**：房间布置（React 界面）原样搬进来，但有了自己的地基和门锁（Rust 后端），能碰文件系统、能 spawn 子进程。对比 Electron：Electron 给每个应用捆一个完整 Chromium（安装包 100+MB），Tauri 用系统自带 WebView，体积小一个数量级。落回术语：**前端经 IPC（invoke/event）调用 Rust `#[tauri::command]` 函数，原生能力全部收敛在 Rust 侧**。

**火星编辑器桌面版实例**：
- `src-tauri/src/vault.rs`：草稿 = 本地 .md 文件 + 文件监听（见 [[本地优先与文件监听]]）
- `src-tauri/src/agent.rs`：`std::process::Command` 启动 `claude -p --output-format stream-json` / `codex exec --json`，JSONL 逐行转发前端，**Rust 侧不解析不合并**（"谁需要理解，谁来做"），与 [[子智能体咨询]] 同模式
- Windows 细节：GUI 进程 spawn 控制台程序会闪黑窗 → `CREATE_NO_WINDOW`；`npm i -g` 装的 CLI 是 `claude.cmd` 批处理，要经 cmd 启动

**与已有概念的关联**：
- [[子智能体咨询]]：同为"包装本机 CLI 而非自接模型 API"
- [[stdio与流式HTTP传输]]：子进程 JSONL over stdio 是同一条通道纪律（stdout 即数据）

**首次接触于**：[[项目笔记/mars-editor]]
