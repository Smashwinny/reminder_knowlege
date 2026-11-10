# sources：可追溯来源清单

全部读取日为 2026-11-11（Asia/Shanghai）。带时区的源时间戳已换算到 Asia/Shanghai。清单上的“久未查看 · 2026/10/20 23:07:11”是收录线索，不是发表时间。

## S1 原帖及作者链
- https://x.com/0xNathanWalk/status/2112539228278239708
- 同对话作者回复：https://x.com/0xNathanWalk/status/2112559706594287843 、2112565630587265535、2112729030135042326、2113913843265270093
- 后续拓扑线索：https://x.com/0xNathanWalk/status/2115089119001170072 、2115837426581348694、2114965391399432317、2112380128751964562
读取：x.get_posts_by_id，x.search_posts_all（conversation_id，第二页 0 条）。全文见 sources/original-post.md（含 note_tweet）。主帖无引用帖。发表于 2026-10-20 21:39:35（Asia/Shanghai）。附件视频已下载并抽帧，见 original-post-video-720p.mp4 与 video-frames/。

## S2 RFC1918
- https://www.rfc-editor.org/rfc/rfc1918.txt
- Address Allocation for Private Internets，1996-02。实读 §3 三段保留块。

## S3 RFC2131
- https://www.rfc-editor.org/rfc/rfc2131.txt
- Dynamic Host Configuration Protocol，1997-03。实读表 2 报文类型与图 3 新地址分配时序（DISCOVER/OFFER/REQUEST/ACK）。

## S4 RFC6598
- https://www.rfc-editor.org/rfc/rfc6598.txt
- IANA-Reserved IPv4 Prefix for Shared Address Space，2012-04。规定 100.64.0.0/10，并写明有别于 RFC1918。

## S5 Tailscale 100.x 文档
- https://tailscale.com/kb/1015/100.x-addresses
- 页面标题 “What are these 100.x.y.z addresses?”，标注 Last validated Jan 12, 2026。说明地址来自 RFC6598，范围 100.64.0.0/10，换网络保持不变。

## S6 Tailscale 工作原理
- https://tailscale.com/blog/how-tailscale-works
- Avery Pennarun，2020-03-20。数据面为 WireGuard（明确提到 userspace Go / wireguard-go），控制面做密钥与端点协调；NAT 穿越失败时使用 DERP。

## S7 ESP-IDF 网络
- 版本标签 v6.1，注释对象指向 commit `fff9895c82d744c7237be8847347bdd1b07c6643`，标签时间 2026-08-25 11:21:22（Asia/Shanghai）。
- https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32/api-reference/network/esp_netif.html
- https://raw.githubusercontent.com/espressif/esp-idf/v6.1/components/esp_netif/include/esp_netif.h
- https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32/api-guides/lwip.html （页面显示 ESP-IDF Programming Guide v6.1）
- 在线 wifi-driver HTML 多次 TLS 失败或仅有跳转页；GitHub 上 `docs/en/api-guides/wifi-driver/index.rst` 只是目录。阅读范围以 ESP-NETIF 文档与头文件中的 DHCP 客户端/服务器 API 为准，不宣称读完全部 Wi-Fi 驱动章节。

## S8 Tailscale 官方嵌入式二进制与 ESP32 issue
- https://tailscale.com/docs/how-to/set-up-small-tailscale （Last validated Jan 5, 2026）
- https://github.com/tailscale/tailscale/issues/5220 （开放 issue，至页面讨论 2026-06 仍非官方 ESP32 库）
- 仓库 tip 快照：https://github.com/tailscale/tailscale/commit/05930082daf8ebacea423346d0e0393d4eba2a0b ，提交 2026-11-11 00:56:08（Asia/Shanghai）。仅作读取当日 main 指针，论证不依赖该笔构建改动。

## S9 社区 ESP32 客户端（对照，非作者项目）
- https://github.com/CamM2325/microlink/tree/216da3300f0493b0860247d43f7af5ce29df63a5
- 提交 2026-03-17 21:06:57（Asia/Shanghai）。README 称静态 SRAM 约 85–116 KB，建议 ESP32-S3 + PSRAM。不是官方客户端，也没有作者署名。

## S10 M5Stack StopWatch 官方文档
- https://docs.m5stack.com/en/core/StopWatch
- https://docs.m5stack.com/zh_CN/core/StopWatch
- 官方规格：ESP32-S3R8，16 MB Flash，8 MB PSRAM，1.75 英寸圆形 AMOLED。出厂固件为表盘/秒表/徽章等，不是本帖眨眼固件。作者混用 Stopclock/StopWatch 名称。

