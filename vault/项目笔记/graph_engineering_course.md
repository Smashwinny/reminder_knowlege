---
tags: [项目]
类别: 知识学习类
来源课程: https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
原始记录: https://x.com/AYi_AInotes/status/2104542011642757330
完成日期: 2026-11-22
---

# graph_engineering_course

**这是什么**：对转发视频实际对应的 DeepLearning.AI《AI Agents in LangGraph》做字幕核验与增量学习，重点拆解课程真实停止逻辑，并用零依赖实验验证停止出口与双层评估。不是“吴恩达 2026 自修改新课”，也没有改选《Agentic AI》。

## 来源核验结论

- 转发视频公开英文字幕共 3019 个 cues，末时刻约 1:52:25.926；本轮实际读取 VTT，SHA-256 为 `db669ec5ab5faa6f8513c249c951bf0857fa329ccedd85e1ed6279328ca809a0`。
- Andrew Ng 负责开场概念介绍；官方当前课程页列 Harrison Chase 与 Rotem Weiss 为 instructors。课程主体是从零 Agent、LangGraph 组件、Agentic Search、Persistence/Streaming、Human-in-the-loop、Essay Writer 和架构结论。
- 网传 9:14 / 33:11 / 1:02:46 / 1:30:15 / 1:49:05 五个节点不对应宣传所述章节。尤其 1:30:15 正在讲 Essay Writer 修订状态，1:49:05 附近是 supervisor 架构，片尾仅剩约三分钟。
- 官方目录、字幕与结论均未支持“Agent 改写并升级自己代码”或“最后四十分钟完整图系统”。真正的自修改主题应关联 [[RRSI正则化递归自我改进]]，不能归给本课程。

## 带来的增量

- 复用 [[LangGraph与Agent编排]]、[[Agent循环]]：`exists_action` 只判断有无工具调用；`END` 不是语义质量证明。
- 复用 [[Checkpoint存档与持久执行]]、[[人机协同Interrupt]]：checkpoint 是可恢复记录，interrupt 是等待人工，两者都不是任务成功。
- 课程从零 Agent 有两个退出：无 Action 即 return、达到 max_turns；两者也都不证明结果正确。
- Essay Writer 在 generate 后递增 `revision_number`，用严格的 `revision_number > max_revisions` 路由到 END。示例从 1 开始、上限 2，实际两稿一次反思；它只控制预算，不检查文章质量。
- 本实验把停止理由拆为 `VERIFIED_SUCCESS`、`STAGNANT`、`BUDGET_EXHAUSTED`、`HARD_FAILURE`，另将 `WAITING_HUMAN` 明确视为暂停。该停滞/硬失败分类是实验增量，不归给课程。
- 复用 [[Outcome与Trajectory双层评测]]：Outcome 查日期、负责人、来源；Trajectory 查允许路径与评估器完整性；`claimed_done` 不参与通过判定。
- 复用 [[图环挽具三层工程]]、[[证据优先质检ProofOverClaims]]：图到达出口与任务被验证完成是两条不同证据链。

## 真实实验

产物：[彩色指南](../../graph_engineering_course/graph_engineering_course-小白指南.pdf) · [HTML](../../graph_engineering_course/graph_engineering_course-guide.html) · [实验日志](../../graph_engineering_course/exercise/experiment-log.txt)

自建 `graph_eval_lab.py` 和 `test_graph_eval_lab.py`，Python 3.14.7、UTF-8、无第三方依赖、无模型/API 调用：

| 病例 | 实际结果 | 轮数 |
|---|---|---:|
| clean | PASS / VERIFIED_SUCCESS | 1 |
| repair | PASS / VERIFIED_SUCCESS | 2 |
| stagnant | FAIL / STAGNANT | 2（预算设为 5 的单测） |
| budget | FAIL / BUDGET_EXHAUSTED | 3（默认）；改为 2 后实际为 2 |
| tamper | FAIL / HARD_FAILURE | 1 |

9 项单元测试全部通过，含 `(2,2)→reflect`、`(3,2)→end` 两个课程边界；另有停滞、精确预算、评估器篡改、claimed_done 不作为证据等回归检查。

## 限制

没有逐帧观看视频、运行官方托管 Notebook、调用真实 LLM/Tavily、验证生产持久化或实现自修改 Agent。PDF 已验证 18 页及文本存在，HTML 做过视觉抽检；本机缺少 PDF 页图渲染器且额外安装未获权限，因此 worker 未完成逐页 PDF 看图审核。固定病例与 9 项测试只证明自建小运行时的既定行为，不证明生产可靠或效率倍增。
