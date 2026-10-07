# WeChatBridge historical experiment record

Local sanitized-copy note: no experiment, SDK setup, fixture generation or upstream execution was performed. Original 2026-10-05 commands, timings, first failures and results remain historical; private absolute paths inside bundled reference evidence use role labels. Current static-member hashes are in bundle_manifest.json, while the 68 generated-output fingerprints describe the historical run.

Date: 2026-10-05 UTC. Environment: Linux x86_64 / Debian 13. Fixed genuine source commit: 07b88822debc3bd544ae7a83bc207633b29c3a04. .NET SDK 10.0.401 / runtime 10.0.12. No external NuGet packages. 46 upstream Core source/project/resource files copied byte-for-byte; repository remained unchanged. Only synthetic chat and attachment data were used.

## Exact six-step replay

From the extracted wechat_bridge_core_exercise directory, execute in order. These exact commands ran successfully in the author environment. Author setup reused the already downloaded, SHA-512-verified official SDK; build was incremental in this sequence. The fresh-unzip reviewer must record separate clean-build times and disclose SDK reuse. Full initial SDK download was 240,059,572 bytes; no isolated download-duration claim is made.

- python3 run.py setup: 0.425859 seconds, passed
- python3 run.py verify: 0.003182 seconds, passed
- python3 run.py fixtures: 0.034352 seconds, passed
- python3 run.py build: 1.792932 seconds, passed
- python3 run.py test: 0.912589 seconds, passed
- python3 run.py report: 0.012787 seconds, passed

Outcome: 42 passed / 0 failed; machine report test duration 247.7362 ms. The later printed SUMMARY includes JSON/report write overhead. Build output: 0 warnings / 0 errors.

## Test coverage

- Archive: 21 cases for stored/deflate payloads, two-message Chinese UTF-8 multiline/BOM/CRLF, attachment hashes, unfamiliar TXT, attachment-only input, malformed/empty/CRC/encrypted/oversized/unsupported/duplicate archive refusal, traversal/absolute/symlink/case-alias path refusal, nonempty destination, cancellation and invalid dates
- Staging: 8 cases for invisible Staging then Ready rename, byte hashes, duplicate naming, invalid second-item rollback, per-file and total limits, suffix-only validation, cancellation and source symlink rejection
- Intent/state: 6 cases for sequential consume-once/restart, exact 90-second expiry, malformed intent consumption, first-seen and metadata persistence, copied model status and future-timestamp characterization
- Collections: 7 cases for ordered freeze and late-share split, restart retry/no recollection, remove/undo and interrupted-removal recovery, corrupt/newer ledger refusal, explicit naming, and protected retention

## Actual failures and adjustments

1. First timing command failed because /usr/bin/time is not installed. Replaced by Bash time, then Python monotonic timing; no upstream change. See reference/logs/build-first.log.
2. First harness run reported 41 passed / 1 failed (I05). The harness wrongly compared an in-memory timestamp retaining fractional seconds to persisted JSON using the upstream whole-second UTC converter. Corrected only the assertion to compare persisted outcome time with persisted batch time. Source hashes remained unchanged. See reference/test-results-first.json and reference/logs/test-first.log.
3. Final focused run and six-step replay both passed 42/42. This is a scoped custom harness against actual upstream Core, not the repository's complete xUnit or macOS suite.

## Failure criteria and interpretation

Every script step exits nonzero for an error; stop at failure. Hash mismatch blocks source trust; SDK checksum mismatch blocks extraction/execution. Build errors block tests. Any failed test blocks the final report. The intentionally duplicate ZIP entry produces a Python warning during fixture generation; that warning is expected test data, and the genuine parser rejects that archive.

InboxWriter accepts .zip-named non-ZIP bytes. Durable Ready publication is not archive-integrity approval. Future timestamps satisfy the current age <90 seconds check. Sequential read-delete intent behavior does not prove concurrent exactly-once delivery. GUIDs are identifiers, not content hashes. Copy/Delivered model values do not prove native clipboard or actual receiving-app behavior.

Not tested: native macOS Share Extension, accessibility/OCR/App Group signing, Windows WPF/Explorer Share Target/Win32 delivery, real WeChat data, any actual clipboard/paste, real knowledge-vault write, target-agent ingestion/upload, native installers/updates. No assertions claim these passed.

## Synthetic inputs and hashes

