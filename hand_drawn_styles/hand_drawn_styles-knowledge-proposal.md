# hand-drawn-styles 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：8e674041-e9f2-4aba-be1f-4b614d670696 ｜ 项目目录：F:\reminder\hand_drawn_styles ｜ 实测 main@5a2f91f

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 提示词配方真源（STYLES.md 模式）
- 一句话定义：把 N 套成品级提示词模板收进单一 Markdown 真源（代码块+槽位声明），所有工具（渲染脚本/Skill 入口/Agent 规则）只从真源机械提取——杜绝"文档与实现两份拷贝"的漂移。
- 领域：AI 工具生态 / 提示工程
- 已有概念关联：[[PromptAsCode提示词即代码]]（其"版本化资产"的组织结构版）；[[确定性脚本]]（提取器零依赖纯标准库）
- 来源项目：hand-drawn-styles（23 配方 / 116 别名实测 pass）

### 2. 槽位 fail-closed 渲染
- 一句话定义：模板渲染缺必填槽位时拒绝输出半成品，报错精确到"缺少占位符：主色调"——宁可报错不交付残次咒语。
- 领域：AI 工具生态 / 工程质量
- 已有概念关联：[[质检Gate与自我纠错循环]]（交付前确定性 Gate）；[[格式压力编因]] 的反面（不给模型"填空压力编因"的机会）
- 来源项目：hand-drawn-styles（实测缺槽报错 / 未知画风报错）

## 二、项目笔记（建议新建 vault\项目笔记\hand_drawn_styles.md）
- 项目是什么：threerocks/hand-drawn-styles，2.6K★，MIT——23 种手绘风格提示词配方库（自称不生图），git main@5a2f91f 实测
- 带来的概念：[[提示词配方真源（STYLES.md 模式）]]、[[槽位 fail-closed 渲染]]
- 实验做了什么：check_skill.py 自检 pass；ink-wash/pixel-art/crayon 三套配方渲染成功；缺槽与未知画风均被明确拒绝
- 坑与结论：README About 栏"5 种画风"与实际 23 种不一致（以 STYLES.md 真源为准）；轻量 zip 可能落后 main

## 三、合并建议（不新建，增补已有笔记）
- [[PromptAsCode提示词即代码]]：增补"配方真源+机械提取"的组织范式
- [[AgentSkills技能包]]：增补一个纯提示词型 Skill 的实例
- [[转绘]]：增补画风 22"源图管内容、锚图管风格"的工程化实例

## 四、MOC 更新建议
"AI / 提示工程（图像生成）"分区增补两条新概念；项目索引加 hand_drawn_styles。
