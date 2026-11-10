# sources：可追溯来源清单

全部读取日为 2026-11-11（Asia/Shanghai）；带时区的时间已转换到 Asia/Shanghai。

## S1 原帖及作者链
- https://x.com/wquguru/status/2112084878842085436
- 作者回复：https://x.com/wquguru/status/2112222077671673864（「官方是第三个」）
- 作者回复：https://x.com/wquguru/status/2112118583698526573（时序/网络，未点名具体工具）
- 相关：https://x.com/P0larTas/status/2112224578596462748（贴出 espressif/qemu）
- https://x.com/MattiaFiumara/status/2112120108919525566（esp32sim 支持经典 ESP32 且核心开源）
读取：x.get_posts_by_id、x.search_posts_all（conversation_id，两页）。全文见 sources/original-post.md。配图已下载并实看：是试板界面，不是三款对照表。
发表于 2026-10-19 15:34:10（Asia/Shanghai）；清单的 2026/10/20 为收录/查看线索。

## S2 Velxio
- https://github.com/davidmonterocrespo24/velxio/tree/8a254109afe4cd17e91fb0aeaabf14ab42c46c4a
- master SHA `8a254109afe4cd17e91fb0aeaabf14ab42c46c4a`
- 提交时间 2026-11-10 11:29:12（Asia/Shanghai）
读取 README、LICENSE（AGPL-3.0）、COMMERCIAL_LICENSE.md、自建/板卡说明。未运行 Docker 或网页编辑器。读取日星标 3679。

## S3 esp32sim 与 esp-emulator
- https://github.com/mikroverk/esp32sim/tree/3d049f5c4df9efefb76406601db7a38661c328b6
- 源码 SHA `3d049f5c4df9efefb76406601db7a38661c328b6`，提交 2026-11-10 05:32:34（Asia/Shanghai）
- 运行发布包 v0.3.0（2026-10-20 13:47:04 UTC = 2026-10-20 21:47:04 Asia/Shanghai），linux-x86_64 SHA `3c18f095fbb8d6fdf49f75bdcf8eaf26717c07c034b8e38cf16bcd6aaed793a6`
- 公开 hello 固件取自该源码 SHA 的 `web/wasm/fw/public/`（C3 与经典 ESP32）。NOTICE 标明 IDF v5.5.4 等许可。
- mask ROM：https://github.com/espressif/esp-rom-elfs/releases/tag/20260528 ，发布 2026-05-28 12:35:06（Asia/Shanghai）；ELF 哈希与官方 fetch 脚本一致。
- https://github.com/espressif/esp-emulator/tree/f77b06d76ec1c8323c21d3543ec86bf426567f22
- 源码/文档 SHA `f77b06d76ec1c8323c21d3543ec86bf426567f22`，提交 2026-11-07 14:07:19（Asia/Shanghai）
- 运行发布 v1.0.0-rc2（2026-11-07 16:06:25 Asia/Shanghai）；linux x86_64 `0911981012ed40e1936b3554271348bf4a9a2ddfd106ce619cd2ad1841232290`，examples `8cacaac81980cb786083481b3b20fd3e6fe38ea225f86b98bb38b9c0d2f82674`
- issue #10：https://github.com/espressif/esp-emulator/issues/10 ，mahavirj 回复 2026-09-07 20:28:17（Asia/Shanghai）：尚未决定公布源码。
读取日星标：esp32sim 1126，esp-emulator 536。

