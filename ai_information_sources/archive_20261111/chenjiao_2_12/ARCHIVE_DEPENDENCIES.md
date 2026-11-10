# 公开归档与练习依赖说明

项目：七个 AI 信息入口：发现、原文与评测分工；原材料：陈娇 第2批 第12项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- 见本目录来源清单及 exercise/SOURCES.md、provenance.json、repositories.json 或 manifest.json 中的固定链接。

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `sources/AI-News.html` | `62a6e0a1c3e6fbe7eb71bacb277e21ed8fdcf62b92e725087d9fe9095df3d78c` |
| `sources/AI-News.txt` | `0172b88c2f5562e0ca04557016170b8224295736d9326685b576e52fb92f763a` |
| `sources/Arena.html` | `9266177727c2a0d808876b08de2fcb467e88c722ee1cd3aef3ba82f31c83f8f6` |
| `sources/Arena.txt` | `7a5b5e8f3533d24e0858f1ad11a450ce9a3a1341401840e757e7853a964f6672` |
| `sources/Artificial-Analysis.html` | `c9cff62f2435469a805ad0274ed8b6e97269dc89bdaf46d5cd64e1216d1b44d9` |
| `sources/Artificial-Analysis.txt` | `44b0067508f6b9a0cfaff2765135196de90d471d37f5bc7ef82fb7ffe7b24860` |
| `sources/HF-Papers.html` | `62f4aecd93f2ab155e1501f43324a0bc4b3e37fe34a0476a0f328028ebfb420d` |
| `sources/HF-Papers.txt` | `afa9a5aa5f35ab5324d0c5fc6e03baeb120f332c74a6d329cd2f6b14f754848f` |
| `sources/The-Batch.html` | `e3fddb4fa01908dafbfabee2cd2131abe5b2be5d024a96bb29b1b92586da951c` |
| `sources/The-Batch.txt` | `1c0ec78df99155061520f0ca8058a54fd7d954a0f69adbad650ab947a57b9741` |
| `sources/alphaXiv.html` | `5d6260d1d25642128b1981132b7c4ba69b6bd5f2cd3a4df682fab846cb0f0b04` |
| `sources/alphaXiv.txt` | `aeb0e2c2552c8c84e6e50835dd9c76d1e386ef22e0a539f74119ad5f4d4332e7` |
| `sources/arXiv.html` | `49e891ef70f216dbba941f3b45dfa7b3c7358f4f4fc619b6fd1ba8ed85ce3fbb` |
| `sources/arXiv.txt` | `580cd0c4114798aba9a79389a29558fd478cd3b8bb005f046d95041899e7e5db` |
| `sources/paper-2611.12865.html` | `5e0657313acf898e01016fb70f5a9469b9442c2a234d92df883a3afe9e71ed81` |
| `sources/vault-信息素养.md` | `811ed1a5f28c4ce12db3e63c9efecb450ea1c0f0dea6451e19c88019d5e81012` |
| `sources/vault-证据状态机.md` | `6716ac478a6881bff50939f58355a33b1f6ab892f71324a382aa5b9e4abe0303` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
