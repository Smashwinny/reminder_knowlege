# 公开归档与练习依赖说明

项目：Pi-Purge 提示词“组合器”，不是权限开关；原材料：马老师 第20261111批 第1项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/ZiChuanLan/pi-purge/blob/efb87cc06b0882ba90bd90e21413d1f7e1a65cbb/extensions/pi-purge.ts#L47-L164
- https://github.com/ZiChuanLan/pi-purge/blob/efb87cc06b0882ba90bd90e21413d1f7e1a65cbb/extensions/pi-purge.ts#L166-L257
- https://github.com/ZiChuanLan/pi-purge/blob/efb87cc06b0882ba90bd90e21413d1f7e1a65cbb/extensions/pi-purge.ts#L18-L45
- https://github.com/ZiChuanLan/pi-purge/blob/efb87cc06b0882ba90bd90e21413d1f7e1a65cbb/package.json#L1-L54
- https://github.com/ZiChuanLan/pi-purge/blob/ffafeb940339d59fc6af4a05dc754019cef3a1ac/extensions/pi-purge.ts#L248-L359
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/extensions/types.ts#L698-L709
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/extensions/runner.ts#L1081-L1145
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/system-prompt.ts#L121-L163
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/src/core/system-prompt.ts#L150-L209
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/src/core/extensions/runner.ts#L1434-L1484
- https://github.com/ZiChuanLan/pi-purge/blob/efb87cc06b0882ba90bd90e21413d1f7e1a65cbb/README.zh-CN.md#L37-L98
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md#L1-L25
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/接缝与桩实现StubSeam.md#L8-L24
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/提示词权威边界.md#L8-L19
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/agent-kernel.md#L8-L18
- https://github.com/ZiChuanLan/pi-purge/blob/efb87cc06b0882ba90bd90e21413d1f7e1a65cbb/test/pi-purge.test.mjs#L71-L162
- https://github.com/ZiChuanLan/pi-purge/blob/efb87cc06b0882ba90bd90e21413d1f7e1a65cbb/test/pi-purge-env-source.test.mjs#L1-L71
- https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/src/core/agent-session.ts#L1232-L1261

