---
tags: [项目笔记, 内容工程, AI Agent]
项目: easel
类别: 开源项目类
学习审核日期: 2026-10-05
上游提交: 6c049ceb73b1b74a73448664dcd4dbc7e051442a
---

# Easel：内容产物契约与发布证据

## 项目是什么

Easel 是组织创作者画像、内容技能、产物索引与发布相关流程的开源工作台。本次学习固定 [ZJU-REAL/Easel 的完整提交](https://github.com/ZJU-REAL/Easel/tree/6c049ceb73b1b74a73448664dcd4dbc7e051442a)，重点是“工序怎样接力、状态能证明什么、检查在哪里真正执行”。实跑范围是 Python 标准库组件；没有把完整应用或外部发布链路作为已验证能力。

`pyproject` 版本为 0.2.1，包内版本为 0.1.1，版本字符串不一致时以完整提交定位。根许可为 Apache-2.0；这不等于所有第三方技能与参考材料的许可已逐项核实。练习包只携带实验所需最小上游模块及根许可。

## 复用并增补的五篇概念

- [[产物留痕与状态外置]]：项目 manifest 只传位置、状态与摘要；完整正文和 `brief.md` 创作意图分别落盘，下游显式读取
- [[证据状态机]]：展示头 `draft/ready/published`、步骤 `done/failed` 与外部平台效果分开；Easel 的双状态域不是强制发布状态机
- [[分镜表驱动生成]]：项目级薄索引与镜头级中间表示互相参照，不混为同一 schema；字段齐全仍须文件、解码、渲染与质量证据
- [[技能路由器与授权硬门]]：画像、登录身份、行动许可各有边界；Skill 文档要求、宿主执行与代码闸门不能相互代替
- [[证据优先质检ProofOverClaims]]：按真实入口、输入、退出码和证据等级报告，组件通过不代表全栈、内容质量或发布通过

本次合并沿用这五篇已有概念，没有另建同义概念，也不据此增加概念计数。返回 [[00-总览|知识库总览]]。

## 一个主实验与真实结果

环境为 Linux x86_64、Python 3.12.14 标准库。未修改上游模块；自写 harness 将画像目录指向虚构夹具，并按记录的 argv 调用原始组件。主实验有六个内部阶段：

1. 建立六文件虚构画像，只修改 `style.md`，其余五维指纹保持不变；验证读取与前缀行为，没有验证模型实际遵守画像
2. 显式调用输出路径验证器，四个不合规路径被拒绝，再保存本地草稿；`manifest` 没有自动调用该验证器，不能称为上游统一沙箱
3. 观察初稿失败：计数 365，超过自选 140±5%（133–147），长度检查退出 1；合成私网 IP 命中 1 处规则，CLI 扫描退出 7；`latest` 实际返回 `failed`
4. 人工修订后计数 143，两项检查退出 0；步骤历史为 `done → failed → done`，项目仍为 `draft`；非法 `kind` 退出 2，元数据字节未变
5. 素材索引共 3 项，其中包括隐藏 `.easel.json`；按 `weibo` 及两个标签只找回 1 篇正文。平台来自路径规则，不是自动读取 manifest 的平台字段
6. 运行原始 manifest、wordcount、content_guard 三个 selftest 入口，并核对复制模块指纹未变

统计分别为 **15/15 项自写命名检查、3/3 个上游 selftest 入口、20 次组件调用**，不得相加或以重放次数增加用例总数；没有运行全量 pytest。指南第一条命令执行上述完整六阶段，后五条读取并验证产物，不是六次独立业务执行。

原学习独立审核从当时最终 PDF 提取第 16–21 页的六条命令，与当时 HTML 逐字核对，并在全新解包目录逐条重放，六条退出码均为 0。原学习的 24 页 PDF 具有逐页实际像素审核记录；HTML 只做结构检查。本次公开整理的内容清理、PDF 重建与复核另记于配套独立审核日志，不把历史重放记作本次重新实跑。具体时间、原始输出、失败判据与整改过程见下方实验及审核日志。

## 坑与结论

- 登记路径不证明文件存在或可用。`.easel.json` 是薄索引，不能把正文或完整创作意图压成一句摘要后丢掉原文
- 项目标签不等于发布回执，最近一条记录不等于最近成功。要读取步骤结果，再核对真实产物与外部效果
- `guard_or_die` 在执行模式且未显式放行时才阻断 BLOCK；CLI `scan` 的 BLOCK 退出 7。扫描通过不等于事实、版权、质量、授权或平台接收通过
- `publish-checklist` 文档提 `meta.json`，总规范采用 `.easel.json`；规范与消费者仍要逐项对拍。画像也不等于账号登录态或强制记忆隔离
- 原始首次 harness 尝试在环境描述阶段被自身进程内审计 hook 拦住；改用 `os.uname` 后第二次成功，两次记录保留。该 hook 是测试守卫，不是 OS 级沙箱
- 原始 manifest 自测故意触发非法 kind 的 argparse stderr，但自测入口退出 0；不能仅看 stderr 就误报失败。日期和绝对路径随重放变化，不宜直接比较不同时区时间字符串

未测范围：OpenClaw 宿主、Easel 主 CLI、Web 服务、模型推理、生图/TTS/视频、真实账号登录、平台审批、外部发布、数据归因与营销效果；`archive/--apply` 未执行。140±5% 仅为练习阈值。原始社交链接当时访问受阻，因此不声称当下读过原帖。上述有限组件验证不能推出完整系统已验证，也不代替本人确认任务完成。

## 六份配套学习成果

- [彩色指南 PDF](../../easel/delivery/easel-guide.pdf)
- [指南 HTML](../../easel/delivery/easel-guide.html)
- [可重放练习 ZIP](../../easel/delivery/easel-exercise.zip)
- [实验日志](../../easel/delivery/easel-experiment-log.md)
- [知识查重与入库提案](../../easel/delivery/easel-knowledge.md)
- [独立审核记录](../../easel/delivery/easel-independent-review.md)

配套知识稿保留学习审核时的入库提案与当时范围；本页及关联概念记录其知识合并结果，不追溯改写早期实验记录。Git 同步结果应以实际远端提交为准。

## 固定源码依据

- [产物接口规范](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/docs/SKILL-SPEC.md)：薄索引、输出布局与 `brief.md`
- [manifest 实现](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/shared/scripts/manifest.py)：展示头、步骤历史、`meta/record/latest`
- [输出路径校验](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/shared/scripts/output_paths.py)：路径布局与拒绝条件
- [画像助手](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/easel/persona.py)：画像文件读取与宿主前缀
- [内容扫描与执行闸门](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/shared/scripts/content_guard.py)：BLOCK/WARN、入口参数与退出码
- [素材索引实现](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/openclaw/asset-manager/scripts/assets.py)：扫描、标签、检索与路径识别

阅读方法：[原 learn-project 方法](https://github.com/Smashwinny/reminder_knowlege/blob/109ffa9763c24f6ff05d2b7f1b1d9ed14e7d79e0/.claude/skills/learn-project/SKILL.md)。本次以该方法的第 8 步合并同义概念、项目笔记与 MOC；不把有限查重范围写成全库无重复，也不把笔记存在视为本人已掌握。
