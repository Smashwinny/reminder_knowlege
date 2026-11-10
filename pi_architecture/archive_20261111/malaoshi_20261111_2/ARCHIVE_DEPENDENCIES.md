# 公开归档与练习依赖说明

项目：Pi 不是一个包  但你的版本只有一个；原材料：马老师 第20261111批 第2项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/agent-kernel.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/archify.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/源码取证图.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/事实与判断分离.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/固定版本中的跨文件时间漂移.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/archify/archify_guide.html
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/CHANGELOG.md#L3-L64
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/CHANGELOG.md#L61-L64
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/package.json#L42-L67
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/CHANGELOG.md#L678-L709
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/README.md#L460-L490
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/README.md#L494-L506
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/package.json#L1-L29
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/package.json#L1-L83
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/package.json#L14-L29
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/package.json#L42-L83
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/provider-attribution.ts#L36-L96
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/settings-manager.ts#L945-L955
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/telemetry.ts#L1-L13
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/modes/interactive/interactive-mode.ts#L1192-L1239
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/agent/package.json#L1-L50
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/ai/package.json#L94-L119
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/codemode/src/runtime/vm.ts#L160-L180
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/docs/codemode.md#L3-L18
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/docs/security.md#L1-L21
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/package.json#L1-L24
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/package.json#L1-L97
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/package.json#L43-L65
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/src/core/settings-defaults.ts#L57-L60
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/src/extensions/codemode/index.ts#L1-L45
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/package.json#L1-L174
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/env/package.json#L1-L54
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/mcp/package.json#L1-L60
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/mcp/src/config.ts#L85-L140
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/schema/package.json#L1-L60
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/CHANGELOG.md#L13-L17
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/CHANGELOG.md#L15-L18
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/CHANGELOG.md#L18-L24
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/CHANGELOG.md#L24-L42
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/CHANGELOG.md#L3-L59
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/install-lock/package-lock.json#L462-L555
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/package.json#L1-L25
- https://github.com/earendil-works/pi/blob/06a466935536f8c9bcacb2d5efc0fc021be1bdff/packages/coding-agent/package.json#L14-L24
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/package.json#L1-L13
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/agent/package.json#L1-L50
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/ai/package.json#L1-L119
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/ai/src/telemetry.ts#L121-L153
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/ai/src/telemetry.ts#L15-L60
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/ai/src/telemetry.ts#L164-L205
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/ai/src/utils/identity.ts#L106-L143
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/ai/src/utils/identity.ts#L61-L82
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/chord/package.json#L1-L196
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/chord/src/telemetry-ingest/sender.ts#L1-L60
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/codemode/package.json#L1-L75
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/codemode/src/runtime/vm.ts#L160-L180
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/CHANGELOG.md#L139-L151
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/CHANGELOG.md#L355-L416
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/CHANGELOG.md#L574-L587
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/CHANGELOG.md#L934-L946
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/docs/codemode.md#L3-L18
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/docs/codemode.md#L60-L95
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/docs/mcp.md#L1-L32
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/docs/mcp.md#L30-L34
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/docs/mcp.md#L62-L82
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/docs/mcp.md#L92-L102
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/docs/security.md#L1-L18
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/install-lock/package-lock.json#L462-L563
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/package.json#L1-L24
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/package.json#L1-L25
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/package.json#L1-L97
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/package.json#L10-L24
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/package.json#L43-L69
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/cli/startup-ui.ts#L180-L198
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/core/client-identity.ts#L1-L16
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/core/settings-defaults.ts#L27-L34
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/core/settings-defaults.ts#L57-L60
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/core/settings-manager.ts#L1070-L1088
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/core/telemetry.ts#L1-L13
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/extensions/codemode/index.ts#L1-L45
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/extensions/codemode/worker.ts#L1-L6
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/modes/interactive/interactive-mode.ts#L1365-L1405
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/modes/interactive/interactive-mode.ts#L1472-L1488
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/coding-agent/src/utils/pi-user-agent.ts#L1-L6
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/durable/package.json#L1-L174
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/env/package.json#L1-L54
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/evals/package.json#L1-L22
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/mcp/package.json#L1-L60
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/mcp/src/config.ts#L85-L140
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/mcp/src/index.ts#L1-L96
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/schema/package.json#L1-L60
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/telemetry/package.json#L1-L54
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/telemetry/src/noop.ts#L1-L37
- https://github.com/earendil-works/pi/blob/65c43bb520edf53f11923f7a927aefd05475c6af/packages/tui/package.json#L1-L63
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/agent/package.json#L1-L68
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/README.md#L453-L479
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/README.md#L490-L502
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/docs/environment-variables.md#L70-L94
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/settings-manager.ts#L948-L968
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/utils/pi-user-agent.ts#L1-L4
- https://github.com/earendil-works/pi/blob/fab2c5353ea4adcbb0d35701897892941f185235/packages/schema/package.json#L1-L56

