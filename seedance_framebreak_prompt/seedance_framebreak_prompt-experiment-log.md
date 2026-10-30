# 实验日志 · Seedance 2.5 frame-break 提示词（seedance_framebreak_prompt）

- 任务：3a2b1895-1561-4c62-95b8-308dccb39dc3（子 agent 分类上报，主控批复后主控完整学习）
- worker：kimi-pool-20261007-w1（主控模式）
- 日期：2026-10-09
- 对象：Kōda (@aimikoda) 公开的 frame-break effect 提示词（主帖 2106044483863191748 + 续帖 2106044848310452333）

## 实验设计

Seedance 为付费云端视频模型，效果无法本机复现。实验面：提示词全文抓取存档 + 结构解析（把"提示词工程"从口号变成可核对的结构）。

## 抓取记录（全部真实执行）

- 主帖（1020 字自述）：koda_tweet.json（fxtwitter，完整）
- 续帖（11950 字提示词全文）：koda_prompt_tweet.json + prompt_fulltext.txt（fxtwitter 完整；首次请求曾截断/超时，重试后完整，过程如实）
- 线程追溯：qrt 链 2105936414185562299 → 2105681229827678485（"En garde!" 首条视频）
- 第三支提示词在更早帖中未收录（如实声明）

## 运行记录

`python parse_prompts.py` → **6/6 通过（exit=0，run_output.txt）**：

- 2 支提示词（3700/8250 字符，均值 5975）
- 五层骨架各提示词全命中：①角色锚定层（Use @[char ref]+Preserve）②视觉目标层（MAIN VISUAL GOAL 大写宣言）③合成顺序层（COMPOSITING ORDER BACK TO FRONT：背景→黑边→前景角色）④物理约束层（黑边等宽固定/定机镜头）⑤节拍层（OPENING 分镜）
- 合成三层齐备 3/3
- Koda 四条方法论观察全记录（黑边漂移/运镜破坏/约束竞争/2.0→2.5 代差）

## 结论

- frame-break 的提示词是"把导演/摄影/合成三岗工作单合并成模型可执行规格书"——五层骨架（锚定/目标/合成序/约束/节拍）可迁移到任何视频生成模型。
- 最有价值的发现是**约束竞争**：越强调黑边固定越可能破坏弹出效果——提示词工程存在约束与目标的内部竞争，不是约束堆越多越好。
- 与 Harness 论文 §7.3 提示词修辞学互证（大写宣言/禁令句式/反效果警告跨域通用）。
- 未验证（诚实声明）：效果未复现（付费云端模型）；解析为结构级验证非效果级验证；@[char ref] 为平台语法。

## 产物

- `exercise/parse_prompts.py`、`exercise/run_output.txt`、`exercise/prompt_fulltext.txt`、`exercise/koda_tweet.json`、`exercise/koda_prompt_tweet.json`、`exercise/insert_svgs.py`
