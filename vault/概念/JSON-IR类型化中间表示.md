---
tags: [概念]
领域: 数据可视化 / AI 协作
别名: ["JSON-IR", "类型化中间表示", "typed candidate", "语义类型DSL"]
首次来源: "[[项目笔记/archify]]"
---

# JSON-IR 类型化中间表示

**一句话定义**：让 LLM 不直接画图（不碰坐标/连线几何），只按 JSON Schema 填一张"语义表"（节点是什么、谁连谁、带什么文字），几何布局由确定性渲染器计算——生成与验收之间隔着一层有类型的中间表示。

**属于领域**：数据可视化 / AI 协作

**通俗理解**：让 LLM 自由画 SVG，就像让实习生直接上沈墨挥毫——坐标算不准、线会穿字；JSON-IR 像给实习生一张**表格**：设备名称、上下游、备注，各栏都有下拉选项。archify 实测：workflow 图节点 type 只许填 `frontend/backend/database/cloud/security/messagebus/external` 七种语义值，填流程图习惯词 `process/decision` 直接被 schema 拒（实验真跑，7 处报错）；改按语义填后 0 错误。**颜色、形状、图例全部由 type 推导**，所以 AI 产的风格永远一致。

**与已有概念的关联**：
- 是 [[修改与约束分离]] 在画图域的实例：约束（schema）管住自由发挥的部分
- 布局交给 [[确定性图布局]] 思想的渲染器：同输入同输出，图才能被引用
- 配合 [[质检Gate与自我纠错循环]]：candidate 先过 schema 门禁再谈渲染
- 与 [[AgentSkills技能包]] 的关系：SKILL.md 教 LLM "怎么填表"，CLI 负责验收

**首次接触于**：[[项目笔记/archify]]
