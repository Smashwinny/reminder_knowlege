# 公开归档版依赖恢复说明

本次公开整理移除了第三方源码、模板及上游说明书副本；原始ZIP仍在本地归档，原创驱动、教学代码、测试和既有结果保留。许可证/NOTICE仅说明来源及条件，不代表源码仍随包提供。

**本轮没有下载依赖、重新执行实验或重新学习；不能宣称清理后的目录直接可运行或已通过复现。** 原HTML/PDF/实验日志及README中的命令描述的是当时完整实验包，公开版需先恢复下表依赖，并检查原README的运行环境和其他外部依赖。不要把历史成功记录当作新环境运行结果。

## 已记录的一手版本

仓库：[garycaogan/ai-live-avatar](https://github.com/garycaogan/ai-live-avatar)  
固定提交：`dc87db8ad53fb81cfe07dcac08215497dfa1a50d`（[固定树](https://github.com/garycaogan/ai-live-avatar/tree/dc87db8ad53fb81cfe07dcac08215497dfa1a50d)）。

版本和路径来自已经保存的sources.md、实验清单/许可与原ZIP，不是本轮重新连接上游的结果。SHA256是从原交付包逐字节计算的预期内容哈希。

## 恢复方法（说明，未执行）

1. 将上述公开仓库的固定提交取回另一个隔离的依赖目录，不把完整上游或.git纳入学习仓库。
2. 以该提交的仓库根为起点读取下表“上游相对路径”；仅将必要文件恢复到本项目archive_20261111下的“练习相对路径”。保留原许可证、署名与第三方条件。
3. 对每个恢复文件计算SHA256并与表中比较。路径不可得或哈希不符时停止恢复、保留差异，不用最新main替代，也不覆盖原创练习。
4. 本说明只交代缺失依赖；没有执行这些步骤，没有确认网络可达/重新取回字节，也没有承诺跨系统或新环境的复现。

| 练习相对路径（恢复位置） | 固定仓库内相对路径 | 原交付字节SHA256 |
|---|---|---|
| `exercise/vendor/live/__init__.py` | `live/__init__.py` | `f0be05b3c775c20a0e2b2f0e56d53e51ee314442aac8746c8b0885799ad4bf26` |
| `exercise/vendor/live/moderation.py` | `live/moderation.py` | `8a8277370823ab29f2a0de80a00fb6c651eb50916476887e2291ad863483674e` |
| `exercise/vendor/live/queue.py` | `live/queue.py` | `c89d755cf4e8ccea71e1afe8f627b7f573b4a08de16f1d539b6c431230431b91` |
| `exercise/vendor/live/router.py` | `live/router.py` | `5c7a6d88ae808851765cdd961ac1e1425b1991e0eafce8f95eb63fd023519853` |
| `exercise/vendor/live/session.py` | `live/session.py` | `9bc34ecfc1a10487a48e43b58a0ee14f5d318a051e7eef639ea5bdc2da2462cf` |
| `exercise/vendor/moderation.json` | `moderation.json` | `8182f5d91d33c1810aa762c84787f37cd56527d92f9260a5ee9124a22f17498e` |
| `exercise/vendor/tests/__init__.py` | `tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `exercise/vendor/tests/test_logic.py` | `tests/test_logic.py` | `4a7f6c8031ea33d38226f36ede3331cec209be5eed083a575891a668fd0d6e93` |