- absolute.zip: 131 bytes; SHA-256 3d586ee733a4e9772866647d6a9156fe481cefeabe8c8e44ff37baa7c554f47c
- attachment-only.zip: 196 bytes; SHA-256 a5e79fe5038ee43a6b90b34d33372aa03ddd12772dbb0874305c92207fa92863
- bad-crc.zip: 413 bytes; SHA-256 c1773431267472272fc48be6d3fca6b0cb0c8c5db7bf6545712910d42d46b03c
- case-alias.zip: 224 bytes; SHA-256 2f238498936946d5f40abfa5f78ed1cbd53253c73340e06ed45ae378ab523027
- crlf-bom.zip: 250 bytes; SHA-256 4b0f833f14911cc56cc2a514a9c3c6db5c231d9e814b5bd08e1e00733f8de6a5
- deflated.zip: 390 bytes; SHA-256 65b1f61e67dca488ad1947968ecd29f8102b951b7d024d38653385ced59f9822
- duplicate.zip: 208 bytes; SHA-256 1b230369dfde7434747d4c097cfe8a9b6be2a07179b8b80f94b363f38dc9f0bd
- empty-file.zip: 116 bytes; SHA-256 1e936cea33177aafca203eb660328eded177d48fdac4c93712d1aac82bd51dbd
- empty.zip: 22 bytes; SHA-256 8739c76e681f900923b900c9df0ef75cf421d39cabb54650c4b9ad19b6a76d85
- encrypted-flag.zip: 413 bytes; SHA-256 56a2487e5e7d532c9f9a7d29ac6d3e19e9e2ff84ab78f2b36f5f95049606ffce
- expected-attachment.bin: 64 bytes; SHA-256 fdeab9acf3710362bd2658cdc9a29e8f9c757fcf9811603a8c447cd1d9151108
- expected-transcript.txt: 109 bytes; SHA-256 e57e32949a4aa07cc7d8de42b794bda1da4df69949d5d47e6e790b59a0936139
- not-a-zip.zip: 23 bytes; SHA-256 864142bd3ff3528faed331d9f2c83a4e1c86f4b6251a154ee36ea6ed7e507589
- notes.txt: 37 bytes; SHA-256 01ea241590ee236dc8a0c2cca82fdde0be635da5e330e0e5b7665c6278a38557
- oversized-declaration.zip: 413 bytes; SHA-256 082c81c274adea983a458f08f060d892bca16676ab7ab68aedfa66a3b711f669
- stored.zip: 413 bytes; SHA-256 3eb53c87fd0489fe34bed4e65c7fbb7571b4936cf07c72a85547930cc5126a20
- symlink.zip: 116 bytes; SHA-256 5d860100523b469a6620bd2a40bb9ee4379629eb2bc5a3c07ea64bf92c00378c
- traversal.zip: 135 bytes; SHA-256 884959408fdfd98e9653f66e07a83720816010de5dc1942389ccc4163d0f92c8
- unknown-text.zip: 158 bytes; SHA-256 8af4fdc321ad2e22574213146defc4eb1248b861e3f1c203f69437290d085748
- unsupported-method.zip: 487 bytes; SHA-256 35ba6a4a9ae6c7f47cb6759790b6a180bac2c8544ab3ae086a729195d804de53

The reference/six-step-experiment-report.json records SHA-256 and sizes for all 68 generated regular output files. Nonportable symlink fixtures are excluded from that regular-file list; no private inputs are present.

## 交付补充：按实际调用收窄用例名称

上文是原作者实验记录，保留其原貌；此段依据冻结 harness 补充精确范围。C05 实际只构造 schemaVersion=8 的账本，验证其被拒绝且原文件未覆盖，并没有同时执行任意损坏 JSON 的收集账本用例。Reader/CollectionService 的恢复检查是在同一进程中新建对象并重读磁盘状态；部分中断状态由测试显式构造。它们不是强杀进程、真实重启、断电或多消费者并发实验。

历史原件完整保留。当前副本仅规范化 reference 日志与报告中的绝对路径，并概括来源整理信息；stdout/stderr 的错误、用例、计时与结果不变。指南及知识笔记继续按此较窄范围解释证据。


## 当前本地副本检查

PDF 由 ReportLab 直接重新生成，并逐页渲染查看；HTML 仅结构检查。HTML 浏览器视觉及 HTML 转 PDF 原路线受环境限制，本次未重试。ZIP 原 105 个成员保持相同范围；46 个 Core 文件、许可和第三方声明、自编脚本、harness 及 20 个合成输入均保留原字节。历史 42 个案例不增加为新测试，初次 41/42 与计时工具缺失记录均保留。当前检查不涉及原生应用、真实聊天、目标 Agent 或真实知识库。

当前副本 ZIP：195021 字节；SHA-256 13b444e0f69f01b311bda92d68ccf8a9589b4344327fc5abcc01e8273c29c4f4
