---
tags: [项目笔记]
类别: 开源项目类（宿主插件）
来源项目: qiaomu_rss_dsh
完成日期: 2026-11-22
---

# qiaomu_rss_dsh：固定插件审计与伴读范围实验

## 项目是什么

joeseesun/qiaomu-rss-dsh 是 DeepSeek Harness 社区 RSS 插件。固定 commit `349398b` 审核 8 个 rss_* 工具、README/package 版本漂移、GPL 与名单许可及隐私开关；未安装宿主或运行上游插件。

## 来源核实

- 上游：https://github.com/joeseesun/qiaomu-rss-dsh
- 固定 commit：https://github.com/joeseesun/qiaomu-rss-dsh/commit/349398b
- 宿主打包文档：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/publish.md

固定版本 README 安装段 v0.7.0、package.json 0.9.0，不冒称当前 main 仍相同。初学期真实 blog.python.org 记录与本轮合成夹具分开。

## 带来的概念

- [[背景摘录与请求选段]]：截断必须标长度和 truncated，不能称整篇。
- [[固定版本中的跨文件时间漂移]]：追加 README/package 安装版本不同步案例，不新建同义概念。
- [[上下文预算与战略压缩]]：范围可见但自动首段不一定充分，真实回答仍需引用核验。

## 实验做了什么

默认离线解析 5 篇合成 RSS，首篇 1525 字符，输出背景 `1500/1525 truncated=True`。6 项 unittest 全部通过。前三次夹具 623/1199/1497 均未触发长文分支，测试失败被保留并修正夹具，没有降低断言。

## 坑与结论

- 未验证宿主伴读、真实 AI 引用或当前 main 漂移。
- GPL 段区分私人使用与分发义务，不用一句话替代许可证全文。
- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`qiaomu_rss_dsh/qiaomu-rss-guide.html`；审核版：`qiaomu_rss_dsh/Qiaomu-RSS插件-小白指南-v2.pdf`。
