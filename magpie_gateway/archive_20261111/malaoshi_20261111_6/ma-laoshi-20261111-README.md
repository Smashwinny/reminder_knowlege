# 第6项 magpie 网关 · 研究与离线实验
状态：真实完成（限定公开研究与离线mock；不表示真实产品集成完成）。
所有时间使用北京时间（Asia/Shanghai）。所有候选成果仅保存在当前独立目录。

## 打开哪个文件
- ma-laoshi-20261111-index.html：单文件轻量彩色学习指南，12问12图、4用途、5步真实实验。
- ma-laoshi-20261111-magpie-gateway.pdf：实际Chromium打印A4，9页，已逐页Read目视检查。
- ma-laoshi-20261111-exercise.zip：两份Python标准库代码和README，解压即可运行，无密钥。
- ma-laoshi-20261111-experiment-log.md：真实命令及原始输出，4个测试分组和编译均成功。
- ma-laoshi-20261111-sources.md：固定SHA、URL、读取成功/失败、原始资料SHA256。
- ma-laoshi-20261111-knowledge-proposal.md：仅合入建议，未触共享vault/Git。
- ma-laoshi-20261111-pdf-review.md：9页逐页检查记录；png位于pdf-review/。
- ma-laoshi-20261111-MANIFEST.sha256：交付内容哈希。
- ma-laoshi-20261111-delivery.zip：本项交付总包。

## 真实完成范围
原帖长文、作者18条回复及其引用上下文、官方公开源码与FAQ/条款实读。原帖没有引用帖对象。固定main SHA与日期。真实启动本地HTTP mock和自写网关，测试文本转换、双模型路由、用量累加、6类拒绝及上游错误。没有跑magpie二进制或Kiro插件。

## 待验证 / 未执行
实际magpie/Claude Code/Desktop集成、Kiro授权/额度、真实模型身份/质量、SSE/工具/多模态与缓存历史修复。真实账户环节被本次研究-only授权排除，不应继续尝试。不接真实Kiro、不登录任何账户、不读凭证、无付费模型调用、无用户本机或配置操作。

## 风险结论
Kiro FAQ直接禁止绕过原生接口的第三方automation harness路由。作者“不会封号”回复不能当保证。AWS条款50.14处理合同主体与滥用检测，不把它冒引为逐字禁止反代条款。优先官方Kiro原生/ACP允许路径，或具备合法模型访问权的官方Claude网关/API方案。
