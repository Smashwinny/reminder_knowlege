# 公开归档与练习依赖说明

项目：57个插件候选 先确认身份，再量成本；原材料：马老师 第20261111批 第3项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-web-all/package.json#L162-L186
- https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-web-all/cordis.patch.yml#L1-L65
- https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/shared/host/mount-once.ts#L47-L141
- https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-ssh/src/index.ts#L139-L151
- https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-task-board/src/index.ts#L623-L637
- https://github.com/omdsh-dev/DSH-better-sidebar/blob/bd6363021dd4af8ca9df239e0c59df35b873d6b4/README.md#L40-L50
- https://github.com/omdsh-dev/DSH-better-sidebar/blob/bd6363021dd4af8ca9df239e0c59df35b873d6b4/package.json#L94-L156
- https://github.com/ranxianglei/billion-context/blob/58a879622484bce344087a69294d08d6da03be84/package.json#L2-L19
- https://github.com/ranxianglei/billion-context/blob/58a879622484bce344087a69294d08d6da03be84/LICENSE#L23-L56
- https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/LICENSE#L1-L25
- https://github.com/MichengAI/dsh-code-review/blob/89cc7166972e4d3c8bf482ee505d8d58c106fa13/package.json#L1-L35
- https://github.com/PC2005-cloud/dsh-pet/blob/c25386848f70f6e40902e4376f6e7b1e196bc326/dsh-pet/package.json#L1-L28
- https://github.com/zhu1090093659/dsh-pet/blob/ae2c9d443eda35a6439597c1787c7607e988bbed/package.json#L1-L25
- https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-ssh/package.json#L1-L63
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/archify.md#L11-L29
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/dsh_plugin_upgrade_skill.md#L12-L30
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md#L1-L25
- https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/packages/dsh-task-board/cordis.patch.yml#L1-L12

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `evidence/MichengAI/dsh-code-review/LICENSE` | `d17f227e4df5da1600391338865ce0f3055211760a36688f816941d58232d8dc` |
| `evidence/MichengAI/dsh-code-review/package.json` | `d4761de1b20006642414b78090b6e7320ec85a49544a995d768911aba32e4d10` |
| `evidence/MichengAI/dsh-codex-ui/LICENSE` | `50e6751797c50dedd75ef1b8a0d9e42f5f8472e9fbce91f34718e9f97b0c780a` |
| `evidence/MichengAI/dsh-codex-ui/package.json` | `3e040d9cf8f64dbfa884a5788e540aa4b8a7078cd3b902b099b430b9609777ca` |
| `evidence/PC2005-cloud/dsh-pet/LICENSE` | `22757dc9c895b2729a2fc684d227cadfb54d5af3dd300029926839e8c4e269ce` |
| `evidence/PC2005-cloud/dsh-pet/dsh-pet/LICENSE` | `22757dc9c895b2729a2fc684d227cadfb54d5af3dd300029926839e8c4e269ce` |
| `evidence/PC2005-cloud/dsh-pet/dsh-pet/package.json` | `7ee3edb723c2187aa73fbec67d4bc9805fa21befe9654d5f7d241c4815160ed1` |
| `evidence/catalog-leads.json` | `1bf903a3672da5092926852307f78e7aa6ef0f4bfc773b436c57d06a10fac14c` |
| `evidence/f-e-n-g-0531/dsh-code-review/LICENSE` | `d86c8a38b01c771a423401b51cb8316f48ef8119bdcc7c4823de9e72ac9eb15b` |
| `evidence/f-e-n-g-0531/dsh-code-review/package.json` | `40b0c222461f369fbca8594f5aa57a411e0458842d31a98350887336f78f86ce` |
| `evidence/omdsh-dev/DSH-better-sidebar/LICENSE` | `f4d265194e0824721af0592462a71fe750c04db3565c23c5d6c65fdee25fb4b0` |
| `evidence/omdsh-dev/DSH-better-sidebar/cordis.patch.yml` | `ec25fc02f0d283e913014bb2cbdef92a17ea360c92f2503d5104b4f8f5e7c064` |
| `evidence/omdsh-dev/DSH-better-sidebar/package.json` | `f6c766af49ccfc41fe9f4595d7d5b763eb31dc44b1ead3bffd2ab2af0bc68bb3` |
| `evidence/ranxianglei/billion-context/LICENSE` | `f27574cd3f4b0b4877da2869953945d66d76a665e7ebb9320a5e87aa76f7ab58` |
| `evidence/ranxianglei/billion-context/dsh.bundle.patch.yml` | `983bb6142e677fed80b7c2350e7acdcf549e0e191b17bbce271478e20069eeff` |
| `evidence/ranxianglei/billion-context/package.json` | `7cb29718e5963502847def13816a5e64c645b7ad9b40c0345258d6351f63eead` |
| `evidence/repo-probes.json` | `0c708cb6e5c6edd43ac8206a7adb9fd79bf3c217ea837e1330f0e670df9da92b` |
| `evidence/run-catalog.txt` | `b7dd2b4283abddc15e817d3d0e507ff44c6974a438376a7c52027d3f3b689269` |
| `evidence/run-cost.txt` | `ef80073f8450718a82a6cd522a505d9f924d73df4cf4b0b0b9d573abef5e3ee6` |
| `evidence/run-guard.txt` | `11053393a6302c8983c153767489db851356358a0cd249246380c165fc64462f` |
| `evidence/run-overlap.txt` | `e654489d0df6dab8b025d368f401418253fda2ebfa5476682e8aec29dd3fe41e` |
| `evidence/static-cost.json` | `df89e4d517b69618cb3c2f77e1d8f3371bcfb8346896c0b4968c375b11b5988b` |
| `evidence/zhu1090093659/dsh-pet/LICENSE` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| `evidence/zhu1090093659/dsh-pet/package.json` | `5ac85407360c1648622e6e8ad489dace22acd407f6b4fefb1d970889327f99ff` |
| `evidence/zhu1090093659/dsh-web/LICENSE` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| `evidence/zhu1090093659/dsh-web/package.json` | `dec739242c720ffac8a1a19ba92bf0545ba059433cc3d71fc039b570073fbfad` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-agents/package.json` | `fce9c72790a52aad8f3ec17f92a5fbaddf0c412f710c9c697217b38bed66286c` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-browser-view/package.json` | `94c96c7c112145f611af043212bec5f00041cbaa79dffd92967969a05ec5d2ce` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-diagrams/package.json` | `875d80a9606ffadee3557f13ea4014d70dfef41ac5e5c9cb0b13b3fcdfc94bb8` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-diagrams/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-i18n/package.json` | `6b622a60940df5588f3dd5d576688b5f2275ba9f1e28eef1437cfc7c158bc358` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-liangshen/package.json` | `c8145afe0481a62f62c194b31f312a7b7d4342fa74d75d647a7d844ab3a28c2e` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-liangshen/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-market/package.json` | `5aeb0d5c4e4ca6db0d022968efba1725d1d3ddfb458560b06a8530512ee3e7ef` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-market/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-message-edit/package.json` | `4a0e64ba5199f5dbc483ea875954a422e489fe03219c8d69e5b41d48ff039bbc` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-plugin-manager/package.json` | `f714660c0b8a26d627643cad3786c289a4a66c7ecbe21c51ef67c6160d797bdb` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-plugin-manager/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-remote-bridge/package.json` | `ce4e733e54238c4f62bb9dbb4ffd5f57b18dab2227cba2ea5c937a7405426df4` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-remote-bridge/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-remote-web-ui/package.json` | `6ee2be2c2140680830d39dbddcf0e47474b86e739b575ffb5d81ad171aea32fa` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-remote-web-ui/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-session-archive/package.json` | `f509eb479599dc8f35f161fc03fbc1cef347227fae8d5b49f1da42a403110e9b` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-session-archive/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-session-id/package.json` | `15fe98f7c962c133ca3212fa0849f7c92e594ed4e5998ac8ea016185450db5bb` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-skill-explorer/package.json` | `e1a130d9e0591894bccef1c464f73804a960ff856806e7144d2810b99d4f0944` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-skill-explorer/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-ssh/cordis.patch.yml` | `7b813b396a9478279f521757c42d97409507460e9c88b0b36593e64f36644440` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-ssh/package.json` | `69de459f457af79b78de68df3dad144b3a58b728525d160a6635806982d10ccf` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-ssh/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-task-board-github/package.json` | `1eb7f1644ab5e5b590fdd00df2a42dcd128aaaaefffa2f887bee6f97910384cc` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-task-board-github/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-task-board-remote/package.json` | `59d1547f834e7b8699c0daa8a99fe828fb28c0e79dccafc062803e96e0d171e7` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-task-board-team/package.json` | `ef3cb30e71b879de995be11f85d276d980522a297101aaef39d2230e960cbbfa` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-task-board/cordis.patch.yml` | `31ae050f81e39663c1e094593b3290c512da0dc5833398dd1f14e57957d5368e` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-task-board/package.json` | `2b8cfea13c9f7dc6cfbfab9c4b193ce37352083e397c717350a802f021b14af0` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-task-board/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-usage/package.json` | `f89613c021efeada1bd46e9c1ec8e7612762559e54f4c369e2640e5720994979` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-usage/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-web-all/cordis.patch.yml` | `72a01e60942c8a84ce3c14ad4ea01e2372afeac96c087503ee4654357a6fa658` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-web-all/package.json` | `c2764d9e686da1d59df35f8dd930fa6af13e3671dbfde8af5a60c24dd189eb25` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-web-settings/package.json` | `03ab572b285438fc2cb46b3e48514474b447a0f3c02ec2e819c0a10e18fb710f` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-web-settings/src/mount-once.ts` | `6f16705a6e07625f888709a1440ce525b54f3e28dc8aa61ddfe42ee6e7a68a2d` |
| `evidence/zhu1090093659/dsh-web/packages/dsh-win-bash/package.json` | `7287fad00cf031c31f6f65b27ee2b7e5f327b08e3a55c8c6c8de338671cb33f1` |
| `evidence/zhu1090093659/dsh-web/shared/host/mount-once.ts` | `eec178914396731ef99e416a809163845138c7d4c3d4fc810e32ef57383770b5` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
