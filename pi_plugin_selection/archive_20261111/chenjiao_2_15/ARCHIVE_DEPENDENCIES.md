# 公开归档与练习依赖说明

项目：Pi 五类插件：选能力，不按下载量闭眼装；原材料：陈娇 第2批 第15项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/nicobailon/pi-mcp-adapter/blob/0beff98460567cd228ae08d99db5f169a1ad3034/README.md
- https://github.com/nicobailon/pi-subagents/blob/52e68e9ef0e563d5c97b28519f9999f1b5fbbbea/README.md
- https://github.com/nicobailon/pi-web-access/blob/322e44fafc1aaa691779cdf2116584e67edd7645/README.md
- https://github.com/ranxianglei/billion-context/blob/133f3525c628c4b959bb79ece82af6df82e131a3/README.md
- https://github.com/juicesharp/rpiv-mono/tree/ce6d3530410812ca504ec294995581a52170f9e1/packages/rpiv-ask-user-question
- https://github.com/earendil-works/pi/blob/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/coding-agent/docs/compaction.md

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `sources/billion-context-README.md` | `85a1ba5e1a3721b63466f5a5a63aee63224fe28072c0ff85dda21f672d0a2622` |
| `sources/billion-context.json` | `2267c84326acb2216a3880ab0171427c0949dbc71e545cdb1f0730205aaad984` |
| `sources/main.json` | `82c50f29ba9b7898af38f35e006e78693ec420fb4adb80d359c28d8860f2e344` |
| `sources/official.html` | `bd81e3a8ddad09d1866440bceb2a90ac5d234da235689c07d2045162dd7b3651` |
| `sources/pi-compaction.md` | `b5b23d10bb86d8ab32b67f80a7e57febd953222c6da6fd422ae91d232ef28faf` |
| `sources/pi-mcp-adapter-README.md` | `089700b205b51ca89a91ba95ecd58bd3540def55fbc18e7232b7ca4c3ce1f622` |
| `sources/pi-mcp-adapter.json` | `002b549cf49af1875c0181652b3bfdd46110bfa949af6a88c1b899be9b0e485a` |
| `sources/pi-subagents-README.md` | `5ecd91ff4eb56b283ff78d68e206fdc07898ceede1a074d22982b56b562ac3b9` |
| `sources/pi-subagents.json` | `d3df4b781c5a08166502f196f9e8d8b50a6663e543cdc626ca504f6ad0f5a041` |
| `sources/pi-web-access-README.md` | `732dd49b983a365f3240f42cdbe129e08eae930fda12147e426a9c7576eae891` |
| `sources/pi-web-access.json` | `c71c5430150e7e0f49ffb4f587a1a94c3cb17582d241e91384122affc8d7c2cc` |
| `sources/question-README.md` | `26cf26c2bd4a82803fed0277ede6bb947521be718ca6c0864cacef28deb130c2` |
| `sources/scoped-question.json` | `4bc4ba1e2f54dac001f7bc320b024459c3f72e338e1fc451179dace4921df921` |
| `sources/vault-Compaction上下文压缩算法.md` | `65343c4cd9aa2dc1e9e1b02c092223bfa6d884280ac95d4c183b09ed340cb8c6` |
| `sources/vault-工具目录膨胀.md` | `e50d628163a1ef8c94ef6e940742fbe16aca7852fcfd5571f9b467ed53932515` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
