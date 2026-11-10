# 公开归档版依赖恢复说明

本次公开整理移除了第三方源码、模板及上游说明书副本；原始ZIP仍在本地归档，原创驱动、教学代码、测试和既有结果保留。许可证/NOTICE仅说明来源及条件，不代表源码仍随包提供。

**本轮没有下载依赖、重新执行实验或重新学习；不能宣称清理后的目录直接可运行或已通过复现。** 原HTML/PDF/实验日志及README中的命令描述的是当时完整实验包，公开版需先恢复下表依赖，并检查原README的运行环境和其他外部依赖。不要把历史成功记录当作新环境运行结果。

## 已记录的一手版本

仓库：[amontlabs/lcu](https://github.com/amontlabs/lcu)  
固定提交：`a7e30c1862707214dfe748d410854771ab4f4494`（[固定树](https://github.com/amontlabs/lcu/tree/a7e30c1862707214dfe748d410854771ab4f4494)）。

版本和路径来自已经保存的sources.md、实验清单/许可与原ZIP，不是本轮重新连接上游的结果。SHA256是从原交付包逐字节计算的预期内容哈希。

## 恢复方法（说明，未执行）

1. 将上述公开仓库的固定提交取回另一个隔离的依赖目录，不把完整上游或.git纳入学习仓库。
2. 以该提交的仓库根为起点读取下表“上游相对路径”；仅将必要文件恢复到本项目archive_20261111下的“练习相对路径”。保留原许可证、署名与第三方条件。
3. 对每个恢复文件计算SHA256并与表中比较。路径不可得或哈希不符时停止恢复、保留差异，不用最新main替代，也不覆盖原创练习。
4. 本说明只交代缺失依赖；没有执行这些步骤，没有确认网络可达/重新取回字节，也没有承诺跨系统或新环境的复现。

| 练习相对路径（恢复位置） | 固定仓库内相对路径 | 原交付字节SHA256 |
|---|---|---|
| `exercise/vendor/adapters/host-guard.mjs` | `adapters/host-guard.mjs` | `5b8360ae81517ae15277d564fff32b4195e350becba0880b6e98c8d84ddc01bc` |
| `exercise/vendor/adapters/test/host-guard.test.mjs` | `adapters/test/host-guard.test.mjs` | `e954ce902ac762d7a178e73eae3f42ad2f454e64ccd85d3fb23e2db7825fe9bc` |
| `exercise/vendor/tests/mcp_client.py` | `tests/mcp_client.py` | `014d97a4a7b760f7aa7584f0e8aec861979904f84fc23be73855f524ff2360eb` |