历史 pi-purge 的 persona 在原实验中替换为无害常量。需要复现时使用原归档已处理的版本及其指纹，不把网上的另一版本直接替换进实验。

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `evidence/dsh-read-failure.txt` | `0738e1d53e03cdde4e379859b024fb665340ccc62ac4ed215101772e5d81327b` |
| `evidence/final-page-01.png` | `db487677b66748242bcb4b30e1df83713ce948874e91a9934b9bb302c97ca830` |
| `evidence/final-page-02.png` | `e1c966380a59d9517b1283eec37eb9437209da34c9c03193285dd85f7a519afd` |
| `evidence/final-page-03.png` | `945b88a756b2fd9d657667efaef60a6f9aa04b2c826e1b24fe010132d7423cb9` |
| `evidence/final-page-04.png` | `9422167ba8d855c96a250c15290367eb246110c50717c582a41ca5c45d0dc9a9` |
| `evidence/final-page-05.png` | `2e3812e863a378c0825824639556ab1d493203a6593cad1e192abc5cbcbbb6d6` |
| `evidence/final-page-06.png` | `3740ed494262d1966ea75ff09536cf117ac2dd2f8332b7259c632b1e51c8c2e9` |
| `evidence/final-page-07.png` | `68c848dc976c557691ffa00cfe1dc0743d0b38b97528fe57cada87bd6706decd` |
| `evidence/final-page-08.png` | `53cc7fee0668d16d40941cbd72229cdc349f5e9a8ff127b44c99cb4bdd2956f9` |
| `evidence/final-page-09.png` | `735323c7b731a89da8f11899fac645f0a0e7cb5530b914b655d1f7d30d323ef8` |
| `evidence/final-page-10.png` | `2d66634ebabc5b8f764203e09c3c5b96a0dad663003d29d6ac41325e39da7597` |
| `evidence/pdf-print.log` | `f1a83de4732e89ace19fa80f30f48438988563d88097aeb205f9beaa7cb8f7f6` |
| `evidence/pdf-text.txt` | `122c0ae5e31cfdf7509ec4345f8da1b0fb362cd1af5cda85a2ba12d0094e8088` |
| `evidence/pi-0842/LICENSE` | `0457f5bcec3b3b211605dfb5d1a49042fd638f3686a410fe099c24a25af13c48` |
| `evidence/pi-0842/packages/coding-agent/package.json` | `820f4adc6d61f2cefbc29ce17e9dfd9aa482248d54be5d0dfa2a868ca000c7b0` |
| `evidence/pi-0842/packages/coding-agent/src/core/agent-session.ts` | `c83f43205f0b0ef014a383b4969f2bce112a8b4280f6e9f889eeae0d7e02ec2e` |
| `evidence/pi-0842/packages/coding-agent/src/core/extensions/runner.ts` | `071a6609afa6aeffa74e485b66474076bd7d70c14503804591ce79739100756c` |
| `evidence/pi-0842/packages/coding-agent/src/core/extensions/types.ts` | `731ef884151310fdb5216845be2a0d4a4b2acd0e985529c5cbbc7528405de821` |
| `evidence/pi-0842/packages/coding-agent/src/core/system-prompt.ts` | `e8b06a0f093c83fd7660a3eae331d5f8ee917702763b1e5044f5c5306e9c1d00` |
| `evidence/pi-current/packages/coding-agent/package.json` | `18b422b7d80f2caa2551d253c0a8409e1caa54b954bfb7d18252e507bb8a0318` |
| `evidence/pi-current/packages/coding-agent/src/core/agent-session.ts` | `dea73f4df16b15c927a4cb6b35ad7a3f9738232acb2d48473f0497f360fda6fe` |
| `evidence/pi-current/packages/coding-agent/src/core/extensions/runner.ts` | `6e305286a99c0364f58dfc89008b5d858363b3f38eb8c93686c3de5bd6b42475` |
| `evidence/pi-current/packages/coding-agent/src/core/extensions/types.ts` | `174549078f95dddd70e656c4eb54f73e0f75782af6a971cf6dc2ee622fa0917c` |
| `evidence/pi-current/packages/coding-agent/src/core/system-prompt.ts` | `eef891d637974d09a6611d33e52d66d5f2a93d6e9512259ba45f593c42143617` |
| `evidence/pi-latest/LICENSE` | `0457f5bcec3b3b211605dfb5d1a49042fd638f3686a410fe099c24a25af13c48` |
| `evidence/pi-latest/packages/coding-agent/package.json` | `18b422b7d80f2caa2551d253c0a8409e1caa54b954bfb7d18252e507bb8a0318` |
| `evidence/pi-latest/packages/coding-agent/src/core/agent-session.ts` | `dea73f4df16b15c927a4cb6b35ad7a3f9738232acb2d48473f0497f360fda6fe` |
| `evidence/pi-latest/packages/coding-agent/src/core/extensions/runner.ts` | `6e305286a99c0364f58dfc89008b5d858363b3f38eb8c93686c3de5bd6b42475` |
| `evidence/pi-latest/packages/coding-agent/src/core/extensions/types.ts` | `174549078f95dddd70e656c4eb54f73e0f75782af6a971cf6dc2ee622fa0917c` |
| `evidence/pi-latest/packages/coding-agent/src/core/system-prompt.ts` | `eef891d637974d09a6611d33e52d66d5f2a93d6e9512259ba45f593c42143617` |
| `evidence/pi-main.json` | `82c50f29ba9b7898af38f35e006e78693ec420fb4adb80d359c28d8860f2e344` |
| `evidence/pinned-redaction.json` | `56ae4e081accb0537082fea698a8a92ed31b3cc0dcf46c0c32c130ebf9784494` |
| `evidence/purge-current-tree.json` | `94aabaa7c248f99b9fd574d69158c252cfcecc15426a693c05b0fba6ce275d7d` |
| `evidence/purge-current/LICENSE` | `b32f2a249e149a652cf298e65d30e30067ac0c32ff8088b130394878fbcd220f` |
| `evidence/purge-current/README.ja.md` | `8a5ce0bdb5cb810bdc8d2d00eb3aa0855bf49952f911a3153bdc48ce8fbe889b` |
| `evidence/purge-current/README.md` | `43f0f8bbeda08344ead0164f074714a305faf388ed22edc6b26fab1375376669` |
| `evidence/purge-current/README.zh-CN.md` | `14cfd2d869353020c75dfff6558d486d93235a3b2f8537adcbcd3c280ce466be` |
| `evidence/purge-current/extensions/pi-purge.ts` | `29c4ed6e83ef35c4b007c5a98c916355955a6c81b03ecc301a26a544b25858a9` |
| `evidence/purge-current/package.json` | `f0362f4a12ddb107a0d78443653040dfb4966b0d9a713ead65dbda88927f17c7` |
| `evidence/purge-current/test/pi-purge-env-source.test.mjs` | `a01d583347a382dcde954e97d307533da005d360f5aef2274dbeeb57fef8400c` |
| `evidence/purge-current/test/pi-purge.test.mjs` | `8dc841e6854a4bbc98a025256f7a4517d637c38c80eba15dfe01ed107c5d2835` |
| `evidence/purge-main.json` | `10a86f11fd5a33f982226667c1e3f70fb52a1b2fea36b7911b1f492956b25b08` |
| `evidence/purge-pinned.json` | `37219eaac299829cb5008014664c4de60d414de75a5e6406dc3795bda9b085ea` |
| `evidence/purge-post-tree.json` | `114c69eafffbbd61a3ac8ca51c449de4a03ee4dfedf88c5ccfcb9c55eaeea2ec` |
| `evidence/purge-post/LICENSE` | `b32f2a249e149a652cf298e65d30e30067ac0c32ff8088b130394878fbcd220f` |
| `evidence/purge-post/README.md.sha256` | `a9e449446a83f7fd1b87fbd62a931f4cd083e55fff858ad3bbed6cc38c101c12` |
| `evidence/purge-post/README.zh-CN.md.sha256` | `f9d9b3cdb3e238cd2105003e016837702cf12a0df3b98065ca6b41f83f44353e` |
| `evidence/purge-post/extensions/pi-purge.ts` | `5bb815a368a262c43c6f1444ea273d4caae988deaaaa13fd8e7f2a7de2141183` |
| `evidence/purge-post/package.json` | `1baac591a2fe1406c0eeccccdf6417a70ac41e40039373d46c9d205932af435b` |
| `evidence/purge-post/test/pi-purge.test.mjs.sha256` | `400dbd698a7a226d802017ff96deed3b914e0079db332128f44bf771c542c37d` |
| `evidence/run-compat.txt` | `97b9da15bc4e849f7e3a6827437840b55f8ca49e6b0363ea60600da87be2fddb` |
| `evidence/run-env.txt` | `c9b8ba1151f5225809b7b358a4a822d16be2b290983f4812456d80c6865ba0c0` |
| `evidence/run-lifecycle.txt` | `cd326572baab2622d1226c7cb318a20343aa45afc81bbd98a964ced1aa4b9030` |
| `evidence/run-modes.txt` | `434ea218a4e49ec8e3dda6e970089a4924fad79f1f4049a8e8d1eff383f97d01` |
| `evidence/run-upstream.txt` | `db66de4c6eaa24d01c0e324a0ad9a8e94ab5712abfaf49525ec3c2427212c4fd` |
| `evidence/vault-main.json` | `6fcd0dcf23a44f2d4d4b815ae6af2e0f12df84a79a8dc2272a07f6684f1cf19f` |
| `evidence/vault-tree.json` | `078ab5a69beab6a31bb3b0d3fd6509fa2dc88995834e2c65fe3e3d96b0c009af` |
| `evidence/vault/agent-kernel/agent_kernel_guide.html` | `c4d9ddda750c81f94ed77dabdcd853cd9c7a3779e3ad43094a067c1d1b12952d` |
| `evidence/vault/vault/00-总览.md` | `a8779f945f617faa941692db5f1bc684228082930fbe4703b8e8eb8b1b3a8580` |
| `evidence/vault/vault/概念/接缝与桩实现StubSeam.md` | `9bc16d51dbfa8fa1a84fd43d2cdcdbf81c9ae2d41272007df08f610a79ffdf58` |
| `evidence/vault/vault/概念/提示词权威边界.md` | `f51e1a1b69e257f494a76b6ae0bab8e110f64913c402ca28e554ab3012ba5e16` |
| `evidence/vault/vault/概念/沙箱与审批正交.md` | `a9e65c39d85a821884b50e6e2a4a1a1944cd18c4fd7961cb8a6c9f65cd645a41` |
| `evidence/vault/vault/项目笔记/agent-kernel.md` | `825d06b3df7fa95605e8743864b9ba9ef7b85a1ca053f8f40aa64ecfb6bf6da4` |
| `evidence/x-original.txt` | `489b8c5a1229aa09dbb0e5985eec833aac1ed4fdb06ff2edf88f0be8b88f8862` |
| `evidence/x-replies-page2.txt` | `69b96d56a871bc254746f849137a8fb64176f4d7e97e6778cdb7d5dc86a28ac4` |
| `evidence/x-replies.txt` | `aa029778deec241aefd6e4babb8c1e4c0a1c2f0e39f71eaa823619afaedd2190` |
| `evidence/zip-smoke.txt` | `6e80887c0c132dc9fe77c3aa2c327fdaa7c872b46211eff2469bd9db520cc7c1` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
