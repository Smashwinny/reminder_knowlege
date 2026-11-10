# 公开归档与练习依赖说明

项目：Magpie 网关：协议统一不等于权限统一；原材料：陈娇 第2批 第13项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/yetone/magpie/blob/40fbec7053ff0bcf7b3ff3e29fa8060a8e93f9db/README.md
- https://github.com/yetone/magpie/blob/40fbec7053ff0bcf7b3ff3e29fa8060a8e93f9db/docs/reference.md

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `sources/README.md` | `2a44f3dd7395260b486b080da3e1a6d3f08dea333178812cd18878356597f8cc` |
| `sources/docs_reference.md` | `fe3b744edc09e7bf328308c2d7f5640ff4f3586f6a54c47e5dcf86942a0b586a` |
| `sources/main.json` | `1f35f7d72f0f5b644ba449346165b945060bb80b2f17371eddc6c4ef6647a463` |
| `sources/vault-BYOK模型网关与用量归因.md` | `9d7527db8a7674368d6ef0abeb946bafe8549a5ca1b01d333ff2389ce020270b` |
| `sources/vault-逐轮模型路由与哨兵代理.md` | `57cb511f58204f8b70492ae0ac889c11fb193338b5a883dc915f6e45676d5e26` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
