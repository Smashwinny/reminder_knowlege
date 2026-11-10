# 来源、固定版本与可读性

访问统一为2026-11-11 Asia/Shanghai；时间均已按Asia/Shanghai（UTC+8）标示。对非Git网页/帖子不编造commit SHA；本地证据SHA256在末尾和SHA256SUMS。搜索摘要只作定位，不作兼容性或性能证据。

## X原帖、两层引用与公开素材
|编号|URL|时间/状态|SHA|
|---|---|---|---|
|X0|https://x.com/i/status/2113232649552892028 （规范作者URL https://x.com/liangzhu_AI/status/2113232649552892028 ）|全文可读，已取note_tweet；创建2026-10-22 19:35:00 Asia/Shanghai；收藏2026-10-23|非Git，不适用|
|X1|https://x.com/dotey/status/2107144243726729645|全文可读；创建2026-10-06 00:21:51 Asia/Shanghai；引用X2|非Git，不适用|
|X2|https://x.com/vista8/status/2106647309102825969|全文可读；创建2026-10-04 15:27:12 Asia/Shanghai；未返回继续引用|非Git，不适用|
|图1|https://pbs.twimg.com/media/HTxQRpWawAET9Fn.jpg|已下载并Read原图，计算器授权失败与Hook建议；不是本轮实验|非Git，不适用|
|图2|https://pbs.twimg.com/media/HTxQV9Ga4AAem72.jpg|已下载并Read原图，浏览器白名单与现有登录态风险；未照做|非Git，不适用|
|视频|https://video.twimg.com/amplify_video/2107144138705555456/vid/avc1/1280x720/Mrd-iwVD9zQ4puDZ.mp4|30.058667秒；已下载并用ffmpeg抽样6帧，Read联系图；未连续观看或听音轨，不当作实测|非Git，不适用|

工具：x.get_posts_by_id；显式读取note_tweet、referenced_tweets及作者字段。全文人工转录保存在sources/x-reading.md，不冒充原始API转储。没有追查全评论区。初次urllib素材403；普通公共curl成功，已据实际内容阅读。

## 知识库查重与旧风格
知识库main固定SHA：`a8674777e18302b8804b137212b1396cbfe5a747`；本项先git ls-remote并在交付前复核，未变化。复用上一项浅克隆 `/workspace/learn-batch/_common/reminder_knowlege`，严格只读；未fetch、checkout、合入或写入。直接项目关键词amontlabs或/lcu在vault中命中0，见sources/dedup-summary.json；相关概念已人工阅读。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md — 前项已实读，本项复用相同SHA的总览与方法。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/程序化工具调用.md — 本项实读；不重写代码式工具基础定义。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/工具目录膨胀.md — 本项实读；仅补LCU双入口与隐式复杂度。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/无障碍树语义桌面自动化.md — 本项实读；不重复通用AX概念。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/沙箱与审批正交.md — 本项实读；补平台权限差异，不重建概念。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/agent_desktop.md — 本项实读；区分观察/动作验收与模拟协议证据。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/agent_desktop/agent_desktop-小白指南.html — 前项已研究的旧风格；复用01-elyterminal/_tools的卡片、问答、SVG与显式分页模板。

## 一手项目仓库
URL https://github.com/amontlabs/lcu ；浅克隆main成功，固定HEAD `a7e30c1862707214dfe748d410854771ab4f4494`。git ls-remote复核一致。提交时间2026-11-10 19:24:21 Asia/Shanghai（原始Git输出为12:24:21+01:00）；提交标题是0.13.6发布说明，但不把main当发布归档，也没有验证任何发行包校验和。

- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/README.md — 全文实读；当前条件、平台、正式/实验适配与无需Python。本地upstream/README.md。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/LICENSE — 全文实读；MIT只覆盖LCU源码。本地upstream/LICENSE。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/docs/PROVENANCE.md — 全文实读；桥与原始组件的分发/许可边界。本地upstream/docs/PROVENANCE.md。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/docs/PARITY-STATUS.md — 全文实读；历史局部保真记录，非本轮复测。本地upstream/docs/PARITY-STATUS.md。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/docs/INSTALLATION.md — 前提部分13–40与定向搜索；不声称全文阅读或执行安装。本地upstream/docs/INSTALLATION.md。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/docs/ADAPTERS.md — 实读1–180及262/282等权限关键段；宿主合同、平台差异、收尾与Schema适配。本地upstream/docs/ADAPTERS.md。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/docs/releases/0.13.6.md — 实读参数oneOf→兼容对象变化说明；非本轮修复验证。本地upstream/docs/releases/0.13.6.md。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/adapters/package.json — 实读；MCP SDK依赖1.30.0；本练习无需安装SDK。本地upstream/adapters/package.json。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/adapters/client.mjs — 精读MODEL_TOOLS、createWorkerTurns与call选段；未导入/启动原服务。本地upstream/adapters/client.mjs。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/adapters/host-guard.mjs — 全文实读并以原样纯测试执行；无真实权限改动。本地upstream/adapters/host-guard.mjs。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/adapters/test/host-guard.test.mjs — 全文实读，7项夹具测试实际通过。本地upstream/adapters/test/host-guard.test.mjs。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/tests/mcp_client.py — 全文实读，原样Client实际对接自编模拟器。本地upstream/tests/mcp_client.py。
- https://github.com/amontlabs/lcu/blob/a7e30c1862707214dfe748d410854771ab4f4494/adapters/test/mcp-fixture.mjs — 全文实读作测试夹具参考；本轮未执行该文件。本地upstream/adapters/test/mcp-fixture.mjs。

## 官方协议一手文档
以下三个固定版本页均已WebFetch全文实读；Git SHA不适用，引用版本为2025-11-25。人工摘录保存在sources/mcp-spec-reading.md。未将新版本或完整MCP合规当成本轮结果。
- https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle
- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools

## 版本冲突与未采纳材料
1. X1说Python3.12+，固定main明确不需要Python；历史帖不覆盖当前安装说明。本练习的Python驱动只是教学实现选择。
2. README的泛化逐应用权限表述不能代替ADAPTERS Linux专节：该节记录原始Linux运行时没有逐应用审批，宿主工具审批是关键闸口。
3. 引用配图含自动回复审批/扩大Chrome白名单/修改设置等建议，仅作为外部风险材料，未执行；本项授权不包括这些动作。
4. X1“逐字节相同”是上游特定macOS记录；当前Claude schema还做兼容性变换。本轮未测原始运行时保真或性能。
5. search仅发现其他修订版本网页，不据摘要推断其协议合同；本实验仅固定2025-11-25。

## 本地公开证据哈希
- `sources/dedup-hits.txt` SHA256 `ae9bf10d4a0c79fa29e69b718e9215940b4a920069d9df5c1aa1b6da7998c623`
- `sources/dedup-summary.json` SHA256 `87eab193031614ff8a3463e7135a58a54fb82119114f04e3a9c8ed026554ba46`
- `sources/ffmpeg-samples.log` SHA256 `bb278d5324a877c4f2d9638849bf217c63209ff08ff44f585848b78894cf138c`
- `sources/mcp-spec-reading.md` SHA256 `68c1aaf4fd3d1e8d5e2c4bcac37b97c00ca41266bec19310df1f1cd82706dfc6`
- `sources/quote-image-1.jpg` SHA256 `368b248eb78fa53d454b3d3e434a90a9a5bab6f126a7f8725de9bf9d6efba6c3`
- `sources/quote-image-2.jpg` SHA256 `e422d5ff12aca673b28130fd7cf949dd921f65c5b3b610b4041483e45eb1300f`
- `sources/quote-video-samples.png` SHA256 `a04b9f7a5099a427cd1a27cb021803476e85d14ae8aabc6ff14e0251c95a4b94`
- `sources/quote-video.mp4` SHA256 `d3bcd01b54c43e90588ad920ebb85f06f4b92503556e06ea4866f159184cad37`
- `sources/x-reading.md` SHA256 `7ed3e1202a9a41bf854fd972f86c77070be10c14f65cc1fbe760342fe7e2a40a`
