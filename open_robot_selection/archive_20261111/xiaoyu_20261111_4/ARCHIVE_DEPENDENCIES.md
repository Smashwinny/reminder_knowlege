# 公开归档与练习依赖说明

项目：开源机器人筛选；原材料：小钰 第20261111批 第4项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- 见本目录来源清单及 exercise/SOURCES.md、provenance.json、repositories.json 或 manifest.json 中的固定链接。

`agibot` 子命令读取原始包外的来源统计。缺少来源文件时它应报告 missing；本归档不补造原始数据或声称再次验证 8259/2 统计。

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `exercise/models/open_manipulator_x.urdf` | `784078c2a5bb16accd2ca4cbcf0d340403d6d343f047b433b503aeae85ef17d3` |
| `exercise/models/so100.urdf` | `f7050417ebbb79358f113ddd4bca2b457b2c6d5048193331db5a04a0066439ed` |
| `exercise/models/so101_new_calib.urdf` | `3a65d2d35e68a8d2f0c2cc176d19b884506543c93ba72980145b80abe276022c` |
| `exercise/models/so101_new_calib.xml` | `d75253eb568e8a7214db9c631ab7bed4217f608a26f7276ebe9a7636cac82580` |
| `exercise/models/turtlebot3_burger.urdf` | `bc453d08d6a3f2da1530201a15807edafffa5158c291dc40f5edb19ae35ca603` |
| `exercise/models/turtlebot3_common_properties.urdf` | `12c424e353b6ee75ad5287b78b16991f73d874d565570c58f4e766e07cb4de55` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
