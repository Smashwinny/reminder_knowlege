# 第7项来源与阅读范围
2026-11-11 Asia/Shanghai；原帖和引用完整文字已实读，原视频未观看。
- https://x.com/ai_xiaomu/status/2110742894776885607 ：2026-10-15 22:41:36 Asia/Shanghai，转述矩阵数字人+Opus。
- https://x.com/wang_aoqi/status/2110700648593600749 ：2026-10-15 19:53:44 Asia/Shanghai，称2号4视频约100客资及数字人/音色克隆/Opus动画；未公开工程/完整参数，客户数与效果未独立核验。
- 原始X MCP响应保存于item06/research/x-original-and-quotes.txt；本轮核对返回ID后抽出两个完整post至source-post.json。原误标文件隔离history，不作为证据。只学习方法线索，不声称复现原作者模板或原视频。

## 去重与一手实现依据
- vault固定main基线a8674777e18302b8804b137212b1396cbfe5a747：https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747 。总览本批此前已读；复用本轮第6项复读的React逐帧视频渲染、动效描述词表和ai-video-pipeline笔记。
- 同批item04/experiment-log.md、item05/knowledge-proposal.md、item06/knowledge-proposal.md：已有底层渲染、门禁与BGM，不重复新增概念。
- https://github.com/remotion-dev/remotion/tree/e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d ：沿用固定源码、LICENSE与4.0.542依赖。Sequence文档本轮第6项已读1–120行。
- https://www.remotion.dev/docs/use-current-frame ：本轮直接实读，说明帧从0开始，定时父层内获得局部帧；全局帧须在上层读取。实际SVG人物全局时钟、内容局部时钟用本地源代码和视频核验。
- worker自写：src/template.json、SVG占位形象、validate_template.py、verify.py；无外部人物图片/音频，无模型API。

## 许可与边界
Remotion采用自己的许可，不是MIT；本次非商业评估，商业/团队应按资格核查。依赖Node24.22.1、Remotion4.0.542、React19.1.0、TS5.9.3，沿用第4项已装运行环境；WeasyPrint70.0打印11页A4并逐页PNG+Read。人物ROI两帧变化不是口型/身份测试，配置校验不是安全沙箱或身份授权系统。未购买、索key、发布或合入vault。
