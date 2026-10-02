---
tags: [项目]
类别: 开源项目类（自改进循环极简教学样本，玩笑外皮）
上游仓库: https://github.com/deveIopedbyed/Ass-Bench
完成日期: 2026-10-03
---

# assbench（Ass Bench）

**这是什么**（一句话）：前端教学博主 Dev Ed（Simo Edwin）的恶搞 AI benchmark「Ass Bench」（assbench.dev，让前沿大模型比 3D 雕塑"保真度"排名，$1 赞助贴纸）背后的 MIT 开源仓库——250 行 Python 7 模块，内核是一条 generate→score→steer 的自改进爬山循环。推文（2026-09-08，735 万浏览）2 天后仓库即开源，玩笑外皮 × 真实工程内核。

**它给我什么能力**：
- 40 行核心循环骨架（generate/score/steer 三槽位 + best 爬山 + runs/ JSON 全量日志），任何生成型任务可套
- rubric 四维加权评分器标准写法（维度×权重×0~1 分×人话评语，评语即下一圈转向原料）
- 接缝+桩打法：ABC 接口先立、stub 桩先跑、真后端后插，骨架期零 API 成本
- "伪 benchmark"识别三连问：有标准答案吗？有留出集吗？评分确定吗？

**引入的概念**：
- [[提示词爬山法PromptHillClimbing]]（generate→score→steer 循环 + 四条工程铁律）
- [[接缝与桩实现StubSeam]]（ModelClient ABC + stub 后端 + 注册表分发）

**实验记录**（`F:\reminder\assbench\exercise\ascii_loop.py`，全部真实运行）：
- 上游 stub 循环真跑通：`python -m ass_bench.cli run --rounds 5` 两遍（Best 0.6450 / 0.6350），JSON 落盘正常
- **坑 1（评分器不确定）**：scorer.py 用 `hash()` 占位，跨进程盐随机——同输入两进程 hash 分别 2560065… / -4392188…，循环两遍分数不同，爬坡全是噪声；修法 = 确定性启发式
- **坑 2（prompt 膨胀）**：steer 只追加不去重，best prompt 中同一句 "add more surface texture detail" 重复 4 次
- **坑 3（自造死锁）**：自己首版渲染器把纹理参数锁进 fill 分支，幂等去重后注释永远无法再引导 → 卡 0.4550；修法 = 注释正交（独立生效）
- 修复后文字版真收敛：0.3161 → 0.6359 → 1.0000 三轮提前停，两遍运行逐位一致（可复现）
- 权重敏感性：proportion 权重 0.3→0.7，维度分不变，总分 r1 0.3161→0.2811、r2 0.6359→0.7770；注意 steer 只看维度绝对分，**权重不参与转向**（循环已知局限）

**坑与结论**：
- Windows 下 hash() 的 PYTHONHASHSEED 盐随机是隐形炸弹，任何"评分/排序"代码禁止用内置 hash 做持久化判定
- 给循环加"防重复"安全带时必须保证各注释独立生效，否则安全带本身勒死循环
- 上游仓库 0 star、后端全 stub、评分全占位——价值在骨架分层与模式示范，不在代码量

**后续可深入的方向**：
- 把 ascii_loop 的 score 槽位换成 LLM 裁判（[[LLM裁判与自动评估]]），对照确定性 rubric 的收敛速度
- 给循环加回滚/退火（允许偶尔接受低分逃出局部最优），对比纯爬山的收敛曲线
