---
tags: [项目]
类别: 知识学习类（提示词工程 / 数据资产型开源仓库）
上游仓库: https://github.com/freestylefly/awesome-gpt-image-2
完成日期: 2026-10-02
---

# awesome_gpt_image_2

**这是什么**（一句话）：苍何把 X 上社区验证过的 GPT-Image2 提示词逆向拆解成 541 条结构化案例 + 21 套工业模板 + 1 个 Agent Skill 的开源库（"Prompt as Code"），曾登顶 GitHub 趋势榜第一。

**它给我什么能力**：
- 按类别/风格/场景检索 541 条真实提示词（cases.json + docs/gallery-*.md 附图对照）
- 21 套"填空即用"模板（docs/templates.md，含避坑指南），模型无关，即梦/GLM 出图也能套
- npm 技能包 gpt-image-2-style-library 可装进 AI 编程助手
- 自建私有提示词库的完整方法论（逆向四步流水线）

**引入的概念**：
- [[PromptAsCode提示词即代码]] — 六块协议 + 槽位 + 质检
- [[提示词逆向工程]] — 收集→拆解→重写→归档，单一事实源

**实验记录**（exercise\，全部真实运行）：
- ex1_stats.py：541 案例/13 类别统计；提示词平均 1257 字符；结构化覆盖率 风格 73%/文字 64%/比例 27%；坑：`re` 的 `\b` 在中文与数字间不成立（"比例9:16"匹配失败），改用 `(?<![.\d])` 环视修复
- ex2_deconstruct.py：案例 #544 解剖成六块协议，逐块原文节选+标注
- ex3_assemble.py：UI 模板函数化，两版只差主色一参，diff 仅 1 行——Prompt as Code 参数化验证
- ex4_lint.py：7 条确定性规则 Prompt Lint，好样例 100/100 PASS，"画一个好看的app界面"14/100 FAIL——[[质检Gate与自我纠错循环]] 的提示工程落地

**坑与结论**：
- README 数字与数据文件会漂移（544 vs 541），一切以 data/cases.json 为准
- 仓库 354MB 大头是案例图片，克隆要耐心；学习只需 data/ + docs/ 两个目录
- 图像生成 API 本机不可用不影响学习：模板方法与 Lint 质检都是纯文本层，可先行练熟

**后续可深入的方向**：
- 把 ex4 Lint + ex3 组装接上 GLM 出图 API，做"生成→Lint→改写"自动循环
- 用逆向四步流水线归档自己满意的出图提示词，攒私有案例库