## S4 乐鑫 QEMU 与工具链文档
- https://github.com/espressif/qemu （运行预编译，不固定一次性编译整个源码树来启动）
- 预编译：esp-develop-9.2.2-20261109，发布 2026-11-09 22:21:25（Asia/Shanghai）
- riscv32 linux SHA `afa59465495295b8aa4f804768983fa30b0bbf33d0f68a047f9caa436b9164c0`
- xtensa linux SHA `fbc3bffa9fa71192847969a627a584aabe2e86d85bed4902a096ff06c2b8a815`
- 文档：https://github.com/espressif/esp-toolchain-docs/blob/cdee381dce7b88b5207ec48c72984ca31d495dd3/qemu/esp32c3/README.md
- 文档仓库 SHA `cdee381dce7b88b5207ec48c72984ca31d495dd3`（提交 2025-09-11 15:12:09 Asia/Shanghai）
- 另保存 latest ESP-IDF C3 QEMU 指南 HTML，仅作交叉阅读。
机器类型实查：xtensa = esp32, esp32s3；riscv32 = esp32c3/c5/c6/c61/h2/h4/p4。

## 查重与风格基线
- https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747
- main SHA `a8674777e18302b8804b137212b1396cbfe5a747`
- 提交时间 2026-11-04 17:42:58（Asia/Shanghai）
已实读 vault/00-总览.md 并检索完整树。风格沿用第 1 项指南：圆角问答卡、渐变标题、青蓝橙、内联 SVG。

## 证据等级与限制
原帖=作者所见与自述测试；仓库文档=固定文本；本批串口=公开固件在本云端的实测。四层不混用。无真板，无作者私有固件，无网页交互，无独立审核。

