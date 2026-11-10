# 公开归档与练习依赖说明

项目：配置能恢复， 身份不要进备份；原材料：马老师 第20261111批 第7项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/git/git/blob/a52a24e03c8c711f1d5e252fba78f9276908129b/Documentation/git-init.txt#L17-L47
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md#L47-L57
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/只读闸门三原则.md#L8-L22
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/agent_desktop/agent_desktop-小白指南.html

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `evidence/ma-laoshi-20261111-author-prompt.txt` | `968902555e233be4551e04d9b0c0833985c3dde4beeebdd909459f3246ffd131` |
| `evidence/ma-laoshi-20261111-author-replies.txt` | `9d348cde8ba0d18655ac89e4f22415a3d12288459ae7ea270d1f1773a35e1a1c` |
| `evidence/ma-laoshi-20261111-experiment-output.txt` | `f38cff89a413c9778da1fa9e9d3b50bfc789e14010942c543facbc5d832404d8` |
| `evidence/ma-laoshi-20261111-git-init.txt` | `40488c060552855a71750fabfe6bf37bccc27b32d247a073007f1146b0705d9e` |
| `evidence/ma-laoshi-20261111-page-1.png` | `8f39b0acca5b60fac95a00bf3482c956623a9997db4c54e6857b7c95c5d34b0e` |
| `evidence/ma-laoshi-20261111-page-2.png` | `0375a50933c099fb03c1717194cb182f4b6cff5e43f6cd5a6ad0dd0bc1451839` |
| `evidence/ma-laoshi-20261111-page-3.png` | `da8b78bf49b4a82e585da9355028ad8c4cd8fc5458ef4d688fe3669bd12629e2` |
| `evidence/ma-laoshi-20261111-page-4.png` | `727d39cfd0c1059860415b8355c7949ad9303d650cbf546ed555bb41cd6f1a5b` |
| `evidence/ma-laoshi-20261111-page-5.png` | `ccd0b7a24b74aa8ae936c1c9ec60bb9eac9f64a3c951bf3ea76fb708e10f425d` |
| `evidence/ma-laoshi-20261111-page-6.png` | `507ecca90d9286d6f2155159c0a78c527ec81651bbf34b81ae3ce19e2c251d83` |
| `evidence/ma-laoshi-20261111-page-7.png` | `f12550e9a19b0c1c8f9699dd15101620002127a78fe193a1482fd454af63d520` |
| `evidence/ma-laoshi-20261111-page-8.png` | `b55f4e2d54ec52ed1fc7ae76c6d8d2b9ce57a6b690b064127626d8cf15a2e5a0` |
| `evidence/ma-laoshi-20261111-post.txt` | `9580fe68f6c25e34dba185a86bdad2aa6db3d11bca93489b4daf8b20efdb024c` |
| `evidence/ma-laoshi-20261111-print-log.txt` | `7a78f161548ff7106e23da4a2e0e825276ed935b6df73a6372c85392f787585b` |
| `evidence/ma-laoshi-20261111-render-log.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `evidence/ma-laoshi-20261111-replies-last-page.txt` | `17039f8fb10e10142550002e434529e5257c93ae0e2348bf9a415b9b30e1f322` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
