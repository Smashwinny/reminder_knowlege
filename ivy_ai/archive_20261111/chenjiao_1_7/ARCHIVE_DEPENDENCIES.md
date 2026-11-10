# 公开归档与练习依赖说明

项目：Ivy AI：让大工作集轮流用内存；原材料：陈娇 第1批 第7项。

这份目录是 2026-11-11 的已有学习成果整理。保留作者生成的教材、原创练习和原实验日志；不把原帖全文、网页镜像、上游代码或安装包重复上传。原日志描述的是云端原始材料当时的运行结果，清理后的公开目录没有再次执行。

## 运行前先补齐材料

1. 先阅读本目录的来源清单（文件名含 sources.md）和 exercise 中的 README，核对所用版本与未验证范围。
2. 若练习读取下面列出的路径，在一个新建的学习目录中恢复它们；可从本机保留的对应原始 ZIP 取回，或按来源清单中的固定 Git 提交链接从官方上游重新下载。不要把 main 的新内容冒充当时快照。
3. 源码/模型恢复到下表给出的相对路径，并保留其 LICENSE/NOTICE。对比文件 SHA-256；在线服务返回的动态网页不能保证与旧指纹相同，无法匹配时保留“待复现”。
4. 依赖和 npm 包按原 README/锁文件另行安装；本次整理不执行安装、联网实验或硬件操作。不要把 HTML/PDF 内的旧“已含快照/离线可运行”理解为这份精简目录已包含被排除文件。

源码参考（完整上下文和其他来源以 sources.md 为准）：

- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md

## 本地原始归档中保留的排除项

| 相对路径 | SHA-256 |
|---|---|
| `exercise/upstream/LICENSE` | `230184f60bae2feaf244f10a8bac053c8ff33a183bcc365b4d8b876d2b7f4809` |
| `exercise/upstream/LICENSE.exception` | `852da0913e3c7ed52d5d5472dbc8755c3a0cb2bd5f026c15ad3c63ab77718bd4` |
| `exercise/upstream/NOTICE.md` | `ccddfe48850e80e6c34b60992cb585f22eb9d7c671cc1cb58ba07c2d573df533` |
| `exercise/upstream/THIRD_PARTY.md` | `16dd4994e385174a5412699b3e626e98e7c96e110e5d4a6f4821e51c30ebe7e9` |
| `exercise/upstream/components/story_core/include/story_arena.h` | `63f9d43eb9e6df81553d440bdb6129970ba855bb8089e21e144f2159c4bdbb56` |
| `exercise/upstream/components/story_core/include/story_log.h` | `9066e3d6eeaa31000bdc18edc7a249740ef5d600829a05c606183c8ba0c149df` |
| `exercise/upstream/components/story_core/story_arena.c` | `a5aea3d22b5706714586fc9ca5b045ff11ffece77e238de16c3dd988d1997fcb` |
| `exercise/upstream/host/check.h` | `c0a335680a271435a53a0e2a0b46444fa520f98279b564e3849c0715ac5d6bc7` |
| `exercise/upstream/host/stubs/esp_log.h` | `12bc7e0a3dce75e55f776ff115f9863ce961042f480dc0c0fdbbafe3293b6dd2` |
| `exercise/upstream/host/test_arena.c` | `a573c4b1d9043e58bb394a772a1429295308da947adfa50b7fba7d68ee288b03` |

以上路径来自对应原始项目包；部分是阅读证据，未必都是每个子命令的运行依赖。原始压缩包保留在本机私有备份，不随本次公开 Git 提交上传。