Pi 0.84.2 的原包名为 `earendil-works-pi-coding-agent-0.84.2.tgz`；须由官方 npm 包的精确版本恢复到 `exercise/lab/`，再按 README 解压。已有自写 manifest/switch/ping-mock 三个脚本保留。

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `evidence/core-freshness.json` | `054467d51a5ccf0cdf708d6fcfa821b00893ad7ce5184f13bd5ee6a467a9bd18` |
| `evidence/npm-0.84.2-metadata-prior.json` | `fc967bc6aea81a42291675515b7d0b64ed695a874561c70b1bf99a8c74afdf5f` |
| `evidence/preparation-notes.md` | `d14d75ea705207704c71d0702a025463eb60f1ef3afe7e476de3fc94456d60e5` |
| `evidence/print.log` | `7be6825cafbc6337633473f1ce3510cbe08d2c8d71bddbef9afdcadfbcddb61b` |
| `evidence/prior-audit.md` | `47feabbaa225be4d4d80d766142a7b0c4d439c4d48638101788fc6927727eaa2` |
| `evidence/prior-x-thread-page2.txt` | `406578449f2bc44ce935b419494e78d39528a7da1769aeaeba8b70475233a124` |
| `evidence/prior-x-thread.txt` | `1efea72e759848b946e88cebd2a3dce4d2788fd1c4d24cb3c43181356e0c3f9c` |
| `evidence/x-quoted-current.txt` | `c4419a9bdbd32f937d59812e5fc169567f9ab38f75c8ac3c357188e827c30193` |
| `evidence/x-thread-current.txt` | `323fcba80adef021d3638abd8d299577cd91a15e1ae3177d6270b15ec1e4a048` |
| `exercise/lab/earendil-works-pi-coding-agent-0.84.2.tgz` | `95b899cd7b1a0c1f0174c7bf33ab427435e3553a7d1f4756661aa9c7f1a68ffa` |
| `exercise/lab/pack.json` | `090acf0a54a4692768ceee6e3c67090457b8195fab9c01d6ddf88af2630db9e9` |
| `exercise/snapshots/0.84.2/packages/agent/package.json` | `ac5e13d2a2aa0d6c78394417b59e18cb0fe92f482d2b075b39bf165312db6c06` |
| `exercise/snapshots/0.84.2/packages/ai/package.json` | `9575365ce609dca8e1fd4fa72471d55006e1e0f81310c0808f93abc4bc14bbf9` |
| `exercise/snapshots/0.84.2/packages/client/package.json` | `beeb2fb7e577c83b372e7549362a58db8e24b03d50342cea7123cbc7407e9813` |
| `exercise/snapshots/0.84.2/packages/coding-agent/CHANGELOG.md` | `7e9e91204ee1f002052070a90332d24a166e0cbc433095cebe4136651e8d91c8` |
| `exercise/snapshots/0.84.2/packages/coding-agent/package.json` | `820f4adc6d61f2cefbc29ce17e9dfd9aa482248d54be5d0dfa2a868ca000c7b0` |
| `exercise/snapshots/0.84.2/packages/coding-agent/src/core/telemetry.ts` | `5ec837b287ea0303f704a5278c586e2a5d4003f3ad2ccad94997d2fa59164855` |
| `exercise/snapshots/0.84.2/packages/coding-agent/src/modes/interactive/interactive-mode.ts` | `ccc403e24d005b47632460c249cf154cdc576448ab32f7001fb6a9d562014b37` |
| `exercise/snapshots/0.84.2/packages/evals/package.json` | `6d35dc909522199ad0026986873b741ca042655ddf48843bf5587692e1479a4d` |
| `exercise/snapshots/0.84.2/packages/protocol/package.json` | `194ed3896da44fabe3cffef3b2abf28a41a4cc7c2e52375c630836274f54a6d7` |
| `exercise/snapshots/0.84.2/packages/server/package.json` | `93ad03f4dbfb8ef5cc4fe6d11049c44bed6197cee342353aba77b227440d83c5` |
| `exercise/snapshots/0.84.2/packages/telemetry/package.json` | `ba3e45a83f94a06a0f311b9412f99e73c760d3eb0adee5909e4f2a356f109958` |
| `exercise/snapshots/0.84.2/packages/tui/package.json` | `2c19fb7e3d1e83a461b6f020b2ffc118b435dcd78a07af8c8def72864cd09e6e` |
| `exercise/snapshots/1.2.0/packages/agent/package.json` | `541f131cd43832f75a9c64ee886c367c219c0772da7047c66053d7cc80db98b9` |
| `exercise/snapshots/1.2.0/packages/ai/package.json` | `3838d036bbb844ea6d4d08ef199423a0335022e34b5d5c8833257f64e4cae625` |
| `exercise/snapshots/1.2.0/packages/chord/package.json` | `d1013b1316b6a87d13c49dc6ff8bae6d46276b477d0eaf028eabd96d86b90247` |
| `exercise/snapshots/1.2.0/packages/codemode/package.json` | `c01c6c0aa35956b8624b8c977e51e55786b81d86f34a90d222ee9f03fe0c6091` |
| `exercise/snapshots/1.2.0/packages/coding-agent/CHANGELOG.md` | `aa489441e4fc3bd2cd3db1c2200549f79eb6a889a7148e4fb8d12bec0c1dbd1e` |
| `exercise/snapshots/1.2.0/packages/coding-agent/package.json` | `d4231a02b6a2ccb357a8e9e420fab9c217490137ade958d4a45a12e169daad0c` |
| `exercise/snapshots/1.2.0/packages/coding-agent/src/core/telemetry.ts` | `5ec837b287ea0303f704a5278c586e2a5d4003f3ad2ccad94997d2fa59164855` |
| `exercise/snapshots/1.2.0/packages/coding-agent/src/modes/interactive/interactive-mode.ts` | `18c012b507b3b510ef61a49b488230ad752e8021fd693a2045fc27655e930b15` |
| `exercise/snapshots/1.2.0/packages/durable/package.json` | `2fc81a444940fff9fe12bad39540a5a88a9dbcf6049dfece77005c6a281d16ad` |
| `exercise/snapshots/1.2.0/packages/env/package.json` | `61950be94c9d6bb8526714776e48d7f7ed7ad55347a453fe26f1fde85e4e0e65` |
| `exercise/snapshots/1.2.0/packages/evals/package.json` | `eb29e415350b7d8c53eec9d6bd7a229d1df7424d97cd48b3d02c6742dec15be0` |
| `exercise/snapshots/1.2.0/packages/mcp/package.json` | `2dd60991ac137e3e5daa06ea091cdcbbb533aff48b5709bed733c38596be6e74` |
| `exercise/snapshots/1.2.0/packages/telemetry/package.json` | `7706dafbe8f125e0d658690c3e5b11c8e265c2611b02eaea9218263424d4c527` |
| `exercise/snapshots/1.2.0/packages/tui/package.json` | `825dd2b1199043dadd9c4f9251dac888e41feef2b82dedba24f8ce7c88cfd42c` |
| `exercise/snapshots/LICENSE-pi` | `0457f5bcec3b3b211605dfb5d1a49042fd638f3686a410fe099c24a25af13c48` |
| `exercise/snapshots/audit-1.5.2/packages/agent/package.json` | `95152a1095f4677284afde73dcf7a8a1525f46be0831177611526c14cea2ccec` |
| `exercise/snapshots/audit-1.5.2/packages/ai/package.json` | `e3c1d5b591123b5ff36ad71001ed7024a7ff600c4807748f4417a0251b753391` |
| `exercise/snapshots/audit-1.5.2/packages/chord/package.json` | `73f1908d3655b3d4fb9903406583bdbba702bc64a3dda750b86bab90f7d65423` |
| `exercise/snapshots/audit-1.5.2/packages/codemode/package.json` | `5fef26332a79610bc737db5e84dd85dd0b8c77fa90a19b6c83707447ba18d9a1` |
| `exercise/snapshots/audit-1.5.2/packages/coding-agent/CHANGELOG.md` | `3b275b77d0f224915358c9cfe43fd9516ad37307f87377c636d1a91753499a60` |
| `exercise/snapshots/audit-1.5.2/packages/coding-agent/package.json` | `18b422b7d80f2caa2551d253c0a8409e1caa54b954bfb7d18252e507bb8a0318` |
| `exercise/snapshots/audit-1.5.2/packages/coding-agent/src/core/telemetry.ts` | `5ec837b287ea0303f704a5278c586e2a5d4003f3ad2ccad94997d2fa59164855` |
| `exercise/snapshots/audit-1.5.2/packages/coding-agent/src/modes/interactive/interactive-mode.ts` | `cd345cb77d54d9f57e78f2500bf81cc185aa4a51a8811f35accd561bb7e35725` |
| `exercise/snapshots/audit-1.5.2/packages/durable/package.json` | `dd6d059528f02bf0f8780894972cb51ae81c2c3c4a01246aa4edc1bebdaa6937` |
| `exercise/snapshots/audit-1.5.2/packages/env/package.json` | `f4156c38c13b78745d5eeb412c2f29b888672a77f1d96cf063fc3b861307867e` |
| `exercise/snapshots/audit-1.5.2/packages/evals/package.json` | `d15d6699345c381e412d7eb548c51ed0c52fca38112143c6909c9c10ce2970af` |
| `exercise/snapshots/audit-1.5.2/packages/mcp/package.json` | `25acfdf6beb2375a79e9edd3652e4849725cf553a3062c188238110db7221bb4` |
| `exercise/snapshots/audit-1.5.2/packages/schema/package.json` | `b0297552afe555ceb41c87632e3b43aa73a68cf8b8a8847a9383587567b09401` |
| `exercise/snapshots/audit-1.5.2/packages/telemetry/package.json` | `bf7908d77cf617b4cdc0277b10edd69ad837980fd1db5e2824a903dfe20a53a7` |
| `exercise/snapshots/audit-1.5.2/packages/tui/package.json` | `a69278408dbc23c0c6efe4079c99b012c14cf2bea78167b72334cdbe319ad4ec` |
| `exercise/snapshots/main-1.5.2/packages/agent/package.json` | `95152a1095f4677284afde73dcf7a8a1525f46be0831177611526c14cea2ccec` |
| `exercise/snapshots/main-1.5.2/packages/ai/package.json` | `e3c1d5b591123b5ff36ad71001ed7024a7ff600c4807748f4417a0251b753391` |
| `exercise/snapshots/main-1.5.2/packages/chord/package.json` | `73f1908d3655b3d4fb9903406583bdbba702bc64a3dda750b86bab90f7d65423` |
| `exercise/snapshots/main-1.5.2/packages/codemode/package.json` | `5fef26332a79610bc737db5e84dd85dd0b8c77fa90a19b6c83707447ba18d9a1` |
| `exercise/snapshots/main-1.5.2/packages/coding-agent/CHANGELOG.md` | `3b275b77d0f224915358c9cfe43fd9516ad37307f87377c636d1a91753499a60` |
| `exercise/snapshots/main-1.5.2/packages/coding-agent/package.json` | `18b422b7d80f2caa2551d253c0a8409e1caa54b954bfb7d18252e507bb8a0318` |
| `exercise/snapshots/main-1.5.2/packages/coding-agent/src/core/telemetry.ts` | `5ec837b287ea0303f704a5278c586e2a5d4003f3ad2ccad94997d2fa59164855` |
| `exercise/snapshots/main-1.5.2/packages/coding-agent/src/modes/interactive/interactive-mode.ts` | `cd345cb77d54d9f57e78f2500bf81cc185aa4a51a8811f35accd561bb7e35725` |
| `exercise/snapshots/main-1.5.2/packages/durable/package.json` | `dd6d059528f02bf0f8780894972cb51ae81c2c3c4a01246aa4edc1bebdaa6937` |
| `exercise/snapshots/main-1.5.2/packages/env/package.json` | `f4156c38c13b78745d5eeb412c2f29b888672a77f1d96cf063fc3b861307867e` |
| `exercise/snapshots/main-1.5.2/packages/evals/package.json` | `d15d6699345c381e412d7eb548c51ed0c52fca38112143c6909c9c10ce2970af` |
| `exercise/snapshots/main-1.5.2/packages/mcp/package.json` | `25acfdf6beb2375a79e9edd3652e4849725cf553a3062c188238110db7221bb4` |
| `exercise/snapshots/main-1.5.2/packages/schema/package.json` | `b0297552afe555ceb41c87632e3b43aa73a68cf8b8a8847a9383587567b09401` |
| `exercise/snapshots/main-1.5.2/packages/telemetry/package.json` | `bf7908d77cf617b4cdc0277b10edd69ad837980fd1db5e2824a903dfe20a53a7` |
| `exercise/snapshots/main-1.5.2/packages/tui/package.json` | `a69278408dbc23c0c6efe4079c99b012c14cf2bea78167b72334cdbe319ad4ec` |
| `exercise/snapshots/provenance.json` | `98b33aa203dd253231df9bac85d703f864b8b7b886240488de66f70169609c4f` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
