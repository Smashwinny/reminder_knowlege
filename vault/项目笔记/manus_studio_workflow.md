---
tags: [项目笔记]
类别: 知识学习类（视频工作流）
来源项目: manus_studio_workflow
完成日期: 2026-11-22
---

# manus_studio_workflow：官方分层接力与本地保守协议

## 项目是什么

学习对象为 Manus 2.0 Video Editor 及原帖 Cue 案例。官方页面确认独立轨道、可编辑工程、人工修改以及“从人工修改继续”。本地另写 locked 保守交接协议，不能把该协议冒充为 Manus 内部字段或产品承诺。

## 来源核实

- https://manus.im/blog/introducing-video-editor
- https://manus.im/blog/introducing-manus-2-0
- 原帖作者入口：https://x.com/Nin19536

2026-11-22 官方 Video Editor 页面未提 locked 控件/字段，也未给具体导出工作流。主帖 140 万与厂商 170 万播放两口径不作审计，24 小时案例无工程文件佐证。

## 带来的概念

- [[分层时间轴人机接力]]：保留同一可编辑工程，与 [[上下文接力]] 的文档搬运、[[人机协同Interrupt]] 的暂停恢复区分。
- 不新建“品牌上下文最小集”：slogan/tone/禁用项/参考案例只是起步检查表，“四项约束 80% 偏差”无依据已删除。
- [[证据优先质检ProofOverClaims]]：官方产品事实、本地协议、案例宣传和真实导出分开。

## 实验做了什么

`exercise/timeline_relay.py` 用深拷贝跑两条路径：尊重锁定时 5 个未锁元素润色、人工 s2 值和备注保留；删除保护时同一 s2 确实被覆盖。默认与自定义合成素材两条命令均复跑，全部断言 PASS。初版只改 note 不会覆盖 value，破坏测试无效，已修复。

## 坑与结论

- 未登录 Manus，真实轨道、AI 接力、视频生成与导出均未实测。
- 分层有利于局部修改是通用工程判断，不是对 24 小时案例瓶颈的已证实归因。
- v2 指南共 10 页，全部逐页渲染检查，原 PDF 保留，manifest 指向 v2。
- 指南：`manus_studio_workflow/manus-studio-guide.html`；审核版：`manus_studio_workflow/Manus-Studio视频工作流-小白指南-v2.pdf`。
