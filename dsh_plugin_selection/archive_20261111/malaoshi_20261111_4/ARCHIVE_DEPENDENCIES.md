# 公开归档与练习依赖说明

项目：不是装满插件  而是补上一个痛点；原材料：马老师 第20261111批 第4项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/docs/billing.md#L7-L23
- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/lib/pricing.js#L1324-L1385
- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/lib/pricing.js#L1366-L1418
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/README.md#L22-L28
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/README.md#L94-L119
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/src/runtime.ts#L102-L132
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/src/runtime.ts#L15-L16
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L101-L144
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L128-L144
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L14-L18
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L35-L50
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/README.md#L63-L74
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/package.json#L1-L70
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/src/snapshot-format.ts#L595-L660
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/LICENSE#L1-L25
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/README.md#L58-L101
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/src/model-approval.mjs#L1-L11
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/src/service.mjs#L191-L216
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L29-L33
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L3-L19
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L35-L55
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/README.md#L5-L27
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/cordis.patch.yml#L4-L10
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/release.json#L1-L5
- https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/package.json
- https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/package.json
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/package.json
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/package.json
- https://github.com/tt-a1i/archify/blob/7e45f36c66de1254d5ad6ba1d878f6499ea269fd/integrations/deepseek-harness/package.json
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/archify.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/dsh_plugin_upgrade_skill.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/metrik.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/用量、额度与估算费用的计量分层.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/源码取证图.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/事实与判断分离.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/固定版本中的跨文件时间漂移.md
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/archify/archify_guide.html

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `evidence/article-relay.json` | `3ea926fbb3991573e636b09d7c67296e3bbeab98d18837df8d3f9d868110c90b` |
| `evidence/article-text.txt` | `adc7bd00621e56f6f7444174ab8a19ca5c29af906551dd32111eec4a122d6f05` |
| `evidence/experiment-first-failure.md` | `34665a77788d1978977bcc28b08608b71e70e9a64773e88ff17bedee611a6dc0` |
| `evidence/print.log` | `8f6a91d8f0b877c245d6ec851acbcfcdaa9b8d9c3e25ade6a10e534cabd35aae` |
| `evidence/repositories.json` | `a2de0a4569142f11dfe408252d33ceb7d6110f8b6bdb7bf75dd296361feb5c95` |
| `evidence/runtime.txt` | `c423b9c020dfc6654ae6008c27cc95c304afc8c71977fedceefc8d54101f0e7f` |
| `evidence/x-author-replies-page1.txt` | `da4188f14b16b87973d14ed9d56ee793e7b112a316f42bf9229156c5767b4ec4` |
| `evidence/x-author-replies-page2.txt` | `87f8ff2906b597919b80907b9fa16a286beeec2c4a483f30399dfdc9a0866770` |
| `evidence/x-original.txt` | `e329d90d393138c32fb8d3cab147771440c01b68db4483e5461459b9b2cf836c` |
| `exercise/upstream/archify/integrations/deepseek-harness/package.json` | `aadb56b730eea4f6641d3b7d2c7b7b886f76fb2322687068a2baad432d7fd8a8` |
| `exercise/upstream/dsh-cost-meter/LICENSE` | `ed6b8056b839e90e46fe185a75fd83a6d687f22a846f68137bfa1ef0f2b233c1` |
| `exercise/upstream/dsh-cost-meter/lib/net.js` | `842073711ecce794ac981b02be9ff529dd039fae8b1fe970533c2da0a318c502` |
| `exercise/upstream/dsh-cost-meter/lib/opendesign-prices.js` | `5a85410b29886353443c925defc33846a0f57312003dfe7d98b5ad50f2c531c3` |
| `exercise/upstream/dsh-cost-meter/lib/opendesign.js` | `657d984e34d8a8c5263e7de6f955aeb7cb8b20102f777619afa6c6e8fe04f23f` |
| `exercise/upstream/dsh-cost-meter/lib/peak-schedule.js` | `2932d18fb121ed61749ca0ef87d323c454548101bd6ea6d981a2053047644681` |
| `exercise/upstream/dsh-cost-meter/lib/price-multiplier.js` | `5e6c7d91774efd3caf18e144c863854a3787e6dcc42c4d4f5d1046d8aee57b21` |
| `exercise/upstream/dsh-cost-meter/lib/pricing.js` | `fe84d028f97c39421efbf94d80d887079eafa50f1a0eb8d358829ecab39f2c5b` |
| `exercise/upstream/dsh-cost-meter/lib/provider-prices-2026-10-15.js` | `3c89da9d0740384b6cba5e3a073ea3512c3ccabf033101f08f9c7267fc117764` |
| `exercise/upstream/dsh-cost-meter/lib/provider-prices-2026-10-28.js` | `e6d48eb2e57bf89d1b08c1c9a207e2fb7a441deabaad7d8bc308b118b9be385a` |
| `exercise/upstream/dsh-cost-meter/lib/provider-prices-2026-11-05.js` | `e22b5a84ff1f1138b02165d608b639030518461c3e0d9b0ec5a97a093f0cf839` |
| `exercise/upstream/dsh-cost-meter/lib/provider-prices.js` | `3d510bca85ed8c8afdc2323d4f1e71930d4f476c4cc7b7eeb875dd91f953eee3` |
| `exercise/upstream/dsh-cost-meter/lib/stepfun-prices.js` | `bec4f7bca5bca1d304d828095e1c532d511368c147c075b88d57fc7ebf8f1afe` |
| `exercise/upstream/dsh-cost-meter/package.json` | `a96abd4ead9f3d1d5a19634f57456a0087fd8728e85ff594b1ca6b8f24a7470d` |
| `exercise/upstream/dsh-rewind/LICENSE` | `895417849e28e3f191601428d25f184ff9fe0926558015e1c99e2e7197570a52` |
| `exercise/upstream/dsh-rewind/package.json` | `d1f90e0a69b4f5516bc6e3c6c489c95c71846ca2e094f1c983170a9ba6bccfe0` |
| `exercise/upstream/dsh-rewind/src/snapshot-format.ts` | `3eefa493cc2c82a59ac2ba074a8610384075269a9639a4ff4136417c7bb14f37` |
| `exercise/upstream/review-feng/LICENSE` | `d86c8a38b01c771a423401b51cb8316f48ef8119bdcc7c4823de9e72ac9eb15b` |
| `exercise/upstream/review-feng/package.json` | `40b0c222461f369fbca8594f5aa57a411e0458842d31a98350887336f78f86ce` |
| `exercise/upstream/review-feng/src/model-approval.mjs` | `d5621f638f273523910c36366ac687cb56eca987868cf3149f70ae9fdb7be5af` |
| `exercise/upstream/review-micheng/package.json` | `d4761de1b20006642414b78090b6e7320ec85a49544a995d768911aba32e4d10` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
