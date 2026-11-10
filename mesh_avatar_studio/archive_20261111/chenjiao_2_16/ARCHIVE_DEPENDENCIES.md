# 公开归档与练习依赖说明

项目：Mesh Avatar Studio：一张图到分层网格底稿；原材料：陈娇 第2批 第16项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/shinshin86/mesh-avatar-studio/blob/3619620266740236327debfcf327f898a99dd7b3/README.md
- https://github.com/shinshin86/mesh-avatar-studio/blob/3619620266740236327debfcf327f898a99dd7b3/docs/format.md
- https://github.com/shinshin86/mesh-avatar-studio/blob/3619620266740236327debfcf327f898a99dd7b3/packages/runtime/README.md

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `sources/README.md` | `c831b47ebf32acf159ca9b8ecd806729601e555b644949f9e9a6cefbbd706d5d` |
| `sources/docs_agent-guide.md` | `f25d90b6ce7853fc372b479be811cb49ef4bfee10b81ffaf775fc9ceddd8952d` |
| `sources/docs_format.md` | `b20ad32283f569926b89813e86925d305d5cb43847765eed2b23322d7c377736` |
| `sources/main.json` | `c993464ad761006fe5922e6e3f4bd00ad842851bc67488be6747884b226a5183` |
| `sources/packages_runtime_README.md` | `291a1c842fdd302b1e2c2f3e1920fdff8a7a4400289f4b65a1886c2b6932f374` |
| `sources/packages_runtime_package.json` | `ea8e0515c3067a710056e89b988a582928c7043ed131dc58234d970b3a3b3ffe` |
| `sources/vault-内容型开源与双许可.md` | `37a76743f06d6bc1248c21d08a7e459b3cf588df93fc59db0f1db77ee54c27b2` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
