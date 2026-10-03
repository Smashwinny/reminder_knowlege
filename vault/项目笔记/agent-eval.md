---
tags: [项目笔记]
类别: 知识学习类
上游: https://x.com/ClorisSignal/status/2095703810392150211（X Article）
任务: 拾遗 d09b06b3（Dean 转发推荐 ClorisSignal 长文《AI Agent 跑通了，怎么证明它真的可以上线？》）
完成日期: 2026-10-03
---

# agent-eval

## 它是什么
X @ClorisSignal 的长文教程（Dean 转发"全程跪着看完"的那篇）：**从 0 到 1 搭一套最小可用的 Agent Evaluation Framework**，围绕一个发布决策（资料研究 Agent v2 能否替换 v1）展开八步法——明确发布决策 → 定义成功与 Hard Failure → 建数据集 → 记结果与轨迹 → 配 Rules/Judge/Human → 重复运行 → 设 Release Gate → 线上失败回流。引 OpenAI（Specify）/Anthropic（Agent eval 复杂性）/NVIDIA（工具使用一等信号）/Princeton（Agent Reliability）/G-Eval/MT-Bench 等一手资料。核心论点：**Agent 最危险的不是报错，而是做错了还显示"已完成"**——评测框架负责证明 Agent 能稳定、安全、可解释地交付。无官方代码仓库，属方法论教程，本子项目按文中描述零依赖复刻。

## 带来的概念
- [[Agent评测框架八步法]] — Charter 先行（Specify）、30 条切片数据集四份分开报告、事故必进 regression
- [[Outcome与Trajectory双层评测]] — 终态与过程分开查；Rules+Judge+Human 三层 grader 分工
- [[HardFailure一票否决与发布门禁]] — 硬失败不进平均分、预注册 Gate、cost per successful task、shadow/canary
- [[pass^k可靠性法则]] — pass@k vs pass^k、3/n 法则、Wilson CI、配对评估

## 实验做了什么（全部真跑，零依赖 Python，exercise\）
1. **最小框架 + Rules 双层 grader**（`exp1_charter_rules.py`）：eval-charter + 30 条切片 case（12+6+4+4+2+2）；mock v1（旧模型无搜索工具）跑全量，Rules 层抓到 fabricated_source×2 / false_success×1（Hard）+ miss_conflict×4 / missing_uncertainty×3 / dead_link×5（Quality），v1 成功率 27/30
2. **v1 vs v2 配对评测 + Release Gate**（`exp2_v1_v2_gate.py`）：v2（新模型+搜索工具）29/30 vs v1 27/30（+6.7pp），配对翻转 3 升 1 降；但 cost per task ×2.92 超 efficiency 门禁 + 残留 1 次 fabricated_source 触发 Hard 否决 → **不发布**——"Hard Failure 不进平均分"的活教材
3. **可靠性与统计**（`exp3_reliability.py`）：pass@5=100% vs pass^5=32.8%（p=0.8）；实测 v1 单次 76.7% 但 pass^3=41.7%/pass^5=16.7%（10/12 flaky）；3/n 法则表；Wilson CI：80% vs 83%（n=100）区间重叠，n≥400 才能分离 80/90

## 坑与结论
- **fxtwitter 能拿 X Article 全文**：`api.fxtwitter.com/.../status/<id>` 返回的 `quote.article.content.blocks` 含 231 个 block 的完整正文（atomic block 里的代码/表格除外，需按文字描述自行实现）
- **成功 ≠ 可靠 ≠ 可发布**：三层递进各要专门证据（单次成功率 → pass^k → 预注册 Gate 全绿）
- **"v2 失败了"没有信息量**，"Retrieval failure 从 8% 升到 17%，集中在跨源问题"才知道查哪——Taxonomy+切片是定位工具，不是报表装饰
- 结论：第一天不需要买平台——一个目录、30 条真实 case、几个检查脚本、一份 Rubric 就能把最重要的闭环跑起来

## 产出
- `agent-eval/Agent评测框架-小白指南.pdf`（12 问彩色图文，5 张 SVG，含 3 实验真实数据）
- `agent-eval/agent_eval_guide.html`（PDF 源）
- `agent-eval/exercise/`（framework.py + 3 个实验脚本 + runs\）

## 链接
- [[LLM裁判与自动评估]]（已有概念的 Judge 子集来源）
- 任务来源：[[项目笔记/00-总览]] · 拾遗 task d09b06b3
