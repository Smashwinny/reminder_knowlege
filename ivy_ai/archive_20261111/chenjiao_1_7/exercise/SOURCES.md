# 第7项来源清单
访问日期：2026-11-11（Asia/Shanghai）
- 原帖：https://x.com/i/status/2112109068584473072；已读全文（note_tweet或article.plain_text），原始JSON和正文见本目录。
- 引用/嵌入帖：https://x.com/i/status/2111853756245737775；文本已读，快照quote-2111853756245737775.txt。
- 引用/嵌入帖：https://x.com/i/status/2111732478486761627；文本已读，快照quote-2111732478486761627.txt。
- 查重总览：https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md
- 知识库main SHA：`a8674777e18302b8804b137212b1396cbfe5a747`
- 已读相关笔记：接缝与桩实现StubSeam、级联语音管线、证据优先质检ProofOverClaims、项目笔记/muse_gadget_sdk。固定快照保存在批次vault-snapshot。
- 样式参考：同SHA的12306_mcp/12306_mcp-guide.html；青蓝渐变、大号编号、橙色重点、卡片问答与实验输出。
- 一手仓库：https://github.com/iamankushpandit/esp_ai/tree/35b2b77088a511a9fdaf3ee5f06ac7ed7bd069cc；SHA `35b2b77088a511a9fdaf3ee5f06ac7ed7bd069cc`。取回文件（非全量逐文件精读）：README.md, components/story_core/include/story_arena.h, components/story_core/story_arena.c, docs/MEMORY_BUDGET.md, host/test_arena.c, host/test_intent.c, host/test_wrap.c, main/hwtest.c, main/hwtest.h。
- Ivy项目官网：https://iamankushpandit.github.io/esp_ai/（检索定位线索，一手细节以固定SHA README和源码为准）。原帖引用实际讲Groki，不能作为Ivy证据。
- C源、测试、日志桩、许可均取自固定SHA；版权归iamankushpandit，GPL-3.0-or-later及SDK linking exception见exercise/upstream/LICENSE、LICENSE.exception、NOTICE.md。原件未改算法。
- 同SHA README内部arena约145KB，MEMORY_BUDGET.md仍写264KB且含早期阶段；数值不混拼。

## 本批证据边界
原帖正文均可读取，未因不可读跳项。媒体视频未观看，不能核实画面。日志只记录实际命令和输出；代码中合成数据、日志桩、未测硬件逐项标明。没有用户密钥、付费API、用户硬件写入或Git发布。

## 原创与上游代码指纹
- exercise/lab.py — SHA256 `eec982d5e824f8dad41216f6fda87cb42e4a78cd591a6dbe787247ce467d13d9`
- exercise/upstream/components/story_core/include/story_arena.h — SHA256 `63f9d43eb9e6df81553d440bdb6129970ba855bb8089e21e144f2159c4bdbb56`
- exercise/upstream/components/story_core/include/story_log.h — SHA256 `9066e3d6eeaa31000bdc18edc7a249740ef5d600829a05c606183c8ba0c149df`
- exercise/upstream/components/story_core/story_arena.c — SHA256 `a5aea3d22b5706714586fc9ca5b045ff11ffece77e238de16c3dd988d1997fcb`
- exercise/upstream/host/check.h — SHA256 `c0a335680a271435a53a0e2a0b46444fa520f98279b564e3849c0715ac5d6bc7`
- exercise/upstream/host/stubs/esp_log.h — SHA256 `12bc7e0a3dce75e55f776ff115f9863ce961042f480dc0c0fdbbafe3293b6dd2`
- exercise/upstream/host/test_arena.c — SHA256 `a573c4b1d9043e58bb394a772a1429295308da947adfa50b7fba7d68ee288b03`

实际精读：各项目README/小智README_zh，Ivy内存预算与arena源/测试；宗主GUIDE接口章节。其余取回文件供追溯，不声称全量审核。