## S11 wireguard-go（本批实际编译运行）
- https://github.com/WireGuard/wireguard-go/tree/b3bc704ef0ee21a36298601a9e1e5ff90377ac52
- 提交 2026-10-25 06:09:52（Asia/Shanghai；源字段 2026-10-25 00:09:52 +0200）。许可证见 wireguard-go-LICENSE.txt。
- 协议论文 https://www.wireguard.com/papers/wireguard.pdf 已落盘，本批不宣称逐节复核全文。

## 查重基准
- https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747
- 提交 2026-11-04 17:42:58（Asia/Shanghai）。已读 vault/00-总览.md 并检索树中网络相关路径。

## 证据等级
原帖与作者回复 = 作者陈述；RFC 与官方文档 = 规范/产品说明；源码与头文件 = 固定文本；本批输出 = 云端教学实验。四层不混用。无 ESP32 实机，无 Tailscale 登录，无独立审核。

## 本地来源指纹（SHA256）

- `esp-idf-commit.json`  19152  `9263f141c6e1eb49830371c68d3493289498d3b78a7708443e69bd549b6992b4`
- `esp-idf-esp_netif.h`  40874  `e051eee1375542121b0170496ee3e9ca9f1a17b17b325c57a9d2680f45fb3e68`
- `esp-idf-lwip.html`  98656  `ede08952fa76be2f21caad56d54b911eaefd088510729e5f45f855fc7f162551`
- `esp-idf-lwip.txt`  32992  `87dda128984b0325834caa470ef249eb88cb2793a9a1ea5edbe590047c7a3b50`
- `esp-idf-netif-v6.1.html`  44036  `137d336bab85e4ef78a496f5e13f11af933dc14d3f0caa90b0c30a1fe3b42a0f`
- `esp-idf-netif-v6.1.txt`  15425  `d670900727bd752f992c3f1e984a134cc495cd8ce278606e325f56edf0679304`
- `esp-idf-netif.html`  43364  `452c16ee2666aabf82f086d690ada959f39fda36ea00f46ad059db3d0e5efd6c`
- `esp-idf-netif.txt`  15332  `3720418af71eb9a5ce82f26c07312d307bc081ccc8acd71d66df2f583631563b`
- `esp-idf-v6.1-tagobj.json`  1318  `cc8638af00f58db7f61cfccc5c4826151fa3ba66f35ce58d2c7603ef5c9c6ae8`
- `esp-idf-v6.1.json`  329  `92350afb55fd037981230efe11d92a421052bae1f6910cc1146a014a743d434f`
- `esp-idf-wifi-driver-index.rst`  263  `38d099d5f8d6b9465aacae10beabe932346715ea3dc7876ce5e93c6a3c263117`
- `esp-idf-wifi-index.html`  276  `5a2b5c1f80d0977cf5641ce899c9e77bd0bc8a340be6d3390af36a8c60cbd755`
- `esp-idf-wifi.html`  276  `5a2b5c1f80d0977cf5641ce899c9e77bd0bc8a340be6d3390af36a8c60cbd755`
- `m5stack-stopwatch-zh.html`  156061  `61882fd865576c57eade57665bcfcb94a156c06c773f7b3193d0f0386c3de9ce`
- `m5stack-stopwatch.html`  156946  `101b3f35aa01c12ed4c3458b1b9b3f65aad8b531a1a2b968090e9b28f1d2dc10`
- `m5stack-stopwatch.txt`  10445  `d90a702723bfe92de8e8ec8e6015fd5c1945fa753e3f887000cadfdb57db675b`
- `microlink-README.md`  33635  `12cc01f7c17d94f827be3c574bad2797901a0660dc5e1aa96dd8dce764b22907`
- `microlink-commit.json`  41543  `4384aad33595e363bdefefe72b5c9d2321b2ab7a967e7417a3e54145024e8f98`
- `original-post-video-720p.mp4`  678562  `69633581f420794712c8f3baee46d7b887daa73775a3eaa52bff27653a7b01ed`
- `original-post.md`  7427  `3655e291481c069d35bf8ca13fb57c7307b12045bd6e6df9e5d5c7e9a8f4665e`
- `reminder_knowlege-commit.json`  95555  `254c82c1446d0c69bdce83a47abf5595ef9533f6916111f24eb3be80db5aee47`
- `reminder_knowlege-tree.json`  1148450  `547c0f342b0fe7ce32981027c56d5a66b3ec5a8b5e35f5f539df815bd03d2f04`
- `reminder_knowlege__vault__00-总览.md`  139753  `a8779f945f617faa941692db5f1bc684228082930fbe4703b8e8eb8b1b3a8580`
- `rfc1918.txt`  22271  `56c43465298772bc4d899923f1785b7b7bf8dd2c9f2f9a53422800ddc5cf9337`
- `rfc2131.txt`  113738  `a043b705785b81762505ded4cf71d61392b2b1da2b4ce1e32c13bc984de5f4a5`
- `rfc4632.txt`  66944  `13694a39f586eb2054407780edccdf7c39332e57f067c8008bba4326bfc24fa9`
- `rfc6598.txt`  22055  `b04d16c5c98b89324d35dc6dc783eface0bedf94c14c9e289b646d39ea55c4c0`
- `tailscale-100x.html`  222137  `d5c44776bc0ec0eda09da295229b71cdca55bba803fd9cbd0f4258d641ffd3e6`
- `tailscale-100x.txt`  2034  `77851cfc38881a8cdbda666deb9d4f22e16e2be8c40250e8666a6f14dcf56979`
- `tailscale-blog-how-nat-traversal-works.html`  313663  `23691c3f9146bdcd6da49c20295021d7f2d4c1f170d51ff11342bc56ad2d2cf1`
- `tailscale-commit.json`  6091  `36e5ecf64d1bedca536a22478d57105d367539ba701de93bb53b35a182ff2b39`
- `tailscale-derp-kb.html`  247941  `17a4e7f8577ecc10a6c4b424b3107ef482338d0048bcea0b923f2c323ed798ef`
- `tailscale-how-it-works.html`  198579  `4a001eb47c1fe634ea151b929a036e4f95a49be061a180020d8c64479d43193a`
- `tailscale-how-it-works.txt`  21427  `45e226a4e8eeef55012989f146735ab451af95bee8a42bf25d387b67d4d61a19`
- `tailscale-kb-1082-firewall-ports.html`  247941  `17a4e7f8577ecc10a6c4b424b3107ef482338d0048bcea0b923f2c323ed798ef`
- `tailscale-kb-1232-derp-servers.html`  244750  `8ae6b0a74a5cf14fa55eb8d11ca5f397610bb5cabad14f14f373bc59c54c1ad8`
- `tailscale-small-binary.html`  248330  `f48c53e09b45995f66312591e2a0792dfae4d42cb2563c8e60993bc8b8fe6b61`
- `tailscale-tailnet.html`  231819  `0fcb4a6956fd376bcf95ad46d22650cabe5db67a0bfc2998cc56f491380a8c1b`
- `video-frames/face_001.jpg`  3494  `29935c2a499226ba5a5eb1c63fed478903947020ba1eaf9be46fbf29f8f5826c`
- `video-frames/face_002.jpg`  4423  `80038d0d3688da5081c78aaf60af721e636d7ae7d32bbac6ecaf6a766f232ce4`
- `video-frames/face_003.jpg`  4363  `a4529185db9f98397c26ceb11fc5aa817ade12b382e262688a8d4c250ac12ab5`
- `video-frames/face_004.jpg`  4413  `957dd879a16e6565fcd078722aabd92f688b424846660fccdc3b5b918965925c`
- `video-frames/face_005.jpg`  4151  `c6d7af5b2b7764613114dd33ad1978f21e8aee4ea7b83396a5e2ec5cf87d35e6`
- `video-frames/face_006.jpg`  4260  `290278139d7b8b683d4de51ce831f76ff3bdfda11fc33171691c29f1c319df42`
- `video-frames/face_007.jpg`  4285  `9a9399c9c319ed6ba3a55092f7b1a62b35b4573a4450e23e53337a0386b098f3`
- `video-frames/face_008.jpg`  4186  `4eaf7a715ed91fc37e425c9018757a59d19a9e00cf3b0a0b9b255071e3c8afd9`
- `video-frames/face_009.jpg`  4325  `3b0fa8b4153b839d3217c118fc22cb4ef39682282753f06df516cd6c9d5e3b82`
- `video-frames/face_010.jpg`  4054  `2714df8ca71240a7baa0375fa6feb6d1dd2ec008914112f56621ac00b59490d2`
- `video-frames/face_011.jpg`  4185  `f85c626ba90d346a7325c200a251bd6e9d040b8b70b799cf2399381a22039fea`
- `video-frames/face_012.jpg`  4172  `2374111685dc232a294a456c7a08de3a8200eeab1918cbe9afc5fa0697866464`
- `video-frames/face_013.jpg`  4070  `62340a28cf9ec8d7f883a872a5f85ede6fbda1b5f2a87c341a563028b097915d`
- `video-frames/face_014.jpg`  4146  `154fefa8168c99be3a6208541b6010fef11fd9b27d2a3726b6d72d0e255bee89`
- `video-frames/face_015.jpg`  4149  `72af3f7129d5636e2d615d108620c99871c3122ff33dff87758e4acaf5d092a7`
- `video-frames/face_016.jpg`  4431  `a959b75700268fbe1bbf508e9b2391a210cb1a8081f45261b0d84e50342f6c27`
- `video-frames/face_017.jpg`  4449  `a81bfb82e838f346d95e47d4b9f722fac1767c6f9ea6d0dc671171ca34bbe24c`
- `video-frames/face_018.jpg`  4341  `afd36660b6fe9a3adea3919833189500e6d1cce0a2f91b9b8ef52fdab23ac9c8`
- `video-frames/face_019.jpg`  4420  `6c1368b96e887a9a0a4b0f05147976020917e10b5a0bd970351f56a65405fc4f`
- `video-frames/face_020.jpg`  4329  `4396e92985077142bf86cbaf141eed7fecbe089bd4a4dfb52b7c2ecac73a4749`
- `video-frames/face_021.jpg`  4454  `959a2c07b73e163e85b92e182c0e1da7ec102e36aaae70dd2818ecdb0e836ba1`
- `video-frames/face_022.jpg`  4366  `b148160da78f5fb9d712fc53416e56c58717b0c8f9e0f288bac8a0d6519047fe`
- `video-frames/face_023.jpg`  4327  `6f1e6a8969b2cad7dd8485aedf28895a7917ef47463815414136f7290e76dff2`
- `video-frames/face_024.jpg`  4477  `18a2e0801cd63f1ae655e478a754668bd9de147c015f6ab097e6c870b692d536`
- `video-frames/face_025.jpg`  4302  `002a4f01250cf6b1e1672531c852fcd91d7501ddf3c1ed89c30818fc68f33b25`
- `video-frames/face_026.jpg`  4224  `5ea22e33273772dbbd61514afd89ff8fa9ae11f4d0db029c4fc5484d2980460a`
- `video-frames/face_027.jpg`  4173  `2fc5afadc5f8ee49ea02dcd46184d18501412403ff872a27d982629c8b8ae12f`
- `video-frames/face_028.jpg`  4349  `ad1db9b6964ea1ef83bb470fce2a0bef5f52579cb7f90df3c8ff4e79ac3f0858`
- `video-frames/face_029.jpg`  4240  `09ded8994bec33dac0ce4127e5354fbaf9a92ba6a6e21d743919033d675a6ad7`
- `video-frames/face_030.jpg`  4141  `ab747908aae20f49de8f3300f67688f7239cdcd60c102425e9a2e896294eef71`
- `video-frames/face_031.jpg`  4438  `2320b65b50b76a98358612ce1ef875b4fc2eb599a44c7549182d1be6af740d62`
- `video-frames/face_032.jpg`  4341  `64c6b235634517230f0326fb091a11206894249c21604ede40aa3ddfd5a6e58e`
- `video-frames/face_033.jpg`  4288  `da3460943d3267af2db320b21f722f6713ec2c31af291e5a73f5bd46648feb5b`
- `video-frames/face_034.jpg`  4465  `80e9382969aedbba22b3b89c2189f57df394e8be0cc37220b2b641d3f2f8349c`
- `video-frames/face_035.jpg`  4181  `ef14f69c5d0a822d801273e0706feac6e147237e08921ec3f3489fc2896190ed`
- `video-frames/face_036.jpg`  4317  `8e2c65450525a163c4f72896b5b63301e2cc991790b36778203409344189cdfe`
- `video-frames/face_037.jpg`  4337  `45ab5eda4f08e5b7b5ac60d21290a16de49167262cc4d1eaf3bf41dcc5963991`
- `video-frames/face_038.jpg`  4268  `4bc39dc9132124233ad96002a04d6aa6368e152135a9ada4037ff7226fbdd030`
- `video-frames/face_039.jpg`  4328  `6a54576d787e5739ab1bca16c136fcb8d590810258430484828f3402fe8708fd`
- `video-frames/face_040.jpg`  4078  `4e2cc071845abbb846f81b2f0dcfb9ab4bc670ba414ad09663997ac81c67685c`
- `video-frames/face_041.jpg`  4097  `8eed85d84c8e5abae4a5065da25de2a77726fd63312cb8f5e64092439527ca69`
- `video-frames/face_042.jpg`  4077  `d04cbbd5c21c7a36415f260d74801f7be940f33b3ef011309edfffc554009232`
- `video-frames/face_043.jpg`  3899  `39bd86e11579655dc44a270c7a9d63ac106b2335f1bc5f2f2d3525fca5e2ec00`
- `video-frames/face_044.jpg`  4129  `dbb88e4c896fb93aa42eae136ee84022c6d4c53a4b71e393c9c6acd313f0f224`
- `video-frames/face_045.jpg`  4034  `77687215d642c29ae4f6bef16156d3c4720643c029a5340029a3cfe039e49a2e`
- `video-frames/face_046.jpg`  4354  `73c4d1265c002ef419b5a33c1789095172f8578234b2c9ebcd2e77743f7e6519`
- `video-frames/face_047.jpg`  4432  `b1be57b8735e61cf1b389efca5b56177b3b78cbe3baf06360903e9f855f2bb07`
- `video-frames/face_048.jpg`  4341  `8c5c0d4d13b89379b653aea07abf264520c7aa5086228d660a52c516fa7ff7e3`
- `video-frames/face_049.jpg`  4490  `b3eda660d8c7d97cd1b347d93c8d662a7558a61afbadaf529c8aa92f7072363b`
- `video-frames/face_050.jpg`  4279  `111eb170c2d6e71d2f7b13c044365492d1e0c0edcc41b773d4727e1acecfb058`
- `video-frames/face_051.jpg`  4257  `5714359e3df61652b3e70aaf5b91f994c26270ec21aae0d2a7b18a6526c9ae2e`
- `video-frames/face_052.jpg`  4163  `98ecf23127442b58417eac6047d45831a61f91aaaf8b387892c4b14cbc8ea18d`
- `video-frames/face_053.jpg`  4214  `646afc41644b03a27244a0035265fbb88ee3076ff15b14e7093cb110e2927574`
- `video-frames/face_054.jpg`  4211  `eec6989f6efdefa863f33a51a0f019b2317c7057b58577c88d2da5ebbb443f8e`
- `video-frames/face_055.jpg`  4059  `0d902e010bec7a771b79a967fe5c6ac7dd60e1228f08f1e62ca969884b0d0b3c`
- `video-frames/frame_0.2.jpg`  39173  `a273da185cfdcd4b7a990fbfc61652b2cd70f3cf648b1221049d3b01b83af260`
- `video-frames/frame_1.5.jpg`  38257  `0822a8841ff34aead37e5651288a1265df169bcf1dc832da6502c539177df2b1`
- `video-frames/frame_10.8.jpg`  38903  `19b0c249f4059cff078f85a00b1abe8a6b6bd05ea9849dbb8e3e7d3c2b217ab9`
- `video-frames/frame_3.jpg`  41066  `10d06e488aad3e8f44e1bc8964ce55d3d550c8baadd82cf778b15413002ce305`
- `video-frames/frame_5.jpg`  38240  `1cc1a0b5c4bc43876ac87c625d6d775b5e67589d2c5c07550d4ff5e02f888a87`
- `video-frames/frame_7.jpg`  39100  `40b852692f641122a3e9b57290c0341dcdf948efea07d48e8ee88cfca40ce242`
- `video-frames/frame_9.jpg`  41520  `df3d07f7e50107389aa3b5a0fd027761e7027fd5929f199557057f6cf633793a`
- `wireguard-go-LICENSE.txt`  1023  `91276db973f25602d1aa43491f59cbc84cb88e6f151e1d0cc82a755563ce0195`
- `wireguard-go-README.md`  3913  `b71a3690a654a4ef4571564c2d740f3074e9e1730f8837499058c51960c3bd43`
- `wireguard-go-commit.json`  4284  `531b48ed38efc579e5f3e62ad9f1d2b960133a1e5404daa569bcab97418f8128`
- `wireguard-paper.pdf`  550175  `b4cf398c21d054e8774af568395b0f7cd0e2b01322809c5dbd66c4135021ca57`
