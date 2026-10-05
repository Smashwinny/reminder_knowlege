---
tags: [概念]
领域: 事件溯源 / 可观测性
别名: [append-only event log, 事件溯源, fold model, 会话转录]
首次来源: "[[项目笔记/zoetrope]]"
---

# JSONL事件日志与折叠模型

**一句话定义**：把系统行为记录成"只追加、每行一个独立 JSON 事件"的日志文件（JSONL），任何时刻的状态都由"从头折叠（fold）已发生的事件"纯函数推导出来，而不是被原地修改。

**属于领域**：事件溯源（Event Sourcing）/ 可观测性。

**通俗理解**（比喻讲完落回术语）：像**银行流水**——账户余额不是被直接涂改的数字，而是每一笔收支流水累加出来的结果；想查"上周三余额"，把流水加到那一笔为止即可。zoetrope 把 Claude Code 的会话转录（`~/.claude/projects/<项目>/<UUID>.jsonl`，官方私有格式）当作这种流水：每行一个独立事件，坏一行跳过不致命；内存里的会话模型（SessionModel）是**事件集合的纯函数**——与事件到达顺序无关（可交换、幂等），所以多文件乱序合并、往回拖进度条、直播和回放四种路径收敛到同一个状态。对照 [[Checkpoint存档与持久执行]]：Checkpoint 存"每步的快照"（重状态、恢复快），事件日志存"每步的动作"（轻存储、任意回放），一个从后往前省，一个从前往后算。

**与已有概念的关联**：
- 相关：[[Checkpoint存档与持久执行]]（快照式存档 vs 事件式日志，两条互补路线）
- 相关：[[三层记忆]]（同为"轨迹→派生视图"的分层）
- 应用：[[多智能体协作]] 的会话可视化（zoetrope 的流动图就是从这种日志折叠出来的）

**首次接触于**：[[项目笔记/zoetrope]]

## Colab CLI：事件记录与有损导出投影（2026-10-05）

[[项目笔记/google_colab_cli]] 复用本概念，不另建“JSONL 事件记录”同义条目。这里的**投影**是按目标格式的规则选择、转换事件字段，不能把原项目的纯函数折叠、幂等、乱序收敛或坏行跳过性质直接归给另一个 JSONL 实现。

固定版本的 `HistoryLogger.log_event` 按行追加记录，构造顺序是 `timestamp`、`event_type`、最后展开 `data`：调用方数据能覆盖前两个字段。`get_history` 对非空行直接 `json.loads`，损坏的 JSON 行会报错。本地日志留痕本身不认证远程执行真实性，也不是防篡改审计日志。

同一批合成事件交给真实 `converter`，四种导出的信息保留范围不同：

- JSONL 导出逐记录保留传入事件对象；这指反序列化后的记录相等，不承诺原文件字节、空白或键排列完全相同
- Notebook 将含 `text` 的输出统一映射为 `stdout`，原 `stderr` 标签丢失；含 `data` 的输出映射为 `display_data`，不保留原 `execute_result` 类型、`execution_count` 和输出 `metadata`
- Notebook 保留受支持的错误输出，但没有 `session_terminated` 分支；结构合法不等于事件齐全
- Markdown 只输出所支持分支及文本输出，会遗漏错误、富输出和终止事件；TXT 的 execution 分支只写代码，不导出执行输出

这些是固定版本的映射边界，没有在原学习实验中修复。Notebook 中出现输出也不证明代码真实执行过；需要另查输入来源和执行证据。文件与运行时状态的关系见 [[产物留痕与状态外置]]、[[Checkpoint存档与持久执行]]。

来源：[history.py](https://github.com/googlecolab/google-colab-cli/blob/a84e094c67544e70d88649ba2d2a1d48511b3af7/src/colab_cli/history.py)、[converter.py](https://github.com/googlecolab/google-colab-cli/blob/a84e094c67544e70d88649ba2d2a1d48511b3af7/src/colab_cli/converter.py)。真实本地记录/转换实验及测试口径见 [实验日志](../../google_colab_cli/delivery/04-experiment-log.md)；输入代码与输出为合成数据，未执行记录中的代码，也没有 Google 认证、云端运行时或账单实测。

## Metrik：累计量、事件身份与来源观察（2026-10-05）

[[项目笔记/metrik]] 提供计量侧案例：日志行、累计快照、用量事件与文件观察是不同对象。JSONL 只是记录格式，不能自动保证事件幂等、乱序收敛、坏行容错或账单正确；上方 Colab CLI 的导出投影边界继续成立。

固定版本 Rust 源码中，Codex 适配器对累计快照做增量计算；分叉继承的历史推进基线，但在首个 turn_context 前不产生新用量。Claude 对同一 provider message ID 的渐进更新按 Token 分量最大值合并。账本把 usage_event 与 event_observation 分开，使“同一事件被两个文件观察到”不直接变成两份用量。累计差分、身份与归一化口径必须结合读取，参见 [[用量、额度与估算费用的计量分层]]。

以上是**固定源码审阅，未运行 Rust 解析器、SQLite 事务或去重账本**。已有 JavaScript 实验的 exact_duplicate_window 只证明窗口输入未被选择器修改，不能给数据库去重背书。当前引擎的 182 天解析视界、约 1500 毫秒文件间预算与回填也仅源码审阅；界面查询周期不等于扫描覆盖范围。

来源：[Codex 适配器](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/adapters/codex.rs#L250-L390)、[Claude 适配器](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/adapters/claude.rs#L114-L195)、[账本](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/storage.rs#L157-L460)、[引擎常量](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/engine.rs#L30-L44)。已执行与未执行项见 [实验日志](../../metrik/delivery/04-experiment-log.md)。
