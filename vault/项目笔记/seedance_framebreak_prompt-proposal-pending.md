---
tags: [项目笔记, 提示词工程, 视频生成, Seedance]
created: 2026-10-09
---

# Seedance 2.5 frame-break 提示词（Koda Prompt Drop）

- 来源：Kōda @aimikoda https://x.com/aimikoda/status/2106044483863191748（主帖自述+续帖 11950 字全文，均本机存档）
- 分类：子 agent 上报 learning 候选 → 主控批复 → 主控完整学习

## 是什么

Seedance 2.5 的 frame-break effect（黑边破框：角色越出 letterbox 压在黑边上制造破屏立体感）的完整公开提示词。2 支各 3700/8250 字符。

## 五层提示词骨架（解析器 6/6 验证）

①角色锚定层：Use @[char ref]+Preserve 外观清单（防跨代漂移）；②视觉目标层：MAIN VISUAL GOAL 大写宣言；③合成顺序层：COMPOSITING ORDER BACK TO FRONT（背景→黑边→前景角色，z 轴欺骗是效果命门）；④物理约束层：黑边等宽固定/定机镜头；⑤节拍层：OPENING 分镜。

## 四条实战观察（比提示词本身更值钱）

①黑边尺寸模型自决（指定百分比仍漂移=布局参数非硬约束）；②运镜破坏黑边；③**约束竞争**：越强调黑边固定越可能破坏弹出效果——约束过强会杀死目标；④2.0 失败 2.5 成功=复杂合成控制有模型代差门槛。

## 本机实证

parse_prompts.py 结构解析 6/6（五层全命中+合成三层齐备+观察全录）；全文存档 exercise/prompt_fulltext.txt。效果未复现（付费云端模型，作者自述不想烧 credits）；结构级验证非效果级验证。

## 可迁移性

五层骨架适用于任何视频/图像生成模型；约束竞争现象在 LLM 工具调用同样存在。

## 关联

- [[图像提示八要素]]（概念更新提案：追加视频五层骨架注记，见 knowledge-proposal.md）
- [[声明式视频源语言]]、[[源码即Prompt]]、[[ai-video-pipeline]]
