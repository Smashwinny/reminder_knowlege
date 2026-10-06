---
tags: [概念]
领域: 前端设计系统
别名: ["Design Token", "设计代币"]
首次来源: "[[项目笔记/awesome-design-md]]"
---

# 设计令牌 DesignToken

**一句话定义**：把设计决策（颜色、字号、间距、圆角）抽成有名字的最小单位（如 `colors.primary: #5e6ad2`），组件引用名字而非裸值，改一处全局生效。

**属于领域**：前端设计系统 / UI 工程。

**通俗理解**：像 CSS 变量的"设计界版本"，更准确地说是[[规格书先行SpecDriven]]里的"客观测量值"在审美领域的对应物——**把"用品牌紫"翻译成 `#5e6ad2`，主观审美就变成了可写进合同、可被脚本校验的数字**。设计软件里叫"全局色板/字符样式"，代码里叫 token，本质同一件事。

**与已有概念的关联**：
- 相关：[[规格书先行SpecDriven]]（token = 写进 spec 的实测值）、[[DESIGN.md规范文档]]（token 的载体）、[[提示词权威边界]]（token 值即"宪法原文"，AI 不许私自改）
- 对比：[[PromptAsCode提示词即代码]] 同构思想——都把模糊的"风格/感觉"固化成结构化、可参数化的文本协议

**首次接触于**：[[项目笔记/awesome-design-md]]

## UI UX Pro Max：原始值、派生值与组件使用分层（2026-10-05）

[[项目笔记/github_tools_increment]] 补充设计值的来源问题：最终推荐由产品检索、类别规则、多域结果与默认值共同组装，不能只看输出文件就断言组件已经引用 token，也不保证与 [[DESIGN.md规范文档]] 的格式自动兼容。

已有独立 helper 对照固定 SaaS (General) 配色行：light 返回原行，dark 改变 7 个颜色字段并附 derived-dark 标记，保留产品身份。这是函数派生值，不是语料中新增一条官方暗色原行。另一个完整查询加“dark mode”的样例连产品类别也改变，两种观察不能混成单变量模式实验。

来源行存在、派生规则正确、组件实际消费与可访问性验收是不同层。单项 ring/background 对比度约 3.454 只覆盖所测配色；没有页面、键盘、焦点或整站验收证据。来源与产物留存关联 [[产物留痕与状态外置]]，验收关联 [[证据优先质检ProofOverClaims]]。

来源：[固定设计组装与配色 helper](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/design_system.py)；[历史实验日志](../../github_tools_increment/delivery/UIUX增量学习_实验日志.txt)。
