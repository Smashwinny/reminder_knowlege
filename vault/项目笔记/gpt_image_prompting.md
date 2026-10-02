---
tags: [项目笔记]
类别: 知识学习类（官方文档精读 / 提示词工程）
上游: OpenAI Developers 官方文档《Image Prompting》+ openai/openai-cookbook notebook
完成日期: 2026-10-03
来源推文: https://x.com/yyyole/status/2097707144359354673
中文入口: https://x.com/leo_xiaolei/status/2097722097921409274（水族店刘老板非机翻全译文，X article 2097707280032542720《OpenAI 官方 GPT-Image 2.5 提示词指南与示例》，含 24 个生成/编辑例子；拾遗任务 f31ab548）
---

# gpt_image_prompting

**这是什么**（一句话）：X 博主沐阳转发指路的 OpenAI 官方《GPT Image 2.5 Prompting Guide》——8 条提示词基本原则 + 约 20 个图文示例 + 模型选型（Flare 速度版/Sunburst 质量版）/API 参数纪律/迁移六步法的系统性方法论（非单条提示词）。

**它给我什么能力**：
- 八要素流水线写提示词：用途→主体→构图→风格→光线→材质→文字→负面，产出可复现
- 精确文字三件套：引号逐字 + 位置字体 + 负向排除（海报/招牌/信息图不翻车）
- 编辑三段式（改动区/保护区/排除区），复杂图单变量多轮迭代不跑偏
- 参数纪律：quality/size/background 与提示词分工，自定义分辨率四约束可代码预校验
- 迁移六步法：先保质量、再赚速度、按工作流灰度

**引入的概念**：
- [[图像提示八要素]] — 官方 8 条原则，[[PromptAsCode提示词即代码]] 的官方版同源思想
- [[修改与约束分离]] — 编辑三段式 + 单变量迭代

**实验记录**（exercise\，全部真实运行，PYTHONUTF8=1；**诚实记录：本机无 OPENAI_API_KEY，按预案全部为文档精读+结构化确定性实验，未编造出图结果**）：
- ex1_eight_elements.py：八要素体检器，6 样例打分单调——抽卡式 40/50 分、官方风格 75~100 分、满分样例 100；坑：规则须按场景计分（R6 只在 edit/iterate 计分），第一版全局计分时单句迭代提示词反低于坏例，改 N/A 不进分母后单调
- ex2_resolution_validator.py：官方分辨率四约束 1:1 翻译成 validate()，文档 7 个示例尺寸全 PASS（3840x2160=8,294,400 px 恰触上限），非法尺寸全 FAIL 且报具体条目，3840x1280 恰 3:1 临界合法
- ex3_edit_constraint.py：编辑约束 A/B/C/D 四段计分——口语编辑 0 分、官方翻译例 50 分（"其他所有元素不变"泛泛保留被扣）、推文家具例 75 分；结论：漏写"什么不能动"比漏写"改什么"更常见
- cookbook_image_gen_prompting_guide.ipynb：官方 notebook 存档（98 cells=72 md+26 code），备有 key 后接线

**坑与结论**：
- 推文正文无外链 facet（"链接放下面了"在评论区），用 api.fxtwitter.com 拿全文+截图比对确认官方指南真实存在（截图即文档页中文版，8 条一一对应）
- 提示词质量可以"机检"：8 条原则不是文采而是确定性规则，可与 awesome-gpt-image-2 的 Prompt Lint 合并成生成流水线前置 Gate
- 官方提醒：重复编辑会悄悄改掉本该保留的细节；像素级不动就走合成，别硬靠提示词

**后续可深入的方向**：
- 有 API key 后：ex1 体检器接在 images.generate 前，真实出图验证"分数与出图质量相关性"
- 把官方 8 条与 awesome-gpt-image-2 的 7 条 Lint 规则合并成统一图像提示词 Gate