## 本地来源指纹（SHA256）
- `davidmonterocrespo24__velxio__latest-commit.json` `c97b9df70eb986eb252bd4f19cd99c9c76bdc8ed311be68099986c9b092f8c9e`
- `davidmonterocrespo24__velxio__releases.json` `686da298decf73743c890b4b7f2a865b51f6e99747a259ee40fd5bd4b1a8a3c4`
- `esp-emulator-issue-10-comments.json` `62a9794ac2af17baef3d6467aab02e6d75857caa38276b47bce937f3a6f9d1a2`
- `esp-emulator-issue-10.json` `68b070698e3f44c451e9edf139c44e42de11ecd79739fb042c9961cc123b36dc`
- `esp-emulator-issues.json` `dad35d2e72138860a70ed613793402b5287da1032db08f38d8c849b5243f4d3d`
- `esp-emulator-tree.json` `45750f0f82e16023eeece49e267db674dfe16a9dc5f1f42e891f3d9e53981446`
- `esp-emulator__LICENSE` `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`
- `esp-emulator__README.md` `e076f9bdf076f5a70c5fd8fcf4238be3a3382c28f9cbca64b801ea1e7f1e98a4`
- `esp-emulator__docs__guides__BROWSER.md` `1abbe2af3bd8f50a6bc11a2202a139991a27f999cc3b45a09016136936f63758`
- `esp-emulator__docs__guides__CLI.md` `22c2dd1cd1040395cc4d85ac9a2c56ef7034a91ed2764bbd8579e5b02dbf0087`
- `esp-emulator__docs__guides__FLASHING.md` `9918d7064ce8ad63a71756b494ad923cdc07ab15a0031dc9e8c27bf4d4df4abe`
- `esp-emulator__docs__guides__NETWORKING.md` `6901e3a9b823f0d27298f7a7f64f6e0ea22fd0e471c8cb51ac1983e1b7270457`
- `esp-emulator__docs__guides__PARTS.md` `277cb9ed159a7fbab3913d4d9209f66e467e981fd57647f473f0a31a5894fe0f`
- `esp-emulator__examples__boards__button__README.md` `17b0909667bceee688d13301bf7669c7762521166a0d88250ecd14a38e673af1`
- `esp-emulator__test_apps__README.md` `1e25b2b5aea36f95ed2c6741709584257371d60c19830747b44035af90c0ccd6`
- `esp-toolchain-docs-commit.json` `6a621560f4ee3ef40ff83fcc28f96efe00003b7e67eb0b9bc850befd0c9583c5`
- `esp-toolchain-docs-qemu-list.json` `a55aa243293aa6a10fd6c21e274b00cf0481d182301f3b39bec83258f695c06b`
- `esp-toolchain-docs__qemu__README.md` `f636f5d9796f49376005d2fe8959579f2b922fa6050f1884b40acaeff52aa1f0`
- `esp-toolchain-docs__qemu__esp32__README.md` `735f24f0413edccb5497ca3fcfe4c7d9a8636f4f40a7f2dbc87de18ce5aedeb7`
- `esp-toolchain-docs__qemu__esp32c3__README.md` `a94db6e32896874da34503ef974240ace9f222609cb50f43efd738c6259b2022`
- `esp-toolchain-docs__qemu__esp32s3__README.md` `f7b08a26ed7a7273b20232bcd58f3da16fb8cb7c7bd8ecb2502c98f49ad5e6d7`
- `esp32sim-tree.json` `bf6dab82faff0302d1ab6558465201e011a7db434429b1676b613a1394457603`
- `esp32sim__LICENSE` `9de2fd8155bb09da4f50be6e5eb0688bfbcc4808e9a94f7713145a321d52a396`
- `esp32sim__README.md` `554e474570650dd44aec9e7da4402575ea88cf703118e131fdacd2c65bed8166`
- `esp32sim__docs__boards.md` `00ad25148ef5a31bcbd1556eade8c61f5f8c6f72ed20035f95b1dc0380913561`
- `esp32sim__docs__cli.md` `bab0be790477de51421e6d86ef3496774132c2f9bc3bd20ea551fe3fe57de802`
- `esp32sim__docs__getting-started.md` `8bd2de2b7cb71c1912ba61d515d6fd24cb0a14a383698e402fb5eb1d679828bb`
- `esp32sim__docs__peripherals.md` `44e799486ba530160ed008da81376eee7d981e73f0ab8540c2da65004e7ec58b`
- `esp32sim__docs__quick-start.md` `db1c703da21d7de0cc135056678e58568f83b3627c54797e0300b5e8d91a0c43`
- `espressif__esp-emulator__latest-commit.json` `1facab1b0f41378576c716e819079a47d9de294b2dcc965a82e03e0794996a4b`
- `espressif__esp-emulator__releases.json` `581c5875e11e416b74cc8ed7431f931d027d42f26c4f0fd4012a14f507074edd`
- `espressif__qemu__latest-commit.json` `85db1087d63b2ef539614082f5db0ef4558ba93e72ee09638fc93de1ee6fbe74`
- `espressif__qemu__releases.json` `cfdd97c9987762e6df51272fb59c58c0081aa2e218ce144d75f3b5f56e21fbd6`
- `firmware-sha256.txt` `fce0d154d6afd28dea59bf1855a3d50827d70486a6d10f5e19fb026ec0d2c47d`
- `idf-qemu-emulation.html` `2a96176ff06c0e2f975c299df4a58ad47061b2420cf28c9240cdbb512885af14`
- `idf-qemu-esp32.html` `64c785b95b91673a0d3e3b6ce5bc9a3009a78d9dbe6228cfaa8d0a6cee719c35`
- `idf-qemu-esp32c3.html` `449013a9fde502a0cd2745823b4a43217c940aa6ccbe7ec2e6038f7f36d3d645`
- `mikroverk__esp32sim__latest-commit.json` `a6e7cd5724ac61ae5c0a61b8067c902467c76ccbc30cd1af244ad99f54912406`
- `mikroverk__esp32sim__releases.json` `d39f14c288fd4005f8ea4adaf1b50033e37b0b6f9fd3ffdfe4ca1f15d2e05564`
- `original-post-image.jpg` `885e3527cdc9cef20289766cdfe85e3a09e30129a711e04086f80bf190c64881`
- `original-post.md` `c43dff7175c70879921882c541bced6b031ec3c921e7fae7a2b2fb59d8615f92`
- `qemu-wiki-Home.md` `6c01b41bd15cf968ee75254534fe20ad707ed59b2b73c95230cb3066bf9937f2`
- `qemu-wiki.html` `78932dd3056c97ae897f70d202625d5bb0aa03d2d5f456ca17b9da2b88fe6221`
- `qemu__COPYING` `6f04ae8364d0079a192b14635f4b1da294ce18724c034c39a6a41d1b09df6100`
- `qemu__LICENSE` `139c64b7a9ae62858ff969aae622ecfcf4f1519655bd92d2e70a1a2fb615690e`
- `qemu__README.rst` `d9e0384f45d047137f74f38b32dec1f31488fdbe2557820c8934e1fbc8fc2efd`
- `reminder_knowlege-commit.json` `254c82c1446d0c69bdce83a47abf5595ef9533f6916111f24eb3be80db5aee47`
- `reminder_knowlege-tree.json` `60f1bcda8e3be426f7e41d5e8fb59efaa236301754bf47b459aac8a462ba50c2`
- `reminder_knowlege__vault__00-总览.md` `a8779f945f617faa941692db5f1bc684228082930fbe4703b8e8eb8b1b3a8580`
- `run-logs/esp-emu-button-control.txt` `8caf24e950babceba7ad2ed54a489eaeda9214f68635249213f014f974e02d4f`
- `run-logs/esp-emu-button-press.txt` `161621fc4f2820eb635f868aa2594b11be0e1efa9eb3e6d490bb88def2021de1`
- `run-logs/esp-emu-button-ready.txt` `ccce83f273e51920e8c4f0bb2202fdd2ba535b68238f72f8f30f63d28b5368ea`
- `run-logs/esp-emu-c3-hello.txt` `abd756df0cf24eecd0c232edf534d7a6e14cf6f0f24bf87136a28093c95f9d86`
- `run-logs/esp-emu-reject-classic.txt` `3f77c41da54c516515b1c9f446a83a762d7743f5e9b07f47b80cd4482765ad89`
- `run-logs/esp32sim-c3-hello.txt` `8bd20abe6fdb93c865011faef2ad5d16cde43bbc723cf45736bc201544048df9`
- `run-logs/esp32sim-classic-hello.txt` `bdd28d910ae7298ab82255e8ebcb95335b4c8cbf1e284c4bde64f8848fe741e0`
- `run-logs/qemu-c3-button-4mb.txt` `3bc19d427dfbbb41e39851d19de03da2fa7e95bfeb2f1894824f3e750191098b`
- `run-logs/qemu-c3-hello.txt` `38fad04b1228cfa8a2982554298220b9c3ad288d7361a9e4008a0d85653789ad`
- `run-logs/qemu-c3-unpadded.txt` `4738934d1c024e2edc615a5afc642da292d1c4e4477059f5f32fa2fda5f8c0d7`
- `run-logs/qemu-classic-hello.txt` `c51d4a817c501932c0841fc8eacfd86ad927854b33e0a288f468c0d2ffcb9f02`
- `velxio-tree.json` `333ec3135896ccd1f02c449178f909f66eb5db89e98c48daa816eed549834bb7`
- `velxio__COMMERCIAL_LICENSE.md` `bf7169c5e94813ed1b70820f868d43dcd334b86af8c489f334581e01c486ab84`
- `velxio__LICENSE` `43cadc830e2c90b4d20e938022168b1c2c51a14e32a3a5dccf4814e28e5fd236`
- `velxio__README.md` `fcb356eb24096de8d1519902e5ddc359848f84953bb8cb209aaed152adecca7e`
- `velxio__docs__ESP32_EMULATION.md` `20ca796d68814571d5edd3b30a11b10633aa9f7e63eb848229efc90a5082203d`
- `velxio__docs__getting-started.md` `ee5098a49e30a07740124af741316819957ca217ff07247a56feca2004b37311`
- `velxio__docs__wiki__circuit-emulation-esp32-qemu.md` `0e6194112f47854289c72a5f109a9ea3a96a0e7b9724b062632c13fdd46bf690`
