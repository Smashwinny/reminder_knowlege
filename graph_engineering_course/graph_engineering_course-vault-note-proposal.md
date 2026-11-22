# graph_engineering_course 知识入库提案

## 已写入的允许范围

- 新建项目笔记：`vault/项目笔记/graph_engineering_course.md`
- 未修改 `vault/00-总览.md`、任何既有概念或其他项目笔记。

## 查重结论

不建议新建“停止条件”“图工程”“双层评估”“自修改 Agent”等概念，现有笔记已经覆盖：

- `[[LangGraph与Agent编排]]` / `[[Agent循环]]`：图路由与循环基础。
- `[[Checkpoint存档与持久执行]]` / `[[人机协同Interrupt]]`：恢复与暂停。
- `[[Outcome与Trajectory双层评测]]`：终态和轨迹分开验收。
- `[[图环挽具三层工程]]`：graph / loop / harness 分层。
- `[[RRSI正则化递归自我改进]]`：真正的 harness 自修改与晋级评估。
- `[[证据优先质检ProofOverClaims]]`：完成必须有独立证据。

## 建议协调者合并的小增量

1. **合并到 `图环挽具三层工程`**：补充《AI Agents in LangGraph》的具体反例——`exists_action` 只判断 tool calls，Essay Writer 的 `revision_number > max_revisions` 只控制修订预算；两者都不能单独证明语义成功。
2. **合并到 `Checkpoint存档与持久执行`**：补充课程实例中的四态区分：checkpoint 是可恢复记录、interrupt 是等待人工、budget exhausted 是失败终态、verified success 才是成功终态。
3. **合并到 `Outcome与Trajectory双层评测`**：链接本项目固定病例实验，作为“claimed_done 不参与验收、评估器篡改硬失败”的零依赖小例子；明确它不构成生产评估或模型质量基准。
4. **MOC 项目索引**：只添加 `[[项目笔记/graph_engineering_course]]` 与上述已有概念链接，不新增重复概念。

## 证据与产物

- 官方课程：https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
- 原记录：https://x.com/AYi_AInotes/status/2104542011642757330
- 下游视频：https://x.com/res1dualedge/status/2104300857928098075/video/1
- 公开字幕：https://video.twimg.com/subtitles/amplify_video/2104187439287828480/0/bmbxEZeaIOpgRuCm.vtt
- 字幕 SHA-256：`db669ec5ab5faa6f8513c249c951bf0857fa329ccedd85e1ed6279328ca809a0`
- 指南：`graph_engineering_course/graph_engineering_course-小白指南.pdf`
- HTML：`graph_engineering_course/graph_engineering_course-guide.html`
- 实验日志：`graph_engineering_course/exercise/experiment-log.txt`

合并前请保留来源范围：学习对象是已核实的《AI Agents in LangGraph》，不是《Agentic AI》，也不是宣传中的自修改新课。
