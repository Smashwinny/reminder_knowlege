# knowledge-proposal（只供协调者合入，不自行提交）

## 状态
真实完成：原帖 note_tweet 与引用帖/作者回复实读、18 个一手仓库 API 元数据 + git ls-remote SHA + LICENSE 实读、AgiBot World 2026 提交 95b159a 的 README/导出收据/98 个 info.json 关键帧统计、SO-100/SO-101/TurtleBot3/OpenMANIPULATOR-X 官方 URDF 正运动学、A4 打印与逐页自查。
部分待验证：任一项目的实物复刻与标定；带网格的 MuJoCo/PyBullet；原帖与数据集视频画面；Theme 2/3 失败样本；九项推理能力与任务目录的逐项映射。不自动勾选用户任务。

## 查重基线
公开 main `a8674777e18302b8804b137212b1396cbfe5a747`，提交时间 2026-11-04 17:42:58（Asia/Shanghai）；实际下载并读总览、openarm 与 robot-web-anatomy 项目笔记、失败反馈具体化、Sim2Real与MuJoCo仿真、机器人数字展台。固定树中没有本 18 项清单或 AGIBOT WORLD Release 4 专条。已有相邻主题只互链，不新增同义笔记。

## 建议改动（候选，不是已执行）
1. 新增 `vault/项目笔记/open-robots-18.md`：记录原帖 18 名、作者“并非全部开源”的补充、各仓 SHA 与许可分层、SO-ARM100 仓已主推 SO-101、SpotMicro 设计/软件分仓、OttoDIY 重定向陷阱。
2. 新增或在总览互链一项数据集案例：`vault/项目笔记/agibot-world-2026-r4.md`（或并入上条）：HF `95b159a10305a0385f369aba5d4b16242526d17b`；98/98 info.json 计数 Success 8259 / Error 2 / Intervention 2；completions 收据的 isResultSucceed 全 false 不能当失败率；error_cause 用词不统一；官方“同等权重”与公开 key_frame 不符。
3. 增补 `vault/概念/失败反馈具体化.md`：只追加机器人数据字段案例（类型 + 原因 + 是否可恢复），不改 agent 循环的原定义，也不把 8259:2 写成“该概念已被数据集完美实现”。
4. 在 `vault/项目笔记/openarm.md` 或总览加一句互链：本批 SO-ARM100 不是 enactic OpenArm。
5. `vault/00-总览.md` 只追加项目索引与上述互链，不改历史累计数量。

## 不应合入为事实的说法
- “这 18 个项目都是 OSI 开源、都可商用复刻”。
- “AGIBOT WORLD Release 4 已对成功与失败样本同等加权”（与 8259:2 的公开 key_frame 计数冲突）。
- “completions.json 的 8146 条 isResultSucceed=false 等于 8146 次任务失败”。
- “本批完成了真机复刻、MuJoCo 带网格仿真或完整数据集训练”。
- “独立审核已完成”：仅同一 worker 逐页自查。

建议索引标签：`学习交付完成；实物复刻/完整数据与视频待验证`。任务状态与网站标签由协调者管理，本 worker 未触及。
