> 公开归档版说明：下文是原完整实验包的历史README。本轮已移除第三方源码，请先阅读项目根目录[ARCHIVE_DEPENDENCIES.md](../ARCHIVE_DEPENDENCIES.md)。本轮未恢复依赖或重跑，不代表当前目录直接可运行。

# ELYTerminal 六步学习实验（中文）

## 范围
上游固定 SHA：9504b5382f3b47b0377063fa3b78cb706f44ed08；阅读日期：2026-11-11（Asia/Shanghai）。这是从完整项目中抽出的组件级实验，不是终端全应用，未启动原生 ELYTerminal GUI。

- `vendor/marks.rs`：上游 `src/term/marks.rs` 原样副本，含 3 个上游测试。
- `vendor/elyterminal.bash`：上游 `assets/shell-integration/bash/elyterminal.bash` 原样副本。
- 两文件以 `vendor/LICENSE-ELYTerminal`（MIT）再分发，保留版权。
- `src/main.rs`：自编薄入口，把 PTY 捕获的 OSC 133 bodies 交给真实上游解析器。
- `lab.py`：自编隔离 HOME 的 PTY 驱动与合成色板计算器；不是上游实现。
- `Cargo.lock`：锁定 log 0.4.28。该依赖第一次运行需公共 crates.io；不需要密钥或付费服务。
- `results/pty.raw` / `pty-readable.txt`：真实 Bash 子进程字节；不是预填期望。
- `results/contrast-demo.html`：合成视觉样例，不是 Ely 截图、不证明 macOS 问题复现。

## 完整命令（在解压后的 exercise 目录）
```sh
python3 lab.py baseline
python3 lab.py shell
CARGO_HOME=/workspace/learn-batch/01-elyterminal/_tools/cargo-home cargo test -- --nocapture
CARGO_HOME=/workspace/learn-batch/01-elyterminal/_tools/cargo-home cargo run -- results/bodies.txt
python3 lab.py contrast
python3 lab.py inventory
```
最后一步需要同级 `upstream/` 快照，只做 metadata；若在其他路径重放，应先从公开上游获取该固定 SHA，或跳过 inventory 并保留未验证说明。前五条不依赖同级仓库；baseline 在仓库不存在时只打印文件指纹及语法检查，不宣称已与上游比对。

## 实测与待验证
已跑通：字节一致性、bash -n、PTY 4 场景、上游 3 测试、18 个真实标记解析、9 个合成透明度场景及2条公式端点断言。
未跑通/未尝试：完整应用构建（本机 Rust 1.85.1 低于上游 1.95 要求）、原生 GUI、macOS 27、宠物动作、中文/软折行点击、性能与内存基准。
初版 lab.py 有字符串语法错误，修复后重新运行通过，失败日志保留在交付日志中。所谓“光标编辑”只测 Bash readline 接收方向键，不测 ELY 鼠标定位。
